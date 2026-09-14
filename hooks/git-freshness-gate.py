#!/usr/bin/env python3
"""
Git Freshness Gate — PreToolUse (Bash) hook.

Hard-blocks `git commit` and `git push` when the target repo is BEHIND its
upstream, so Claude can never build history on a stale base in a multi-machine
setup. Surgical scope: only commit/push are gated; every other command (reads,
edits, pulls, status, other Bash) flows freely.

Why gate at commit, not just push: in a --ff-only workflow the divergence that
forces a merge/rebase is created the moment you commit on a stale base. A
rejected push is non-destructive but too late — the messy history already exists.

Contract: exit 2 blocks the tool call and feeds stderr back to Claude; exit 0
allows. Fail-OPEN on every ambiguity (can't resolve repo, no upstream, offline,
fetch timeout) — blocking real work is worse than the rare miss.

"""

import json
import os
import shlex
import subprocess
import sys
import time

FETCH_THROTTLE_S = 120   # skip fetch if the stamp is fresher than this
FETCH_TIMEOUT_S = 8      # give up on a slow/offline fetch and fail open
GIT_TIMEOUT_S = 5        # local git plumbing calls


def is_git(token):
    """True if a token invokes git (git, /usr/bin/git, \\git, etc.)."""
    return token == 'git' or os.path.basename(token.lstrip('\\')) == 'git'


def split_segments(tokens):
    """Split a token list into command segments on shell operators."""
    segments, current = [], []
    for tok in tokens:
        if tok in ('&&', '||', ';', '|', '&'):
            if current:
                segments.append(current)
            current = []
        else:
            current.append(tok)
    if current:
        segments.append(current)
    return segments


def parse_git_segment(seg):
    """
    Given one segment's tokens, if it's a git commit/push return
    (subcommand, repo_dir_override_or_None). Otherwise return None.

    Handles global options that precede the subcommand, notably `-C <path>`
    (the repo override) and `-c <cfg>` (skip its arg). The first non-option
    token after `git` is the subcommand.
    """
    if not seg or not is_git(seg[0]):
        return None

    repo_override = None
    i = 1
    while i < len(seg):
        tok = seg[i]
        if tok == '-C':                       # repo dir override
            repo_override = seg[i + 1] if i + 1 < len(seg) else None
            i += 2
            continue
        if tok.startswith('-C') and len(tok) > 2:   # -C<path>
            repo_override = tok[2:]
            i += 1
            continue
        if tok == '-c':                       # config override: skip its arg
            i += 2
            continue
        if tok.startswith('-'):               # other global flag (-P, --no-pager, ...)
            i += 1
            continue
        # first bare token is the subcommand
        if tok in ('commit', 'push'):
            return (tok, repo_override)
        return None
    return None


def find_gated_target(command, base_cwd):
    """
    Walk the whole command. Return (subcommand, repo_dir) for the first
    commit/push found, resolving repo dir from `-C`, a running `cd`, or cwd.
    Return None if no commit/push present.
    """
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None

    cwd = base_cwd
    for seg in split_segments(tokens):
        # A `cd <path>` segment shifts cwd for later segments in the chain.
        if seg and seg[0] == 'cd' and len(seg) >= 2 and not seg[1].startswith('-'):
            cwd = os.path.abspath(os.path.join(cwd, os.path.expanduser(seg[1])))
            continue
        parsed = parse_git_segment(seg)
        if parsed:
            subcmd, override = parsed
            if override:
                repo_dir = os.path.abspath(os.path.join(cwd, os.path.expanduser(override)))
            else:
                repo_dir = cwd
            return (subcmd, repo_dir)
    return None


def git(args, cwd, timeout=GIT_TIMEOUT_S):
    """Run a git command, return stripped stdout or None on any failure."""
    try:
        r = subprocess.run(['git', '-C', cwd, *args],
                           capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def main():
    data = json.load(sys.stdin)
    command = data.get('tool_input', {}).get('command', '')
    if not command:
        sys.exit(0)

    # Fail fast when offline / keys missing instead of waiting out the full
    # fetch timeout. setdefault so a user's own GIT_SSH_COMMAND wins.
    os.environ.setdefault('GIT_SSH_COMMAND',
                          'ssh -o ConnectTimeout=5 -o BatchMode=yes')

    base_cwd = os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
    target = find_gated_target(command, base_cwd)
    if target is None:
        sys.exit(0)                     # no commit/push in this command
    subcmd, repo_dir = target

    toplevel = git(['rev-parse', '--show-toplevel'], repo_dir)
    if not toplevel:
        sys.exit(0)                     # not a git repo → fail open

    # Throttled fetch, stamped inside .git (machine-local, never tracked).
    git_dir = git(['rev-parse', '--absolute-git-dir'], toplevel) \
        or os.path.join(toplevel, '.git')
    stamp = os.path.join(git_dir, '.claude-fetch-stamp')
    fresh = False
    try:
        fresh = (time.time() - os.path.getmtime(stamp)) < FETCH_THROTTLE_S
    except OSError:
        fresh = False
    if not fresh:
        fetched = git(['fetch', '--quiet'], toplevel, timeout=FETCH_TIMEOUT_S)
        if fetched is None:
            sys.exit(0)                 # offline / fetch failed → fail open
        try:
            with open(stamp, 'w'):
                pass
        except OSError:
            pass                        # stamp is best-effort throttle only

    # Compare against upstream; fall back to origin/main.
    behind = git(['rev-list', '--count', 'HEAD..@{u}'], toplevel)
    ahead = git(['rev-list', '--count', '@{u}..HEAD'], toplevel)
    if behind is None:
        behind = git(['rev-list', '--count', 'HEAD..origin/main'], toplevel)
        ahead = git(['rev-list', '--count', 'origin/main..HEAD'], toplevel)
    if behind is None:
        sys.exit(0)                     # no upstream to compare → fail open

    try:
        behind_n = int(behind)
        ahead_n = int(ahead) if ahead is not None else 0
    except ValueError:
        sys.exit(0)

    if behind_n == 0:
        sys.exit(0)                     # up to date (or purely ahead) → allow

    repo_name = os.path.basename(toplevel)
    print('🔒 BLOCKED: git freshness gate', file=sys.stderr)
    print('', file=sys.stderr)
    print(f'{repo_name} is {behind_n} commit(s) behind origin — '
          f'{subcmd} on a stale base would diverge your history.', file=sys.stderr)
    print('', file=sys.stderr)
    if ahead_n == 0:
        print(f'Fix: git -C {toplevel} pull --ff-only   (clean fast-forward), '
              f'then re-run.', file=sys.stderr)
    else:
        print(f'Fix: branches diverged ({ahead_n} ahead, {behind_n} behind) — '
              f'--ff-only will refuse. Run: git -C {toplevel} pull --rebase, '
              f'then re-run.', file=sys.stderr)
    sys.exit(2)


if __name__ == '__main__':
    main()

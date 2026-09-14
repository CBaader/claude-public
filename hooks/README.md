# Claude Code Hooks

Three hooks from daily use. Two guard shell commands before they run (`PreToolUse` on `Bash`); one adds a reminder when a prompt asks for a checkable fact (`UserPromptSubmit`).

| Hook | Event | What it does |
|------|-------|--------------|
| `dangerous-command-blocker.py` | PreToolUse / Bash | Blocks catastrophic commands, protects uncommitted work, warns on suspicious patterns |
| `git-freshness-gate.py` | PreToolUse / Bash | Blocks `git commit` and `git push` when the repo is behind its upstream |
| `verify-facts-reminder.py` | UserPromptSubmit | Injects a "do not answer from memory" reminder when the prompt asks for a live fact |

## How a hook talks to Claude Code

- Claude Code runs the command with the event payload as JSON on stdin. A `Bash` `PreToolUse` payload carries `tool_name` and `tool_input.command`; a `UserPromptSubmit` payload carries `prompt`.
- Exit 0 allows the action. Exit 2 blocks it and feeds the hook's stderr back to Claude as the reason. Exit 1 is a non-blocking error: the action proceeds, so a policy hook must use exit 2.
- JSON on stdout with `hookSpecificOutput.additionalContext` injects text into Claude's context on exit 0. Plain stdout does the same with less control.

Reference: https://code.claude.com/docs/en/hooks

## Installation

1. Copy the scripts to your Claude hooks directory:

```bash
mkdir -p ~/.claude/hooks
cp *.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py
```

2. Wire them in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/dangerous-command-blocker.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/git-freshness-gate.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/verify-facts-reminder.py"
          }
        ]
      }
    ]
  }
}
```

Take only the hooks you want; each entry is independent.

## dangerous-command-blocker.py

Multi-level protection that blocks or warns about dangerous shell commands before execution.

### Protection Levels

| Level | Action | What it catches |
|-------|--------|-----------------|
| 0 - Uncommitted work | Blocks | `rm` on files with staged/unstaged/untracked changes in git repos |
| 1 - Catastrophic | Blocks | `rm -rf /`, `dd if=`, fork bombs, `chmod 777 /`, remote code execution pipes |
| 2 - Critical paths | Blocks | `rm .git/`, `rm .env`, `rm package.json`, `mv` to `/dev/null` |
| 3 - Suspicious | Warns | `rm && chained`, wildcards, `find -delete`, `xargs rm` |

### How Level 0 Works

Before any `rm` command, the hook:
1. Extracts file targets from the command (handles flags, paths, wildcards)
2. For each target, runs `git status --porcelain` to check for uncommitted changes
3. Blocks if any file has staged changes, unstaged modifications, or is untracked

This prevents accidental deletion of work that has not been committed yet.

### Test

```bash
# This should be blocked:
claude -p "run: rm -rf /"
```

### Bypassing

If you need to run a blocked command intentionally:
- Run it manually in your terminal (outside Claude Code)
- Or temporarily remove the hook from settings.json

Level 1 also catches `curl ... | python3` and `curl ... | sh`. If you genuinely need a pipe like that, write the script to a file first and run the file.

## git-freshness-gate.py

Hard-blocks `git commit` and `git push` when the target repo is behind its upstream. Everything else flows freely: reads, edits, pulls, status, other Bash.

**Why gate at commit, not just push.** In a fast-forward-only workflow the divergence that later forces a merge or rebase is created the moment you commit on a stale base. A rejected push is non-destructive but too late; the messy history already exists. On a machine you share with other sessions, or across several machines syncing through git, this is the single most common way history goes wrong.

How it works:
- Parses the command, including `git -C <dir>`, `cd <dir> && git ...` chains and global flags, to find the first `commit` or `push` and the repo it targets.
- Fetches with a 120-second throttle (a stamp file inside `.git`, never tracked) and an 8-second timeout.
- Compares `HEAD` against `@{u}`, falling back to `origin/main`.
- Fails **open** on every ambiguity: not a repo, no upstream, offline, fetch timeout. Blocking real work is worse than the rare miss.
- On a block, prints the exact fix: `git pull --ff-only` when the branch is only behind, `git pull --rebase` when it has diverged.

Uses `CLAUDE_PROJECT_DIR` as the base directory when Claude Code sets it, otherwise the current working directory.

### Test

In a repo that is behind its remote, ask Claude to commit. You should see:

```
🔒 BLOCKED: git freshness gate

<repo> is 2 commit(s) behind origin — commit on a stale base would diverge your history.

Fix: git -C /path/to/repo pull --ff-only   (clean fast-forward), then re-run.
```

## verify-facts-reminder.py

When a prompt looks like it is asking for a live, checkable fact, the hook injects a one-line reminder to run the tool first (`date` for the time, read the file, the CLI, the relevant doc) instead of answering from memory. Categories: time, date, price or cost, file contents, library or API version.

Triggers are deliberately generous. A false positive costs one injected line; a false negative is the fabricated-fact failure the hook exists to prevent. The hook never blocks and never errors: any parse failure exits 0 silently.

Pair it with a rule in your `CLAUDE.md` that says the same thing. The rule sets the standard; the hook fires it at the moment of action, when a session-start instruction may already have scrolled out of attention.

### Test

```bash
echo '{"prompt":"what time is it"}' | python3 verify-facts-reminder.py
# prints a JSON object with hookSpecificOutput.additionalContext

echo '{"prompt":"refactor the parser"}' | python3 verify-facts-reminder.py
# prints nothing
```

## Requirements

- Python 3.7+ (standard library only)
- git on PATH (for Level 0 of the blocker and for the freshness gate)

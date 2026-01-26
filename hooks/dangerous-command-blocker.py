#!/usr/bin/env python3
"""
Dangerous Command Blocker Hook
Multi-level security system for blocking dangerous shell commands
"""

import glob
import json
import os
import re
import shlex
import subprocess
import sys


def is_command(token, command_names):
    """
    Check if a token represents one of the given commands.
    Handles: rm, /bin/rm, /usr/bin/rm, \rm, etc.
    """
    if isinstance(command_names, str):
        command_names = (command_names,)

    # Exact match
    if token in command_names:
        return True

    # Backslash-escaped (e.g., \rm to bypass aliases)
    if token.lstrip('\\') in command_names:
        return True

    # Absolute/relative path (e.g., /bin/rm, ./rm, ../bin/rm)
    basename = os.path.basename(token)
    if basename in command_names:
        return True

    return False


# Load command from stdin
data = json.load(sys.stdin)
cmd = data.get('tool_input', {}).get('command', '')

# === LEVEL 0: UNCOMMITTED WORK PROTECTION ===
# Block rm on files with uncommitted changes in git repos

def extract_command_targets(command, command_names):
    """
    Extract file paths from a command (rm, mv, etc.).

    Note: Naturally handles sudo/doas/env prefixes because we scan all tokens
    looking for the command name, not just the first token.
    e.g., 'sudo -u root rm -rf /tmp/foo' -> finds 'rm', extracts '/tmp/foo'
    """
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []

    targets = []
    in_cmd = False
    end_of_flags = False

    for token in tokens:
        if is_command(token, command_names):
            in_cmd = True
            end_of_flags = False
            continue
        if in_cmd:
            if token == '--':
                end_of_flags = True
                continue
            if token.startswith('-') and not end_of_flags:
                continue
            if token in ('&&', '||', ';', '|'):
                in_cmd = False
                end_of_flags = False
                continue
            targets.append(token)

    return targets

def check_git_status(filepath):
    """
    Check if a file has uncommitted changes.
    Returns: (is_in_git_repo, has_uncommitted_changes, status_description)

    Note: TOCTOU race exists between this check and actual rm execution.
    Acceptable risk for a pre-command hook - the window is milliseconds.
    """
    # Resolve to absolute path
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)

    # Check if path exists (rm on non-existent files is fine)
    if not os.path.exists(filepath):
        return (False, False, 'does not exist')

    # Get directory for git commands
    if os.path.isdir(filepath):
        check_dir = filepath
    else:
        check_dir = os.path.dirname(filepath)

    # Check if we're in a git repo
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=check_dir,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return (False, False, 'not in git repo')
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return (False, False, 'git check failed')

    # Check file status with git status --porcelain
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain', '--', filepath],
            cwd=check_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        status_output = result.stdout.strip()

        if status_output:
            # File has some git status (modified, staged, untracked, etc.)
            status_code = status_output[:2] if len(status_output) >= 2 else status_output

            status_meanings = {
                'M ': 'staged modifications',
                ' M': 'unstaged modifications',
                'MM': 'staged and unstaged modifications',
                'A ': 'staged new file',
                'AM': 'staged new file with modifications',
                '??': 'untracked file',
                'D ': 'staged deletion',
                ' D': 'unstaged deletion',
                'R ': 'renamed',
                'C ': 'copied',
            }

            desc = status_meanings.get(status_code, f'uncommitted changes ({status_code})')
            return (True, True, desc)

        # No output means file is clean/committed or ignored
        # Double-check it's actually tracked
        result = subprocess.run(
            ['git', 'ls-files', '--', filepath],
            cwd=check_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stdout.strip():
            # File is tracked and clean
            return (True, False, 'committed and clean')
        else:
            # File is not tracked (probably ignored or outside repo)
            return (True, False, 'not tracked by git')

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return (False, False, 'git status check failed')

def check_uncommitted_protection(command):
    """Check if rm command targets files with uncommitted work."""
    if not re.search(r'\brm\b', command):
        return None  # Not an rm command

    targets = extract_command_targets(command, 'rm')
    if not targets:
        return None

    uncommitted_files = []

    for target in targets:
        # Skip obvious non-file patterns
        if target in ('*', '.', '..'):
            continue

        # Handle wildcards - expand and check each matched file
        if '*' in target or '?' in target or '[' in target:
            dir_path = os.path.dirname(target) or '.'
            if os.path.isdir(dir_path):
                try:
                    # Expand the glob pattern
                    expanded = glob.glob(target)
                    if expanded:
                        # Check each matched file
                        for expanded_path in expanded:
                            is_in_repo, has_uncommitted, status = check_git_status(expanded_path)
                            if is_in_repo and has_uncommitted:
                                uncommitted_files.append((expanded_path, status))
                    else:
                        # No matches - check if we're in a git repo anyway (conservative)
                        result = subprocess.run(
                            ['git', 'rev-parse', '--git-dir'],
                            cwd=dir_path,
                            capture_output=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            uncommitted_files.append((target, 'wildcard pattern in git repo (no current matches)'))
                except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
                    pass
            continue

        is_in_repo, has_uncommitted, status = check_git_status(target)

        if is_in_repo and has_uncommitted:
            uncommitted_files.append((target, status))

    return uncommitted_files if uncommitted_files else None

# Run uncommitted work check
uncommitted = check_uncommitted_protection(cmd)
if uncommitted:
    print(f'🛡️  BLOCKED: Uncommitted work protection!', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'The following files have uncommitted changes:', file=sys.stderr)
    for filepath, status in uncommitted:
        print(f'  • {filepath} ({status})', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'Command: {cmd[:100]}', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'To proceed, either:', file=sys.stderr)
    print(f'  1. Commit your changes first: git add <file> && git commit', file=sys.stderr)
    print(f'  2. Stash your changes: git stash', file=sys.stderr)
    print(f'  3. Run the command manually in your terminal if intentional', file=sys.stderr)
    sys.exit(2)

# === LEVEL 1: CATASTROPHIC COMMANDS (ALWAYS BLOCK) ===
# Regex patterns for non-path-based checks
catastrophic_patterns = [
    (r'\b(dd\s+if=|dd\s+of=/dev)', 'dd disk operations'),
    (r'\b(mkfs\.|mkswap\s|fdisk\s)', 'filesystem formatting'),
    (r'\b:(\(\))?\s*\{\s*:\s*\|\s*:\s*&\s*\}', 'fork bomb'),
    (r'>\s*/dev/sd[a-z]', 'direct disk write'),
    (r'\bchmod\s+(-R\s+)?777\s+/', 'chmod 777 on root'),
    (r'\bchown\s+(-R\s+)?.*\s+/$', 'chown on root directory'),
    # Subshell/command execution bypasses
    (r'\b(bash|sh|zsh|dash)\s+(-c\s+)?["\'].*\brm\s', 'rm inside subshell'),
    # Remote code execution (sudo/doas prefix handled explicitly)
    (r'\b(curl|wget)\b.*\|\s*((sudo|doas)\s+)?(bash|sh|zsh|dash|python|perl|ruby)', 'remote code execution via pipe'),
    (r'\b(curl|wget)\b.*-[oO]\s*-.*\|\s*((sudo|doas)\s+)?(bash|sh)', 'remote code execution via pipe'),
]

for pattern, desc in catastrophic_patterns:
    if re.search(pattern, cmd, re.IGNORECASE):
        print(f'❌ BLOCKED: Catastrophic command detected!', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'Reason: {desc}', file=sys.stderr)
        print(f'Command: {cmd[:100]}', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'This command could cause IRREVERSIBLE system damage or data loss.', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'Safety tips:', file=sys.stderr)
        print(f'  • Never use rm -rf with /, ~, or * wildcards', file=sys.stderr)
        print(f'  • Avoid recursive operations on system directories', file=sys.stderr)
        print(f'  • Use specific file paths instead of wildcards', file=sys.stderr)
        print(f'  • For cleanup, target specific directories: rm -rf /tmp/myproject', file=sys.stderr)
        sys.exit(2)

# Path-based catastrophic checks using parsed tokens (handles quoted paths)
def check_catastrophic_rm_targets(command):
    """Check rm targets for catastrophic paths using parsed tokens."""
    if not re.search(r'\brm\b', command):
        return None

    targets = extract_command_targets(command, 'rm')
    for target in targets:
        # Normalise path for comparison
        normalised = os.path.normpath(os.path.expanduser(target))

        # Root directory
        if normalised == '/' or target == '/':
            return 'rm on root directory'

        # Home directory
        if normalised == os.path.expanduser('~') or target == '~':
            return 'rm on home directory'

        # Bare wildcard (just * or patterns like /*)
        if target == '*' or target.endswith('/*') or normalised == '/*':
            return 'rm with dangerous wildcard'

        # Wildcard at root level
        if target.startswith('/*') or target.startswith('/tmp/../*'):
            return 'rm with root-level wildcard'

    return None

catastrophic_reason = check_catastrophic_rm_targets(cmd)
if catastrophic_reason:
        print(f'❌ BLOCKED: Catastrophic command detected!', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'Reason: {catastrophic_reason}', file=sys.stderr)
        print(f'Command: {cmd[:100]}', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'This command could cause IRREVERSIBLE system damage or data loss.', file=sys.stderr)
        sys.exit(2)

# === LEVEL 2: CRITICAL PATH PROTECTION ===
# Protected paths/filenames and their descriptions
CRITICAL_PATHS = {
    # Directories (checked as path component)
    '.claude': 'Claude Code configuration',
    '.git': 'Git repository',
    'node_modules': 'Node.js dependencies',
    # Files (checked as basename or suffix)
    '.env': 'Environment variables',
    'package.json': 'Package manifest',
    'package-lock.json': 'Lock file',
    'yarn.lock': 'Yarn lock file',
    'Cargo.toml': 'Rust manifest',
    'go.mod': 'Go module file',
    'requirements.txt': 'Python dependencies',
    'Gemfile': 'Ruby dependencies',
    'Gemfile.lock': 'Ruby lock file',
    'composer.json': 'PHP dependencies',
}

def check_critical_paths(command):
    """Check if command targets critical paths using parsed tokens."""
    if not re.search(r'\b(rm|mv)\b', command):
        return None

    targets = extract_command_targets(command, ('rm', 'mv'))

    for target in targets:
        # Get basename and normalised path
        basename = os.path.basename(target.rstrip('/'))
        normalised = os.path.normpath(target)
        path_parts = normalised.split(os.sep)

        for protected, description in CRITICAL_PATHS.items():
            # Check if protected path is a component of the path
            if protected in path_parts:
                return (target, description)
            # Check basename match
            if basename == protected:
                return (target, description)
            # Check suffix match for dotfiles (e.g., .env, .env.local)
            if protected.startswith('.') and basename.endswith(protected):
                return (target, description)

    return None

critical_match = check_critical_paths(cmd)
if critical_match:
    target, desc = critical_match
    print(f'🛑 BLOCKED: Critical path protection activated!', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'Protected resource: {desc}', file=sys.stderr)
    print(f'Target: {target}', file=sys.stderr)
    print(f'Command: {cmd[:100]}', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'This path contains critical project files that should not be deleted accidentally.', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'If you really need to modify this:', file=sys.stderr)
    print(f'  1. Disable the hook temporarily in ~/.claude/settings.json', file=sys.stderr)
    print(f'  2. Execute the command manually in your terminal', file=sys.stderr)
    print(f'  3. Or modify specific files instead of using rm/mv on entire directories', file=sys.stderr)
    sys.exit(2)

# Check for mv to /dev/null (data destruction)
def check_mv_to_dev_null(command):
    """Check if mv command targets /dev/null."""
    targets = extract_command_targets(command, 'mv')
    if len(targets) >= 2 and targets[-1] == '/dev/null':
        return targets[-2]  # Return the source file
    return None

mv_dev_null_source = check_mv_to_dev_null(cmd)
if mv_dev_null_source:
    print(f'❌ BLOCKED: Data destruction detected!', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'Reason: mv to /dev/null destroys data', file=sys.stderr)
    print(f'Source: {mv_dev_null_source}', file=sys.stderr)
    print(f'Command: {cmd[:100]}', file=sys.stderr)
    print(f'', file=sys.stderr)
    print(f'If you want to delete the file, use rm instead (with proper review).', file=sys.stderr)
    sys.exit(2)

# === LEVEL 3: SUSPICIOUS PATTERNS (WARNING) ===
# These exit 0 (allow) but print a warning to stderr
suspicious_patterns = [
    (r'\brm\s+.*\s+&&', 'chained rm commands'),
    (r'\bfind\s+.*-delete', 'find -delete operation'),
    (r'\bxargs\s+.*\brm', 'xargs with rm'),
    (r'\brm\s+.*\$\(', 'rm with command substitution'),
    (r'\brm\s+.*`', 'rm with backtick substitution'),
    # File truncation (legitimate for creating empty files, but can destroy data)
    (r'>\s*[^|&\s]+\.(log|txt|json|env|conf|cfg|yaml|yml|md)(\s|$)', 'file truncation on common config/data file'),
]

for pattern, desc in suspicious_patterns:
    if re.search(pattern, cmd, re.IGNORECASE):
        print(f'⚠️  WARNING: Suspicious command pattern detected!', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'Pattern: {desc}', file=sys.stderr)
        print(f'Command: {cmd[:100]}', file=sys.stderr)
        print(f'', file=sys.stderr)
        print(f'This command uses patterns that could accidentally delete more than intended.', file=sys.stderr)
        print(f'Consider reviewing the command carefully before execution.', file=sys.stderr)
        print(f'', file=sys.stderr)
        # Exit 0 = allow command to proceed (warning only, not blocking)
        # Use exit 2 here to block instead of warn
        sys.exit(0)

# Command is safe
sys.exit(0)

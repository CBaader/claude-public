# Claude Code Hooks

Pre-execution hooks for Claude Code that add safety checks before running shell commands.

## dangerous-command-blocker.py

Multi-level protection system that blocks or warns about dangerous shell commands before execution.

### Protection Levels

| Level | Action | What it catches |
|-------|--------|-----------------|
| 0 - Uncommitted work | Blocks | `rm` on files with staged/unstaged/untracked changes in git repos |
| 1 - Catastrophic | Blocks | `rm -rf /`, `dd if=`, fork bombs, `chmod 777 /`, remote code execution pipes |
| 2 - Critical paths | Blocks | `rm .git/`, `rm .env`, `rm package.json`, `mv` to `/dev/null` |
| 3 - Suspicious | Warns | `rm && chained`, wildcards, `find -delete`, `xargs rm` |

### Installation

1. Copy the script to your Claude hooks directory:

```bash
mkdir -p ~/.claude/hooks
cp dangerous-command-blocker.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/dangerous-command-blocker.py
```

2. Add the hook to `~/.claude/settings.json`:

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
          }
        ]
      }
    ]
  }
}
```

3. Test it works:

```bash
# This should be blocked:
claude -p "run: rm -rf /"
```

### How Level 0 Works

Before any `rm` command, the hook:
1. Extracts file targets from the command (handles flags, paths, wildcards)
2. For each target, runs `git status --porcelain` to check for uncommitted changes
3. Blocks if any file has: staged changes, unstaged modifications, or is untracked

This prevents accidental deletion of work that hasn't been committed yet.

### Bypassing

If you need to run a blocked command intentionally:
- Run it manually in your terminal (outside Claude Code)
- Or temporarily remove the hook from settings.json

### Requirements

- Python 3.6+
- git (for Level 0 uncommitted work protection)

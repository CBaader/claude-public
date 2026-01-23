# CLAUDE.md Template

A starting point for your global Claude Code preferences. Copy to `~/CLAUDE.md`.

## Communication Style

[Describe how you want Claude to communicate. Examples:]
- Terse and direct, or detailed and explanatory?
- Technical depth assumed?
- Critique ideas freely or be diplomatic?

## Language

[Your language preferences. Examples:]
- British/American English
- Avoid specific patterns (em-dashes, passive voice, etc.)

## Technical Environment

- [Your OS]
- [Primary languages/tools]
- [Package managers]

## Claude Code Settings

Recommended config for `~/.claude/settings.json`:

```json
{
  "cleanupPeriodDays": 99999
}
```

- `cleanupPeriodDays: 99999` preserves session history indefinitely

## Git Commits

[Your commit preferences. Examples:]
- Conventional commits format
- No co-author lines
- Always include ticket numbers

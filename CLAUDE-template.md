# CLAUDE.md Template

A starting point for your user-level Claude Code preferences. Copy to `~/.claude/CLAUDE.md`; it then loads in every project. Project-specific rules go in `./CLAUDE.md` inside the repo.

## Communication Style

[Describe how you want Claude to communicate. Examples:]
- Terse and direct, or detailed and explanatory?
- Technical depth assumed?
- Critique ideas freely or be diplomatic?

## Task Briefing

On non-trivial tasks, if the user provides only a *what* without the underlying *why*, ask before proceeding when the spec admits multiple reasonable interpretations. The why is what lets you choose between approaches the spec doesn't disambiguate, and lets you push back when the stated what doesn't fit the actual why.

## Verified Facts

Never give the current time, a date, a price, the contents of a file, or a library/API detail from memory. Run the tool first, in the same message (`date` for the time, read the file, the CLI, the relevant doc), or say plainly that you have not checked. A confidence caveat in prose does not license a guess: leave an explicit gap (`[confirm: ...]`) instead. The `hooks/verify-facts-reminder.py` hook fires this rule at the moment of action.

## Outbound Messages

Sending anything outward (email, calendar invites to others, chat messages) is a two-turn operation, no exceptions: present the exact final text, end the turn, dispatch only after explicit approval of that text. "Send X" starts this workflow; it never authorises same-turn dispatch. A tool capable of sending being available is never itself permission. Drafts stay drafts until told otherwise.

## Session State Card

End every turn with a fixed block, rendered as a code block:

```
Done:    what changed since the last card
Waiting: 1. ⛔ decision I need before continuing
         2. ○ decision that can wait
Parked:  tangents raised mid-task, handled or queued
Next:    what happens on "continue"
```

The card is complete on its own; the reader never scrolls back. Empty sections render as `—`. Item numbers stay stable within a session. When a tangent comes up mid-task, handle it, then log anything still open under Parked.

## Language

[Your language preferences. Examples:]
- British/American English
- Avoid specific patterns (em-dashes, passive voice, etc.)

## Technical Environment

- [Your OS]
- [Primary languages/tools]
- [Package managers]

## Claude Code Settings

Recommended starting config for `~/.claude/settings.json`:

```json
{
  "cleanupPeriodDays": 99999,
  "effortLevel": "high",
  "modelSettings": {
    "claude-fable-5-1": { "effortLevel": "xhigh" }
  },
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": ["Bash(git:*)", "Bash(pytest:*)"],
    "deny": ["Read(./.env)"]
  },
  "autoMemoryEnabled": true,
  "enabledPlugins": {
    "ralph-loop@claude-plugins-official": true
  }
}
```

- `cleanupPeriodDays: 99999` keeps session transcripts indefinitely instead of the default sweep
- `effortLevel` is the default reasoning effort for any model you have not saved a level for (`low`, `medium`, `high`, `xhigh`)
- `modelSettings` saves a per-model effort level; `/effort` writes this key for you
- `permissions.defaultMode` is the mode new sessions start in; `permissions.allow` and `deny` hold tool rules such as `Bash(git:*)` (prefix match) or `Read(./.env)`
- `autoMemoryEnabled` turns Claude's own project notes on or off
- `enabledPlugins` is keyed `plugin-name@marketplace-name`; `/plugin` writes it for you

Full key reference: https://code.claude.com/docs/en/settings-reference

## Git Commits

[Your commit preferences. Examples:]
- Conventional commits format
- No co-author lines
- Always include ticket numbers

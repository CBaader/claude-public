# Claude Code & Cowork: Best Practices Guide
## A Beginner-Friendly Reference

### What changed in 2026 (guide updated 14 September 2026)

This guide was first written in early 2026 and rechecked against Claude Code 2.1.269 and the current documentation in September 2026. If you read an earlier version:

- **Corrected:** the `#` memory shortcut is gone (tell Claude instead); `CLAUDE.local.md` is not gitignored for you; plan mode is `/plan`, not "Shift+Tab twice"; `opus` now means Opus 5 and `fable` Fable 5.1; the default effort is `high`; hooks read a JSON event from stdin (there is no `$FILE_PATH`); there is no built-in "Bash" subagent, and subagent files are `.claude/agents/<name>.md`; permission rules are `Bash(rm *)`-style entries in settings, not `ask Bash --cmd`; auto mode is `--permission-mode auto` and the starting mode on Pro, Max and Team; worktrees start with `claude --worktree`; `/review` is an alias of `/code-review`; the `--channels` flag is gone.
- **Added:** rules files and auto memory (section 3); plugins and marketplaces (13); background sessions, agent teams and cloud sessions (17); Remote Control and mobile (18); a tour of the commands added this year (22).

---

## 1. The `/init` Command — What It Actually Does

**The problem it solves:** Every time you start a new Claude Code session, Claude doesn't know anything about your project. You'd have to explain your folder structure, coding style, and common commands every single time.

**What `/init` does:** When you type `/init` in Claude Code, it scans your project and creates a `CLAUDE.md` file — a "memory file" that Claude reads automatically at the start of every future session.

**When to use it:**
- When you first start using Claude Code on any project
- When you clone a new repository and want Claude to understand it

**Example:**
```
> /init
Claude: I've analyzed your project and created CLAUDE.md with:
- Your tech stack (React, TypeScript, Node.js)
- Common commands (npm run build, npm test)
- Project structure overview
```

**Important:** The generated file is just a starting point. You should review and customize it (see next section).

---

## 2. The CLAUDE.md File — Your Project's Memory

### What It Is

A markdown file that acts as Claude's "memory" for your project. Claude reads it automatically at the start of every session, so you don't have to repeat yourself.

### Where It Lives

| Location | Purpose | Who sees it |
|----------|---------|-------------|
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team instructions for this project | Everyone via git |
| `./.claude/rules/*.md` | Team rules split into topic files; add `paths:` frontmatter to load one only for matching files (see section 3) | Everyone via git |
| `./CLAUDE.local.md` | Your personal preferences for this project | Just you (add it to `.gitignore` yourself; nothing does that for you) |
| `~/.claude/CLAUDE.md` | Your preferences for ALL projects | Just you |
| Managed policy file (on macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`) | Organisation-wide instructions your IT team deploys | Everyone at the company |

Claude also loads any `CLAUDE.md` in the directories above the one you start in, and picks up ones in subdirectories when it reads files there.

### How to Create One

**Option 1 — Let Claude do it:**
```
> /init
```

**Option 2 — Create manually:**
Just create a file called `CLAUDE.md` in your project's root folder.

**Option 3 — Ask Claude during a conversation:**
```
> Add to CLAUDE.md: always use async/await, never .then() chains
```
(The old `#` shortcut for this was removed in Claude Code 2.0.70.)

### What to Put In It

Structure it around three questions:

**WHAT is this project?**
```markdown
# Project Overview
- Frontend: React with TypeScript
- Backend: Express.js
- Database: PostgreSQL
- This is an e-commerce platform for selling books
```

**HOW do I work on it?**
```markdown
# Common Commands
- `npm run dev` — Start development server
- `npm test` — Run tests
- `npm run build` — Build for production

# Git Workflow
- Branch naming: feature/name or bugfix/name
- Always run tests before committing
```

**WHAT should Claude avoid?**
```markdown
# Important Constraints
- Never modify files in /legacy — that code is frozen
- Don't use console.log for debugging, use the logger utility
- Authentication logic lives in /src/auth — don't duplicate it
```

### Keep It Short

Anthropic's guidance is under 200 lines per CLAUDE.md file: longer files eat context and reduce adherence. If Claude ignores your instructions, your file is probably too long. When it grows, split it into `.claude/rules/` files and scope the path-specific ones so they only load when Claude touches matching files (section 3).

**Don't include:**
- Code style rules (use a linter instead — it's more reliable)
- Things that only apply sometimes
- Entire documentation files (reference them instead)

---

## 3. Rules Files and Auto Memory

### `.claude/rules/`: CLAUDE.md in Pieces

When one CLAUDE.md grows past 200 lines, split it. Every `.md` file under `.claude/rules/` (subdirectories included) loads at launch with the same priority as `.claude/CLAUDE.md`. Add `paths:` frontmatter and the rule loads only when Claude works on matching files:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API conventions
- Every endpoint returns JSON with an `error` field on failure
- Validate input at the boundary, never deeper down
```

Personal rules that should apply to every project on your machine go in `~/.claude/rules/`.

### Auto Memory: Claude's Own Notes

Claude Code now keeps notes of its own, separate from CLAUDE.md: things it learned while working with you, such as a build quirk, a preference you stated once, where a config lives. They sit in `~/.claude/projects/<project>/memory/`, one topic file per memory, indexed by `MEMORY.md`, which loads into every session. All worktrees and subdirectories of one git repository share a memory directory.

- On by default. Toggle it in `/memory`, or set `"autoMemoryEnabled": false` in settings, per project or globally.
- `/memory` lists what has been stored, so you can read and prune it.
- Memory files survive the `cleanupPeriodDays` sweep that deletes old transcripts.

**CLAUDE.md vs auto memory:** you write CLAUDE.md and it is instructions; Claude writes memory and it is observations. If Claude keeps rediscovering the same fact, promote it into CLAUDE.md.

---

## 4. Continuing & Resuming Sessions

### The Problem

When you close Claude Code, your conversation history is saved but not automatically loaded next time. Starting fresh means Claude forgets everything you discussed.

### Preserving Session History

By default, old sessions get cleaned up. To keep them indefinitely, set `cleanupPeriodDays` to a high number in your settings:

```json
{
  "cleanupPeriodDays": 99999
}
```

**Note:** `0` fails validation. Use a large value such as `3650`. Auto memory files (section 3) are never swept, whatever you set here.

### The Solution

**`claude --continue` (or `claude -c`):**
Picks up exactly where you left off in the *most recent* session in that folder.

```bash
# You were working on the auth feature yesterday
# Today you open terminal in the same project folder:
claude -c

# Claude loads yesterday's conversation and remembers:
# - The auth bug you were debugging
# - The files you were editing
# - Your discussion about the approach
```

**`claude --resume` (or `claude -r`):**
Lets you pick *which* session to resume (useful when you have multiple).

```bash
claude --resume
# Shows a list:
# 1. auth-refactor (2 days ago)
# 2. database-migration (1 week ago)
# 3. bug-fix-login (2 weeks ago)
# Pick one to continue

# Or open the picker already filtered by a search term:
claude --resume auth-refactor
```

### Pro Tips

**Name your sessions:** Use `/rename` during a session to give it a memorable name:
```
> /rename auth-refactor
```
Then later: `claude --resume auth-refactor` opens the picker filtered to that name, or `/resume auth-refactor` inside a session resumes it directly.

**Start fresh for each issue:** Rather than accumulating context in one long session, start a new window for each distinct task. This keeps context clean and avoids confusion from earlier discussions.

---

## 5. Context Management — Staying Within Limits

### The Problem

Every message, file read, and tool result adds to your session's context window. When it fills up, Claude starts compressing older messages automatically — which can lose important details from earlier in the conversation.

### Checking Your Usage

```
> /context
```

Shows how much of your context window you've used. Check this when Claude starts forgetting things you discussed earlier.

### The `/compact` Command

When context is getting full, run:

```
> /compact
```

Claude summarises the conversation so far into a compressed form, freeing up space. You keep the key decisions and context without the full transcript.

You can pass an instruction to tell Claude what to prioritise when summarising:

```
> /compact keep the details of the authentication refactor
```

This ensures important context (like a feature you're actively building) survives the compaction rather than being condensed away.

**When to compact:**
- Before starting a new phase of work in the same session
- When `/context` shows you're above 60-70%
- When Claude seems to forget earlier discussion

### Better Strategy: Fresh Sessions

Rather than compacting repeatedly, start new sessions for distinct tasks:

```bash
claude          # New session for a new task
claude -c       # Continue when it's the same task
```

Compaction is a pressure valve, not a workflow. If you're compacting often, you're probably doing too much in one session.

---

## 6. The @ Syntax for Adding Files

### What It Does

The `@` symbol tells Claude "read this file and include it in our conversation."

### How to Use It

**In your prompt:**
```
> Please review @src/auth/login.ts for security issues

> How do @package.json and @tsconfig.json relate to each other?

> Add error handling to @src/utils/api.ts
```

**In your CLAUDE.md file:**
```markdown
# Key Files
For API documentation, see @docs/api-guide.md
For our coding standards, see @docs/style-guide.md
```

### VS Code Tip

When using Claude Code in VS Code, hold **Shift** while dragging files into the chat to add them to context.

### When to Use vs. Not Use

**Use @** when you want Claude to definitely read a specific file right now.

**Don't use @** for large files or many files — it bloats your context. Instead, mention the path and let Claude decide:
```markdown
# In CLAUDE.md — DON'T do this:
@docs/complete-api-reference.md  # Embeds entire file every session

# DO this instead:
If you need API details, read docs/complete-api-reference.md
```

---

## 7. Plan Mode — Going Back and Forth

### What It Is

A mode where Claude focuses on *planning* before *doing*. Instead of immediately writing code, Claude proposes an approach and waits for your feedback.

### How to Enter Plan Mode

**Option 1:** Type `/plan`, or `/plan add user authentication` to enter plan mode and start on that task straight away.

**Option 2:** Press `Shift+Tab` to cycle permission modes until the status bar shows `⏸ plan mode on`. From Manual mode that is two presses (Manual → accept edits → plan); if your session started in auto mode it is three. Press `Shift+Tab` again to leave plan mode without approving anything.

**Option 3:** Start the whole session in it: `claude --permission-mode plan`.

**Option 4:** Ask Claude explicitly:
```
> Before coding anything, let's plan this out. What's your approach?
```

When Claude presents the plan you get a prompt to approve it, approve and switch to auto mode, or send it back with feedback.

### What "Going Back and Forth" Means

It's a dialogue about the plan before execution:

```
You: I need to add user authentication to this app.

Claude: Here's my plan:
1. Add a users table to the database
2. Create login/register API endpoints
3. Add JWT token handling
4. Create login form component

You: Good, but we're using sessions not JWT. Also, we already
     have a users table.

Claude: Updated plan:
1. Add session handling to existing users table
2. Create login/register endpoints using express-session
3. Create login form component

You: Looks good. One more thing — add a "forgot password" flow.

Claude: Updated plan:
[includes forgot password steps]

You: Perfect, go ahead and implement.
```

### Challenging the Plan

When Claude proposes something and you're not sure about it, push back:

```
Claude: I'll modify the database schema to add a new column...

You: Wait — explain why you're changing the schema. What problem
     does this solve and what are the alternatives?

Claude: [Explains reasoning, alternatives, and trade-offs]
```

Other useful prompts:
- "What could go wrong with this approach?"
- "What are you assuming here?"
- "Is there a simpler way to do this?"
- "Show me the specific lines you're changing before you change them"

### The Two-Tool Pattern: Claude.ai for Planning, Claude Code for Building

Several Anthropic teams (Legal, Growth Marketing) use a two-step process: brainstorm the full approach in Claude.ai's conversational interface first, then have it summarise everything into a step-by-step prompt that you paste into Claude Code for implementation.

This works well when:
- You're a non-developer or working outside your expertise
- The task is complex enough to benefit from freeform exploration before committing to code
- You want to separate "what should we build?" from "build it"

The key step is asking Claude.ai to condense the discussion into an implementation prompt — a structured handoff rather than copy-pasting a messy conversation.

### The Slot Machine Pattern: Accept or Restart

The opposite of careful planning. For tasks where Claude's autonomous output is either right or wrong (refactoring, boilerplate, unfamiliar-language implementations):

1. **Commit your current state** (the checkpoint)
2. **Let Claude work autonomously** for up to 30 minutes with auto-accept on
3. **Review the result.** Either accept it or `git reset` back to your checkpoint and try again with a different prompt

Starting over often has a higher success rate than trying to correct Claude mid-stream. Anthropic's Data Science team calls this the "slot machine" approach — you're betting on a clean autonomous run rather than wrestling with incremental fixes.

**When to use this instead of plan mode:**
- The task is self-contained and verifiable (you'll know immediately if the output works)
- You're delegating in an unfamiliar language or codebase where you can't meaningfully steer
- The cost of a failed attempt is just time, not lost work (because you checkpointed)

### Why This Matters

Without planning, Claude tends to jump straight into coding and may build the wrong thing. Planning catches misunderstandings *before* you waste time on incorrect implementations. But for the right class of task, the slot machine pattern is a legitimate alternative — sometimes it's faster to let Claude take a swing and judge the result than to plan every step.

---

## 8. Choosing a Model, Extended Thinking and Effort Levels

### Picking a Model

Switch models with the `/model` command. The current line-up (September 2026):

| Model | When to use it |
|-------|----------------|
| **Claude Opus 5** | What `/model opus` selects. The default on Max, Team Premium, Enterprise and API accounts — the workhorse for complex reasoning and long-horizon agentic work |
| **Claude Sonnet 5** | What `/model sonnet` selects. The default on Pro and Team Standard — near-Opus coding quality at lower cost, with a native 1M-token context window |
| **Claude Fable 5.1** | The most capable model, for the hardest problems and multi-hour autonomous sessions. Never the default: opt in with `/model fable`. On some plans it bills to usage credits rather than your included limits |
| **Claude Haiku 4.5** | Fastest and cheapest — simple, speed-critical tasks |

Useful aliases: `best` (Fable where you have it, otherwise Opus), `opus[1m]` (Opus with a 1M-token context), `opusplan` (Opus while planning, Sonnet while executing). `/model` saves your choice as the default for new sessions; press `s` in the picker to switch for this session only.

**Getting the most from the top-tier models** (Fable 5.1 especially, but the habits transfer):

- **Give it the goal, not the steps.** Describe the outcome and let the model plan the path. Use `/goal` to keep it working until a completion condition is met.
- **Hand over bigger asynchronous tasks.** Work you'd normally break up — large migrations, multi-hour implementations — can run as one session without losing the thread.
- **Skip the guardrail prompts.** Instructions like "make sure to test" are unnecessary; recent models review their own work. Qualitative feedback works better than itemised instructions.
- **Give it ambiguous problems.** Root-causing, outage debugging, architecture calls — newer models identify underlying causes rather than symptoms.

### What It Is

Extended thinking is enabled by default for all supported Claude models. No magic keywords needed.

### How to Control Reasoning Depth

Use the `/effort` command to set the thinking level:

```
/effort low        → Fast, minimal reasoning; short, latency-sensitive tasks only
/effort medium     → Cheaper, trades away some intelligence
/effort high       → The default on every model that supports effort (Opus 4.7 alone defaults to xhigh)
/effort xhigh      → Deeper reasoning at higher token spend
/effort max        → Deepest reasoning; prone to overthinking, and applies to the current session only
/effort ultracode  → Not a model level: xhigh plus Claude orchestrating dynamic workflows for every substantive task
```

`/effort status` prints the current level. A level you confirm with `Enter` is saved per model as your default; press `s` in the `/effort` slider to apply it to this session only. Adding the word `ultrathink` anywhere in a prompt asks for deeper reasoning on that turn without changing the session setting.

The `CLAUDE_CODE_EFFORT_LEVEL` environment variable pins the level for a session and overrides both `--effort` and `/effort`. `MAX_THINKING_TOKENS=0` turns thinking off altogether on the Anthropic API, except on Fable models, where it cannot be turned off.

### Effort in Skill and Agent Frontmatter

Skills and subagent definitions can specify an `effort` field in their YAML frontmatter:

```yaml
---
name: architectural-review
description: Review system design for scalability issues
effort: high
---
```

Valid values: `low`, `medium`, `high`, `xhigh`, `max` (which of them a given model supports varies; an unsupported level runs at the highest supported one below it).

This overrides the session's effort level while the skill is active, then reverts. Without a skill override, Claude Code takes the first of: an explicit choice (`CLAUDE_CODE_EFFORT_LEVEL`, `--effort`, or `/effort`), the level saved in your settings for that model, then the model's default.

This means skills that need deep reasoning (debugging, architecture review) can guarantee they get it without requiring you to remember `/effort high` first. Conversely, a lightweight skill like a formatter can specify `low` to save tokens.

### When to Increase Effort

- Complex architectural decisions
- Tricky debugging where the cause isn't obvious
- Code that handles money, security, or critical systems
- When Claude's first answer seems superficial

---

## 9. Prompting Strategy: Name the Solution

### The Approach

If you know (or suspect) an orthodox solution exists, just name it. Don't explain how to do it - let Claude handle the details.

**Instead of:**
```
> I need to find which commit introduced this bug. Can you help me
  do a binary search through the git history?
```

**Just say:**
```
> Use git bisect to find which commit introduced this bug
```

### Why This Works

Claude knows the standard tools and techniques. By naming the solution, you skip the back-and-forth and let Claude get straight to execution.

**More examples:**
- "Use a bloom filter for this lookup"
- "Implement this with a debounce"
- "Set up pre-commit hooks for linting"

### Taste Over Implementation

You provide the judgment ("this should use caching"), Claude provides the implementation. Focus on *what* and *why*, let Claude handle *how*.

---

## 10. Hooks — Automating Repeated Tasks

### What They Are (Beginner Explanation)

Hooks are automatic actions that run at specific moments — like "every time Claude edits a file, run the code formatter."

Think of them as "if this happens, do that" rules.

### Available Trigger Points

| When | What You Might Do |
|------|-------------------|
| Before Claude uses a tool | Block dangerous commands |
| After Claude edits a file | Run formatter, run tests |
| When session ends | Send yourself a notification |
| When Claude needs permission | Custom approval logic |

There are 33 events in all. The ones you meet first are `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` and `SessionEnd`; newer ones include `PermissionRequest`, `SubagentStart`, `PostCompact`, `FileChanged` and `WorktreeCreate`.

### How to Set Them Up (Easy Way)

Ask Claude:

```
> Add a PostToolUse hook that runs Prettier on every file you edit
```

Claude writes the `hooks` block into `.claude/settings.json` (this project) or `~/.claude/settings.json` (all your projects). `/hooks` is a viewer, not a wizard: it lists every configured hook, which settings file it came from, and what it runs.

### Example: Auto-Format After Edits

When Claude edits any file, automatically run Prettier:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

A hook receives a JSON description of the event on standard input, so the file path is read with `jq` from `.tool_input.file_path` (there is no `$FILE_PATH` variable). The environment variables a hook does get are `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_EFFORT` and, in web sessions, `CLAUDE_CODE_REMOTE`. Two output contracts matter: exit code `2` blocks the action and sends your stderr back to Claude; exit `0` with a JSON `additionalContext` field on stdout injects text into Claude's context.

### Pre-Built Hook: Dangerous Command Blocker

Want to skip permission prompts but still block dangerous commands like `rm -rf`? See the [dangerous-command-blocker](hooks/dangerous-command-blocker.py) in this repo for a multi-level safety hook that protects uncommitted work, blocks catastrophic commands, and warns on suspicious patterns.

### For Beginners

You don't need hooks to use Claude Code effectively. They're a power feature for when you find yourself repeatedly asking Claude to do the same thing, or when you want guardrails against mistakes.

---

## 11. Subagents — Parallel Workers

### What They Are (Beginner Explanation)

Subagents are like Claude spawning helper Claudes to work on subtasks. Each one gets its own context and can work independently.

### Why They're Useful

**Without subagents:** One Claude tries to do everything, context fills up fast.

**With subagents:**
- Main Claude coordinates
- Subagent A explores the codebase
- Subagent B runs tests
- Subagent C reviews code
- They each have their own context space

### Built-in Subagents

Claude Code comes with some ready to use:

| Agent | What It Does |
|-------|--------------|
| Explore | Fast codebase searching (read-only; runs on your session's model, capped at Opus) |
| Plan | Research during plan mode (read-only) |
| general-purpose | Multi-step work that needs both exploration and edits |

Three helpers (`claude`, `statusline-setup`, `claude-code-guide`) are invoked automatically when needed.

### How to Use Them

Claude often spawns them automatically for complex tasks. You can also request:

```
> Use the explore agent to find all files that handle authentication

> Have a subagent review the code I just wrote for security issues
```

### Creating Custom Subagents

Ask Claude, or write the file yourself. A subagent is one markdown file at `~/.claude/agents/<name>.md` (all projects) or `.claude/agents/<name>.md` (this project): YAML frontmatter plus a system prompt.

```markdown
---
name: security-reviewer
description: Reviews code changes for security issues. Use after implementing auth or input handling.
tools: Read, Grep, Glob
---

You are a security reviewer. Look for injection, auth bypass, secret leakage and unsafe deserialisation. Report file and line for every finding.
```

`/agents` no longer opens a creation wizard (since 2.1.198); it prints a reminder to do the above.

### Preloading Skills into Subagents

Subagent definitions (`.claude/agents/<name>.md`) can list skills in their YAML frontmatter:

```yaml
---
name: excel-worker
description: Create Excel spreadsheets and process data
skills:
  - document-skills:xlsx
  - document-skills:pptx
---

You are a document specialist. Use the preloaded skills to create
professional spreadsheets and presentations.
```

The full skill content gets injected into the subagent's context at startup — it's content injection, not a reference. Each subagent gets everything it needs immediately, with no discovery phase. This makes it work well with parallel agents: dispatch multiple workers, each preloaded with exactly the skills they need.

**Note:** Because the entire skill text is stuffed into the subagent's context window at spawn time, each parallel agent pays the token cost of those skills. Be selective about what you preload.

### For Beginners

Like hooks, subagents are a power feature. Start by just using Claude normally. When you notice context filling up on complex tasks, that's when subagents become valuable.

---

## 12. Skills — Custom Commands for Repeated Workflows

### What They Are

Skills are reusable prompts that you invoke like slash commands. Where CLAUDE.md gives Claude passive knowledge ("here's how this project works"), skills give it active playbooks — step-by-step instructions for specific tasks.

### How to Use Them

Type `/` followed by the skill name:

```
> /interview
Claude: [Runs structured requirements gathering]

> /commit
Claude: [Follows your commit workflow]
```

### Built-in vs Custom Skills

Claude Code ships with built-in skills (`/code-review`, `/simplify`, `/loop`, `/doctor` and more). You can also create your own — they're just markdown files in a specific location:

```
~/.claude/skills/<name>/SKILL.md      # Available in all projects
.claude/skills/<name>/SKILL.md        # Available in this project only
```

Custom slash commands have been merged into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy` and behave the same. Use the skill folder for anything new, because it can carry supporting files.

### Skill Frontmatter

Skills support YAML frontmatter for metadata and configuration:

```yaml
---
name: debug
description: Systematic debugging methodology
effort: high
---
```

Key fields: `name`; `description` (Claude reads it to decide when the skill applies, so write it as "what it does and when to use it"); `argument-hint`; `disable-model-invocation: true` (only you can trigger it); `user-invocable: false` (only Claude can); `allowed-tools`; `model`; `effort` (see section 8); `context: fork` (runs in a separate subagent context); `paths` (activate only for matching files); `hooks`. Note that `skills:` is a *subagent* field, not a skill field. The frontmatter is optional but useful for skills that need specific behaviour.

### What Makes a Good Skill

A skill should encode a **workflow you'd otherwise have to explain every time**:

- **Interview skill:** Structured requirements gathering before building — asks the right questions in the right order
- **Commit skill:** Enforces your commit message format, runs checks, pushes
- **Debug skill:** Systematic debugging methodology instead of ad-hoc guessing

### Example: The Build Workflow

A three-step workflow for non-trivial tasks:

```
/interview   →  Gather requirements (what, constraints, edge cases)
/plan        →  Design the approach, get approval
/ralph-loop  →  Build it, iterating until done
```

Each step produces output that feeds the next. See [workflow-guide.md](skills/workflow-guide.md) for details.

### For Beginners

Start without custom skills. When you notice yourself giving Claude the same multi-step instructions repeatedly, that's a skill waiting to be extracted.

---

## 13. Plugins and Marketplaces

### What They Are

A plugin bundles skills, subagents, hooks and MCP servers into one installable unit. Standalone files in `.claude/` are for your own workflow; plugins are for sharing, with teammates, with the community, with your other machines. A plugin's skills are namespaced, so a plugin called `commit-commands` gives you `/commit-commands:commit`.

### Marketplaces

A marketplace is a catalogue of plugins. Two steps: add the marketplace, then install plugins from it. Claude Code adds Anthropic's official marketplace, `claude-plugins-official`, automatically the first time you start it. Browse it with `/plugin` (the Discover tab) or at [claude.com/plugins](https://claude.com/plugins).

```
> /plugin install github@claude-plugins-official
> /plugin marketplace add anthropics/claude-plugins-community
> /plugin install <name>@claude-community
```

`/plugin` with no argument opens the plugin manager; `list`, `install`, `enable` and `disable` act directly. The same commands exist outside a session as `claude plugin ...`. Installed plugins are recorded under `enabledPlugins` in your settings file and extra marketplaces under `extraKnownMarketplaces`, so a team can pin both in the project's `.claude/settings.json`.

### Writing One

Add a `.claude-plugin/plugin.json` manifest to a folder holding `skills/`, `agents/`, `hooks/hooks.json` or `.mcp.json`. Test it with `claude --plugin-dir ./my-plugin`, validate it with `claude plugin validate .`. The docs walk through converting an existing `.claude/` setup into a plugin.

### For Beginners

Install one or two from the official marketplace when you have a concrete need, such as a GitHub integration or a commit workflow. Don't build your own until you have a skill you want on more than one machine.

---

## 14. Permission Rules Explained

### What Those Cryptic Lines Mean

Permission rules live in your settings file under `permissions`, one list per decision:

```json
{
  "permissions": {
    "ask": ["Bash(rm *)"]
  }
}
```

Let's break this down:

- `ask` = "Ask me for permission"
- `Bash` = "When running terminal commands"
- `(rm *)` = "If the command starts with `rm `" (the delete command)

**In plain English:** "Whenever Claude tries to run a command that deletes files, ask me first instead of just doing it."

The shape is always `Tool(pattern)`: `Bash(npm run *)`, `Read(./.env)`, `Edit(docs/**)`, `WebFetch(domain:example.com)`. A bare tool name (`Read`) matches every use of that tool. The `*` stands for whatever follows; `Bash(git log *)` matches `git log` commands only, `Bash(git *)` every git command. Rules that try to match the command field by name, such as `Bash(command:rm *)`, are ignored with a startup warning.

### The Three Permission Levels

| Level | Meaning |
|-------|---------|
| `allow` | Just do it, don't ask |
| `ask` | Ask me before doing it |
| `deny` | Never allow this |

### Practical Examples

```json
{
  "permissions": {
    "allow": ["Read", "Bash(npm run *)", "Bash(git commit *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)", "Bash(curl *)", "Bash(wget *)"]
  }
}
```

- `allow` — read any file, run npm scripts and commit without asking
- `ask` — prompt before every push
- `deny` — never read the `.env` file; never run curl or wget

Deny rules win over allow rules, and a deny on the whole `Bash` tool removes it from Claude entirely. A `Bash(curl *)` deny does not catch `/usr/bin/curl` or `sh -c 'curl ...'`, so if a network restriction must hold, pair it with the sandbox's network allowlist (section 15).

### How to Configure

Type `/permissions`. The dialog lists every rule and which settings file it came from, and lets you add or remove rules while Claude is working. Or edit the `permissions` block in `.claude/settings.json` (project) or `~/.claude/settings.json` (personal) directly.

### For Beginners

The default settings are fine for most people. Only customize if:
- Claude keeps asking permission for things you always approve → add `allow` rules
- You want to prevent Claude from doing something specific → add `deny` rules
- You're working with sensitive files and want to review every action → add `ask` rules

**Tip:** if sessions feel noisy with permission prompts, run `/fewer-permission-prompts`. It scans your recent transcripts, ranks the read-only Bash and MCP calls you keep approving, and drafts a narrow allowlist for `.claude/settings.json`. More accurate than eyeballing which rules to add.

---

## 15. Autonomous Execution — Sandbox and Auto Mode

### The Problem They Solve

Without either feature, you face a dilemma:
- **Too many prompts:** Claude asks permission for every command, which is annoying
- **Too dangerous:** Using `--dangerously-skip-permissions` lets Claude do anything, including mistakes

Claude Code offers two complementary approaches to this problem: **Sandbox Mode** (boundary-based) and **Auto Mode** (classifier-based). They solve the same problem differently and can be used together.

### Auto Mode

Auto Mode uses a second model, the classifier (Sonnet 5 by default), to review each action before it runs. Safe actions proceed automatically; anything irreversible, destructive or aimed outside your environment is blocked, and Claude is told which rule blocked it so it can try a safer route. Your own `ask` and `deny` rules are checked before the classifier and still prompt or block.

```bash
claude --permission-mode auto
```

The key insight: when the permission prompt *does* fire, you know it's because something was genuinely flagged — so it deserves your attention rather than reflexive approval.

**Availability:** every plan and provider. On Pro, Max and Team plans it is now the built-in *starting* mode, so a fresh session may already be in it; the status bar shows `⏵⏵ auto mode on`. Press `Shift+Tab` to switch to Manual. Organisations can remove it with `permissions.disableAutoMode`.

### Sandbox Mode

Sandbox mode defines boundaries upfront — which directories and network hosts Claude can access — then lets Claude work freely within them.

### How to Set It Up

Type `/sandbox` in Claude Code:

```
> /sandbox
Claude: Choose a sandbox mode:
1. Auto-allow mode (recommended)
2. Regular permissions mode
```

### The Two Modes

**Auto-allow mode (recommended):**
- Commands inside the sandbox run automatically, no permission prompts
- Commands that need to break the sandbox (like accessing the network) still ask
- Your explicit allow/deny rules are still respected

**Regular permissions mode:**
- All commands still go through the permission flow
- But they're still isolated — Claude can only access files/network you've allowed

### What Gets Sandboxed

| Boundary | What It Means |
|----------|---------------|
| Filesystem | Claude can only access specific directories you define |
| Network | Claude can only connect to servers you've approved |

### Example

You might configure:
- **Allowed directories:** Your project folder, `/tmp`
- **Allowed network:** `api.github.com`, `registry.npmjs.org`

Claude can now freely read/write files in your project, install npm packages, and call GitHub — but can't touch your system files or call random websites.

### How They Differ

| | Sandbox Mode | Auto Mode |
|---|---|---|
| **Approach** | Boundary-based | Classifier-based |
| **Controls** | Where Claude can access (dirs, network) | What Claude can do (action risk level) |
| **Setup** | You define the boundaries | Automatic classification |
| **Availability** | All plans (macOS, Linux, WSL2) | All plans; the starting mode on Pro, Max and Team |

They complement each other: sandbox restricts *where*, auto mode restricts *what*.

### For Beginners

Start without either. If you find yourself:
- Always clicking "allow" → try auto mode first (simplest)
- Wanting hard boundaries on filesystem/network access → add sandbox
- Wanting both → they work together

---

## 16. Running Multiple Sessions in Parallel

### Why You'd Want This

Claude works one thing at a time in a single session. But you might want:
- Claude A implementing a feature
- Claude B writing tests
- Claude C refactoring another part

### The Problem

If two Claudes edit the same file simultaneously, they'll overwrite each other. You need separate workspaces.

### Method 1: Built-in Worktrees (Easiest)

Claude Code has built-in worktree support. Start a session with `--worktree` (or `-w`) and a name:

```bash
claude --worktree feature-auth
# → .claude/worktrees/feature-auth/ on a new branch, worktree-feature-auth
```

Or ask Claude mid-session to "work in a worktree" and it creates one itself. Add `.claude/worktrees/` to your `.gitignore`. When you exit, Claude Code offers to keep or remove the worktree; the branch can then be merged or discarded.

### Method 2: Manual Git Worktrees

For more control, create worktrees yourself:

```bash
# Create a worktree for feature work
git worktree add ../my-project-feature feature-branch

# Create another for bugfixes
git worktree add ../my-project-bugfix bugfix-branch

# Now you have:
# /my-project          ← main branch
# /my-project-feature  ← feature branch
# /my-project-bugfix   ← bugfix branch
```

Open a terminal in each folder, run `claude` in each. They're completely independent.

### Method 3: Multiple Terminal Tabs/Panes

**In VS Code:**
- Terminal → New Terminal (or `Ctrl+Shift+``)
- Each terminal can run a separate Claude session

**Using tmux (power users):**
```bash
tmux new-session -s claude1
# In another terminal:
tmux new-session -s claude2
```

Sessions persist even if you close your laptop.

### Method 4: Claude Desktop App and Web

The Claude desktop app offers a worktree option when you start a session, so each session gets its own isolated checkout without you creating it.

Claude Code on the web (claude.ai/code) runs sessions on Anthropic-managed cloud machines; they keep going after you close the tab, and you can watch them from the Claude mobile app. Start one from your terminal with `claude --cloud "description"` and pull one back with `/teleport`. Section 17 has more.

Cowork, the Claude desktop app's agent for non-coding work (files, calendar, email, the browser), is in beta on web and mobile since July 2026, so a Cowork task started at your desk can be checked from your phone.

### Method 5: Background Sessions and Remote Control

`claude --bg "prompt"` starts a session that runs with no terminal attached; `claude agents` shows all of them on one screen (section 17). `/remote-control` makes the session you are in reachable from claude.ai/code and the Claude phone app while everything keeps running on your machine (section 18).

Both are for long-running tasks: start at your desk, then monitor and steer from elsewhere. (The earlier `--channels` flag for Telegram and Discord is gone.)

### Caution

- **Token usage:** Multiple sessions consume tokens quickly
- **Mental load:** Managing multiple Claudes is like running multiple meetings simultaneously
- **Merge conflicts:** When you're done, you'll need to merge the branches

### For Beginners

Start with one session. Parallel sessions are for when:
- You're comfortable with git branching and merging
- Your tasks are clearly separable
- You're on a plan with enough token allowance

---

## 17. Background Sessions, Agent Teams and Cloud Sessions

### Background Sessions and Agent View

A background session is a full Claude Code conversation running with no terminal attached. Start one with `claude --bg "migrate the test suite to vitest"` (it prints an id), or detach the session you are in with `/background`. `claude agents` opens agent view: one screen listing every background session under Needs input, Working and Completed, where you can peek, reply, attach and dispatch new ones.

```bash
claude attach <id>   # open a background session in this terminal
claude logs <id>     # print its recent output
claude stop <id>     # stop it; the conversation is kept
```

Related, inside a session:

- `/fork [prompt]` copies the current conversation into a new background session and keeps working here.
- `/subtask <task>` spawns a background subagent that inherits the full conversation; its result comes back to you.
- `/tasks` shows the background work in the current session.
- `/batch <instruction>` decomposes a large change into 5 to 30 independent units and, once you approve the plan, spawns one background subagent per unit, each in its own worktree, each opening a pull request.

### Agent Teams (Experimental)

Agent teams let several Claude Code instances work as a team: one lead coordinates and assigns tasks, and teammates each get their own context window and message each other. Off by default; enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. The docs' own advice is to check whether subagents already do the job before reaching for a team.

### Cloud Sessions

Claude Code on the web ([claude.ai/code](https://claude.ai/code)) runs sessions on Anthropic-managed cloud infrastructure. They persist when you close the browser, and you can watch them from the Claude mobile app. `claude --cloud "description"` starts one from the terminal, `/teleport` pulls a web session into your terminal, and `/schedule` sets up routines that run in the cloud on a timer. Research preview on Pro, Max and Team.

### For Beginners

`claude --bg` is the one to try first: kick off a long task, carry on in another terminal, check `claude agents` later.

---

## 18. Remote Control and Mobile

Remote Control connects claude.ai/code, or the Claude app on iOS and Android, to a session running on your own machine. Claude keeps running locally: your files, MCP servers and tools stay where they are, and you steer from your phone or a browser. Messages from terminal, browser and phone all land in the same conversation; attach a photo from your phone and Claude sees it.

```
> /remote-control          # inside a session (alias /rc)
claude --remote-control    # start a session with it on
> /mobile                  # QR code to install the Claude app
```

Available on all plans; on Team and Enterprise an Owner has to switch it on in admin settings. If your laptop sleeps or the network drops, Claude Code reconnects and delivers the queued messages. From the app you can pick Manual, Accept edits and Plan modes, but not auto or bypass.

**Claude in Slack.** `/install-slack-app` installs the Claude Slack app (Anthropic calls it Claude Tag). Mention @Claude in a channel and it works from there.

### For Beginners

Turn it on before you walk away from a long task. Then glance at your phone instead of sitting at the desk.

---

## 19. Updating CLAUDE.md During Conversation

### Telling Claude Directly

The `#` shortcut that once did this was removed in Claude Code 2.0.70. Say it in natural language instead:

```
> Update CLAUDE.md to remember that we use PostgreSQL, not MySQL

Claude: Done. I've added to your CLAUDE.md:
"Database: PostgreSQL (not MySQL)"
```

Or:

```
> Add to CLAUDE.md: Our API endpoints should always return JSON

Claude: Added to CLAUDE.md.
```

### Viewing What's Stored

```
> /memory
```

This opens your CLAUDE.md files so you can review and edit them directly. The same screen shows Claude's auto memory (section 3) and lets you switch it off.

### Why This Matters

Every time you find yourself repeating something to Claude, that's a sign to save it to CLAUDE.md. Future sessions will already know.

---

## 20. MCP Servers — Connecting Claude to External Tools

### What MCP Is (Plain English)

**MCP = Model Context Protocol**

Think of it as a universal plug system. Just like USB lets you connect any device to your computer, MCP lets Claude connect to any compatible service.

Without MCP: Claude can only read/write files and run commands on your computer.

With MCP: Claude can also interact with GitHub, databases, Notion, Slack, and hundreds of other services.

### Real Examples

| MCP Server | What Claude Can Do |
|------------|-------------------|
| GitHub | Read issues, create PRs, review code |
| Notion | Read/write pages in your Notion workspace |
| PostgreSQL | Query your database directly |
| Stripe | Look up payments, customers |
| Slack | Read messages, post updates |

### How to Add an MCP Server

**For remote/cloud services (most common):**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**For local tools:**
```bash
claude mcp add --transport stdio my-tool -- npx my-tool-server
```

Servers that stream over SSE take `--transport sse`. For anything else, including a config block copied from another client's setup instructions, pass the JSON straight in:
```bash
claude mcp add-json example '{"command":"npx","args":["-y","@example/mcp-server"]}'
```

### Managing MCP Servers

```bash
# See what's connected
claude mcp list

# Remove a server
claude mcp remove notion

# Test a server
claude mcp get notion
```

### Security Warning

MCP servers are third-party code. Only install servers you trust. A malicious server could:
- Access data Claude sends to it
- Inject harmful instructions

### For Beginners

You don't need MCP to use Claude Code. It's useful when:
- You want Claude to interact with a specific service (GitHub, database, etc.)
- The service has an official or well-reviewed MCP server available

Start without it. Add MCP servers when you have a specific need.

---

## 21. Code Review — Catching Real Bugs

### What It Is

Claude Code can review pull requests and surface substantive issues — not just style nitpicks, but bugs that only emerge from reading large amounts of code in context.

### Why It's Different from Linters

Traditional code review tools and linters catch surface-level issues: naming conventions, unused imports, formatting. Claude Code Review reads the entire PR in context and catches logic errors, subtle bugs, security issues, and architectural problems that require understanding how the code fits together.

Anthropic's internal results, as published with the launch in 2026: PRs with substantive review comments went from 16% to 54% after adoption. On large PRs (1,000+ lines), 84% surface findings, averaging 7.5 issues per review, with less than 1% marked incorrect by engineers.

### How to Use It

```
> /code-review              # review the current diff
> /code-review high 1234    # review PR #1234 at high effort
> /code-review ultra        # deep multi-agent review in a cloud sandbox
> /code-review --fix        # apply the findings to your working tree
```

`/review` is an alias of `/code-review`, and `/ultrareview` of `/code-review ultra`. From the command line, `claude ultrareview` runs the cloud review of the current branch.

The managed Code Review service, which reviews every GitHub pull request automatically and posts inline comments, is a research preview for Team and Enterprise plans. Everyone else uses `/code-review` locally, or runs Claude in their own CI through GitHub Actions.

### When to Use It

- Before merging any non-trivial PR
- On large PRs where manual review is exhausting
- When you want a second pair of eyes on security-sensitive code
- As part of your CI pipeline for automated review

### For Beginners

If you're working solo, code review is still valuable — Claude catches things you'll miss because you're too close to the code. If you're on a team, it complements human review rather than replacing it: humans catch design issues and business logic problems, Claude catches the bugs hiding in the implementation details.

---

## 22. Commands Worth Knowing in 2026

A tour of what has arrived since this guide was first written. Every one is built in.

| Command | What It Does |
|---------|--------------|
| `/plan [task]` | Enter plan mode straight from the prompt |
| `/effort ultracode` | `xhigh` reasoning plus dynamic workflow orchestration for every substantive task; heavier on tokens |
| `/code-review [level] [--fix] [pr#]` | Review the current diff or a PR at `low` to `max`; `ultra` runs a multi-agent cloud review; `/review` is an alias |
| `/security-review` | Vulnerability pass over the current branch |
| `/simplify [target]` | Reuse and simplification cleanups on changed code |
| `/run`, `/verify` | Launch your app and confirm a change works, not just that tests pass |
| `/doctor`, `/skill-doctor` | Setup checkup; what each skill costs in context and how often it fires |
| `/insights`, `/usage` | HTML report on your recent sessions; cost and plan limits (`/cost` and `/stats` are aliases) |
| `/rewind` | Roll the conversation and/or the code back to an earlier point |
| `/btw [question]` | Side question without adding to the conversation |
| `/goal [condition]` | Keep working across turns until the condition is met |
| `/loop [interval] [prompt]` | Repeat a prompt on a timer while the session is open |
| `/import codex\|gemini\|cursor` | Bring instruction files, MCP servers and skills over from another agent |
| `/focus`, `/fast` | Show only your last prompt and a one-line tool summary; toggle fast mode |

---

## 23. Avoiding the Setup Trap

### The Problem

It's tempting to endlessly optimise your Claude Code setup - tweaking CLAUDE.md, adding hooks, configuring permissions, reading more guides. This feels productive but produces nothing.

### The Rule

**Ship actual work.** Your setup exists to serve real output, not the other way around.

- Build only the pieces you need, when you need them
- If you haven't shipped something this week, stop configuring
- A basic setup that produces results beats a perfect setup that doesn't

### Signs You're in the Trap

- You've spent more time on CLAUDE.md than on actual tasks
- You're reading your third "Claude Code tips" article today
- Your hooks are more sophisticated than your project

### The Fix

Close this guide. Open your project. Ask Claude to help you finish something real.

---

## Learning Resources

- [Zvi's Claude Code Tips (Part 3)](https://thezvi.substack.com/p/claude-codes-3) — hooks, subagents, and workflow patterns
- [Zvi's Claude Code, Cowork and Codex (Part 6)](https://thezvi.substack.com/p/claude-code-cowork-and-codex-6-claude) — auto mode, code review, dispatch, skills frontmatter
- [Zvi's Open Problems With Claude's Constitution](https://thezvi.substack.com/p/open-problems-with-claudes-constitution) — the third part of his constitution series, companion to the commentary in this repo
- [Claude Code documentation](https://code.claude.com/docs/en/overview) — the reference every claim in this guide was checked against
- [Anthropic's Official Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Claude Code for Non-Coders](https://everything.intellectronica.net/p/claude-code-for-non-coders)
- [Among the Agents (Workflow Philosophy)](https://www.hyperdimensional.co/p/among-the-agents)
- [Garry Tan's gstack](https://github.com/garrytan/gstack) — MIT-licensed Claude Code skill setup with planning, implementation, and browse skills
- [Hooks Reference](https://code.claude.com/docs/en/hooks)

---

## Quick Reference: Essential Commands

| Command | What It Does |
|---------|--------------|
| `/init` | Create initial CLAUDE.md for your project |
| `/memory` | Edit your CLAUDE.md files; view or switch off auto memory |
| `/context` | See how much context you've used |
| `/compact` | Compress conversation to free up context |
| `/clear` | Reset context (start fresh) |
| `/plan [task]` | Enter plan mode |
| `/model`, `/effort` | Pick the model; set reasoning depth |
| `/sandbox` | Toggle the Bash sandbox |
| `/hooks` | View configured hooks |
| `/permissions` | Manage allow, ask and deny rules |
| `/plugin` | Install and manage plugins |
| `/rename`, `/resume` | Name a session; resume one by name |
| `/tasks` | Background work in this session |
| `/code-review` | Review the current diff or a PR (`/review` is an alias) |
| `/remote-control` | Steer this session from your phone or browser |
| `/btw` | Side question while Claude works |
| `/usage` | Cost and plan limits |

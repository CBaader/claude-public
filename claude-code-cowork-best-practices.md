# Claude Code & Cowork: Best Practices Guide
## A Beginner-Friendly Reference

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
| `./CLAUDE.md` (project root) | Team instructions for this project | Everyone via git |
| `./CLAUDE.local.md` | Your personal preferences for this project | Just you (auto-gitignored) |
| `~/.claude/CLAUDE.md` | Your preferences for ALL projects | Just you |

### How to Create One

**Option 1 — Let Claude do it:**
```
> /init
```

**Option 2 — Create manually:**
Just create a file called `CLAUDE.md` in your project's root folder.

**Option 3 — Add to it during conversation:**
Press the `#` key and type an instruction. Claude will add it to your CLAUDE.md automatically.
```
# Always use async/await, never .then() chains
```

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

Target 100-200 lines maximum. If Claude ignores your instructions, your file is probably too long. Claude's system already has ~50 instructions, so yours compete for attention.

**Don't include:**
- Code style rules (use a linter instead — it's more reliable)
- Things that only apply sometimes
- Entire documentation files (reference them instead)

---

## 3. Continuing & Resuming Sessions

### The Problem

When you close Claude Code, your conversation history is saved but not automatically loaded next time. Starting fresh means Claude forgets everything you discussed.

### Preserving Session History

By default, old sessions get cleaned up. To keep them indefinitely, set `cleanupPeriodDays` to a high number in your settings:

```json
{
  "cleanupPeriodDays": 99999
}
```

**Note:** Use a high number, not 0 (which may behave unexpectedly).

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

# Or specify directly:
claude --resume auth-refactor
```

### Pro Tips

**Name your sessions:** Use `/rename` during a session to give it a memorable name:
```
> /rename auth-refactor
```
Then later: `claude --resume auth-refactor`

**Start fresh for each issue:** Rather than accumulating context in one long session, start a new window for each distinct task. This keeps context clean and avoids confusion from earlier discussions.

---

## 4. Context Management — Staying Within Limits

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

## 5. The @ Syntax for Adding Files

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

## 6. Plan Mode — Going Back and Forth

### What It Is

A mode where Claude focuses on *planning* before *doing*. Instead of immediately writing code, Claude proposes an approach and waits for your feedback.

### How to Enter Plan Mode

**Option 1:** Press `Shift+Tab` twice

**Option 2:** Ask Claude explicitly:
```
> Before coding anything, let's plan this out. What's your approach?
```

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

### Why This Matters

Without planning, Claude tends to jump straight into coding and may build the wrong thing. Planning catches misunderstandings *before* you waste time on incorrect implementations.

---

## 7. Extended Thinking and Effort Levels

### What It Is

Extended thinking is now enabled by default for all supported Claude models (31,999 token budget). You no longer need magic keywords like "ultrathink" or "think hard" - those were deprecated in January 2026 and have no effect.

### How to Control Reasoning Depth

Use the `/effort` command to set the thinking level:

```
/effort low     → Fast responses, minimal reasoning overhead
/effort medium  → Balanced (default for most tasks)
/effort high    → Deep analysis, maximum reasoning depth
```

The `/model` command selects which model to use. With Opus 4.6, thinking uses adaptive reasoning that dynamically allocates tokens based on your chosen effort level.

For fine-grained control, the `MAX_THINKING_TOKENS` environment variable overrides the default budget (up to 63,999 on 64K output models).

### When to Increase Effort

- Complex architectural decisions
- Tricky debugging where the cause isn't obvious
- Code that handles money, security, or critical systems
- When Claude's first answer seems superficial

---

## 8. Prompting Strategy: Name the Solution

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

## 9. Hooks — Automating Repeated Tasks

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

### How to Set Them Up (Easy Way)

Type `/hooks` and Claude will guide you through creating one:

```
> /hooks
Claude: What event should trigger your hook?
1. PreToolUse (before Claude takes an action)
2. PostToolUse (after Claude completes an action)
3. Stop (when Claude finishes responding)
[etc.]
```

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
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

### Pre-Built Hook: Dangerous Command Blocker

Want to skip permission prompts but still block dangerous commands like `rm -rf`? See the [dangerous-command-blocker](hooks/dangerous-command-blocker.py) in this repo for a multi-level safety hook that protects uncommitted work, blocks catastrophic commands, and warns on suspicious patterns.

### For Beginners

You don't need hooks to use Claude Code effectively. They're a power feature for when you find yourself repeatedly asking Claude to do the same thing, or when you want guardrails against mistakes.

---

## 10. Subagents — Parallel Workers

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
| Explore | Fast codebase searching (read-only) |
| Plan | Helps with planning (read-only) |
| Bash | Runs terminal commands separately |

### How to Use Them

Claude often spawns them automatically for complex tasks. You can also request:

```
> Use the explore agent to find all files that handle authentication

> Have a subagent review the code I just wrote for security issues
```

### Creating Custom Subagents

Type `/agents` to create your own:

```
> /agents
Claude: What kind of subagent would you like to create?

> A code reviewer that checks for security issues
Claude: [guides you through setup]
```

### For Beginners

Like hooks, subagents are a power feature. Start by just using Claude normally. When you notice context filling up on complex tasks, that's when subagents become valuable.

---

## 11. Skills — Custom Commands for Repeated Workflows

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

Claude Code ships with built-in skills. You can also create your own — they're just markdown files in a specific location:

```
~/.claude/skills/<name>/SKILL.md      # Available in all projects
.claude/skills/<name>/SKILL.md        # Available in this project only
```

### What Makes a Good Skill

A skill should encode a **workflow you'd otherwise have to explain every time**:

- **Interview skill:** Structured requirements gathering before building — asks the right questions in the right order
- **Commit skill:** Enforces your commit message format, runs checks, pushes
- **Debug skill:** Systematic debugging methodology instead of ad-hoc guessing

### Example: The Build Workflow

A three-step workflow for non-trivial tasks:

```
/interview  →  Gather requirements (what, constraints, edge cases)
/plan       →  Design the approach, get approval
/implement  →  Build it, iterating until done
```

Each step produces output that feeds the next. See [workflow-guide.md](skills/workflow-guide.md) for details.

### For Beginners

Start without custom skills. When you notice yourself giving Claude the same multi-step instructions repeatedly, that's a skill waiting to be extracted.

---

## 12. Permission Rules Explained

### What Those Cryptic Lines Mean

```
ask Bash --cmd '/\brm\b/'      # Prompt on delete commands
```

Let's break this down:

- `ask` = "Ask me for permission"
- `Bash` = "When running terminal commands"
- `--cmd '/\brm\b/'` = "If the command contains 'rm'" (the delete command)

**In plain English:** "Whenever Claude tries to run a command that deletes files, ask me first instead of just doing it."

### The Three Permission Levels

| Level | Meaning |
|-------|---------|
| `allow` | Just do it, don't ask |
| `ask` | Ask me before doing it |
| `deny` | Never allow this |

### Practical Examples

**"Ask before any git commands":**
```
ask Bash --cmd '/\bgit\b/'
```

**"Allow all file reads without asking":**
```
allow Read
```

**"Never let Claude access the internet":**
```
deny Bash --cmd '/\bcurl\b/'
deny Bash --cmd '/\bwget\b/'
```

### How to Configure

Type `/permissions` and follow the prompts:

```
> /permissions
Claude: Current permission rules:
[shows your rules]

What would you like to change?
```

### For Beginners

The default settings are fine for most people. Only customize if:
- Claude keeps asking permission for things you always approve → add `allow` rules
- You want to prevent Claude from doing something specific → add `deny` rules
- You're working with sensitive files and want to review every action → add `ask` rules

---

## 13. Sandbox Mode — Safe Autonomous Execution

### The Problem It Solves

Without sandboxing, you face a dilemma:
- **Too many prompts:** Claude asks permission for every command, which is annoying
- **Too dangerous:** Using `--dangerously-skip-permissions` lets Claude do anything, including mistakes

Sandbox mode is the middle ground: define boundaries upfront, then let Claude work freely within them.

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

### For Beginners

Start without sandboxing. If you find yourself:
- Always clicking "allow" → consider sandbox with auto-allow
- Worried Claude might do something dangerous → sandbox restricts what's possible

---

## 14. Running Multiple Sessions in Parallel

### Why You'd Want This

Claude works one thing at a time in a single session. But you might want:
- Claude A implementing a feature
- Claude B writing tests
- Claude C refactoring another part

### The Problem

If two Claudes edit the same file simultaneously, they'll overwrite each other. You need separate workspaces.

### Method 1: Built-in Worktrees (Easiest)

Claude Code has built-in worktree support. Type `/worktree` or ask Claude to work in isolation:

```
> /worktree
Claude: Created worktree on branch worktree-feature-auth
        Working directory: .claude/worktrees/feature-auth
```

This creates an isolated copy of your repo where Claude can work without affecting your main branch. When you're done, the worktree can be merged or discarded.

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

The Claude desktop app has built-in support for parallel sessions with git worktrees. It manages the worktree creation for you.

The web version (claude.ai/code) runs in cloud sandboxes. You can have multiple browser tabs, each with its own session.

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

## 15. Updating CLAUDE.md During Conversation

### The # Key Shortcut

While chatting with Claude, press `#` and type an instruction. Claude will add it to your CLAUDE.md:

```
# Always use TypeScript strict mode
```

Claude responds: "Added to CLAUDE.md: Always use TypeScript strict mode"

### Telling Claude Directly

You can also just say it in natural language:

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

This opens your CLAUDE.md files so you can review and edit them directly.

### Why This Matters

Every time you find yourself repeating something to Claude, that's a sign to save it to CLAUDE.md. Future sessions will already know.

---

## 16. MCP Servers — Connecting Claude to External Tools

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

## Quick Reference: Essential Commands

| Command | What It Does |
|---------|--------------|
| `/init` | Create initial CLAUDE.md for your project |
| `/memory` | Edit your CLAUDE.md files |
| `/context` | See how much context you've used |
| `/compact` | Compress conversation to free up context |
| `/clear` | Reset context (start fresh) |
| `/sandbox` | Configure sandbox boundaries |
| `/hooks` | Set up automation rules |
| `/agents` | Create subagents |
| `/permissions` | Configure permission rules |
| `/rename` | Name your session for easy resuming |
| `/worktree` | Create isolated workspace for parallel work |

---

## 17. Avoiding the Setup Trap

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

- [Zvi's Claude Code Tips (Part 3)](https://thezvi.substack.com/p/claude-codes-3)
- [Anthropic's Official Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Claude Code for Non-Coders](https://everything.intellectronica.net/p/claude-code-for-non-coders)
- [Among the Agents (Workflow Philosophy)](https://www.hyperdimensional.co/p/among-the-agents)
- [Hooks Reference](https://docs.claude.com/en/docs/claude-code/hooks)

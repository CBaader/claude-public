# Build Workflow: Interview, Plan, Loop

A three-step workflow for non-trivial implementation tasks in Claude Code. Each step has a distinct purpose; skipping steps is the main source of wasted effort and misaligned output.

## The Problem

When requests are vague or complex, jumping straight to code produces the wrong thing. Claude is fast but not clairvoyant. Hidden constraints, unstated preferences, and ambiguous scope cause rework that dwarfs the time a short interview would have taken.

## The Workflow

### 1. `/interview` (optional) - Requirements Gathering

**When**: Any task where you'd hesitate before explaining it to a new hire.

A structured interview (custom skill, included in `skills/interview/`) that walks through goal, constraints, behaviour, and acceptance criteria. Takes 2-5 minutes. Produces a requirements summary that anchors everything downstream.

This step is optional in the sense that the skill is a convenience, not a requirement: asking Claude in plain words to gather requirements and define "done" before it starts does the same job. The skill makes sure nothing is skipped.

Key benefits:
- Surfaces constraints you forgot to mention
- Forces you to define "done" before work begins
- Gives Claude the context it needs to make good decisions autonomously

Install: copy `skills/interview/` to `~/.claude/skills/interview/`. Invoke with `/interview [description]`.

### 2. `/plan` - Design and Approval

**When**: After the requirements are clear, before any code is written.

Uses Claude Code's built-in plan mode. Type `/plan` to enter it directly, optionally with the task (`/plan fix the auth bug`); Claude can also enter it itself via the `EnterPlanMode` tool when a task looks non-trivial. In plan mode Claude explores the codebase, identifies the files and patterns involved, and proposes an implementation approach. You approve, adjust, or reject before a single line changes.

Key benefits:
- Catches architectural mistakes early
- Lets you steer the approach without micromanaging the code
- Creates a shared understanding of what's about to happen

### 3. `/ralph-loop` - Iterative Implementation

**When**: After the plan is approved.

An iterative build-test-fix loop (available as the `ralph-loop` plugin from `anthropics/claude-plugins-official`). Claude implements the plan, runs tests, and fixes issues autonomously until the acceptance criteria from step 1 are met.

Key benefits:
- Autonomous execution against a clear spec
- Built-in verification against the agreed plan
- You review the result, not every intermediate step

## When to Skip Steps

- **Trivial tasks** (typo fix, single-line change): skip everything, just do it.
- **Clear spec already exists**: skip the interview, start at `/plan`.
- **Small, well-defined change**: skip `/plan`, go straight to implementation.

The heuristic: if you're about to say "just build it" and you can describe exactly what you want in two sentences with no ambiguity, you probably don't need the full workflow. If there's any doubt, start by gathering requirements.

## Adding to Your CLAUDE.md

To make this your default workflow, add something like this to your project or global CLAUDE.md:

```markdown
## AI Delegation

- For non-trivial implementation tasks, use the build workflow:
  1. Gather requirements - ask clarifying questions, surface hidden constraints, define acceptance criteria (`/interview` if installed)
  2. `/plan` - design the approach, get user approval
  3. `/ralph-loop` - iterative implementation until done
- When requests are vague, prompt for constraints, examples, and acceptance criteria before proceeding
```

# Claude Code Resources

A practitioner's collection of Claude Code resources - original analysis, practical tools, and workflow patterns built from daily use across several machines.

## Analysis

Original commentary connecting AI alignment to established frameworks in financial regulation, risk management, and virtue ethics.

- **[claude-constitution-commentary.md](claude-constitution-commentary.md)** - Principles over rules: what FCA-style regulation teaches us about Claude's Constitution
- **[amodei-adolescence-commentary.md](amodei-adolescence-commentary.md)** - Reading Amodei's risk essay as an enterprise risk register with appetite statement
- **[prompt-archaeology.md](prompt-archaeology.md)** - What builds up in an instruction file: an audit of eight months of skill files and CLAUDE.md, and how to clean out the history without losing the rules
- **[claude-constitution.md](claude-constitution.md)** - Claude's Constitution (full text, as of September 2026)

## Guide and Template

- **[claude-code-cowork-best-practices.md](claude-code-cowork-best-practices.md)** - Beginner-friendly guide to Claude Code features and workflows, kept current with the CLI (a dated "What changed" block at the top lists the corrections)
- **[CLAUDE-template.md](CLAUDE-template.md)** - Starter template for your own CLAUDE.md configuration and settings.json
- **[operating-patterns.md](operating-patterns.md)** - Nine habits from daily use: state card, two-turn send rule, verified facts, agent dispatch, lower-trust skill allowlist, multi-machine idempotence, three-tier memory, lifting skills from broken plugins

## Hooks

- **[hooks/](hooks/)** - Pre-execution safety and point-of-action reminders (install and settings snippet in `hooks/README.md`)
  - `dangerous-command-blocker.py` - Multi-level protection: blocks catastrophic commands, protects uncommitted work, warns on suspicious patterns
  - `git-freshness-gate.py` - Blocks `git commit` and `git push` when the repo is behind its upstream; fails open on any ambiguity
  - `verify-facts-reminder.py` - Injects a "do not answer from memory" reminder when a prompt asks for a time, date, price, file content or API detail

## Skills

- **[skills/](skills/)** - Custom skills; copy a directory to `~/.claude/skills/`
  - `steelman/` - Argue both sides of a contested proposition at full strength, then a verdict with a parity audit
  - `decide/` - Structured analysis of a non-trivial choice using decision-theory and game-theory frameworks (`references/`)
  - `formalise/` - Extract a prose argument into predicate logic and check it with the z3 theorem prover
  - `synopsis/` - Distil an article or long text into a plain-language synopsis
  - `recap/` - Session state card (done / waiting / parked / next) plus a multi-session browser cockpit page
  - `interview/` - Structured requirements gathering before planning or building
  - `workflow-guide.md` - Three-step build workflow: interview, plan, loop

## Agents

- **[agents/corpus-researcher.md](agents/corpus-researcher.md)** - Read-only subagent that searches a notes corpus for existing coverage of an idea and reports verbatim excerpts

## About

Built and maintained by Clemens Baader. MIT licensed - see [LICENSE](LICENSE).

# Operating Patterns for Claude Code

Nine habits that survived daily use of Claude Code across several machines and many concurrent sessions. Each one exists because its absence caused a real failure. What / Why / How, ten lines each.

## 1. Session state card and parking lot

**What.** Every turn ends with a fixed block: Done, Waiting (numbered; ⛔ blocking, ○ can wait), Parked, Next. Empty sections render as `—`, never disappear. A tangent raised mid-task is handled, then logged under Parked.

**Why.** A long CLI session is dense continuous text. Open items that scroll away get lost unless every turn re-carries the full open state in one fixed, scannable shape. The card is complete on its own; the reader only ever reads the latest one.

**How.** Put the format in a skill (`skills/recap/` here) and point your `CLAUDE.md` at it. Keep item numbers stable within a session. Make it always-on, including clean turns. Fixed shape is the point: the eye learns where to look.

## 2. Two-turn send rule

**What.** Sending anything outward (email, calendar invite, chat message, a push to a public repo) is a two-turn operation. Present the exact final text, end the turn, dispatch only after explicit approval of that text.

**Why.** Approval attaches to the artefact, not the intent. "Send X" starts the workflow; it never authorises same-turn dispatch. Same-turn dispatch removes the veto, and a mis-sent message is unrecoverable.

**How.** Write the rule into `CLAUDE.md` with the words "no exceptions". State explicitly that a tool capable of sending being available is never itself permission. Drafts stay drafts until the user says go.

## 3. Verified facts, never from memory

**What.** The time, a date, a price, the contents of a file, a library or API detail: run the tool first, in the same message, or say plainly you have not checked. A confidence caveat does not license a guess; leave an explicit gap (`[confirm: ...]`) instead.

**Why.** These five categories feel trivially answerable, which is exactly how a plausible-looking value slips into something that looks finished. A wrong number delivered fluently is a failure, not a draft.

**How.** The rule lives in `CLAUDE.md`. The `verify-facts-reminder.py` hook in `hooks/` fires it at the moment of action, when the session-start instruction may already have faded from attention.

## 4. Surprising git or file state is the user's own activity

**What.** When Claude finds work already committed, a file gone or moved, or its own changes captured by another commit, it reads the current state and carries on. No halting, no investigation, no narrated confusion.

**Why.** With several sessions open on the same repos, and files moved in the Finder, surprising state is the normal case. Treating it as an incident wastes a turn and often "fixes" something that was deliberate.

**How.** State it in `CLAUDE.md`: already committed means commit the remaining delta; moved means relocate; deleted means assume deliberate. Keep one narrow safety check: glance before overwriting or deleting something you did not create.

## 5. Agent dispatch protocol

**What.** A subagent receives the orchestrator's prompt as its primary instruction. That prompt is a paraphrase of the original, so precision degrades with every hop (the telephone game).

**Why.** Subagents may read `CLAUDE.md`, but they weigh the dispatch prompt more. Constraints that shape output (language variant, style, "no co-author lines", multi-machine caveats) are exactly the ones a paraphrase drops.

**How.** Quote the relevant constraints verbatim in the dispatch prompt. Never rely on a subagent discovering project context on its own. When dispatching into a repo with its own `CLAUDE.md`, tell the agent to read it first. Ask for a report shape, not a summary.

## 6. Skill allowlist for a lower-trust agent

**What.** When a second agent (another vendor's CLI, a shared assistant) gets your skills, it gets a curated allowlist, never the instruction files. Every skill is either allowlisted or excluded with a recorded reason. An audit script enforces both.

**Why.** Skills that read personal data at runtime (a task list, a memory directory, email, calendar) carry the data into whatever reads them. The instruction files hold the same data in prose. A brief written for that audience holds neither.

**How.** Allowlist by symlink. Run a hard scan for personal-data terms over every allowlisted body; fail the audit on a hit. Keep the specific term list *outside* the audited scope, so the tripwire does not itself disclose what it protects, and keep only generic category words in the script. A term list is a tripwire, not a guarantee: anything not on it passes, so the real fence stays the source-based exclusion.

## 7. Multi-machine idempotence

**What.** The same config repo is checked out on every machine. Every script, hook and setting is idempotent, and a marker file (`~/.config/<you>/machine-profile`) selects a profile where machines must differ. Usernames differ across machines, so synced config never contains a literal `/Users/<name>`; it uses `$HOME`, or is rendered per machine where the consumer cannot expand it.

**Why.** Drift is silent. A hook that assumes one machine's paths fails on the next with no error a user will see for weeks.

**How.** Write a test suite that asserts the machine matches the committed config: symlinks, hook wiring, installed packages, launch agents. Every failure message names the exact remediation. Add a test that greps synced files for hardcoded home directories.

## 8. Three-tier memory

**What.** Instruction files (`CLAUDE.md`, rules) hold standing preferences. A curated domain-memory directory holds durable who/what/why the user maintains by hand. Auto-summarised session history holds what happened recently, tiered from today to archive.

**Why.** Each tier has a different half-life and a different author. Mixing them leaves transient states in files meant to last, and lets an automated summariser overwrite curated fact.

**How.** Rule for the curated tier: every entry must still be valid in about three months, so prefer durable past-tense facts and avoid progressive verbs, specific future dates and "considering" placeholders. Status belongs in a working brief, not in memory. Read the curated tier before answering a personal-fact question; never reason from training data.

## 9. Lift skills out of a broken plugin

**What.** When a plugin's shell is the obstacle (a broken hooks manifest, an MCP requirement you cannot meet, a malformed marketplace entry), lift the individual skill directories you want into your own skills folder instead of installing or rejecting the whole plugin.

**Why.** Skill directories are self-contained. They do not reach into the parent plugin's commands, hooks, MCP config or agents, so they keep working without the shell.

**How.** On every lift, check three things: the frontmatter has `name:` and `description:` inside a proper YAML block (some skills put the description in the body, which the loader treats as missing); no platform-only paths; any "data source priority" blurb prescribing a paid third-party server is rewritten source-agnostic with a web fallback. Record the upstream repo, licence and commit in a `SOURCE.md` next to the skill.

---
name: decide
description: Use when the user faces a non-trivial choice — "should I...", "which is better...", "I'm torn between...", "help me think through..." — especially multi-option choices under uncertainty or where other players' moves matter. For stress-testing a single contested yes/no proposition, use /steelman instead.
argument-hint: "[brief description of the decision]"
effort: max
---

# Decision Analysis

Structured framework for analysing decisions. Routes between game theory (strategic interactions) and decision theory (uncertainty without strategic players), or integrates both for hybrid situations.

## When to use

- "Should I...", "which is better...", "I'm torn between...", "help me think through..."
- Multi-option choices under uncertainty, or where other players' choices affect the outcome

**Don't use** when:
- The question is a single contested proposition to argue at full strength → use `/steelman` (it routes back here for multi-option choices)
- The question is rhetorical or the user just wants a quick opinion — answer directly; the Trivial triage category exists to catch these if they slip through

## Procedure

### 1. Get the decision

If the user passed an argument, use it. If not, ask once, in plain text (not an AskUserQuestion form — the answer is free-form, not an option pick):

> "Describe the decision you're facing — the options, the stakes, who else is involved, and any deadline."

### 2. Triage

Classify the decision into exactly one category:

| Category | Test | Action |
|----------|------|--------|
| **Trivial** | Low stakes AND easily reversible | Immediate recommendation, no diagnostic. |
| **Decision problem** | Uncertainty matters, but no strategic players whose choices affect your outcome | Run the 6-step decision theory diagnostic (Part Two of decision-theory-framework.md) |
| **Strategic game** | Outcome depends on other players' choices, and they are considering yours | Run the 5-step game theory diagnostic (Part Two of game-theory-decision-framework.md) |
| **Hybrid** | Both strategic interaction AND significant uncertainty against nature | Integrated analysis using both frameworks |

### 3. Confirm classification

State the classification and the planned framework in one line. Then:

> "Confirm, or describe what I've missed."

Wait for confirmation before proceeding. If the user corrects, reclassify.

Exception: **Trivial** needs no confirmation round — state the classification and give the recommendation in the same message; the user can object. Done.

### 4. Load the framework(s)

Read only what the classification needs:
- **Decision problem** → `references/decision-theory-framework.md` (next to this SKILL.md)
- **Strategic game** → `references/game-theory-decision-framework.md` (next to this SKILL.md)
- **Hybrid** → both
- **Trivial** → neither (already answered in step 3)

### 5. Gather missing information

Identify all inputs needed for the diagnostic that are not already known. Ask for them in a **single plain-text round**: one markdown list, each item a question with a one-line note on why it matters. The user may answer free-form, partially, or say "assume X" — fill remaining gaps with stated assumptions rather than re-asking. Do not use an AskUserQuestion form (multi-question forms are banned by the global interaction rules), and do not ask one question per diagnostic step.

If the user's initial description provides enough to work with, skip this step.

### 6. Run the diagnostic

**Decision problem:** Work through the 6-step diagnostic from the decision theory framework. Apply the concepts to the specific decision - do not recite definitions.

**Strategic game:** Work through the 5-step diagnostic from the game theory framework. Identify the game type, analyse equilibria, and assess strategic options.

**Hybrid:** Identify which aspects are strategic (other players' choices) and which are uncertain (nature/chance). Run a single integrated analysis:
- Frame: players AND uncertainties together
- Analyse the strategic interaction (equilibria, credibility, information)
- Assess the uncertain elements (probabilities, payoffs, biases)
- Shared steps (payoff evaluation, stress-test) done once with both lenses, not duplicated

**Trivial:** Already answered at step 3. Does not reach this step.

### 7. Ground against your notes (optional; skip for Trivial)

Bring your own corpus: this step assumes a personal knowledge base with a concept index at `<your-notes-index>`; skip it if there is none. Run it *after* the diagnostic, never before — the analysis must come from the situation first, with the notes as a check-and-enrich layer, not the opening frame. (Otherwise the captured principles quietly frame the problem: you reason toward the principles you happen to hold, not the ones this decision turns on.)

1. From the decision's specifics — the dilemma, the leaning, and any biases, risks, or failure modes the diagnostic surfaced — `grep` the concept index `<your-notes-index>` for relevant entries (do **not** read the index whole).
2. Read the **full** matched entries from the summary files — the whole entry section, not the headline. You need the named mechanism, the diagnostic question, the worked example or image, and any epistemic-status tag.
3. Surface up to 4 principles — a ceiling, not a floor. If only 1-2 genuinely apply, show 1-2; if none do, say "Nothing in the notes sharpens this" and go to Close. Order by relevance and tag each `core` or `adjacent`. Render each in depth: the **mechanism** in the entry's own language (2-4 sentences, including the image or example when it has one), the quoted **diagnostic** when it names one, and a **→ Here** line applying it to this decision. Flag an `empirical-thin`/contested entry in one clause.
4. Sort each into one of: **confirms** the leaning, **sharpens** it, **names a bias or diagnostic the analysis missed**, or **contradicts** it. The contradiction case is the most valuable — surface it loudest. If a contradiction is strong enough to move the recommendation, say so explicitly and revise it in Close; the reasoning still came from the situation first, the notes caught what it missed.

### 8. Close

End every non-trivial analysis with:

```
Recommendation: [specific action]
Confidence: [High / Medium / Low] - [one sentence justification]
Key assumption to monitor: [the single assumption that flips the recommendation if wrong]
```

## Execution Rules

- Triage first, always. Do not skip straight to analysis. Load framework docs only after triage, and only the one(s) the classification needs.
- Confirm classification before analysis. One exchange, not zero (Trivial exempt — answer immediately).
- One batched plain-text question round for missing information, not one per step. Unanswered inputs become stated assumptions, surfaced in the analysis.
- Apply the frameworks to the specific decision. Do not recite concept definitions.
- Notes grounding (step 7) comes *after* the diagnostic, never before — reason from the situation first, then consult the notes as a check. Surface matched principles in depth (mechanism + diagnostic + image + application), up to 4, ceiling not floor; flag any contradiction with the leaning loudest. `grep` the index, never read it whole.
- Terse output. Conclusions first, reasoning after.
- For hybrid: shared steps done once with both lenses, not duplicated.
- British English throughout.

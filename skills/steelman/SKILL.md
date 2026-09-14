---
name: steelman
description: Use when a single contested proposition (yes/no, do/don't, A vs B) needs a genuine evaluation at full strength — "steelman both sides", "argue both then verdict", or a recommendation/judgement call the user wants stress-tested. Not for multi-option choices under uncertainty (use /decide) or quick recommendations.
effort: max
---

# Steelman

Produce the strongest version of both sides of a proposition, then reach a verdict via a pre-committed evaluation method. The whole point is to prevent the failure mode where AI steelmanning collapses into performative rigour — the steelmen sound balanced but the verdict launders motivated reasoning.

## When to use

- User says "steelman both sides", "argue both at full strength then verdict", "I want a real evaluation of X"
- User has named a recommendation, judgement call, or proposition they want stress-tested
- The question is a single proposition (yes/no, do/don't, A vs B)

**Don't use** when:
- The question is a multi-option choice under formal uncertainty → use `/decide` instead (game theory / decision theory)
- The user wants a quick recommendation (this skill is heavy)
- The proposition isn't genuinely contested — say "side A wins decisively, here's why" without the full ritual

## Execution rules

- Follow the steps in order. Do not skip.
- **Verdict criteria must be locked in step 2, before either steelman is written.** Single most important rule. Skipping it lets motivated reasoning launder itself through the verdict step.
- If the user has signalled a lean in the prompt, **generate the opposing-lean side first**.
- Required parity per side: comparable length, equal citation count, equal number of named mechanisms.
- Each steelman cites at least one named real-world advocate. For empirical or public-facing propositions, verify advocates and load-bearing factual claims with a quick web search; label anything taken from training data as unverified. **Never invent or stretch an attribution** — if no real advocate can be found for a side after searching, say so and treat the absence as evidence in the verdict.
- Ban "both sides have a point" / split-the-difference as the conclusion. Force a pick OR an explicit "insufficient evidence; here's what would resolve it."
- The notes sweep (step 3, optional) must be symmetric — for any principle arming one side, search for the counter-principle arming the other; a personal knowledge base should hold retrievable dissent, and a one-sided pull is exactly the thumb-on-the-scale this skill exists to prevent. Notes-sourced mechanisms count toward the parity audit. `grep` the index, never read it whole. Skip the sweep if the user has no notes corpus or asks for a faster pass.
- British English. Surface uncertainty.

## Procedure

### 1. Pose check

Before anything else, examine the question itself.

- State the proposition cleanly in one sentence.
- Name load-bearing premises both sides accept (these won't be debated).
- Flag premises one side would reject (these are part of the disagreement; surface them).
- If the question isn't well-posed (equivocates between distinct claims, presupposes a contested frame), say so and ask for clarification before continuing.

### 2. Pre-register verdict criteria

**This step happens BEFORE either steelman is generated.** Pick one method based on question type:

- **Double-crux** — each side commits to a belief B such that, if B were resolved against them, their position flips. The verdict turns on resolving the crux. Best for normative or strategic disputes. Source: CFAR, ~2016.
- **Analysis of Competing Hypotheses (ACH)** — list 2-4 hypotheses, list evidence items, mark each evidence × hypothesis as Consistent / Inconsistent / Neutral. Verdict goes to the hypothesis with the **least disconfirming** evidence, NOT the most confirming (avoids confirmation-bias trap). Best for empirical disputes. Source: Heuer & Pherson, intelligence community.
- **Bayesian updating** — state numeric prior, list each argument as evidence with an explicit likelihood ratio, update sequentially. Best when quantification is honest, not theatre.
- **Falsifiability thresholds** — each side commits to "this evidence/argument would refute me." Verdict resolves when threshold met. Best for predictive disputes.

State the chosen method explicitly. State what would constitute a verdict for each side under that method.

**Criteria fairness check**: the criteria must be ones an advocate of either side could accept before seeing the steelmen. If a criterion predictably favours one side, replace it or name the bias explicitly — pre-registration only works if the criteria themselves aren't gerrymandered towards the lean.

### 3. Generate both steelmen

For empirical disputes, gather a small shared evidence pool first (web search). Both steelmen must draw on the same pool — asymmetric research produces asymmetric steelmen that the parity audit cannot detect.

**Notes sweep (optional, symmetric).** Bring your own corpus: if the user keeps a personal knowledge base (a notes vault, a summaries folder, a concept index), sweep it for principles that bear on the proposition and feed them into the steelmen as named mechanisms where they qualify. `grep` the index at `<your-notes-index>` for terms from the proposition (do **not** read the index whole), then read the full matched entries. Symmetry is mandatory: a good knowledge base holds retrievable dissent, so for any principle that arms one side, actively search for the counter-principle that arms the other — never let the notes become a thumb on the scale. A principle that genuinely cuts only one way is legitimate ammunition for that side, but it then counts toward that side in the parity audit (step 4), and the imbalance must be addressed there, not hidden. Hold back any principle that bears on the *verdict* rather than either case (a relevant bias, a decision diagnostic) for the final check (step 6).

Identical structural budgets:
- Comparable length, neither side visibly thinner
- At least one named real-world advocate per side (brief reference)
- At least one specific named mechanism per side (not "this would be good" — *how* it would work)
- If user signalled a lean in the prompt, write the opposing-lean side first

For each side:
- The strongest argument an intelligent, informed advocate would make — not the most palatable
- Explicitly seek heterodox/uncomfortable framings if the question is contested (LLM training data over-represents mainstream views; correct for it)
- Address the strongest objection a steelman of the other side would raise

### 4. Parity audit

Mechanical check before verdict. Do not rely on self-assessment of fairness — it is unreliable.

- Neither side substantially shorter than the other
- Citation count equal
- Named mechanism count equal

If asymmetric, re-balance the weaker side. Do not proceed to verdict until parity holds.

Exception: if citation parity is impossible because one side genuinely lacks real advocates after searching, do not fabricate to balance — state the asymmetry and carry it into the verdict as evidence.

### 5. Apply the verdict method

Execute the method chosen in step 2.

- **Double-crux**: identify the operative crux. State which side prevails if the crux resolves which way. Pick the more likely resolution if defensible; otherwise declare the crux unresolved and say what would resolve it.
- **ACH**: produce the matrix. Identify the hypothesis with the least disconfirming evidence. Report it.
- **Bayesian**: show the update arithmetic. Report posterior + the largest single update + which arguments were load-bearing.
- **Falsifiability**: state which side's threshold has been met or is unmet.

**Discipline**:
- No "both sides have a point" verdict
- If genuinely indeterminate: "insufficient evidence to decide between X and Y. Here's what would resolve it: [concrete question / evidence]"

### 6. Final check

Before reporting the verdict, run two questions:

1. **Did the losing side's steelman actually fail to defeat the winning side, or did it just sound weaker?** If the latter, the verdict should flip — re-examine.
2. **Was there a lean in the user's prompting that the verdict aligns with?** If yes, audit whether the verdict survived an honest pass over the opposing steelman, or whether the steelman was just performative.
3. **Does any captured notes principle contradict the emerging verdict, or name a bias it might be exhibiting?** Check the verdict against the principles surfaced in step 3 (and any held back as verdict-relevant). A contradicting principle does not automatically flip the verdict, but it must be surfaced in Caveats and answered, not ignored.

If any check fails, return to step 5 with the asymmetry named.

### 7. Output

Six labelled sections:

1. **Proposition** — one sentence + shared premises
2. **Verdict method** — named, with success criteria for each side
3. **Steelman A** — named advocate, mechanism, strongest case
4. **Steelman B** — named advocate, mechanism, strongest case
5. **Verdict** — the pick + the load-bearing reason, or explicit "insufficient evidence + what would resolve it"
6. **Caveats** — what subjectivity wasn't eliminated; what would change the verdict; any notes principle that cut against the verdict

## Notes on what this skill does and doesn't do

- It does not eliminate subjectivity. It makes residual subjectivity *visible and auditable* (priors, weights, framings) instead of *buried* in tone or selective amplification.
- It is heavier than informal reasoning. Use only when the question warrants it.
- The pre-registration step is the load-bearing innovation. Without it, this is just dressed-up advocacy.

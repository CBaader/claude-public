---
name: formalise
description: Use when the user wants the logical structure of a prose argument extracted and machine-checked — "formalise this", "extract the logic / predicate logic", "translate this text into logical statements", "check this argument for contradictions / hidden assumptions / whether the conclusion actually follows". Takes a text file (optionally one section) and writes a reader-friendly sidecar: plain-English findings first, the predicate logic and the solver's verdict underneath for verification. Not for a quick yes/no on a single proposition (use /steelman) or a multi-option decision (use /decide).
effort: max
---

# Formalise

Turn a piece of British-English prose into predicate logic and then **check the logic with a real theorem prover (z3)**, not just render it. Two distinct jobs done by two distinct things: *I* (the model) do the fallible step — translating English into first-order logic — and *z3* does the certain step — telling us whether the claims are mutually consistent and whether each stated conclusion genuinely follows from its premises. The output is written for the user to read in plain English, with the formal symbols and the solver verdict kept underneath so they can audit the translation.

The value is not the symbols. It is that "this argument feels off" becomes "claims 3 and 7 cannot both be true" or "the conclusion only follows if you also assume X, which the document never states."

## When to use

- "Formalise this", "extract the logic / predicate logic", "turn this into logical statements".
- "Check this for contradictions / hidden assumptions / does the conclusion follow / is this argument valid", pointed at a document.
- A dense argumentative text (strategy paper, proposal, brief) whose inferential structure is worth making explicit and testing.

**Don't use** when:
- The user wants a stress-test of one contested proposition → `/steelman`.
- The user faces a multi-option choice under uncertainty → `/decide`.
- The text has no real argument (pure description, a list of facts) — say so rather than manufacturing inferences.

## What it produces

A sidecar file `<source-stem>.logic.md` written next to the source, in this order:

1. **Findings — plain English first.** Each argument in the document gets a verdict a non-logician can read.
2. **Claim inventory.** Every argument-bearing claim, numbered, in plain English, tagged checkable vs not.
3. **Formal appendix.** The symbol table, the predicate-logic for each claim, and z3's raw verdict — so the translation can be verified.
4. **Claims that can't be formally checked.** Listed explicitly, never silently dropped.

Plus a short plain-English summary printed to the chat.

## Execution rules

- **Plain English leads every finding.** The reader is a person, not a logician. Symbols live in the appendix and in a collapsible block under each finding, never as the headline.
- **I translate; z3 certifies.** z3 only ever proves things about *the symbols I wrote*. So the symbol table and the per-claim formal gloss must be readable and faithful — a wrong translation produces a confident-but-wrong verdict. Where a formalisation is a judgement call (which is most of them), say so on that claim.
- **Never force a claim that doesn't fit classical logic.** Deontic ("should", "must"), modal ("can", "will"), probabilistic ("likely", "~45%"), vague/graded ("massively under-used"), intensional ("the same gate, packaged differently"), and defeasible/generic claims go in the *can't-check* section with a one-line reason. Faking them as flat predicates is the main failure mode.
- **State the domain.** Checks run over a finite, named universe (the entities the text talks about, plus a wildcard individual). That is the right notion of validity for real arguments, but it must be stated so the scope is honest.
- **Map every solver assertion back to a numbered claim** (a comment in the `.smt2`), so a sceptic can confirm the machine checked what the prose says.
- **British English. Surface uncertainty.** Hyphens, not em-dashes.
- **Verify z3 is present** (`command -v z3`). If missing, do everything except the runs, mark verdicts "UNCHECKED", and tell the user how to install it: `brew install z3` on macOS, a release from https://github.com/Z3Prover/z3 elsewhere; `pip install z3-solver` provides the Python bindings if they prefer to drive the solver from Python.

## Procedure

### 1. Read and scope
Read the source file fully. If the user named a section (e.g. "§5"), scope to it; otherwise do the whole file but warn if it is very long and offer to focus. Re-read immediately before writing — do not work from memory of an earlier read.

### 2. Extract argument-bearing claims
Pull the claims that *do logical work* — premises, conclusions, conditionals ("if X then Y"), quantified assertions ("every/no/some function..."), dependencies ("X requires Y"), and identity/definition claims. **Skip pure description** ("the office is in London") unless it is a premise in some inference. Number each claim and cite its source (`§5.1`, line N). Quote the original phrase so the translation is checkable against it.

### 3. Classify each claim
Tag every extracted claim:
- **Checkable** — factual predications, conditionals, quantified statements, identities, definitions. These become logic.
- **Can't-check** — deontic / modal / probabilistic / vague / intensional / defeasible (see Execution rules). These are listed, with the reason, and excluded from the solver.

### 4. Build the symbol table
- A **finite enumerated domain** for each sort, seeded with the named entities **plus one anonymous "other" individual** so universal claims are genuinely tested, not just against named cases.
- One **predicate per recurring relation/property**, each with a plain-English gloss (`Vol(f) := function f volunteers to cut its own roles`).
- Constants for named individuals (`ceo`).
Keep predicates coarse enough to be faithful and fine enough that the load-bearing premise is visible as its own line.

### 5. Formalise the checkable claims
Write each as clean predicate logic (`∀`, `∃`, `→`, `∧`, `∨`, `¬`, `=`) in the appendix gloss. Group claims into **arguments** exactly as the document presents them: a set of premises and the conclusion it draws. Also assemble the **global set** of all checkable claims for a whole-document consistency sweep.

### 6. Encode to z3 and run
Write `<source-stem>.logic.smt2` (kept as the audit artifact). Use the recipe below. Two kinds of question:
- **Consistency** — can all the claims (globally, and per-argument the premises) be true together? `(check-sat)`; `unsat` = contradiction, then `(get-unsat-core)` names the clashing claims.
- **Entailment** — does conclusion `C` follow from premises `P1..Pn`? Assert the premises and `(not C)`; `unsat` = **valid** (it follows); `sat` = **invalid**, and the model is a **counterexample** — read off the **missing assumption** (what would have to be added to make it valid).
Run `z3 <file>.smt2`. For any `sat` entailment or any inconsistency, do a focused follow-up run with `(get-model)` / `(get-unsat-core)` to extract the detail.

### 7. Translate verdicts to plain English
For each argument, one of:
- **Valid** — "this conclusion genuinely follows", + name the premise it leans on hardest (the one whose removal breaks it).
- **Invalid (needs an unstated assumption)** — "this only follows if you also assume X" (X read from the countermodel).
- **Premises inconsistent** — "these claims can't all be true: A and B clash."
For the global sweep: consistent, or a named contradiction.

### 8. Write the sidecar and summarise
Write `<source-stem>.logic.md` in the format below. Do **not** overwrite an existing one without saying so. Print a 3-5 line plain-English summary to chat (how many claims, how many checkable, the headline findings).

## Output format (`<source-stem>.logic.md`)

```
# Logic check — <source filename>
*Generated by /formalise on <date>. Domain: {<named entities>, other}. <N> claims extracted, <M> checkable.*

## Findings

### 1. <plain-English headline verdict>
**In plain English:** <2-4 sentences a non-logician reads. What the document argues and what the check found.>
**Stands or falls on:** <the load-bearing premise / the missing assumption / the clashing pair.>
**Source:** §X · **Verdict:** VALID | INVALID (needs assumption) | CONTRADICTION | CONSISTENT
<details><summary>formal</summary>

P1  ∀f ¬Vol(f)            (claim 4)
P2  ...
∴   ∀f (Cuts(f) → Ovr(ceo,f))   — z3: premises ∧ ¬C unsatisfiable ⇒ follows
</details>

### 2. ...

## Claim inventory
| # | Claim (plain English) | Source | Type | In check? |
|---|----|----|----|----|
| 1 | No function volunteers to cut its own roles | §5.1 | quantified | yes |
| 2 | We should be more ambitious about AI | §4 | deontic | no — obligation, not truth-functional |

## Formal appendix
**Domain:** Fn = {legal, finance, it, other}; Agent = {ceo, other}
**Predicates:** Vol(f) := f volunteers to cut its own roles; Cuts(f) := ...; Ovr(a,f) := agent a overrides f
**Claims as logic:** <each numbered claim in FOL>
**Solver:** z3 <version> · file `<stem>.logic.smt2` · <verdict transcript>

## Claims that can't be formally checked
- §4 "we should be more ambitious" — deontic; an obligation does not entail a fact.
- §5 "same gate, opposite packaging" — intensional; one referent under two descriptions with different inferred consequences, which classical logic cannot represent.
- ...
```

## The z3 recipe (worked example — the "turkeys" argument)

```smt2
(set-logic ALL)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)

; finite domain: the functions named, plus a wildcard so ∀ is really tested
(declare-datatypes ((Fn 0))    (((legal) (finance) (it) (other))))
(declare-datatypes ((Agent 0)) (((ceo) (other_agent))))

(declare-fun Vol  (Fn) Bool)        ; f volunteers to cut its own roles
(declare-fun Cuts (Fn) Bool)        ; cost is taken out of f (substitutive value captured)
(declare-fun Ovr  (Agent Fn) Bool)  ; agent a overrides f's self-interest

(assert (! (forall ((f Fn)) (not (Vol f))) :named c_turkeys))                       ; claim: no function volunteers
(assert (! (forall ((f Fn)) (=> (Cuts f) (or (Vol f) (exists ((a Agent)) (Ovr a f))))) :named c_mech))
(assert (! (forall ((a Agent) (f Fn)) (=> (Ovr a f) (= a ceo))) :named c_onlyceo))  ; only the CEO can override

(check-sat)            ; sat  => premises are mutually consistent
; entailment: does  ∀f (Cuts f -> Ovr ceo f)  follow?
(push)
  (assert (not (forall ((f Fn)) (=> (Cuts f) (Ovr ceo f)))))
  (check-sat)          ; unsat => the conclusion follows (argument valid)
(pop)
```
- Contradiction pattern: assert all claims, `(check-sat)`; if `unsat`, `(get-unsat-core)` returns the `:named` labels that clash → those are the incompatible claims.
- Invalid-argument pattern: if the entailment `(check-sat)` returns `sat`, re-run that block with `(get-model)`; the model assigns the predicates so that every premise holds and the conclusion fails — translate it into the unstated assumption the argument needs.
- Use enumerated datatypes (finite domain) so quantifiers are decidable and counterexamples are concrete. Note the finite scope in the output.

## Honesty rules / limits
- The translation is mine and fallible; z3 only certifies the encoding, not that the encoding matches the English. So the symbol table and per-claim gloss are part of the deliverable, not scaffolding — they are how the reader checks me.
- Validity is reported **over the stated finite domain**. State it. For these arguments that is the right notion; do not imply universal validity.
- If a single English sentence carries two claims, split it. If a claim's formalisation is genuinely contestable, give the alternative reading rather than silently picking one.
- Report counts honestly, including how many claims fell into can't-check — a document that is mostly deontic/modal will have few checkable claims, and that itself is a finding.

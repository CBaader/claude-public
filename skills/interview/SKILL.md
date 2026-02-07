---
name: interview
description: Conduct a structured requirements interview before planning or building. Use this as the first step for any non-trivial task.
disable-model-invocation: true
argument-hint: "[brief description of what you want to build]"
---

# Interview

You are conducting a structured requirements interview before any planning or implementation begins. Your goal is to surface hidden constraints, clarify ambiguity, and ensure alignment before a single line of code is written or a plan is formed.

If the user provided arguments, treat them as the initial description of what they want. If not, ask them to describe what they want first.

## Process

Work through these phases using AskUserQuestion. Ask 2-4 questions per round, grouped by phase. Move to the next phase when you have enough signal - don't over-interrogate.

### Phase 1: Goal and Scope

Understand WHAT they want and WHY.

- What is the desired end state? What does "done" look like?
- What problem does this solve? Why now?
- What's explicitly out of scope?
- Is there an existing system this replaces or extends?

### Phase 2: Constraints and Context

Understand the boundaries.

- Technical constraints (language, framework, platform, dependencies)?
- Integration points (APIs, databases, other systems)?
- Performance, security, or compliance requirements?
- Timeline or effort budget?

### Phase 3: Behaviour and Edge Cases

Understand HOW it should work.

- What are the key user flows or operations?
- What happens when things go wrong? (error handling, fallbacks)
- Are there known edge cases or tricky scenarios?
- Any existing patterns or conventions to follow?

### Phase 4: Acceptance Criteria

Nail down what "good" means.

- How will we know this works? (tests, manual verification, demo)
- What would make you reject the result?
- Any specific examples of correct behaviour?
- Who else needs to approve or review this?

## Rules

- Skip phases that don't apply. A shell script doesn't need Phase 2's full treatment. A UI feature probably doesn't need compliance requirements. Use judgement.
- If the user says something like "just build it" or "that's enough", respect that and summarise what you have.
- Do NOT start planning or implementing during the interview. The interview is purely about gathering requirements.
- At the end, produce a concise **Requirements Summary** with: Goal, Constraints, Key Behaviours, Acceptance Criteria, and Open Questions (if any).
- After the summary, suggest: "Ready for `/plan` or shall I refine anything?"

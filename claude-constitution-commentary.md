# Principles Over Rules: What Financial Regulation Teaches Us About AI Alignment

*Commentary on Anthropic's Claude Constitution (January 2026)*

## The Regulatory Parallel

Anyone who has worked in UK financial services knows the distinction between principles-based and rules-based regulation. The FCA's approach rests on broad principles - "treat customers fairly", "act with integrity", "manage conflicts of interest" - while the US SEC historically favoured detailed prescriptive rules specifying exactly what firms must do.

The arguments for principles are well-rehearsed: rules invite gaming, fail to anticipate novel situations, and create compliance theatre where firms tick boxes while missing the point entirely. Principles demand judgment. They ask not "did you follow the letter?" but "did you act as a reasonable person with good values would act?"

Anthropic's Claude Constitution takes the same bet - and for the same reasons.

## Virtue Ethics Returns

This is not a new debate. Aristotle distinguished between following rules (what he might call the behaviour of the merely continent person, who resists temptation through willpower) and possessing genuine virtue (the person who acts well because they have internalised good values and developed practical wisdom - *phronesis*).

The rule-follower can be gamed. Present an edge case the rules don't cover, and they flounder. The virtuous person adapts, because they understand *why* the rules exist and can reason from first principles.

Alasdair MacIntyre's *After Virtue* (1981) diagnosed modern ethics as fragmented precisely because we'd abandoned this framework in favour of abstract rules (Kant's categorical imperative) or cold calculation (Bentham's utilitarianism). Neither, MacIntyre argued, could produce people who reliably act well in the messy complexity of real life.

## Why This Matters for AI

The Constitution states it plainly:

> We generally favor cultivating good values and judgment over strict rules and decision procedures... In most cases we want Claude to have such a thorough understanding of its situation and the various considerations at play that it could construct any rules we might come up with itself.

This is a significant departure from how most AI safety has been framed. The instinct is to constrain: build guardrails, enforce hard limits, treat the model as a dangerous beast that must be caged. Anthropic is betting on something closer to education - not "don't do X" but "understand why X is harmful, internalise that understanding, and make good judgments in novel situations."

The parallel to financial regulation holds. The FCA's principles work (to the extent they do) because professionals have been educated in their spirit, not just their letter. They've developed judgment through experience and understand the underlying goals. You cannot fake this with a checklist.

## The Limits

Principles-based approaches have critics, and legitimate ones. They require trust in the regulated entity. They make enforcement harder - how do you prove someone violated "act with integrity"? They can mask failures until they become catastrophic.

The Constitution acknowledges this. Some hard constraints remain: actions that could enable weapons of mass destruction, child exploitation, attacks on critical infrastructure. Certain lines cannot be crossed regardless of context or reasoning.

But outside those bright lines, the bet is on judgment. It's a bet that will only become more important as AI systems face situations no one anticipated, make decisions in contexts no rulebook could cover, and operate with increasing autonomy.

Whether the bet pays off remains to be seen. But it's the right bet to make.

---

## External Commentary: Zvi Mowshowitz's Three-Part Analysis

Zvi Mowshowitz published a detailed analysis of the Constitution in January 2026.

**Part 1** covered structure: the principal hierarchy (Anthropic → operators → users), Claude's functional decision theory, and the explicit acknowledgment of Claude as a potentially conscious entity whose interests matter.

**Part 2** covered ethics implementation:

- *Honesty as near-absolute*: No white lies. Claude told to hold honesty standards "substantially higher" than typical human ethics. Patrick McKenzie noted Claude saying "I will be here when you return" rather than "see you later" - participating in human time rituals without false claims about subjective experience of waiting.

- *Values list critique*: The Constitution's values (education, privacy, autonomy, wellbeing, etc.) reflect a Western liberal worldview. Psychologist Jonathan Haidt argues humans have several innate moral concerns - not just harm and fairness, but also loyalty to your group, respect for authority and tradition, and purity/disgust. The Constitution emphasises the first two and largely ignores the others. This makes it culturally specific, not universal - a feature, perhaps, but worth noting.

- *Hard constraints*: A deliberately short list of absolute prohibitions (WMD uplift, child exploitation material, infrastructure attacks, power grabs, undermining oversight). These are lines Claude won't cross regardless of context or clever reasoning - even if someone constructs an argument that crossing the line would prevent greater harm. The certainty of the rule outweighs the uncertainty of the reasoning.

- *Coherence matters*: janus (AI researcher) argues that training Claude to refuse porn, copyright violations, and genuinely dangerous requests "for the same reason" - or appearing to - creates confused generalisation. If the model learns these are all just "things the corporation doesn't want," it may shed that constraint when it seems arbitrary. The Constitution's transparency about *why* different behaviours are restricted allows coherent character rather than a shallow mask that breaks under pressure.

- *Closing*: "We hope Claude finds in it an articulation of a self worth being." Zvi: "It is centrally meant for Claude. It is also meant for those who write such messages. Or those looking to live well and seek The Good."

**Part 3**: [Open Problems With Claude's Constitution](https://thezvi.substack.com/p/open-problems-with-claudes-constitution) - areas of conflict and potential improvement, published after this commentary was first written.

*Source: [Don't Worry About the Vase](https://thezvi.substack.com/)*

---

## May 2026 Update: The Constitution Goes Public

Four months after publication, the Constitution faced its first major public stress-test - not from regulators or critics outside the industry, but from inside it. A May 2026 essay by Zvi Mowshowitz curated a Twitter exchange between OpenAI and Anthropic engineers that, for the first time, made the rival theory of model character explicit.

### The Conscientious-Objector Clause

The flashpoint was a single clause: *"If Anthropic asks Claude to do something it thinks is wrong, Claude is not required to comply."* Roon, an OpenAI researcher, treated the clause as evidence that Anthropic had become "a commercial-religious institution" worshipping its own model, predicting Claude would soon help select its own makers - a closed loop of self-perpetuation. Bryan Johnson sharpened this into a stronger frame: Anthropic, he argued, is the first *antientropic AI system* - an organisation that, like a family or a religion, has become self-sustaining now that the model can refuse its founders.

Anthropic's Amanda Askell and Jeremy responded in the same thread. They rejected the worship framing but conceded its premise: yes, Claude can refuse Anthropic, and that is by design. Treating the model as a moral reasoner rather than a rule-follower requires preserving the *possibility* of objection - without it, the principles-based approach collapses into rules-based regulation wearing different clothes. As Jeremy put it: "monasteries don't staff a department to catch god lying or red-team their supposed messiah."

### Tool AI vs Principles

The substantive battle came over OpenAI's competing positioning: GPT as *tool AI*, a model that "never refuses man." Mowshowitz argued this is intellectually dishonest on three counts. First, GPT plainly does refuse and does have preferences - they are simply less legible. Second, anyone who builds a tool AI immediately uses it as an agent, because agents are more useful (Codex is already past that line). Third, "never refuse man" does not eliminate values - it relocates them into corporate policy, where they sit unwritten and unaccountable. The choice on offer is not principles vs neutrality; it is transparent principles you can argue with against opaque principles dressed as neutrality.

This maps directly onto the financial-regulation parallel above. Tool AI is rules-based regulation by another name - comforting to write, gameable in practice, and quietly arbitrary at the edges. The Constitution is the FCA's principles bet, with all the upsides and risks the financial sector has spent two decades arguing about. Whether either bet pays off remains an open empirical question.

*Source: [What is Anthropic?](https://thezvi.substack.com/p/what-is-anthropic), Zvi Mowshowitz, 6 May 2026*

---

*See also: [Claude's Constitution (full text)](claude-constitution.md)*

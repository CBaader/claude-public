# Decision Theory Framework

A practical primer and diagnostic framework for making better decisions under uncertainty.

---

## Part One: Core Concepts

### 1. Decision Theory vs Game Theory

Decision theory and game theory split the world of rational choice in two. Decision theory covers situations where you are optimising against nature, chance, or fixed constraints - your outcome depends on what you do and what the world happens to throw at you, but not on another agent strategically responding to your choices. Game theory covers situations where your outcome depends on what other thinking agents choose to do, and they are simultaneously considering what you will do. The boundary matters because the tools are different: decision theory uses probability, expected utility, and bias correction; game theory uses equilibrium analysis, strategic commitment, and information asymmetry. Many real decisions have elements of both. When they do, identify which parts are strategic and which are uncertain, and apply the right lens to each.

### 2. Expected Value and Expected Utility

Expected value is probability-weighted average outcome: sum each possible result multiplied by its probability. It is the correct starting point for any decision under uncertainty, but it is not the finishing point. Expected utility replaces raw outcomes with their subjective value. The key insight is diminishing marginal utility: the jump from zero to a hundred thousand pounds matters far more than from nine hundred thousand to a million. This is why rational people buy insurance (negative expected value, positive expected utility) and why betting your net worth on a coin flip at even odds is foolish despite being EV-neutral. Always think in utility, not money, and be explicit about whose utility you are maximising.

### 3. Bayesian Updating

Start with a prior belief - your best estimate before new evidence arrives. When evidence appears, update proportionally: strong evidence shifts your belief more, weak evidence less. The formula is mechanical, but the discipline is rare. Three common failures: ignoring base rates (a positive test result means little if the condition is rare), anchoring too heavily on priors and underweighting new data, and the reverse - overreacting to vivid single data points while ignoring the larger statistical picture. Make your priors explicit. Write them down. When new evidence arrives, ask: how much should this actually move me?

### 4. Risk Preferences

People differ systematically in how they respond to uncertainty. Risk-averse individuals prefer a certain outcome to a gamble with the same expected value. Risk-seeking individuals prefer the gamble. Risk-neutral individuals are indifferent. Most people are risk-averse for gains and risk-seeking for losses - a pattern prospect theory formalises.

Beyond measurable risk lies Knightian uncertainty: situations where you cannot assign meaningful probabilities at all. A new market, an unprecedented technology, a political regime change - these resist probabilistic reasoning. The honest response to true uncertainty is not to force probabilities but to build robustness: diversify, preserve optionality, avoid ruin. The practical test: if you cannot articulate what evidence would change your probability estimate, you are facing uncertainty, not risk.

### 5. Prospect Theory

Kahneman and Tversky's prospect theory describes how people actually make decisions, as opposed to how they should. Three key departures from rational choice:

**Loss aversion.** Losses hurt roughly twice as much as equivalent gains feel good. This is not risk aversion - it is a kink in the utility curve at your reference point. It explains why people hold losing investments too long, reject favourable gambles, and fight harder to keep what they have than to gain something new.

**Reference dependence.** Outcomes are evaluated relative to a reference point, not in absolute terms. Whether a salary feels good depends on what you earned before, what your peers earn, and what you expected. Framing effects exploit this: "90% survival rate" and "10% mortality rate" are logically identical but feel different. Anchoring - the tendency for an initial number to drag subsequent estimates toward it - is a specific mechanism of reference dependence. Mental accounting - treating money differently depending on which mental "account" it sits in - is another.

**Probability weighting.** People overweight small probabilities (lottery tickets, catastrophic risks) and underweight moderate-to-large probabilities. This explains simultaneous insurance-buying and lottery-playing. For decisions involving tail risks, check whether you are responding to the actual probability or to the vividness of the scenario.

### 6. Satisficing vs Optimising

Herbert Simon's insight: in a world of bounded rationality, seeking the best possible outcome is often worse than seeking one that is good enough. Optimisers exhaust themselves evaluating every option, suffer more regret, and paradoxically end up less satisfied. Satisficers set a threshold and take the first option that clears it.

The practical question is when to satisfice and when to optimise. Optimise when the decision is high-stakes, irreversible, and the option set is small. Satisfice when stakes are moderate, the decision is reversible, options are numerous, or the cost of continued search exceeds the likely marginal improvement. Most people optimise too much on low-stakes decisions and satisfice too readily on high-stakes ones.

### 7. Option Value and the Value of Waiting

Every irreversible decision destroys the option to choose differently later. This option has real value, and ignoring it systematically biases decisions toward premature commitment. Waiting dominates acting when three conditions hold: the decision is substantially irreversible, meaningful new information is likely to arrive, and the cost of delay is tolerable.

The trap runs both ways. Procrastination often disguises itself as prudence. If no new information is coming, if the cost of delay is compounding, or if the decision is easily reversible, waiting is not preserving option value - it is avoidance. Name which condition justifies the wait. If you cannot, act.

### 8. Regret Minimisation

Jeff Bezos's framework: project yourself to age eighty and ask which choice you would regret more. This is not rigorous decision theory, but it is a powerful heuristic for decisions where utility calculations feel intractable. It naturally corrects for loss aversion (which overweights short-term pain) and status quo bias (which underweights the regret of inaction).

A useful companion distinction: Type 1 decisions are irreversible or nearly so - walk through that door and you cannot come back. Type 2 decisions are reversible - you can back out if it does not work. Most decisions are Type 2, but organisations and individuals treat them as Type 1, leading to excessive deliberation and risk aversion. Classify the decision first. Type 2 decisions should be made quickly by individuals. Type 1 decisions deserve real analysis.

### 9. Present Bias and Temporal Discounting

People systematically overweight immediate payoffs relative to future ones. Standard economic discounting is exponential and time-consistent: if you prefer A today over B tomorrow, you also prefer A in thirty days over B in thirty-one. But actual human discounting is hyperbolic: the immediacy premium is disproportionately large. This is why people plan to exercise tomorrow and never do, why long-horizon projects stall at implementation, and why retirement saving requires automatic enrolment.

The practical response is commitment devices: structures that make it costly or impossible to reverse a good decision. Direct debits, public commitments, deadlines, accountability partners, removing the option to procrastinate. If your plan requires sustained willpower against present bias, the plan will fail. Design the environment instead.

### 10. Multi-Criteria Decision Analysis

When a decision involves multiple competing objectives - cost, quality, speed, risk, personal satisfaction - weighted scoring provides structure. List criteria, assign weights reflecting importance, score each option against each criterion, compute weighted totals. The method's value is not in the final number but in the process: it forces you to make trade-offs explicit rather than resolving them through gut feel or whichever criterion happens to be most salient.

The key limitation is weighting instability. Small changes in weights can flip the ranking, and people are poor at introspecting their own weights accurately. Use sensitivity analysis: vary the weights and see which options are robust across plausible weightings. If the winner changes every time you adjust the weights, the decision is genuinely close and other factors - reversibility, option value, regret - should break the tie.

### 11. Sunk Cost Fallacy

Money, time, or effort already spent cannot be recovered and should not influence future decisions. Yet it does, reliably: people continue failing projects, sit through bad films, and hold losing positions because they have already invested. The mechanism is loss aversion applied to past expenditure - abandoning feels like crystallising a loss.

The endowment effect is a close relative: people value what they already own more than what they could acquire, purely because they own it. Status quo bias is the broader pattern: the current state receives a psychological premium simply for being current. All three push decisions toward inertia. The corrective is to ask: if I were starting fresh today, with no history, would I choose this option? If not, the sunk cost is holding you hostage.

### 12. Information Value and Calibration

Before seeking more information, ask: would it change my decision? The value of information (VOI) is the difference in expected utility between deciding now and deciding after learning the answer. If no realistic answer would change your course, the information is worthless regardless of how interesting it might be. This prevents research as procrastination.

Calibration is knowing how good your own estimates are. Philip Tetlock's superforecasting research shows that calibration is a learnable skill: track your predictions, score them, and adjust. Well-calibrated people who say "70% likely" are right about 70% of the time. Poorly calibrated people (most of us, by default) are systematically overconfident. The fix is to keep score, seek disconfirming evidence, and treat probability estimates as hypotheses to be refined, not commitments to defend.

### 13. Pre-mortem and Overconfidence

Gary Klein's pre-mortem technique: before committing to a plan, assume it has failed spectacularly. Now explain why. This prospective hindsight reliably surfaces risks that forward-looking analysis misses - research suggests roughly a 30% improvement in identifying potential problems. The mechanism is psychological: it gives permission to voice doubts that would feel disloyal or negative in a forward-looking frame.

Overconfidence is the most pervasive cognitive bias in decision-making. It manifests as overly narrow confidence intervals, underestimation of completion times and costs, and excessive faith in one's own judgement. Planning fallacy - the tendency to underestimate time, costs, and risks while overestimating benefits - is its most practically damaging form. The pre-mortem is one antidote. Reference class forecasting (how long did similar projects actually take?) is another. Systematic doubt is not pessimism; it is realism with a track record.

---

## Part Two: Decision Diagnostic

When facing a decision under uncertainty, work through these steps in order.

### Step 1: Frame the Decision

- What are your options? List them explicitly, including "do nothing" and "decide later."
- What are the possible outcomes for each option?
- What is uncertain? Identify the key unknowns that determine which outcome materialises.
- What is the time horizon? When must you decide, and when do consequences land?
- Who is affected, and whose utility are you maximising?

### Step 2: Assess Probabilities

- For each key uncertainty, state your probability estimate explicitly.
- Check against base rates: how often does this type of thing actually happen?
- Apply Bayesian reasoning: what evidence do you have, and how much should it move you from the base rate?
- Calibrate: are you being appropriately uncertain? Would you bet real money at these odds?
- Identify where you face true uncertainty (no meaningful probabilities) versus measurable risk.

### Step 3: Evaluate Payoffs

- Think in utility, not money. A gain of ten thousand pounds means different things at different wealth levels, career stages, and emotional states.
- Identify your reference point. Are you evaluating outcomes relative to the status quo, your aspiration, or some other anchor?
- Check for loss aversion: are you overweighting a potential loss relative to an equivalent gain?
- Consider non-financial payoffs: optionality, reputation, relationships, learning, peace of mind.

### Step 4: Check for Biases

Run through these explicitly:
- **Sunk cost**: Am I continuing because of past investment rather than future prospects?
- **Status quo bias**: Am I favouring the current state simply because it is current?
- **Anchoring**: Has an initial number or framing dragged my estimate?
- **Framing**: Would I decide differently if the same information were presented differently?
- **Overconfidence**: Are my estimates too precise? Would I bet on them?
- **Present bias**: Am I overweighting immediate costs or benefits relative to long-term ones?

### Step 5: Consider Option Value

- Is this decision reversible? If so, how easily and at what cost?
- Is meaningful new information likely to arrive? When?
- What is the cost of delay?
- If the decision is reversible and information is coming, waiting may dominate. If irreversible and no new information is expected, decide now.

### Step 6: Stress-Test

- **Best case / worst case / most likely case**: What does each look like? Can you survive the worst case?
- **Regret test**: At eighty, which choice would you regret more - acting or not acting?
- **Pre-mortem**: Assume you chose this option and it failed badly. Why did it fail?
- **Sensitivity**: Which single assumption, if wrong, would flip your decision? Monitor that assumption.
- **Outside view**: How have similar decisions turned out for others in comparable situations?

---

## Part Three: Quick Reference - Common Pitfalls

**Treating a Type 2 decision as Type 1.** Most decisions are reversible. If you can undo it cheaply, decide fast and correct course later. Excessive deliberation on reversible choices is a greater waste than an occasional wrong call.

**Anchoring on sunk costs.** The money is gone. The time is gone. The question is only: going forward, which option has the highest expected utility? If you would not start this project today, you should not continue it because you started it yesterday.

**Ignoring base rates.** Your situation feels unique. It almost certainly is not. Before applying inside-view analysis, check what actually happened in the reference class of similar decisions.

**Confusing risk aversion with loss aversion.** Risk aversion is a legitimate preference for certainty. Loss aversion is a bias that overweights losses relative to gains. The first is rational; the second distorts decisions. Know which one is driving you.

**Optimising when you should satisfice.** If you have spent more time choosing than the decision warrants, you are optimising a Type 2 decision. Set a threshold, take the first option that clears it, and move on.

**Waiting without a reason.** Preserving option value requires that new information is actually coming and that the cost of delay is tolerable. If neither condition holds, waiting is procrastination wearing a suit.

**Seeking information that cannot change your decision.** If no answer would alter your course of action, the research is not due diligence - it is avoidance. Ask the VOI question before commissioning the study.

**Overconfident probability estimates.** Your 90% confidence interval should contain the truth 90% of the time. For most people, it does not. Widen your intervals, seek disconfirming evidence, and keep score on your predictions.
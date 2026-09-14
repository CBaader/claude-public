# Game Theory Decision Framework

A practical primer and diagnostic framework for applying game theory to real decisions.

---

## Part One: Core Concepts

### 1. Is This Actually a Game?

A situation is a strategic game when your outcome depends not just on what you do, but on what others do. If you're optimising against nature or fixed constraints, it's a decision problem, not a game. The distinction matters: decision problems need expected-value thinking; games need strategic thinking.

### 2. Players

Identify every actor whose choices affect your outcome. Include players who seem passive - they may be choosing inaction strategically. Consider whether a single entity (a company, a regulator, a family) is really one player or several with different incentives.

### 3. Strategies

A strategy is a complete plan of action: what you will do in every possible situation you might face. Don't confuse a strategy with a single move. In sequential games, your strategy must specify what you'd do at every decision point, including ones you hope never to reach.

### 4. Payoffs

Payoffs encode what each player actually cares about. Be honest about your own: money, reputation, time, relationships, optionality, and peace of mind are all legitimate payoffs. Other players' payoffs are harder to assess but essential - misreading them is the most common source of strategic error.

### 5. Sequential vs Simultaneous

If players move in turn and can observe prior moves, analyse by backward induction: start at the end and work backwards. If players move without knowing what others have chosen, analyse by looking for dominant strategies, then Nash equilibria. Most real situations combine both.

### 6. Nash Equilibrium

A set of strategies where no player can improve their outcome by changing their own strategy alone. This is the resting point of rational play. Key caveats: there may be multiple equilibria (coordination problem), the equilibrium may be inefficient (prisoners' dilemma), and reaching equilibrium assumes players are rational and believe others are too.

### 7. Dominant and Dominated Strategies

If one strategy is always better regardless of what others do, it dominates. If one strategy is always worse, it's dominated. Eliminate dominated strategies first - this often simplifies the problem dramatically. If you have a dominant strategy, play it. If your opponent has one, assume they'll play it.

### 8. Focal Points

When a game has multiple equilibria, how do players coordinate without communication? Thomas Schelling showed that they converge on focal points: outcomes that are salient, prominent, or "obvious" given shared context. The salience is cultural, not mathematical - round numbers in salary negotiations, industry-standard pricing tiers, established conventions in jurisdictional disputes, the dominant platform in a standards battle. Focal points explain why coordination often succeeds in practice despite the theoretical prediction of indeterminacy. They also create strategic opportunity: if you can frame the situation so that your preferred outcome becomes the obvious one, you win the coordination game without overt negotiation. The practical lesson is to invest in understanding shared context - what the other side considers natural, default, or expected - because that is where coordination will gravitate.

### 9. Mixed Strategies

When no pure strategy is reliably best, randomising can be optimal. This applies most in competitive (zero-sum) situations: negotiations, pricing, timing. The practical lesson isn't to literally roll dice; it's to be unpredictable and to recognise when your opponent benefits from unpredictability.

### 10. Information Structure

What does each player know, and when? Key distinctions:

- **Complete vs incomplete information**: Do you know the other players' payoffs and capabilities?
- **Perfect vs imperfect information**: Can you observe all previous moves?
- **Symmetric vs asymmetric information**: Does one side know something the other doesn't?

Asymmetric information drives most real-world strategic complexity. Four patterns recur:

- **Adverse selection** (hidden characteristics, before the deal): one side knows something the other can't observe before committing. Insurance attracts the high-risk; second-hand markets are flooded by sellers who know their goods are lemons. The uninformed side prices defensively, which drives away good types, which worsens the pool.
- **Moral hazard** (hidden actions, after the deal): once committed, one side behaves differently because the other can't observe their effort or care. The insured take more risks; the salaried employee coasts. Solutions include monitoring, performance-linked pay, and reputation effects.
- **Signalling** (informed party acts to reveal type): the signal must be costly enough that only the genuine type would send it. A degree signals ability because completing one is harder for weaker candidates. A firm pays dividends to signal financial health. The cost is the point - cheap signals are ignored.
- **Screening** (uninformed party designs choices that force revelation): instead of waiting for signals, you offer a menu where different types self-select. An insurer offering high-premium/low-deductible versus low-premium/high-deductible plans separates cautious from reckless. Employers offering fixed salary versus commission-heavy pay do the same.

### 11. Credibility and Commitment

A threat or promise only works if the other side believes you'll follow through. Credibility requires that carrying out the action is in your interest once the moment arrives. Ways to make commitments credible: restrict your own options, change your own payoffs (contractually, reputationally), delegate to someone with different incentives, or build reputation through repeated play.

### 12. Repeated Interaction

One-shot games and repeated games produce radically different behaviour. In repeated play, cooperation can be sustained because players can punish defection in future rounds. The key variable is the shadow of the future: how much weight players place on future payoffs relative to present ones. If the relationship has a known endpoint, cooperation unravels from the end backwards (though in practice, uncertainty about the endpoint often sustains it).

### 13. Collective Action and the Prisoners' Dilemma

When individually rational behaviour leads to collectively bad outcomes, you have a social dilemma. The prisoners' dilemma is the archetype, but chicken (who swerves first?) and assurance (I'll cooperate if you will) are equally common. Each has different solutions: dilemmas need enforcement or punishment; chicken needs commitment devices; assurance needs communication and trust.

### 14. Bargaining

Division of surplus between parties who both benefit from agreement but prefer different terms. Key factors: outside options (your best alternative to a negotiated agreement - the walk-away outcome if no deal is reached), patience (who can wait longer and bear the cost of delay?), information (who knows more about the true value at stake?), and commitment power (who can credibly lock in a position?). The party with the stronger outside option, more patience, or better information captures more of the surplus. Knowing your own walk-away point with precision, and estimating the other side's, is the single most important piece of preparation for any negotiation.

### 15. Mechanism Design

Instead of playing within given rules, can you design the rules? Auctions, contracts, incentive schemes, and organisational structures are all mechanism design. The core question: what rules will cause self-interested players to produce the outcome you want?

---

## Part Two: Decision Diagnostic

When facing a strategic decision, work through these steps in order.

### Step 1: Frame the Game

- Who are the players? List them. Include anyone whose actions affect your outcome.
- What does each player want? State their payoffs explicitly. Where you're uncertain, identify your best guess and note the uncertainty.
- What are each player's available strategies? Be specific and exhaustive.
- Is the interaction sequential, simultaneous, or both?
- Is this a one-shot interaction or part of an ongoing relationship?
- What information does each player have? What's hidden?

### Step 2: Identify the Game Type

Most real situations map onto a small number of canonical games:

- **Prisoners' dilemma**: Both sides would benefit from cooperation, but each has an individual incentive to defect. Look for enforcement, repetition, or reputation as solutions.
- **Coordination / assurance**: Both sides want to coordinate but aren't sure the other will. Communication, focal points, and credible signals help.
- **Chicken**: Both sides prefer the other to back down, but mutual escalation is catastrophic. Commitment and brinkmanship are the tools.
- **Battle of the sexes**: Both prefer agreement to disagreement, but disagree on which agreement. Bargaining power, precedent, and side payments matter.
- **Zero-sum competition**: Your gain is their loss. Unpredictability (mixed strategies) and information advantages are key.
- **Principal-agent**: One party delegates to another with different incentives. Contract design, monitoring, and incentive alignment are the tools.
- **Signalling / screening**: One party has private information the other wants to infer. Costly signals, menu design, and reputation matter.

### Step 3: Analyse Equilibria

- Does any player have a dominant strategy? If you do, play it. If they do, assume they will.
- Eliminate dominated strategies iteratively.
- Identify Nash equilibria. If there are multiple, assess which is most likely given context, history, and focal points.
- In sequential games, apply backward induction. Check whether threats and promises are credible.
- If the game is repeated, assess whether cooperation can be sustained and what triggers or punishments would support it.

### Step 4: Assess Your Strategic Options

- **Commitment**: Can you credibly commit to a course of action to change the other player's best response?
- **Information**: Can you acquire, reveal, or conceal information to shift the game in your favour?
- **Timing**: Is there a first-mover or second-mover advantage? Can you change the order of play?
- **Framing**: Can you redefine the game - change the players, strategies, payoffs, or rules?
- **Coalition**: Can you bring in additional players or form alliances to shift the balance?
- **Exit**: Is walking away your strongest move? What's your best alternative if no agreement is reached?

### Step 5: Stress-Test

- What assumptions are you making about other players' payoffs and rationality? What if those are wrong?
- What's the worst-case outcome? Can you survive it?
- Are you confusing a one-shot game with a repeated one, or vice versa?
- Are you overweighting your own perspective? What does this look like from the other side?
- Is there a simpler explanation for the other player's behaviour than strategic calculation?
- Have you accounted for the possibility that the other player is also trying to change the game?

---

## Part Three: Quick Reference - Common Pitfalls

**Assuming your opponent is irrational when they simply have different payoffs.** The most common strategic error. Before concluding someone is acting irrationally, check whether they might value things you haven't considered.

**Ignoring credibility.** Threats and promises are cheap. Ask: if the moment came, would they actually follow through? Would you?

**Failing to think forward.** In sequential games, the move that looks best now may lead to a terrible position later. Always reason from the endgame backwards.

**Neglecting the repeated nature of the interaction.** Burning someone in a one-shot feels different when you'll face them again next quarter. Reputation is a strategic asset.

**Overcomplicating the analysis.** Most real decisions involve two or three key players and a handful of strategies. If your game tree has fifty nodes, you've probably lost the forest for the trees. Simplify ruthlessly, then check whether what you removed actually matters.

**Confusing the map for the territory.** Game theory is a lens, not reality. Players are not perfectly rational, information is messier than models assume, and payoffs are rarely precise. Use the framework to structure thinking, not to generate false precision.

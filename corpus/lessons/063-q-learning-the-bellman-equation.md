---
title: "06.3 — Q-Learning & The Bellman Equation"
subject: "Behavioral Psychology & Reinforcement Learning"
catalog: advanced
audience_tier: higher-education
chapter: "6.3"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 06.3 — Q-Learning & The Bellman Equation

> *"An optimal policy has the property that whatever the initial state and initial decision are, the remaining decisions must constitute an optimal policy with regard to the state resulting from the first decision."*
> — Richard Bellman, *Dynamic Programming* (1957)

> *"Q-learning… learns the value of the optimal policy independently of the agent's actions."*
> — Christopher Watkins, *Learning from Delayed Rewards* (1989)

This chapter formalizes the full reinforcement learning framework: Markov Decision Processes, the Bellman equations (expectation and optimality), and the Q-learning algorithm that converges to optimal behavior without a model of the environment. We derive everything from first principles and connect it to the behavioral conditioning framework of Chapters 12.1–12.2.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define a Markov Decision Process (MDP) and identify its components in behavioral experiments.
2. Derive the Bellman Expectation Equation for $V^\pi$ and $Q^\pi$.
3. Derive the Bellman Optimality Equation and explain why it characterizes $\pi^*$.
4. Implement Q-learning with $\epsilon$-greedy exploration on a gridworld.
5. Prove Q-learning convergence under Robbins-Monro conditions.
6. Compute Q-value updates by hand for small MDPs.
7. Connect Q-learning to operant conditioning: $Q(s,a)$ as the "learned value of an action in context."

---

## 🖼️ Visual Anchor — Gridworld with Optimal Policy

![psych-06__fig3](psych-06__fig3.svg)

---

## 📚 1. Definitions

### Definition 06.3.1 — Markov Decision Process (MDP)

A **Markov Decision Process** is a tuple $\mathcal{M} = (S, A, P, R, \gamma)$ where:

- $S$ = finite set of states
- $A$ = finite set of actions
- $P(s'|s,a)$ = state transition probability: $\Pr(s_{t+1} = s' \mid s_t = s, a_t = a)$
- $R(s,a,s')$ = reward function (or $R(s,a)$ = expected reward)
- $\gamma \in [0,1)$ = discount factor

The **Markov property**: $\Pr(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, \ldots) = \Pr(s_{t+1} | s_t, a_t)$. The future depends only on the present state and action, not the history.

### Definition 06.3.2 — Policy $\pi$

A **policy** maps states to action probabilities:

$$
\pi(a|s) = \Pr(a_t = a \mid s_t = s)
$$

A **deterministic policy**: $\pi(s) = a$ (one action per state).

### Definition 06.3.3 — State-Value Function $V^\pi(s)$

The expected return starting from state $s$ and following policy $\pi$:

$$
V^\pi(s) = E_\pi\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k} \mid s_t = s\right]
$$

### Definition 06.3.4 — Action-Value Function $Q^\pi(s,a)$

The expected return starting from state $s$, taking action $a$, then following $\pi$:

$$
Q^\pi(s,a) = E_\pi\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k} \mid s_t = s, a_t = a\right]
$$

Relationship: $V^\pi(s) = \sum_a \pi(a|s) Q^\pi(s,a)$

### Definition 06.3.5 — Optimal Value Functions

$$
V^*(s) = \max_\pi V^\pi(s) \quad \forall s
$$

$$
Q^*(s,a) = \max_\pi Q^\pi(s,a) \quad \forall s, a
$$

The optimal policy satisfies: $\pi^*(a|s) = 1$ if $a = \arg\max_{a'} Q^*(s,a')$.

### Definition 06.3.6 — $\epsilon$-Greedy Policy

$$
\pi_\epsilon(a|s) = \begin{cases} 1 - \epsilon + \frac{\epsilon}{|A|} & \text{if } a = \arg\max_{a'} Q(s,a') \\ \frac{\epsilon}{|A|} & \text{otherwise} \end{cases}
$$

With probability $1-\epsilon$: exploit (choose best known action). With probability $\epsilon$: explore (choose random action).

### Definition 06.3.7 — Off-Policy Learning

Learning about one policy (the **target policy** $\pi$) while following a different policy (the **behavior policy** $b$). Q-learning is off-policy: it learns $Q^*$ (the optimal policy's values) while following $\pi_\epsilon$ (an exploratory policy).

---


## 🔬 2. Behavioral Mechanisms

### 2.1 From Skinner Box to MDP

The Skinner box is a physical implementation of an MDP:

| MDP Component | Skinner Box Analog |
|---|---|
| State $s$ | Environmental configuration (light on/off, lever position, time since last reward) |
| Action $a$ | Behavioral response (press lever, nose-poke, do nothing) |
| Transition $P(s'|s,a)$ | Physical consequences of action (lever press → food delivery mechanism) |
| Reward $R(s,a)$ | Reinforcement/punishment (food pellet = +1, shock = −1) |
| Discount $\gamma$ | Temporal myopia (how much the animal values future vs. immediate reward) |
| Policy $\pi$ | The animal's learned behavioral strategy |

### 2.2 Exploration vs. Exploitation in Animal Behavior

Animals naturally implement $\epsilon$-greedy-like strategies:

- **Exploitation:** Repeating actions that previously yielded reward (habit formation, dorsal striatum).
- **Exploration:** Trying novel actions or visiting unfamiliar locations (curiosity, hippocampal novelty detection).

The balance is modulated by:
- **Norepinephrine** (locus coeruleus): increases exploration under uncertainty.
- **Tonic dopamine:** higher levels → more exploratory behavior.
- **Stress/threat:** shifts toward exploitation of known-safe behaviors (reduced $\epsilon$).

### 2.3 Model-Based vs. Model-Free in the Brain

The brain implements **both** strategies:

- **Model-free (habitual):** Dorsal striatum stores cached Q-values. Fast but inflexible. Corresponds to Q-learning.
- **Model-based (goal-directed):** Prefrontal cortex + hippocampus simulate future states. Slow but flexible. Corresponds to planning/tree search.

Evidence: Outcome devaluation experiments. After extensive training, rats continue pressing a lever for food even after the food is paired with nausea (model-free habit). Early in training, they immediately stop (model-based, goal-directed).

---

## 📐 3. Mathematical Formulations

### 3.1 Bellman Expectation Equation — Derivation

**For $V^\pi$:**

Starting from the definition:

$$
V^\pi(s) = E_\pi\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k} \mid s_t = s\right]
$$

Separate the first reward from the rest:

$$
V^\pi(s) = E_\pi\left[r_t + \gamma \sum_{k=0}^{\infty} \gamma^k r_{t+1+k} \mid s_t = s\right]
$$

The inner sum is $V^\pi(s_{t+1})$:

$$
V^\pi(s) = E_\pi\left[r_t + \gamma V^\pi(s_{t+1}) \mid s_t = s\right]
$$

Expanding the expectation over actions and transitions:

$$
V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) \left[R(s,a,s') + \gamma V^\pi(s')\right]
$$

This is a system of $|S|$ linear equations in $|S|$ unknowns — solvable exactly for small MDPs.

**For $Q^\pi$:**

$$
Q^\pi(s,a) = \sum_{s'} P(s'|s,a) \left[R(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')\right]
$$

### 3.2 Bellman Optimality Equation — Derivation

The optimal value function satisfies:

$$
V^*(s) = \max_a Q^*(s,a)
$$

Substituting the Bellman expectation equation with the optimal policy (which always picks the best action):

$$
V^*(s) = \max_a \sum_{s'} P(s'|s,a) \left[R(s,a,s') + \gamma V^*(s')\right]
$$

**For $Q^*$:**

$$
Q^*(s,a) = \sum_{s'} P(s'|s,a) \left[R(s,a,s') + \gamma \max_{a'} Q^*(s',a')\right]
$$

This is the **Bellman optimality equation for Q**. It states: the value of taking action $a$ in state $s$ equals the expected immediate reward plus the discounted value of the best action in the next state.

**Key property:** This is a fixed-point equation. $Q^*$ is the unique fixed point of the Bellman optimality operator:

$$
(T^* Q)(s,a) = \sum_{s'} P(s'|s,a) \left[R(s,a,s') + \gamma \max_{a'} Q(s',a')\right]
$$

### 3.3 Q-Learning Algorithm — Derivation

**Problem:** We don't know $P(s'|s,a)$ or $R(s,a,s')$. We can only observe samples $(s_t, a_t, r_t, s_{t+1})$.

**Solution:** Replace the expectation in the Bellman optimality equation with a sample-based stochastic approximation:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[\underbrace{r_t + \gamma \max_{a'} Q(s_{t+1}, a')}_{\text{sample Bellman target}} - Q(s_t, a_t)\right]
$$

**Expanding:**

$$
Q(s_t, a_t) \leftarrow (1-\alpha) Q(s_t, a_t) + \alpha \left[r_t + \gamma \max_{a'} Q(s_{t+1}, a')\right]
$$

This is a weighted average of the old estimate and the new sample target.

**Why "off-policy":** The update uses $\max_{a'}$ regardless of which action the agent actually takes next. The agent can follow any exploratory policy (e.g., $\epsilon$-greedy) while still learning the optimal Q-values.

### 3.4 Convergence Proof (Sketch)

**Theorem (Watkins & Dayan, 1992):** Q-learning converges to $Q^*$ with probability 1 if:

1. All state-action pairs are visited infinitely often.
2. Learning rates satisfy Robbins-Monro: $\sum_t \alpha_t(s,a) = \infty$, $\sum_t \alpha_t^2(s,a) < \infty$.
3. Rewards are bounded.

**Proof sketch:**

Define the Bellman optimality operator $T^*$:

$$
(T^*Q)(s,a) = E[r + \gamma \max_{a'} Q(s',a') \mid s, a]
$$

**Step 1:** $T^*$ is a $\gamma$-contraction in the max-norm:

$$
\|T^*Q_1 - T^*Q_2\|_\infty \leq \gamma \|Q_1 - Q_2\|_\infty
$$

*Proof of contraction:*

$$
|(T^*Q_1)(s,a) - (T^*Q_2)(s,a)| = \left|E\left[\gamma\max_{a'}Q_1(s',a') - \gamma\max_{a'}Q_2(s',a')\right]\right|
$$

$$
\leq \gamma E\left[\left|\max_{a'}Q_1(s',a') - \max_{a'}Q_2(s',a')\right|\right]
$$

$$
\leq \gamma E\left[\max_{a'}|Q_1(s',a') - Q_2(s',a')|\right] \leq \gamma \|Q_1 - Q_2\|_\infty
$$

**Step 2:** By Banach fixed-point theorem, $T^*$ has a unique fixed point $Q^*$.

**Step 3:** Q-learning is a stochastic approximation of the iteration $Q \leftarrow T^*Q$. Under Robbins-Monro conditions, stochastic approximation converges to the fixed point. $\blacksquare$

### 3.5 Value Iteration (Planning with Known Model)

When $P$ and $R$ are known, we can compute $Q^*$ directly:

$$
Q_{k+1}(s,a) = \sum_{s'} P(s'|s,a)\left[R(s,a,s') + \gamma \max_{a'} Q_k(s',a')\right]
$$

This converges to $Q^*$ at rate $O(\gamma^k)$ since $T^*$ is a $\gamma$-contraction.

### 3.6 SARSA — On-Policy Alternative

SARSA updates using the **actual next action** $a_{t+1}$ (chosen by the current policy) instead of $\max$:

$$
Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha\left[r_t + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t,a_t)\right]
$$

SARSA converges to $Q^{\pi_\epsilon}$ (the value of the exploratory policy), not $Q^*$. It is more conservative — it accounts for the fact that the agent sometimes explores randomly.

**Key difference from Q-learning:**
- Q-learning: $\text{target} = r + \gamma \max_{a'} Q(s', a')$ — optimistic, assumes optimal future behavior.
- SARSA: $\text{target} = r + \gamma Q(s', a_{t+1})$ — realistic, uses actual next action (which may be exploratory).

**When to use which:**
- Q-learning: when you want to learn the optimal policy regardless of current behavior (off-policy).
- SARSA: when safety matters and you need to account for your own exploration noise (on-policy). Near cliffs/dangers, SARSA learns safer paths because it "knows" it might accidentally explore into danger.

### 3.7 Expected SARSA

A compromise between Q-learning and SARSA:

$$
Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha\left[r_t + \gamma \sum_{a'}\pi(a'|s_{t+1})Q(s_{t+1},a') - Q(s_t,a_t)\right]
$$

This uses the **expected value** under the current policy rather than a single sample. It reduces variance compared to SARSA while remaining on-policy. With a greedy policy ($\epsilon = 0$), Expected SARSA becomes Q-learning.

---


## ✍️ 4. Worked Examples

### Example 06.3.1 — Q-Learning on a 3-State MDP

<details>
<summary>States: {A, B, C(terminal)}. Actions: {left, right}. From A: right→B (r=0), left→A (r=0). From B: right→C (r=+10), left→A (r=0). γ=0.9, α=0.5. Initialize Q=0 everywhere. Simulate 4 episodes of Q-learning with ε=0.3.</summary>

**Episode 1:** A →(right)→ B →(right)→ C. Rewards: 0, 10.

Update B→C (backward from terminal):

$$
Q(B, \text{right}) \leftarrow 0 + 0.5[10 + 0.9 \cdot \max_a Q(C,a) - 0] = 0.5[10 + 0] = 5.0
$$

Update A→B:

$$
Q(A, \text{right}) \leftarrow 0 + 0.5[0 + 0.9 \cdot \max_a Q(B,a) - 0] = 0.5[0 + 0.9(5.0)] = 0.5 \times 4.5 = 2.25
$$

After Episode 1: Q(A,right)=2.25, Q(B,right)=5.0, all others=0.

**Episode 2:** A →(right)→ B →(right)→ C.

$$
Q(B, \text{right}) \leftarrow 5.0 + 0.5[10 + 0 - 5.0] = 5.0 + 2.5 = 7.5
$$

$$
Q(A, \text{right}) \leftarrow 2.25 + 0.5[0 + 0.9(7.5) - 2.25] = 2.25 + 0.5[6.75 - 2.25] = 2.25 + 2.25 = 4.5
$$

**Episode 3:** A →(left, exploring)→ A →(right)→ B →(right)→ C.

$$
Q(A, \text{left}) \leftarrow 0 + 0.5[0 + 0.9 \cdot \max_a Q(A,a) - 0] = 0.5[0.9 \times 4.5] = 2.025
$$

$$
Q(B, \text{right}) \leftarrow 7.5 + 0.5[10 - 7.5] = 7.5 + 1.25 = 8.75
$$

$$
Q(A, \text{right}) \leftarrow 4.5 + 0.5[0 + 0.9(8.75) - 4.5] = 4.5 + 0.5[7.875 - 4.5] = 4.5 + 1.6875 = 6.1875
$$

**Episode 4:** A →(right)→ B →(right)→ C.

$$
Q(B, \text{right}) \leftarrow 8.75 + 0.5[10 - 8.75] = 8.75 + 0.625 = 9.375
$$

$$
Q(A, \text{right}) \leftarrow 6.1875 + 0.5[0 + 0.9(9.375) - 6.1875] = 6.1875 + 0.5[8.4375 - 6.1875] = 6.1875 + 1.125 = 7.3125
$$

**True optimal values:** $Q^*(B,\text{right}) = 10$, $Q^*(A,\text{right}) = 0.9 \times 10 = 9$.

After 4 episodes: Q(B,right)=9.375 (93.75% of true), Q(A,right)=7.3125 (81.25% of true). Converging. ✓

</details>

### Example 06.3.2 — Bellman Equation for a 2×2 Gridworld

<details>
<summary>2×2 grid. States: (0,0), (0,1), (1,0), (1,1)=goal(r=+5, terminal). Actions: up/down/left/right (deterministic, walls bounce back). γ=0.9. Write and solve the Bellman optimality equations.</summary>

**State transitions (deterministic):**
- (0,0): right→(0,1), down→(1,0), up→(0,0), left→(0,0)
- (0,1): down→(1,1)=goal(r=5), left→(0,0), up→(0,1), right→(0,1)
- (1,0): right→(1,1)=goal(r=5), up→(0,0), down→(1,0), left→(1,0)

All non-goal transitions have r=−1 (step cost).

**Bellman optimality equations:**

$$
V^*(0,1) = \max_a Q^*(0,1,a) = \max\{-1 + 0.9 \cdot 0, -1 + 0.9 V^*(0,0), \ldots\}
$$

For (0,1), best action is "down" → goal:

$$
V^*(0,1) = -1 + 0.9 \cdot V^*(\text{goal}) + r_{\text{goal}}
$$

Wait — reward is received on transition TO goal. So:

$$
Q^*(0,1, \text{down}) = 5 + 0.9 \cdot 0 = 5 \quad \text{(reach goal, get +5, terminal)}
$$

$$
Q^*(0,1, \text{left}) = -1 + 0.9 \cdot V^*(0,0)
$$

Similarly:

$$
Q^*(1,0, \text{right}) = 5 + 0 = 5
$$

For (0,0):

$$
V^*(0,0) = \max\{Q^*(0,0,\text{right}), Q^*(0,0,\text{down}), \ldots\}
$$

$$
Q^*(0,0, \text{right}) = -1 + 0.9 \cdot V^*(0,1) = -1 + 0.9(5) = -1 + 4.5 = 3.5
$$

$$
Q^*(0,0, \text{down}) = -1 + 0.9 \cdot V^*(1,0) = -1 + 0.9(5) = 3.5
$$

Therefore: $V^*(0,0) = 3.5$, $V^*(0,1) = 5$, $V^*(1,0) = 5$.

**Optimal policy:** From (0,0): right or down (both equally good). From (0,1): down. From (1,0): right.

</details>

### Example 06.3.3 — ε-Greedy Exploration: Avoidance Trap

<details>
<summary>An agent has two actions: "safe" (r=+1 always) and "risky" (r=+10 with prob 0.8, r=−20 with prob 0.2). True Q*(risky) = 0.8(10)+0.2(−20) = +4 > Q*(safe) = +1. But after one bad experience, Q(risky)=−20. Show how ε-greedy recovers the true value.</summary>

**Initial bad experience:** Agent tries "risky", gets r=−20.

$$
Q(\text{risky}) = 0 + 1.0 \times (-20) = -20 \quad \text{(first visit, α=1)}
$$

With $\epsilon = 0$: agent **never** tries risky again. Stuck at Q(safe)=1. **Local minimum.**

**With $\epsilon = 0.1$, $\alpha = 0.2$:**

The agent tries "risky" with probability 0.1/2 = 0.05 per step.

After ~20 steps, it tries risky again. Say it gets r=+10:

$$
Q(\text{risky}) \leftarrow -20 + 0.2(10 - (-20)) = -20 + 6 = -14
$$

Still negative. Tries again after ~20 more steps, gets r=+10:

$$
Q(\text{risky}) \leftarrow -14 + 0.2(10 - (-14)) = -14 + 4.8 = -9.2
$$

Continuing (assuming 80% success rate, expected update per trial):

$$
E[\Delta Q] = 0.2 \times [E[r] - Q] = 0.2 \times [4 - Q]
$$

This converges to $Q = 4$ (the true expected value).

After ~50 exploratory trials: $Q(\text{risky}) \approx 4 \gt  Q(\text{safe}) = 1$. The agent now exploits "risky."

**Behavioral parallel:** This is exactly the process of overcoming avoidant attachment. The "risky" action (vulnerability/trust) has a true expected value higher than isolation, but early negative experiences created a deeply negative Q-estimate. Only sustained exploration (therapy, safe relationships) can update the estimate.

</details>

### Example 06.3.4 — Value Iteration by Hand

<details>
<summary>3 states: s₁, s₂, s₃(terminal, r=0). From s₁: action a→s₂ (r=2), action b→s₃ (r=8). From s₂: action a→s₃ (r=4), action b→s₁ (r=0). γ=0.5. Run value iteration until convergence.</summary>

**Iteration 0:** $Q_0(s,a) = 0$ for all.

**Iteration 1:**

$$
Q_1(s_1, a) = 2 + 0.5 \cdot \max\{Q_0(s_2, a), Q_0(s_2, b)\} = 2 + 0 = 2
$$

$$
Q_1(s_1, b) = 8 + 0.5 \cdot \max\{Q_0(s_3, \cdot)\} = 8 + 0 = 8
$$

$$
Q_1(s_2, a) = 4 + 0.5 \cdot 0 = 4
$$

$$
Q_1(s_2, b) = 0 + 0.5 \cdot \max\{Q_0(s_1, \cdot)\} = 0
$$

$V_1(s_1) = \max(2, 8) = 8$, $V_1(s_2) = \max(4, 0) = 4$.

**Iteration 2:**

$$
Q_2(s_1, a) = 2 + 0.5 \cdot V_1(s_2) = 2 + 0.5(4) = 4
$$

$$
Q_2(s_1, b) = 8 + 0.5 \cdot 0 = 8
$$

$$
Q_2(s_2, a) = 4 + 0 = 4
$$

$$
Q_2(s_2, b) = 0 + 0.5 \cdot V_1(s_1) = 0 + 0.5(8) = 4
$$

$V_2(s_1) = 8$, $V_2(s_2) = 4$.

**Iteration 3:**

$$
Q_3(s_1, a) = 2 + 0.5(4) = 4, \quad Q_3(s_1, b) = 8
$$

$$
Q_3(s_2, a) = 4, \quad Q_3(s_2, b) = 0 + 0.5(8) = 4
$$

**Converged!** $V^*(s_1) = 8$ (take action b), $V^*(s_2) = 4$ (either action).

Optimal policy: $\pi^*(s_1) = b$ (go directly to terminal for r=8).

</details>

### Example 06.3.5 — SARSA vs Q-Learning Near a Cliff

<details>
<summary>A 1×4 grid: [Start, Safe, Cliff(r=−100,terminal), Goal(r=+10,terminal)]. Actions: right, left. From Safe: right→Cliff, left→Start. From Start: right→Safe. ε=0.1, α=0.5, γ=0.9. Compare Q-learning and SARSA values for Q(Safe, right).</summary>

**Q-Learning (off-policy, uses max):**

Q-learning updates Q(Safe, right) using the Bellman optimality target regardless of what action is actually taken next:

$$
Q(Safe, right) \leftarrow Q(Safe, right) + \alpha[r + \gamma \max_{a'} Q(Cliff, a') - Q(Safe, right)]
$$

Since Cliff is terminal: $\max_{a'} Q(Cliff, a') = 0$.

$$
Q(Safe, right) \leftarrow Q + 0.5[-100 + 0 - Q]
$$

After one experience: $Q(Safe, right) = 0 + 0.5(-100) = -50$.

After convergence: $Q^*(Safe, right) = -100$ (the true value of stepping into the cliff).

Q-learning learns the **optimal** policy (which avoids the cliff), but during training the agent still falls off the cliff with probability ε/2 = 0.05 per visit to Safe.

**SARSA (on-policy, uses actual next action):**

SARSA updates using the action actually taken next (which includes ε-greedy randomness):

$$
Q(Safe, right) \leftarrow Q + \alpha[r + \gamma Q(Cliff, a') - Q]
$$

But SARSA also considers: what is Q(Safe, left)?

The key difference: SARSA's Q(Start, right) accounts for the fact that from Safe, the ε-greedy policy will sometimes go right (into cliff). So:

$$
Q^{\text{SARSA}}(Start, right) = -1 + \gamma \cdot E_\pi[Q(Safe, a)]
$$

$$
= -1 + 0.9[(1-\epsilon/2) \cdot Q(Safe, left) + (\epsilon/2) \cdot Q(Safe, right)]
$$

SARSA learns a **safer** policy that accounts for its own exploration noise. It values being near the cliff less because it knows it might accidentally step off.

**Behavioral interpretation:** 
- Q-learning = "What's the best I could do?" (optimistic, ignores own fallibility)
- SARSA = "What will I actually experience given my tendency to make mistakes?" (realistic, accounts for own impulsivity)

For a trauma-adapted agent: SARSA is more appropriate because it accounts for the agent's own dysregulation (random sympathetic activation = random "bad" actions). Q-learning would be overconfident about the agent's ability to execute the optimal policy perfectly.

</details>

---

## 🧠 5. AI/RL Translation

| Behavioral Concept | Q-Learning Concept | Formal Correspondence |
|---|---|---|
| Learned action preference | $Q(s,a)$ | Higher Q → more likely to choose action |
| "What should I do here?" | $\pi^*(s) = \arg\max_a Q^*(s,a)$ | Optimal policy from Q-table |
| Trial-and-error learning | Q-update from $(s,a,r,s')$ samples | Model-free learning |
| Habit (automatic behavior) | Converged Q-values, $\epsilon \to 0$ | Exploitation-dominant policy |
| Curiosity / novelty-seeking | $\epsilon$-greedy exploration | Random action with prob $\epsilon$ |
| "Knowing the rules" (model-based) | Value iteration with known $P, R$ | Planning |
| Avoidance learning | $Q(s, a_{\text{avoid}}) \gg Q(s, a_{\text{approach}})$ | Negative reward dominates |
| Extinction of avoidance | Updating Q with new positive evidence | Exploration reveals true Q |
| Shaping (successive approximation) | Reward shaping: $R' = R + \gamma\Phi(s') - \Phi(s)$ | Potential-based shaping preserves $\pi^*$ |

### The Fundamental Connection

Operant conditioning IS Q-learning with biological hardware:

1. The **dorsal striatum** stores Q-values (state-action associations).
2. **Dopamine RPE** ($\delta$) is the TD error that updates Q-values.
3. **Action selection** uses a softmax/ε-greedy-like mechanism (basal ganglia direct/indirect pathways).
4. **Exploration** is modulated by norepinephrine and tonic dopamine.
5. **Discount factor** $\gamma$ is modulated by serotonin.

The brain is a Q-learning agent with neural function approximation, eligibility traces, and multiple parallel learning systems (model-free + model-based).

---

## 🧬 6. Synthesis

### Parameter Tuning: Biological and Artificial

The Q-learning algorithm has three critical hyperparameters. Each has a biological analog and a therapeutic intervention:

| Parameter | Too Low | Too High | Biological Modulator | Therapeutic Intervention |
|---|---|---|---|---|
| $\alpha$ (learning rate) | Rigid, doesn't update beliefs | Unstable, overreacts to noise | Dopamine receptor density | Neuroplasticity enhancement (exercise, sleep, novelty) |
| $\gamma$ (discount) | Impulsive, myopic | Paralyzed by distant consequences | Serotonin (5-HT) | SSRIs increase $\gamma$; mindfulness training |
| $\epsilon$ (exploration) | Stuck in local optima (avoidance) | Chaotic, never commits | Norepinephrine, tonic DA | Exposure therapy increases $\epsilon$ for feared actions |

### The Avoidance Trap as a Q-Learning Failure Mode

The most clinically relevant insight from Q-learning theory:

**Problem:** An agent with $Q(s, \text{trust}) = -20$ (from early trauma) and $Q(s, \text{isolate}) = +1$ will **never** discover that the true $Q^*(\text{trust}) = +4$ if $\epsilon = 0$.

**Solutions (both computational and therapeutic):**

1. **Increase $\epsilon$:** Force exploration of the feared action. Therapy: graduated exposure.
2. **Optimistic initialization:** Set all Q-values high initially, forcing exploration of everything. Therapy: "assume good intent" as a cognitive reframe.
3. **Upper Confidence Bound (UCB):** Explore actions with high uncertainty. Therapy: "I don't actually know what would happen if I tried."
4. **Transfer learning:** Import Q-values from a safe context. Therapy: positive relationship experiences in one domain transfer to others.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- [06.1 - Classical & Operant Conditioning](06.1---Classical-&-Operant-Conditioning) — Rescorla-Wagner as single-state Q-learning
- [06.2 - Dopamine & Reward Prediction Error](06.2---Dopamine-&-Reward-Prediction-Error) — The neural implementation of the TD error
- [06.5 - Trauma Adaptations - C-PTSD as Reinforcement Learning](06.5---Trauma-Adaptations---C-PTSD-as-Reinforcement-Learning) — Avoidance as Q-learning failure
- [06.6 - RLHF - Reinforcement Learning from Human Feedback](06.6---RLHF---Reinforcement-Learning-from-Human-Feedback) — Using human preferences instead of scalar reward
- [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) — Full AI/ML treatment
- [3.4 - Systems of Linear ODEs & State Space](3.4---Systems-of-Linear-ODEs-&-State-Space) — State-space formulation of MDPs

### Authoritative Sources
1. **Sutton, R.S. & Barto, A.G.** (2018). *Reinforcement Learning: An Introduction*. Chapters 3–6.
2. **Watkins, C.J.C.H.** (1989). *Learning from Delayed Rewards*. PhD thesis, Cambridge.
3. **Bellman, R.** (1957). *Dynamic Programming*. Princeton University Press.
4. **David Silver** — UCL RL Course, Lectures 3–5.
5. **MIT 6.832** (Tedrake) — Underactuated Robotics, optimal control formulation.

### Practice
- [12.3_bellman_qlearning.py](12.3_bellman_qlearning.py) — Q-learning gridworld implementation with convergence visualization

---

*Next: [06.4 - Polyvagal Theory & Autonomic Regulation](06.4---Polyvagal-Theory-&-Autonomic-Regulation) →*

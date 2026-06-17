---
title: "06.1 — Classical & Operant Conditioning"
subject: "Behavioral Psychology & Reinforcement Learning"
catalog: advanced
audience_tier: higher-education
chapter: "6.1"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 06.1 — Classical & Operant Conditioning

> *"Give me a child and I'll shape him into anything."*
> — B.F. Skinner

> *"The alimentary reflex can be called forth not only by the substance which is introduced into the mouth, but also by the sight of it, and even by the sound which accompanies its introduction."*
> — Ivan Pavlov, *Conditioned Reflexes* (1927)

The entire edifice of reinforcement learning — from Sutton & Barto's textbook algorithms to modern RLHF — rests on two empirical pillars discovered in animal behavior laboratories: **classical conditioning** (Pavlov) and **operant conditioning** (Skinner/Thorndike). This chapter formalizes both paradigms, derives the Rescorla-Wagner learning rule (the direct ancestor of the TD-learning update), and maps every behavioral concept to its computational counterpart.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Distinguish classical from operant conditioning by their causal structure (stimulus-driven vs. consequence-driven).
2. Define and identify: CS, US, CR, UR, reinforcement schedules, extinction, spontaneous recovery.
3. Derive the **Rescorla-Wagner update rule** $\Delta V_i = \alpha_i \beta_j (\lambda - \Sigma V)$ from first principles.
4. Prove that Rescorla-Wagner converges to $V = \lambda$ under repeated pairing.
5. Map classical conditioning → supervised learning and operant conditioning → reinforcement learning.
6. Compute associative strengths across multi-trial conditioning experiments.
7. Explain blocking, overshadowing, and conditioned inhibition as emergent properties of the update rule.

---

## 🖼️ Visual Anchor — Conditioning Paradigms

![psych-06__fig1](psych-06__fig1.svg)

---


## 📚 1. Definitions

### Definition 06.1.1 — Unconditioned Stimulus (US)

A stimulus that **naturally and automatically** triggers a response without prior learning. The US has innate biological significance.

$$
\text{US} \xrightarrow{\text{innate}} \text{UR (Unconditioned Response)}
$$

*Examples:* Food → salivation; loud noise → startle; physical pain → withdrawal reflex.

### Definition 06.1.2 — Unconditioned Response (UR)

The **unlearned, reflexive** response to the unconditioned stimulus. It requires no training.

### Definition 06.1.3 — Conditioned Stimulus (CS)

A previously **neutral stimulus** that, after repeated pairing with a US, comes to elicit a conditioned response on its own.

$$
\text{CS (after pairing)} \xrightarrow{\text{learned}} \text{CR (Conditioned Response)}
$$

### Definition 06.1.4 — Conditioned Response (CR)

The **learned response** to the conditioned stimulus. It is typically similar to the UR but often weaker or slightly different in form.

### Definition 06.1.5 — Associative Strength $V$

The **current predictive value** that a CS holds for the US. In the Rescorla-Wagner model, $V_i \in [0, \lambda]$ represents how strongly stimulus $i$ predicts the outcome. When $V = \lambda$, the CS perfectly predicts the US and no further learning occurs.

### Definition 06.1.6 — Reinforcement (Operant)

Any consequence of a behavior that **increases the probability** of that behavior recurring:

- **Positive reinforcement (R+):** Adding a desirable stimulus after the behavior.
- **Negative reinforcement (R−):** Removing an aversive stimulus after the behavior.

### Definition 06.1.7 — Punishment (Operant)

Any consequence of a behavior that **decreases the probability** of that behavior recurring:

- **Positive punishment (P+):** Adding an aversive stimulus after the behavior.
- **Negative punishment (P−):** Removing a desirable stimulus after the behavior.

### Definition 06.1.8 — Extinction

The gradual **weakening and eventual disappearance** of a conditioned response when the CS is repeatedly presented without the US (classical) or when the behavior is no longer reinforced (operant).

$$
\text{Extinction: } V_{n+1} = V_n + \alpha\beta(0 - V_n) = V_n(1 - \alpha\beta) \to 0
$$

### Definition 06.1.9 — Reinforcement Schedule

The **rule** determining which instances of a behavior are reinforced:

| Schedule | Rule | Example | Resistance to Extinction |
|----------|------|---------|--------------------------|
| Fixed Ratio (FR-n) | Every $n$-th response | Piecework pay | Moderate |
| Variable Ratio (VR-n) | Average every $n$ responses | Slot machines | Very High |
| Fixed Interval (FI-t) | First response after $t$ seconds | Salary check | Low |
| Variable Interval (VI-t) | First response after avg $t$ seconds | Checking email | High |

### Definition 06.1.10 — Policy $\pi$ (RL Parallel)

In reinforcement learning, a **policy** $\pi: S \to A$ (or $\pi(a|s)$ for stochastic policies) maps states to actions. The operant conditioning analog: the organism's learned behavioral repertoire mapping situations (states) to actions.

### Definition 06.1.11 — Blocking (Kamin, 1969)

If stimulus A already perfectly predicts the US ($V_A = \lambda$), then adding a new stimulus B in compound (A+B → US) produces **no learning** about B because the prediction error $(\lambda - V_A - V_B) = 0$. This is a direct consequence of the Rescorla-Wagner error-correction mechanism.

---


## 🔬 2. Behavioral Mechanisms

### 2.1 Pavlov's Classical Conditioning Circuit

Ivan Pavlov (1849–1936) discovered classical conditioning while studying digestion in dogs. The mechanism:

**Phase 1 — Pre-conditioning:**
- The bell (neutral stimulus) produces no salivation.
- Food (US) reliably produces salivation (UR) via the salivary reflex arc.

**Phase 2 — Acquisition (repeated CS-US pairing):**
- Bell rings → food presented → salivation occurs.
- After $n$ pairings, the neural pathway strengthens: auditory cortex → amygdala → salivary nucleus.
- The associative strength $V$ increases trial-by-trial according to the Rescorla-Wagner rule.

**Phase 3 — Post-conditioning:**
- Bell alone → salivation (now a CR).
- The CS has become a **predictor** of the US.

**Neural substrate:** The amygdala forms the CS-US association. The cerebellum handles timing (trace conditioning). The prefrontal cortex mediates extinction (new inhibitory learning, not erasure).

### 2.2 Thorndike's Law of Effect & Skinner's Operant Chamber

Edward Thorndike (1874–1949) placed cats in puzzle boxes. Behaviors followed by satisfying consequences were "stamped in" (Law of Effect, 1898).

B.F. Skinner (1904–1990) formalized this into **operant conditioning** using the Skinner box:

1. **Antecedent (State $s$):** The environmental context — light on, lever present.
2. **Behavior (Action $a$):** The organism's voluntary response — press lever.
3. **Consequence (Reward $r$):** The outcome — food pellet delivered.

The **three-term contingency** $S \to R \to C$ (Stimulus → Response → Consequence) is the behavioral precursor to the MDP tuple $(s, a, r, s')$.

### 2.3 Shaping & Successive Approximation

Skinner trained complex behaviors by reinforcing successive approximations:

1. Reinforce any movement toward the lever.
2. Reinforce touching the lever.
3. Reinforce pressing the lever.
4. Require full press for reinforcement.

This is directly analogous to **curriculum learning** in AI: training on progressively harder tasks, or **reward shaping** in RL where intermediate rewards guide the agent toward the final objective.

### 2.4 Schedules of Reinforcement — Behavioral Signatures

Each schedule produces a characteristic **cumulative response curve**:

- **FR (Fixed Ratio):** Post-reinforcement pause, then rapid responding ("ratio strain" at high ratios).
- **VR (Variable Ratio):** Steady, high-rate responding. Most resistant to extinction. (Gambling addiction mechanism.)
- **FI (Fixed Interval):** "Scallop" pattern — slow start, accelerating as interval end approaches.
- **VI (Variable Interval):** Steady, moderate-rate responding.

### 2.5 Biological Constraints on Learning

Not all CS-US pairings are equally learnable (Garcia & Koelling, 1966):
- Taste → nausea: one-trial learning (adaptive for poison avoidance).
- Sound → nausea: very difficult to condition.
- Sound → shock: easy to condition.

This **preparedness** constrains the hypothesis space — analogous to **inductive bias** in machine learning architectures.

---


## 📐 3. Mathematical Formulations

### 3.1 The Rescorla-Wagner Model (1972)

The Rescorla-Wagner model is the foundational error-correction learning rule for classical conditioning. It states that learning occurs only when the outcome is **surprising** — i.e., when there is a discrepancy between what is predicted and what actually occurs.

**Setup:** Let there be $k$ conditioned stimuli $\text{CS}_1, \text{CS}_2, \ldots, \text{CS}_k$ present on a given trial. Each has an associative strength $V_i$. The total prediction is:

$$
V_{\text{total}} = \sum_{i \in \text{present}} V_i
$$

**The Update Rule:**

On each trial where stimulus $i$ is present:

$$
\Delta V_i = \alpha_i \cdot \beta_j \cdot (\lambda - V_{\text{total}})
$$

where:
- $\alpha_i \in (0, 1]$ = salience of CS$_i$ (how noticeable the stimulus is)
- $\beta_j \in (0, 1]$ = learning rate associated with the US (subscript $j$ distinguishes US-present trials $\beta_1$ from US-absent trials $\beta_2$, typically $\beta_1 > \beta_2$)
- $\lambda$ = maximum associative strength supportable by the US (asymptote); $\lambda = 1$ when US is present, $\lambda = 0$ when US is absent
- $V_{\text{total}}$ = sum of associative strengths of all CSs present on this trial

**The prediction error** is $\delta = \lambda - V_{\text{total}}$.

### 3.2 Derivation: Convergence of Rescorla-Wagner

**Claim:** Under repeated CS-US pairings with a single CS, $V_n \to \lambda$ as $n \to \infty$.

**Proof:**

With a single CS present on every trial, $V_{\text{total}} = V_n$. The update becomes:

$$
V_{n+1} = V_n + \alpha\beta(\lambda - V_n)
$$

Let $\eta = \alpha\beta \in (0,1)$. Then:

$$
V_{n+1} = V_n + \eta(\lambda - V_n) = V_n(1 - \eta) + \eta\lambda
$$

This is a **linear first-order recurrence**. Define the error $e_n = \lambda - V_n$:

$$
e_{n+1} = \lambda - V_{n+1} = \lambda - [V_n(1-\eta) + \eta\lambda]
$$

$$
e_{n+1} = \lambda - V_n + \eta V_n - \eta\lambda = (\lambda - V_n)(1 - \eta)
$$

$$
e_{n+1} = (1 - \eta) \cdot e_n
$$

By induction:

$$
e_n = (1 - \eta)^n \cdot e_0
$$

Since $0 < \eta < 1$, we have $0 < (1-\eta) < 1$, so:

$$
\lim_{n \to \infty} e_n = \lim_{n \to \infty} (1-\eta)^n \cdot e_0 = 0
$$

Therefore:

$$
\lim_{n \to \infty} V_n = \lambda \quad \blacksquare
$$

**Rate of convergence:** The half-life (trials to reduce error by 50%) is:

$$
n_{1/2} = \frac{\ln(0.5)}{\ln(1 - \alpha\beta)} = \frac{-\ln 2}{\ln(1 - \alpha\beta)}
$$

For $\alpha = 0.3, \beta = 0.5$: $n_{1/2} = \frac{0.693}{\ln(1-0.15)} \approx \frac{0.693}{0.1625} \approx 4.3$ trials.

### 3.3 Derivation: Blocking as Zero Prediction Error

**Setup:** Phase 1 trains CS_A alone until $V_A = \lambda$. Phase 2 presents compound (A+B) with the same US.

**Phase 2 update for CS_B:**

$$
\Delta V_B = \alpha_B \beta (\lambda - V_A - V_B)
$$

At the start of Phase 2: $V_A = \lambda$, $V_B = 0$:

$$
\Delta V_B = \alpha_B \beta (\lambda - \lambda - 0) = \alpha_B \beta \cdot 0 = 0
$$

No learning occurs for B because the prediction error is zero. A already perfectly predicts the US, so B is **blocked**. $\blacksquare$

### 3.4 Extinction Dynamics

When the US is omitted ($\lambda = 0$) but the CS is presented:

$$
\Delta V = \alpha\beta_2(0 - V_n) = -\alpha\beta_2 V_n
$$

$$
V_{n+1} = V_n(1 - \alpha\beta_2)
$$

This is exponential decay:

$$
V_n = V_0 (1 - \alpha\beta_2)^n \to 0
$$

Note: $\beta_2$ (US-absent learning rate) is typically smaller than $\beta_1$ (US-present), so extinction is slower than acquisition — matching empirical data.

### 3.5 The Operant Conditioning Update (Bandit Formulation)

For a single state (stateless environment), operant conditioning reduces to the **multi-armed bandit** update. Let $Q(a)$ be the estimated value of action $a$:

$$
Q_{n+1}(a) = Q_n(a) + \alpha [R_n - Q_n(a)]
$$

where $R_n$ is the reward received after taking action $a$ on trial $n$.

This is identical in form to Rescorla-Wagner with:
- $Q(a) \leftrightarrow V$ (associative strength)
- $R_n \leftrightarrow \lambda$ (actual outcome)
- $\alpha \leftrightarrow \alpha\beta$ (combined learning rate)

**Action selection** uses a softmax (Boltzmann) policy:

$$
\pi(a|s) = \frac{e^{Q(a)/\tau}}{\sum_{a'} e^{Q(a')/\tau}}
$$

where $\tau$ is the temperature parameter controlling exploration vs. exploitation.

### 3.6 Matching Law (Herrnstein, 1961)

On concurrent VI-VI schedules, organisms distribute responses proportionally to reinforcement rates:

$$
\frac{B_1}{B_1 + B_2} = \frac{r_1}{r_1 + r_2}
$$

where $B_i$ = response rate on alternative $i$, $r_i$ = reinforcement rate on alternative $i$.

The generalized matching law adds sensitivity and bias parameters:

$$
\log\left(\frac{B_1}{B_2}\right) = a \cdot \log\left(\frac{r_1}{r_2}\right) + \log(b)
$$

where $a$ = sensitivity (typically $\approx 0.8$, indicating undermatching) and $b$ = bias.

---


## ✍️ 4. Worked Examples

### Example 06.1.1 — Basic Rescorla-Wagner Acquisition

<details>
<summary>A single CS (bell) is paired with food (US) over 8 trials. Parameters: α = 0.4, β₁ = 0.5, λ = 1.0, V₀ = 0. Compute V after each trial.</summary>

The combined learning rate is $\eta = \alpha\beta_1 = 0.4 \times 0.5 = 0.2$.

The recurrence is $V_{n+1} = V_n + 0.2(1 - V_n)$.

**Trial 1:**

$$
V_1 = 0 + 0.2(1 - 0) = 0.200
$$

**Trial 2:**

$$
V_2 = 0.200 + 0.2(1 - 0.200) = 0.200 + 0.160 = 0.360
$$

**Trial 3:**

$$
V_3 = 0.360 + 0.2(1 - 0.360) = 0.360 + 0.128 = 0.488
$$

**Trial 4:**

$$
V_4 = 0.488 + 0.2(1 - 0.488) = 0.488 + 0.102 = 0.590
$$

**Trial 5:**

$$
V_5 = 0.590 + 0.2(1 - 0.590) = 0.590 + 0.082 = 0.672
$$

**Trial 6:**

$$
V_6 = 0.672 + 0.2(1 - 0.672) = 0.672 + 0.066 = 0.738
$$

**Trial 7:**

$$
V_7 = 0.738 + 0.2(1 - 0.738) = 0.738 + 0.052 = 0.790
$$

**Trial 8:**

$$
V_8 = 0.790 + 0.2(1 - 0.790) = 0.790 + 0.042 = 0.832
$$

**Verification via closed form:** $V_n = 1 - (1-0.2)^n = 1 - 0.8^n$.

$V_8 = 1 - 0.8^8 = 1 - 0.1678 = 0.832$. ✓

The learning curve is negatively accelerated — large initial gains that diminish as $V \to \lambda$.

</details>

### Example 06.1.2 — Blocking Demonstration

<details>
<summary>Phase 1: CS_A paired with US for 20 trials (α_A = 0.3, β = 0.6, λ = 1). Phase 2: Compound (A+B) paired with same US for 10 trials (α_B = 0.5). Show that B acquires negligible associative strength.</summary>

**Phase 1 — Training A alone:**

$\eta_A = 0.3 \times 0.6 = 0.18$

After 20 trials: $V_A = 1 - (1-0.18)^{20} = 1 - 0.82^{20}$

$$
0.82^{20} = 0.82^{10} \times 0.82^{10}
$$

$0.82^{10} = 0.1374$ (computed: $\ln(0.82) = -0.1985$, so $0.82^{10} = e^{-1.985} = 0.1374$)

$$
0.82^{20} = 0.1374^2 = 0.0189
$$

$$
V_A^{(20)} = 1 - 0.0189 = 0.981 \approx \lambda
$$

**Phase 2 — Compound A+B, starting with $V_A = 0.981$, $V_B = 0$:**

Trial 1 of Phase 2:

$$
\delta = \lambda - V_A - V_B = 1 - 0.981 - 0 = 0.019
$$

$$
\Delta V_A = 0.3 \times 0.6 \times 0.019 = 0.0034
$$

$$
\Delta V_B = 0.5 \times 0.6 \times 0.019 = 0.0057
$$

After trial 1: $V_A = 0.984$, $V_B = 0.006$.

Trial 2:

$$
\delta = 1 - 0.984 - 0.006 = 0.010
$$

$$
\Delta V_B = 0.5 \times 0.6 \times 0.010 = 0.003
$$

After trial 2: $V_B = 0.009$.

The prediction error is already near zero, so B gains almost nothing. After 10 compound trials, $V_B \lt  0.02$ — **B is blocked**.

**Interpretation:** A already explains the US. Adding B provides no new predictive information. This is the Rescorla-Wagner model's greatest triumph: explaining blocking without invoking attention.

</details>

### Example 06.1.3 — Extinction After Acquisition

<details>
<summary>After 8 acquisition trials (V₈ = 0.832 from Example 06.1.1), the US is omitted for 12 extinction trials. Parameters: α = 0.4, β₂ = 0.3 (US-absent rate). Compute the extinction curve.</summary>

During extinction, $\lambda = 0$:

$$
V_{n+1} = V_n + \alpha\beta_2(0 - V_n) = V_n(1 - 0.4 \times 0.3) = V_n \times 0.88
$$

Starting from $V_0^{\text{ext}} = 0.832$:

| Trial | $V_n$ |
|-------|--------|
| 0 | 0.832 |
| 1 | 0.832 × 0.88 = 0.732 |
| 2 | 0.732 × 0.88 = 0.644 |
| 3 | 0.644 × 0.88 = 0.567 |
| 4 | 0.567 × 0.88 = 0.499 |
| 5 | 0.499 × 0.88 = 0.439 |
| 6 | 0.439 × 0.88 = 0.386 |
| 7 | 0.386 × 0.88 = 0.340 |
| 8 | 0.340 × 0.88 = 0.299 |
| 9 | 0.299 × 0.88 = 0.263 |
| 10 | 0.263 × 0.88 = 0.232 |
| 11 | 0.232 × 0.88 = 0.204 |
| 12 | 0.204 × 0.88 = 0.179 |

**Closed form:** $V_n = 0.832 \times 0.88^n$

Half-life: $n_{1/2} = \frac{\ln 0.5}{\ln 0.88} = \frac{-0.693}{-0.128} = 5.4$ trials.

Note extinction is slower than acquisition ($n_{1/2}^{\text{acq}} = 3.1$ trials with $\eta = 0.2$) because $\beta_2 \lt  \beta_1$.

</details>

### Example 06.1.4 — Operant Conditioning: Avoidant Attachment as Over-Penalized Vulnerability

<details>
<summary>Model a child learning avoidant attachment. State: "caregiver present." Actions: {seek comfort, self-soothe}. The caregiver inconsistently rejects bids for comfort (P+ with probability 0.7). Compute Q-values over 20 trials.</summary>

**Setup (single-state bandit):**
- Action $a_1$ = seek comfort: reward = +3 (when accepted, prob 0.3) or −5 (when rejected, prob 0.7)
- Action $a_2$ = self-soothe: reward = +1 (reliable, prob 1.0)
- Learning rate $\alpha = 0.1$, initial $Q(a_1) = Q(a_2) = 0$

**Expected reward for $a_1$:** $E[R|a_1] = 0.3(+3) + 0.7(-5) = 0.9 - 3.5 = -2.6$

**Expected reward for $a_2$:** $E[R|a_2] = +1.0$

The Q-values will converge to: $Q^*(a_1) = -2.6$, $Q^*(a_2) = +1.0$.

**Simulated trajectory** (using seed for reproducibility — outcomes for $a_1$: R, R, A, R, R, R, A, R, R, R where R=reject, A=accept):

Trials 1-5 (exploring $a_1$):

$$
Q_1(a_1) = 0 + 0.1(-5 - 0) = -0.5
$$

$$
Q_2(a_1) = -0.5 + 0.1(-5 - (-0.5)) = -0.5 - 0.45 = -0.95
$$

$$
Q_3(a_1) = -0.95 + 0.1(+3 - (-0.95)) = -0.95 + 0.395 = -0.555
$$

$$
Q_4(a_1) = -0.555 + 0.1(-5 - (-0.555)) = -0.555 - 0.445 = -1.0
$$

$$
Q_5(a_1) = -1.0 + 0.1(-5 - (-1.0)) = -1.0 - 0.4 = -1.4
$$

After just 5 trials, $Q(a_1) = -1.4$ while $Q(a_2)$ remains at 0 (untried). A greedy agent now **permanently avoids** $a_1$ (seeking comfort).

Trials 6-10 (exploiting $a_2$):

$$
Q_6(a_2) = 0 + 0.1(1 - 0) = 0.1
$$

$$
Q_7(a_2) = 0.1 + 0.1(1 - 0.1) = 0.19
$$

$$
Q_{10}(a_2) = 1 - 0.9^5 \times 1 = 0.41
$$

**Result:** The agent learns a stable policy $\pi^* = a_2$ (self-soothe/avoid vulnerability). This is the **avoidant attachment style** — a locally optimal policy that avoids the high-variance, net-negative action. The tragedy: with a different caregiver (acceptance prob = 0.9), $a_1$ would yield $E[R] = 0.9(3) + 0.1(-5) = 2.2 \gt  1.0$. But the agent never explores to discover this.

**Clinical parallel:** Therapy increases the exploration rate $\epsilon$, allowing the individual to sample $a_1$ in safe contexts and update $Q(a_1)$ with new evidence.

</details>

### Example 06.1.5 — Conditioned Inhibition (CS predicts absence of US)

<details>
<summary>CS_A is paired with US (V_A → 1). Then compound A+X is presented WITHOUT the US. Show that X becomes a conditioned inhibitor (V_X < 0).</summary>

**Phase 1:** Train A alone, $V_A \to \lambda = 1$ (as before).

**Phase 2:** Present A+X, no US ($\lambda = 0$). Starting: $V_A = 1.0$, $V_X = 0$.

Parameters: $\alpha_A = 0.3$, $\alpha_X = 0.4$, $\beta_2 = 0.4$.

**Trial 1:**

$$
\delta = 0 - V_A - V_X = 0 - 1.0 - 0 = -1.0
$$

$$
\Delta V_A = 0.3 \times 0.4 \times (-1.0) = -0.12
$$

$$
\Delta V_X = 0.4 \times 0.4 \times (-1.0) = -0.16
$$

After trial 1: $V_A = 0.88$, $V_X = -0.16$.

**Trial 2:**

$$
\delta = 0 - 0.88 - (-0.16) = 0 - 0.72 = -0.72
$$

$$
\Delta V_X = 0.4 \times 0.4 \times (-0.72) = -0.115
$$

After trial 2: $V_X = -0.275$.

**Trial 3:**

$$
\delta = 0 - (0.88 - 0.12 \times 0.72) - (-0.275 - 0.115) = \ldots
$$

Continuing iteratively, $V_X$ becomes increasingly negative. At equilibrium: $V_A + V_X = 0$, so $V_X = -V_A$.

**Interpretation:** X has become a **conditioned inhibitor** — it signals the *absence* of the US. Presenting X alone produces a response *below* baseline. In RL terms, X has negative value: it predicts reward will be *less* than expected.

</details>

---


## 🧠 5. AI/RL Translation

| Behavioral Psychology | Reinforcement Learning | Mathematical Form |
|---|---|---|
| Conditioned Stimulus (CS) | State feature / observation $s$ | Input to value function |
| Unconditioned Stimulus (US) | Primary reward $r$ | Scalar signal |
| Associative Strength $V$ | Value function $V(s)$ | $V: S \to \mathbb{R}$ |
| Rescorla-Wagner $\Delta V$ | TD(0) update | $\Delta V = \alpha[\delta]$ |
| Prediction Error $(\lambda - V)$ | TD error $\delta = r + \gamma V(s') - V(s)$ | Scalar surprise signal |
| Extinction | Value decay without reward | $V \to 0$ when $r = 0$ |
| Blocking | No update when $\delta = 0$ | Already-explained variance |
| Reinforcement schedule | Reward schedule / sparse reward | Frequency of $r > 0$ |
| Shaping | Reward shaping / curriculum learning | Intermediate $r$ signals |
| Operant action selection | Policy $\pi(a|s)$ | Softmax / $\epsilon$-greedy |
| Law of Effect | Policy gradient theorem | $\nabla J \propto E[\nabla \log \pi \cdot Q]$ |
| Matching Law | Proportional allocation | $\pi(a) \propto Q(a)$ |
| Biological preparedness | Inductive bias / architecture | CNN for vision, RNN for sequences |

### Key Insight: Rescorla-Wagner IS TD(0) with γ = 0

The Rescorla-Wagner update:

$$
V_{n+1} = V_n + \alpha\beta(\lambda - V_n)
$$

The TD(0) update with $\gamma = 0$ (single-step, no future states):

$$
V(s) \leftarrow V(s) + \alpha[r - V(s)]
$$

These are **identical** when we identify $\lambda \leftrightarrow r$ and $\alpha\beta \leftrightarrow \alpha$. Classical conditioning is temporal-difference learning in a one-step environment. The extension to multi-step environments (adding $\gamma V(s')$) is what transforms Pavlovian prediction into full RL — covered in [06.3 - Q-Learning & The Bellman Equation](06.3---Q-Learning-&-The-Bellman-Equation).

### From Pavlov to Deep RL: The Lineage

```
Pavlov (1927)          → Stimulus-response association
    ↓
Rescorla-Wagner (1972) → Error-correction learning rule
    ↓
Sutton & Barto (1981)  → TD learning (adding temporal credit)
    ↓
Watkins (1989)         → Q-learning (adding action selection)
    ↓
Mnih et al. (2015)     → Deep Q-Networks (neural function approximation)
    ↓
Schulman et al. (2017) → PPO (policy gradient + clipping)
    ↓
Ouyang et al. (2022)   → RLHF (human as reward model)
```

---

## 🧬 6. Synthesis

### Bridging Human Behavior Design and AI Reward Engineering

The Rescorla-Wagner model reveals a profound structural identity: **biological learning and artificial learning share the same error-correction architecture**. This has bidirectional implications:

**Human → AI direction:**

1. **Variable ratio schedules** produce the most persistent behavior in animals. In AI, **sparse but variable rewards** (rather than dense constant rewards) can produce more robust policies that resist catastrophic forgetting.

2. **Blocking** shows that organisms only learn from *informative* stimuli. AI systems benefit from the same principle: **prioritized experience replay** (Schaul et al., 2015) samples transitions with high TD-error, ignoring already-learned patterns.

3. **Biological preparedness** (some associations are easier to learn) maps to **inductive bias** in neural architectures. Just as taste-nausea conditioning is privileged, convolutional architectures are "prepared" for spatial patterns.

**AI → Human direction (therapeutic implications):**

1. **Avoidant attachment** (Example 06.1.4) is a policy stuck in a local optimum due to insufficient exploration. The RL solution — **increase $\epsilon$** — maps to the therapeutic intervention of **graduated exposure**: systematically sampling the feared action (vulnerability) in controlled, safe environments to update $Q(a_{\text{trust}})$ with new positive evidence.

2. **Extinction is not erasure** — it is new inhibitory learning (Bouton, 2004). The original CS-US association persists (explaining spontaneous recovery). In RL terms: the old Q-values are not deleted; a new context-dependent policy is layered on top. This explains why trauma responses can resurface under stress (context shift removes the inhibitory overlay).

3. **Reward shaping** in AI (adding intermediate rewards to guide learning) parallels **therapeutic scaffolding**: breaking overwhelming goals into achievable sub-goals, each with its own reinforcement signal.

**Parameter correspondence for intervention:**

| Human Parameter | RL Parameter | Intervention |
|---|---|---|
| Willingness to try new behavior | Exploration rate $\epsilon$ | Exposure therapy |
| Sensitivity to rejection | Negative reward magnitude $|r^-|$ | Cognitive reappraisal |
| Speed of updating beliefs | Learning rate $\alpha$ | Neuroplasticity (exercise, sleep) |
| Influence of past vs. present | Discount factor $\gamma$ | Mindfulness (present-focus) |

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- [06.2 - Dopamine & Reward Prediction Error](06.2---Dopamine-&-Reward-Prediction-Error) — The neural implementation of the prediction error $\delta$
- [06.3 - Q-Learning & The Bellman Equation](06.3---Q-Learning-&-The-Bellman-Equation) — Extending Rescorla-Wagner to multi-step, multi-state environments
- [06.5 - Trauma Adaptations - C-PTSD as Reinforcement Learning](06.5---Trauma-Adaptations---C-PTSD-as-Reinforcement-Learning) — Avoidant attachment as local-minimum lock-in
- [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) — Full AI/ML treatment of RL algorithms
- [05.6 - Neuromodulators - Dopamine, Serotonin, Acetylcholine](05.6---Neuromodulators---Dopamine,-Serotonin,-Acetylcholine) — Biological substrate of learning signals
- [3.4 - Systems of Linear ODEs & State Space](3.4---Systems-of-Linear-ODEs-&-State-Space) — State-space formulation underlying MDP dynamics

### Authoritative Sources
1. **Sutton, R.S. & Barto, A.G.** (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. [Free PDF](http://incompleteideas.net/book/the-book-2nd.html) — Chapter 14: Psychology.
2. **Rescorla, R.A. & Wagner, A.R.** (1972). A theory of Pavlovian conditioning: Variations in the effectiveness of reinforcement and nonreinforcement. In *Classical Conditioning II*, pp. 64–99.
3. **Schultz, W.** (1997). A Neural Substrate of Prediction and Reward. *Science*, 275, 1593–1599.
4. **David Silver** — UCL Course on Reinforcement Learning. [Lecture slides](https://www.davidsilver.uk/teaching/)
5. **Pavlov, I.P.** (1927). *Conditioned Reflexes*. Oxford University Press.
6. **Skinner, B.F.** (1938). *The Behavior of Organisms*. Appleton-Century-Crofts.
7. **Kamin, L.J.** (1969). Predictability, surprise, attention, and conditioning. In *Punishment and Aversive Behavior*, pp. 279–296.

### Practice
- [12.1_conditioning.py](12.1_conditioning.py) — Rescorla-Wagner derivation drills and operant conditioning problems

---

*Next: [06.2 - Dopamine & Reward Prediction Error](06.2---Dopamine-&-Reward-Prediction-Error) →*

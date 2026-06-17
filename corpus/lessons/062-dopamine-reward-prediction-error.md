---
title: "06.2 — Dopamine & Reward Prediction Error"
subject: "Behavioral Psychology & Reinforcement Learning"
catalog: advanced
audience_tier: higher-education
chapter: "6.2"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 06.2 — Dopamine & Reward Prediction Error

> *"The responses of dopamine neurons… code for a prediction error of reward — the discrepancy between the actual reward received and the predicted reward."*
> — Wolfram Schultz, *A Neural Substrate of Prediction and Reward* (Science, 1997)

> *"The error in prediction drives learning. When the world surprises us, we update our model. When it doesn't, we coast."*
> — Richard S. Sutton & Andrew G. Barto, *Reinforcement Learning: An Introduction*

This chapter establishes the most remarkable bridge between neuroscience and computer science: the discovery that **midbrain dopamine neurons implement the temporal-difference (TD) reward prediction error** — the exact same mathematical signal used in AI reinforcement learning algorithms. Schultz's 1997 paper demonstrated that dopamine is not a "pleasure chemical" but a **learning signal** encoding surprise.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain why dopamine encodes **prediction error**, not pleasure.
2. Reproduce Schultz's three experimental conditions (unexpected reward, expected reward, omitted reward) and predict dopamine firing patterns.
3. Derive the TD(0) update rule and identify each term with its neural correlate.
4. Compute RPE ($\delta_t$) for multi-step reward sequences.
5. Explain dopamine's role in the transition from US-response to CS-response during learning.
6. Connect VTA/SNc dopamine circuits to the basal ganglia's direct/indirect pathways.
7. Model addiction, hyperfocus, and anhedonia as RPE system dysfunctions.

---

## 🖼️ Visual Anchor — Schultz Dopamine Firing Patterns

![psych-06__fig2](psych-06__fig2.svg)

---


## 📚 1. Definitions

### Definition 06.2.1 — Reward Prediction Error (RPE, $\delta$)

The **reward prediction error** is the signed difference between the actual outcome and the predicted outcome:

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

where:
- $r_t$ = reward received at time $t$
- $\gamma \in [0,1]$ = temporal discount factor
- $V(s_t)$ = predicted value of current state
- $V(s_{t+1})$ = predicted value of next state

When $\delta > 0$: outcome is **better** than expected (positive surprise).
When $\delta = 0$: outcome **matches** prediction (no learning).
When $\delta < 0$: outcome is **worse** than expected (disappointment).

### Definition 06.2.2 — Dopamine

A monoamine neurotransmitter produced primarily in the **ventral tegmental area (VTA)** and **substantia nigra pars compacta (SNc)**. In the context of learning, dopamine neurons encode the RPE signal $\delta_t$ through their phasic firing rate:

- **Burst firing** (above baseline ~4 Hz → 20+ Hz): encodes $\delta > 0$
- **Baseline tonic firing** (~4 Hz): encodes $\delta = 0$
- **Pause/dip** (below baseline → 0 Hz): encodes $\delta < 0$

### Definition 06.2.3 — Temporal Difference (TD) Learning

A class of model-free RL algorithms that update value estimates based on the difference between **temporally successive predictions**, without waiting for the final outcome:

$$
V(s_t) \leftarrow V(s_t) + \alpha \cdot \delta_t
$$

The key insight: you can learn from incomplete sequences by bootstrapping — using your current estimate of the next state's value as a proxy for the true future return.

### Definition 06.2.4 — Value Function $V(s)$

The **expected cumulative discounted reward** from state $s$ onward, following policy $\pi$:

$$
V^\pi(s) = E_\pi\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k} \mid s_t = s\right]
$$

Neurally, $V(s)$ is encoded in the **ventral striatum** (nucleus accumbens) and **orbitofrontal cortex**.

### Definition 06.2.5 — Phasic vs. Tonic Dopamine

- **Phasic dopamine:** Brief bursts or dips (100–500 ms) encoding RPE. Drives learning and updating of predictions.
- **Tonic dopamine:** Sustained baseline level. Sets the overall "gain" of the reward system. Modulates motivation, exploration rate, and response vigor.

Low tonic dopamine → anhedonia, low motivation (depression).
High tonic dopamine → increased exploration, impulsivity (mania, stimulant drugs).

### Definition 06.2.6 — Reward Prediction (Expectation)

The brain's current estimate of upcoming reward, computed from learned associations. Mathematically: $V(s_t)$ — the value function evaluated at the current state. This prediction is what dopamine neurons compare against actual outcomes.

### Definition 06.2.7 — Temporal Discount Factor $\gamma$

The degree to which future rewards are devalued relative to immediate rewards:

$$
\text{Present value of reward } r \text{ at time } t+k = \gamma^k \cdot r
$$

- $\gamma = 0$: completely myopic (only immediate reward matters)
- $\gamma = 1$: no discounting (all future rewards equally valued)
- Typical biological $\gamma \approx 0.9$–$0.99$ (varies with serotonin levels, prefrontal function)

### Definition 06.2.8 — Eligibility Trace

A decaying memory of recently visited states that allows credit assignment across multiple time steps:

$$
e_t(s) = \gamma \lambda \cdot e_{t-1}(s) + \mathbf{1}[s_t = s]
$$

Neurally implemented via synaptic tags that mark recently active synapses as eligible for modification when the dopamine signal arrives.

---


## 🔬 2. Behavioral Mechanisms

### 2.1 Schultz's Three Conditions (1997)

Wolfram Schultz recorded from dopamine neurons in the VTA of monkeys performing a classical conditioning task. The three landmark findings:

**Condition A — Unexpected Reward (before learning):**
- Monkey receives juice with no preceding cue.
- Dopamine neurons fire a **burst** at the moment of reward delivery.
- Interpretation: $\delta = r - V(s) = r - 0 = r > 0$. The reward was unpredicted, so the full reward magnitude appears as positive RPE.

**Condition B — Expected Reward (after learning):**
- A light (CS) reliably precedes juice by 1 second.
- After training, dopamine neurons fire a **burst at CS onset** but show **no response at reward delivery**.
- Interpretation: The prediction has shifted backward in time. At CS: $\delta = 0 + \gamma V(s_{\text{reward}}) - V(s_{\text{pre-CS}}) > 0$ (CS now predicts reward). At reward: $\delta = r + \gamma V(s') - V(s_{\text{post-CS}}) = 0$ (reward is fully predicted).

**Condition C — Omitted Reward (prediction violation):**
- CS is presented but juice is withheld.
- Dopamine neurons fire a **burst at CS** (as in B) but show a **dip below baseline** at the time reward was expected.
- Interpretation: At expected reward time: $\delta = 0 + \gamma V(s') - V(s) < 0$. The predicted reward failed to materialize — negative RPE.

### 2.2 The Signal Transfer Phenomenon

During learning, the dopamine burst **migrates backward in time** from the US to the earliest reliable predictor (CS). This is precisely what TD learning predicts: value propagates backward through the state sequence via bootstrapping.

**Timeline of signal transfer:**
1. **Trial 1:** Burst at US only.
2. **Trials 2–5:** Burst at US diminishes; small burst begins at CS.
3. **Trials 10+:** Full burst at CS; no response at US.
4. **Omission trial:** Burst at CS; dip at expected US time.

This backward propagation is the neural implementation of the TD backup: $V(s_t) \leftarrow V(s_t) + \alpha[r + \gamma V(s_{t+1}) - V(s_t)]$.

### 2.3 Neural Circuitry

**Source:** VTA (ventral tegmental area) and SNc (substantia nigra pars compacta) — ~400,000 dopamine neurons in humans.

**Projections (parallel pathways):**
1. **Mesolimbic pathway** (VTA → Nucleus Accumbens): Reward valuation, motivation, "wanting."
2. **Mesocortical pathway** (VTA → Prefrontal Cortex): Working memory, planning, cognitive control.
3. **Nigrostriatal pathway** (SNc → Dorsal Striatum): Action selection, habit formation, motor programs.

**Mechanism of action:**
- Dopamine burst → D1 receptor activation → LTP (long-term potentiation) at corticostriatal synapses → strengthen the state-action association that preceded reward.
- Dopamine dip → D2 receptor disinhibition → LTD (long-term depression) → weaken the association.

### 2.4 Dysfunction States

| Condition | Dopamine Dysfunction | RPE Interpretation |
|-----------|---------------------|-------------------|
| **Addiction** | Drugs hijack RPE: massive $\delta > 0$ that never habituates | Artificial supernormal stimulus; $V(s_{\text{drug}})$ inflated beyond all natural rewards |
| **Depression/Anhedonia** | Low tonic DA; blunted phasic response | $\delta \approx 0$ for all outcomes; nothing feels surprising or rewarding |
| **ADHD/Hyperfocus** | Dysregulated phasic DA; high sensitivity to novel stimuli | Excessive $\delta$ for novel stimuli; insufficient $\delta$ for routine tasks |
| **Parkinson's** | SNc neuronal death → low nigrostriatal DA | Impaired action selection; motor programs cannot be initiated |
| **Schizophrenia** | Excessive mesolimbic DA | Aberrant salience: $\delta > 0$ assigned to irrelevant stimuli → delusions |

### 2.5 Dopamine and Temporal Discounting

The discount factor $\gamma$ is modulated by serotonin (5-HT) in the dorsal raphe nucleus. Low serotonin → low $\gamma$ → impulsive choices (preferring small immediate rewards over large delayed ones). This explains the comorbidity of impulsivity with serotonin-related disorders.

Dopamine itself modulates the **vigor** of action (how quickly/energetically the organism pursues reward) rather than the discount rate per se.

---


## 📐 3. Mathematical Formulations

### 3.1 The TD(0) Update Rule — Full Derivation

**Goal:** Learn the value function $V(s)$ from experience without a model of the environment.

**Starting point:** The true value function satisfies the Bellman expectation equation:

$$
V^\pi(s) = E_\pi[r_t + \gamma V^\pi(s_{t+1}) \mid s_t = s]
$$

We cannot compute this expectation exactly (we don't know the transition probabilities). Instead, we use a **sample-based stochastic approximation**:

**Step 1 — Observe a transition:** From state $s_t$, take action per policy $\pi$, observe reward $r_t$ and next state $s_{t+1}$.

**Step 2 — Compute the TD target:** The sample estimate of the right-hand side of Bellman:

$$
\text{TD target} = r_t + \gamma V(s_{t+1})
$$

**Step 3 — Compute the TD error (RPE):**

$$
\delta_t = \underbrace{r_t + \gamma V(s_{t+1})}_{\text{TD target (actual + bootstrap)}} - \underbrace{V(s_t)}_{\text{current prediction}}
$$

**Step 4 — Update the value estimate:**

$$
V(s_t) \leftarrow V(s_t) + \alpha \cdot \delta_t
$$

Expanding:

$$
V(s_t) \leftarrow V(s_t) + \alpha \left[ r_t + \gamma V(s_{t+1}) - V(s_t) \right]
$$

$$
V(s_t) \leftarrow (1 - \alpha) V(s_t) + \alpha \left[ r_t + \gamma V(s_{t+1}) \right]
$$

This is a **convex combination** of the old estimate and the new sample target, weighted by $\alpha$.

### 3.2 Convergence of TD(0)

**Theorem (Sutton, 1988; Dayan, 1992):** Under the following conditions, TD(0) converges to $V^\pi$ with probability 1:

1. All states are visited infinitely often.
2. The learning rate satisfies: $\sum_t \alpha_t = \infty$ and $\sum_t \alpha_t^2 < \infty$ (Robbins-Monro conditions).
3. The MDP is finite and the policy $\pi$ is fixed.

**Sketch of proof:** TD(0) is a stochastic approximation to the Bellman operator $T^\pi$:

$$
(T^\pi V)(s) = E_\pi[r + \gamma V(s') \mid s]
$$

$T^\pi$ is a $\gamma$-contraction in the sup-norm:

$$
\|T^\pi V_1 - T^\pi V_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty
$$

By the Banach fixed-point theorem, $T^\pi$ has a unique fixed point $V^\pi$. The stochastic approximation theory (Robbins-Monro) guarantees that the noisy iterates converge to this fixed point under the stated learning rate conditions. $\blacksquare$

### 3.3 Multi-Step TD Error Decomposition

The return from time $t$ can be written as a telescoping sum of TD errors:

$$
G_t - V(s_t) = \sum_{k=0}^{T-t-1} \gamma^k \delta_{t+k}
$$

**Proof by expansion:**

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

$$
\gamma \delta_{t+1} = \gamma r_{t+1} + \gamma^2 V(s_{t+2}) - \gamma V(s_{t+1})
$$

$$
\gamma^2 \delta_{t+2} = \gamma^2 r_{t+2} + \gamma^3 V(s_{t+3}) - \gamma^2 V(s_{t+2})
$$

Summing (telescoping cancellation of $V$ terms):

$$
\sum_{k=0}^{T-t-1} \gamma^k \delta_{t+k} = \sum_{k=0}^{T-t-1} \gamma^k r_{t+k} + \gamma^{T-t} V(s_T) - V(s_t)
$$

If $s_T$ is terminal ($V(s_T) = 0$):

$$
\sum_{k=0}^{T-t-1} \gamma^k \delta_{t+k} = G_t - V(s_t) \quad \blacksquare
$$

**Implication:** The total discounted return minus the baseline equals the sum of discounted TD errors. This is the foundation of the **advantage function** $A(s,a) = Q(s,a) - V(s)$ used in policy gradient methods.

### 3.4 Schultz's Data as TD Computation

Model the conditioning experiment as a 3-state MDP:

- $s_0$: pre-trial (no stimuli)
- $s_1$: CS presented (light on)
- $s_2$: US time (reward or no reward)

**Before learning:** $V(s_0) = V(s_1) = V(s_2) = 0$.

**Trial 1 (unexpected reward, $r = 1$ at $s_2$):**

$$
\delta_2 = r + \gamma V(s_3) - V(s_2) = 1 + 0 - 0 = +1 \quad \text{(burst at US)}
$$

$$
V(s_2) \leftarrow 0 + \alpha(1) = \alpha
$$

**Trial 2:**

At $s_1 \to s_2$ transition:

$$
\delta_1 = 0 + \gamma V(s_2) - V(s_1) = \gamma\alpha - 0 = \gamma\alpha > 0 \quad \text{(small burst at CS)}
$$

At $s_2$ (reward received):

$$
\delta_2 = 1 + 0 - V(s_2) = 1 - \alpha \quad \text{(reduced burst at US)}
$$

**After many trials (convergence):** $V(s_1) = \gamma$, $V(s_2) = 1$.

At CS: $\delta_1 = 0 + \gamma V(s_2) - V(s_1) = \gamma \cdot 1 - \gamma = 0$ ... wait, let's be more careful.

Actually at convergence with $\gamma < 1$: $V(s_1) = \gamma \cdot 1 = \gamma$ (one step before reward of 1).

$$
\delta_1 = 0 + \gamma V(s_2) - V(s_1) = \gamma(1) - \gamma = 0
$$

Hmm — but Schultz shows a burst at CS. The resolution: the burst occurs during **acquisition** (before full convergence), and at convergence the burst is at the **earliest unpredicted predictor**. If we add $s_0 \to s_1$:

$$
\delta_0 = 0 + \gamma V(s_1) - V(s_0) = \gamma^2 - V(s_0)
$$

At convergence: $V(s_0) = \gamma^2$, so $\delta_0 = 0$. The burst has propagated to whatever state first signals the upcoming reward chain. In Schultz's experiment, the CS is the earliest predictor, so the burst stabilizes there.

**Omission trial (reward withheld at $s_2$):**

$$
\delta_2 = 0 + \gamma V(s_3) - V(s_2) = 0 - 1 = -1 \quad \text{(dip below baseline)}
$$

This matches Schultz's observation of a pause in dopamine firing at the expected reward time.

### 3.5 TD(λ) — Bridging TD(0) and Monte Carlo

TD(λ) uses eligibility traces to blend TD(0) (bootstrap from next state) with Monte Carlo (wait for full return):

$$
V(s) \leftarrow V(s) + \alpha \delta_t \cdot e_t(s)
$$

where the eligibility trace:

$$
e_t(s) = \begin{cases} \gamma\lambda \cdot e_{t-1}(s) + 1 & \text{if } s = s_t \\ \gamma\lambda \cdot e_{t-1}(s) & \text{otherwise} \end{cases}
$$

- $\lambda = 0$: pure TD(0), update only the current state.
- $\lambda = 1$: equivalent to Monte Carlo (every-visit), update all states in the trajectory.
- $\lambda \in (0,1)$: intermediate — exponentially decaying credit to past states.

**Neural implementation:** Synaptic eligibility traces (Izhikevich, 2007) — recently active synapses remain "tagged" for ~seconds, eligible for modification when the dopamine signal arrives.

---


## ✍️ 4. Worked Examples

### Example 06.2.1 — Computing RPE Across a 4-State Episode

<details>
<summary>An agent traverses states s₁→s₂→s₃→s₄(terminal). Rewards: r₁=0, r₂=0, r₃=+5. Current value estimates: V(s₁)=2, V(s₂)=3, V(s₃)=4, V(s₄)=0. γ=0.9, α=0.1. Compute all TD errors and updated values.</summary>

**Step 1: Compute TD errors at each transition.**

Transition $s_1 \to s_2$ (reward $r_1 = 0$):

$$
\delta_1 = r_1 + \gamma V(s_2) - V(s_1) = 0 + 0.9(3) - 2 = 2.7 - 2 = +0.7
$$

Transition $s_2 \to s_3$ (reward $r_2 = 0$):

$$
\delta_2 = r_2 + \gamma V(s_3) - V(s_2) = 0 + 0.9(4) - 3 = 3.6 - 3 = +0.6
$$

Transition $s_3 \to s_4$ (reward $r_3 = +5$, terminal):

$$
\delta_3 = r_3 + \gamma V(s_4) - V(s_3) = 5 + 0.9(0) - 4 = 5 - 4 = +1.0
$$

**Step 2: Update values.**

$$
V(s_1) \leftarrow 2 + 0.1(0.7) = 2.07
$$

$$
V(s_2) \leftarrow 3 + 0.1(0.6) = 3.06
$$

$$
V(s_3) \leftarrow 4 + 0.1(1.0) = 4.10
$$

**Step 3: Verify with true values.**

True values (working backward): $V^*(s_3) = 5$, $V^*(s_2) = 0.9 \times 5 = 4.5$, $V^*(s_1) = 0.9 \times 4.5 = 4.05$.

All TD errors are positive → all current estimates are too low → values increase toward true values. ✓

**Dopamine interpretation:** All three transitions produce positive RPE (burst firing). The largest burst ($\delta_3 = 1.0$) occurs at the reward itself — this is the "unexpected reward" pattern from Schultz Condition A.

</details>

### Example 06.2.2 — Signal Transfer During Learning

<details>
<summary>Model Schultz's experiment: CS at t=1, US at t=2. γ=0.95, α=0.2. Start with V(CS)=V(US)=0. Simulate 10 trials showing the dopamine burst transferring from US to CS.</summary>

Each trial: $s_0$(pre) → $s_1$(CS) → $s_2$(US, r=1) → terminal.

| Trial | V(CS) before | V(US) before | δ at CS | δ at US | V(CS) after | V(US) after |
|-------|-------------|-------------|---------|---------|-------------|-------------|
| 1 | 0 | 0 | 0+0.95(0)−0 = 0 | 1+0−0 = **1.0** | 0 | 0.20 |
| 2 | 0 | 0.20 | 0+0.95(0.20)−0 = **0.19** | 1+0−0.20 = **0.80** | 0.038 | 0.36 |
| 3 | 0.038 | 0.36 | 0+0.95(0.36)−0.038 = **0.304** | 1+0−0.36 = **0.64** | 0.099 | 0.488 |
| 4 | 0.099 | 0.488 | 0+0.95(0.488)−0.099 = **0.365** | 1−0.488 = **0.512** | 0.172 | 0.590 |
| 5 | 0.172 | 0.590 | 0.95(0.590)−0.172 = **0.389** | 1−0.590 = **0.410** | 0.250 | 0.672 |
| 6 | 0.250 | 0.672 | 0.95(0.672)−0.250 = **0.388** | 1−0.672 = **0.328** | 0.328 | 0.738 |
| 7 | 0.328 | 0.738 | 0.95(0.738)−0.328 = **0.373** | 1−0.738 = **0.262** | 0.403 | 0.790 |
| 8 | 0.403 | 0.790 | 0.95(0.790)−0.403 = **0.348** | 1−0.790 = **0.210** | 0.472 | 0.832 |
| 9 | 0.472 | 0.832 | 0.95(0.832)−0.472 = **0.318** | 1−0.832 = **0.168** | 0.536 | 0.866 |
| 10 | 0.536 | 0.866 | 0.95(0.866)−0.536 = **0.287** | 1−0.866 = **0.134** | 0.593 | 0.893 |

**Observation:** δ at US **decreases** monotonically (1.0 → 0.134) while δ at CS **rises then plateaus** (0 → 0.389 → 0.287). The dopamine burst transfers from US to CS, exactly matching Schultz's recordings.

At convergence: $V(\text{US}) \to 1$, $V(\text{CS}) \to 0.95$, $\delta_{\text{US}} \to 0$, $\delta_{\text{CS}} \to 0$.

</details>

### Example 06.2.3 — Reward Omission (Negative RPE)

<details>
<summary>After convergence (V(CS)=0.95, V(US)=1.0), the reward is omitted on a probe trial. Compute the RPE at each time step.</summary>

**At CS presentation ($s_0 \to s_1$):**

$$
\delta_{\text{CS}} = 0 + \gamma V(\text{US}) - V(s_0) = 0.95(1.0) - V(s_0)
$$

If $V(s_0) = \gamma \cdot V(\text{CS}) = 0.95 \times 0.95 = 0.9025$:

$$
\delta_{\text{CS}} = 0.95 - 0.9025 = +0.0475 \approx 0 \quad \text{(minimal burst)}
$$

**At expected reward time (reward omitted, $r = 0$):**

$$
\delta_{\text{US}} = 0 + \gamma V(s_{\text{terminal}}) - V(\text{US}) = 0 + 0 - 1.0 = -1.0
$$

**Interpretation:** A massive negative RPE ($\delta = -1.0$) — the dopamine neurons **pause completely**. This is the neural correlate of disappointment/frustration. The value estimate will decrease:

$$
V(\text{US}) \leftarrow 1.0 + 0.2(-1.0) = 0.80
$$

One omission trial reduces $V(\text{US})$ by 20%. This is why a single betrayal of trust (expected reward omitted) produces such a strong negative emotional response — the RPE magnitude equals the full expected reward.

</details>

### Example 06.2.4 — Addiction as Hijacked RPE

<details>
<summary>A drug produces reward r=10 (vs. natural reward r=1). Model how the value function becomes distorted after 5 drug exposures vs. 5 natural reward exposures. α=0.2, γ=0.9.</summary>

**Natural reward pathway (r=1):**

Starting $V(\text{drug cue}) = 0$:

$$
V_n = 1 \cdot \gamma \cdot [1 - (1-\alpha)^n] = 0.9[1 - 0.8^n]
$$

After 5 trials: $V_5 = 0.9(1 - 0.8^5) = 0.9(1 - 0.328) = 0.9 \times 0.672 = 0.605$

**Drug pathway (r=10):**

The drug produces supraphysiological dopamine release. Effective reward signal: $r = 10$.

$$
V_n^{\text{drug}} = 10 \cdot \gamma \cdot [1 - (1-\alpha)^n] = 9.0[1 - 0.8^n]
$$

After 5 trials: $V_5^{\text{drug}} = 9.0 \times 0.672 = 6.05$

**Comparison:**

$$
\frac{V^{\text{drug}}}{V^{\text{natural}}} = \frac{6.05}{0.605} = 10
$$

The drug cue is valued **10× higher** than natural reward cues. All other activities (food, social connection, exercise) have $V \lt  1$ while the drug cue has $V \gt  6$. The policy becomes:

$$
\pi^*(s) = \arg\max_a Q(s,a) = a_{\text{drug}} \quad \forall s
$$

**Tolerance:** With repeated use, the brain downregulates dopamine receptors, effectively reducing $\alpha$ for the drug. Now $\delta$ for the drug decreases (tolerance), but $\delta$ for natural rewards becomes **negative** (anhedonia) because the baseline expectation is calibrated to drug-level rewards.

</details>

### Example 06.2.5 — Hyperfocus as RPE Dysregulation (ADHD/Trauma Context)

<details>
<summary>Model hyperfocus: a task produces variable reward (interesting moments). For a dysregulated dopamine system, the RPE sensitivity is amplified by factor k=3 for novel stimuli but dampened (k=0.3) for routine stimuli. Show how this creates the hyperfocus/boredom dichotomy.</summary>

**Standard agent:** $\delta = r + \gamma V(s') - V(s)$, update: $\Delta V = \alpha \delta$

**Dysregulated agent:** $\delta_{\text{eff}} = k \cdot \delta$ where $k$ depends on novelty:

$$
k = \begin{cases} 3.0 & \text{if stimulus is novel/interesting} \\ 0.3 & \text{if stimulus is routine/familiar} \end{cases}
$$

**Scenario: Two tasks available.**
- Task A (routine): $r = 2$ per time step, predictable → $\delta \approx 0$ after learning → $\delta_{\text{eff}} = 0.3 \times 0 = 0$
- Task B (novel project): $r$ varies between 0 and 8, mean = 2 → frequent $\delta \neq 0$ → $\delta_{\text{eff}} = 3 \times \delta$

For the dysregulated agent, Task B produces **9× the effective learning signal** compared to a neurotypical agent. The value function for Task B inflates rapidly:

$$
V_{\text{dysreg}}(\text{Task B}) = V_{\text{typical}} + \sum_t (k-1)\alpha\delta_t \gg V_{\text{typical}}(\text{Task A})
$$

**Result:** The agent becomes locked into Task B (hyperfocus) because switching to Task A produces near-zero RPE. This is not a "choice" — it's a policy dictated by a miscalibrated reward signal.

**Clinical parallel:** The trauma-adapted nervous system amplifies RPE for threat-related stimuli (hypervigilance) and dampens RPE for safety-related stimuli (emotional numbing). Same mechanism, different stimulus categories.

</details>

---

## 🧠 5. AI/RL Translation

| Neuroscience | AI/RL Algorithm | Mathematical Identity |
|---|---|---|
| Dopamine burst/dip | TD error $\delta_t$ | $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ |
| VTA/SNc neurons | Error computation module | Scalar signal broadcast |
| Nucleus Accumbens | Value function $V(s)$ | Critic network |
| Dorsal Striatum | Policy $\pi(a|s)$ | Actor network |
| Synaptic eligibility trace | $e_t(s)$ in TD(λ) | Decaying credit assignment |
| Signal transfer (US→CS) | Value backup propagation | Bootstrapping |
| Reward omission dip | Negative TD error | $\delta < 0$ → decrease $V$ |
| Tonic dopamine level | Exploration temperature $\tau$ | Higher tonic → more exploration |
| D1/D2 receptor balance | LTP/LTD at synapses | Strengthen/weaken associations |
| Addiction (supernormal stimulus) | Reward hacking | Agent exploits reward signal flaw |

### The Schultz-Sutton Isomorphism

The correspondence between dopamine neurons and TD learning is not merely an analogy — it is a **quantitative isomorphism**:

1. **Timing:** Dopamine bursts occur at the precise moment predicted by the TD error computation.
2. **Magnitude:** Burst amplitude scales linearly with RPE magnitude (Bayer & Glimcher, 2005).
3. **Sign:** Bursts for $\delta > 0$, pauses for $\delta < 0$, baseline for $\delta = 0$.
4. **Transfer:** The signal migrates backward in time exactly as TD bootstrapping predicts.
5. **Blocking:** No dopamine response to redundant predictors (Waelti et al., 2001).

This is one of the most successful quantitative theories in all of neuroscience.

---

## 🧬 6. Synthesis

### Bidirectional Design Implications

**From Neuroscience → AI Design:**

1. **Tonic/phasic separation:** The brain separates the "motivation/exploration" signal (tonic DA) from the "learning" signal (phasic DA). AI systems could benefit from separating the exploration schedule from the value update — e.g., using a separate "curiosity module" (Pathak et al., 2017) that modulates exploration independently of the reward signal.

2. **Eligibility traces are biologically real:** The brain doesn't just update the most recent state — it updates all recently-active synapses proportionally to their recency. This validates TD(λ) over TD(0) as the more biologically faithful algorithm.

3. **Reward magnitude asymmetry:** Dopamine dips are bounded (neurons can't fire below 0 Hz) but bursts can be very large. This creates an asymmetry: positive surprises produce larger learning signals than negative surprises. AI systems might benefit from asymmetric learning rates: $\alpha^+ > \alpha^-$.

**From AI → Human Intervention (Therapeutic Implications):**

1. **Anhedonia as low learning rate:** If tonic dopamine is depleted, $\alpha_{\text{eff}} \approx 0$ — positive experiences produce no update. Intervention: artificially increase $\alpha$ via behavioral activation (force exposure to rewarding stimuli even without motivation) or pharmacology (dopamine agonists).

2. **Trauma hypervigilance as miscalibrated $V(s)$:** The trauma-adapted brain has $V(\text{safe situations}) \approx V(\text{dangerous situations})$ — everything is predicted to be threatening. The TD errors for actual safety are positive ($\delta > 0$) but the system has learned to **ignore** positive RPE for social stimuli (dampened $\alpha$ for trust-related states). Therapy must selectively increase $\alpha$ for safety signals.

3. **The exploration-exploitation dilemma in recovery:** A person with avoidant attachment has a policy that exploits isolation (known, moderate reward). Trying vulnerability is exploration with high perceived variance. The RL solution: **optimistic initialization** — artificially set $V(\text{trust}) > V(\text{isolate})$ initially, forcing exploration. Therapeutically: create safe relationships where trust is reliably rewarded, building positive $V$ estimates from scratch.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- [06.1 - Classical & Operant Conditioning](06.1---Classical-&-Operant-Conditioning) — Rescorla-Wagner as the precursor to TD learning
- [06.3 - Q-Learning & The Bellman Equation](06.3---Q-Learning-&-The-Bellman-Equation) — Extending TD to action-value functions
- [06.4 - Polyvagal Theory & Autonomic Regulation](06.4---Polyvagal-Theory-&-Autonomic-Regulation) — How autonomic state modulates the RPE system
- [06.5 - Trauma Adaptations - C-PTSD as Reinforcement Learning](06.5---Trauma-Adaptations---C-PTSD-as-Reinforcement-Learning) — RPE dysfunction in trauma
- [05.6 - Neuromodulators - Dopamine, Serotonin, Acetylcholine](05.6---Neuromodulators---Dopamine,-Serotonin,-Acetylcholine) — Full neurochemistry
- [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) — AI implementation of TD algorithms
- [34.4 - Autonomic Nervous System Telemetry - HRV](34.4---Autonomic-Nervous-System-Telemetry---HRV) — Measuring autonomic state

### Authoritative Sources
1. **Schultz, W.** (1997). A Neural Substrate of Prediction and Reward. *Science*, 275(5306), 1593–1599.
2. **Sutton, R.S. & Barto, A.G.** (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. Chapters 6 (TD Learning) and 15 (Neuroscience).
3. **David Silver** — UCL RL Course, Lecture 4: Model-Free Prediction.
4. **Bayer, H.M. & Glimcher, P.W.** (2005). Midbrain dopamine neurons encode a quantitative reward prediction error signal. *Neuron*, 47(1), 129–141.
5. **Montague, P.R., Dayan, P., & Sejnowski, T.J.** (1996). A framework for mesencephalic dopamine systems based on predictive Hebbian learning. *Journal of Neuroscience*, 16(5), 1936–1947.

### Practice
- [12.2_rpe_simulator.py](12.2_rpe_simulator.py) — TD RPE simulation matching Schultz 1997 firing patterns

---

*Next: [06.3 - Q-Learning & The Bellman Equation](06.3---Q-Learning-&-The-Bellman-Equation) →*

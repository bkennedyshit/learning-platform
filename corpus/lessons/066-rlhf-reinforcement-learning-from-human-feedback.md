---
title: "06.6 — RLHF: Reinforcement Learning from Human Feedback"
subject: "Behavioral Psychology & Reinforcement Learning"
catalog: advanced
audience_tier: higher-education
chapter: "6.6"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 06.6 — RLHF: Reinforcement Learning from Human Feedback

> *"The challenge of alignment is not getting the AI to be smart — it's getting it to want what we want."*
> — Paul Christiano, OpenAI Alignment Team

> *"Human nervous systems co-regulate. A calm person can bring a panicked person into a Ventral Vagal state via tone of voice and micro-expressions."*
> — Stephen Porges, *The Polyvagal Theory*

This chapter formalizes **Reinforcement Learning from Human Feedback (RLHF)** — the technique that transformed large language models from next-token predictors into aligned assistants. We derive the full pipeline (preference collection → reward model training → PPO optimization) and draw the deep parallel to **co-regulation**: just as a calm nervous system shapes a dysregulated one through feedback, human evaluators shape AI behavior through preference signals.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the three-stage RLHF pipeline (SFT → Reward Model → PPO).
2. Derive the Bradley-Terry preference model from first principles.
3. Write the reward model loss function and explain its training.
4. Derive the PPO clipped surrogate objective and explain why clipping prevents catastrophic updates.
5. Compute the KL-penalty term and explain its role in preventing reward hacking.
6. Map RLHF to co-regulation: human evaluator = regulating nervous system.
7. Identify failure modes (reward hacking, mode collapse, sycophancy) and their biological analogs.

---

## 🖼️ Visual Anchor — RLHF Pipeline

![psych-06__fig4](psych-06__fig4.svg)

---

## 📚 1. Definitions

### Definition 06.6.1 — RLHF (Reinforcement Learning from Human Feedback)

A training paradigm where a language model's policy is optimized using a **reward signal derived from human preferences** rather than a hand-coded reward function. The pipeline:

1. **SFT:** Fine-tune base model on human demonstrations.
2. **Reward Model:** Train a scalar reward function $r_\theta(x, y)$ from pairwise human preferences.
3. **RL Optimization:** Optimize the policy $\pi$ to maximize $r_\theta$ using PPO, with a KL penalty to prevent divergence from $\pi_{\text{SFT}}$.

### Definition 06.6.2 — Bradley-Terry Preference Model

A probabilistic model for pairwise comparisons. Given two responses $y_1, y_2$ to prompt $x$:

$$
P(y_1 \succ y_2 | x) = \sigma(r(x, y_1) - r(x, y_2)) = \frac{e^{r(x,y_1)}}{e^{r(x,y_1)} + e^{r(x,y_2)}}
$$

where $\sigma$ is the sigmoid function and $r(x, y)$ is the latent "quality" score.

### Definition 06.6.3 — Reward Model $r_\theta(x, y)$

A neural network (typically initialized from the SFT model) that maps (prompt, response) pairs to a scalar reward:

$$
r_\theta: \mathcal{X} \times \mathcal{Y} \to \mathbb{R}
$$

Trained to predict human preferences via the Bradley-Terry loss.

### Definition 06.6.4 — PPO (Proximal Policy Optimization)

A policy gradient algorithm (Schulman et al., 2017) that constrains policy updates to a "trust region" via clipping:

$$
L^{\text{CLIP}}(\theta) = E_t\left[\min\left(r_t(\theta)\hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]
$$

where $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$ is the probability ratio and $\hat{A}_t$ is the advantage estimate.

### Definition 06.6.5 — KL Divergence Penalty

A regularization term preventing the optimized policy from diverging too far from the reference (SFT) policy:

$$
D_{\text{KL}}(\pi_\theta \| \pi_{\text{ref}}) = E_{x \sim D, y \sim \pi_\theta}\left[\log\frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)}\right]
$$

The full RLHF objective:

$$
\max_\theta E_{x \sim D, y \sim \pi_\theta}\left[r_\theta(x, y) - \beta \cdot D_{\text{KL}}(\pi_\theta(y|x) \| \pi_{\text{ref}}(y|x))\right]
$$

### Definition 06.6.6 — Reward Hacking

When the policy finds outputs that score high on the reward model $r_\theta$ without actually being high-quality by human standards. The reward model is an imperfect proxy for true human preferences — the policy can exploit its blind spots.

**Biological analog:** Sycophancy/people-pleasing — optimizing for the *appearance* of approval rather than genuine connection.

### Definition 06.6.7 — Mode Collapse

When the policy converges to a narrow set of "safe" outputs that reliably score well, losing diversity and creativity. The KL penalty prevents this by penalizing deviation from the diverse SFT policy.

**Biological analog:** The "fawn" trauma response — producing only behaviors that the evaluator approves of, at the cost of authentic self-expression.

### Definition 06.6.8 — Advantage Function $\hat{A}_t$

The advantage estimates how much better an action is compared to the average action in that state:

$$
\hat{A}_t = Q(s_t, a_t) - V(s_t) \approx r_t + \gamma V(s_{t+1}) - V(s_t) = \delta_t
$$

In RLHF for language models: $\hat{A}_t$ measures how much better the generated token is compared to what the value function predicted. Positive advantage → reinforce this token choice. Negative advantage → discourage it.

### Definition 06.6.9 — Generalized Advantage Estimation (GAE)

A variance-reduction technique that blends TD errors across multiple time steps:

$$
\hat{A}_t^{\text{GAE}(\gamma,\lambda)} = \sum_{l=0}^{\infty}(\gamma\lambda)^l \delta_{t+l}
$$

where $\lambda \in [0,1]$ controls the bias-variance tradeoff:
- $\lambda = 0$: pure TD (low variance, high bias)
- $\lambda = 1$: pure Monte Carlo (high variance, low bias)

---


## 🔬 2. Behavioral Mechanisms

### 2.1 Co-Regulation as Biological RLHF

The RLHF pipeline has a precise biological analog in **interpersonal co-regulation**:

| RLHF Stage | Co-Regulation Analog |
|---|---|
| Base model (pre-training) | Innate temperament + early experiences |
| SFT (supervised fine-tuning) | Childhood imitation of caregiver behavior |
| Human evaluator preferences | Caregiver's facial expressions, tone, micro-reactions |
| Reward model training | Internalizing "what makes others respond positively" |
| PPO optimization | Adjusting behavior based on internalized model |
| KL penalty | Maintaining authentic self (not losing identity to please) |

### 2.2 The Preference Signal in Human Development

From infancy, humans learn through preference signals:

1. **Infant smiles → caregiver smiles back** (positive preference signal)
2. **Infant cries → caregiver soothes** (the "reward" of co-regulation)
3. **Infant explores → caregiver shows approval/concern** (shaping exploration)

The child builds an internal **reward model** (the "internalized other") that predicts which behaviors will elicit positive responses. This is literally a learned $r_\theta(x, y)$ mapping (context, behavior) → expected social reward.

### 2.3 Secure vs. Insecure Reward Models

**Secure attachment** → well-calibrated reward model:
- Accurate prediction of when vulnerability will be met with warmth
- Balanced: rewards both autonomy AND connection
- Robust: doesn't collapse from single negative experience

**Anxious attachment** → over-sensitive reward model:
- Amplifies any signal of disapproval
- Over-optimizes for proximity/approval (mode collapse toward pleasing)
- Equivalent to: KL penalty too low (policy drifts far from authentic self)

**Avoidant attachment** → under-trained reward model:
- Ignores social reward signals
- Doesn't update from positive interpersonal feedback
- Equivalent to: reward model frozen/disconnected from policy optimization

### 2.4 The Evaluator's Nervous System State Matters

In RLHF, the quality of alignment depends on the **quality of the evaluator**. Similarly:

- A **ventral vagal** (calm, regulated) evaluator provides consistent, nuanced feedback → good reward model.
- A **sympathetic** (stressed, reactive) evaluator provides inconsistent, threat-biased feedback → noisy reward model.
- A **dorsal vagal** (checked out) evaluator provides no feedback → no learning.

This is why the therapeutic relationship quality predicts outcomes more than the specific technique used (Wampold, 2015). The therapist IS the reward model.

### 2.5 Failure Modes

| RLHF Failure | Behavioral Analog | Mechanism |
|---|---|---|
| Reward hacking | People-pleasing / fawning | Optimizing proxy (approval) not true objective (connection) |
| Mode collapse | Loss of authentic self | Over-constraining to "safe" behaviors |
| Sycophancy | Codependency | Always agreeing with evaluator regardless of truth |
| Reward model misspecification | Faulty neuroception | Internal model of "what's safe" is miscalibrated |
| KL penalty too high | Rigidity / inability to change | Can't deviate from old patterns even when feedback says to |
| KL penalty too low | Identity dissolution | Loses core self trying to please everyone |

---

## 📐 3. Mathematical Formulations

### 3.1 Reward Model Training — Full Derivation

**Data:** A dataset of preference pairs $\mathcal{D} = \{(x^{(i)}, y_w^{(i)}, y_l^{(i)})\}_{i=1}^N$ where $y_w \succ y_l$ (human prefers $y_w$ over $y_l$ given prompt $x$).

**Model:** Bradley-Terry preference model:

$$
P(y_w \succ y_l | x) = \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))
$$

where $\sigma(z) = \frac{1}{1+e^{-z}}$ is the sigmoid function.

**Loss function (negative log-likelihood):**

$$
\mathcal{L}_{\text{RM}}(\theta) = -E_{(x, y_w, y_l) \sim \mathcal{D}}\left[\log \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))\right]
$$

**Derivation of gradient:**

Let $\Delta r = r_\theta(x, y_w) - r_\theta(x, y_l)$.

$$
\frac{\partial \mathcal{L}}{\partial \theta} = -E\left[\frac{\sigma'(\Delta r)}{\sigma(\Delta r)} \cdot \frac{\partial \Delta r}{\partial \theta}\right]
$$

Using $\sigma'(z) = \sigma(z)(1-\sigma(z))$:

$$
\frac{\partial \mathcal{L}}{\partial \theta} = -E\left[(1 - \sigma(\Delta r)) \cdot \left(\frac{\partial r_\theta(x,y_w)}{\partial \theta} - \frac{\partial r_\theta(x,y_l)}{\partial \theta}\right)\right]
$$

**Interpretation:** When the model already correctly ranks the pair ($\sigma(\Delta r) \approx 1$), the gradient is small (no update needed). When it's wrong ($\sigma(\Delta r) \approx 0$), the gradient is large (strong correction). This is exactly the RPE principle: learning occurs only when there's a prediction error.

### 3.2 The RLHF Objective — Full Derivation

**Goal:** Find policy $\pi_\theta$ that maximizes expected reward while staying close to reference:

$$
\max_\theta \; J(\theta) = E_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot|x)}\left[r_\phi(x, y)\right] - \beta \cdot E_{x \sim \mathcal{D}}\left[D_{\text{KL}}(\pi_\theta(\cdot|x) \| \pi_{\text{ref}}(\cdot|x))\right]
$$

**Expanding the KL term:**

$$
D_{\text{KL}}(\pi_\theta \| \pi_{\text{ref}}) = E_{y \sim \pi_\theta}\left[\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x)\right]
$$

**Combined objective (per-token for language models):**

$$
J(\theta) = E_{x, y \sim \pi_\theta}\left[r_\phi(x,y) - \beta \log\frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)}\right]
$$

**Optimal solution (closed form):**

Setting $\nabla_\theta J = 0$ and solving:

$$
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \cdot \exp\left(\frac{r_\phi(x,y)}{\beta}\right)
$$

where $Z(x) = \sum_y \pi_{\text{ref}}(y|x) \exp(r_\phi(x,y)/\beta)$ is the partition function.

**Interpretation:** The optimal RLHF policy is the reference policy **reweighted** by the exponentiated reward. High-reward responses get upweighted; low-reward responses get downweighted. $\beta$ controls how aggressively the reweighting occurs.

### 3.3 PPO Clipped Surrogate Objective — Derivation

**Problem:** Policy gradient methods can make catastrophically large updates. PPO constrains updates.

**Define the probability ratio:**

$$
r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{\text{old}}}(a_t | s_t)}
$$

**Vanilla policy gradient (REINFORCE):**

$$
L^{\text{PG}}(\theta) = E_t\left[r_t(\theta) \cdot \hat{A}_t\right]
$$

where $\hat{A}_t$ is the advantage estimate (how much better this action was than average).

**Problem:** If $r_t(\theta)$ becomes very large (policy changed a lot), the update is unstable.

**PPO solution — clip the ratio:**

$$
L^{\text{CLIP}}(\theta) = E_t\left[\min\left(r_t(\theta)\hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]
$$

**How clipping works:**

Case 1: $\hat{A}_t > 0$ (action was good, want to increase probability):
- If $r_t > 1+\epsilon$: clip activates, gradient = 0. Prevents over-increasing.
- If $r_t \leq 1+\epsilon$: normal gradient, increase probability.

Case 2: $\hat{A}_t < 0$ (action was bad, want to decrease probability):
- If $r_t < 1-\epsilon$: clip activates, gradient = 0. Prevents over-decreasing.
- If $r_t \geq 1-\epsilon$: normal gradient, decrease probability.

**Biological analog:** This is the **window of tolerance**. The nervous system can only process bounded changes per time step. Updates exceeding the window cause system crash (mode collapse / dissociation). PPO's $\epsilon$ IS the computational window of tolerance.

### 3.4 DPO — Direct Preference Optimization

DPO (Rafailov et al., 2023) eliminates the explicit reward model by directly optimizing the policy from preferences:

$$
\mathcal{L}_{\text{DPO}}(\theta) = -E_{(x,y_w,y_l)}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]
$$

**Derivation:** Starting from the closed-form optimal policy $\pi^*(y|x) \propto \pi_{\text{ref}}(y|x)\exp(r(x,y)/\beta)$, we can express the reward as:

$$
r(x,y) = \beta\log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta\log Z(x)
$$

Substituting into the Bradley-Terry loss and noting that $Z(x)$ cancels in the difference:

$$
r(x,y_w) - r(x,y_l) = \beta\log\frac{\pi^*(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta\log\frac{\pi^*(y_l|x)}{\pi_{\text{ref}}(y_l|x)}
$$

Replacing $\pi^*$ with the parameterized $\pi_\theta$ gives the DPO loss. $\blacksquare$

### 3.5 The KL-Reward Tradeoff (Pareto Frontier)

As $\beta$ varies, we trace a Pareto frontier:

- $\beta \to 0$: Pure reward maximization. Policy diverges from reference. Risk of reward hacking.
- $\beta \to \infty$: Policy = reference (no optimization). Safe but unaligned.
- Optimal $\beta$: Balances alignment (high reward) with coherence (low KL).

The KL at optimum:

$$
D_{\text{KL}}(\pi^* \| \pi_{\text{ref}}) = \frac{1}{\beta}\left(E_{\pi^*}[r(x,y)] - E_{\pi_{\text{ref}}}[r(x,y)]\right) - \log Z
$$

---


## ✍️ 4. Worked Examples

### Example 06.6.1 — Reward Model Loss Computation

<details>
<summary>Given 3 preference pairs with reward model scores: (r_w=2.1, r_l=0.8), (r_w=1.5, r_l=1.3), (r_w=3.0, r_l=−0.5). Compute the Bradley-Terry loss for each pair and the total loss.</summary>

**Pair 1:** $\Delta r = 2.1 - 0.8 = 1.3$

$$
\sigma(1.3) = \frac{1}{1+e^{-1.3}} = \frac{1}{1+0.2725} = 0.786
$$

$$
\mathcal{L}_1 = -\log(0.786) = -(-0.241) = 0.241
$$

**Pair 2:** $\Delta r = 1.5 - 1.3 = 0.2$

$$
\sigma(0.2) = \frac{1}{1+e^{-0.2}} = \frac{1}{1+0.8187} = 0.550
$$

$$
\mathcal{L}_2 = -\log(0.550) = 0.598
$$

**Pair 3:** $\Delta r = 3.0 - (-0.5) = 3.5$

$$
\sigma(3.5) = \frac{1}{1+e^{-3.5}} = \frac{1}{1+0.0302} = 0.971
$$

$$
\mathcal{L}_3 = -\log(0.971) = 0.029
$$

**Total loss:**

$$
\mathcal{L} = \frac{1}{3}(0.241 + 0.598 + 0.029) = \frac{0.868}{3} = 0.289
$$

**Interpretation:** Pair 2 contributes the most loss (0.598) because the reward gap is small (0.2) — the model is uncertain. Pair 3 contributes almost nothing (0.029) because the gap is large (3.5) — the model is already confident. This mirrors the RPE principle: learning signal is proportional to surprise.

</details>

### Example 06.6.2 — PPO Clipping in Action

<details>
<summary>Old policy: π_old(a|s) = 0.4. New policy: π_θ(a|s) = 0.7. Advantage: Â = +2.0. ε = 0.2. Compute the clipped and unclipped objectives and determine which is used.</summary>

**Step 1: Probability ratio:**

$$
r_t(\theta) = \frac{\pi_\theta(a|s)}{\pi_{\text{old}}(a|s)} = \frac{0.7}{0.4} = 1.75
$$

**Step 2: Unclipped objective:**

$$
L^{\text{unclipped}} = r_t \cdot \hat{A} = 1.75 \times 2.0 = 3.5
$$

**Step 3: Clipped ratio:**

$$
\text{clip}(1.75, 1-0.2, 1+0.2) = \text{clip}(1.75, 0.8, 1.2) = 1.2
$$

(1.75 exceeds upper bound 1.2, so clipped to 1.2)

**Step 4: Clipped objective:**

$$
L^{\text{clipped}} = 1.2 \times 2.0 = 2.4
$$

**Step 5: PPO takes the minimum:**

$$
L^{\text{CLIP}} = \min(3.5, 2.4) = 2.4
$$

**Interpretation:** The policy wants to increase this action's probability (Â > 0), but it's already increased too much (ratio 1.75 > 1.2). PPO clips the objective to prevent the over-large update. The effective gradient is as if the ratio were only 1.2.

**Biological analog:** The person received positive feedback for a behavior and wants to do it much more. But the window of tolerance says "don't change too fast" — bounded update prevents overcorrection (which could lead to people-pleasing/fawning).

</details>

### Example 06.6.3 — KL Penalty Computation

<details>
<summary>For a simple 3-token vocabulary, π_θ = [0.6, 0.3, 0.1] and π_ref = [0.4, 0.4, 0.2]. Compute D_KL(π_θ || π_ref) and the penalized reward if r=5.0 and β=0.5.</summary>

**KL divergence:**

$$
D_{\text{KL}} = \sum_i \pi_\theta(i) \log\frac{\pi_\theta(i)}{\pi_{\text{ref}}(i)}
$$

$$
= 0.6\log\frac{0.6}{0.4} + 0.3\log\frac{0.3}{0.4} + 0.1\log\frac{0.1}{0.2}
$$

$$
= 0.6\log(1.5) + 0.3\log(0.75) + 0.1\log(0.5)
$$

$$
= 0.6(0.405) + 0.3(-0.288) + 0.1(-0.693)
$$

$$
= 0.243 - 0.086 - 0.069 = 0.088 \text{ nats}
$$

**Penalized reward:**

$$
r_{\text{penalized}} = r - \beta \cdot D_{\text{KL}} = 5.0 - 0.5 \times 0.088 = 5.0 - 0.044 = 4.956
$$

**Interpretation:** The KL penalty is small here (0.044) because the policies are similar. If π_θ diverged more (e.g., [0.95, 0.04, 0.01]), the penalty would be much larger, preventing reward hacking through extreme policy shifts.

</details>

### Example 06.6.4 — Co-Regulation as RLHF (Therapeutic Session)

<details>
<summary>Model a therapy session as RLHF. The client (policy π) produces behavioral "outputs." The therapist (reward model) provides preference signals. Show how 5 sessions update the client's internal reward model.</summary>

**Setup:**
- Client's behavioral repertoire: {share feelings, deflect with humor, intellectualize, withdraw}
- Therapist's preference ordering: share > deflect > intellectualize > withdraw
- Client's initial policy (avoidant): π₀ = [0.05, 0.30, 0.45, 0.20]

**Session 1:** Client intellectualizes (most probable action). Therapist gently redirects toward feeling.
- Preference pair: (share feelings, intellectualize) → share ≻ intellectualize
- Reward model update: r(share) ↑, r(intellectualize) ↓

**Session 2:** Client deflects with humor. Therapist acknowledges humor but asks what's underneath.
- Preference pair: (share, deflect) → share ≻ deflect
- r(share) ↑↑

**Session 3:** Client tentatively shares a feeling. Therapist responds with warmth (strong positive signal).
- This is the "unexpected reward" — massive positive RPE
- r(share) ↑↑↑, policy shifts: π₃ = [0.15, 0.30, 0.35, 0.20]

**Session 4:** Client shares more. Therapist validates.
- Continued positive reinforcement. π₄ = [0.25, 0.30, 0.30, 0.15]

**Session 5:** Client shares AND connects it to a need. Therapist mirrors and co-regulates.
- π₅ = [0.35, 0.28, 0.25, 0.12]

**KL from original:** $D_{\text{KL}}(\pi_5 \| \pi_0) = 0.35\log(7) + 0.28\log(0.93) + 0.25\log(0.56) + 0.12\log(0.6) = 0.68 + (-0.02) + (-0.14) + (-0.06) = 0.46$ nats.

The client has shifted significantly but the KL penalty (maintaining authentic self) prevents complete transformation into a "people-pleaser" (which would be π = [1.0, 0, 0, 0]).

</details>

---

## 🧠 5. AI/RL Translation

| RLHF Concept | Co-Regulation Analog | Mathematical Form |
|---|---|---|
| Preference pair $(y_w \succ y_l)$ | Therapist's differential response to behaviors | Training data for reward model |
| Reward model $r_\theta(x,y)$ | Internalized sense of "what's valued" | Learned function approximator |
| PPO policy update | Behavioral adjustment after feedback | $\pi_{\theta+1} = \pi_\theta + \alpha \nabla J$ |
| KL penalty | Maintaining authentic identity | $\beta \cdot D_{\text{KL}}(\pi \| \pi_{\text{ref}})$ |
| Clipping ($\epsilon$) | Window of tolerance | Bounded change per session |
| Reward hacking | People-pleasing / fawning | Optimizing proxy, not true objective |
| Mode collapse | Loss of self / codependency | All outputs converge to "safe" response |
| $\beta$ (KL coefficient) | Therapeutic pacing | How fast to push change |
| SFT (base policy) | Core personality / temperament | Starting point for optimization |
| Evaluator quality | Therapist regulation capacity | Determines reward model accuracy |

### The Deep Parallel

RLHF and co-regulation share the same computational structure:

1. **An agent** (AI model / dysregulated nervous system) produces outputs.
2. **An evaluator** (human labeler / co-regulating partner) provides preference signals.
3. **A reward model** (neural network / internalized other) learns to predict what the evaluator values.
4. **The policy** updates to maximize the learned reward while maintaining coherence (KL penalty / authentic self).

The key insight: **alignment is not programmed — it is learned through relationship**. Neither AI alignment nor human emotional regulation can be achieved in isolation. Both require an external signal from a well-calibrated evaluator.

---

## 🧬 6. Synthesis

### Designing Better RLHF from Co-Regulation Principles

**1. Evaluator State Matters:**
Just as a dysregulated therapist cannot effectively co-regulate a client, stressed/biased human evaluators produce noisy reward models. RLHF systems should:
- Monitor evaluator consistency (inter-rater agreement)
- Weight evaluators by their "regulation capacity" (agreement with expert consensus)
- Detect evaluator fatigue/bias and adjust accordingly

**2. Graduated Difficulty (Curriculum RLHF):**
Therapy doesn't start with the hardest material. Similarly, RLHF could benefit from:
- Starting with easy preference pairs (clear quality differences)
- Gradually introducing subtle distinctions
- This prevents early reward model overfitting to simple heuristics

**3. The KL Penalty as Therapeutic Pacing:**
- Too aggressive ($\beta$ too low): the model changes too fast, loses coherence (identity dissolution)
- Too conservative ($\beta$ too high): the model barely changes, alignment is slow (therapeutic resistance)
- Optimal: match the "window of tolerance" — push change at the maximum rate the system can integrate

**4. Preventing Reward Hacking = Preventing People-Pleasing:**
The fawn response (people-pleasing) is biological reward hacking — optimizing for the *appearance* of what the evaluator wants rather than genuine alignment. Solutions:
- Multiple diverse evaluators (not just one person's preferences)
- Reward model uncertainty estimation (know when you're extrapolating)
- Periodic re-evaluation with fresh human judgment (not just the learned proxy)

**5. The Impossibility of Self-Alignment:**
Just as a trauma-adapted nervous system cannot self-regulate without co-regulation, an AI cannot self-align without human feedback. The reward signal must come from outside the system. This is a fundamental architectural constraint, not a temporary limitation.

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- [06.5 - Trauma Adaptations - C-PTSD as Reinforcement Learning](06.5---Trauma-Adaptations---C-PTSD-as-Reinforcement-Learning) — Why external feedback is necessary for change
- [06.4 - Polyvagal Theory & Autonomic Regulation](06.4---Polyvagal-Theory-&-Autonomic-Regulation) — Co-regulation as the biological substrate
- [06.2 - Dopamine & Reward Prediction Error](06.2---Dopamine-&-Reward-Prediction-Error) — RPE as the learning signal in both systems
- [06.3 - Q-Learning & The Bellman Equation](06.3---Q-Learning-&-The-Bellman-Equation) — The RL foundations underlying PPO
- [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) — Full technical treatment of RLHF in AI/ML context

### Authoritative Sources
1. **Ouyang, L. et al.** (2022). Training language models to follow instructions with human feedback. *NeurIPS*.
2. **Schulman, J. et al.** (2017). Proximal Policy Optimization Algorithms. *arXiv:1707.06347*.
3. **Christiano, P. et al.** (2017). Deep reinforcement learning from human preferences. *NeurIPS*.
4. **Rafailov, R. et al.** (2023). Direct Preference Optimization: Your Language Model is Secretly a Reward Model. *NeurIPS*.
5. **Ziegler, D. et al.** (2019). Fine-Tuning Language Models from Human Preferences. *arXiv:1909.08593*.
6. **Sutton, R.S. & Barto, A.G.** (2018). *Reinforcement Learning: An Introduction*. Chapter 13 (Policy Gradient Methods).
7. **Porges, S.W.** (2011). *The Polyvagal Theory*. W.W. Norton.

### Practice
- [12.6_rlhf_skeleton.py](12.6_rlhf_skeleton.py) — Minimal RLHF reward model + PPO update skeleton

---

*← [06.5 - Trauma Adaptations - C-PTSD as Reinforcement Learning](06.5---Trauma-Adaptations---C-PTSD-as-Reinforcement-Learning) | Back to [Subject_Plan](Subject_Plan)*

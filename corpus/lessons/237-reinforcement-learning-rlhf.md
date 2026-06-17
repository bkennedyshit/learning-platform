---
title: "Reinforcement Learning Rlhf"
subject: "AI & Machine Learning Systems"
catalog: advanced
audience_tier: higher-education
chapter: "23.7"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 23.7 — Reinforcement Learning & RLHF

> *"Reinforcement learning is the first computational theory of intelligence — an agent learns what to do by trial and error, maximizing a numerical reward signal."*
> — **Richard S. Sutton**, *Reinforcement Learning: An Introduction* (2018)

Reinforcement Learning (RL) trains agents to make sequential decisions by maximizing cumulative reward. This chapter builds from Markov Decision Processes through the Bellman equations, derives Q-learning and policy gradient methods, and culminates in RLHF — the technique that aligns large language models with human preferences.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define a Markov Decision Process (MDP) and its components.
2. Derive the Bellman optimality equations for $V^*$ and $Q^*$.
3. Implement Q-learning with epsilon-greedy exploration on a gridworld.
4. Derive the policy gradient theorem (REINFORCE).
5. Explain Proximal Policy Optimization (PPO) and its clipped objective.
6. Describe the RLHF pipeline: reward model training → PPO fine-tuning.
7. Solve small MDPs by hand using value iteration.

---

## 🖼️ Visual Anchor — Agent-Environment Loop

![track-10__10.7-fig1](track-10__10.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 23.7.1 — Markov Decision Process (MDP)

An MDP is a tuple $(\mathcal{S}, \mathcal{A}, P, R, \gamma)$:
- $\mathcal{S}$: state space
- $\mathcal{A}$: action space
- $P(s'|s,a)$: transition probability
- $R(s,a)$: reward function (or $R(s,a,s')$)
- $\gamma \in [0,1)$: discount factor

### Definition 23.7.2 — Policy

A **policy** $\pi: \mathcal{S} \to \Delta(\mathcal{A})$ maps states to probability distributions over actions. $\pi(a|s)$ is the probability of taking action $a$ in state $s$.

### Definition 23.7.3 — Value Function

The **state-value function** under policy $\pi$:

$$
V^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^\infty \gamma^t R(s_t, a_t) \mid s_0 = s\right]
$$

The **action-value function** (Q-function):

$$
Q^\pi(s, a) = \mathbb{E}_\pi\left[\sum_{t=0}^\infty \gamma^t R(s_t, a_t) \mid s_0 = s, a_0 = a\right]
$$

### Definition 23.7.4 — Bellman Equations

**Bellman expectation equation:**

$$
V^\pi(s) = \sum_a \pi(a|s)\left[R(s,a) + \gamma\sum_{s'}P(s'|s,a)V^\pi(s')\right]
$$

**Bellman optimality equation:**

$$
V^*(s) = \max_a\left[R(s,a) + \gamma\sum_{s'}P(s'|s,a)V^*(s')\right]
$$

$$
Q^*(s,a) = R(s,a) + \gamma\sum_{s'}P(s'|s,a)\max_{a'}Q^*(s',a')
$$

### Definition 23.7.5 — Q-Learning Update

Model-free, off-policy temporal difference learning:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha\left[r_t + \gamma\max_{a'}Q(s_{t+1}, a') - Q(s_t, a_t)\right]
$$

The term in brackets is the **TD error** $\delta_t$.

### Definition 23.7.6 — RLHF Pipeline

1. **Supervised Fine-Tuning (SFT):** Train LLM on human demonstrations
2. **Reward Model:** Train $R_\phi(x, y)$ on human preference pairs $(y_w \succ y_l | x)$
3. **PPO Optimization:** Fine-tune LLM policy $\pi_\theta$ to maximize $R_\phi$ with KL penalty:

$$
\max_\theta \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot|x)}[R_\phi(x,y)] - \beta D_{KL}(\pi_\theta \| \pi_{ref})
$$

---

## 📐 2. Axioms / Postulates

**Postulate 10.7.P1 (Markov Property):** The future is independent of the past given the present: $P(s_{t+1}|s_0,\ldots,s_t,a_t) = P(s_{t+1}|s_t,a_t)$.

**Postulate 10.7.P2 (Reward Hypothesis — Sutton):** All goals can be described by the maximization of expected cumulative reward.

**Postulate 10.7.P3 (Exploration-Exploitation Tradeoff):** An agent must balance exploiting known high-reward actions with exploring unknown actions that might yield higher reward.

---

## 🛡️ 3. Lemmas

### Lemma 23.7.1 — Contraction of Bellman Operator

The Bellman optimality operator $T$ defined by $(TQ)(s,a) = R(s,a) + \gamma\sum_{s'}P(s'|s,a)\max_{a'}Q(s',a')$ is a $\gamma$-contraction in the sup-norm:

$$
\|TQ_1 - TQ_2\|_\infty \leq \gamma\|Q_1 - Q_2\|_\infty
$$

By the Banach fixed-point theorem, value iteration converges to the unique $Q^*$.

### Lemma 23.7.2 — Policy Gradient Log-Trick

$$
\nabla_\theta \pi_\theta(a|s) = \pi_\theta(a|s)\nabla_\theta\log\pi_\theta(a|s)
$$

This allows computing $\nabla_\theta\mathbb{E}_\pi[R]$ without differentiating through the environment.

---

## 👑 4. Theorems

### Theorem 23.7.1 — Policy Gradient Theorem (Sutton et al., 1999)

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^T \nabla_\theta\log\pi_\theta(a_t|s_t) \cdot G_t\right]
$$

where $G_t = \sum_{k=t}^T \gamma^{k-t}r_k$ is the return from time $t$.

### Theorem 23.7.2 — Q-Learning Convergence

Under conditions: (1) all state-action pairs visited infinitely often, (2) learning rate $\alpha_t$ satisfies $\sum\alpha_t = \infty$, $\sum\alpha_t^2 < \infty$, Q-learning converges to $Q^*$ with probability 1.

### Theorem 23.7.3 — PPO Clipped Objective

$$
L^{CLIP}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]
$$

where $r_t(\theta) = \pi_\theta(a_t|s_t)/\pi_{\theta_{old}}(a_t|s_t)$ and $\hat{A}_t$ is the advantage estimate. The clipping prevents destructively large policy updates.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Derivation of Bellman Equation

**Step 1.** Expand $V^\pi(s)$:

$$
V^\pi(s) = \mathbb{E}_\pi[r_0 + \gamma r_1 + \gamma^2 r_2 + \cdots | s_0 = s]
$$

**Step 2.** Separate first reward:

$$
= \mathbb{E}_\pi[r_0 | s_0=s] + \gamma\mathbb{E}_\pi[r_1 + \gamma r_2 + \cdots | s_0=s]
$$

**Step 3.** By Markov property, the second term depends only on $s_1$:

$$
= \sum_a\pi(a|s)R(s,a) + \gamma\sum_a\pi(a|s)\sum_{s'}P(s'|s,a)V^\pi(s')
$$

$$
= \sum_a\pi(a|s)\left[R(s,a) + \gamma\sum_{s'}P(s'|s,a)V^\pi(s')\right] \quad \blacksquare
$$

### 5.2 Policy Gradient Derivation (REINFORCE)

**Step 1.** Objective: $J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)]$ where $\tau = (s_0, a_0, r_0, s_1, \ldots)$.

**Step 2.** Trajectory probability: $p_\theta(\tau) = p(s_0)\prod_{t=0}^T\pi_\theta(a_t|s_t)P(s_{t+1}|s_t,a_t)$.

**Step 3.** Gradient:

$$
\nabla_\theta J = \nabla_\theta\int p_\theta(\tau)R(\tau)\,d\tau = \int p_\theta(\tau)\nabla_\theta\log p_\theta(\tau) \cdot R(\tau)\,d\tau
$$

**Step 4.** Log-probability of trajectory:

$$
\log p_\theta(\tau) = \log p(s_0) + \sum_t[\log\pi_\theta(a_t|s_t) + \log P(s_{t+1}|s_t,a_t)]
$$

Only $\log\pi_\theta$ depends on $\theta$:

$$
\nabla_\theta\log p_\theta(\tau) = \sum_t\nabla_\theta\log\pi_\theta(a_t|s_t)
$$

**Step 5.** Final result:

$$
\nabla_\theta J = \mathbb{E}_\tau\left[\left(\sum_t\nabla_\theta\log\pi_\theta(a_t|s_t)\right)R(\tau)\right]
$$

With baseline subtraction and causality: $\nabla_\theta J = \mathbb{E}\left[\sum_t\nabla_\theta\log\pi_\theta(a_t|s_t)(G_t - b(s_t))\right]$. $\blacksquare$

### 5.3 RLHF Reward Model — Bradley-Terry Model

**Step 1.** Given preference pair $(y_w, y_l)$ for prompt $x$ (human prefers $y_w$):

$$
P(y_w \succ y_l | x) = \sigma(R_\phi(x, y_w) - R_\phi(x, y_l))
$$

where $\sigma$ is sigmoid (Bradley-Terry model).

**Step 2.** Training loss (negative log-likelihood):

$$
\mathcal{L}(\phi) = -\mathbb{E}_{(x,y_w,y_l)}\left[\log\sigma(R_\phi(x,y_w) - R_\phi(x,y_l))\right]
$$

**Step 3.** The reward model learns to assign higher scores to human-preferred completions.

---

## 💻 6. Code Examples

### Q-Learning on 4×4 Gridworld

```python
import numpy as np

class GridWorld:
    """4x4 grid. Goal at (3,3). Walls, rewards, terminal states."""
    def __init__(self):
        self.size = 4
        self.goal = (3, 3)
        self.state = (0, 0)
        # Actions: 0=up, 1=right, 2=down, 3=left
        self.actions = [(-1,0), (0,1), (1,0), (0,-1)]
    
    def reset(self):
        self.state = (0, 0)
        return self.state
    
    def step(self, action):
        dr, dc = self.actions[action]
        r, c = self.state
        nr, nc = max(0, min(3, r+dr)), max(0, min(3, c+dc))
        self.state = (nr, nc)
        
        if self.state == self.goal:
            return self.state, 1.0, True   # reward, done
        return self.state, -0.01, False     # small step penalty

def q_learning(env, episodes=1000, alpha=0.1, gamma=0.99, epsilon=0.1):
    """
    Q-learning with epsilon-greedy.
    Q: (16, 4) — 16 states × 4 actions
    """
    Q = np.zeros((env.size**2, 4))  # shape: (16, 4)
    
    def state_idx(s): return s[0] * env.size + s[1]
    
    for ep in range(episodes):
        s = env.reset()
        done = False
        while not done:
            si = state_idx(s)
            # Epsilon-greedy action selection
            if np.random.random() < epsilon:
                a = np.random.randint(4)
            else:
                a = np.argmax(Q[si])  # exploit
            
            s_next, reward, done = env.step(a)
            si_next = state_idx(s_next)
            
            # Q-learning update (Bellman)
            td_target = reward + gamma * np.max(Q[si_next]) * (1 - done)
            td_error = td_target - Q[si, a]
            Q[si, a] += alpha * td_error  # shape: scalar update
            
            s = s_next
    
    return Q

env = GridWorld()
Q = q_learning(env, episodes=5000)
print("Learned Q-values (reshaped as 4x4 grid, max over actions = V*):")
V = Q.max(axis=1).reshape(4, 4)
print(np.round(V, 2))
```

> **See also:** `_practice/scripts/10.7_rl_q_learning.py` for full gridworld with visualization.

---

## 🧮 7. Worked Examples

### Example 23.7.E1 — Value Iteration on 3-State MDP

<details>
<summary>🔍 Full Solution</summary>

**MDP:** States $\{s_1, s_2, s_3\}$, actions $\{a, b\}$, $\gamma = 0.9$.

Transitions (deterministic): $s_1 \xrightarrow{a} s_2$ (r=1), $s_1 \xrightarrow{b} s_3$ (r=0), $s_2 \xrightarrow{a} s_3$ (r=2), $s_2 \xrightarrow{b} s_1$ (r=0), $s_3$ is terminal (r=0).

**Iteration 0:** $V_0 = (0, 0, 0)$.

**Iteration 1:**

$$
V_1(s_1) = \max(1 + 0.9 \cdot 0, 0 + 0.9 \cdot 0) = \max(1, 0) = 1 \quad (a^*)
$$

$$
V_1(s_2) = \max(2 + 0.9 \cdot 0, 0 + 0.9 \cdot 0) = \max(2, 0) = 2 \quad (a^*)
$$

$$
V_1(s_3) = 0 \quad \text{(terminal)}
$$

**Iteration 2:**

$$
V_2(s_1) = \max(1 + 0.9 \cdot 2, 0 + 0.9 \cdot 0) = \max(2.8, 0) = 2.8 \quad (a^*)
$$

$$
V_2(s_2) = \max(2 + 0.9 \cdot 0, 0 + 0.9 \cdot 1) = \max(2, 0.9) = 2 \quad (a^*)
$$

**Iteration 3:**

$$
V_3(s_1) = \max(1 + 0.9 \cdot 2, 0) = 2.8 \quad \text{(converged)}
$$

**Optimal policy:** $\pi^*(s_1) = a$, $\pi^*(s_2) = a$.

</details>

### Example 23.7.E2 — Q-Learning Update Step

<details>
<summary>🔍 Full Solution</summary>

**Problem:** Current $Q(s_1, \text{right}) = 0.5$. Agent takes action "right" in $s_1$, receives $r=1$, transitions to $s_2$. $\max_{a'}Q(s_2, a') = 0.8$. $\alpha=0.1$, $\gamma=0.99$.

**TD target:** $r + \gamma\max_{a'}Q(s_2,a') = 1 + 0.99 \times 0.8 = 1.792$.

**TD error:** $\delta = 1.792 - 0.5 = 1.292$.

**Update:** $Q(s_1, \text{right}) \leftarrow 0.5 + 0.1 \times 1.292 = 0.5 + 0.1292 = 0.6292$.

</details>

### Example 23.7.E3 — REINFORCE Gradient Estimate

<details>
<summary>🔍 Full Solution</summary>

**Problem:** Softmax policy $\pi_\theta(a|s) = \text{softmax}(\theta^T\phi(s,a))$. State features $\phi(s,a_1) = (1,0)$, $\phi(s,a_2) = (0,1)$. $\theta = (0.5, -0.5)$. Trajectory return $G = 3$ for action $a_1$.

**Step 1.** Policy: $\pi(a_1|s) = \frac{e^{0.5}}{e^{0.5}+e^{-0.5}} = \frac{1.649}{1.649+0.607} = 0.731$.

**Step 2.** Score function: $\nabla_\theta\log\pi(a_1|s) = \phi(s,a_1) - \sum_a\pi(a|s)\phi(s,a)$

$= (1,0) - [0.731(1,0) + 0.269(0,1)] = (1,0) - (0.731, 0.269) = (0.269, -0.269)$.

**Step 3.** Gradient estimate: $\nabla_\theta J \approx G \cdot \nabla_\theta\log\pi = 3 \times (0.269, -0.269) = (0.807, -0.807)$.

**Interpretation:** Increase $\theta_1$ (makes $a_1$ more likely) since $a_1$ led to positive return.

</details>

### Example 23.7.E4 — PPO Clipped Ratio

<details>
<summary>🔍 Full Solution</summary>

**Problem:** Old policy $\pi_{old}(a|s) = 0.3$, new policy $\pi_\theta(a|s) = 0.6$, advantage $\hat{A} = 2.0$, $\epsilon = 0.2$.

**Ratio:** $r(\theta) = 0.6/0.3 = 2.0$.

**Clipped ratio:** $\text{clip}(2.0, 0.8, 1.2) = 1.2$.

**Objective terms:**
- Unclipped: $r \cdot \hat{A} = 2.0 \times 2.0 = 4.0$
- Clipped: $1.2 \times 2.0 = 2.4$

**PPO loss:** $\min(4.0, 2.4) = 2.4$.

The clipping prevents the policy from changing too much in one step (ratio capped at 1.2 since advantage is positive).

</details>

### Example 23.7.E5 — Discount Factor and Effective Horizon

<details>
<summary>🔍 Full Solution</summary>

**Problem:** An agent receives reward $r=1$ at every step. Compare total discounted return for $\gamma = 0.9$ vs $\gamma = 0.99$.

**For $\gamma = 0.9$:**

$$
G = \sum_{t=0}^\infty \gamma^t = \frac{1}{1-\gamma} = \frac{1}{0.1} = 10
$$

Effective horizon: $\approx 1/(1-\gamma) = 10$ steps. Rewards beyond step 10 contribute $\lt  0.35$ total.

**For $\gamma = 0.99$:**

$$
G = \frac{1}{1-0.99} = 100
$$

Effective horizon: $\approx 100$ steps. The agent plans much further ahead.

**Practical implication:** Higher $\gamma$ enables long-term planning but increases variance in return estimates (more future randomness accumulated). Lower $\gamma$ is more myopic but easier to learn.

</details>

### Example 23.7.E6 — Reward Model Score Comparison

<details>
<summary>🔍 Full Solution</summary>

**Problem:** Reward model outputs $R(x, y_w) = 2.3$ and $R(x, y_l) = 1.1$ for a preference pair. Compute the predicted preference probability and the loss.

**Bradley-Terry probability:**

$$
P(y_w \succ y_l) = \sigma(R(x,y_w) - R(x,y_l)) = \sigma(2.3 - 1.1) = \sigma(1.2)
$$

$$
= \frac{1}{1+e^{-1.2}} = \frac{1}{1+0.3012} = \frac{1}{1.3012} = 0.7685
$$

**Loss (negative log-likelihood):**

$$
\mathcal{L} = -\log(0.7685) = 0.2632
$$

**Interpretation:** The reward model assigns 76.85% probability to the human-preferred response being better. The loss is relatively low — the model is learning the preference correctly.

</details>

---

## 🖼️ Additional Visual — Q-Value Gridworld

![track-10__10.7-fig2](track-10__10.7-fig2.svg)

---

## ⚠️ Common Pitfalls

### Pitfall 1 — Reward Shaping Gone Wrong

Adding intermediate rewards to speed learning can create unintended optimal policies. If you reward the agent for getting closer to the goal, it might oscillate near the goal without reaching it (collecting proximity rewards forever). **Solution:** Use potential-based reward shaping: $F(s,s') = \gamma\Phi(s') - \Phi(s)$ which provably preserves the optimal policy.

### Pitfall 2 — Deadly Triad (Function Approximation + Bootstrapping + Off-Policy)

Combining neural network Q-functions with TD learning and off-policy data (experience replay) can diverge. DQN solves this with target networks (frozen copy updated periodically) and experience replay buffers.

### Pitfall 3 — KL Penalty Too Low in RLHF

If $\beta$ in the RLHF objective is too small, the policy can "hack" the reward model — finding adversarial outputs that score high on $R_\phi$ but are nonsensical. The KL penalty keeps the policy close to the SFT baseline.

### Pitfall 4 — Discount Factor Interpretation

$\gamma = 0.99$ means the agent effectively plans $\approx 1/(1-\gamma) = 100$ steps ahead. $\gamma = 0.9$ plans only $\approx 10$ steps. For long-horizon tasks, $\gamma$ must be close to 1, but this makes learning harder (high variance in returns).

---

## 📝 Additional Derivations

### 5.4 Advantage Function and Variance Reduction

The **advantage function** $A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$ measures how much better action $a$ is compared to the average. Using it in policy gradient:

$$
\nabla_\theta J = \mathbb{E}\left[\sum_t \nabla_\theta\log\pi_\theta(a_t|s_t)A^\pi(s_t, a_t)\right]
$$

This has lower variance than using raw returns $G_t$ because $\mathbb{E}_a[A^\pi(s,a)] = 0$ (the baseline is already subtracted).

**GAE (Generalized Advantage Estimation):**

$$
\hat{A}_t^{GAE(\gamma,\lambda)} = \sum_{l=0}^\infty (\gamma\lambda)^l \delta_{t+l}
$$

where $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ is the TD error. $\lambda = 0$ gives 1-step TD (low variance, high bias); $\lambda = 1$ gives Monte Carlo (high variance, no bias).

### 5.5 DQN: Deep Q-Network Architecture

**Key innovations (Mnih et al., 2015):**

1. **Experience Replay:** Store transitions $(s, a, r, s')$ in buffer $\mathcal{D}$. Sample mini-batches uniformly for training. Breaks temporal correlations.

2. **Target Network:** Maintain a frozen copy $Q_{\bar\theta}$ updated every $C$ steps:

$$
\mathcal{L}(\theta) = \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}}\left[(r + \gamma\max_{a'}Q_{\bar\theta}(s',a') - Q_\theta(s,a))^2\right]
$$

3. **Gradient:** $\nabla_\theta\mathcal{L} = -\mathbb{E}[\delta \cdot \nabla_\theta Q_\theta(s,a)]$ where $\delta$ is the TD error.

### 5.6 RLHF — Complete Pipeline Derivation

**Phase 1: SFT.** Fine-tune base LLM on demonstration data: $\max_\theta \mathbb{E}_{(x,y) \sim \mathcal{D}_{demo}}[\log\pi_\theta(y|x)]$.

**Phase 2: Reward Model.** Collect comparison data: for prompt $x$, generate $y_1, y_2$, human labels which is better. Train:

$$
\mathcal{L}_{RM}(\phi) = -\mathbb{E}\left[\log\sigma(R_\phi(x, y_w) - R_\phi(x, y_l))\right]
$$

**Phase 3: PPO.** Optimize:

$$
\max_\theta \mathbb{E}_{x \sim \mathcal{D}}\left[\mathbb{E}_{y \sim \pi_\theta(\cdot|x)}[R_\phi(x,y)] - \beta D_{KL}(\pi_\theta(\cdot|x) \| \pi_{ref}(\cdot|x))\right]
$$

The KL term prevents reward hacking. In practice, the KL is computed token-by-token:

$$
D_{KL} = \sum_t \log\frac{\pi_\theta(y_t|x, y_{<t})}{\pi_{ref}(y_t|x, y_{<t})}
$$

---

## 🔗 8. Cross-links & Further Reading

### Internal Cross-links
- Bellman equations as fixed-point problems: [3.4 - Systems of Linear ODEs](3.4---Systems-of-Linear-ODEs)
- Eigenvalues in MDP transition matrices: [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization)
- Policy gradient uses log-derivative trick: [23.1 - Statistical Learning & Optimization](23.1---Statistical-Learning-&-Optimization)
- Neural networks as function approximators: [23.2 - Deep Neural Networks - Backprop & Architecture](23.2---Deep-Neural-Networks---Backprop-&-Architecture)
- LLM alignment via RLHF: [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs)
- KL divergence in RLHF objective: [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion)

### External References
- **Sutton & Barto (2018)** — *Reinforcement Learning: An Introduction* (free PDF, [incompleteideas.net/book](http://incompleteideas.net/book/the-book-2nd.html))
- **Schulman et al. (2017)** — *Proximal Policy Optimization Algorithms* ([arXiv:1707.06347](https://arxiv.org/abs/1707.06347))
- **Ouyang et al. (2022)** — *Training language models to follow instructions with human feedback* (InstructGPT/RLHF, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155))
- **Stanford CS234** — Reinforcement Learning ([cs234.stanford.edu](https://cs234.stanford.edu/))
- **David Silver's RL Course** — UCL/DeepMind ([youtube](https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ))




---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Policy Gradient Theorem Derivation

**Problem:** Derive the policy gradient theorem from first principles: $\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi_\theta}(s, a)\right]$, showing every step of the derivation including the log-derivative trick.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Define the Objective

The expected return under policy $\pi_\theta$:

$$
J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^{T} \gamma^t r_t\right] = \sum_s d^{\pi}(s) \sum_a \pi_\theta(a|s) Q^{\pi}(s,a)
$$

where $d^{\pi}(s) = \sum_{t=0}^{\infty} \gamma^t P(s_t = s | \pi)$ is the discounted state visitation distribution.

#### Step 2: Gradient of the Objective

$$
\nabla_\theta J(\theta) = \nabla_\theta \sum_s d^{\pi}(s) \sum_a \pi_\theta(a|s) Q^{\pi}(s,a)
$$

The key difficulty: $d^{\pi}(s)$ also depends on $\theta$ (changing the policy changes which states are visited). The policy gradient theorem shows we can ignore this dependency:

$$
\nabla_\theta J(\theta) = \sum_s d^{\pi}(s) \sum_a \nabla_\theta \pi_\theta(a|s) Q^{\pi}(s,a)
$$

(The proof that $\nabla_\theta d^{\pi}$ terms cancel is non-trivial; see Sutton et al., 1999.)

#### Step 3: The Log-Derivative Trick (REINFORCE Trick)

For any function $f(\theta)$:

$$
\nabla_\theta f(\theta) = f(\theta) \cdot \nabla_\theta \log f(\theta)
$$

This follows from the chain rule: $\nabla_\theta \log f = \frac{\nabla_\theta f}{f} \implies \nabla_\theta f = f \cdot \nabla_\theta \log f$.

Applying to $\pi_\theta(a|s)$:

$$
\nabla_\theta \pi_\theta(a|s) = \pi_\theta(a|s) \cdot \nabla_\theta \log \pi_\theta(a|s)
$$

#### Step 4: Substitute Back

$$
\nabla_\theta J(\theta) = \sum_s d^{\pi}(s) \sum_a \pi_\theta(a|s) \nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi}(s,a)
$$

$$
= \mathbb{E}_{s \sim d^{\pi}, \; a \sim \pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi}(s,a)\right]
$$

#### Step 5: Trajectory Form (REINFORCE)

For episodic tasks, this can be written over full trajectories:

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot G_t\right]
$$

where $G_t = \sum_{k=t}^{T} \gamma^{k-t} r_k$ is the return-to-go from time $t$.

#### Step 6: Why This is Remarkable

The gradient $\nabla_\theta J$ can be estimated from samples without knowing the environment dynamics (model-free). We only need:
1. Sample trajectories by running $\pi_\theta$
2. Compute returns $G_t$
3. Compute $\nabla_\theta \log \pi_\theta(a_t|s_t)$ (the "score function")

No differentiation through the environment is required.

**Final Answer:**

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi_\theta}(s,a)\right]
$$

</details>

### Example 9.2 — REINFORCE with Baseline: Variance Reduction Proof

**Problem:** Prove that subtracting a state-dependent baseline $b(s)$ from the return does not bias the policy gradient estimator but reduces its variance. Derive the optimal baseline.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Baseline-Subtracted Estimator

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot (Q^{\pi}(s,a) - b(s))\right]
$$

We need to show: $\mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot b(s)\right] = 0$.

#### Step 2: Proof of Unbiasedness

$$
\mathbb{E}_{a \sim \pi_\theta(\cdot|s)}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot b(s)\right] = b(s) \sum_a \nabla_\theta \pi_\theta(a|s)
$$

$$
= b(s) \cdot \nabla_\theta \sum_a \pi_\theta(a|s) = b(s) \cdot \nabla_\theta 1 = 0
$$

The key step: $\sum_a \pi_\theta(a|s) = 1$ for all $\theta$ (probabilities sum to 1), so its gradient is zero. Since $b(s)$ does not depend on $a$, it factors out of the expectation over actions.

Therefore the baseline introduces zero bias regardless of the choice of $b(s)$.

#### Step 3: Variance Analysis

The variance of the estimator $\hat{g} = \nabla_\theta \log \pi_\theta(a|s)(Q(s,a) - b(s))$ is:

$$
\text{Var}(\hat{g}) = \mathbb{E}[\hat{g}^2] - (\mathbb{E}[\hat{g}])^2
$$

Since $\mathbb{E}[\hat{g}]$ is fixed (unbiased), minimizing variance means minimizing $\mathbb{E}[\hat{g}^2]$.

For scalar case (single parameter):

$$
\mathbb{E}[\hat{g}^2] = \mathbb{E}\left[(\nabla_\theta \log \pi)^2 (Q - b)^2\right]
$$

#### Step 4: Optimal Baseline

Taking derivative w.r.t. $b$ and setting to zero:

$$
\frac{\partial}{\partial b} \mathbb{E}\left[(\nabla_\theta \log \pi)^2 (Q - b)^2\right] = -2\mathbb{E}\left[(\nabla_\theta \log \pi)^2 (Q - b)\right] = 0
$$

$$
b^* = \frac{\mathbb{E}\left[(\nabla_\theta \log \pi)^2 Q\right]}{\mathbb{E}\left[(\nabla_\theta \log \pi)^2\right]}
$$

This is a weighted average of $Q$ values, weighted by the squared score function magnitude.

#### Step 5: Practical Approximation

In practice, $b(s) \approx V^{\pi}(s)$ (the value function) is used. This is close to optimal and has the intuitive interpretation:

$$
Q^{\pi}(s,a) - V^{\pi}(s) = A^{\pi}(s,a) \quad \text{(the advantage function)}
$$

The advantage measures how much better action $a$ is compared to the average action under $\pi$. Actions better than average get positive gradient; worse actions get negative gradient.

#### Step 6: Variance Reduction Magnitude

Without baseline: $\text{Var} \propto \mathbb{E}[G_t^2]$ (returns can be large, e.g., 100s)

With baseline: $\text{Var} \propto \mathbb{E}[A_t^2]$ (advantages are centered around 0)

Typical reduction: 10–100× lower variance, enabling practical training with fewer samples.

**Final Answer:** The baseline $b(s)$ is unbiased because $\sum_a \nabla_\theta \pi_\theta(a|s) = \nabla_\theta 1 = 0$, and the optimal baseline is:

$$
b^*(s) = \frac{\mathbb{E}_a\left[\|\nabla_\theta \log\pi\|^2 Q(s,a)\right]}{\mathbb{E}_a\left[\|\nabla_\theta \log\pi\|^2\right]} \approx V^{\pi}(s)
$$

</details>


### Example 9.3 — PPO Clipped Surrogate Objective Derivation

**Problem:** Derive the PPO clipped objective from the trust-region policy optimization (TRPO) framework, showing why clipping the probability ratio prevents destructively large policy updates.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Importance Sampling Ratio

When updating policy $\pi_\theta$ using data collected under old policy $\pi_{\theta_{\text{old}}}$:

$$
r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}
$$

The surrogate objective (from TRPO):

$$
L^{CPI}(\theta) = \mathbb{E}_t\left[r_t(\theta) \hat{A}_t\right]
$$

where $\hat{A}_t$ is the estimated advantage.

#### Step 2: The Problem with Unconstrained Optimization

If $\hat{A}_t \gt  0$ (good action), maximizing $L^{CPI}$ pushes $r_t \to \infty$ — the new policy assigns arbitrarily high probability to this action. This can be catastrophic because:
1. The advantage estimate $\hat{A}_t$ is noisy
2. Large policy changes invalidate the importance sampling approximation
3. Performance can collapse irreversibly

#### Step 3: TRPO's Solution — KL Constraint

TRPO constrains the update:

$$
\max_\theta \; \mathbb{E}_t[r_t(\theta)\hat{A}_t] \quad \text{s.t.} \quad \mathbb{E}_t[D_{KL}(\pi_{\theta_{\text{old}}}(\cdot|s_t) \| \pi_\theta(\cdot|s_t))] \leq \delta
$$

This requires computing second-order derivatives (Fisher information matrix) — expensive.

#### Step 4: PPO's Solution — Clipping

PPO replaces the KL constraint with a simpler clipping mechanism:

$$
L^{CLIP}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]
$$

with $\epsilon = 0.2$ typically.

#### Step 5: Case Analysis

**Case 1: $\hat{A}_t \gt  0$ (action was good)**

We want to increase $\pi_\theta(a_t|s_t)$, so $r_t$ increases. But:

$$
\min(r_t \hat{A}_t, \; (1+\epsilon)\hat{A}_t) = \begin{cases} r_t \hat{A}_t & \text{if } r_t \leq 1+\epsilon \\ (1+\epsilon)\hat{A}_t & \text{if } r_t \gt  1+\epsilon \end{cases}
$$

Once $r_t \gt  1.2$, the objective is flat — no gradient to push $r_t$ higher. The policy change is bounded.

**Case 2: $\hat{A}_t \lt  0$ (action was bad)**

We want to decrease $\pi_\theta(a_t|s_t)$, so $r_t$ decreases. But:

$$
\min(r_t \hat{A}_t, \; (1-\epsilon)\hat{A}_t) = \begin{cases} r_t \hat{A}_t & \text{if } r_t \geq 1-\epsilon \\ (1-\epsilon)\hat{A}_t & \text{if } r_t \lt  1-\epsilon \end{cases}
$$

(Note: with $\hat{A}_t \lt  0$, the min selects the more negative value, which is the less aggressive update.)

Once $r_t \lt  0.8$, the objective is flat — the policy won't be pushed further away.

#### Step 6: The Full PPO Objective

In practice, PPO also includes a value function loss and entropy bonus:

$$
L(\theta) = \mathbb{E}_t\left[L^{CLIP}(\theta) - c_1 L^{VF}(\theta) + c_2 S[\pi_\theta](s_t)\right]
$$

where $L^{VF} = (V_\theta(s_t) - V_t^{\text{target}})^2$ and $S$ is the entropy bonus encouraging exploration.

**Final Answer:**

$$
L^{CLIP} = \mathbb{E}_t\left[\min\left(\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}\hat{A}_t, \; \text{clip}\left(\frac{\pi_\theta}{\pi_{\theta_{\text{old}}}}, 1\pm\epsilon\right)\hat{A}_t\right)\right]
$$

</details>

### Example 9.4 — Bradley-Terry Preference Model for RLHF Reward Learning

**Problem:** Derive the reward model training loss used in RLHF from the Bradley-Terry model of pairwise preferences. Show how human preference labels $(y_w \succ y_l | x)$ are converted into a scalar reward function.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Bradley-Terry Model

Given two responses $y_1, y_2$ to prompt $x$, the probability that a human prefers $y_1$ over $y_2$ is modeled as:

$$
P(y_1 \succ y_2 | x) = \frac{\exp(r(x, y_1))}{\exp(r(x, y_1)) + \exp(r(x, y_2))} = \sigma(r(x, y_1) - r(x, y_2))
$$

where $r(x, y)$ is the scalar reward and $\sigma$ is the sigmoid function.

#### Step 2: Intuition

The Bradley-Terry model assumes preferences are determined by a latent "quality" score, with noise following a logistic distribution. The probability of preferring $y_w$ (winner) over $y_l$ (loser) depends only on the difference in rewards — a natural assumption for ordinal comparisons.

#### Step 3: Maximum Likelihood Training

Given a dataset of human preferences $\mathcal{D} = \{(x^{(i)}, y_w^{(i)}, y_l^{(i)})\}_{i=1}^N$:

$$
\mathcal{L}_{\text{reward}} = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}}\left[\log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))\right]
$$

This is binary cross-entropy where the "label" is always 1 (the winner is always preferred):

$$
= -\frac{1}{N}\sum_{i=1}^{N} \log \sigma(r_\phi(x^{(i)}, y_w^{(i)}) - r_\phi(x^{(i)}, y_l^{(i)}))
$$

#### Step 4: Gradient of the Reward Model Loss

$$
\frac{\partial \mathcal{L}}{\partial \phi} = -\mathbb{E}\left[(1 - \sigma(\Delta r)) \cdot \left(\frac{\partial r_\phi(x, y_w)}{\partial \phi} - \frac{\partial r_\phi(x, y_l)}{\partial \phi}\right)\right]
$$

where $\Delta r = r_\phi(x, y_w) - r_\phi(x, y_l)$.

When $\Delta r$ is large (model already correctly ranks the pair), $(1 - \sigma(\Delta r)) \approx 0$ — small gradient. When $\Delta r$ is small or negative (model is wrong), the gradient is large — focusing learning on hard examples.

#### Step 5: From Reward Model to RLHF Objective

Once $r_\phi$ is trained, the LLM policy $\pi_\theta$ is optimized:

$$
\max_\theta \; \mathbb{E}_{x \sim \mathcal{D}, \; y \sim \pi_\theta(\cdot|x)}\left[r_\phi(x, y)\right] - \beta \cdot D_{KL}(\pi_\theta \| \pi_{\text{ref}})
$$

The KL penalty prevents the policy from deviating too far from the reference (SFT) model, which would exploit reward model errors.

#### Step 6: Numerical Example

Suppose for prompt "Explain gravity":
- $y_w$ = "Gravity is the force..." (good response), $r_\phi(x, y_w) = 2.3$
- $y_l$ = "Gravity is when things fall" (mediocre), $r_\phi(x, y_l) = 1.1$

$$
P(y_w \succ y_l) = \sigma(2.3 - 1.1) = \sigma(1.2) = 0.769
$$

Loss contribution: $-\log(0.769) = 0.263$

If the model incorrectly assigns $r(y_w) = 0.5$, $r(y_l) = 1.8$:

$$
P(y_w \succ y_l) = \sigma(0.5 - 1.8) = \sigma(-1.3) = 0.214
$$

Loss: $-\log(0.214) = 1.54$ — much higher, driving the model to correct its ranking.

**Final Answer:**

$$
\mathcal{L}_{\text{reward}} = -\mathbb{E}\left[\log\sigma(r_\phi(x, y_w) - r_\phi(x, y_l))\right]
$$

</details>



---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 23.1 Generalized Advantage Estimation (GAE) Derivation

**Motivation:** The advantage $A_t = Q(s_t, a_t) - V(s_t)$ can be estimated with different bias-variance tradeoffs:
- **1-step TD:** $\hat{A}_t^{(1)} = r_t + \gamma V(s_{t+1}) - V(s_t)$ — low variance, high bias
- **Monte Carlo:** $\hat{A}_t^{(\infty)} = \sum_{k=0}^{T-t} \gamma^k r_{t+k} - V(s_t)$ — high variance, low bias

GAE (Schulman et al., 2016) provides a smooth interpolation.

**Definition of TD residual:**

$$
\delta_t^V = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

**$n$-step advantage:**

$$
\hat{A}_t^{(n)} = \sum_{k=0}^{n-1} \gamma^k \delta_{t+k}^V = -V(s_t) + r_t + \gamma r_{t+1} + \ldots + \gamma^{n-1} r_{t+n-1} + \gamma^n V(s_{t+n})
$$

**GAE as exponentially-weighted average:**

$$
\hat{A}_t^{\text{GAE}(\gamma, \lambda)} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}^V
$$

$$
= \delta_t^V + (\gamma\lambda)\delta_{t+1}^V + (\gamma\lambda)^2 \delta_{t+2}^V + \ldots
$$

**Proof that this interpolates between TD and MC:**

- $\lambda = 0$: $\hat{A}_t^{\text{GAE}} = \delta_t^V = r_t + \gamma V(s_{t+1}) - V(s_t)$ (1-step TD, low variance)
- $\lambda = 1$: $\hat{A}_t^{\text{GAE}} = \sum_{l=0}^{\infty} \gamma^l \delta_{t+l}^V = \sum_{l=0}^{\infty} \gamma^l r_{t+l} - V(s_t)$ (Monte Carlo, zero bias if $V$ is ignored)

**Practical computation (backward recursion):**

$$
\hat{A}_T = \delta_T, \quad \hat{A}_t = \delta_t + \gamma\lambda \hat{A}_{t+1}
$$

This is $O(T)$ and can be computed in a single backward pass over the trajectory.

**Typical value:** $\lambda = 0.95$ provides a good bias-variance tradeoff for most continuous control tasks.

### 23.2 KL-Divergence Regularization in RLHF

The RLHF objective with KL penalty:

$$
\max_\theta \; \mathbb{E}_{x \sim \mathcal{D}}\left[\mathbb{E}_{y \sim \pi_\theta(\cdot|x)}[r_\phi(x, y)] - \beta D_{KL}(\pi_\theta(\cdot|x) \| \pi_{\text{ref}}(\cdot|x))\right]
$$

**Why KL regularization is essential:**

1. **Reward hacking:** Without KL penalty, the policy finds adversarial outputs that score high on $r_\phi$ but are nonsensical (exploiting reward model errors).

2. **Distribution shift:** The reward model was trained on outputs from $\pi_{\text{ref}}$. As $\pi_\theta$ diverges, $r_\phi$ becomes unreliable (out-of-distribution).

**Closed-form optimal policy:** The KL-regularized objective has an analytical solution:

$$
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{r_\phi(x,y)}{\beta}\right)
$$

where $Z(x) = \sum_y \pi_{\text{ref}}(y|x)\exp(r_\phi(x,y)/\beta)$ is the partition function.

**Proof:** The objective is:

$$
\max_\pi \sum_y \pi(y|x) r(x,y) - \beta \sum_y \pi(y|x) \log\frac{\pi(y|x)}{\pi_{\text{ref}}(y|x)}
$$

Taking the functional derivative w.r.t. $\pi(y|x)$ with Lagrange multiplier for the normalization constraint:

$$
r(x,y) - \beta\log\frac{\pi(y|x)}{\pi_{\text{ref}}(y|x)} - \beta - \lambda = 0
$$

$$
\log\frac{\pi(y|x)}{\pi_{\text{ref}}(y|x)} = \frac{r(x,y)}{\beta} - 1 - \frac{\lambda}{\beta}
$$

$$
\pi^*(y|x) \propto \pi_{\text{ref}}(y|x) \exp\left(\frac{r(x,y)}{\beta}\right)
$$

**$\beta$ selection:** Too small → reward hacking; too large → no learning. Typical: $\beta = 0.01$–$0.1$. Some implementations use adaptive $\beta$ targeting a specific KL budget.

### 23.3 Direct Preference Optimization (DPO) vs PPO

**DPO (Rafailov et al., 2023)** eliminates the need for a separate reward model and RL training loop by directly optimizing the policy from preference data.

**Key insight:** The closed-form optimal policy under KL-regularized RLHF implies:

$$
r(x, y) = \beta \log \frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)
$$

Substituting into the Bradley-Terry preference model:

$$
P(y_w \succ y_l | x) = \sigma(r(x,y_w) - r(x,y_l))
$$

$$
= \sigma\left(\beta \log\frac{\pi^*(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi^*(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)
$$

The $Z(x)$ terms cancel! The DPO loss directly optimizes $\pi_\theta$ to satisfy preferences:

$$
\mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E}_{(x,y_w,y_l)}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]
$$

**Advantages of DPO over PPO-based RLHF:**
- No reward model training (fewer parameters, less compute)
- No RL training loop (no value function, no GAE, no clipping)
- Stable optimization (standard cross-entropy-like loss)
- Mathematically equivalent to RLHF under Bradley-Terry assumptions

**Disadvantages:**
- Cannot iteratively improve (offline only — uses fixed preference dataset)
- Assumes Bradley-Terry model is correct (may not capture complex human preferences)
- No exploration — cannot discover novel high-reward behaviors
- PPO with online data collection can continue improving beyond the preference dataset

**Practical comparison:** DPO achieves comparable performance to PPO-RLHF on standard benchmarks (MT-Bench, AlpacaEval) with ~3× less compute, but PPO-RLHF with iterative data collection (online RLHF) can achieve higher final performance given sufficient compute budget.

---

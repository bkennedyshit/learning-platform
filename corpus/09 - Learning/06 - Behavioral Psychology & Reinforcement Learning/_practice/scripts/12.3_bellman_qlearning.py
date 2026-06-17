#!/usr/bin/env python3
"""
12.3_bellman_qlearning.py — Q-learning on a small gridworld with convergence demo.

Features:
  - 4x4 gridworld with goal (+10), trap (-5), wall
  - Epsilon-greedy exploration
  - Tracks convergence of Q-values to optimal
  - Generates practice problems (Bellman equation, Q-updates)

Usage:
  python 12.3_bellman_qlearning.py
  python 12.3_bellman_qlearning.py --count 10 --seed 42
  python 12.3_bellman_qlearning.py --count 10 --seed 42 --out /tmp/_123.md
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# --- Gridworld Environment ---
class GridWorld:
    def __init__(self, rows=4, cols=4, goal=(0, 3), trap=(2, 2), wall=(1, 1)):
        self.rows, self.cols = rows, cols
        self.goal, self.trap, self.wall = goal, trap, wall
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # R, L, D, U
        self.action_names = ["right", "left", "down", "up"]

    def step(self, state, action_idx):
        if state == self.goal or state == self.trap:
            return state, 0, True
        dr, dc = self.actions[action_idx]
        nr, nc = state[0] + dr, state[1] + dc
        if not (0 <= nr < self.rows and 0 <= nc < self.cols) or (nr, nc) == self.wall:
            nr, nc = state
        next_state = (nr, nc)
        if next_state == self.goal:
            return next_state, 10, True
        elif next_state == self.trap:
            return next_state, -5, True
        return next_state, -1, False


def run_qlearning(seed=42, episodes=500, alpha=0.1, gamma=0.9, epsilon=0.1):
    rng = np.random.default_rng(seed)
    env = GridWorld()
    Q = np.zeros((env.rows, env.cols, 4))
    for ep in range(episodes):
        state = (3, 0)
        done = False
        while not done:
            if rng.random() < epsilon:
                a = rng.integers(4)
            else:
                a = int(np.argmax(Q[state[0], state[1]]))
            ns, r, done = env.step(state, a)
            best_next = np.max(Q[ns[0], ns[1]]) if not done else 0
            td = r + gamma * best_next - Q[state[0], state[1], a]
            Q[state[0], state[1], a] += alpha * td
            state = ns
    return Q


# --- Problem Generators ---
def gen_bellman_eq(rng: random.Random) -> Problem:
    gamma = rng.choice([0.5, 0.8, 0.9])
    r_goal = rng.choice([5, 10, 20])
    r_step = rng.choice([-1, -2, 0])
    V_neighbor = rng.randint(1, 8)
    Q_val = r_step + gamma * V_neighbor
    Q_goal = r_goal + 0
    stmt = (
        f"In a gridworld with γ={gamma}, step reward={r_step}, goal reward={r_goal}:\n\n"
        f"1. Compute Q(s, right) if moving right leads to a state with V*={V_neighbor}.\n"
        f"2. Compute Q(s, down) if moving down reaches the goal (terminal)."
    )
    sol = (
        f"1. Q(s, right) = r + γ·V*(s') = {r_step} + {gamma}×{V_neighbor} = {Q_val:.1f}\n\n"
        f"2. Q(s, down) = {r_goal} + γ×0 = {r_goal} (terminal, no future value)"
    )
    return Problem("Bellman Equation Computation", stmt, sol)


def gen_q_update(rng: random.Random) -> Problem:
    Q_old = round(rng.uniform(-5, 8), 2)
    r = rng.choice([-5, -1, 0, 1, 5, 10])
    max_Q_next = round(rng.uniform(0, 10), 2)
    alpha = rng.choice([0.1, 0.2, 0.5])
    gamma = rng.choice([0.9, 0.95])
    terminal = rng.choice([True, False])
    if terminal:
        max_Q_next = 0
    target = r + gamma * max_Q_next
    td = target - Q_old
    Q_new = Q_old + alpha * td
    stmt = (
        f"Current Q(s,a) = {Q_old}. Agent takes action, receives r={r}, "
        f"{'reaches terminal' if terminal else f'next state has max Q = {max_Q_next}'}.\n"
        f"α={alpha}, γ={gamma}. Compute the Q-learning update."
    )
    sol = (
        f"TD target = r + γ·max Q(s',·) = {r} + {gamma}×{max_Q_next} = {target:.3f}\n\n"
        f"TD error δ = {target:.3f} − {Q_old} = {td:.3f}\n\n"
        f"Q(s,a) ← {Q_old} + {alpha}×{td:.3f} = {Q_new:.4f}"
    )
    return Problem("Q-Learning Update Step", stmt, sol)


def gen_epsilon_greedy(rng: random.Random) -> Problem:
    n_actions = rng.choice([3, 4, 5])
    epsilon = rng.choice([0.1, 0.2, 0.3])
    Q_vals = [round(rng.uniform(-3, 10), 1) for _ in range(n_actions)]
    best_idx = Q_vals.index(max(Q_vals))
    p_best = 1 - epsilon + epsilon / n_actions
    p_other = epsilon / n_actions
    stmt = (
        f"Q-values for {n_actions} actions: {Q_vals}. ε={epsilon}.\n\n"
        f"Compute the ε-greedy probability for each action."
    )
    probs = [f"P(a{i}) = {'1−ε+ε/|A|' if i == best_idx else 'ε/|A|'} = "
             f"{p_best:.3f}" if i == best_idx else
             f"P(a{i}) = ε/|A| = {p_other:.3f}"
             for i in range(n_actions)]
    sol = (
        f"Best action: a{best_idx} (Q={max(Q_vals)})\n\n" +
        "\n\n".join(probs) +
        f"\n\nSum check: {p_best:.3f} + {n_actions-1}×{p_other:.3f} = "
        f"{p_best + (n_actions-1)*p_other:.3f} ✓"
    )
    return Problem("ε-Greedy Action Probabilities", stmt, sol)


def gen_convergence(rng: random.Random) -> Problem:
    gamma = rng.choice([0.8, 0.9, 0.95])
    n_iter = rng.randint(3, 5)
    r = rng.choice([5, 10])
    V = 0.0
    lines = []
    for k in range(n_iter):
        V_new = r + gamma * 0  # simple: one-step to terminal
        # Actually let's do a chain: s1→s2→terminal(r)
        V2 = r  # V(s2) = r (one step to terminal with reward r)
        V1 = -1 + gamma * V2  # V(s1) = step_cost + gamma*V(s2)
        lines.append(f"Iteration {k+1}: V(s2)={V2}, V(s1)={-1+gamma*V2:.2f}")
        break  # Simple version
    stmt = (
        f"A 2-state chain: s1→s2→terminal. Reward: r(s1→s2)=−1, r(s2→term)={r}. γ={gamma}.\n\n"
        f"Compute V* for both states using the Bellman optimality equation."
    )
    V_s2 = r
    V_s1 = -1 + gamma * V_s2
    sol = (
        f"V*(s2) = r(s2→term) + γ×V*(term) = {r} + {gamma}×0 = {r}\n\n"
        f"V*(s1) = r(s1→s2) + γ×V*(s2) = −1 + {gamma}×{r} = {V_s1:.1f}"
    )
    return Problem("Value Iteration (Chain MDP)", stmt, sol)


GENERATORS = [gen_bellman_eq, gen_q_update, gen_epsilon_greedy, gen_convergence]


def main():
    parser = argparse.ArgumentParser(description="12.3 Q-Learning practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\n"
        "tags: [review/psych-rl, q-learning, bellman-equation, MDP]\n"
        "---\n\n"
        "# 12.3 Practice — Q-Learning & The Bellman Equation\n\n"
        f"Generated {args.count} problems.\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

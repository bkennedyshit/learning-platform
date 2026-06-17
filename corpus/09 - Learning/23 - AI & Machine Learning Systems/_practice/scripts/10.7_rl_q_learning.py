#!/usr/bin/env python3
"""
10.7_rl_q_learning.py — Practice problems for Reinforcement Learning.

Archetypes:
  1. Bellman equation evaluation (compute V or Q for given MDP)
  2. Q-learning update step
  3. Value iteration on small gridworld
  4. Policy gradient score function
  5. Epsilon-greedy action selection probability

Usage:
  python 10.7_rl_q_learning.py --count 10 --seed 42
  python 10.7_rl_q_learning.py --demo
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
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )


def gen_bellman(rng: random.Random) -> Problem:
    gamma = rng.choice([0.9, 0.95, 0.99])
    r = round(rng.uniform(-1, 5), 1)
    v_next = round(rng.uniform(0, 10), 1)
    q = r + gamma * v_next
    stmt = (
        f"Compute $Q(s, a)$ given: reward $r={r}$, next state value $V(s')={v_next}$, "
        f"$\\gamma={gamma}$ (deterministic transition)."
    )
    sol = f"$Q(s,a) = r + \\gamma V(s') = {r} + {gamma} \\times {v_next} = {q:.3f}$"
    return Problem("Bellman equation", stmt, sol)


def gen_q_update(rng: random.Random) -> Problem:
    q_old = round(rng.uniform(-1, 5), 2)
    r = round(rng.uniform(-1, 3), 1)
    q_max_next = round(rng.uniform(0, 5), 2)
    alpha = rng.choice([0.01, 0.05, 0.1, 0.2])
    gamma = rng.choice([0.9, 0.95, 0.99])
    td_target = r + gamma * q_max_next
    td_error = td_target - q_old
    q_new = q_old + alpha * td_error
    stmt = (
        f"Q-learning update: $Q(s,a)={q_old}$, $r={r}$, "
        f"$\\max_{{a'}}Q(s',a')={q_max_next}$, $\\alpha={alpha}$, $\\gamma={gamma}$."
    )
    sol = (
        f"TD target: $r + \\gamma\\max Q = {r} + {gamma}\\times{q_max_next} = {td_target:.4f}$\n\n"
        f"TD error: ${td_target:.4f} - {q_old} = {td_error:.4f}$\n\n"
        f"$Q_{{new}} = {q_old} + {alpha}\\times{td_error:.4f} = {q_new:.4f}$"
    )
    return Problem("Q-learning update", stmt, sol)


def gen_value_iteration(rng: random.Random) -> Problem:
    gamma = 0.9
    # Simple 2-state MDP
    r1a = rng.randint(0, 5)
    r1b = rng.randint(0, 5)
    # s1->a->s2 (r1a), s1->b->s1 (r1b), s2 terminal (r=0)
    v0 = [0, 0]
    v1_s1 = max(r1a + gamma*0, r1b + gamma*0)
    v1 = [v1_s1, 0]
    v2_s1 = max(r1a + gamma*0, r1b + gamma*v1_s1)
    stmt = (
        f"2-state MDP: $s_1 \\xrightarrow{{a}} s_2$ (r={r1a}), $s_1 \\xrightarrow{{b}} s_1$ (r={r1b}), "
        f"$s_2$ terminal. $\\gamma={gamma}$. Run 2 iterations of value iteration."
    )
    sol = (
        f"**Iter 1:** $V(s_1) = \\max({r1a}+0, {r1b}+0) = {v1_s1}$\n\n"
        f"**Iter 2:** $V(s_1) = \\max({r1a}+0, {r1b}+{gamma}\\times{v1_s1}) = "
        f"\\max({r1a}, {r1b+gamma*v1_s1:.1f}) = {v2_s1:.1f}$"
    )
    return Problem("Value iteration", stmt, sol)


def gen_epsilon_greedy(rng: random.Random) -> Problem:
    epsilon = rng.choice([0.05, 0.1, 0.2])
    n_actions = rng.choice([4, 6])
    best_action = rng.randint(0, n_actions-1)
    p_best = (1 - epsilon) + epsilon/n_actions
    p_other = epsilon/n_actions
    stmt = (
        f"$\\epsilon$-greedy with $\\epsilon={epsilon}$, {n_actions} actions. "
        f"Best action is $a_{{{best_action}}}$. What is $P(a_{{{best_action}}})$ and $P(a_{{other}})$?"
    )
    sol = (
        f"$P(a_{{{best_action}}}) = 1-\\epsilon + \\epsilon/{n_actions} = {1-epsilon} + {epsilon/n_actions:.4f} = {p_best:.4f}$\n\n"
        f"$P(a_{{other}}) = \\epsilon/{n_actions} = {epsilon}/{n_actions} = {p_other:.4f}$\n\n"
        f"Check: ${p_best:.4f} + {n_actions-1}\\times{p_other:.4f} = {p_best+(n_actions-1)*p_other:.4f}$ ✓"
    )
    return Problem("Epsilon-greedy probability", stmt, sol)


def run_demo():
    print("=" * 60)
    print("DEMO: Q-Learning on 4×4 Gridworld")
    print("=" * 60)

    # 4x4 grid, goal at (3,3), -0.01 step penalty, +1 at goal
    size = 4
    goal = (3, 3)
    actions = [(-1,0), (0,1), (1,0), (0,-1)]  # up, right, down, left
    action_names = ['↑', '→', '↓', '←']

    Q = np.zeros((size*size, 4))
    alpha, gamma, epsilon = 0.1, 0.99, 0.1
    episodes = 10000

    for ep in range(episodes):
        s = (0, 0)
        for _ in range(100):  # max steps
            si = s[0]*size + s[1]
            if np.random.random() < epsilon:
                a = np.random.randint(4)
            else:
                a = np.argmax(Q[si])

            dr, dc = actions[a]
            ns = (max(0, min(3, s[0]+dr)), max(0, min(3, s[1]+dc)))
            nsi = ns[0]*size + ns[1]

            r = 1.0 if ns == goal else -0.01
            done = ns == goal

            Q[si, a] += alpha * (r + gamma * np.max(Q[nsi]) * (1-done) - Q[si, a])
            s = ns
            if done:
                break

    print("\nOptimal Value Function V*(s) = max_a Q(s,a):")
    V = Q.max(axis=1).reshape(size, size)
    print(np.round(V, 2))

    print("\nOptimal Policy:")
    policy = Q.argmax(axis=1).reshape(size, size)
    for r in range(size):
        row = ""
        for c in range(size):
            if (r, c) == goal:
                row += " G "
            else:
                row += f" {action_names[policy[r,c]]} "
        print(row)


GENERATORS = [gen_bellman, gen_q_update, gen_value_iteration, gen_epsilon_greedy]


def main():
    parser = argparse.ArgumentParser(description="10.7 RL practice")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    lines = ["---", "tags: [review/ai, reinforcement-learning, q-learning, rlhf]",
             "generated: true", "---", "", "# 10.7 Reinforcement Learning — Practice Problems", ""]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()

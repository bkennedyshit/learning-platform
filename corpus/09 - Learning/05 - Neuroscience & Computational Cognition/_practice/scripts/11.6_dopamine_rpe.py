#!/usr/bin/env python3
"""
11.6_dopamine_rpe.py — TD-learning simulator showing dopamine-as-RPE firing.

Modes:
  --demo : Run TD learning on a simple Markov chain, plot RPE evolution
  default: Generate TD-error drill problems

Usage:
  python 11.6_dopamine_rpe.py --demo
  python 11.6_dopamine_rpe.py --count 10 --seed 42
"""
from __future__ import annotations

import argparse
import random
import sys
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


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo")
        sys.exit(1)

    # Simple 5-state chain: s0 -> s1 -> s2 -> s3 -> s4(terminal, reward=1)
    n_states = 5
    gamma = 0.9
    alpha = 0.1
    n_episodes = 200

    V = np.zeros(n_states)
    V_history = [V.copy()]
    delta_history = []

    for ep in range(n_episodes):
        deltas = []
        for s in range(n_states - 1):
            r = 1.0 if s == n_states - 2 else 0.0
            s_next = s + 1
            V_next = 0.0 if s_next == n_states - 1 else V[s_next]
            delta = r + gamma * V_next - V[s]
            V[s] += alpha * delta
            deltas.append(delta)
        V_history.append(V.copy())
        delta_history.append(deltas)

    V_history = np.array(V_history)
    delta_history = np.array(delta_history)

    fig, axes = plt.subplots(3, 1, figsize=(10, 8))

    # Value function evolution
    for s in range(n_states - 1):
        axes[0].plot(V_history[:, s], label=f"V(s{s})")
    axes[0].set_ylabel("Value V(s)")
    axes[0].set_title("TD Learning: Value Function Convergence")
    axes[0].legend()
    axes[0].axhline(0.9**3, color='gray', linestyle='--', alpha=0.5)

    # RPE (dopamine) at each state over episodes
    for s in range(n_states - 1):
        axes[1].plot(delta_history[:, s], label=f"δ at s{s}", alpha=0.7)
    axes[1].set_ylabel("TD Error (δ)")
    axes[1].set_title("Reward Prediction Error (Dopamine Signal)")
    axes[1].axhline(0, color='gray', linestyle='--')
    axes[1].legend()

    # Final episode RPE pattern (like Schultz's monkey data)
    axes[2].bar(range(n_states - 1), delta_history[-1], color='steelblue', alpha=0.7)
    axes[2].set_xlabel("State")
    axes[2].set_ylabel("δ (final episode)")
    axes[2].set_title("Final Episode: RPE Transferred to Earliest Predictor")
    axes[2].axhline(0, color='gray', linestyle='--')
    axes[2].set_xticks(range(n_states - 1))
    axes[2].set_xticklabels([f"s{i} ({'cue' if i==0 else 'reward' if i==3 else ''})" for i in range(n_states-1)])

    plt.tight_layout()
    plt.savefig("dopamine_rpe_demo.png", dpi=150)
    print("Saved: dopamine_rpe_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_td_error(rng: random.Random) -> Problem:
    n_states = rng.randint(3, 5)
    gamma = round(rng.choice([0.8, 0.9, 0.95]), 2)
    alpha = round(rng.choice([0.05, 0.1, 0.2]), 2)
    V = [round(rng.uniform(0, 1), 2) for _ in range(n_states)]
    V[-1] = 0  # terminal
    rewards = [0] * (n_states - 1)
    rewards[-1] = rng.choice([1, 2, 5])
    s = rng.randint(0, n_states - 2)
    r = rewards[s]
    V_next = V[s + 1] if s + 1 < n_states else 0
    delta = r + gamma * V_next - V[s]
    V_new = V[s] + alpha * delta

    stmt = (
        f"States $s_0, \\ldots, s_{n_states-1}$ (terminal). "
        f"$V = [{', '.join(f'{v:.2f}' for v in V)}]$, $\\gamma = {gamma}$, $\\alpha = {alpha}$. "
        f"Reward at $s_{n_states-2} \\to s_{n_states-1}$: $r = {rewards[-1]}$. "
        f"Compute TD error $\\delta$ at state $s_{s}$ and update $V(s_{s})$."
    )
    sol = (
        f"$\\delta_{s} = r_{s} + \\gamma V(s_{{{s+1}}}) - V(s_{s}) = {r} + {gamma}({V_next:.2f}) - {V[s]:.2f} = {delta:.4f}$\n\n"
        f"DA signal: **{'burst (δ>0)' if delta > 0.01 else 'pause (δ<0)' if delta < -0.01 else 'no change (δ≈0)'}**\n\n"
        f"$V(s_{s}) \\leftarrow {V[s]:.2f} + {alpha}({delta:.4f}) = {V_new:.4f}$"
    )
    return Problem("TD error computation", stmt, sol)


def gen_three_factor(rng: random.Random) -> Problem:
    x_pre = round(rng.uniform(0.3, 1.0), 2)
    x_post = round(rng.uniform(0.3, 1.0), 2)
    eta = 0.01
    M = round(rng.uniform(-2, 3), 1)
    dw = eta * x_pre * x_post * M
    modulator = "DA burst" if M > 0 else "DA pause" if M < 0 else "no modulation"
    stmt = (
        f"Three-factor rule: $x_{{\\text{{pre}}}} = {x_pre}$, $x_{{\\text{{post}}}} = {x_post}$, "
        f"$\\eta = {eta}$, modulator $M = {M}$ ({modulator}). Compute $\\Delta w$."
    )
    sol = (
        f"$\\Delta w = {eta} \\times {x_pre} \\times {x_post} \\times {M} = {dw:.5f}$\n\n"
        f"Result: **{'LTP (strengthening)' if dw > 0 else 'LTD (weakening)' if dw < 0 else 'no change'}**"
    )
    return Problem("Three-factor learning", stmt, sol)


def gen_ach_learning_rate(rng: random.Random) -> Problem:
    alpha_0 = 0.01
    k = rng.choice([3, 5, 8, 10])
    ach = round(rng.uniform(0, 1), 2)
    alpha_eff = alpha_0 * (1 + k * ach)
    base_dw = round(rng.uniform(0.002, 0.01), 4)
    actual_dw = base_dw * (1 + k * ach)
    stmt = (
        f"Baseline $\\alpha_0 = {alpha_0}$, ACh gain $k = {k}$, $[\\text{{ACh}}] = {ach}$. "
        f"Base STDP event $\\Delta w_0 = {base_dw}$. Compute effective weight change."
    )
    sol = (
        f"$\\alpha_{{\\text{{eff}}}} = {alpha_0} \\times (1 + {k} \\times {ach}) = {alpha_0} \\times {1+k*ach:.2f} = {alpha_eff:.4f}$\n\n"
        f"$\\Delta w = {base_dw} \\times {1+k*ach:.2f} = {actual_dw:.5f}$\n\n"
        f"ACh amplification: **{1+k*ach:.1f}×** the baseline plasticity"
    )
    return Problem("ACh learning rate modulation", stmt, sol)


GENERATORS = [gen_td_error, gen_three_factor, gen_ach_learning_rate]


def main():
    parser = argparse.ArgumentParser(description="11.6 Dopamine RPE simulator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/neuro, dopamine, TD-learning, neuromodulators, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.6 Practice — Neuromodulators & TD Learning\n\n"
        f"Generated {args.count} problems (seed={seed}).\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

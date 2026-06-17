#!/usr/bin/env python3
"""
11.7_bio_vs_ai_compare.py — Side-by-side simulation of Hebbian vs backprop
on the same toy task (AND, OR, XOR).

Modes:
  --demo : Train both learning rules on AND/OR/XOR, plot convergence comparison
  default: Generate comparison drill problems

Usage:
  python 11.7_bio_vs_ai_compare.py --demo
  python 11.7_bio_vs_ai_compare.py --count 10 --seed 42
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


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)


# --- Hebbian single-layer learner ---
def train_hebbian(X, y, epochs=100, eta=0.01):
    n_features = X.shape[1]
    w = np.random.randn(n_features) * 0.1
    b = 0.0
    losses = []
    for _ in range(epochs):
        total_loss = 0
        for xi, yi in zip(X, y):
            z = np.dot(w, xi) + b
            out = sigmoid(z)
            # Oja-like update with target modulation
            err = yi - out
            w += eta * err * xi
            b += eta * err
            total_loss += err**2
        losses.append(total_loss / len(X))
    predictions = sigmoid(X @ w + b)
    return w, b, losses, predictions


# --- Backprop 2-layer learner ---
def train_backprop(X, y, hidden=4, epochs=500, eta=0.5):
    n_in = X.shape[1]
    W1 = np.random.randn(n_in, hidden) * 0.5
    b1 = np.zeros(hidden)
    W2 = np.random.randn(hidden, 1) * 0.5
    b2 = np.zeros(1)
    losses = []

    for _ in range(epochs):
        # Forward
        z1 = X @ W1 + b1
        h = sigmoid(z1)
        z2 = h @ W2 + b2
        out = sigmoid(z2).flatten()

        # Loss
        loss = np.mean((y - out) ** 2)
        losses.append(loss)

        # Backward
        d_out = (out - y) * sigmoid_deriv(z2.flatten())
        dW2 = h.T @ d_out.reshape(-1, 1) / len(X)
        db2 = np.mean(d_out)

        d_hidden = np.outer(d_out, W2.flatten()) * sigmoid_deriv(z1)
        dW1 = X.T @ d_hidden / len(X)
        db1 = np.mean(d_hidden, axis=0)

        W2 -= eta * dW2
        b2 -= eta * db2
        W1 -= eta * dW1
        b1 -= eta * db1

    predictions = sigmoid(sigmoid(X @ W1 + b1) @ W2 + b2).flatten()
    return losses, predictions


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo")
        sys.exit(1)

    np.random.seed(42)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    tasks = {
        "AND": np.array([0, 0, 0, 1], dtype=float),
        "OR": np.array([0, 1, 1, 1], dtype=float),
        "XOR": np.array([0, 1, 1, 0], dtype=float),
    }

    fig, axes = plt.subplots(3, 2, figsize=(12, 10))

    for row, (task_name, y) in enumerate(tasks.items()):
        # Hebbian (single layer)
        _, _, hebb_losses, hebb_pred = train_hebbian(X, y, epochs=200, eta=0.1)

        # Backprop (2-layer)
        bp_losses, bp_pred = train_backprop(X, y, hidden=4, epochs=200, eta=1.0)

        # Loss curves
        axes[row, 0].plot(hebb_losses, 'b', label='Hebbian (1-layer)', linewidth=1.5)
        axes[row, 0].plot(bp_losses, 'r', label='Backprop (2-layer)', linewidth=1.5)
        axes[row, 0].set_ylabel("MSE Loss")
        axes[row, 0].set_title(f"{task_name} — Learning Curves")
        axes[row, 0].legend()
        axes[row, 0].set_ylim(0, 0.3)

        # Predictions
        x_pos = np.arange(4)
        width = 0.25
        axes[row, 1].bar(x_pos - width, y, width, label='Target', color='gray', alpha=0.5)
        axes[row, 1].bar(x_pos, hebb_pred, width, label='Hebbian', color='blue', alpha=0.7)
        axes[row, 1].bar(x_pos + width, bp_pred, width, label='Backprop', color='red', alpha=0.7)
        axes[row, 1].set_xticks(x_pos)
        axes[row, 1].set_xticklabels(['(0,0)', '(0,1)', '(1,0)', '(1,1)'])
        axes[row, 1].set_title(f"{task_name} — Final Predictions")
        axes[row, 1].legend()
        axes[row, 1].set_ylim(0, 1.2)

    axes[-1, 0].set_xlabel("Epoch")
    axes[-1, 1].set_xlabel("Input pattern")
    plt.tight_layout()
    plt.savefig("bio_vs_ai_compare_demo.png", dpi=150)
    print("Saved: bio_vs_ai_compare_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_comparison(rng: random.Random) -> Problem:
    dims = [
        ("Learning rule", "Local (STDP/Hebbian)", "Global (backpropagation)"),
        ("Communication", "Binary spikes (~1ms)", "Continuous float values"),
        ("Energy per op", "~10⁻¹⁵ J (1 fJ)", "~10⁻⁸ J"),
        ("Feedback", "Massive recurrence", "Mostly feedforward"),
        ("Error signal", "Neuromodulators (DA)", "Explicit loss gradient"),
        ("Noise", "Intrinsic stochasticity", "Deterministic (usually)"),
        ("Scale", "86B neurons, 150T synapses", "Up to ~1.8T parameters"),
        ("Attention", "ACh + top-down feedback", "Scaled dot-product attention"),
    ]
    dim, bio, ai = rng.choice(dims)
    stmt = f"Compare biological and artificial neural networks on the dimension: **{dim}**."
    sol = f"**Biological:** {bio}\n\n**Artificial:** {ai}"
    return Problem("Bio vs AI comparison", stmt, sol)


def gen_energy_calc(rng: random.Random) -> Problem:
    n_neurons = rng.choice([100, 160, 200]) * 1_000_000
    syns_per = rng.choice([500, 1000, 2000])
    e_syn = 1e-15  # 1 fJ
    cycle_ms = rng.choice([10, 20, 50])
    total_ops = n_neurons * syns_per
    total_energy = total_ops * e_syn
    power = total_energy / (cycle_ms * 1e-3)
    stmt = (
        f"Estimate brain power: {n_neurons/1e6:.0f}M active neurons, "
        f"{syns_per} synaptic ops/neuron/cycle, cycle = {cycle_ms} ms, "
        f"energy/synapse = $10^{{-15}}$ J."
    )
    sol = (
        f"Total ops: ${n_neurons/1e6:.0f} \\times 10^6 \\times {syns_per} = {total_ops:.2e}$\n\n"
        f"Energy/cycle: ${total_ops:.2e} \\times 10^{{-15}} = {total_energy:.2e}$ J\n\n"
        f"Power: ${total_energy:.2e} / {cycle_ms*1e-3}$ s $= {power:.1f}$ W"
    )
    return Problem("Neural energy efficiency", stmt, sol)


def gen_xor_separability(rng: random.Random) -> Problem:
    task = rng.choice(["AND", "OR", "XOR", "NAND", "NOR", "XNOR"])
    separable = task in ["AND", "OR", "NAND", "NOR"]
    stmt = (
        f"Is the **{task}** function linearly separable? "
        f"Can a single-layer Hebbian network learn it?"
    )
    sol = (
        f"**{task}** is {'linearly separable ✓' if separable else 'NOT linearly separable ✗'}.\n\n"
        f"A single-layer network {'CAN' if separable else 'CANNOT'} learn {task}. "
        + ("A decision boundary (hyperplane) exists that separates the classes."
           if separable else
           "Requires a hidden layer (multi-layer architecture) to create nonlinear decision boundary.")
    )
    return Problem("Linear separability", stmt, sol)


GENERATORS = [gen_comparison, gen_energy_calc, gen_xor_separability]


def main():
    parser = argparse.ArgumentParser(description="11.7 Bio vs AI comparison")
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
        "---\ntags: [review/neuro, computational-cognition, bio-vs-ai, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.7 Practice — Computational Cognition: Bio vs AI\n\n"
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

#!/usr/bin/env python3
"""
10.2_backprop.py — Practice problem generator for Chapter 10.2
(Deep Neural Networks: Backpropagation & Architecture).

Generates randomized drill problems across 5 archetypes:
  1. Forward pass through a 2-layer MLP (compute activations)
  2. Backward pass: compute dL/dW for a given layer
  3. Activation function derivative evaluation
  4. Parameter count for a given architecture
  5. Gradient magnitude estimation (vanishing gradient)

Usage:
  python 10.2_backprop.py
  python 10.2_backprop.py --count 10 --seed 7
  python 10.2_backprop.py --demo

Exit code 0 on success.
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
            f"{self.statement_md}\n\n"
            "?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_forward_pass(rng: random.Random) -> Problem:
    W1 = np.array([[rng.uniform(-1,1) for _ in range(2)] for _ in range(2)])
    x = np.array([rng.randint(-2,2), rng.randint(-2,2)], dtype=float)
    W2 = np.array([[rng.uniform(-1,1) for _ in range(2)]])
    z1 = W1 @ x
    h1 = np.maximum(0, z1)
    z2 = (W2 @ h1)[0]

    def fmt(arr): return ", ".join(f"{v:.3f}" for v in arr)

    stmt = (
        f"Compute the forward pass for input $x = ({fmt(x)})$ through:\n\n"
        f"$W^{{(1)}} = \\begin{{pmatrix}}{W1[0,0]:.2f}&{W1[0,1]:.2f}\\\\{W1[1,0]:.2f}&{W1[1,1]:.2f}\\end{{pmatrix}}$, "
        f"$W^{{(2)}} = ({W2[0,0]:.2f}, {W2[0,1]:.2f})$, ReLU activation. Biases = 0."
    )
    sol = (
        f"$z^{{(1)}} = W^{{(1)}}x = ({fmt(z1)})$\n\n"
        f"$h^{{(1)}} = \\text{{ReLU}}(z^{{(1)}}) = ({fmt(h1)})$\n\n"
        f"$z^{{(2)}} = W^{{(2)}}h^{{(1)}} = {z2:.4f}$"
    )
    return Problem("Forward pass", stmt, sol)


def gen_backward_pass(rng: random.Random) -> Problem:
    h = np.array([rng.uniform(0,2), rng.uniform(0,2)])
    delta = round(rng.uniform(-1,1), 3)
    dW2 = delta * h

    def fmt(arr): return ", ".join(f"{v:.3f}" for v in arr)

    stmt = (
        f"Given $\\delta^{{(2)}} = {delta}$ and hidden activation $h = ({fmt(h)})$, "
        "compute $\\partial\\mathcal{{L}}/\\partial W^{{(2)}}$."
    )
    sol = (
        f"$\\frac{{\\partial\\mathcal{{L}}}}{{\\partial W^{{(2)}}}} = \\delta^{{(2)}} \\cdot h^T = "
        f"{delta} \\cdot ({fmt(h)}) = ({fmt(dW2)})$"
    )
    return Problem("Backward pass (weight gradient)", stmt, sol)


def gen_activation_deriv(rng: random.Random) -> Problem:
    z = round(rng.uniform(-3, 3), 2)
    act = rng.choice(["sigmoid", "tanh", "relu"])
    if act == "sigmoid":
        s = 1/(1+np.exp(-z))
        deriv = s*(1-s)
        formula = f"$\\sigma'(z) = \\sigma(z)(1-\\sigma(z)) = {s:.4f}\\cdot{1-s:.4f} = {deriv:.6f}$"
    elif act == "tanh":
        t = np.tanh(z)
        deriv = 1 - t**2
        formula = f"$\\tanh'(z) = 1 - \\tanh^2(z) = 1 - {t:.4f}^2 = {deriv:.6f}$"
    else:
        deriv = 1.0 if z > 0 else 0.0
        formula = f"$\\text{{ReLU}}'(z) = \\mathbb{{1}}[z>0] = {int(deriv)}$"
    stmt = f"Compute the derivative of {act} at $z = {z}$."
    sol = formula
    return Problem("Activation derivative", stmt, sol)


def gen_param_count(rng: random.Random) -> Problem:
    layers = [rng.choice([16,32,64,128,256,784])]
    for _ in range(rng.randint(1,3)):
        layers.append(rng.choice([16,32,64,128,256]))
    layers.append(rng.choice([2,5,10]))
    arch_str = " → ".join(str(l) for l in layers)
    total = sum(layers[i]*layers[i+1] + layers[i+1] for i in range(len(layers)-1))
    stmt = f"Count the total trainable parameters in an MLP with architecture: {arch_str}."
    details = []
    for i in range(len(layers)-1):
        p = layers[i]*layers[i+1] + layers[i+1]
        details.append(f"Layer {i+1}: ${layers[i]}\\times{layers[i+1]} + {layers[i+1]} = {p}$")
    sol = "\n\n".join(details) + f"\n\n**Total: {total} parameters.**"
    return Problem("Parameter count", stmt, sol)


def gen_vanishing(rng: random.Random) -> Problem:
    L = rng.randint(5, 12)
    act = rng.choice(["sigmoid", "tanh"])
    max_deriv = 0.25 if act == "sigmoid" else 1.0
    factor = max_deriv ** (L-1)
    stmt = (
        f"For a {L}-layer network with {act} activations and $\\|W^{{(\\ell)}}\\| \\approx 1$, "
        "estimate the maximum gradient magnitude at layer 1 relative to the output gradient."
    )
    sol = (
        f"Max derivative of {act}: ${max_deriv}$.\n\n"
        f"Gradient ratio: $({max_deriv})^{{{L-1}}} = {factor:.2e}$.\n\n"
        f"The gradient at layer 1 is at most ${factor:.2e}$ of the output gradient."
    )
    return Problem("Vanishing gradient estimate", stmt, sol)


def run_demo():
    print("=" * 60)
    print("DEMO: 2-Layer MLP learning XOR with manual backprop")
    print("=" * 60)
    np.random.seed(42)
    X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
    y = np.array([0,1,1,0], dtype=float)

    W1 = np.random.randn(4, 2) * 0.5
    b1 = np.zeros(4)
    W2 = np.random.randn(1, 4) * 0.5
    b2 = np.zeros(1)
    lr = 0.5

    for epoch in range(2000):
        loss = 0
        for i in range(4):
            z1 = W1 @ X[i] + b1
            h1 = np.maximum(0, z1)
            z2 = W2 @ h1 + b2
            pred = z2[0]
            loss += 0.5*(pred - y[i])**2

            d2 = np.array([pred - y[i]])
            dW2 = np.outer(d2, h1)
            db2 = d2
            dh1 = W2.T @ d2
            d1 = dh1.flatten() * (z1 > 0)
            dW1 = np.outer(d1, X[i])
            db1 = d1

            W2 -= lr * dW2
            b2 -= lr * db2
            W1 -= lr * dW1
            b1 -= lr * db1

        if epoch % 500 == 0:
            print(f"Epoch {epoch:4d}: loss = {loss:.6f}")

    print("\nFinal predictions:")
    for i in range(4):
        z1 = W1 @ X[i] + b1
        h1 = np.maximum(0, z1)
        pred = (W2 @ h1 + b2)[0]
        print(f"  {X[i]} -> {pred:.4f} (target: {y[i]})")


GENERATORS = [gen_forward_pass, gen_backward_pass, gen_activation_deriv, gen_param_count, gen_vanishing]


def main():
    parser = argparse.ArgumentParser(description="10.2 Backprop practice problems")
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

    lines = [
        "---", "tags: [review/ai, backpropagation, mlp, neural-networks]",
        "generated: true", "---", "",
        "# 10.2 Backpropagation — Practice Problems", "",
    ]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

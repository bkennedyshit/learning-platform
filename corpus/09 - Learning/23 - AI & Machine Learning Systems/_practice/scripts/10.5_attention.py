#!/usr/bin/env python3
"""
10.5_attention.py — Practice problems for Transformer Architectures.

Archetypes:
  1. Compute scaled dot-product attention for small QKV
  2. Multi-head dimension bookkeeping
  3. Positional encoding computation
  4. Parameter count for Transformer model
  5. Causal mask application

Usage:
  python 10.5_attention.py --count 10 --seed 42
  python 10.5_attention.py --demo
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


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def gen_attention(rng: random.Random) -> Problem:
    n, dk = 3, 2
    Q = np.array([[rng.randint(-1,2) for _ in range(dk)] for _ in range(n)], dtype=float)
    K = np.array([[rng.randint(-1,2) for _ in range(dk)] for _ in range(n)], dtype=float)
    V = np.array([[rng.randint(0,2) for _ in range(dk)] for _ in range(n)], dtype=float)
    scores = Q @ K.T / np.sqrt(dk)
    weights = softmax(scores)
    output = weights @ V

    def mat(m): return "\\begin{pmatrix}" + "\\\\".join("&".join(f"{v:.0f}" for v in row) for row in m) + "\\end{pmatrix}"

    stmt = (
        f"Compute Attention$(Q,K,V)$ with $d_k={dk}$:\n\n"
        f"$Q={mat(Q)}$, $K={mat(K)}$, $V={mat(V)}$"
    )
    w_str = "\\\\".join("&".join(f"{v:.3f}" for v in row) for row in weights)
    o_str = "\\\\".join("&".join(f"{v:.3f}" for v in row) for row in output)
    sol = (
        f"$QK^T/\\sqrt{{{dk}}} = $ (compute scores)\n\n"
        f"Attention weights: $\\begin{{pmatrix}}{w_str}\\end{{pmatrix}}$\n\n"
        f"Output: $\\begin{{pmatrix}}{o_str}\\end{{pmatrix}}$"
    )
    return Problem("Scaled dot-product attention", stmt, sol)


def gen_multihead_dims(rng: random.Random) -> Problem:
    d_model = rng.choice([256, 512, 768, 1024])
    h = rng.choice([4, 8, 12, 16])
    d_k = d_model // h
    n = rng.choice([64, 128, 256, 512])
    params = 4 * d_model * d_model
    stmt = (
        f"Multi-head attention: $d_{{model}}={d_model}$, $h={h}$ heads, sequence length $n={n}$. "
        "State: (a) $d_k$, (b) shape of attention matrix per head, (c) total MHA parameters."
    )
    sol = (
        f"(a) $d_k = d_{{model}}/h = {d_model}/{h} = {d_k}$\n\n"
        f"(b) Attention matrix per head: $(n \\times n) = ({n} \\times {n})$\n\n"
        f"(c) Parameters: $4 \\times d_{{model}}^2 = 4 \\times {d_model}^2 = {params:,}$"
    )
    return Problem("Multi-head dimensions", stmt, sol)


def gen_pos_encoding(rng: random.Random) -> Problem:
    pos = rng.randint(1, 20)
    d_model = 512
    i = rng.randint(0, 5)
    omega = 1.0 / (10000 ** (2*i / d_model))
    pe_sin = np.sin(pos * omega)
    pe_cos = np.cos(pos * omega)
    stmt = (
        f"Compute positional encoding for position $pos={pos}$, "
        f"dimensions $2i={2*i}$ and $2i+1={2*i+1}$ with $d_{{model}}={d_model}$."
    )
    sol = (
        f"$\\omega_{{{i}}} = 1/10000^{{{2*i}/{d_model}}} = {omega:.6f}$\n\n"
        f"$PE_{{{pos},{2*i}}} = \\sin({pos} \\times {omega:.6f}) = {pe_sin:.6f}$\n\n"
        f"$PE_{{{pos},{2*i+1}}} = \\cos({pos} \\times {omega:.6f}) = {pe_cos:.6f}$"
    )
    return Problem("Positional encoding", stmt, sol)


def gen_param_count(rng: random.Random) -> Problem:
    L = rng.choice([6, 12, 24])
    d = rng.choice([256, 512, 768])
    h = rng.choice([4, 8, 12])
    d_ff = 4 * d
    V = rng.choice([30000, 50000, 100000])
    per_layer = 4*d*d + 2*d*d_ff + 4*d  # MHA + FFN + norms
    total = L * per_layer + V * d
    stmt = (
        f"Transformer: $L={L}$ layers, $d_{{model}}={d}$, $h={h}$ heads, "
        f"$d_{{ff}}={d_ff}$, vocab $V={V:,}$. Estimate total parameters."
    )
    sol = (
        f"Per layer: MHA=$4d^2={4*d*d:,}$ + FFN=$2d \\cdot d_{{ff}}={2*d*d_ff:,}$ + norms=$4d={4*d}$"
        f" = ${per_layer:,}$\n\n"
        f"All layers: ${L} \\times {per_layer:,} = {L*per_layer:,}$\n\n"
        f"Embeddings: $V \\times d = {V*d:,}$\n\n"
        f"**Total ≈ {total:,}** ({total/1e6:.1f}M parameters)"
    )
    return Problem("Transformer parameter count", stmt, sol)


def run_demo():
    print("=" * 60)
    print("DEMO: Scaled Dot-Product Attention from Scratch")
    print("=" * 60)
    np.random.seed(42)

    n, d_k, d_v = 4, 8, 8
    Q = np.random.randn(n, d_k)
    K = np.random.randn(n, d_k)
    V = np.random.randn(n, d_v)

    scores = Q @ K.T / np.sqrt(d_k)
    weights = softmax(scores)
    output = weights @ V

    print(f"\nQ shape: {Q.shape}, K shape: {K.shape}, V shape: {V.shape}")
    print(f"Scores (QKᵀ/√d_k) shape: {scores.shape}")
    print(f"\nAttention weights (each row sums to 1):")
    print(weights.round(3))
    print(f"\nRow sums: {weights.sum(axis=1).round(6)}")
    print(f"\nOutput shape: {output.shape}")

    # Causal mask demo
    print("\n--- With Causal Mask ---")
    mask = np.triu(np.full((n, n), -np.inf), k=1)
    masked_scores = scores + mask
    masked_weights = softmax(masked_scores)
    print(f"Masked attention weights:")
    print(masked_weights.round(3))
    print("(Upper triangle is zero — no future information leakage)")


GENERATORS = [gen_attention, gen_multihead_dims, gen_pos_encoding, gen_param_count]


def main():
    parser = argparse.ArgumentParser(description="10.5 Attention practice")
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

    lines = ["---", "tags: [review/ai, transformer, attention, llm]",
             "generated: true", "---", "", "# 10.5 Transformers — Practice Problems", ""]
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

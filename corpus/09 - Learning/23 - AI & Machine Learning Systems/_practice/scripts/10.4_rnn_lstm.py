#!/usr/bin/env python3
"""
10.4_rnn_lstm.py — Practice problems for RNNs & LSTMs.

Archetypes:
  1. RNN forward pass (compute h_t given h_{t-1}, x_t)
  2. LSTM gate computation
  3. Vanishing gradient magnitude estimation
  4. Parameter count comparison (RNN vs LSTM vs GRU)
  5. BPTT gradient at a specific time step

Usage:
  python 10.4_rnn_lstm.py --count 10 --seed 42
  python 10.4_rnn_lstm.py --demo
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


def gen_rnn_forward(rng: random.Random) -> Problem:
    H, D = 2, 2
    W_hh = np.array([[round(rng.uniform(-0.5,0.5),2) for _ in range(H)] for _ in range(H)])
    W_xh = np.array([[round(rng.uniform(-0.5,0.5),2) for _ in range(D)] for _ in range(H)])
    h_prev = np.array([round(rng.uniform(-1,1),2) for _ in range(H)])
    x_t = np.array([round(rng.uniform(-1,1),2) for _ in range(D)])
    z = W_hh @ h_prev + W_xh @ x_t
    h_t = np.tanh(z)

    def fmt(a): return f"({', '.join(f'{v:.4f}' for v in a)})"

    stmt = (
        f"Compute $h_t$ for RNN cell with $h_{{t-1}} = {fmt(h_prev)}$, $x_t = {fmt(x_t)}$,\n\n"
        f"$W_{{hh}} = \\begin{{pmatrix}}{W_hh[0,0]}&{W_hh[0,1]}\\\\{W_hh[1,0]}&{W_hh[1,1]}\\end{{pmatrix}}$, "
        f"$W_{{xh}} = \\begin{{pmatrix}}{W_xh[0,0]}&{W_xh[0,1]}\\\\{W_xh[1,0]}&{W_xh[1,1]}\\end{{pmatrix}}$"
    )
    sol = (
        f"$z = W_{{hh}}h_{{t-1}} + W_{{xh}}x_t = {fmt(z)}$\n\n"
        f"$h_t = \\tanh(z) = {fmt(h_t)}$"
    )
    return Problem("RNN forward step", stmt, sol)


def gen_lstm_gates(rng: random.Random) -> Problem:
    c_prev = round(rng.uniform(-2, 2), 2)
    f_t = round(rng.uniform(0.5, 0.99), 2)
    i_t = round(rng.uniform(0.1, 0.8), 2)
    c_tilde = round(rng.uniform(-1, 1), 2)
    o_t = round(rng.uniform(0.3, 0.9), 2)
    c_t = f_t * c_prev + i_t * c_tilde
    h_t = o_t * np.tanh(c_t)
    stmt = (
        f"LSTM single unit: $c_{{t-1}}={c_prev}$, $f_t={f_t}$, $i_t={i_t}$, "
        f"$\\tilde{{c}}_t={c_tilde}$, $o_t={o_t}$. Compute $c_t$ and $h_t$."
    )
    sol = (
        f"$c_t = {f_t} \\cdot {c_prev} + {i_t} \\cdot {c_tilde} = {f_t*c_prev:.4f} + {i_t*c_tilde:.4f} = {c_t:.4f}$\n\n"
        f"$h_t = {o_t} \\cdot \\tanh({c_t:.4f}) = {o_t} \\cdot {np.tanh(c_t):.4f} = {h_t:.4f}$"
    )
    return Problem("LSTM gate computation", stmt, sol)


def gen_vanishing(rng: random.Random) -> Problem:
    lam = round(rng.uniform(0.5, 0.95), 2)
    T = rng.randint(10, 50)
    mag = lam ** T
    stmt = (
        f"RNN with $|\\lambda_{{\\max}}(W_{{hh}})| = {lam}$. "
        f"Estimate gradient magnitude ratio from step $T={T}$ back to step 1."
    )
    sol = f"$|\\lambda|^{{{T}}} = {lam}^{{{T}}} = {mag:.6f}$. Gradient retains only ${mag*100:.4f}\\%$ of output magnitude."
    return Problem("Vanishing gradient", stmt, sol)


def gen_param_count(rng: random.Random) -> Problem:
    H = rng.choice([64, 128, 256, 512])
    D = rng.choice([32, 64, 128, 256])
    rnn_p = H*H + H*D + H
    lstm_p = 4*(H*(H+D) + H)
    gru_p = 3*(H*(H+D) + H)
    stmt = f"Compare parameter counts for RNN, LSTM, GRU with $H={H}$, $D={D}$."
    sol = (
        f"**RNN:** $H^2 + HD + H = {H}^2 + {H}\\cdot{D} + {H} = {rnn_p:,}$\n\n"
        f"**LSTM:** $4(H(H+D) + H) = 4({H}\\cdot{H+D} + {H}) = {lstm_p:,}$\n\n"
        f"**GRU:** $3(H(H+D) + H) = 3({H}\\cdot{H+D} + {H}) = {gru_p:,}$"
    )
    return Problem("Parameter count", stmt, sol)


def run_demo():
    print("=" * 60)
    print("DEMO: RNN vs LSTM gradient flow over 50 time steps")
    print("=" * 60)
    np.random.seed(0)
    H = 4

    # RNN: gradient product
    W_hh = np.random.randn(H, H) * 0.5
    eigenvalues = np.linalg.eigvals(W_hh)
    spectral_radius = np.max(np.abs(eigenvalues))
    print(f"\nRNN W_hh spectral radius: {spectral_radius:.4f}")

    grad_product = np.eye(H)
    rnn_norms = []
    for t in range(50):
        tanh_deriv = np.diag(np.random.uniform(0.5, 1.0, H))
        grad_product = tanh_deriv @ W_hh @ grad_product
        rnn_norms.append(np.linalg.norm(grad_product))

    print(f"RNN gradient norm after 10 steps: {rnn_norms[9]:.6f}")
    print(f"RNN gradient norm after 50 steps: {rnn_norms[49]:.6f}")

    # LSTM: gradient through cell state
    lstm_norms = []
    cell_grad = np.ones(H)
    for t in range(50):
        f_t = np.random.uniform(0.85, 0.99, H)
        cell_grad = cell_grad * f_t
        lstm_norms.append(np.linalg.norm(cell_grad))

    print(f"\nLSTM cell gradient norm after 10 steps: {lstm_norms[9]:.6f}")
    print(f"LSTM cell gradient norm after 50 steps: {lstm_norms[49]:.6f}")
    print(f"\nRatio (LSTM/RNN) at step 50: {lstm_norms[49]/max(rnn_norms[49],1e-15):.1f}x better")


GENERATORS = [gen_rnn_forward, gen_lstm_gates, gen_vanishing, gen_param_count]


def main():
    parser = argparse.ArgumentParser(description="10.4 RNN/LSTM practice")
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

    lines = ["---", "tags: [review/ai, rnn, lstm, sequence-modeling]",
             "generated: true", "---", "", "# 10.4 RNNs & LSTMs — Practice Problems", ""]
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

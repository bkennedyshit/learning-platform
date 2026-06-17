#!/usr/bin/env python3
"""
11.4_callosal_transfer.py — Hemispheric communication delay simulator
and bilateral-task reaction-time model.

Modes:
  --demo : Simulate coupled-hemisphere dynamics and CUD measurement
  default: Generate lateralization/IHTT drill problems

Usage:
  python 11.4_callosal_transfer.py --demo
  python 11.4_callosal_transfer.py --count 10 --seed 42
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


def sigmoid(x, beta=1.0, theta=2.0):
    return 1.0 / (1.0 + np.exp(-beta * (x - theta)))


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo")
        sys.exit(1)

    dt = 0.1  # ms
    T = 200.0
    steps = int(T / dt)
    t = np.linspace(0, T, steps)

    # Parameters
    a = 3.0  # self-excitation
    tau = 10.0  # time constant (ms)
    I_stim = 2.0  # stimulus strength

    configs = [
        ("Strong Lateralization (c=-2.0)", -2.0),
        ("Moderate Lateralization (c=-1.0)", -1.0),
        ("Bilateral Processing (c=-0.3)", -0.3),
    ]

    fig, axes = plt.subplots(len(configs), 1, figsize=(10, 8), sharex=True)

    for ax, (label, c) in zip(axes, configs):
        L = np.zeros(steps)
        R = np.zeros(steps)
        L[0] = 0.1
        R[0] = 0.1

        # Stimulus to right hemisphere at t=50ms
        I_L = np.zeros(steps)
        I_R = np.zeros(steps)
        I_R[int(50 / dt):int(55 / dt)] = I_stim

        # IHTT delay (10ms for callosal transfer)
        delay_steps = int(10.0 / dt)

        for i in range(1, steps):
            R_delayed = R[max(0, i - delay_steps)]
            L_delayed = L[max(0, i - delay_steps)]

            dL = (-L[i-1] + sigmoid(a * L[i-1] + c * R_delayed + I_L[i-1])) / tau
            dR = (-R[i-1] + sigmoid(a * R[i-1] + c * L_delayed + I_R[i-1])) / tau

            L[i] = L[i-1] + dt * dL
            R[i] = R[i-1] + dt * dR

        ax.plot(t, L, 'b', label='Left hemisphere', linewidth=1.5)
        ax.plot(t, R, 'r', label='Right hemisphere', linewidth=1.5)
        ax.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Stimulus onset')
        ax.set_ylabel("Activity")
        ax.set_title(label)
        ax.legend(loc="upper right")
        ax.set_ylim(-0.1, 1.1)

    axes[-1].set_xlabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("callosal_transfer_demo.png", dpi=150)
    print("Saved: callosal_transfer_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_ihtt(rng: random.Random) -> Problem:
    d_axon = rng.choice([1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    path_mm = rng.randint(70, 120)
    t_syn = rng.choice([0.5, 1.0, 1.5])
    v = 6 * d_axon
    t_cond = (path_mm * 1e-3) / v * 1000  # ms
    ihtt = t_cond + t_syn
    stmt = (
        f"Calculate IHTT for a callosal axon: diameter = {d_axon} μm, "
        f"path length = {path_mm} mm, synaptic delay = {t_syn} ms."
    )
    sol = (
        f"$v = 6 \\times {d_axon} = {v:.0f}$ m/s\n\n"
        f"$t_{{\\text{{cond}}}} = \\frac{{{path_mm} \\times 10^{{-3}}}}{{{v:.0f}}} \\times 1000 = {t_cond:.2f}$ ms\n\n"
        f"$\\text{{IHTT}} = {t_cond:.2f} + {t_syn} = {ihtt:.2f}$ ms"
    )
    return Problem("IHTT calculation", stmt, sol)


def gen_bandwidth(rng: random.Random) -> Problem:
    n_axons = rng.choice([20, 40, 60, 80, 100, 150, 200]) * 1_000_000
    rate = rng.choice([5, 10, 15, 20])
    p = rate / 1000
    H = -p * np.log2(p) - (1 - p) * np.log2(1 - p) if 0 < p < 1 else 0
    bw = n_axons * 1000 * H
    stmt = (
        f"Estimate callosal bandwidth: {n_axons/1e6:.0f} million axons, "
        f"mean firing rate = {rate} Hz, 1 ms time bins."
    )
    sol = (
        f"$p = {rate}/1000 = {p}$\n\n"
        f"$H(p) = -{p}\\log_2({p}) - {1-p:.3f}\\log_2({1-p:.3f}) = {H:.4f}$ bits/bin\n\n"
        f"$C = {n_axons/1e6:.0f} \\times 10^6 \\times 1000 \\times {H:.4f} = {bw:.2e}$ bits/s "
        f"$\\approx {bw/1e9:.2f}$ Gbit/s"
    )
    return Problem("Callosal bandwidth", stmt, sol)


def gen_laterality_index(rng: random.Random) -> Problem:
    A_L = round(rng.uniform(0.2, 5.0), 2)
    A_R = round(rng.uniform(0.2, 5.0), 2)
    LI = (A_L - A_R) / (A_L + A_R)
    if LI > 0.2:
        interp = "left-lateralized"
    elif LI < -0.2:
        interp = "right-lateralized"
    else:
        interp = "bilateral"
    stmt = (
        f"fMRI activation: left hemisphere $A_L = {A_L}$, right hemisphere $A_R = {A_R}$. "
        f"Compute the laterality index and interpret."
    )
    sol = (
        f"$LI = \\frac{{{A_L} - {A_R}}}{{{A_L} + {A_R}}} = \\frac{{{A_L - A_R:.2f}}}{{{A_L + A_R:.2f}}} = {LI:.3f}$\n\n"
        f"Interpretation: **{interp}** (LI {'> 0.2' if LI > 0.2 else '< -0.2' if LI < -0.2 else '∈ [-0.2, 0.2]'})"
    )
    return Problem("Laterality index", stmt, sol)


GENERATORS = [gen_ihtt, gen_bandwidth, gen_laterality_index]


def main():
    parser = argparse.ArgumentParser(description="11.4 Callosal transfer simulator")
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
        "---\ntags: [review/neuro, lateralization, corpus-callosum, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.4 Practice — Hemispheric Lateralization\n\n"
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

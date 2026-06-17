#!/usr/bin/env python3
"""
11.3_stdp_simulator.py — STDP weight-update rule simulation
comparing Hebb / anti-Hebb / classical STDP.

Modes:
  --demo : Run STDP simulation showing weight evolution for correlated spike trains
  default: Generate plasticity drill problems in SR card format

Usage:
  python 11.3_stdp_simulator.py --demo
  python 11.3_stdp_simulator.py --count 10 --seed 42
  python 11.3_stdp_simulator.py --out /tmp/_113.md
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


def stdp_kernel(dt, A_plus=0.01, A_minus=0.012, tau_plus=20.0, tau_minus=20.0):
    """Compute STDP weight change for a given dt = t_post - t_pre."""
    if dt > 0:
        return A_plus * np.exp(-dt / tau_plus)
    elif dt < 0:
        return -A_minus * np.exp(dt / tau_minus)
    return 0.0


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo")
        sys.exit(1)

    np.random.seed(42)
    duration = 1000.0  # ms
    dt_sim = 0.1
    n_pre = 5
    w_init = 0.5

    # Generate pre/post spike trains (Poisson)
    r_pre = 20.0  # Hz
    r_post = 15.0

    # Three learning rules
    rules = {
        "Classical STDP": {"A+": 0.005, "A-": 0.005, "tau+": 20, "tau-": 20},
        "Hebbian (LTP only)": {"A+": 0.005, "A-": 0.0, "tau+": 20, "tau-": 20},
        "Anti-Hebbian (LTD only)": {"A+": 0.0, "A-": 0.005, "tau+": 20, "tau-": 20},
    }

    fig, axes = plt.subplots(len(rules), 1, figsize=(10, 8), sharex=True)

    for ax, (rule_name, params) in zip(axes, rules.items()):
        weights = np.full(n_pre, w_init)
        weight_history = [weights.copy()]

        # Generate spike trains
        pre_spikes = [np.sort(np.random.uniform(0, duration,
                      size=int(r_pre * duration / 1000))) for _ in range(n_pre)]
        # Post spikes: correlated with first 2 pre neurons (5ms delay)
        post_spikes = []
        for t in pre_spikes[0]:
            if np.random.rand() < 0.3:
                post_spikes.append(t + 5 + np.random.randn())
        post_spikes = np.array(sorted(post_spikes))

        # Apply STDP
        time_points = np.linspace(0, duration, 100)
        for t_idx in range(1, len(time_points)):
            t_start = time_points[t_idx - 1]
            t_end = time_points[t_idx]
            post_in_window = post_spikes[(post_spikes >= t_start) & (post_spikes < t_end)]

            for i in range(n_pre):
                pre_in_window = pre_spikes[i][(pre_spikes[i] >= t_start) & (pre_spikes[i] < t_end)]
                dw = 0.0
                for tp in pre_in_window:
                    for tpost in post_in_window:
                        dt = tpost - tp
                        if abs(dt) < 100:
                            dw += stdp_kernel(dt, params["A+"], params["A-"],
                                            params["tau+"], params["tau-"])
                weights[i] = np.clip(weights[i] + dw, 0, 1)
            weight_history.append(weights.copy())

        wh = np.array(weight_history)
        for i in range(n_pre):
            label = f"Synapse {i+1}" + (" (correlated)" if i == 0 else "")
            ax.plot(time_points, wh[:len(time_points), i], label=label,
                   linewidth=2 if i == 0 else 1)
        ax.set_ylabel("Weight")
        ax.set_title(rule_name)
        ax.legend(loc="upper right", fontsize=8)
        ax.set_ylim(0, 1)

    axes[-1].set_xlabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("stdp_comparison_demo.png", dpi=150)
    print("Saved: stdp_comparison_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_stdp_calc(rng: random.Random) -> Problem:
    t_pre = rng.randint(50, 200)
    dt = rng.choice([-15, -10, -5, 5, 10, 15, 20, 25])
    t_post = t_pre + dt
    A_p, A_m = 0.01, 0.012
    tau_p, tau_m = 20.0, 20.0
    w0 = round(rng.uniform(0.3, 0.8), 2)
    dw = stdp_kernel(dt, A_p, A_m, tau_p, tau_m)
    w_new = w0 + dw
    direction = "LTP" if dt > 0 else "LTD"
    stmt = (
        f"Pre spike at $t_{{\\text{{pre}}}} = {t_pre}$ ms, post spike at $t_{{\\text{{post}}}} = {t_post}$ ms. "
        f"$A_+ = {A_p}$, $A_- = {A_m}$, $\\tau_+ = \\tau_- = {tau_p}$ ms, $w_0 = {w0}$. "
        f"Compute $\\Delta w$ and new weight."
    )
    sol = (
        f"$\\Delta t = {t_post} - {t_pre} = {dt}$ ms → **{direction}**\n\n"
        f"$$\n\\Delta w = {'A_+' if dt > 0 else '-A_-'} \\exp\\left(-\\frac{{|{dt}|}}{{{tau_p}}}\\right) "
        f"= {A_p if dt > 0 else -A_m} \\times e^{{{-abs(dt)/tau_p:.2f}}} = {dw:.6f}\n$$\n\n"
        f"$w_{{\\text{{new}}}} = {w0} + {dw:.6f} = {w_new:.6f}$"
    )
    return Problem("STDP weight update", stmt, sol)


def gen_nmda_block(rng: random.Random) -> Problem:
    V = rng.choice([-70, -60, -50, -40, -30, -20, -10, 0, 10, 20])
    Mg = round(rng.uniform(0.5, 2.0), 1)
    B = 1.0 / (1.0 + (Mg / 3.57) * np.exp(-0.062 * V))
    stmt = (
        f"Calculate NMDA Mg²⁺ unblock fraction at $V_m = {V}$ mV with $[\\text{{Mg}}^{{2+}}]_o = {Mg}$ mM."
    )
    sol = (
        f"$$\nB({V}) = \\frac{{1}}{{1 + \\frac{{{Mg}}}{{3.57}} \\exp(-0.062 \\times {V})}} "
        f"= \\frac{{1}}{{1 + {Mg/3.57:.4f} \\times e^{{{-0.062*V:.3f}}}}} = {B:.4f}\n$$\n\n"
        f"**{B*100:.1f}%** of NMDA current is available at this voltage."
    )
    return Problem("NMDA Mg²⁺ block", stmt, sol)


def gen_oja_step(rng: random.Random) -> Problem:
    x = np.array([round(rng.uniform(-2, 2), 1) for _ in range(2)])
    w = np.array([round(rng.uniform(-1, 1), 1) for _ in range(2)])
    w = w / np.linalg.norm(w)
    eta = 0.1
    y = float(np.dot(w, x))
    dw = eta * y * (x - y * w)
    w_new = w + dw
    stmt = (
        f"Oja's rule: $\\mathbf{{x}} = ({x[0]}, {x[1]})^T$, $\\mathbf{{w}} = ({w[0]:.3f}, {w[1]:.3f})^T$, "
        f"$\\eta = {eta}$. Compute one update step."
    )
    sol = (
        f"$y = \\mathbf{{w}}^T\\mathbf{{x}} = {w[0]:.3f}({x[0]}) + {w[1]:.3f}({x[1]}) = {y:.4f}$\n\n"
        f"$\\Delta\\mathbf{{w}} = {eta} \\times {y:.4f} \\times [({x[0]}, {x[1]})^T - {y:.4f}({w[0]:.3f}, {w[1]:.3f})^T]$\n\n"
        f"$= ({dw[0]:.5f}, {dw[1]:.5f})^T$\n\n"
        f"$\\mathbf{{w}}_{{\\text{{new}}}} = ({w_new[0]:.4f}, {w_new[1]:.4f})^T$"
    )
    return Problem("Oja's rule iteration", stmt, sol)


GENERATORS = [gen_stdp_calc, gen_nmda_block, gen_oja_step]


def main():
    parser = argparse.ArgumentParser(description="11.3 STDP simulator & practice")
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
        "---\ntags: [review/neuro, STDP, hebbian-learning, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.3 Practice — Synaptic Plasticity & Hebbian Learning\n\n"
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

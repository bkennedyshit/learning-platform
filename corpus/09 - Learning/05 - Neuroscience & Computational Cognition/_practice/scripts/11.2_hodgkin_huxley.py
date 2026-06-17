#!/usr/bin/env python3
"""
11.2_hodgkin_huxley.py — Hodgkin-Huxley action potential simulator
and practice problem generator for Chapter 11.2.

Modes:
  --demo    : Integrate HH equations, plot voltage trace + ion currents
  (default) : Generate Nernst/GHK/LIF drill problems in SR card format

Usage:
  python 11.2_hodgkin_huxley.py --demo
  python 11.2_hodgkin_huxley.py --count 10 --seed 42
  python 11.2_hodgkin_huxley.py --out /tmp/_112.md
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


# --- HH Simulation ---
def alpha_m(V): return 0.1 * (25 - V) / (np.exp((25 - V) / 10) - 1) if abs(25 - V) > 1e-7 else 1.0
def beta_m(V): return 4.0 * np.exp(-V / 18)
def alpha_h(V): return 0.07 * np.exp(-V / 20)
def beta_h(V): return 1.0 / (np.exp((30 - V) / 10) + 1)
def alpha_n(V): return 0.01 * (10 - V) / (np.exp((10 - V) / 10) - 1) if abs(10 - V) > 1e-7 else 0.1
def beta_n(V): return 0.125 * np.exp(-V / 80)


def hh_derivs(state, t, I_ext):
    V, m, h, n = state
    gNa, gK, gL = 120.0, 36.0, 0.3
    ENa, EK, EL = 50.0, -77.0, -54.4
    Cm = 1.0

    INa = gNa * m**3 * h * (V - ENa)
    IK = gK * n**4 * (V - EK)
    IL = gL * (V - EL)

    dVdt = (I_ext - INa - IK - IL) / Cm
    dmdt = alpha_m(V) * (1 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1 - n) - beta_n(V) * n
    return [dVdt, dmdt, dhdt, dndt]


def run_hh_simulation(I_ext=10.0, duration=50.0, dt=0.01):
    """Integrate HH equations using RK4."""
    steps = int(duration / dt)
    t = np.linspace(0, duration, steps)
    # Initial conditions (resting state)
    V0 = 0.0  # HH convention: rest = 0
    m0 = alpha_m(V0) / (alpha_m(V0) + beta_m(V0))
    h0 = alpha_h(V0) / (alpha_h(V0) + beta_h(V0))
    n0 = alpha_n(V0) / (alpha_n(V0) + beta_n(V0))

    state = np.array([V0, m0, h0, n0], dtype=float)
    V_trace = np.zeros(steps)
    m_trace = np.zeros(steps)
    h_trace = np.zeros(steps)
    n_trace = np.zeros(steps)

    for i in range(steps):
        V_trace[i], m_trace[i], h_trace[i], n_trace[i] = state
        # RK4
        k1 = np.array(hh_derivs(state, t[i], I_ext))
        k2 = np.array(hh_derivs(state + 0.5 * dt * k1, t[i] + 0.5 * dt, I_ext))
        k3 = np.array(hh_derivs(state + 0.5 * dt * k2, t[i] + 0.5 * dt, I_ext))
        k4 = np.array(hh_derivs(state + dt * k3, t[i] + dt, I_ext))
        state = state + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    # Compute currents
    gNa, gK, gL = 120.0, 36.0, 0.3
    ENa, EK, EL = 50.0, -77.0, -54.4
    INa = gNa * m_trace**3 * h_trace * (V_trace - ENa)
    IK = gK * n_trace**4 * (V_trace - EK)
    IL = gL * (V_trace - EL)

    return t, V_trace, INa, IK, IL, m_trace, h_trace, n_trace


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo. Install: pip install matplotlib")
        sys.exit(1)

    t, V, INa, IK, IL, m, h, n = run_hh_simulation(I_ext=10.0, duration=50.0)

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(t, V, 'k', linewidth=1.5)
    axes[0].set_ylabel("V (mV)")
    axes[0].set_title("Hodgkin-Huxley Action Potential (I_ext = 10 µA/cm²)")
    axes[0].axhline(-55, color='gray', linestyle='--', alpha=0.5, label='Threshold')
    axes[0].legend()

    axes[1].plot(t, -INa, 'r', label='-I_Na', linewidth=1.2)
    axes[1].plot(t, -IK, 'b', label='-I_K', linewidth=1.2)
    axes[1].plot(t, -IL, 'g', label='-I_L', linewidth=0.8)
    axes[1].set_ylabel("Current (µA/cm²)")
    axes[1].legend()

    axes[2].plot(t, m, 'r', label='m (Na⁺ activation)', linewidth=1.2)
    axes[2].plot(t, h, 'orange', label='h (Na⁺ inactivation)', linewidth=1.2)
    axes[2].plot(t, n, 'b', label='n (K⁺ activation)', linewidth=1.2)
    axes[2].set_ylabel("Gating variable")
    axes[2].set_xlabel("Time (ms)")
    axes[2].legend()

    plt.tight_layout()
    plt.savefig("hodgkin_huxley_demo.png", dpi=150)
    print("Saved: hodgkin_huxley_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_nernst(rng: random.Random) -> Problem:
    ions = [
        ("K⁺", +1, (3, 8), (120, 160)),
        ("Na⁺", +1, (130, 155), (8, 15)),
        ("Ca²⁺", +2, (1.5, 3.0), (0.00005, 0.0002)),
        ("Cl⁻", -1, (100, 130), (3, 8)),
    ]
    name, z, out_range, in_range = rng.choice(ions)
    c_out = round(rng.uniform(*out_range), 1)
    c_in = round(rng.uniform(*in_range), 2 if "Ca" in name else 1)
    E = 61.5 / z * np.log10(c_out / c_in)
    stmt = (
        f"Calculate the Nernst equilibrium potential for **{name}** at 37°C.\n\n"
        f"Given: $[{name}]_{{\\text{{out}}}} = {c_out}$ mM, $[{name}]_{{\\text{{in}}}} = {c_in}$ mM, $z = {z:+d}$."
    )
    sol = (
        f"$$\nE_{{{name}}} = \\frac{{61.5}}{{ {z} }} \\log_{{10}}\\frac{{ {c_out} }}{{ {c_in} }} "
        f"= {61.5/z:.1f} \\times \\log_{{10}}({c_out/c_in:.4f}) = {61.5/z:.1f} \\times {np.log10(c_out/c_in):.4f} = {E:.1f} \\text{{ mV}}\n$$"
    )
    return Problem("Nernst equation", stmt, sol)


def gen_ghk(rng: random.Random) -> Problem:
    PK, PNa, PCl = 1.0, round(rng.uniform(0.02, 0.08), 3), round(rng.uniform(0.3, 0.6), 2)
    Ko, Ki = rng.randint(3, 8), rng.randint(120, 160)
    Nao, Nai = rng.randint(130, 155), rng.randint(8, 15)
    Clo, Cli = rng.randint(100, 130), rng.randint(3, 8)
    num = PK * Ko + PNa * Nao + PCl * Cli
    den = PK * Ki + PNa * Nai + PCl * Clo
    Vm = 26.72 * np.log(num / den)
    stmt = (
        f"Compute resting $V_m$ via GHK with $P_K:{PNa}:{PCl}$ and concentrations "
        f"K⁺=[{Ko}/{Ki}], Na⁺=[{Nao}/{Nai}], Cl⁻=[{Clo}/{Cli}] (out/in, mM)."
    )
    sol = (
        f"Numerator: ${PK}({Ko}) + {PNa}({Nao}) + {PCl}({Cli}) = {num:.2f}$\n\n"
        f"Denominator: ${PK}({Ki}) + {PNa}({Nai}) + {PCl}({Clo}) = {den:.2f}$\n\n"
        f"$$\nV_m = 26.72 \\ln\\frac{{{num:.2f}}}{{{den:.2f}}} = 26.72 \\times {np.log(num/den):.4f} = {Vm:.1f} \\text{{ mV}}\n$$"
    )
    return Problem("GHK voltage equation", stmt, sol)


def gen_lif_rate(rng: random.Random) -> Problem:
    tau = rng.choice([10, 12, 15, 20])
    Rm = rng.choice([8, 10, 12, 15])
    I = round(rng.uniform(1.5, 5.0), 1)
    Vrest, Vth, Vreset = -70, -55, -80
    Vinf = Vrest + Rm * I
    if Vinf <= Vth:
        I = round((Vth - Vrest) / Rm + rng.uniform(0.5, 3.0), 1)
        Vinf = Vrest + Rm * I
    f = 1000 / (tau * np.log((Vinf - Vreset) / (Vinf - Vth)))
    stmt = (
        f"LIF neuron: $\\tau_m = {tau}$ ms, $R_m = {Rm}$ MΩ, $V_{{rest}} = {Vrest}$ mV, "
        f"$V_{{thresh}} = {Vth}$ mV, $V_{{reset}} = {Vreset}$ mV. Find firing rate for $I = {I}$ nA."
    )
    sol = (
        f"$V_\\infty = {Vrest} + {Rm} \\times {I} = {Vinf:.1f}$ mV (> threshold ✓)\n\n"
        f"$$\nf = \\left[{tau} \\ln\\frac{{{Vinf:.1f} - ({Vreset})}}{{{Vinf:.1f} - ({Vth})}}\\right]^{{-1}} "
        f"= \\left[{tau} \\ln\\frac{{{Vinf-Vreset:.1f}}}{{{Vinf-Vth:.1f}}}\\right]^{{-1}} = {f:.1f} \\text{{ Hz}}\n$$"
    )
    return Problem("LIF firing rate", stmt, sol)


GENERATORS = [gen_nernst, gen_ghk, gen_lif_rate]


def generate_problems(count: int, seed: int) -> list[Problem]:
    rng = random.Random(seed)
    return [GENERATORS[i % len(GENERATORS)](rng) for i in range(count)]


def main():
    parser = argparse.ArgumentParser(description="11.2 HH simulator & practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true", help="Run HH simulation demo")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    problems = generate_problems(args.count, seed)

    header = (
        "---\ntags: [review/neuro, action-potential, hodgkin-huxley, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.2 Practice — Action Potentials & Ion Channels\n\n"
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

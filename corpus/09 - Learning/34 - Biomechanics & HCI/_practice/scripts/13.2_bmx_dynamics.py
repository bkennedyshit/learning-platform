#!/usr/bin/env python3
"""
13.2_bmx_dynamics.py — Practice problem generator for Chapter 13.2
(Rotational Dynamics in Extreme Sports).

Generates randomized drill problems across 5 archetypes:
  1. Moment of inertia via parallel axis theorem
  2. Angular momentum conservation (tuck/extend)
  3. Takeoff requirements for n rotations
  4. Energy cost of configuration change
  5. Composite body MOI (segmental method)

Usage:
  python 13.2_bmx_dynamics.py
  python 13.2_bmx_dynamics.py --count 12 --seed 42
  python 13.2_bmx_dynamics.py --count 12 --seed 42 --out /tmp/_132.md
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path


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


def gen_parallel_axis(rng: random.Random) -> Problem:
    mass = round(rng.uniform(1.0, 8.0), 1)
    I_cm = round(rng.uniform(0.01, 0.5), 3)
    d = round(rng.uniform(0.1, 0.8), 2)
    I_total = I_cm + mass * d**2

    stmt = (
        f"A body segment has mass $m = {mass}$ kg, $I_{{\\text{{cm}}}} = {I_cm}$ kg·m², "
        f"and its CM is $d = {d}$ m from the rotation axis.\n\n"
        "Compute the moment of inertia about the rotation axis using the parallel axis theorem."
    )
    sol = (
        f"$I = I_{{\\text{{cm}}}} + md^2 = {I_cm} + {mass} \\times {d}^2 = {I_cm} + {mass * d**2:.4f} = {I_total:.4f}$ kg·m²"
    )
    return Problem("Parallel axis theorem", stmt, sol)


def gen_conservation(rng: random.Random) -> Problem:
    I1 = round(rng.uniform(8, 16), 1)
    I2 = round(rng.uniform(2.5, 5.5), 1)
    omega1 = round(rng.uniform(2, 5), 1)
    L = I1 * omega1
    omega2 = L / I2

    stmt = (
        f"A rider with $I_{{\\text{{ext}}}} = {I1}$ kg·m² rotates at $\\omega_1 = {omega1}$ rad/s, "
        f"then tucks to $I_{{\\text{{tuck}}}} = {I2}$ kg·m².\n\n"
        "Find the new angular velocity and the ratio $\\omega_2/\\omega_1$."
    )
    sol = (
        f"$L = I_1\\omega_1 = {I1} \\times {omega1} = {L:.2f}$ kg·m²/s\n\n"
        f"$\\omega_2 = L/I_2 = {L:.2f}/{I2} = {omega2:.3f}$ rad/s\n\n"
        f"Ratio: $\\omega_2/\\omega_1 = {I1}/{I2} = {I1/I2:.2f}$"
    )
    return Problem("Angular momentum conservation", stmt, sol)


def gen_takeoff_requirements(rng: random.Random) -> Problem:
    n_rot = rng.choice([1, 1.5, 2])
    T = round(rng.uniform(0.6, 1.4), 2)
    I_ext = round(rng.uniform(9, 14), 1)
    I_tuck = round(rng.uniform(3, 5), 1)
    tuck_frac = round(rng.uniform(0.6, 0.85), 2)

    t_tuck = tuck_frac * T
    t_ext = T - t_tuck
    ratio = I_tuck / I_ext
    # omega_tuck * t_tuck + ratio*omega_tuck * t_ext = 2*pi*n
    denom = t_tuck + ratio * t_ext
    omega_tuck = 2 * math.pi * n_rot / denom
    L = I_tuck * omega_tuck
    omega_takeoff = L / I_ext

    stmt = (
        f"A rider needs {n_rot} rotation(s) in $T = {T}$ s airtime. "
        f"$I_{{\\text{{ext}}}} = {I_ext}$, $I_{{\\text{{tuck}}}} = {I_tuck}$ kg·m². "
        f"Tuck fraction: {tuck_frac}.\n\n"
        "Find: required $L$, $\\omega_{{\\text{{takeoff}}}}$, and average takeoff torque (contact = 0.15 s)."
    )
    sol = (
        f"$t_{{\\text{{tuck}}}} = {tuck_frac} \\times {T} = {t_tuck:.3f}$ s, "
        f"$t_{{\\text{{ext}}}} = {t_ext:.3f}$ s\n\n"
        f"$\\omega_{{\\text{{tuck}}}} = \\frac{{2\\pi \\times {n_rot}}}{{{t_tuck:.3f} + ({I_tuck}/{I_ext}) \\times {t_ext:.3f}}} = {omega_tuck:.3f}$ rad/s\n\n"
        f"$L = {I_tuck} \\times {omega_tuck:.3f} = {L:.2f}$ kg·m²/s\n\n"
        f"$\\omega_{{\\text{{takeoff}}}} = {L:.2f}/{I_ext} = {omega_takeoff:.3f}$ rad/s\n\n"
        f"$\\bar\\tau = {L:.2f}/0.15 = {L/0.15:.1f}$ N·m"
    )
    return Problem("Takeoff requirements for n rotations", stmt, sol)


def gen_energy_cost(rng: random.Random) -> Problem:
    L = round(rng.uniform(25, 50), 1)
    I_ext = round(rng.uniform(9, 14), 1)
    I_tuck = round(rng.uniform(3, 5), 1)

    T_ext = L**2 / (2 * I_ext)
    T_tuck = L**2 / (2 * I_tuck)
    W = T_tuck - T_ext

    stmt = (
        f"A rider has $L = {L}$ kg·m²/s. They transition from $I = {I_ext}$ to $I = {I_tuck}$ kg·m².\n\n"
        "Compute rotational KE before and after, and the muscular work required."
    )
    sol = (
        f"$T_{{\\text{{ext}}}} = L^2/(2I_{{\\text{{ext}}}}) = {L}^2/(2 \\times {I_ext}) = {T_ext:.2f}$ J\n\n"
        f"$T_{{\\text{{tuck}}}} = L^2/(2I_{{\\text{{tuck}}}}) = {L}^2/(2 \\times {I_tuck}) = {T_tuck:.2f}$ J\n\n"
        f"$W = {T_tuck:.2f} - {T_ext:.2f} = {W:.2f}$ J"
    )
    return Problem("Energy cost of tucking", stmt, sol)


def gen_composite_moi(rng: random.Random) -> Problem:
    n_seg = rng.randint(3, 5)
    segments = []
    total = 0.0
    for i in range(n_seg):
        m = round(rng.uniform(2, 20), 1)
        Icm = round(rng.uniform(0.01, 0.5), 3)
        d = round(rng.uniform(0.05, 0.7), 2)
        I_seg = Icm + m * d**2
        segments.append((m, Icm, d, I_seg))
        total += I_seg

    table = "| Segment | m (kg) | I_cm (kg·m²) | d (m) |\n|:---|:---|:---|:---|\n"
    for i, (m, Icm, d, _) in enumerate(segments):
        table += f"| Seg {i+1} | {m} | {Icm} | {d} |\n"

    sol_lines = "Using $I_i = I_{{cm,i}} + m_i d_i^2$:\n\n"
    for i, (m, Icm, d, I_seg) in enumerate(segments):
        sol_lines += f"Seg {i+1}: ${Icm} + {m}\\times{d}^2 = {I_seg:.4f}$ kg·m²\n\n"
    sol_lines += f"**Total:** $I = {total:.4f}$ kg·m²"

    stmt = f"Compute the total MOI for this composite body:\n\n{table}"
    return Problem("Composite body MOI", stmt, sol_lines)


GENERATORS = [gen_parallel_axis, gen_conservation, gen_takeoff_requirements, gen_energy_cost, gen_composite_moi]


def main():
    parser = argparse.ArgumentParser(description="13.2 BMX Dynamics practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/biomech, rotational-dynamics, practice]\ndate: 2026-05-23\n---\n\n"
        "# 13.2 BMX Rotational Dynamics — Practice Problems\n\n#review/biomech\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

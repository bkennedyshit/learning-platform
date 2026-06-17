#!/usr/bin/env python3
"""
3.7_heat_wave_pdes.py — Practice problem generator for Chapter 3.7
(The Heat & Wave PDEs: Separation of Variables).

Archetypes:
  1. Heat equation with given Fourier IC
  2. Heat equation requiring coefficient computation
  3. Wave equation (standing wave)
  4. d'Alembert solution
  5. Classify PDE type

Usage:
  python 3.7_heat_wave_pdes.py --count 8
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import sympy as sp


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


def gen_heat_simple(rng: random.Random) -> Problem:
    alpha2 = rng.choice([1, 2, 4])
    n1 = rng.randint(1, 3)
    n2 = rng.randint(n1 + 1, n1 + 3)
    a = rng.randint(1, 5)
    b = rng.randint(-5, -1)
    stmt = (
        f"Solve: $u_t = {alpha2}u_{{xx}}$, $u(0,t)=u(\\pi,t)=0$, "
        f"$u(x,0) = {a}\\sin {n1}x + ({b})\\sin {n2}x$."
    )
    sol = (
        f"Eigenvalues $\\lambda_n = n^2$. Solution:\n\n"
        f"$$\nu(x,t) = {a}e^{{-{alpha2*n1**2}t}}\\sin {n1}x + ({b})e^{{-{alpha2*n2**2}t}}\\sin {n2}x\n$$"
    )
    return Problem("Heat equation (Fourier IC)", stmt, sol)


def gen_heat_compute(rng: random.Random) -> Problem:
    stmt = (
        "Solve: $u_t = u_{xx}$, $u(0,t)=u(1,t)=0$, $u(x,0) = x(1-x)$.\n\n"
        "Compute the first two nonzero Fourier sine coefficients."
    )
    sol = (
        "$B_n = 2\\int_0^1 x(1-x)\\sin(n\\pi x)\\,dx$.\n\n"
        "Integration by parts (twice):\n\n"
        "$B_n = \\frac{4}{n^3\\pi^3}[1-(-1)^n]$.\n\n"
        "$B_n = 0$ for even $n$; $B_n = \\frac{8}{n^3\\pi^3}$ for odd $n$.\n\n"
        "$B_1 = 8/\\pi^3 \\approx 0.258$, $B_3 = 8/(27\\pi^3) \\approx 0.0096$.\n\n"
        "$$\nu(x,t) \\approx \\frac{8}{\\pi^3}e^{-\\pi^2 t}\\sin(\\pi x) + \\frac{8}{27\\pi^3}e^{-9\\pi^2 t}\\sin(3\\pi x) + \\cdots\n$$"
    )
    return Problem("Heat equation (compute coefficients)", stmt, sol)


def gen_wave(rng: random.Random) -> Problem:
    c = rng.randint(1, 4)
    n = rng.randint(1, 3)
    A = rng.randint(1, 5)
    stmt = (
        f"Solve: $u_{{tt}} = {c**2}u_{{xx}}$, $u(0,t)=u(\\pi,t)=0$, "
        f"$u(x,0) = {A}\\sin {n}x$, $u_t(x,0) = 0$."
    )
    sol = (
        f"$c = {c}$, $L = \\pi$. Since $u_t(x,0)=0$, all $B_n = 0$.\n\n"
        f"$A_{n} = {A}$ (matching IC), all others zero.\n\n"
        f"$$\nu(x,t) = {A}\\cos({c*n}t)\\sin({n}x)\n$$"
    )
    return Problem("Wave equation (standing wave)", stmt, sol)


def gen_dalembert(rng: random.Random) -> Problem:
    c = rng.randint(1, 4)
    stmt = (
        f"Use d'Alembert's formula for $u_{{tt}} = {c**2}u_{{xx}}$, "
        f"$u(x,0) = \\cos x$, $u_t(x,0) = 0$, $x \\in \\mathbb{{R}}$."
    )
    sol = (
        f"$g(x) = 0$, so:\n\n"
        f"$$\nu(x,t) = \\frac{{1}}{{2}}[\\cos(x+{c}t) + \\cos(x-{c}t)]\n$$\n\n"
        f"By sum-to-product: $u = \\cos x\\cos({c}t)$."
    )
    return Problem("d'Alembert solution", stmt, sol)


def gen_classify_pde(rng: random.Random) -> Problem:
    cases = [
        ("u_t = 3u_{xx}", "parabolic (heat-type)", "B²−AC = 0"),
        ("u_{tt} = 5u_{xx}", "hyperbolic (wave-type)", "B²−AC > 0"),
        ("u_{xx} + u_{yy} = 0", "elliptic (Laplace-type)", "B²−AC < 0"),
        ("u_{tt} - 4u_{xx} = 0", "hyperbolic (wave-type)", "B²−AC > 0"),
    ]
    eq, ptype, reason = rng.choice(cases)
    stmt = f"Classify the PDE: ${eq}$."
    sol = f"Discriminant: ${reason}$. This is **{ptype}**."
    return Problem("PDE classification", stmt, sol)


GENERATORS = [gen_heat_simple, gen_heat_compute, gen_wave, gen_dalembert, gen_classify_pde]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.7 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.7_heat_wave_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.7 Practice — Heat & Wave PDEs\n",
        f"Generated: {today} | Seed: {seed} | Count: {args.count}\n\n---\n",
    ]
    for idx, p in enumerate(problems, 1):
        lines.append(p.render(idx))
        lines.append("\n---\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Wrote {args.count} problems to {out_path}")


if __name__ == "__main__":
    main()

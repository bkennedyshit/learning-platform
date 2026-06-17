#!/usr/bin/env python3
"""
3.6_laplace.py — Practice problem generator for Chapter 3.6
(Laplace Transforms).

Archetypes:
  1. Compute Laplace transform from definition
  2. Inverse Laplace via partial fractions
  3. Solve IVP using Laplace
  4. s-shifting application
  5. Convolution integral

Usage:
  python 3.6_laplace.py --count 8
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


def gen_forward(rng: random.Random) -> Problem:
    a = rng.randint(-3, 3)
    n = rng.randint(0, 3)
    t = sp.Symbol('t', positive=True)
    s = sp.Symbol('s')
    f = t**n * sp.exp(a * t)
    F = sp.factorial(n) / (s - a)**(n + 1)
    stmt = f"Compute $\\mathcal{{L}}\\{{{sp.latex(f)}\\}}$."
    sol = (
        f"Using the formula $\\mathcal{{L}}\\{{t^n e^{{at}}\\}} = \\frac{{n!}}{{(s-a)^{{n+1}}}}$:\n\n"
        f"$$\n\\mathcal{{L}}\\{{{sp.latex(f)}\\}} = {sp.latex(F)}, \\quad s > {a}\n$$"
    )
    return Problem("Forward Laplace transform", stmt, sol)


def gen_inverse_pf(rng: random.Random) -> Problem:
    r1 = rng.randint(-4, -1)
    r2 = rng.randint(1, 4)
    s = sp.Symbol('s')
    # F(s) = 1/((s-r1)(s-r2))
    A = sp.Rational(1, r1 - r2)
    B = sp.Rational(1, r2 - r1)
    stmt = f"Find $\\mathcal{{L}}^{{-1}}\\left\\{{\\frac{{1}}{{(s-({r1}))(s-{r2})}}\\right\\}}$."
    sol = (
        f"Partial fractions: $\\frac{{1}}{{(s{'+' if -r1>0 else ''}{-r1})(s-{r2})}} = "
        f"\\frac{{{sp.latex(A)}}}{{s{'+' if -r1>0 else ''}{-r1}}} + \\frac{{{sp.latex(B)}}}{{s-{r2}}}$.\n\n"
        f"Invert: $f(t) = {sp.latex(A)}e^{{{r1}t}} + {sp.latex(B)}e^{{{r2}t}}$."
    )
    return Problem("Inverse Laplace (partial fractions)", stmt, sol)


def gen_ivp_laplace(rng: random.Random) -> Problem:
    # y'' + by' + cy = 0, y(0)=y0, y'(0)=yp0
    r1, r2 = -1, -2
    b = -(r1 + r2)  # 3
    c = r1 * r2  # 2
    y0 = rng.randint(1, 3)
    yp0 = rng.randint(-2, 2)
    stmt = (
        f"Solve via Laplace: $y'' + {b}y' + {c}y = 0$, $y(0)={y0}$, $y'(0)={yp0}$."
    )
    # (s^2+3s+2)Y = s*y0 + yp0 + b*y0
    num_const = y0
    rhs = f"{y0}s + {yp0 + b * y0}"
    # Y = (y0*s + yp0+b*y0)/((s+1)(s+2))
    # Partial fractions
    A = y0 * (-1) + yp0 + b * y0  # at s=-1: num/(s+2)|s=-1
    num_at_m1 = y0 * (-1) + (yp0 + b * y0)
    A_val = num_at_m1  # / ((-1)+2) = /1
    num_at_m2 = y0 * (-2) + (yp0 + b * y0)
    B_val = num_at_m2 / ((-2) + 1)  # / (-1)
    sol = (
        f"Transform: $(s^2+{b}s+{c})Y = {y0}s + {yp0+b*y0}$.\n\n"
        f"$Y = \\frac{{{y0}s+{yp0+b*y0}}}{{(s+1)(s+2)}}$.\n\n"
        f"Partial fractions → $y(t) = {A_val}e^{{-t}} + {-B_val}e^{{-2t}}$."
    )
    return Problem("IVP via Laplace", stmt, sol)


def gen_s_shift(rng: random.Random) -> Problem:
    a = rng.randint(1, 4)
    omega = rng.randint(1, 3)
    stmt = f"Compute $\\mathcal{{L}}\\{{e^{{{a}t}}\\sin {omega}t\\}}$."
    sol = (
        f"$s$-shifting: $\\mathcal{{L}}\\{{e^{{at}}f(t)\\}} = F(s-a)$.\n\n"
        f"$\\mathcal{{L}}\\{{\\sin {omega}t\\}} = \\frac{{{omega}}}{{s^2+{omega**2}}}$.\n\n"
        f"Replace $s \\to s-{a}$:\n\n"
        f"$$\n\\mathcal{{L}}\\{{e^{{{a}t}}\\sin {omega}t\\}} = \\frac{{{omega}}}{{(s-{a})^2+{omega**2}}}\n$$"
    )
    return Problem("s-shifting theorem", stmt, sol)


def gen_convolution(rng: random.Random) -> Problem:
    a = rng.randint(1, 3)
    b = rng.randint(a + 1, a + 3)
    stmt = (
        f"Use the convolution theorem to find $\\mathcal{{L}}^{{-1}}\\left\\{{\\frac{{1}}{{(s+{a})(s+{b})}}\\right\\}}$."
    )
    sol = (
        f"$F = 1/(s+{a})$, $G = 1/(s+{b})$, so $f = e^{{-{a}t}}$, $g = e^{{-{b}t}}$.\n\n"
        f"$(f*g)(t) = \\int_0^t e^{{-{a}\\tau}}e^{{-{b}(t-\\tau)}}d\\tau = e^{{-{b}t}}\\int_0^t e^{{{b-a}\\tau}}d\\tau$\n\n"
        f"$= e^{{-{b}t}}\\cdot\\frac{{e^{{{b-a}t}}-1}}{{{b-a}}} = \\frac{{e^{{-{a}t}}-e^{{-{b}t}}}}{{{b-a}}}$."
    )
    return Problem("Convolution theorem", stmt, sol)


GENERATORS = [gen_forward, gen_inverse_pf, gen_ivp_laplace, gen_s_shift, gen_convolution]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.6 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.6_laplace_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.6 Practice — Laplace Transforms\n",
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

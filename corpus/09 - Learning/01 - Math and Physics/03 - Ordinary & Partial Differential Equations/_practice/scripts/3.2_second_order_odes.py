#!/usr/bin/env python3
"""
3.2_second_order_odes.py — Practice problem generator for Chapter 3.2
(Second-Order Linear Homogeneous ODEs).

Archetypes:
  1. Distinct real roots
  2. Repeated root
  3. Complex conjugate roots
  4. IVP with complex roots
  5. Wronskian computation
  6. Classify damping type

Usage:
  python 3.2_second_order_odes.py
  python 3.2_second_order_odes.py --count 12 --seed 7
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


def gen_distinct_real(rng: random.Random) -> Problem:
    r1 = rng.randint(-5, -1)
    r2 = rng.randint(r1 + 1, 0) if r1 < -1 else rng.randint(-5, r1 - 1)
    if r1 == r2:
        r2 = r1 + 1
    # ay'' + by' + cy = 0 with a=1, b=-(r1+r2), c=r1*r2
    b = -(r1 + r2)
    c = r1 * r2
    stmt = f"Find the general solution of $y'' + {b}y' + {c}y = 0$."
    sol = (
        f"Characteristic equation: $r^2 + {b}r + {c} = 0$.\n\n"
        f"Roots: $r_1 = {r1}$, $r_2 = {r2}$.\n\n"
        f"General solution: $y = c_1 e^{{{r1}x}} + c_2 e^{{{r2}x}}$."
    )
    return Problem("Distinct real roots", stmt, sol)


def gen_repeated(rng: random.Random) -> Problem:
    r = rng.randint(-4, -1)
    b = -2 * r
    c = r * r
    stmt = f"Find the general solution of $y'' + {b}y' + {c}y = 0$."
    sol = (
        f"Characteristic equation: $r^2 + {b}r + {c} = (r + {-r})^2 = 0$.\n\n"
        f"Repeated root: $r = {r}$.\n\n"
        f"General solution: $y = (c_1 + c_2 x)e^{{{r}x}}$."
    )
    return Problem("Repeated root", stmt, sol)


def gen_complex(rng: random.Random) -> Problem:
    alpha = rng.randint(-3, -1)
    beta = rng.randint(1, 4)
    # r = alpha ± i*beta => r^2 - 2*alpha*r + (alpha^2+beta^2) = 0
    b = -2 * alpha
    c = alpha**2 + beta**2
    stmt = f"Find the general solution of $y'' + {b}y' + {c}y = 0$."
    sol = (
        f"Characteristic equation: $r^2 + {b}r + {c} = 0$.\n\n"
        f"$r = \\frac{{-{b} \\pm \\sqrt{{{b**2} - {4*c}}}}}{{2}} = {alpha} \\pm {beta}i$.\n\n"
        f"General solution: $y = e^{{{alpha}x}}(c_1\\cos {beta}x + c_2\\sin {beta}x)$."
    )
    return Problem("Complex conjugate roots", stmt, sol)


def gen_ivp_complex(rng: random.Random) -> Problem:
    alpha = rng.randint(-3, -1)
    beta = rng.randint(1, 3)
    y0 = rng.randint(1, 4)
    yp0 = rng.randint(-3, 3)
    b = -2 * alpha
    c = alpha**2 + beta**2
    # c1 = y0, c2 = (yp0 - alpha*y0)/beta
    c2 = sp.Rational(yp0 - alpha * y0, beta)
    stmt = (
        f"Solve the IVP: $y'' + {b}y' + {c}y = 0$, $y(0) = {y0}$, $y'(0) = {yp0}$."
    )
    sol = (
        f"Roots: $r = {alpha} \\pm {beta}i$.\n\n"
        f"$y = e^{{{alpha}x}}(c_1\\cos {beta}x + c_2\\sin {beta}x)$.\n\n"
        f"$y(0) = c_1 = {y0}$.\n\n"
        f"$y'(0) = {alpha}c_1 + {beta}c_2 = {yp0}$, so $c_2 = {sp.latex(c2)}$.\n\n"
        f"**Solution:** $y = e^{{{alpha}x}}({y0}\\cos {beta}x + {sp.latex(c2)}\\sin {beta}x)$."
    )
    return Problem("IVP (complex roots)", stmt, sol)


def gen_wronskian(rng: random.Random) -> Problem:
    r1 = rng.randint(-4, -1)
    r2 = rng.randint(r1 + 1, 2)
    if r1 == r2:
        r2 += 1
    stmt = (
        f"Compute the Wronskian of $y_1 = e^{{{r1}x}}$ and $y_2 = e^{{{r2}x}}$."
    )
    sol = (
        f"$W = \\begin{{vmatrix}} e^{{{r1}x}} & e^{{{r2}x}} \\\\ "
        f"{r1}e^{{{r1}x}} & {r2}e^{{{r2}x}} \\end{{vmatrix}}$\n\n"
        f"$= {r2}e^{{{r1+r2}x}} - {r1}e^{{{r1+r2}x}} = {r2-r1}e^{{{r1+r2}x}} \\neq 0$.\n\n"
        f"The solutions are linearly independent."
    )
    return Problem("Wronskian computation", stmt, sol)


def gen_classify(rng: random.Random) -> Problem:
    a = 1
    b = rng.randint(1, 6)
    c = rng.randint(1, 10)
    disc = b**2 - 4 * a * c
    if disc > 0:
        classification = "overdamped"
    elif disc == 0:
        classification = "critically damped"
    else:
        classification = "underdamped"
    stmt = (
        f"Classify the damping for $y'' + {b}y' + {c}y = 0$. "
        f"State the discriminant and type."
    )
    sol = (
        f"$\\Delta = b^2 - 4ac = {b}^2 - 4({a})({c}) = {b**2} - {4*c} = {disc}$.\n\n"
        f"Since $\\Delta {'> 0' if disc > 0 else '= 0' if disc == 0 else '< 0'}$, "
        f"the system is **{classification}**."
    )
    return Problem("Classify damping", stmt, sol)


GENERATORS = [
    gen_distinct_real, gen_repeated, gen_complex,
    gen_ivp_complex, gen_wronskian, gen_classify,
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.2 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.2_second_order_odes_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.2 Practice — Second-Order Linear Homogeneous ODEs\n",
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

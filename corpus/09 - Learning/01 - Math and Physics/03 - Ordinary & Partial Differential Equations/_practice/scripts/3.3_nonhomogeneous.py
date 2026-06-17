#!/usr/bin/env python3
"""
3.3_nonhomogeneous.py — Practice problem generator for Chapter 3.3
(Nonhomogeneous ODEs & Undetermined Coefficients).

Archetypes:
  1. Polynomial forcing
  2. Exponential forcing (no duplication)
  3. Exponential forcing with duplication (resonance)
  4. Trigonometric forcing
  5. Variation of parameters setup

Usage:
  python 3.3_nonhomogeneous.py --count 8 --seed 42
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


def gen_poly_forcing(rng: random.Random) -> Problem:
    r1, r2 = rng.randint(-3, -1), rng.randint(1, 3)
    b = -(r1 + r2)
    c = r1 * r2
    a_coeff = rng.randint(1, 4)
    stmt = f"Find $y_p$ for $y'' + {b}y' + {c}y = {a_coeff}x$."
    # yp = Ax + B; A*c = a_coeff => A = a_coeff/c; b*A + c*B = 0 => B = -bA/c
    x = sp.Symbol('x')
    A = sp.Rational(a_coeff, c)
    B = sp.Rational(-b * a_coeff, c**2)
    sol = (
        f"Guess $y_p = Ax + B$. Then $y_p'' = 0$, $y_p' = A$.\n\n"
        f"Substitute: ${b}A + {c}(Ax+B) = {a_coeff}x$.\n\n"
        f"$x$: ${c}A = {a_coeff}$, so $A = {sp.latex(A)}$.\n\n"
        f"$x^0$: ${b}A + {c}B = 0$, so $B = {sp.latex(B)}$.\n\n"
        f"$y_p = {sp.latex(A)}x + ({sp.latex(B)})$."
    )
    return Problem("Polynomial forcing", stmt, sol)


def gen_exp_forcing(rng: random.Random) -> Problem:
    r1, r2 = rng.randint(-4, -1), rng.randint(1, 3)
    alpha = rng.choice([i for i in range(-3, 4) if i != r1 and i != r2])
    b = -(r1 + r2)
    c = r1 * r2
    k = rng.randint(1, 5)
    denom = alpha**2 + b * alpha + c
    A = sp.Rational(k, denom)
    stmt = f"Find $y_p$ for $y'' + {b}y' + {c}y = {k}e^{{{alpha}x}}$."
    sol = (
        f"Guess $y_p = Ae^{{{alpha}x}}$.\n\n"
        f"Substitute: $A({alpha}^2 + {b}\\cdot{alpha} + {c})e^{{{alpha}x}} = {k}e^{{{alpha}x}}$.\n\n"
        f"$A({denom}) = {k}$, so $A = {sp.latex(A)}$.\n\n"
        f"$y_p = {sp.latex(A)}e^{{{alpha}x}}$."
    )
    return Problem("Exponential forcing", stmt, sol)


def gen_resonance(rng: random.Random) -> Problem:
    r = rng.randint(-3, -1)
    b = -2 * r
    c = r**2
    k = rng.randint(1, 4)
    # Repeated root r, forcing ke^{rx} => yp = A x^2 e^{rx}, 2A = k
    A = sp.Rational(k, 2)
    stmt = f"Find $y_p$ for $y'' + {b}y' + {c}y = {k}e^{{{r}x}}$."
    sol = (
        f"Characteristic roots: $r = {r}$ (repeated). Forcing duplicates homogeneous solution.\n\n"
        f"Multiply guess by $x^2$: $y_p = Ax^2 e^{{{r}x}}$.\n\n"
        f"After substitution: $2A = {k}$, so $A = {sp.latex(A)}$.\n\n"
        f"$y_p = {sp.latex(A)}x^2 e^{{{r}x}}$."
    )
    return Problem("Resonance (duplication)", stmt, sol)


def gen_trig_forcing(rng: random.Random) -> Problem:
    omega_n = rng.randint(1, 4)
    omega_f = rng.choice([i for i in range(1, 6) if i != omega_n])
    k = rng.randint(1, 5)
    c_val = omega_n**2
    denom = c_val - omega_f**2
    B = sp.Rational(k, denom)
    stmt = f"Find $y_p$ for $y'' + {c_val}y = {k}\\sin {omega_f}x$."
    sol = (
        f"Guess $y_p = A\\cos {omega_f}x + B\\sin {omega_f}x$.\n\n"
        f"$y_p'' = -{omega_f**2}A\\cos {omega_f}x - {omega_f**2}B\\sin {omega_f}x$.\n\n"
        f"Substitute: $(-{omega_f**2} + {c_val})A\\cos + (-{omega_f**2}+{c_val})B\\sin = {k}\\sin$.\n\n"
        f"${denom}A = 0 \\Rightarrow A = 0$; ${denom}B = {k} \\Rightarrow B = {sp.latex(B)}$.\n\n"
        f"$y_p = {sp.latex(B)}\\sin {omega_f}x$."
    )
    return Problem("Trigonometric forcing", stmt, sol)


def gen_vop_setup(rng: random.Random) -> Problem:
    omega = rng.randint(1, 3)
    stmt = (
        f"Set up (but do not fully integrate) the variation of parameters formulas for "
        f"$y'' + {omega**2}y = \\tan {omega}x$."
    )
    sol = (
        f"$y_1 = \\cos {omega}x$, $y_2 = \\sin {omega}x$, $W = {omega}$.\n\n"
        f"$u_1' = -\\dfrac{{\\sin {omega}x \\cdot \\tan {omega}x}}{{{omega}}} "
        f"= -\\dfrac{{\\sin^2 {omega}x}}{{{omega}\\cos {omega}x}}$.\n\n"
        f"$u_2' = \\dfrac{{\\cos {omega}x \\cdot \\tan {omega}x}}{{{omega}}} "
        f"= \\dfrac{{\\sin {omega}x}}{{{omega}}}$."
    )
    return Problem("Variation of parameters (setup)", stmt, sol)


GENERATORS = [gen_poly_forcing, gen_exp_forcing, gen_resonance, gen_trig_forcing, gen_vop_setup]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.3 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.3_nonhomogeneous_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.3 Practice — Nonhomogeneous ODEs\n",
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

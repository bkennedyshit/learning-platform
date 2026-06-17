#!/usr/bin/env python3
"""
3.8_nonlinear_pdes.py — Practice problem generator for Chapter 3.8
(Non-linear PDEs & Solitons).

Archetypes:
  1. Method of characteristics for inviscid Burgers
  2. Shock formation time
  3. Rankine-Hugoniot shock speed
  4. KdV soliton parameter identification
  5. Cole-Hopf transformation setup

Usage:
  python 3.8_nonlinear_pdes.py --count 8
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


def gen_characteristics(rng: random.Random) -> Problem:
    # u_t + u u_x = 0, u(x,0) = a - bx
    a = rng.randint(1, 4)
    b = rng.randint(1, 3)
    stmt = (
        f"Solve $u_t + uu_x = 0$ with $u(x,0) = {a} - {b}x$ using characteristics. "
        f"Find the shock formation time."
    )
    sol = (
        f"Characteristics: $x = \\xi + ({a}-{b}\\xi)t$.\n\n"
        f"Solve for $\\xi$: $\\xi = (x - {a}t)/(1 - {b}t)$.\n\n"
        f"$u(x,t) = {a} - {b}\\xi = ({a} - {b}x)/(1 - {b}t)$.\n\n"
        f"$f'(\\xi) = -{b}$, so $t_s = 1/{b}$.\n\n"
        f"Shock forms at $t = {sp.latex(sp.Rational(1, b))}$."
    )
    return Problem("Method of characteristics", stmt, sol)


def gen_shock_time(rng: random.Random) -> Problem:
    # u(x,0) = -a*sin(x), f'(x) = -a*cos(x), min = -a at x=0
    a = rng.randint(1, 5)
    stmt = (
        f"For $u_t + uu_x = 0$ with $u(x,0) = -{a}\\sin x$, find the shock formation time."
    )
    sol = (
        f"$f'(x) = -{a}\\cos x$. Minimum of $f'$ is $-{a}$ (at $x = 0$).\n\n"
        f"$t_s = -1/\\min f' = -1/(-{a}) = {sp.latex(sp.Rational(1, a))}$."
    )
    return Problem("Shock formation time", stmt, sol)


def gen_rankine_hugoniot(rng: random.Random) -> Problem:
    uL = rng.randint(2, 6)
    uR = rng.randint(0, uL - 1)
    # f(u) = u^2/2 for Burgers
    fL = sp.Rational(uL**2, 2)
    fR = sp.Rational(uR**2, 2)
    s = sp.Rational(uL**2 - uR**2, 2 * (uL - uR))
    stmt = (
        f"A shock in Burgers' equation has $u_L = {uL}$ and $u_R = {uR}$. "
        f"Find the shock speed using Rankine-Hugoniot."
    )
    sol = (
        f"$f(u) = u^2/2$. $f(u_L) = {sp.latex(fL)}$, $f(u_R) = {sp.latex(fR)}$.\n\n"
        f"$s = \\frac{{f(u_R) - f(u_L)}}{{u_R - u_L}} = \\frac{{{sp.latex(fR)} - {sp.latex(fL)}}}{{{uR} - {uL}}} = {sp.latex(s)}$.\n\n"
        f"(Equivalently, $s = (u_L + u_R)/2 = {sp.latex(sp.Rational(uL+uR, 2))}$.)"
    )
    return Problem("Rankine-Hugoniot shock speed", stmt, sol)


def gen_kdv_soliton(rng: random.Random) -> Problem:
    c = rng.choice([1, 2, 4, 8])
    amp = sp.Rational(c, 2)
    width = sp.sqrt(c) / 2
    stmt = (
        f"A KdV soliton travels at speed $c = {c}$. "
        f"State its amplitude and width parameter."
    )
    sol = (
        f"$u(x,t) = \\frac{{c}}{{2}}\\text{{sech}}^2\\left(\\frac{{\\sqrt{{c}}}}{{2}}(x - ct)\\right)$.\n\n"
        f"Amplitude: $c/2 = {sp.latex(amp)}$.\n\n"
        f"Width parameter: $\\sqrt{{c}}/2 = {sp.latex(width)}$.\n\n"
        f"Taller solitons are narrower and faster."
    )
    return Problem("KdV soliton parameters", stmt, sol)


def gen_cole_hopf(rng: random.Random) -> Problem:
    nu = rng.choice([1, 2])
    stmt = (
        f"State the Cole-Hopf transformation for $u_t + uu_x = {nu}u_{{xx}}$ "
        f"and the resulting equation for $\\phi$."
    )
    sol = (
        f"Substitution: $u = -{2*nu}\\dfrac{{\\phi_x}}{{\\phi}}$.\n\n"
        f"This transforms Burgers' equation into the heat equation:\n\n"
        f"$$\n\\phi_t = {nu}\\phi_{{xx}}\n$$\n\n"
        f"Solve the linear heat equation for $\\phi$, then recover $u$."
    )
    return Problem("Cole-Hopf transformation", stmt, sol)


GENERATORS = [gen_characteristics, gen_shock_time, gen_rankine_hugoniot, gen_kdv_soliton, gen_cole_hopf]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.8 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.8_nonlinear_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.8 Practice — Non-linear PDEs & Solitons\n",
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

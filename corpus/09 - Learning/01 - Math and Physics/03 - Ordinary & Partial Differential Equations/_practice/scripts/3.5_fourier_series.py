#!/usr/bin/env python3
"""
3.5_fourier_series.py — Practice problem generator for Chapter 3.5
(Fourier Series & Boundary Value Problems).

Archetypes:
  1. Compute Fourier coefficients for simple functions
  2. Fourier sine series on [0, L]
  3. Fourier cosine series on [0, L]
  4. Parseval's theorem application
  5. Identify odd/even and predict zero coefficients

Usage:
  python 3.5_fourier_series.py --count 8
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


def gen_full_fourier(rng: random.Random) -> Problem:
    # f(x) = x on [-pi, pi]
    x = sp.Symbol('x')
    n = sp.Symbol('n', positive=True, integer=True)
    stmt = "Compute the Fourier series of $f(x) = x$ on $[-\\pi, \\pi]$."
    sol = (
        "$f$ is odd, so $a_n = 0$ for all $n \\geq 0$.\n\n"
        "$b_n = \\frac{1}{\\pi}\\int_{-\\pi}^{\\pi}x\\sin(nx)\\,dx = \\frac{2}{\\pi}\\int_0^{\\pi}x\\sin(nx)\\,dx$.\n\n"
        "Integration by parts: $u = x$, $dv = \\sin(nx)\\,dx$:\n\n"
        "$$\nb_n = \\frac{2}{\\pi}\\left[-\\frac{x\\cos(nx)}{n}\\Big|_0^\\pi + \\frac{1}{n}\\int_0^\\pi\\cos(nx)\\,dx\\right] = \\frac{2}{\\pi}\\cdot\\frac{-\\pi(-1)^n}{n} = \\frac{-2(-1)^n}{n}\n$$\n\n"
        "$$\nx = \\sum_{n=1}^{\\infty}\\frac{-2(-1)^n}{n}\\sin(nx) = 2\\left[\\sin x - \\frac{\\sin 2x}{2} + \\frac{\\sin 3x}{3} - \\cdots\\right]\n$$"
    )
    return Problem("Full Fourier series", stmt, sol)


def gen_sine_series(rng: random.Random) -> Problem:
    k = rng.randint(1, 3)
    stmt = f"Compute the Fourier sine series of $f(x) = {k}$ on $[0, \\pi]$."
    sol = (
        f"$b_n = \\frac{{2}}{{\\pi}}\\int_0^\\pi {k}\\sin(nx)\\,dx = \\frac{{{2*k}}}{{\\pi}}\\left[-\\frac{{\\cos(nx)}}{{n}}\\right]_0^\\pi$\n\n"
        f"$= \\frac{{{2*k}}}{{n\\pi}}[1 - (-1)^n]$.\n\n"
        f"$b_n = 0$ for even $n$; $b_n = \\frac{{{4*k}}}{{n\\pi}}$ for odd $n$.\n\n"
        f"$$\n{k} = \\frac{{{4*k}}}{{\\pi}}\\sum_{{k=0}}^{{\\infty}}\\frac{{\\sin((2k+1)x)}}{{2k+1}}\n$$"
    )
    return Problem("Fourier sine series", stmt, sol)


def gen_cosine_series(rng: random.Random) -> Problem:
    stmt = "Compute the Fourier cosine series of $f(x) = x^2$ on $[0, \\pi]$."
    sol = (
        "$a_0 = \\frac{2}{\\pi}\\int_0^\\pi x^2\\,dx = \\frac{2\\pi^2}{3}$.\n\n"
        "For $n \\geq 1$, integrate by parts twice:\n\n"
        "$a_n = \\frac{2}{\\pi}\\int_0^\\pi x^2\\cos(nx)\\,dx = \\frac{4(-1)^n}{n^2}$.\n\n"
        "$$\nx^2 = \\frac{\\pi^2}{3} + 4\\sum_{n=1}^{\\infty}\\frac{(-1)^n}{n^2}\\cos(nx)\n$$"
    )
    return Problem("Fourier cosine series", stmt, sol)


def gen_parseval(rng: random.Random) -> Problem:
    stmt = (
        "Using the Fourier series of $f(x) = x$ on $[-\\pi,\\pi]$, "
        "apply Parseval's theorem to evaluate $\\sum_{n=1}^{\\infty}\\frac{1}{n^2}$."
    )
    sol = (
        "$\\frac{1}{\\pi}\\int_{-\\pi}^{\\pi}x^2\\,dx = \\frac{2\\pi^2}{3}$.\n\n"
        "Parseval: $\\frac{2\\pi^2}{3} = \\sum_{n=1}^{\\infty}b_n^2 = \\sum_{n=1}^{\\infty}\\frac{4}{n^2}$.\n\n"
        "$\\sum_{n=1}^{\\infty}\\frac{1}{n^2} = \\frac{\\pi^2}{6}$. (Basel problem!)"
    )
    return Problem("Parseval's theorem", stmt, sol)


def gen_odd_even(rng: random.Random) -> Problem:
    funcs = [
        ("x^3", "odd", "$a_n = 0$ for all $n$"),
        ("x^2", "even", "$b_n = 0$ for all $n$"),
        ("|x|", "even", "$b_n = 0$ for all $n$"),
        ("x^3 - x", "odd", "$a_n = 0$ for all $n$"),
    ]
    f, parity, result = rng.choice(funcs)
    stmt = f"Is $f(x) = {f}$ on $[-\\pi,\\pi]$ odd or even? Which Fourier coefficients vanish?"
    sol = f"$f(-x) = {'−' if parity == 'odd' else ''}f(x)$, so $f$ is **{parity}**.\n\n{result}."
    return Problem("Odd/even classification", stmt, sol)


GENERATORS = [gen_full_fourier, gen_sine_series, gen_cosine_series, gen_parseval, gen_odd_even]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.5 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.5_fourier_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.5 Practice — Fourier Series & BVPs\n",
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

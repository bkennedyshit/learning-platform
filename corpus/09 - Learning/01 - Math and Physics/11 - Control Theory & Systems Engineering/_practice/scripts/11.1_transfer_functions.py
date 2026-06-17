#!/usr/bin/env python3
"""
11.1_transfer_functions.py — Practice problem generator for Chapter 11.1
(Laplace Transforms & Transfer Functions).

Archetypes:
  1. Compute Laplace transform from definition
  2. Inverse Laplace via partial fractions (distinct real poles)
  3. Inverse Laplace with complex conjugate poles
  4. Derive transfer function from ODE
  5. Identify poles/zeros and classify stability
  6. Final Value Theorem application

Usage:
  python 11.1_transfer_functions.py
  python 11.1_transfer_functions.py --count 12 --seed 42
  python 11.1_transfer_functions.py --count 12 --seed 42 --out /tmp/_111.md
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

s = sp.Symbol('s')
t = sp.Symbol('t', positive=True)

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_laplace_exp(rng: random.Random) -> Problem:
    a = rng.randint(1, 8)
    F = 1/(s + a)
    stmt = f"Compute $\\mathcal{{L}}\\{{e^{{-{a}t}}\\}}$ from the integral definition."
    sol = (f"$$\\int_0^\\infty e^{{-{a}t}}e^{{-st}}dt = \\int_0^\\infty e^{{-(s+{a})t}}dt "
           f"= \\left[\\frac{{e^{{-(s+{a})t}}}}{{-(s+{a})}}\\right]_0^\\infty = \\frac{{1}}{{s+{a}}}$$")
    return Problem("Laplace of exponential", stmt, sol)

def gen_partial_real(rng: random.Random) -> Problem:
    p1, p2 = sorted(rng.sample(range(1, 9), 2))
    K = rng.randint(1, 10)
    G = K / ((s + p1)*(s + p2))
    Y = G / s
    pf = sp.apart(Y, s)
    yt = sp.inverse_laplace_transform(Y, s, t)
    stmt = (f"Find $y(t) = \\mathcal{{L}}^{{-1}}\\left\\{{\\dfrac{{{K}}}{{s(s+{p1})(s+{p2})}}\\right\\}}$. "
            "Show all partial fraction steps.")
    A = sp.Rational(K, p1*p2)
    B_num = K
    B = sp.Rational(-K, p1*(p2-p1))
    C = sp.Rational(K, p2*(p2-p1))
    sol = (f"Partial fractions: ${sp.latex(pf)}$\n\n"
           f"Inverse transform: $y(t) = {sp.latex(yt)}$")
    return Problem("Inverse Laplace (distinct real poles)", stmt, sol)

def gen_tf_from_ode(rng: random.Random) -> Problem:
    m = rng.randint(1, 4)
    b = rng.randint(1, 8)
    k = rng.randint(1, 10)
    stmt = (f"Derive the transfer function $G(s)=X(s)/F(s)$ for the system "
            f"${m}\\ddot{{x}} + {b}\\dot{{x}} + {k}x = f(t)$ with zero ICs.")
    G = sp.Rational(1, 1) / (m*s**2 + b*s + k)
    disc = b**2 - 4*m*k
    pole_info = "real" if disc >= 0 else "complex conjugate"
    sol = (f"Apply Laplace: $({m}s^2 + {b}s + {k})X(s) = F(s)$\n\n"
           f"$$G(s) = \\frac{{1}}{{{m}s^2 + {b}s + {k}}}$$\n\n"
           f"Poles are {pole_info}: $s = \\frac{{-{b} \\pm \\sqrt{{{b**2}-{4*m*k}}}}}{{{2*m}}}$")
    return Problem("Transfer function from ODE", stmt, sol)

def gen_poles_stability(rng: random.Random) -> Problem:
    coeffs = [1, rng.randint(-3, 6), rng.randint(-5, 15), rng.randint(1, 20)]
    poly = sum(c * s**(3-i) for i, c in enumerate(coeffs))
    roots = sp.solve(poly, s)
    stable = all(sp.re(r) < 0 for r in roots)
    stmt = f"Find the poles of $G(s) = 1/({sp.latex(poly)})$ and classify stability."
    sol = (f"Poles: ${', '.join(sp.latex(r) for r in roots)}$\n\n"
           f"All poles in LHP: {'Yes' if stable else 'No'} → **{'Stable' if stable else 'Unstable'}**")
    return Problem("Poles and stability classification", stmt, sol)

def gen_fvt(rng: random.Random) -> Problem:
    K = rng.randint(2, 15)
    p1 = rng.randint(1, 5)
    p2 = rng.randint(p1+1, 9)
    Y = sp.Rational(K, 1) / (s * (s+p1) * (s+p2))
    fv = sp.limit(s * Y, s, 0)
    stmt = (f"Given $Y(s) = \\dfrac{{{K}}}{{s(s+{p1})(s+{p2})}}$, "
            "find $y(\\infty)$ using the Final Value Theorem.")
    sol = (f"$y(\\infty) = \\lim_{{s\\to 0}} sY(s) = \\lim_{{s\\to 0}} "
           f"\\frac{{{K}}}{{(s+{p1})(s+{p2})}} = \\frac{{{K}}}{{{p1*p2}}} = {fv}$")
    return Problem("Final Value Theorem", stmt, sol)

GENERATORS = [gen_laplace_exp, gen_partial_real, gen_tf_from_ode, gen_poles_stability, gen_fvt]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.1 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, laplace, transfer-function]\n"
              "type: practice\n---\n# 11.1 Practice — Laplace Transforms & Transfer Functions\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(output)} bytes to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

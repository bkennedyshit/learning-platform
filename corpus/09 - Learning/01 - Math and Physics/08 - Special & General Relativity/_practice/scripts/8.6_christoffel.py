#!/usr/bin/env python3
"""
8.6_christoffel.py — Practice problems for Chapter 8.6
(Covariant Derivative & Christoffel Symbols).

Archetypes:
  1. Christoffel symbols for 2-sphere
  2. Christoffel symbols for diagonal metric
  3. Covariant derivative of a vector
  4. Parallel transport equation setup
  5. Covariant divergence computation
  6. Geodesic equation for given metric

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, simplify, sin, cos, cot, symbols, Function

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_sphere_christoffel(rng: random.Random) -> Problem:
    R = Rational(rng.choice([1,2,3,5]),1)
    stmt = (f"Compute all non-zero Christoffel symbols for the sphere of radius $R={latex(R)}$: "
            f"$ds^2 = {latex(R**2)}(d\\theta^2 + \\sin^2\\theta\\,d\\phi^2)$.")
    sol = (f"$\\Gamma^\\theta_{{\\phi\\phi}} = -\\sin\\theta\\cos\\theta$\n\n"
           f"$\\Gamma^\\phi_{{\\theta\\phi}} = \\Gamma^\\phi_{{\\phi\\theta}} = \\cot\\theta$\n\n"
           f"All others = 0. (Note: $R$ cancels in the Christoffel symbols for a sphere.)")
    return Problem("Christoffel Symbols (Sphere)", stmt, sol)

def gen_diagonal_christoffel(rng: random.Random) -> Problem:
    # 2D metric ds^2 = e^{2x}dx^2 + e^{2x}dy^2
    stmt = ("Compute Christoffel symbols for $ds^2 = e^{2x}(dx^2 + dy^2)$.")
    sol = ("$g_{11} = g_{22} = e^{2x}$, $g^{11} = g^{22} = e^{-2x}$\n\n"
           "$\\Gamma^1_{11} = \\frac{1}{2}g^{11}\\partial_1 g_{11} = \\frac{1}{2}e^{-2x}(2e^{2x}) = 1$\n\n"
           "$\\Gamma^1_{22} = -\\frac{1}{2}g^{11}\\partial_1 g_{22} = -1$\n\n"
           "$\\Gamma^2_{12} = \\Gamma^2_{21} = \\frac{1}{2}g^{22}\\partial_1 g_{22} = 1$\n\n"
           "All others = 0.")
    return Problem("Christoffel Symbols (Conformal Flat)", stmt, sol)

def gen_covariant_div(rng: random.Random) -> Problem:
    stmt = ("For a vector $V^\\mu = (0, f(r), 0, 0)$ in Schwarzschild spacetime, "
            "compute $\\nabla_\\mu V^\\mu$ using $\\nabla_\\mu V^\\mu = \\frac{1}{\\sqrt{-g}}\\partial_\\mu(\\sqrt{-g}V^\\mu)$.")
    sol = ("$\\sqrt{-g} = cr^2\\sin\\theta$ for Schwarzschild.\n\n"
           "$\\nabla_\\mu V^\\mu = \\frac{1}{r^2}\\partial_r(r^2 f(r)) = \\frac{2f}{r} + f'(r)$")
    return Problem("Covariant Divergence", stmt, sol)

def gen_geodesic_eq(rng: random.Random) -> Problem:
    stmt = ("Write the geodesic equations for the metric $ds^2 = -dt^2 + a(t)^2 dx^2$ (1+1 FLRW). "
            "Identify the conserved quantity.")
    sol = ("Christoffel: $\\Gamma^0_{11} = a\\dot{a}$, $\\Gamma^1_{01} = \\dot{a}/a$.\n\n"
           "$\\ddot{t} + a\\dot{a}\\dot{x}^2 = 0$\n\n"
           "$\\ddot{x} + 2(\\dot{a}/a)\\dot{t}\\dot{x} = 0$\n\n"
           "Conserved: $p_x = a^2 \\dot{x}$ (since $\\partial_x g_{\\mu\\nu} = 0$).")
    return Problem("Geodesic Equation (FLRW 1+1)", stmt, sol)

GENERATORS = [gen_sphere_christoffel, gen_diagonal_christoffel, gen_covariant_div, gen_geodesic_eq]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, christoffel, covariant-derivative]\nseed: {seed}\n---\n\n# 8.6 Practice — Christoffel Symbols\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

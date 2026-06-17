#!/usr/bin/env python3
"""
8.5_manifolds_metrics.py — Practice problems for Chapter 8.5
(Differential Geometry: Manifolds & Metrics).

Archetypes:
  1. Compute metric determinant and inverse
  2. Proper distance in Schwarzschild
  3. Proper time for static observer
  4. Coordinate transformation of metric
  5. Line element on surfaces (sphere, torus)
  6. Killing vector identification

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, simplify, sqrt, sin, cos, Matrix, symbols

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_metric_inverse(rng: random.Random) -> Problem:
    r = sp.Symbol('r', positive=True)
    rs = sp.Symbol('r_s', positive=True)
    f = 1 - rs/r
    g00 = -f
    g11 = 1/f
    g22 = r**2
    det_g = g00 * g11 * g22
    stmt = "For the 2+1 Schwarzschild metric $ds^2 = -f\\,dt^2 + f^{-1}dr^2 + r^2 d\\phi^2$, compute $\\det(g)$ and $g^{\\mu\\nu}$."
    sol = (f"$g_{{\\mu\\nu}} = \\text{{diag}}(-f, 1/f, r^2)$ where $f = 1-r_s/r$\n\n"
           f"$\\det(g) = (-f)(1/f)(r^2) = -r^2$\n\n"
           f"$g^{{\\mu\\nu}} = \\text{{diag}}(-1/f, f, 1/r^2)$")
    return Problem("Metric Inverse & Determinant", stmt, sol)

def gen_proper_distance(rng: random.Random) -> Problem:
    r1 = Rational(rng.choice([3,4,5,6]),1)
    r2 = Rational(rng.choice([8,10,15,20]),1)
    stmt = (f"In Schwarzschild spacetime ($r_s = 2$), compute the proper radial distance "
            f"from $r = {latex(r1)}r_s$ to $r = {latex(r2)}r_s$ (set up the integral).")
    sol = (f"$\\ell = \\int_{{{latex(r1)}r_s}}^{{{latex(r2)}r_s}} \\frac{{dr}}{{\\sqrt{{1-r_s/r}}}}$\n\n"
           f"This exceeds the coordinate distance ${latex(r2-r1)}r_s$ due to spatial curvature.")
    return Problem("Proper Radial Distance", stmt, sol)

def gen_proper_time_static(rng: random.Random) -> Problem:
    r_over_rs = Rational(rng.choice([2,3,5,10]),1)
    factor = simplify(sqrt(1 - 1/r_over_rs))
    stmt = f"A static observer at $r = {latex(r_over_rs)}r_s$ in Schwarzschild. Find $d\\tau/dt$."
    sol = (f"$d\\tau = \\sqrt{{1-r_s/r}}\\,dt = \\sqrt{{1-1/{latex(r_over_rs)}}}\\,dt = {latex(factor)}\\,dt$\n\n"
           f"Clock runs at {latex(simplify(factor*100))}% of coordinate time rate.")
    return Problem("Static Observer Proper Time", stmt, sol)

def gen_sphere_metric(rng: random.Random) -> Problem:
    R = Rational(rng.choice([1,2,5,10]),1)
    theta0 = sp.Symbol('theta_0')
    circumference = simplify(2*sp.pi*R)
    stmt = f"On a sphere of radius $R = {latex(R)}$, compute the circumference of the equator and the area."
    sol = (f"Metric: $ds^2 = {latex(R**2)}(d\\theta^2 + \\sin^2\\theta\\,d\\phi^2)$\n\n"
           f"Equatorial circumference ($\\theta=\\pi/2$): $C = \\int_0^{{2\\pi}} {latex(R)}\\,d\\phi = {latex(circumference)}$\n\n"
           f"Area: $A = \\int_0^\\pi\\int_0^{{2\\pi}} {latex(R**2)}\\sin\\theta\\,d\\theta\\,d\\phi = {latex(4*sp.pi*R**2)}$")
    return Problem("Sphere Metric Geometry", stmt, sol)

GENERATORS = [gen_metric_inverse, gen_proper_distance, gen_proper_time_static, gen_sphere_metric]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, manifolds, metrics]\nseed: {seed}\n---\n\n# 8.5 Practice — Manifolds & Metrics\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

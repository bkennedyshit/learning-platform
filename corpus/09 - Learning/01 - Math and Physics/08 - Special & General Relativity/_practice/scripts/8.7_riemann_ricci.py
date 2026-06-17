#!/usr/bin/env python3
"""
8.7_riemann_ricci.py — Practice problems for Chapter 8.7
(Geodesics & Curvature: Riemann & Ricci Tensors).

Archetypes:
  1. Riemann tensor for 2-sphere
  2. Ricci scalar computation
  3. Kretschner scalar for Schwarzschild
  4. Geodesic deviation (tidal acceleration)
  5. Independent components counting
  6. Bianchi identity verification

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, simplify, sqrt

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_sphere_riemann(rng: random.Random) -> Problem:
    a = Rational(rng.choice([1,2,3,5,10]),1)
    R_scalar = simplify(2/a**2)
    stmt = f"Compute the Ricci scalar $R$ for a sphere of radius $a = {latex(a)}$."
    sol = (f"$R^\\theta_{{\\phi\\theta\\phi}} = \\sin^2\\theta$, $R_{{\\theta\\phi\\theta\\phi}} = {latex(a**2)}\\sin^2\\theta$\n\n"
           f"$R_{{\\theta\\theta}} = 1$, $R_{{\\phi\\phi}} = \\sin^2\\theta$\n\n"
           f"$R = g^{{\\theta\\theta}}R_{{\\theta\\theta}} + g^{{\\phi\\phi}}R_{{\\phi\\phi}} = "
           f"1/{latex(a**2)} + 1/{latex(a**2)} = {latex(R_scalar)}$")
    return Problem("Ricci Scalar (Sphere)", stmt, sol)

def gen_kretschner(rng: random.Random) -> Problem:
    r_over_rs = Rational(rng.choice([2,3,5,10]),1)
    K = simplify(12 / r_over_rs**6)
    stmt = f"Compute the Kretschner scalar $K = R_{{\\mu\\nu\\alpha\\beta}}R^{{\\mu\\nu\\alpha\\beta}}$ at $r = {latex(r_over_rs)}r_s$."
    sol = (f"$K = 12r_s^2/r^6 = 12/({latex(r_over_rs)}r_s)^6 \\times r_s^2 = 12/{latex(r_over_rs**6)} \\cdot r_s^{{-4}}$\n\n"
           f"$K = {latex(K)}/r_s^4$ (finite → not a true singularity)")
    return Problem("Kretschner Scalar", stmt, sol)

def gen_tidal(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1,5,10]),1)
    r_mult = Rational(rng.choice([10,100,1000]),1)
    # Tidal accel ~ 2GM/r^3 per meter
    stmt = (f"Two particles separated by 1 m fall radially toward a mass ${latex(M_mult)}M_\\odot$ "
            f"at distance $r = {latex(r_mult)}$ km. Estimate tidal acceleration.")
    sol = (f"$a_{{tidal}} = 2GM/(r^3) \\times \\xi$\n\n"
           f"$= 2 \\times 6.674\\times10^{{-11}} \\times {latex(M_mult)} \\times 1.989\\times10^{{30}} / "
           f"({latex(r_mult)} \\times 10^3)^3$\n\n"
           f"Compute numerically for the given values.")
    return Problem("Tidal Acceleration", stmt, sol)

def gen_components(rng: random.Random) -> Problem:
    n = rng.choice([2,3,4,5,6])
    N = n**2 * (n**2 - 1) // 12
    stmt = f"How many independent components does the Riemann tensor have in $n = {n}$ dimensions?"
    sol = f"$N = n^2(n^2-1)/12 = {n}^2({n**2}-1)/12 = {n**2}\\times{n**2-1}/12 = {N}$"
    return Problem("Riemann Tensor Components", stmt, sol)

GENERATORS = [gen_sphere_riemann, gen_kretschner, gen_tidal, gen_components]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, riemann-tensor, curvature]\nseed: {seed}\n---\n\n# 8.7 Practice — Riemann & Ricci Tensors\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.7_relativistic_em.py — Practice problem generator for Chapter 7.7
(Relativistic Electrodynamics & Four-Vectors).

Archetypes:
  1. Lorentz transformation of E and B fields
  2. Four-vector construction (current, potential)
  3. Lorentz invariant computation
  4. Relativistic Doppler / wave four-vector

Usage: python 7.7_relativistic_em.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, sqrt, symbols

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_field_transform(rng: random.Random) -> Problem:
    beta = Rational(rng.randint(1, 9), 10)
    gamma = 1 / sqrt(1 - beta**2)
    Ey = rng.randint(100, 1000)
    Bz = Rational(rng.randint(1, 5), 1000000)
    Ey_prime = gamma * (Ey - beta * sp.Symbol('c') * Bz)
    stmt = (f"A frame $S'$ moves at $\\beta = {latex(beta)}$ along $x$. In $S$: $E_y = {Ey}$ V/m, "
            f"$B_z = {latex(Bz)}$ T. Find $E'_y$.")
    sol = (f"$\\gamma = 1/\\sqrt{{1-\\beta^2}} = {latex(gamma)}$\n\n"
           f"$E'_y = \\gamma(E_y - vB_z) = {latex(gamma)}({Ey} - {latex(beta)}c \\cdot {latex(Bz)})$\n\n"
           f"$= {latex(gamma)}({Ey} - {latex(beta *(3e8)* float(Bz)):.1f})$ V/m")
    return Problem("Lorentz transformation of E-field", stmt, sol)

def gen_four_current(rng: random.Random) -> Problem:
    rho = rng.randint(1, 9) * sp.Integer(10)**(-6)
    vx = Rational(rng.randint(1, 9), 10) * sp.Symbol('c')
    stmt = (f"A charge distribution has $\\rho = {latex(rho)}$ C/m³ and moves at $v_x = {latex(vx)}$. "
            "Write the four-current $J^\\mu$.")
    sol = (f"$J^\\mu = (c\\rho, \\rho v_x, 0, 0) = (c\\cdot{latex(rho)},\\; {latex(rho)}\\cdot{latex(vx)},\\; 0,\\; 0)$")
    return Problem("Four-current construction", stmt, sol)

def gen_invariant(rng: random.Random) -> Problem:
    Ex = rng.randint(100, 500)
    Ey = rng.randint(100, 500)
    Bz = Rational(rng.randint(1, 5), 1000)
    E2 = Ex**2 + Ey**2
    c2B2 = (3e8)**2 * float(Bz)**2
    inv = E2 - c2B2
    stmt = (f"Given $E_x = {Ex}$ V/m, $E_y = {Ey}$ V/m, $B_z = {latex(Bz)}$ T (all others zero). "
            "Compute the Lorentz invariant $E^2 - c^2B^2$.")
    sol = (f"$E^2 = {Ex}^2 + {Ey}^2 = {E2}$ (V/m)²\n\n"
           f"$c^2B^2 = (3\\times10^8)^2({latex(Bz)})^2 = {c2B2:.2e}$ (V/m)²\n\n"
           f"$E^2 - c^2B^2 = {inv:.2e}$ (V/m)²\n\n"
           "This value is the same in all inertial frames.")
    return Problem("Lorentz invariant computation", stmt, sol)

def gen_doppler(rng: random.Random) -> Problem:
    beta = Rational(rng.randint(1, 8), 10)
    f0 = rng.choice([1e9, 5e14, 1e15])
    gamma = 1 / sqrt(1 - beta**2)
    f_obs = f0 * float(gamma) * (1 - float(beta))  # receding source
    stmt = (f"A source emitting at $f_0 = {f0:.2e}$ Hz recedes at $\\beta = {latex(beta)}$. "
            "Find the observed frequency (relativistic Doppler).")
    sol = (f"$$f_{{\\text{{obs}}}} = f_0\\sqrt{{\\frac{{1-\\beta}}{{1+\\beta}}}} = "
           f"{f0:.2e}\\sqrt{{\\frac{{1-{latex(beta)}}}{{1+{latex(beta)}}}}}$$\n\n"
           f"$$= {f_obs:.4e} \\text{{ Hz}}$$")
    return Problem("Relativistic Doppler effect", stmt, sol)

GENERATORS = [gen_field_transform, gen_four_current, gen_invariant, gen_doppler]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, relativistic-em, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.7 Relativistic Electrodynamics — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.3_magnetostatics.py — Practice problem generator for Chapter 7.3
(Magnetostatics: Biot-Savart & Ampère's Law).

Archetypes:
  1. Biot-Savart for straight wire segment
  2. Ampère's Law (solenoid/toroid)
  3. Force between parallel wires
  4. Magnetic dipole moment of a loop
  5. Vector potential calculation

Usage:
  python 7.3_magnetostatics.py --count 12 --seed 42
"""

from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import pi, Rational, latex, sqrt

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_wire_field(rng: random.Random) -> Problem:
    I = rng.randint(1, 20)
    s = Rational(rng.randint(1, 10), 100)
    mu0 = sp.Symbol('mu_0')
    B = mu0 * I / (2 * pi * s)
    stmt = f"An infinite straight wire carries current $I = {I}$ A. Find $|\\mathbf{{B}}|$ at distance $s = {latex(s)}$ m."
    sol = f"$$B = \\frac{{\\mu_0 I}}{{2\\pi s}} = \\frac{{\\mu_0 \\cdot {I}}}{{2\\pi \\cdot {latex(s)}}} = {latex(B)}$$"
    return Problem("B-field of infinite wire", stmt, sol)

def gen_solenoid(rng: random.Random) -> Problem:
    n = rng.randint(500, 2000)
    I = rng.randint(1, 10)
    mu0_val = sp.Float(4e-7) * pi
    B = mu0_val * n * I
    stmt = f"A solenoid has $n = {n}$ turns/m and carries $I = {I}$ A. Find $B$ inside."
    sol = (f"$$B = \\mu_0 n I = (4\\pi\\times10^{{-7}})({n})({I})$$\n\n"
           f"$$B = {float(B):.6f} \\text{{ T}} \\approx {float(B)*1000:.3f} \\text{{ mT}}$$")
    return Problem("Solenoid field (Ampère's Law)", stmt, sol)

def gen_parallel_wires(rng: random.Random) -> Problem:
    I1, I2 = rng.randint(1, 15), rng.randint(1, 15)
    d = Rational(rng.randint(1, 10), 100)
    mu0 = sp.Symbol('mu_0')
    f_per_l = mu0 * I1 * I2 / (2 * pi * d)
    stmt = (f"Two parallel wires separated by $d = {latex(d)}$ m carry currents "
            f"$I_1 = {I1}$ A and $I_2 = {I2}$ A in the same direction. Find force/length.")
    sol = (f"$$\\frac{{F}}{{L}} = \\frac{{\\mu_0 I_1 I_2}}{{2\\pi d}} = {latex(f_per_l)}$$\n\n"
           "Direction: **attractive** (same-direction currents attract).")
    return Problem("Force between parallel wires", stmt, sol)

def gen_dipole_moment(rng: random.Random) -> Problem:
    I = rng.randint(1, 10)
    R = Rational(rng.randint(1, 10), 100)
    m = I * pi * R**2
    stmt = f"A circular loop of radius $R = {latex(R)}$ m carries current $I = {I}$ A. Find $|\\mathbf{{m}}|$."
    sol = f"$$m = IA = I\\pi R^2 = {I}\\pi({latex(R)})^2 = {latex(m)} \\text{{ A·m}}^2$$"
    return Problem("Magnetic dipole moment", stmt, sol)

def gen_vector_potential(rng: random.Random) -> Problem:
    n = rng.randint(500, 2000)
    I = rng.randint(1, 5)
    R = Rational(rng.randint(1, 5), 100)
    s = R + Rational(rng.randint(1, 5), 100)
    mu0 = sp.Symbol('mu_0')
    A = mu0 * n * I * R**2 / (2 * s)
    stmt = (f"For a solenoid ($n={n}$/m, $I={I}$ A, radius $R={latex(R)}$ m), "
            f"find $A_\\varphi$ at $s = {latex(s)}$ m (outside).")
    sol = (f"$$A_\\varphi = \\frac{{\\mu_0 n I R^2}}{{2s}} = \\frac{{\\mu_0({n})({I})({latex(R)})^2}}{{2({latex(s)})}}$$\n\n"
           f"$$= {latex(A)}$$")
    return Problem("Vector potential (solenoid exterior)", stmt, sol)

GENERATORS = [gen_wire_field, gen_solenoid, gen_parallel_wires, gen_dipole_moment, gen_vector_potential]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, magnetostatics, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.3 Magnetostatics — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

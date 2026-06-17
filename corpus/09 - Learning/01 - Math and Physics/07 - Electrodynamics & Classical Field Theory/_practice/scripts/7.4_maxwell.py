#!/usr/bin/env python3
"""
7.4_maxwell.py — Practice problem generator for Chapter 7.4
(Electrodynamics: Induction & Maxwell's Equations).

Archetypes:
  1. Faraday's Law EMF calculation
  2. Displacement current in a capacitor
  3. Identify which Maxwell equation applies
  4. Continuity equation verification
  5. Wave equation speed calculation

Usage: python 7.4_maxwell.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import pi, Rational, latex, cos, sin, sqrt

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_faraday_emf(rng: random.Random) -> Problem:
    B0 = rng.randint(1, 5) * Rational(1, 10)
    A = Rational(rng.randint(1, 8), 100)
    omega = rng.randint(50, 500)
    emf_peak = B0 * A * omega
    stmt = (f"A loop of area $A = {latex(A)}$ m² rotates at $\\omega = {omega}$ rad/s "
            f"in a uniform field $B_0 = {latex(B0)}$ T. Find the peak EMF.")
    sol = (f"$$\\mathcal{{E}}_{{\\max}} = B_0 A \\omega = ({latex(B0)})({latex(A)})({omega})$$\n\n"
           f"$$= {latex(emf_peak)} \\text{{ V}}$$")
    return Problem("Faraday's Law (rotating loop)", stmt, sol)

def gen_displacement_current(rng: random.Random) -> Problem:
    I = rng.randint(1, 10)
    R = Rational(rng.randint(1, 5), 100)
    s = Rational(rng.randint(1, 4), 100)
    mu0 = sp.Symbol('mu_0')
    B = mu0 * I * s / (2 * pi * R**2)
    stmt = (f"A capacitor with circular plates of radius $R = {latex(R)}$ m is charging "
            f"at $I = {I}$ A. Find $B$ at radius $s = {latex(s)}$ m between the plates.")
    sol = (f"$$B = \\frac{{\\mu_0 I s}}{{2\\pi R^2}} = \\frac{{\\mu_0 \\cdot {I} \\cdot {latex(s)}}}{{2\\pi({latex(R)})^2}}$$\n\n"
           f"$$= {latex(B)}$$")
    return Problem("Displacement current (capacitor)", stmt, sol)

def gen_maxwell_identify(rng: random.Random) -> Problem:
    scenarios = [
        ("$\\oint\\mathbf{E}\\cdot d\\mathbf{a} = Q/\\varepsilon_0$", "Gauss's Law (I)"),
        ("$\\oint\\mathbf{B}\\cdot d\\mathbf{a} = 0$", "No monopoles (II)"),
        ("$\\oint\\mathbf{E}\\cdot d\\mathbf{l} = -d\\Phi_B/dt$", "Faraday's Law (III)"),
        ("$\\oint\\mathbf{B}\\cdot d\\mathbf{l} = \\mu_0 I + \\mu_0\\varepsilon_0 d\\Phi_E/dt$", "Ampère-Maxwell (IV)"),
    ]
    eq, name = rng.choice(scenarios)
    stmt = f"Identify which of Maxwell's equations is expressed by: {eq}"
    sol = f"This is **{name}**."
    return Problem("Identify Maxwell equation", stmt, sol)

def gen_wave_speed(rng: random.Random) -> Problem:
    eps_r = rng.choice([2, 4, 9, 16])
    mu_r = 1
    v = sp.Symbol('c') / sqrt(eps_r * mu_r)
    stmt = (f"An EM wave propagates in a dielectric with $\\varepsilon_r = {eps_r}$, $\\mu_r = {mu_r}$. "
            "Find the wave speed.")
    sol = (f"$$v = \\frac{{c}}{{\\sqrt{{\\varepsilon_r \\mu_r}}}} = \\frac{{c}}{{\\sqrt{{{eps_r}}}}} "
           f"= \\frac{{c}}{{{int(sqrt(eps_r)) if sqrt(eps_r) == int(sqrt(eps_r)) else latex(sqrt(eps_r))}}}$$\n\n"
           f"$$v = {latex(Rational(3,int(sqrt(eps_r))))} \\times 10^8 \\text{{ m/s}}$$")
    return Problem("Wave speed in dielectric", stmt, sol)

GENERATORS = [gen_faraday_emf, gen_displacement_current, gen_maxwell_identify, gen_wave_speed]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, maxwell-equations, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.4 Maxwell's Equations — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

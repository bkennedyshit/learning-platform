#!/usr/bin/env python3
"""
7.1_electrostatics.py — Practice problem generator for Chapter 7.1
(Electrostatics: Gauss's Law & Potential).

Generates randomized drill problems across 6 archetypes:
  1. Coulomb force between point charges
  2. Electric field from superposition of point charges
  3. Gauss's Law with spherical symmetry
  4. Gauss's Law with cylindrical symmetry
  5. Electrostatic potential from integration
  6. Energy of a charge configuration

Usage:
  python 7.1_electrostatics.py
  python 7.1_electrostatics.py --count 12 --seed 42
  python 7.1_electrostatics.py --count 12 --seed 42 --out /tmp/_71.md

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import sympy as sp
from sympy import pi, sqrt, Rational, latex, oo


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# ---------------------------------------------------------------------------
# Archetype 1: Coulomb force
# ---------------------------------------------------------------------------
def gen_coulomb_force(rng: random.Random) -> Problem:
    q1 = rng.choice([-3, -2, -1, 1, 2, 3, 4, 5]) * sp.Integer(10)**(-6)
    q2 = rng.choice([-3, -2, -1, 1, 2, 3, 4, 5]) * sp.Integer(10)**(-6)
    r = Rational(rng.randint(1, 5), 10)  # meters
    k = Rational(9, 1) * 10**9  # approx 1/(4*pi*eps0)
    F = k * q1 * q2 / r**2
    stmt = (
        f"Two point charges $q_1 = {latex(q1)}$ C and $q_2 = {latex(q2)}$ C "
        f"are separated by $r = {latex(r)}$ m. "
        "Compute the magnitude and direction (attractive/repulsive) of the Coulomb force."
    )
    direction = "repulsive" if F > 0 else "attractive"
    sol = (
        f"$$F = k\\frac{{|q_1 q_2|}}{{r^2}} = (9\\times10^9)\\frac{{|{latex(q1)}||{latex(q2)}|}}{{({latex(r)})^2}}$$\n\n"
        f"$$F = {latex(abs(F))} \\text{{ N}}$$\n\n"
        f"Since $q_1 q_2 {'>' if q1*q2 > 0 else '<'} 0$, the force is **{direction}**."
    )
    return Problem("Coulomb force between point charges", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Superposition of E fields
# ---------------------------------------------------------------------------
def gen_superposition_E(rng: random.Random) -> Problem:
    q1 = rng.randint(1, 5) * sp.Integer(10)**(-9)
    q2 = rng.randint(-5, -1) * sp.Integer(10)**(-9)
    d = Rational(rng.randint(2, 6), 10)
    k = Rational(9, 1) * 10**9
    # Field at midpoint
    r = d / 2
    E1 = k * q1 / r**2  # pointing away from q1
    E2 = k * abs(q2) / r**2  # pointing toward q2
    E_net = E1 + E2  # both point same direction (from + to -)
    stmt = (
        f"Charges $q_1 = +{latex(q1)}$ C and $q_2 = {latex(q2)}$ C are placed "
        f"at $x = 0$ and $x = {latex(d)}$ m respectively. "
        "Find the electric field at the midpoint between them."
    )
    sol = (
        f"At the midpoint $x = {latex(r)}$ m, distance to each charge is ${latex(r)}$ m.\n\n"
        f"$E_1 = k|q_1|/r^2 = {latex(E1)}$ N/C (pointing in $+x$ direction, away from $q_1$)\n\n"
        f"$E_2 = k|q_2|/r^2 = {latex(E2)}$ N/C (pointing in $+x$ direction, toward $q_2$)\n\n"
        f"Both fields point in the same direction ($+x$), so:\n\n"
        f"$$E_{{\\text{{net}}}} = {latex(E_net)} \\text{{ N/C in }} +\\hat{{x}}$$"
    )
    return Problem("Superposition of electric fields", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Gauss's Law (spherical)
# ---------------------------------------------------------------------------
def gen_gauss_sphere(rng: random.Random) -> Problem:
    Q = rng.randint(1, 8) * sp.Integer(10)**(-6)
    R = Rational(rng.randint(1, 5), 100)  # radius in meters
    r_out = R + Rational(rng.randint(1, 5), 100)
    eps0 = sp.Symbol('varepsilon_0')
    E_out = Q / (4 * pi * eps0 * r_out**2)
    stmt = (
        f"A conducting sphere of radius $R = {latex(R)}$ m carries total charge "
        f"$Q = {latex(Q)}$ C. Find $|\\mathbf{{E}}|$ at $r = {latex(r_out)}$ m from the center."
    )
    sol = (
        f"By Gauss's Law with a spherical Gaussian surface at $r = {latex(r_out)}$ m:\n\n"
        f"$$E \\cdot 4\\pi r^2 = Q/\\varepsilon_0$$\n\n"
        f"$$E = \\frac{{Q}}{{4\\pi\\varepsilon_0 r^2}} = \\frac{{{latex(Q)}}}{{4\\pi\\varepsilon_0 ({latex(r_out)})^2}}$$\n\n"
        f"$$E = \\frac{{{latex(Q)}}}{{4\\pi\\varepsilon_0 \\cdot {latex(r_out**2)}}}$$"
    )
    return Problem("Gauss's Law (spherical symmetry)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Gauss's Law (cylindrical)
# ---------------------------------------------------------------------------
def gen_gauss_cylinder(rng: random.Random) -> Problem:
    lam = rng.randint(1, 9) * sp.Integer(10)**(-9)  # C/m
    s = Rational(rng.randint(1, 10), 100)  # distance in m
    eps0 = sp.Symbol('varepsilon_0')
    E = lam / (2 * pi * eps0 * s)
    stmt = (
        f"An infinite line charge has linear charge density $\\lambda = {latex(lam)}$ C/m. "
        f"Find $|\\mathbf{{E}}|$ at distance $s = {latex(s)}$ m from the wire."
    )
    sol = (
        f"By Gauss's Law with a cylindrical Gaussian surface of radius $s$ and length $L$:\n\n"
        f"$$E \\cdot 2\\pi s L = \\lambda L / \\varepsilon_0$$\n\n"
        f"$$E = \\frac{{\\lambda}}{{2\\pi\\varepsilon_0 s}} = \\frac{{{latex(lam)}}}{{2\\pi\\varepsilon_0 \\cdot {latex(s)}}}$$"
    )
    return Problem("Gauss's Law (cylindrical symmetry)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Potential from integration
# ---------------------------------------------------------------------------
def gen_potential(rng: random.Random) -> Problem:
    q = rng.randint(1, 6) * sp.Integer(10)**(-9)
    a = Rational(rng.randint(1, 5), 10)
    b = Rational(rng.randint(6, 10), 10)
    k = Rational(9, 1) * 10**9
    phi_a = k * q / a
    phi_b = k * q / b
    delta_phi = phi_a - phi_b
    stmt = (
        f"A point charge $q = {latex(q)}$ C is at the origin. "
        f"Compute the potential difference $\\phi({latex(a)}) - \\phi({latex(b)})$ "
        f"(with $\\phi(\\infty) = 0$)."
    )
    sol = (
        f"$$\\phi(r) = \\frac{{kq}}{{r}}$$\n\n"
        f"$$\\phi({latex(a)}) = \\frac{{(9\\times10^9)({latex(q)})}}{{{latex(a)}}} = {latex(phi_a)} \\text{{ V}}$$\n\n"
        f"$$\\phi({latex(b)}) = \\frac{{(9\\times10^9)({latex(q)})}}{{{latex(b)}}} = {latex(phi_b)} \\text{{ V}}$$\n\n"
        f"$$\\Delta\\phi = {latex(delta_phi)} \\text{{ V}}$$"
    )
    return Problem("Electrostatic potential calculation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: Energy of charge configuration
# ---------------------------------------------------------------------------
def gen_energy(rng: random.Random) -> Problem:
    q = rng.randint(1, 4) * sp.Integer(10)**(-6)
    d = Rational(rng.randint(1, 5), 10)
    k = Rational(9, 1) * 10**9
    # 3 charges at vertices of equilateral triangle
    W = 3 * k * q**2 / d  # 3 pairs, each at distance d
    stmt = (
        f"Three identical charges $q = {latex(q)}$ C are placed at the vertices of an "
        f"equilateral triangle with side length $d = {latex(d)}$ m. "
        "Find the total electrostatic energy of the configuration."
    )
    sol = (
        f"There are $\\binom{{3}}{{2}} = 3$ pairs, each separated by $d = {latex(d)}$ m.\n\n"
        f"$$W = 3 \\cdot \\frac{{kq^2}}{{d}} = 3 \\cdot \\frac{{(9\\times10^9)({latex(q)})^2}}{{{latex(d)}}}$$\n\n"
        f"$$W = {latex(W)} \\text{{ J}}$$"
    )
    return Problem("Energy of charge configuration", stmt, sol)


# ---------------------------------------------------------------------------
# Generator dispatch
# ---------------------------------------------------------------------------
GENERATORS = [
    gen_coulomb_force,
    gen_superposition_E,
    gen_gauss_sphere,
    gen_gauss_cylinder,
    gen_potential,
    gen_energy,
]


def generate_problems(count: int, seed: int) -> list[Problem]:
    rng = random.Random(seed)
    problems = []
    for i in range(count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))
    return problems


def main():
    parser = argparse.ArgumentParser(description="Generate electrostatics practice problems")
    parser.add_argument("--count", type=int, default=12, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    problems = generate_problems(args.count, seed)

    header = (
        "---\n"
        "tags: [practice, electrostatics, review/math]\n"
        f"generated_seed: {seed}\n"
        f"problem_count: {args.count}\n"
        "---\n\n"
        "# 7.1 Electrostatics — Practice Problems\n\n"
        f"Generated with seed `{seed}`. {args.count} problems across 6 archetypes.\n\n"
        "---\n\n"
    )

    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

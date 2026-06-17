#!/usr/bin/env python3
"""
7.2_laplace_poisson.py — Practice problem generator for Chapter 7.2
(Laplace & Poisson Equations).

Generates randomized drill problems across 6 archetypes:
  1. Verify a function is harmonic (satisfies Laplace's equation)
  2. Separation of variables in Cartesian coordinates
  3. Legendre polynomial expansion coefficients
  4. Method of images (grounded plane)
  5. Multipole expansion (monopole + dipole terms)
  6. Uniqueness theorem application

Usage:
  python 7.2_laplace_poisson.py
  python 7.2_laplace_poisson.py --count 12 --seed 42
  python 7.2_laplace_poisson.py --count 12 --seed 42 --out /tmp/_72.md

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import sympy as sp
from sympy import symbols, cos, sin, exp, pi, Rational, latex, diff, simplify


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


x, y, z, r, theta = symbols('x y z r theta', real=True)


def gen_harmonic_check(rng: random.Random) -> Problem:
    choices = [
        (x**2 - y**2, True),
        (x**2 + y**2, False),
        (exp(x) * cos(y), True),
        (x*y, True),
        (x**3 - 3*x*y**2, True),
        (x**2 + y**2 + z**2, False),
    ]
    func, is_harmonic = rng.choice(choices)
    lap = diff(func, x, 2) + diff(func, y, 2)
    if z in func.free_symbols:
        lap += diff(func, z, 2)
    stmt = (
        f"Determine whether $\\phi(x,y) = {latex(func)}$ satisfies Laplace's equation $\\nabla^2\\phi = 0$."
    )
    sol = (
        f"$$\\frac{{\\partial^2\\phi}}{{\\partial x^2}} = {latex(diff(func, x, 2))}$$\n\n"
        f"$$\\frac{{\\partial^2\\phi}}{{\\partial y^2}} = {latex(diff(func, y, 2))}$$\n\n"
        f"$$\\nabla^2\\phi = {latex(simplify(lap))}$$\n\n"
        + (f"Since $\\nabla^2\\phi = 0$, the function **is harmonic**. ✓"
           if is_harmonic else
           f"Since $\\nabla^2\\phi \\neq 0$, the function is **not harmonic**. ✗")
    )
    return Problem("Verify harmonic function", stmt, sol)


def gen_separation_cartesian(rng: random.Random) -> Problem:
    a = rng.randint(1, 4)
    b = rng.randint(1, 4)
    n = rng.randint(1, 3)
    m = rng.randint(1, 3)
    gamma = sp.sqrt(Rational(n**2, a**2) + Rational(m**2, b**2)) * pi
    stmt = (
        f"A rectangular region has $0 \\leq x \\leq {a}$, $0 \\leq y \\leq {b}$. "
        f"Using separation of variables with $\\phi = 0$ on three sides, "
        f"find the decay constant $\\gamma_{{nm}}$ for mode $(n,m) = ({n},{m})$."
    )
    sol = (
        f"From separation of variables:\n\n"
        f"$$\\gamma_{{nm}} = \\pi\\sqrt{{\\frac{{n^2}}{{a^2}} + \\frac{{m^2}}{{b^2}}}} "
        f"= \\pi\\sqrt{{\\frac{{{n**2}}}{{{a**2}}} + \\frac{{{m**2}}}{{{b**2}}}}} = {latex(gamma)}$$"
    )
    return Problem("Separation of variables (Cartesian)", stmt, sol)


def gen_legendre_coeff(rng: random.Random) -> Problem:
    V0 = rng.randint(1, 10) * 10
    stmt = (
        f"A sphere of radius $R$ has potential $\\phi(R,\\theta) = {V0}\\cos\\theta$ on its surface. "
        "Find the potential for $r > R$ (exterior solution)."
    )
    sol = (
        f"Since $\\cos\\theta = P_1(\\cos\\theta)$, only the $l=1$ term contributes.\n\n"
        f"For $r > R$: $\\phi(r,\\theta) = \\frac{{B_1}}{{r^2}}P_1(\\cos\\theta)$\n\n"
        f"Boundary condition at $r = R$: $B_1/R^2 = {V0}$, so $B_1 = {V0}R^2$.\n\n"
        f"$$\\phi(r,\\theta) = {V0}\\frac{{R^2}}{{r^2}}\\cos\\theta$$\n\n"
        f"This is a dipole potential with effective moment $p = 4\\pi\\varepsilon_0 {V0} R^2$."
    )
    return Problem("Legendre polynomial expansion", stmt, sol)


def gen_image_plane(rng: random.Random) -> Problem:
    q_val = rng.randint(1, 8)
    d_val = rng.randint(1, 5)
    stmt = (
        f"A charge $q = {q_val}$ μC is at height $d = {d_val}$ cm above an infinite "
        "grounded conducting plane. Find the image charge and the force on $q$."
    )
    q = q_val * sp.Integer(10)**(-6)
    d = Rational(d_val, 100)
    k = Rational(9, 1) * 10**9
    F = k * q**2 / (2*d)**2
    sol = (
        f"**Image charge:** $q' = -{q_val}$ μC at distance ${d_val}$ cm below the plane.\n\n"
        f"**Separation:** $2d = {2*d_val}$ cm $= {latex(2*d)}$ m.\n\n"
        f"**Force:** (attractive, toward plane)\n\n"
        f"$$F = \\frac{{kq^2}}{{(2d)^2}} = \\frac{{(9\\times10^9)({latex(q)})^2}}{{({latex(2*d)})^2}} = {latex(F)} \\text{{ N}}$$"
    )
    return Problem("Method of images (grounded plane)", stmt, sol)


def gen_multipole(rng: random.Random) -> Problem:
    q1 = rng.randint(1, 5)
    q2 = -rng.randint(1, 5)
    d = Rational(rng.randint(1, 4), 10)
    Q = q1 + q2
    p = (q1 * d/2 + q2 * (-d/2))  # dipole moment (1D)
    stmt = (
        f"Charges $q_1 = {q1}$ nC at $x = +{latex(d/2)}$ m and $q_2 = {q2}$ nC at "
        f"$x = -{latex(d/2)}$ m. Find the monopole and dipole terms of the multipole expansion."
    )
    sol = (
        f"**Monopole:** $Q = q_1 + q_2 = {q1} + ({q2}) = {Q}$ nC\n\n"
        f"$$\\phi_{{\\text{{mono}}}} = \\frac{{kQ}}{{r}} = \\frac{{k \\cdot {Q}\\times10^{{-9}}}}{{r}}$$\n\n"
        f"**Dipole moment:** $p = q_1(d/2) + q_2(-d/2) = {q1}({latex(d/2)}) + ({q2})({latex(-d/2)})$\n\n"
        f"$p = {latex(p)}$ nC·m\n\n"
        f"$$\\phi_{{\\text{{dip}}}} = \\frac{{kp\\cos\\theta}}{{r^2}}$$"
    )
    return Problem("Multipole expansion", stmt, sol)


def gen_uniqueness(rng: random.Random) -> Problem:
    stmt = (
        "A hollow conducting shell has inner radius $a$ and outer radius $b$. "
        "The inner surface is at potential $V_1$ and the outer at $V_2$. "
        "Using the uniqueness theorem, argue that the solution in the region $a < r < b$ "
        "is uniquely determined, and find it."
    )
    sol = (
        "**Uniqueness argument:** The region $a < r < b$ is charge-free ($\\rho = 0$), "
        "so $\\phi$ satisfies Laplace's equation. Dirichlet boundary conditions are specified "
        "on both boundaries. By the First Uniqueness Theorem, the solution is unique.\n\n"
        "**Solution:** With spherical symmetry, $\\phi(r) = A + B/r$.\n\n"
        "Boundary conditions: $A + B/a = V_1$ and $A + B/b = V_2$.\n\n"
        "Solving: $B = \\frac{(V_1 - V_2)ab}{b - a}$ and $A = V_2 - B/b$.\n\n"
        "$$\\phi(r) = \\frac{V_1 a(b-r) + V_2 b(r-a)}{r(b-a)}$$"
    )
    return Problem("Uniqueness theorem application", stmt, sol)


GENERATORS = [
    gen_harmonic_check,
    gen_separation_cartesian,
    gen_legendre_coeff,
    gen_image_plane,
    gen_multipole,
    gen_uniqueness,
]


def generate_problems(count: int, seed: int) -> list[Problem]:
    rng = random.Random(seed)
    return [GENERATORS[i % len(GENERATORS)](rng) for i in range(count)]


def main():
    parser = argparse.ArgumentParser(description="Generate Laplace/Poisson practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    problems = generate_problems(args.count, seed)

    header = (
        "---\ntags: [practice, laplace-poisson, review/math]\n"
        f"generated_seed: {seed}\nproblem_count: {args.count}\n---\n\n"
        "# 7.2 Laplace & Poisson — Practice Problems\n\n---\n\n"
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

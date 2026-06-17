#!/usr/bin/env python3
"""
4.7_rigid_body.py — Practice problem generator for Chapter 4.7
(Rigid Body Dynamics & Euler Angles).

Archetypes:
  1. Inertia tensor calculation (discrete masses)
  2. Principal moments via eigenvalues
  3. Parallel axis theorem
  4. Torque-free precession frequency
  5. Rotational kinetic energy
  6. Euler's equations — stability of rotation

Usage:
  python 4.7_rigid_body.py --count 8 --seed 42
"""
from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
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
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_inertia_discrete(rng: random.Random) -> Problem:
    n = rng.randint(2, 4)
    masses = [rng.randint(1, 5) for _ in range(n)]
    positions = [(rng.randint(-3, 3), rng.randint(-3, 3), 0) for _ in range(n)]
    # I_zz = sum m_i(x_i^2 + y_i^2)
    Izz = sum(m * (x**2 + y**2) for m, (x, y, z) in zip(masses, positions))
    pos_str = ", ".join(f"$m_{i+1}={masses[i]}$ at $({positions[i][0]},{positions[i][1]},0)$" for i in range(n))
    stmt = (
        f"Compute $I_{{zz}}$ (moment of inertia about the z-axis) for point masses: {pos_str}."
    )
    terms = " + ".join(f"{m}({x}^2+{y}^2)" for m, (x, y, z) in zip(masses, positions))
    sol = (
        f"$I_{{zz}} = \\sum m_i(x_i^2 + y_i^2) = {terms} = {Izz}$ kg·m²"
    )
    return Problem("Inertia Tensor (Discrete Masses)", stmt, sol)


def gen_principal_moments(rng: random.Random) -> Problem:
    # 2x2 inertia tensor (planar body)
    Ixx = rng.randint(2, 10)
    Iyy = rng.randint(2, 10)
    Ixy = rng.randint(-min(Ixx, Iyy) + 1, min(Ixx, Iyy) - 1)
    I = sp.Matrix([[Ixx, -Ixy], [-Ixy, Iyy]])
    evals = I.eigenvals()
    eigenvalues = sorted(I.eigenvals().keys())
    stmt = (
        f"Find the principal moments of inertia for the 2D inertia tensor "
        f"$I = \\begin{{pmatrix}}{Ixx} & {-Ixy} \\\\ {-Ixy} & {Iyy}\\end{{pmatrix}}$ kg·m²."
    )
    sol = (
        f"Solve $\\det(I - \\lambda\\mathbf{{1}}) = 0$:\n\n"
        f"$({Ixx}-\\lambda)({Iyy}-\\lambda) - {Ixy**2} = 0$\n\n"
        f"$\\lambda^2 - {Ixx+Iyy}\\lambda + {Ixx*Iyy - Ixy**2} = 0$\n\n"
        f"Principal moments: $I_1 = {sp.latex(eigenvalues[0])}$, $I_2 = {sp.latex(eigenvalues[1])}$ kg·m²"
    )
    return Problem("Principal Moments (Eigenvalues)", stmt, sol)


def gen_parallel_axis(rng: random.Random) -> Problem:
    Icm = rng.randint(1, 20)
    M = rng.randint(1, 8)
    d = rng.randint(1, 5)
    I_new = Icm + M * d**2
    stmt = (
        f"A body has $I_{{cm}} = {Icm}$ kg·m², mass $M = {M}$ kg. "
        f"Find the moment of inertia about a parallel axis at distance $d = {d}$ m from the CM."
    )
    sol = (
        f"Parallel axis theorem: $I = I_{{cm}} + Md^2 = {Icm} + {M}\\cdot{d}^2 = {Icm} + {M*d**2} = {I_new}$ kg·m²"
    )
    return Problem("Parallel Axis Theorem", stmt, sol)


def gen_precession(rng: random.Random) -> Problem:
    I1 = rng.randint(2, 8)
    I3 = I1 + rng.randint(1, 5)
    w3 = rng.randint(5, 20)
    Omega = sp.Rational(I3 - I1, I1) * w3
    stmt = (
        f"A symmetric top ($I_1 = I_2 = {I1}$, $I_3 = {I3}$ kg·m²) spins torque-free "
        f"with $\\omega_3 = {w3}$ rad/s. Find the body-frame precession frequency $\\Omega$."
    )
    sol = (
        f"$\\Omega = \\frac{{I_3 - I_1}}{{I_1}}\\omega_3 = \\frac{{{I3}-{I1}}}{{{I1}}}\\cdot{w3} = {sp.latex(Omega)}$ rad/s"
    )
    return Problem("Torque-Free Precession", stmt, sol)


def gen_rotational_ke(rng: random.Random) -> Problem:
    I1 = rng.randint(1, 5)
    I2 = rng.randint(1, 5)
    I3 = rng.randint(1, 5)
    w1 = rng.randint(1, 6)
    w2 = rng.randint(1, 6)
    w3 = rng.randint(1, 6)
    T = sp.Rational(I1 * w1**2 + I2 * w2**2 + I3 * w3**2, 2)
    stmt = (
        f"Compute the rotational kinetic energy for a body with principal moments "
        f"$I_1={I1}, I_2={I2}, I_3={I3}$ kg·m² and angular velocity "
        f"$\\boldsymbol{{\\omega}} = ({w1}, {w2}, {w3})$ rad/s."
    )
    sol = (
        f"$T = \\frac{{1}}{{2}}(I_1\\omega_1^2 + I_2\\omega_2^2 + I_3\\omega_3^2)$\n\n"
        f"$= \\frac{{1}}{{2}}({I1}\\cdot{w1}^2 + {I2}\\cdot{w2}^2 + {I3}\\cdot{w3}^2)$\n\n"
        f"$= \\frac{{1}}{{2}}({I1*w1**2} + {I2*w2**2} + {I3*w3**2}) = {sp.latex(T)}$ J"
    )
    return Problem("Rotational Kinetic Energy", stmt, sol)


def gen_stability(rng: random.Random) -> Problem:
    stmt = (
        "For a rigid body with $I_1 < I_2 < I_3$, determine the stability of "
        "rotation about each principal axis (torque-free). Which axes give stable rotation?"
    )
    sol = (
        "Linearize Euler's equations about rotation purely about each axis:\n\n"
        "**About $\\hat e_1$ (smallest $I$):** Perturbations $\\omega_2, \\omega_3$ satisfy:\n"
        "$I_2\\dot\\omega_2 = (I_3-I_1)\\omega_3\\omega_1$, $I_3\\dot\\omega_3 = (I_1-I_2)\\omega_1\\omega_2$.\n"
        "Product $(I_3-I_1)(I_1-I_2) < 0$ → oscillatory → **stable**.\n\n"
        "**About $\\hat e_3$ (largest $I$):** Product $(I_1-I_3)(I_2-I_3)$: both factors negative → product positive... "
        "Actually: $(I_2-I_3)(I_1-I_2)$... Let's be careful.\n\n"
        "The intermediate axis theorem: rotation about $\\hat e_2$ (intermediate moment) is **unstable**. "
        "Rotation about $\\hat e_1$ and $\\hat e_3$ (smallest and largest) is **stable**.\n\n"
        "This is the **tennis racket theorem** (Dzhanibekov effect)."
    )
    return Problem("Stability of Rotation (Intermediate Axis)", stmt, sol)


GENERATORS = [
    gen_inertia_discrete, gen_principal_moments, gen_parallel_axis,
    gen_precession, gen_rotational_ke, gen_stability,
]


def main():
    parser = argparse.ArgumentParser(description="Generate rigid body dynamics problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, rigid-body, euler-angles, inertia-tensor]", "---", "",
             "# Practice: Rigid Body Dynamics (4.7)", ""]
    for idx, p in enumerate(problems, 1):
        lines.append(p.render(idx))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

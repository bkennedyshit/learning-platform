#!/usr/bin/env python3
"""
4.3_lagrangian.py — Practice problem generator for Chapter 4.3
(Lagrangian Mechanics: Euler-Lagrange).

Archetypes:
  1. Simple pendulum E-L derivation
  2. Bead on rotating hoop — find equilibria
  3. Coupled oscillators — normal mode frequencies
  4. Atwood machine via Lagrangian
  5. Particle on inclined plane
  6. Identify cyclic coordinates and conserved quantities

Usage:
  python 4.3_lagrangian.py --count 8 --seed 42
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


def gen_pendulum(rng: random.Random) -> Problem:
    l = rng.randint(1, 5)
    m = rng.randint(1, 6)
    stmt = (
        f"Derive the equation of motion for a simple pendulum of mass $m={m}$ kg "
        f"and length $\\ell={l}$ m using the Lagrangian method."
    )
    sol = (
        f"$T = \\frac{{1}}{{2}}m\\ell^2\\dot\\theta^2 = \\frac{{1}}{{2}}({m})({l})^2\\dot\\theta^2$\n\n"
        f"$U = -mg\\ell\\cos\\theta = -({m})(g)({l})\\cos\\theta$\n\n"
        f"$L = \\frac{{{m*l**2}}}{{2}}\\dot\\theta^2 + {m*l}g\\cos\\theta$\n\n"
        f"$\\frac{{\\partial L}}{{\\partial\\dot\\theta}} = {m*l**2}\\dot\\theta$, "
        f"$\\frac{{d}}{{dt}}(\\cdot) = {m*l**2}\\ddot\\theta$\n\n"
        f"$\\frac{{\\partial L}}{{\\partial\\theta}} = -{m*l}g\\sin\\theta$\n\n"
        f"E-L: ${m*l**2}\\ddot\\theta + {m*l}g\\sin\\theta = 0 \\implies \\ddot\\theta + \\frac{{g}}{{{l}}}\\sin\\theta = 0$"
    )
    return Problem("Simple Pendulum (Lagrangian)", stmt, sol)


def gen_coupled_oscillators(rng: random.Random) -> Problem:
    m = rng.randint(1, 4)
    k = rng.randint(1, 6)
    kappa = rng.randint(1, 4)
    w1_sq = sp.Rational(k, m)
    w2_sq = sp.Rational(k + 2 * kappa, m)
    stmt = (
        f"Two identical masses $m={m}$ kg are connected to walls by springs $k={k}$ N/m "
        f"and to each other by a spring $\\kappa={kappa}$ N/m. Find the normal mode frequencies."
    )
    sol = (
        f"$M = {m}I_2$, $K = \\begin{{pmatrix}}{k+kappa} & -{kappa} \\\\ -{kappa} & {k+kappa}\\end{{pmatrix}}$\n\n"
        f"$\\det(K - \\omega^2 M) = 0$: $({k+kappa} - {m}\\omega^2)^2 - {kappa}^2 = 0$\n\n"
        f"$\\omega_1^2 = \\frac{{k}}{{m}} = {sp.latex(w1_sq)}$ rad²/s² (symmetric mode)\n\n"
        f"$\\omega_2^2 = \\frac{{k+2\\kappa}}{{m}} = {sp.latex(w2_sq)}$ rad²/s² (antisymmetric mode)\n\n"
        f"$\\omega_1 = {sp.latex(sp.sqrt(w1_sq))}$ rad/s, $\\omega_2 = {sp.latex(sp.sqrt(w2_sq))}$ rad/s"
    )
    return Problem("Coupled Oscillators — Normal Modes", stmt, sol)


def gen_atwood_lagrangian(rng: random.Random) -> Problem:
    m1 = rng.randint(3, 10)
    m2 = rng.randint(1, m1 - 1)
    a = sp.Rational(m1 - m2, m1 + m2)
    stmt = (
        f"Use the Lagrangian method to find the acceleration of an Atwood machine "
        f"with $m_1={m1}$ kg and $m_2={m2}$ kg."
    )
    sol = (
        f"Generalized coordinate $x$ (downward displacement of $m_1$).\n\n"
        f"$T = \\frac{{1}}{{2}}(m_1+m_2)\\dot x^2 = \\frac{{{m1+m2}}}{{2}}\\dot x^2$\n\n"
        f"$U = -m_1 gx + m_2 gx = -({m1}-{m2})gx$\n\n"
        f"$L = \\frac{{{m1+m2}}}{{2}}\\dot x^2 + ({m1-m2})gx$\n\n"
        f"E-L: $({m1+m2})\\ddot x = ({m1-m2})g$\n\n"
        f"$a = {sp.latex(a)}g \\approx {float(a):.4f}g$"
    )
    return Problem("Atwood Machine (Lagrangian)", stmt, sol)


def gen_inclined_plane(rng: random.Random) -> Problem:
    angle = rng.randint(15, 75)
    m = rng.randint(1, 8)
    theta = sp.Rational(angle, 1)
    stmt = (
        f"A block of mass $m={m}$ kg slides on a frictionless inclined plane "
        f"at angle $\\alpha = {angle}°$. Using generalized coordinate $s$ (distance along slope), "
        "find the equation of motion via the Lagrangian."
    )
    sol = (
        f"$T = \\frac{{1}}{{2}}m\\dot s^2$, $U = mgs\\sin\\alpha$ (height = $s\\sin\\alpha$)\n\n"
        f"$L = \\frac{{1}}{{2}}m\\dot s^2 - mgs\\sin\\alpha$\n\n"
        f"E-L: $m\\ddot s = -mg\\sin\\alpha \\implies \\ddot s = -g\\sin({angle}°)$\n\n"
        f"$a = g\\sin({angle}°) \\approx {9.8*sp.sin(sp.rad(angle)):.3f}$ m/s² (down the slope)"
    )
    return Problem("Inclined Plane (Lagrangian)", stmt, sol)


def gen_cyclic_coordinate(rng: random.Random) -> Problem:
    stmt = (
        "A particle moves in 3D with Lagrangian "
        "$L = \\frac{1}{2}m(\\dot{r}^2 + r^2\\dot\\theta^2 + r^2\\sin^2\\theta\\,\\dot\\phi^2) - U(r)$. "
        "Identify all cyclic coordinates and state the corresponding conserved quantities."
    )
    sol = (
        "$\\phi$ is cyclic: $\\frac{\\partial L}{\\partial\\phi} = 0$.\n\n"
        "Conserved quantity: $p_\\phi = \\frac{\\partial L}{\\partial\\dot\\phi} = mr^2\\sin^2\\theta\\,\\dot\\phi = L_z$ "
        "(z-component of angular momentum).\n\n"
        "$r$ and $\\theta$ are NOT cyclic (potential depends on $r$; $\\theta$ appears in $T$).\n\n"
        "Since $\\partial L/\\partial t = 0$, energy $H = T + U$ is also conserved (Noether/time symmetry)."
    )
    return Problem("Cyclic Coordinates & Conservation", stmt, sol)


def gen_bead_hoop(rng: random.Random) -> Problem:
    R = rng.randint(1, 4)
    Omega = rng.randint(2, 8)
    stmt = (
        f"A bead slides on a circular hoop of radius $R={R}$ m rotating at "
        f"$\\Omega={Omega}$ rad/s about a vertical diameter. Find the non-trivial "
        "equilibrium angle $\\theta_0$ (measured from bottom). Use $g=9.8$ m/s²."
    )
    cos_val = sp.Rational(98, 10) / (R * Omega**2)
    cos_float = float(cos_val)
    exists = cos_float <= 1
    sol = (
        f"Equilibrium condition: $\\cos\\theta_0 = \\frac{{g}}{{R\\Omega^2}} = "
        f"\\frac{{9.8}}{{{R}\\cdot{Omega}^2}} = {sp.latex(cos_val)}$\n\n"
    )
    if exists:
        sol += f"Since ${sp.latex(cos_val)} \\leq 1$, the equilibrium exists: $\\theta_0 = \\arccos({sp.latex(cos_val)}) \\approx {sp.deg(sp.acos(cos_val)).evalf():.1f}°$"
    else:
        sol += f"Since ${sp.latex(cos_val)} > 1$, no non-trivial equilibrium exists. Only $\\theta=0$ (bottom) is stable."
    return Problem("Bead on Rotating Hoop", stmt, sol)


GENERATORS = [
    gen_pendulum, gen_coupled_oscillators, gen_atwood_lagrangian,
    gen_inclined_plane, gen_cyclic_coordinate, gen_bead_hoop,
]


def main():
    parser = argparse.ArgumentParser(description="Generate Lagrangian mechanics problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, lagrangian-mechanics, euler-lagrange]", "---", "",
             "# Practice: Lagrangian Mechanics (4.3)", ""]
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

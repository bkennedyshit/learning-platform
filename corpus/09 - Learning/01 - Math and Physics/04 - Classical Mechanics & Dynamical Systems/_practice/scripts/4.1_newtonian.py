#!/usr/bin/env python3
"""
4.1_newtonian.py — Practice problem generator for Chapter 4.1
(Newtonian Dynamics & Conservation Laws).

Generates randomized drill problems across 6 archetypes:
  1. Elastic collision (1D) — find final velocities
  2. Conservation of momentum (2D) — explosion/breakup
  3. Work-energy theorem — find speed after work done
  4. Angular momentum conservation — spinning skater
  5. Escape velocity calculation
  6. Atwood machine acceleration and tension

Usage:
  python 4.1_newtonian.py
  python 4.1_newtonian.py --count 12 --seed 42
  python 4.1_newtonian.py --out problems.md
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


def gen_elastic_collision(rng: random.Random) -> Problem:
    m1 = rng.randint(1, 8)
    m2 = rng.randint(1, 8)
    v1 = rng.randint(2, 12)
    # target at rest
    v1f = sp.Rational(m1 - m2, m1 + m2) * v1
    v2f = sp.Rational(2 * m1, m1 + m2) * v1
    # verify
    assert m1 * v1 == m1 * v1f + m2 * v2f
    stmt = (
        f"A ball of mass $m_1 = {m1}$ kg moving at $v_1 = {v1}$ m/s "
        f"collides elastically with a stationary ball of mass $m_2 = {m2}$ kg. "
        "Find the final velocities $v_1'$ and $v_2'$."
    )
    sol = (
        f"Using elastic collision formulas:\n\n"
        f"$$\nv_1' = \\frac{{m_1 - m_2}}{{m_1 + m_2}}v_1 = "
        f"\\frac{{{m1}-{m2}}}{{{m1}+{m2}}}\\cdot{v1} = {sp.latex(v1f)} \\text{{ m/s}}\n$$\n\n"
        f"$$\nv_2' = \\frac{{2m_1}}{{m_1+m_2}}v_1 = "
        f"\\frac{{2\\cdot{m1}}}{{{m1}+{m2}}}\\cdot{v1} = {sp.latex(v2f)} \\text{{ m/s}}\n$$\n\n"
        f"Verify momentum: ${m1}\\cdot{v1} = {m1}\\cdot{sp.latex(v1f)} + {m2}\\cdot{sp.latex(v2f)} = {m1*v1}$ ✓"
    )
    return Problem("1D Elastic Collision", stmt, sol)


def gen_momentum_2d(rng: random.Random) -> Problem:
    M = rng.randint(4, 12)
    v0 = rng.randint(3, 10)
    m1 = rng.randint(1, M - 1)
    m2 = M - m1
    # after explosion, m1 goes perpendicular
    v1y = rng.randint(2, 8)
    # momentum conservation: M*v0 = m1*v1x + m2*v2x, 0 = m1*v1y + m2*v2y
    # let v1x = 0 for simplicity
    v2x = sp.Rational(M * v0, m2)
    v2y = sp.Rational(-m1 * v1y, m2)
    stmt = (
        f"A projectile of mass $M = {M}$ kg moving at ${v0}$ m/s (x-direction) "
        f"explodes into two pieces: $m_1 = {m1}$ kg moves purely in the y-direction "
        f"at ${v1y}$ m/s. Find the velocity of $m_2 = {m2}$ kg."
    )
    sol = (
        f"Conservation of x-momentum: $M v_0 = m_1(0) + m_2 v_{{2x}}$\n\n"
        f"$v_{{2x}} = \\frac{{{M}\\cdot{v0}}}{{{m2}}} = {sp.latex(v2x)}$ m/s\n\n"
        f"Conservation of y-momentum: $0 = m_1 v_{{1y}} + m_2 v_{{2y}}$\n\n"
        f"$v_{{2y}} = -\\frac{{{m1}\\cdot{v1y}}}{{{m2}}} = {sp.latex(v2y)}$ m/s\n\n"
        f"$|\\mathbf{{v}}_2| = \\sqrt{{v_{{2x}}^2 + v_{{2y}}^2}} = "
        f"{sp.latex(sp.sqrt(v2x**2 + v2y**2))}$ m/s"
    )
    return Problem("2D Momentum Conservation (Explosion)", stmt, sol)


def gen_work_energy(rng: random.Random) -> Problem:
    m = rng.randint(1, 10)
    v0 = rng.randint(0, 5)
    F = rng.randint(5, 30)
    d = rng.randint(2, 10)
    W = F * d
    vf_sq = sp.Rational(2 * W, m) + v0**2
    vf = sp.sqrt(vf_sq)
    stmt = (
        f"A block of mass ${m}$ kg, initially at ${v0}$ m/s, is pushed by a "
        f"constant force $F = {F}$ N over a distance $d = {d}$ m (frictionless). "
        "Find the final speed."
    )
    sol = (
        f"Work-energy theorem: $W = \\Delta T = \\frac{{1}}{{2}}m v_f^2 - \\frac{{1}}{{2}}m v_0^2$\n\n"
        f"$W = Fd = {F}\\cdot{d} = {W}$ J\n\n"
        f"$v_f = \\sqrt{{\\frac{{2W}}{{m}} + v_0^2}} = "
        f"\\sqrt{{\\frac{{2\\cdot{W}}}{{{m}}} + {v0**2}}} = {sp.latex(vf)}$ m/s"
        f" $\\approx {float(vf):.3f}$ m/s"
    )
    return Problem("Work-Energy Theorem", stmt, sol)


def gen_angular_momentum(rng: random.Random) -> Problem:
    I1 = rng.randint(3, 10)
    w1 = rng.randint(2, 8)
    I2_factor = sp.Rational(rng.randint(1, I1 - 1), I1)
    I2 = I1 * I2_factor
    w2 = sp.Rational(I1 * w1, I2)
    stmt = (
        f"A figure skater with moment of inertia $I_1 = {I1}$ kg·m² spins at "
        f"$\\omega_1 = {w1}$ rad/s. They pull their arms in, reducing their moment "
        f"of inertia to $I_2 = {sp.latex(I2)}$ kg·m². Find $\\omega_2$."
    )
    sol = (
        f"Angular momentum conservation: $I_1\\omega_1 = I_2\\omega_2$\n\n"
        f"$\\omega_2 = \\frac{{I_1\\omega_1}}{{I_2}} = "
        f"\\frac{{{I1}\\cdot{w1}}}{{{sp.latex(I2)}}} = {sp.latex(w2)}$ rad/s"
    )
    assert I1 * w1 == I2 * w2
    return Problem("Angular Momentum Conservation", stmt, sol)


def gen_escape_velocity(rng: random.Random) -> Problem:
    # Use scaled units: M in 10^24 kg, R in 10^6 m
    M_val = rng.randint(1, 20)
    R_val = rng.randint(2, 12)
    G = sp.Rational(667, 10**13)  # 6.67e-11 in rational approx
    M = M_val * 10**24
    R = R_val * 10**6
    v_esc_sq = 2 * sp.Rational(667, 10**13) * M_val * 10**24 / (R_val * 10**6)
    v_esc = sp.sqrt(v_esc_sq)
    v_num = float(v_esc)
    stmt = (
        f"Find the escape velocity from a planet of mass "
        f"$M = {M_val} \\times 10^{{24}}$ kg and radius $R = {R_val} \\times 10^6$ m. "
        f"Use $G = 6.67 \\times 10^{{-11}}$ N·m²/kg²."
    )
    sol = (
        f"$v_{{\\text{{esc}}}} = \\sqrt{{\\frac{{2GM}}{{R}}}} = "
        f"\\sqrt{{\\frac{{2(6.67\\times10^{{-11}})({M_val}\\times10^{{24}})}}"
        f"{{{R_val}\\times10^6}}}}$\n\n"
        f"$\\approx {v_num:.0f}$ m/s $= {v_num/1000:.2f}$ km/s"
    )
    return Problem("Escape Velocity", stmt, sol)


def gen_atwood(rng: random.Random) -> Problem:
    m1 = rng.randint(3, 12)
    m2 = rng.randint(1, m1 - 1)
    g = sp.Symbol('g')
    a = sp.Rational(m1 - m2, m1 + m2)
    T = sp.Rational(2 * m1 * m2, m1 + m2)
    stmt = (
        f"An Atwood machine has masses $m_1 = {m1}$ kg and $m_2 = {m2}$ kg. "
        "Find the acceleration (as a fraction of $g$) and the tension."
    )
    sol = (
        f"$a = \\frac{{m_1 - m_2}}{{m_1 + m_2}}g = "
        f"\\frac{{{m1}-{m2}}}{{{m1}+{m2}}}g = {sp.latex(a)}g$\n\n"
        f"$T = \\frac{{2m_1 m_2}}{{m_1+m_2}}g = "
        f"\\frac{{2\\cdot{m1}\\cdot{m2}}}{{{m1}+{m2}}}g = {sp.latex(T)}g$ N"
    )
    return Problem("Atwood Machine", stmt, sol)


GENERATORS = [
    gen_elastic_collision,
    gen_momentum_2d,
    gen_work_energy,
    gen_angular_momentum,
    gen_escape_velocity,
    gen_atwood,
]


def main():
    parser = argparse.ArgumentParser(description="Generate Newtonian mechanics problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = []
    for i in range(args.count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))

    lines = [
        "---",
        "tags: [review/math, classical-mechanics, newtonian]",
        "---",
        "",
        "# Practice: Newtonian Dynamics & Conservation Laws (4.1)",
        "",
    ]
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

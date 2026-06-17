#!/usr/bin/env python3
"""
4.4_central_forces.py — Practice problem generator for Chapter 4.4
(Central Forces & Keplerian Orbits).

Archetypes:
  1. Kepler period from semi-major axis
  2. Eccentricity from periapsis/apoapsis
  3. Escape velocity from planet parameters
  4. Hohmann transfer delta-v
  5. Orbit equation from energy and angular momentum
  6. Vis-viva speed calculation

Usage:
  python 4.4_central_forces.py --count 8 --seed 42
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


def gen_kepler_period(rng: random.Random) -> Problem:
    a_au = sp.Rational(rng.randint(1, 40), rng.randint(1, 4))
    T = a_au ** sp.Rational(3, 2)
    stmt = (
        f"A planet orbits the Sun with semi-major axis $a = {sp.latex(a_au)}$ AU. "
        "Find its orbital period in years using Kepler's third law ($T^2 = a^3$ in AU/yr units)."
    )
    sol = (
        f"$T = a^{{3/2}} = ({sp.latex(a_au)})^{{3/2}} = {sp.latex(T)}$ years "
        f"$\\approx {float(T):.3f}$ years"
    )
    return Problem("Kepler Period Calculation", stmt, sol)


def gen_eccentricity(rng: random.Random) -> Problem:
    rmin = sp.Rational(rng.randint(1, 10), rng.randint(1, 3))
    rmax = rmin + sp.Rational(rng.randint(1, 20), rng.randint(1, 3))
    e = (rmax - rmin) / (rmax + rmin)
    a = (rmin + rmax) / 2
    stmt = (
        f"An orbit has periapsis $r_{{\\min}} = {sp.latex(rmin)}$ AU and "
        f"apoapsis $r_{{\\max}} = {sp.latex(rmax)}$ AU. Find the eccentricity and semi-major axis."
    )
    sol = (
        f"$e = \\frac{{r_{{\\max}} - r_{{\\min}}}}{{r_{{\\max}} + r_{{\\min}}}} = "
        f"\\frac{{{sp.latex(rmax)} - {sp.latex(rmin)}}}{{{sp.latex(rmax)} + {sp.latex(rmin)}}} = {sp.latex(e)}$\n\n"
        f"$a = \\frac{{r_{{\\min}} + r_{{\\max}}}}{{2}} = {sp.latex(a)}$ AU"
    )
    return Problem("Eccentricity from Apsidal Distances", stmt, sol)


def gen_escape_vel(rng: random.Random) -> Problem:
    M = rng.randint(1, 15)  # in 10^24 kg
    R = rng.randint(2, 10)  # in 10^6 m
    v_sq = 2 * 6.674e-11 * M * 1e24 / (R * 1e6)
    v = v_sq ** 0.5
    stmt = (
        f"Calculate the escape velocity from a planet with $M = {M} \\times 10^{{24}}$ kg "
        f"and $R = {R} \\times 10^6$ m."
    )
    sol = (
        f"$v_{{esc}} = \\sqrt{{\\frac{{2GM}}{{R}}}} = "
        f"\\sqrt{{\\frac{{2(6.674\\times10^{{-11}})({M}\\times10^{{24}})}}{{{R}\\times10^6}}}}$\n\n"
        f"$= \\sqrt{{{v_sq:.2e}}} \\approx {v:.0f}$ m/s $= {v/1000:.2f}$ km/s"
    )
    return Problem("Escape Velocity", stmt, sol)


def gen_hohmann(rng: random.Random) -> Problem:
    r1 = rng.randint(1, 5)  # in units of R_earth orbit
    r2 = r1 + rng.randint(1, 8)
    # In normalized units where GM=1, v_c = 1/sqrt(r)
    # dv1 = sqrt(2r2/(r1(r1+r2))) - 1/sqrt(r1)
    # dv2 = 1/sqrt(r2) - sqrt(2r1/(r2(r1+r2)))
    vc1 = 1 / sp.sqrt(r1)
    vt1 = sp.sqrt(sp.Rational(2 * r2, r1 * (r1 + r2)))
    dv1 = vt1 - vc1
    vc2 = 1 / sp.sqrt(r2)
    vt2 = sp.sqrt(sp.Rational(2 * r1, r2 * (r1 + r2)))
    dv2 = vc2 - vt2
    stmt = (
        f"Compute the total $\\Delta v$ for a Hohmann transfer from circular orbit "
        f"$r_1 = {r1}$ to $r_2 = {r2}$ (in units where $GM = 1$)."
    )
    sol = (
        f"$v_{{c1}} = 1/\\sqrt{{{r1}}} = {sp.latex(vc1)}$\n\n"
        f"$v_{{t1}} = \\sqrt{{\\frac{{2r_2}}{{r_1(r_1+r_2)}}}} = \\sqrt{{\\frac{{{2*r2}}}{{{r1*(r1+r2)}}}}} = {sp.latex(vt1)}$\n\n"
        f"$\\Delta v_1 = {sp.latex(sp.simplify(dv1))}$\n\n"
        f"$v_{{c2}} = 1/\\sqrt{{{r2}}} = {sp.latex(vc2)}$\n\n"
        f"$v_{{t2}} = \\sqrt{{\\frac{{2r_1}}{{r_2(r_1+r_2)}}}} = {sp.latex(vt2)}$\n\n"
        f"$\\Delta v_2 = {sp.latex(sp.simplify(dv2))}$\n\n"
        f"Total: $\\Delta v = \\Delta v_1 + \\Delta v_2 \\approx {float(dv1)+float(dv2):.4f}$"
    )
    return Problem("Hohmann Transfer Δv", stmt, sol)


def gen_orbit_equation(rng: random.Random) -> Problem:
    e = sp.Rational(rng.randint(1, 9), 10)
    p = rng.randint(1, 8)
    stmt = (
        f"Write the orbit equation $r(\\theta)$ for an orbit with semi-latus rectum "
        f"$p = {p}$ and eccentricity $e = {sp.latex(e)}$. "
        "Find $r_{{\\min}}$ and $r_{{\\max}}$."
    )
    rmin = sp.Rational(p, 1) / (1 + e)
    rmax = sp.Rational(p, 1) / (1 - e)
    sol = (
        f"$r(\\theta) = \\frac{{p}}{{1 + e\\cos\\theta}} = \\frac{{{p}}}{{1 + {sp.latex(e)}\\cos\\theta}}$\n\n"
        f"$r_{{\\min}} = \\frac{{p}}{{1+e}} = \\frac{{{p}}}{{{sp.latex(1+e)}}} = {sp.latex(rmin)}$\n\n"
        f"$r_{{\\max}} = \\frac{{p}}{{1-e}} = \\frac{{{p}}}{{{sp.latex(1-e)}}} = {sp.latex(rmax)}$"
    )
    return Problem("Orbit Equation", stmt, sol)


def gen_vis_viva(rng: random.Random) -> Problem:
    a = rng.randint(2, 10)
    r = rng.randint(1, a)
    # v^2 = GM(2/r - 1/a), use GM=1
    v_sq = sp.Rational(2, r) - sp.Rational(1, a)
    v = sp.sqrt(v_sq)
    stmt = (
        f"Using the vis-viva equation with $GM=1$, find the speed at $r={r}$ "
        f"for an orbit with semi-major axis $a={a}$."
    )
    sol = (
        f"$v^2 = GM\\left(\\frac{{2}}{{r}} - \\frac{{1}}{{a}}\\right) = "
        f"\\frac{{2}}{{{r}}} - \\frac{{1}}{{{a}}} = {sp.latex(v_sq)}$\n\n"
        f"$v = {sp.latex(v)} \\approx {float(v):.4f}$"
    )
    return Problem("Vis-Viva Speed", stmt, sol)


GENERATORS = [
    gen_kepler_period, gen_eccentricity, gen_escape_vel,
    gen_hohmann, gen_orbit_equation, gen_vis_viva,
]


def main():
    parser = argparse.ArgumentParser(description="Generate central force problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, central-forces, kepler, orbits]", "---", "",
             "# Practice: Central Forces & Keplerian Orbits (4.4)", ""]
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

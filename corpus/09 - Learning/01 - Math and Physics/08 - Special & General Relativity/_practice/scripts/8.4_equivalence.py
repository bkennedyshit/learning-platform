#!/usr/bin/env python3
"""
8.4_equivalence.py — Practice problems for Chapter 8.4
(Equivalence Principle & Curved Spacetime).

Archetypes:
  1. Gravitational redshift calculation
  2. Gravitational time dilation (GPS-style)
  3. Shapiro time delay estimate
  4. Light deflection (EP prediction)
  5. Schwarzschild radius computation

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, simplify, sqrt, log, pi

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

G = sp.Symbol('G', positive=True)
c = sp.Symbol('c', positive=True)

def gen_redshift(rng: random.Random) -> Problem:
    M_solar = Rational(2,1)  # x10^30 kg (symbolic)
    R_km = Rational(rng.choice([10, 15, 20, 5800, 700000]),1)
    M_mult = Rational(rng.choice([1, 2, 3, 10]),1)
    rs_over_R = Rational(3, R_km)  # simplified symbolic
    stmt = (f"A star has mass ${latex(M_mult)}M_\\odot$ and radius ${latex(R_km)}$ km. "
            "Compute the gravitational redshift $z$ of light from its surface.")
    sol = (f"$r_s = 2GM/c^2 = {latex(M_mult)} \\times 2.95$ km $= {latex(M_mult*Rational(295,100))}$ km\n\n"
           f"$z = (1-r_s/R)^{{-1/2}} - 1 \\approx r_s/(2R)$ for weak fields\n\n"
           f"$z \\approx {latex(M_mult*Rational(295,100))}/(2\\times{latex(R_km)}) = "
           f"{latex(simplify(M_mult*Rational(295,100)/(2*R_km)))}$")
    return Problem("Gravitational Redshift", stmt, sol)

def gen_time_dilation_grav(rng: random.Random) -> Problem:
    h_km = Rational(rng.choice([400, 20200, 35786]),1)
    stmt = (f"A satellite orbits at altitude $h = {latex(h_km)}$ km above Earth. "
            "Estimate the gravitational time dilation (fractional rate difference) relative to ground.")
    R_E = Rational(6371,1)
    GM_over_c2 = Rational(443,100)  # mm ≈ 4.43e-3 m
    frac = simplify(GM_over_c2 * (Rational(1,1)/R_E - Rational(1,1)/(R_E + h_km)))
    sol = (f"$\\Delta\\tau/\\Delta t \\approx GM/c^2 \\times (1/R_E - 1/(R_E+h))$\n\n"
           f"$= 4.43\\times10^{{-3}}\\text{{ m}} \\times (1/{latex(R_E)} - 1/{latex(R_E+h_km)})\\times10^{{-3}}$ m$^{{-1}}$\n\n"
           f"Fractional difference $\\approx {latex(frac)}\\times10^{{-6}}$ (per km units)")
    return Problem("Gravitational Time Dilation", stmt, sol)

def gen_schwarzschild_radius(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1, 5, 10, 1000000, 4000000]),1)
    rs = simplify(M_mult * Rational(295,100))  # in km
    stmt = f"Compute the Schwarzschild radius for a mass of ${latex(M_mult)}M_\\odot$."
    sol = f"$r_s = 2GM/c^2 = {latex(M_mult)} \\times 2.95\\text{{ km}} = {latex(rs)}$ km"
    return Problem("Schwarzschild Radius", stmt, sol)

def gen_light_deflection_ep(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1, 2, 5]),1)
    R_mult = Rational(rng.choice([1, 2, 3]),1)
    # EP prediction: 2GM/(c^2 b), GR: 4GM/(c^2 b)
    delta_ep = simplify(2 * M_mult * Rational(295,100) / (R_mult * Rational(696000,1)))
    delta_gr = 2 * delta_ep
    stmt = (f"Light passes at ${latex(R_mult)}R_\\odot$ from a star of mass ${latex(M_mult)}M_\\odot$. "
            "Compute deflection (EP and full GR).")
    sol = (f"EP: $\\delta = 2GM/(c^2 b) = 2\\times{latex(M_mult)}\\times1.475\\text{{ km}}/({latex(R_mult)}\\times696000\\text{{ km}})$\n\n"
           f"GR: $\\delta = 4GM/(c^2 b)$ = twice the EP value")
    return Problem("Light Deflection", stmt, sol)

GENERATORS = [gen_redshift, gen_time_dilation_grav, gen_schwarzschild_radius, gen_light_deflection_ep]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, equivalence-principle, curved-spacetime]\nseed: {seed}\n---\n\n# 8.4 Practice — Equivalence Principle\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

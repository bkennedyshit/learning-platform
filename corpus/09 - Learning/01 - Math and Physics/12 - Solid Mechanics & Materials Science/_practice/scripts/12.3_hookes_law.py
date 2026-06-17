#!/usr/bin/env python3
"""
12.3_hookes_law.py — Practice problem generator for Chapter 12.3
(Hooke's Law & Material Properties).

Archetypes:
  1. 3D stress → strain (generalized Hooke's Law)
  2. Determine elastic constants from test data
  3. Biaxial stress (pressure vessel)
  4. Strain energy in a loaded member
  5. Plane stress stiffness matrix application

Usage:
  python 12.3_hookes_law.py --count 15 --seed 99
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_3d_strain(rng: random.Random) -> Problem:
    E = rng.choice([70, 100, 120, 200, 210])
    nu = rng.choice([sp.Rational(1,4), sp.Rational(3,10), sp.Rational(1,3)])
    sxx = rng.randint(-100, 200)
    syy = rng.randint(-100, 200)
    szz = rng.randint(-100, 200)
    exx = sp.Rational(1, E) * (sxx - nu*(syy + szz))
    eyy = sp.Rational(1, E) * (syy - nu*(sxx + szz))
    ezz = sp.Rational(1, E) * (szz - nu*(sxx + syy))
    stmt = (f"Steel: $E = {E}$ GPa, $\\nu = {sp.latex(nu)}$. Stress state: "
            f"$\\sigma_{{xx}} = {sxx}$, $\\sigma_{{yy}} = {syy}$, $\\sigma_{{zz}} = {szz}$ MPa (no shear). "
            f"Find all normal strains.")
    sol = (f"$\\varepsilon_{{xx}} = \\frac{{1}}{{{E}}}[{sxx} - {sp.latex(nu)}({syy}+{szz})] = "
           f"\\frac{{1}}{{{E}}}[{sxx} - {sp.latex(nu)}({syy+szz})] = {sp.latex(exx)}\\times10^{{-3}}$\n\n"
           f"$\\varepsilon_{{yy}} = \\frac{{1}}{{{E}}}[{syy} - {sp.latex(nu)}({sxx}+{szz})] = {sp.latex(eyy)}\\times10^{{-3}}$\n\n"
           f"$\\varepsilon_{{zz}} = \\frac{{1}}{{{E}}}[{szz} - {sp.latex(nu)}({sxx}+{syy})] = {sp.latex(ezz)}\\times10^{{-3}}$\n\n"
           f"Volumetric: $e = {sp.latex(exx+eyy+ezz)}\\times10^{{-3}}$")
    return Problem("3D generalized Hooke's Law", stmt, sol)

def gen_elastic_constants(rng: random.Random) -> Problem:
    E = rng.choice([70, 100, 120, 200])
    nu_num = rng.choice([25, 30, 33])
    nu = sp.Rational(nu_num, 100)
    G = sp.Rational(E * 100, 2*(100 + nu_num))
    K = sp.Rational(E * 100, 3*(100 - 2*nu_num))
    stmt = (f"A material has $E = {E}$ GPa and $\\nu = {sp.latex(nu)}$. "
            f"Compute the shear modulus $G$ and bulk modulus $K$.")
    sol = (f"$G = \\frac{{E}}{{2(1+\\nu)}} = \\frac{{{E}}}{{2(1+{sp.latex(nu)})}} = "
           f"\\frac{{{E}}}{{2 \\cdot {sp.latex(1+nu)}}} = {sp.latex(G)}$ GPa\n\n"
           f"$K = \\frac{{E}}{{3(1-2\\nu)}} = \\frac{{{E}}}{{3(1-{sp.latex(2*nu)})}} = "
           f"\\frac{{{E}}}{{3 \\cdot {sp.latex(1-2*nu)}}} = {sp.latex(K)}$ GPa")
    return Problem("Elastic constants relationship", stmt, sol)

def gen_pressure_vessel(rng: random.Random) -> Problem:
    E = 200
    nu = sp.Rational(3, 10)
    s1 = rng.choice([80, 100, 120, 150, 180])
    s2 = s1 // 2  # axial = hoop/2 for cylinder
    e1 = sp.Rational(1, E) * (s1 - nu * s2)
    e2 = sp.Rational(1, E) * (s2 - nu * s1)
    e3 = sp.Rational(-nu, E) * (s1 + s2)
    stmt = (f"Thin-walled cylinder (steel, $E={E}$ GPa, $\\nu={sp.latex(nu)}$): "
            f"$\\sigma_{{hoop}} = {s1}$ MPa, $\\sigma_{{axial}} = {s2}$ MPa, $\\sigma_{{radial}} = 0$. "
            f"Find all three strains.")
    sol = (f"$\\varepsilon_1 = \\frac{{1}}{{{E}}}[{s1} - {sp.latex(nu)}({s2})] = {sp.latex(e1)}\\times10^{{-3}}$\n\n"
           f"$\\varepsilon_2 = \\frac{{1}}{{{E}}}[{s2} - {sp.latex(nu)}({s1})] = {sp.latex(e2)}\\times10^{{-3}}$\n\n"
           f"$\\varepsilon_3 = \\frac{{-{sp.latex(nu)}}}{{{E}}}({s1}+{s2}) = {sp.latex(e3)}\\times10^{{-3}}$ (wall thins)")
    return Problem("Pressure vessel strains", stmt, sol)

def gen_strain_energy(rng: random.Random) -> Problem:
    E = rng.choice([70, 200, 210])
    L = rng.choice([1, 2, 3, 4])
    A = rng.choice([200, 400, 500, 800, 1000])
    P = rng.choice([20, 30, 40, 50, 60, 80, 100])
    sigma = sp.Rational(P * 1000, A)  # MPa
    U = sp.Rational(P**2 * 1000**2 * L, 2 * A * E * 10**6)  # Joules... let's keep symbolic
    delta = sp.Rational(P * L * 1000, A * E * 1000)  # mm
    U_val = sp.Rational(P**2 * L, 2 * A * E) * 1000  # in Joules (simplified)
    stmt = (f"A rod ($E={E}$ GPa, $L={L}$ m, $A={A}$ mm²) carries axial load $P={P}$ kN. "
            f"Find the elongation and strain energy stored.")
    sol = (f"$\\delta = \\frac{{PL}}{{AE}} = \\frac{{{P}\\times10^3 \\times {L}}}{{{A}\\times10^{{-6}} \\times {E}\\times10^9}}$\n\n"
           f"$= \\frac{{{P*L}\\times10^3}}{{{A*E}\\times10^3}} = {sp.latex(sp.Rational(P*L, A*E))}$ m "
           f"$= {float(sp.Rational(P*L*1000, A*E)):.3f}$ mm\n\n"
           f"$U = \\frac{{P^2 L}}{{2AE}} = \\frac{{{P}^2\\times10^6 \\times {L}}}{{2 \\times {A}\\times10^{{-6}} \\times {E}\\times10^9}}$"
           f" $= {float(sp.Rational(P**2 * L * 1000000, 2 * A * E * 1000)):.2f}$ J")
    return Problem("Strain energy in axial member", stmt, sol)

GENERATORS = [gen_3d_strain, gen_elastic_constants, gen_pressure_vessel, gen_strain_energy]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.3 Hooke's Law problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.3 Hooke's Law & Material Properties — Practice Problems\n",
             f"#review/mechanics  Generated {args.count} problems\n\n---\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("\n---\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Written {len(text)} bytes → {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()

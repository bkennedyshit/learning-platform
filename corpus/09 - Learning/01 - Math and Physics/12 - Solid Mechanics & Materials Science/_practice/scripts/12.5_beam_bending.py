#!/usr/bin/env python3
"""
12.5_beam_bending.py — Practice problem generator for Chapter 12.5
(Bending of Beams & Shear Stress).

Archetypes:
  1. Maximum bending stress (simply-supported, point load)
  2. Maximum bending stress (cantilever, uniform load)
  3. Shear stress at neutral axis (rectangular section)
  4. Cantilever deflection (point load)
  5. Section modulus design

Usage:
  python 12.5_beam_bending.py --count 15 --seed 42
"""
from __future__ import annotations
import argparse, random, math
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

def gen_bending_ss(rng: random.Random) -> Problem:
    L = rng.choice([3, 4, 5, 6, 8])
    P = rng.choice([10, 15, 20, 25, 30, 40, 50])
    b = rng.choice([50, 75, 100, 150])
    h = rng.choice([150, 200, 250, 300])
    M_max = P * L / 4  # kN·m (midspan load)
    I = b * h**3 / 12  # mm^4
    c = h / 2  # mm
    sigma = M_max * 1e6 * (c/1000) / (I * 1e-12)  # Pa
    sigma_MPa = sigma / 1e6
    stmt = (f"Simply-supported beam, $L = {L}$ m, midspan load $P = {P}$ kN. "
            f"Rectangular section ${b} \\times {h}$ mm. Find maximum bending stress.")
    sol = (f"$M_{{\\max}} = PL/4 = {P}\\times{L}/4 = {M_max}$ kN·m\n\n"
           f"$I = bh^3/12 = {b}\\times{h}^3/12 = {I:.0f}$ mm⁴ = ${I*1e-12:.4e}$ m⁴\n\n"
           f"$c = h/2 = {c}$ mm\n\n"
           f"$\\sigma_{{\\max}} = Mc/I = {M_max}\\times10^3 \\times {c/1000} / {I*1e-12:.4e} = {sigma_MPa:.1f}$ MPa")
    return Problem("Bending stress (SS beam, midspan load)", stmt, sol)

def gen_bending_cantilever(rng: random.Random) -> Problem:
    L = rng.choice([2, 3, 4, 5])
    w = rng.choice([3, 5, 6, 8, 10, 12])
    b = rng.choice([50, 75, 100])
    h = rng.choice([150, 200, 250, 300])
    M_max = w * L**2 / 2  # kN·m (at fixed end)
    I = b * h**3 / 12
    c = h / 2
    sigma_MPa = M_max * 1e6 * (c/1000) / (I * 1e-12) / 1e6
    stmt = (f"Cantilever beam, $L = {L}$ m, uniform load $w = {w}$ kN/m. "
            f"Section ${b} \\times {h}$ mm. Find maximum bending stress.")
    sol = (f"$M_{{\\max}} = wL^2/2 = {w}\\times{L}^2/2 = {M_max}$ kN·m (at fixed end)\n\n"
           f"$I = {b}\\times{h}^3/12 = {I:.0f}$ mm⁴\n\n"
           f"$\\sigma_{{\\max}} = Mc/I = {sigma_MPa:.1f}$ MPa")
    return Problem("Bending stress (cantilever, UDL)", stmt, sol)

def gen_shear_rect(rng: random.Random) -> Problem:
    L = rng.choice([3, 4, 5, 6])
    P = rng.choice([10, 15, 20, 30, 40])
    b = rng.choice([50, 75, 100])
    h = rng.choice([150, 200, 250, 300])
    V = P / 2  # kN (max shear at support for SS beam)
    A = b * h  # mm²
    tau_max = 1.5 * V * 1000 / A  # MPa (3V/2A for rectangle)
    stmt = (f"SS beam, $L={L}$ m, midspan load $P={P}$ kN. Section ${b}\\times{h}$ mm. "
            f"Find maximum shear stress (at support, neutral axis).")
    sol = (f"$V_{{\\max}} = P/2 = {V}$ kN (at supports)\n\n"
           f"For rectangular section: $\\tau_{{\\max}} = \\frac{{3V}}{{2A}} = \\frac{{3\\times{V}\\times10^3}}{{2\\times{A}}} = {tau_max:.2f}$ MPa\n\n"
           f"(Occurs at the neutral axis)")
    return Problem("Shear stress (rectangular beam)", stmt, sol)

def gen_deflection_cantilever(rng: random.Random) -> Problem:
    L = rng.choice([2, 3, 4, 5])
    P = rng.choice([5, 8, 10, 15, 20])
    E = rng.choice([70, 200, 210])
    b = rng.choice([50, 75, 100])
    h = rng.choice([100, 150, 200, 250])
    I = b * h**3 / 12  # mm^4
    I_m4 = I * 1e-12
    delta = P * 1000 * L**3 / (3 * E * 1e9 * I_m4)  # m
    stmt = (f"Cantilever ($E={E}$ GPa), $L={L}$ m, tip load $P={P}$ kN. "
            f"Section ${b}\\times{h}$ mm. Find tip deflection.")
    sol = (f"$I = {b}\\times{h}^3/12 = {I:.0f}$ mm⁴ = ${I_m4:.4e}$ m⁴\n\n"
           f"$\\delta = \\frac{{PL^3}}{{3EI}} = \\frac{{{P}\\times10^3 \\times {L}^3}}{{3\\times{E}\\times10^9\\times{I_m4:.4e}}}$\n\n"
           f"$= {delta*1000:.2f}$ mm")
    return Problem("Cantilever deflection (tip load)", stmt, sol)

def gen_section_design(rng: random.Random) -> Problem:
    M = rng.choice([10, 15, 20, 30, 50, 80])
    sigma_allow = rng.choice([120, 150, 160, 200, 250])
    S_req = M * 1e6 / (sigma_allow * 1e6) * 1e6  # mm³
    stmt = (f"A beam must resist $M = {M}$ kN·m with allowable stress $\\sigma_{{allow}} = {sigma_allow}$ MPa. "
            f"Find the required section modulus $S$.")
    sol = (f"$S_{{req}} = M/\\sigma_{{allow}} = {M}\\times10^6 / ({sigma_allow}\\times10^6) \\times 10^6$\n\n"
           f"$= {M*1e6/(sigma_allow*1e6)*1e6:.0f}$ mm³ = ${M/sigma_allow*1e6:.0f}$ mm³\n\n"
           f"Select a beam with $S \\geq {S_req:.0f}$ mm³ from steel tables.")
    return Problem("Section modulus design", stmt, sol)

GENERATORS = [gen_bending_ss, gen_bending_cantilever, gen_shear_rect,
              gen_deflection_cantilever, gen_section_design]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.5 Beam Bending problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.5 Bending of Beams & Shear Stress — Practice Problems\n",
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

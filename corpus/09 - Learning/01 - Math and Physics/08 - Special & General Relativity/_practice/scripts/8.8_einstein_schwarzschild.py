#!/usr/bin/env python3
"""
8.8_einstein_schwarzschild.py — Practice problems for Chapter 8.8
(Einstein Field Equations & Schwarzschild Black Holes).

Archetypes:
  1. Schwarzschild radius computation
  2. Effective potential and ISCO
  3. Perihelion precession calculation
  4. Light deflection angle
  5. Radial infall proper time
  6. Friedmann equation application
  7. Photon sphere radius
  8. Gravitational wave frequency estimate

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, simplify, sqrt, pi

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_precession(rng: random.Random) -> Problem:
    # Mercury-like parameters
    a_AU = Rational(rng.choice([387, 723, 1000]),1000)  # semi-major in AU
    e = Rational(rng.choice([206, 7, 17]),1000)  # eccentricity
    a_m = simplify(a_AU * Rational(1496,10))  # x10^8 m (simplified)
    stmt = (f"A planet orbits at $a = {latex(a_AU)}$ AU with eccentricity $e = {latex(e)}$. "
            "Compute the GR perihelion precession per orbit (in arcseconds).")
    sol = (f"$\\Delta\\phi = \\frac{{6\\pi GM_\\odot}}{{c^2 a(1-e^2)}}$\n\n"
           f"$= \\frac{{6\\pi \\times 1.475\\text{{ km}}}}{{{latex(a_AU)} \\times 1.496\\times10^8\\text{{ km}} "
           f"\\times (1-{latex(e)}^2)}}$\n\n"
           f"Convert to arcseconds: multiply by $206265''$/rad")
    return Problem("Perihelion Precession", stmt, sol)

def gen_light_deflection(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1,2,5,10]),1)
    b_mult = Rational(rng.choice([1,2,3,5]),1)
    # delta = 4GM/(c^2 b), with GM_sun/c^2 = 1.475 km, R_sun = 696000 km
    stmt = (f"Compute the GR light deflection angle for a photon passing at "
            f"${latex(b_mult)}R_\\odot$ from a star of mass ${latex(M_mult)}M_\\odot$.")
    sol = (f"$\\delta = \\frac{{4GM}}{{c^2 b}} = \\frac{{4 \\times {latex(M_mult)} \\times 1.475\\text{{ km}}}}"
           f"{{{latex(b_mult)} \\times 696000\\text{{ km}}}}$\n\n"
           f"$= {latex(simplify(4*M_mult*Rational(1475,1000)/(b_mult*696000)))}$ rad\n\n"
           f"Convert: $\\times 206265 = $ arcseconds")
    return Problem("Light Deflection (GR)", stmt, sol)

def gen_isco(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1,5,10,4000000]),1)
    r_isco_km = simplify(3 * M_mult * Rational(295,100))
    stmt = f"Find the ISCO radius for a Schwarzschild black hole of mass ${latex(M_mult)}M_\\odot$."
    sol = (f"$r_{{ISCO}} = 6GM/c^2 = 3r_s = 3 \\times {latex(M_mult)} \\times 2.95\\text{{ km}} = {latex(r_isco_km)}$ km\n\n"
           f"$r_{{photon}} = 3GM/c^2 = 1.5r_s = {latex(simplify(r_isco_km/2))}$ km")
    return Problem("ISCO & Photon Sphere", stmt, sol)

def gen_infall_time(rng: random.Random) -> Problem:
    M_mult = Rational(rng.choice([1,10,4000000]),1)
    rs_m = simplify(M_mult * Rational(2950,1))  # meters
    tau = simplify(2*rs_m/(3*Rational(3,1)*10**8))  # very rough
    stmt = (f"Estimate the proper time for radial infall from the horizon to the singularity "
            f"for a ${latex(M_mult)}M_\\odot$ black hole.")
    sol = (f"$\\Delta\\tau = 2r_s/(3c) = 2 \\times {latex(M_mult)} \\times 2.95\\text{{ km}} / (3 \\times 3\\times10^5\\text{{ km/s}})$\n\n"
           f"$= {latex(simplify(2*M_mult*Rational(295,100)/(3*300000)))}$ seconds\n\n"
           f"For solar mass: $\\sim 6.6\\,\\mu$s. For Sgr A*: $\\sim 26$ s.")
    return Problem("Radial Infall Proper Time", stmt, sol)

def gen_friedmann(rng: random.Random) -> Problem:
    H0 = Rational(70,1)  # km/s/Mpc
    stmt = (f"Given $H_0 = {latex(H0)}$ km/s/Mpc, compute the critical density "
            "$\\rho_c = 3H_0^2/(8\\pi G)$.")
    sol = ("$H_0 = 70$ km/s/Mpc $= 70/(3.086\\times10^{19})$ s$^{-1}$ $= 2.27\\times10^{-18}$ s$^{-1}$\n\n"
           "$\\rho_c = 3H_0^2/(8\\pi G) = 3(2.27\\times10^{-18})^2/(8\\pi \\times 6.674\\times10^{-11})$\n\n"
           "$= 9.2\\times10^{-27}$ kg/m$^3$ $\\approx 5.5$ protons/m$^3$")
    return Problem("Friedmann Critical Density", stmt, sol)

GENERATORS = [gen_precession, gen_light_deflection, gen_isco, gen_infall_time, gen_friedmann]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=15)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, einstein-equations, schwarzschild, black-holes]\nseed: {seed}\n---\n\n# 8.8 Practice — Einstein Field Equations & Black Holes\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

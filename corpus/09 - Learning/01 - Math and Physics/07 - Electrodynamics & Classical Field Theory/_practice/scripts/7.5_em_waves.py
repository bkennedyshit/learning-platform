#!/usr/bin/env python3
"""
7.5_em_waves.py — Practice problem generator for Chapter 7.5
(Electromagnetic Wave Propagation & Poynting Vector).

Archetypes:
  1. Poynting vector / intensity calculation
  2. Radiation pressure
  3. Fresnel reflection at normal incidence
  4. Polarization state identification
  5. Wavelength / frequency / energy relations

Usage: python 7.5_em_waves.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Rational, latex, sqrt, pi

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_intensity(rng: random.Random) -> Problem:
    E0 = rng.randint(50, 500)
    c = 3e8
    eps0 = 8.854e-12
    I = 0.5 * c * eps0 * E0**2
    stmt = f"A plane wave has peak electric field $E_0 = {E0}$ V/m. Find the time-averaged intensity."
    sol = (f"$$I = \\frac{{1}}{{2}}c\\varepsilon_0 E_0^2 = \\frac{{1}}{{2}}(3\\times10^8)(8.854\\times10^{{-12}})({E0})^2$$\n\n"
           f"$$I = {I:.4f} \\text{{ W/m}}^2$$")
    return Problem("Intensity from E-field amplitude", stmt, sol)

def gen_radiation_pressure(rng: random.Random) -> Problem:
    I = rng.randint(100, 2000)
    reflecting = rng.choice([True, False])
    P = (2*I if reflecting else I) / 3e8
    surface = "perfectly reflecting" if reflecting else "perfectly absorbing"
    stmt = f"Light of intensity $I = {I}$ W/m² hits a {surface} surface. Find the radiation pressure."
    factor = "2I/c" if reflecting else "I/c"
    sol = f"$$P = {factor} = {'{:.2e}'.format(P)} \\text{{ Pa}}$$"
    return Problem("Radiation pressure", stmt, sol)

def gen_fresnel_normal(rng: random.Random) -> Problem:
    n1 = 1
    n2 = rng.choice([Rational(3,2), Rational(5,3), 2, Rational(5,2)])
    r = (n1 - n2) / (n1 + n2)
    R = r**2
    T = 1 - R
    stmt = f"Light passes from air ($n_1=1$) into a medium with $n_2 = {latex(n2)}$ at normal incidence. Find $R$ and $T$."
    sol = (f"$$r = \\frac{{n_1-n_2}}{{n_1+n_2}} = \\frac{{1-{latex(n2)}}}{{1+{latex(n2)}}} = {latex(r)}$$\n\n"
           f"$$R = r^2 = {latex(R)}$$\n\n$$T = 1 - R = {latex(T)}$$")
    return Problem("Fresnel reflection (normal incidence)", stmt, sol)

def gen_wavelength(rng: random.Random) -> Problem:
    f_val = rng.choice([1e9, 5e9, 2.4e9, 1e14, 5e14])
    lam = 3e8 / f_val
    stmt = f"Find the wavelength of an EM wave with frequency $f = {f_val:.2e}$ Hz."
    sol = f"$$\\lambda = c/f = (3\\times10^8)/({f_val:.2e}) = {lam:.4e} \\text{{ m}}$$"
    return Problem("Wavelength-frequency relation", stmt, sol)

GENERATORS = [gen_intensity, gen_radiation_pressure, gen_fresnel_normal, gen_wavelength]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, em-waves, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.5 EM Waves — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
16.3_stoichiometry.py — Practice problem generator for Chapter 16.3
(Stoichiometry & Reactions).

Generates randomized drill problems:
  1. Mole/mass/particle conversions
  2. Limiting reagent calculations
  3. Percent yield problems
  4. Solution dilution (M1V1 = M2V2)
  5. Balancing equations (simple)

Usage:
  python 16.3_stoichiometry.py
  python 16.3_stoichiometry.py --count 20 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

MOLAR_MASSES = {"H2O": 18.02, "CO2": 44.01, "NaCl": 58.44, "CaCO3": 100.09,
                "Fe2O3": 159.69, "Al2O3": 101.96, "C6H12O6": 180.16,
                "NH3": 17.03, "H2SO4": 98.08, "NaOH": 40.00, "HCl": 36.46}

def gen_mole_conversion(rng: random.Random) -> Problem:
    compound = rng.choice(list(MOLAR_MASSES.keys()))
    M = MOLAR_MASSES[compound]
    mass = round(rng.uniform(5, 200), 1)
    moles = mass / M
    particles = moles * 6.022e23
    stmt = (f"Convert {mass} g of {compound} (M = {M} g/mol) to:\n"
            f"(a) moles, (b) number of molecules.")
    sol = (f"(a) $n = {mass}/{M} = {moles:.4f}$ mol\n\n"
           f"(b) $N = {moles:.4f} \\times 6.022 \\times 10^{{23}} = {particles:.3e}$ molecules")
    return Problem("Mole-mass-particle conversion", stmt, sol)

def gen_limiting_reagent(rng: random.Random) -> Problem:
    reactions = [
        ("2H2 + O2 -> 2H2O", ["H2","O2","H2O"], [2,1,2], [2.016,32.00,18.02]),
        ("N2 + 3H2 -> 2NH3", ["N2","H2","NH3"], [1,3,2], [28.02,2.016,17.03]),
        ("2Al + 3Cl2 -> 2AlCl3", ["Al","Cl2","AlCl3"], [2,3,2], [26.98,70.90,133.34]),
    ]
    rxn_str, species, coeffs, masses_mol = rng.choice(reactions)
    m1 = round(rng.uniform(5, 50), 1)
    m2 = round(rng.uniform(5, 50), 1)
    n1 = m1 / masses_mol[0]
    n2 = m2 / masses_mol[1]
    ratio_needed = coeffs[1] / coeffs[0]
    n2_needed = n1 * ratio_needed
    if n2 < n2_needed:
        limiting = species[1]
        n_product = n2 * (coeffs[2] / coeffs[1])
    else:
        limiting = species[0]
        n_product = n1 * (coeffs[2] / coeffs[0])
    m_product = n_product * masses_mol[2]
    stmt = (f"For the reaction: ${rxn_str}$\n\n"
            f"If {m1} g of {species[0]} reacts with {m2} g of {species[1]}, "
            f"determine the limiting reagent and theoretical yield of {species[2]}.")
    sol = (f"$n_{{{species[0]}}} = {m1}/{masses_mol[0]} = {n1:.4f}$ mol\n\n"
           f"$n_{{{species[1]}}} = {m2}/{masses_mol[1]} = {n2:.4f}$ mol\n\n"
           f"Limiting reagent: **{limiting}**\n\n"
           f"Theoretical yield: ${n_product:.4f}$ mol × {masses_mol[2]} g/mol = **{m_product:.2f} g** of {species[2]}")
    return Problem("Limiting reagent & theoretical yield", stmt, sol)

def gen_percent_yield(rng: random.Random) -> Problem:
    theoretical = round(rng.uniform(10, 100), 1)
    pct = round(rng.uniform(50, 95), 1)
    actual = round(theoretical * pct / 100, 2)
    stmt = (f"A reaction has a theoretical yield of {theoretical} g. "
            f"If {actual} g of product is obtained, what is the percent yield?")
    sol = f"$\\%\\text{{yield}} = \\frac{{{actual}}}{{{theoretical}}} \\times 100\\% = {pct:.1f}\\%$"
    return Problem("Percent yield", stmt, sol)

def gen_dilution(rng: random.Random) -> Problem:
    c1 = round(rng.uniform(0.5, 6.0), 2)
    v1 = round(rng.uniform(10, 100), 1)
    c2 = round(rng.uniform(0.01, c1 * 0.5), 3)
    v2 = c1 * v1 / c2
    stmt = (f"What volume of {c1} M HCl must be diluted to prepare a solution with "
            f"concentration {c2} M, starting from {v1} mL?")
    sol = (f"$c_1 V_1 = c_2 V_2$\n\n"
           f"$V_2 = \\frac{{c_1 V_1}}{{c_2}} = \\frac{{{c1} \\times {v1}}}{{{c2}}} = {v2:.1f}$ mL")
    return Problem("Dilution (M₁V₁ = M₂V₂)", stmt, sol)

ARCHETYPES = [gen_mole_conversion, gen_limiting_reagent, gen_percent_yield, gen_dilution]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or Path(__file__).resolve().parent.parent / "16.3_drills.md"
    problems = [rng.choice(ARCHETYPES)(rng) for _ in range(args.count)]
    header = (f"---\ntags: [chemistry, stoichiometry, practice]\nchapter: 16.3\n"
              f"type: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n"
              f"# Chapter 16.3 — Practice: Stoichiometry\n\n---\n\n")
    body = "\n\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body + "\n", encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

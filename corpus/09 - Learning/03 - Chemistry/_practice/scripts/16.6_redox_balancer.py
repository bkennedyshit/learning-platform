#!/usr/bin/env python3
"""
16.6_redox_balancer.py — Practice problem generator for Chapter 16.6
(Electrochemistry & Redox).

Generates randomized drill problems:
  1. Cell potential from standard reduction potentials
  2. Nernst equation calculations
  3. Faraday's law (electrolysis mass/time)
  4. ΔG from E°cell

Usage:
  python 16.6_redox_balancer.py
  python 16.6_redox_balancer.py --count 20 --seed 42
"""
from __future__ import annotations
import argparse, random, math
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

HALF_CELLS = [
    ("Zn2+/Zn", -0.76, "Zn", 65.38, 2),
    ("Cu2+/Cu", 0.34, "Cu", 63.55, 2),
    ("Ag+/Ag", 0.80, "Ag", 107.87, 1),
    ("Fe2+/Fe", -0.44, "Fe", 55.85, 2),
    ("Ni2+/Ni", -0.26, "Ni", 58.69, 2),
    ("Sn2+/Sn", -0.14, "Sn", 118.71, 2),
    ("Pb2+/Pb", -0.13, "Pb", 207.2, 2),
    ("Au3+/Au", 1.50, "Au", 196.97, 3),
]

def gen_cell_potential(rng: random.Random) -> Problem:
    c1, c2 = rng.sample(HALF_CELLS, 2)
    name1, E1, _, _, n1 = c1
    name2, E2, _, _, n2 = c2
    if E1 > E2:
        cathode, anode = c1, c2
    else:
        cathode, anode = c2, c1
    E_cell = cathode[1] - anode[1]
    n = min(cathode[4], anode[4])  # simplified
    dG = -n * 96485 * E_cell / 1000
    stmt = (f"Calculate $E^\\circ_{{\\text{{cell}}}}$ and $\\Delta G^\\circ$ for a cell with:\n"
            f"- Cathode: {cathode[0]} ($E^\\circ = {cathode[1]:+.2f}$ V)\n"
            f"- Anode: {anode[0]} ($E^\\circ = {anode[1]:+.2f}$ V)\n\n"
            f"Use $n = {n}$ electrons transferred.")
    sol = (f"$E^\\circ_{{\\text{{cell}}}} = E^\\circ_{{\\text{{cathode}}}} - E^\\circ_{{\\text{{anode}}}} "
           f"= {cathode[1]:+.2f} - ({anode[1]:+.2f}) = {E_cell:+.2f}$ V\n\n"
           f"$\\Delta G^\\circ = -nFE^\\circ = -({n})(96485)({E_cell:.2f}) = {dG:.1f}$ kJ/mol")
    return Problem("Standard cell potential & ΔG°", stmt, sol)

def gen_nernst(rng: random.Random) -> Problem:
    c1, c2 = rng.sample(HALF_CELLS, 2)
    if c1[1] > c2[1]:
        cathode, anode = c1, c2
    else:
        cathode, anode = c2, c1
    E_std = cathode[1] - anode[1]
    n = 2
    conc_cat = round(10**rng.uniform(-3, 0), 4)
    conc_an = round(10**rng.uniform(-3, 0), 4)
    Q = conc_an / conc_cat
    E = E_std - (0.0592/n) * math.log10(Q)
    stmt = (f"For the cell {anode[0]}|{cathode[0]} with $E^\\circ = {E_std:.2f}$ V, $n = {n}$:\n\n"
            f"Calculate $E$ when $[\\text{{anode ion}}] = {conc_an}$ M and $[\\text{{cathode ion}}] = {conc_cat}$ M.")
    sol = (f"$Q = \\frac{{[\\text{{product}}]}}{{[\\text{{reactant}}]}} = \\frac{{{conc_an}}}{{{conc_cat}}} = {Q:.4f}$\n\n"
           f"$E = E^\\circ - \\frac{{0.0592}}{{{n}}}\\log Q = {E_std:.2f} - \\frac{{0.0592}}{{{n}}}\\log({Q:.4f})$\n\n"
           f"$= {E_std:.2f} - {0.0592/n:.4f} \\times ({math.log10(Q):.3f}) = {E:.3f}$ V")
    return Problem("Nernst equation", stmt, sol)

def gen_faraday(rng: random.Random) -> Problem:
    _, _, metal, M, n = rng.choice(HALF_CELLS)
    current = round(rng.uniform(1, 10), 2)
    time_min = rng.randint(10, 120)
    time_s = time_min * 60
    charge = current * time_s
    moles_e = charge / 96485
    moles_metal = moles_e / n
    mass = moles_metal * M
    stmt = (f"A current of {current} A flows for {time_min} minutes through a solution of {metal}$^{{{n}+}}$. "
            f"How many grams of {metal} are deposited? ($M = {M}$ g/mol, $n = {n}$)")
    sol = (f"$Q = It = {current} \\times {time_s} = {charge:.0f}$ C\n\n"
           f"$n_{{e^-}} = Q/F = {charge:.0f}/96485 = {moles_e:.5f}$ mol\n\n"
           f"$n_{{\\text{{{metal}}}}} = {moles_e:.5f}/{n} = {moles_metal:.5f}$ mol\n\n"
           f"$m = {moles_metal:.5f} \\times {M} = {mass:.3f}$ g")
    return Problem("Faraday's law (electrolysis)", stmt, sol)

ARCHETYPES = [gen_cell_potential, gen_nernst, gen_faraday]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or Path(__file__).resolve().parent.parent / "16.6_drills.md"
    problems = [rng.choice(ARCHETYPES)(rng) for _ in range(args.count)]
    header = (f"---\ntags: [chemistry, electrochemistry, redox, practice]\nchapter: 16.6\n"
              f"type: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n"
              f"# Chapter 16.6 — Practice: Electrochemistry & Redox\n\n---\n\n")
    body = "\n\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body + "\n", encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

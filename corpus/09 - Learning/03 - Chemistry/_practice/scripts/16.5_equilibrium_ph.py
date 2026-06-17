#!/usr/bin/env python3
"""
16.5_equilibrium_ph.py — Practice problem generator for Chapter 16.5
(Acids, Bases & Equilibrium).

Generates randomized drill problems:
  1. pH of strong acid/base
  2. pH of weak acid (Ka given)
  3. Buffer pH (Henderson-Hasselbalch)
  4. Ksp and molar solubility
  5. Equilibrium constant from concentrations

Usage:
  python 16.5_equilibrium_ph.py
  python 16.5_equilibrium_ph.py --count 20 --seed 42
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

def gen_strong_acid_ph(rng: random.Random) -> Problem:
    acids = ["HCl", "HNO3", "HBr"]
    acid = rng.choice(acids)
    conc = round(10**rng.uniform(-4, -1), 4)
    pH = -math.log10(conc)
    stmt = f"Calculate the pH of {conc} M {acid} solution."
    sol = (f"{acid} is a strong acid (100% dissociation).\n\n"
           f"$[\\text{{H}}^+] = {conc}$ M\n\n"
           f"$\\text{{pH}} = -\\log({conc}) = {pH:.2f}$")
    return Problem("pH of strong acid", stmt, sol)

def gen_weak_acid_ph(rng: random.Random) -> Problem:
    acids = [("CH3COOH", "acetic acid", 1.8e-5),
             ("HF", "hydrofluoric acid", 6.8e-4),
             ("HCN", "hydrocyanic acid", 6.2e-10),
             ("HCOOH", "formic acid", 1.8e-4)]
    formula, name, Ka = rng.choice(acids)
    conc = round(rng.uniform(0.01, 0.5), 3)
    x = math.sqrt(Ka * conc)
    pH = -math.log10(x)
    pct = (x / conc) * 100
    stmt = (f"Calculate the pH of {conc} M {name} ({formula}). "
            f"$K_a = {Ka:.2e}$.")
    sol = (f"Weak acid equilibrium: $K_a = x^2/(C_0 - x) \\approx x^2/C_0$\n\n"
           f"$x = \\sqrt{{K_a \\cdot C_0}} = \\sqrt{{{Ka:.2e} \\times {conc}}} = {x:.4e}$ M\n\n"
           f"Check 5% rule: ${pct:.1f}\\%$ {'< 5% ✓' if pct < 5 else '> 5% — use quadratic'}\n\n"
           f"$\\text{{pH}} = -\\log({x:.4e}) = {pH:.2f}$")
    return Problem("pH of weak acid", stmt, sol)

def gen_buffer_ph(rng: random.Random) -> Problem:
    buffers = [("CH3COOH/CH3COO-", 4.74), ("NH4+/NH3", 9.25),
               ("H2PO4-/HPO4^2-", 7.20), ("HCO3-/CO3^2-", 10.33)]
    name, pKa = rng.choice(buffers)
    c_acid = round(rng.uniform(0.05, 0.5), 3)
    c_base = round(rng.uniform(0.05, 0.5), 3)
    ratio = c_base / c_acid
    pH = pKa + math.log10(ratio)
    stmt = (f"Calculate the pH of a buffer containing {c_acid} M acid and "
            f"{c_base} M conjugate base for the {name} system (p$K_a$ = {pKa}).")
    sol = (f"Henderson-Hasselbalch: $\\text{{pH}} = \\text{{p}}K_a + \\log\\frac{{[A^-]}}{{[HA]}}$\n\n"
           f"$= {pKa} + \\log\\frac{{{c_base}}}{{{c_acid}}} = {pKa} + \\log({ratio:.3f}) = {pKa} + ({math.log10(ratio):.3f}) = {pH:.2f}$")
    return Problem("Buffer pH (Henderson-Hasselbalch)", stmt, sol)

def gen_ksp_solubility(rng: random.Random) -> Problem:
    salts = [("AgCl", "Ag+ + Cl-", 1.8e-10, 1, 1),
             ("PbI2", "Pb2+ + 2I-", 9.8e-9, 1, 2),
             ("Ca(OH)2", "Ca2+ + 2OH-", 4.7e-6, 1, 2),
             ("BaSO4", "Ba2+ + SO4^2-", 1.1e-10, 1, 1)]
    formula, eq, Ksp, m, n = rng.choice(salts)
    coeff = m**m * n**n
    s = (Ksp / coeff) ** (1/(m+n))
    stmt = (f"Calculate the molar solubility of {formula} in pure water. "
            f"$K_{{sp}} = {Ksp:.2e}$. Dissolution: {formula} ⇌ {eq}.")
    sol = (f"Let solubility = $s$. Then $[\\text{{cation}}] = {m}s$, $[\\text{{anion}}] = {n}s$.\n\n"
           f"$K_{{sp}} = ({m}s)^{m}({n}s)^{n} = {coeff}s^{m+n} = {Ksp:.2e}$\n\n"
           f"$s = \\left(\\frac{{{Ksp:.2e}}}{{{coeff}}}\\right)^{{1/{m+n}}} = {s:.3e}$ M")
    return Problem("Ksp & molar solubility", stmt, sol)

ARCHETYPES = [gen_strong_acid_ph, gen_weak_acid_ph, gen_buffer_ph, gen_ksp_solubility]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or Path(__file__).resolve().parent.parent / "16.5_drills.md"
    problems = [rng.choice(ARCHETYPES)(rng) for _ in range(args.count)]
    header = (f"---\ntags: [chemistry, equilibrium, pH, practice]\nchapter: 16.5\n"
              f"type: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n"
              f"# Chapter 16.5 — Practice: Acids, Bases & Equilibrium\n\n---\n\n")
    body = "\n\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body + "\n", encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

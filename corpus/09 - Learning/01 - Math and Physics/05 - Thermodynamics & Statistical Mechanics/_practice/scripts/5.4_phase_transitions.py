#!/usr/bin/env python3
"""
5.4_phase_transitions.py — Practice problem generator for Chapter 5.4
(Chemical Potential & Phase Transitions).

Archetypes:
  1. Clausius-Clapeyron: slope of coexistence curve
  2. Boiling point at different pressure
  3. Gibbs phase rule application
  4. Van der Waals critical point
  5. Latent heat from P-T data
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx):
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

R = 8.314

def gen_cc_slope(rng: random.Random) -> Problem:
    L = rng.choice([6010, 40700, 2260000])  # J/mol for fusion, vap(mol), vap(kg)
    name = {6010:"ice-water fusion",40700:"water vaporization",2260000:"water vap(per kg)"}[L]
    T = rng.choice([273, 373, 350])
    dv = rng.choice([1.6e-6, 30.1e-3, 1.67])  # m^3/mol or m^3/kg
    slope = L/(T*dv)
    stmt = (f"For {name} at $T = {T}\\,\\text{{K}}$: $L = {L}\\,\\text{{J/mol}}$, "
            f"$\\Delta v = {dv:.2e}\\,\\text{{m}}^3/\\text{{mol}}$. Find $dP/dT$.")
    sol = f"$dP/dT = L/(T\\Delta v) = {L}/({T} \\times {dv:.2e}) = {slope:.2e}\\,\\text{{Pa/K}}$."
    return Problem("Clausius-Clapeyron slope", stmt, sol)

def gen_boiling_alt(rng: random.Random) -> Problem:
    T1 = 373; P1 = 101325
    L = 40700
    P2 = rng.choice([80000, 70000, 60000, 50000])
    inv_T2 = 1/T1 - R*math.log(P2/P1)/L
    T2 = 1/inv_T2
    stmt = (f"Water boils at $373\\,\\text{{K}}$ at $101.3\\,\\text{{kPa}}$. "
            f"At what temperature does it boil at $P = {P2/1000:.0f}\\,\\text{{kPa}}$? ($L = 40.7\\,\\text{{kJ/mol}}$)")
    sol = (f"Integrated C-C: $\\ln(P_2/P_1) = -(L/R)(1/T_2 - 1/T_1)$.\n\n"
           f"$1/T_2 = 1/{T1} - (R/L)\\ln(P_2/P_1) = {1/T1:.6f} - ({R}/{L})\\ln({P2/P1:.4f})$\n\n"
           f"$= {1/T1:.6f} - {R/L:.6f} \\times {math.log(P2/P1):.4f} = {inv_T2:.6f}$\n\n"
           f"$T_2 = {T2:.1f}\\,\\text{{K}} = {T2-273.15:.1f}°\\text{{C}}$.")
    return Problem("Boiling point at altitude", stmt, sol)

def gen_phase_rule(rng: random.Random) -> Problem:
    C = rng.choice([1,2,3])
    Ph = rng.choice([p for p in [1,2,3] if C-p+2 >= 0])
    F = C - Ph + 2
    desc = {(1,1):"pure substance, single phase",(1,2):"pure substance, two-phase coexistence",
            (1,3):"pure substance at triple point",(2,1):"binary mixture, single phase",
            (2,2):"binary at boiling",(2,3):"binary eutectic point",
            (3,1):"ternary single phase",(3,2):"ternary two-phase",(3,3):"ternary three-phase"}
    d = desc.get((C,Ph), f"{C}-component, {Ph}-phase system")
    stmt = f"Apply the Gibbs phase rule to a {d} ($C={C}$, $P={Ph}$). How many degrees of freedom?"
    sol = f"$F = C - P + 2 = {C} - {Ph} + 2 = {F}$. There are **{F}** independent intensive variables."
    return Problem("Gibbs phase rule", stmt, sol)

def gen_vdw_critical(rng: random.Random) -> Problem:
    a = rng.choice([0.1, 0.2, 0.5, 1.0, 3.6])
    b = rng.choice([2e-5, 3e-5, 4e-5, 5e-5])
    Tc = 8*a/(27*R*b); Pc = a/(27*b**2); Vc = 3*b
    stmt = (f"For a van der Waals gas with $a = {a}\\,\\text{{Pa·m}}^6/\\text{{mol}}^2$ and "
            f"$b = {b:.1e}\\,\\text{{m}}^3/\\text{{mol}}$, find $T_c$, $P_c$, $V_c$.")
    sol = (f"$T_c = 8a/(27Rb) = 8({a})/(27 \\times {R} \\times {b:.1e}) = {Tc:.1f}\\,\\text{{K}}$.\n\n"
           f"$P_c = a/(27b^2) = {a}/(27 \\times ({b:.1e})^2) = {Pc:.2e}\\,\\text{{Pa}}$.\n\n"
           f"$V_c = 3b = 3 \\times {b:.1e} = {Vc:.2e}\\,\\text{{m}}^3/\\text{{mol}}$.")
    return Problem("Van der Waals critical point", stmt, sol)

def gen_latent_from_data(rng: random.Random) -> Problem:
    T = rng.choice([273, 300, 350, 373])
    dPdT = rng.choice([1.35e7, 3.5e3, 1.0e4])
    dv = rng.choice([1.6e-6, 30e-3, 20e-3])
    L = T*dv*dPdT
    stmt = (f"At $T = {T}\\,\\text{{K}}$, the coexistence curve slope is $dP/dT = {dPdT:.2e}\\,\\text{{Pa/K}}$ "
            f"and $\\Delta v = {dv:.2e}\\,\\text{{m}}^3/\\text{{mol}}$. Find the latent heat.")
    sol = f"$L = T\\Delta v(dP/dT) = {T} \\times {dv:.2e} \\times {dPdT:.2e} = {L:.0f}\\,\\text{{J/mol}} = {L/1000:.2f}\\,\\text{{kJ/mol}}$."
    return Problem("Latent heat from slope", stmt, sol)

ARCHETYPES = [gen_cc_slope, gen_boiling_alt, gen_phase_rule, gen_vdw_critical, gen_latent_from_data]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.4_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [thermodynamics, phase-transitions, practice, \"#review/math\"]\nchapter: 5.4\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.4 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

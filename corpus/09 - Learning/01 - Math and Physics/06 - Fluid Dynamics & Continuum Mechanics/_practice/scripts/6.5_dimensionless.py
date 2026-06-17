#!/usr/bin/env python3
"""
6.5_dimensionless.py — Practice problem generator for Chapter 6.5
(Dimensionless Numbers — Reynolds & Froude).

Archetypes:
  1. Buckingham Pi theorem (count Pi groups)
  2. Reynolds number for various scenarios
  3. Froude number and wave speed
  4. Model-prototype scaling (Froude similarity)
  5. Identify dominant forces from dimensionless numbers

Usage:
  python 6.5_dimensionless.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )

def gen_pi_count(rng: random.Random) -> Problem:
    n = rng.randint(5, 8)
    k = 3
    p = n - k
    stmt = (f"A physical problem involves $n={n}$ variables expressible in $k={k}$ fundamental "
            f"dimensions (M, L, T). How many independent dimensionless groups exist?")
    sol = f"By Buckingham Pi: $p = n - r = {n} - {k} = {p}$ dimensionless groups (assuming rank $r={k}$)."
    return Problem("Buckingham Pi count", stmt, sol)

def gen_re_scenario(rng: random.Random) -> Problem:
    scenarios = [
        ("blood in capillary", 0.001, 0.01, 3.3e-6),
        ("submarine", 10, 100, 1.1e-6),
        ("oil pipeline", 2, 0.5, 5e-5),
        ("airplane wing", 250, 3, 1.5e-5),
    ]
    name, U, L, nu = rng.choice(scenarios)
    Re = U * L / nu
    stmt = f"Compute Re for {name}: $U={U}$ m/s, $L={L}$ m, $\\nu={nu}$ m²/s."
    regime = "Stokes" if Re < 1 else "laminar" if Re < 2300 else "turbulent"
    sol = f"$\\text{{Re}} = UL/\\nu = {U}\\times{L}/{nu} = {Re:.0f}$. Regime: **{regime}**."
    return Problem("Reynolds number scenario", stmt, sol)

def gen_froude(rng: random.Random) -> Problem:
    U = rng.randint(2, 20)
    L = rng.choice([1, 5, 10, 50, 100])
    g = 9.81
    Fr = U / math.sqrt(g * L)
    stmt = f"A ship moves at $U={U}$ m/s with waterline length $L={L}$ m. Compute the Froude number."
    sol = (f"$\\text{{Fr}} = U/\\sqrt{{gL}} = {U}/\\sqrt{{9.81\\times{L}}} = "
           f"{U}/{math.sqrt(g*L):.2f} = {Fr:.3f}$.\n\n"
           + ("Subcritical (Fr < 1): gravity waves propagate upstream." if Fr < 1
              else "Supercritical (Fr > 1): gravity waves cannot propagate upstream."))
    return Problem("Froude number", stmt, sol)

def gen_model_scaling(rng: random.Random) -> Problem:
    lam = rng.choice([10, 20, 50, 100])
    Up = rng.randint(5, 30)
    Um = Up / math.sqrt(lam)
    stmt = (f"A 1:{lam} scale model is tested under Froude similarity. "
            f"Prototype speed is $U_p={Up}$ m/s. Find model speed.")
    sol = (f"$U_m = U_p/\\sqrt{{\\lambda}} = {Up}/\\sqrt{{{lam}}} = {Um:.3f}$ m/s.\n\n"
           f"Force scaling: $F_p = F_m \\cdot \\lambda^3 = F_m \\times {lam**3}$.")
    return Problem("Model-prototype scaling", stmt, sol)

def gen_identify_forces(rng: random.Random) -> Problem:
    Re = rng.choice([0.01, 100, 1e6])
    Fr = rng.choice([0.1, 1.0, 5.0])
    stmt = (f"A flow has Re $= {Re}$ and Fr $= {Fr}$. Which forces dominate?")
    inertia_vs_visc = "Viscous dominates" if Re < 1 else "Inertia dominates over viscosity"
    inertia_vs_grav = "Gravity dominates" if Fr < 1 else "Inertia dominates over gravity"
    sol = f"Re={Re}: {inertia_vs_visc}.\n\nFr={Fr}: {inertia_vs_grav}."
    return Problem("Identify dominant forces", stmt, sol)

GENERATORS = [gen_pi_count, gen_re_scenario, gen_froude, gen_model_scaling, gen_identify_forces]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.5 Practice — Dimensionless Numbers\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

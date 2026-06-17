#!/usr/bin/env python3
"""
6.8_compressible.py — Practice problem generator for Chapter 6.8
(Compressible Flow & Shock Waves).

Archetypes:
  1. Speed of sound calculation
  2. Isentropic flow relations (T, p, rho vs Mach)
  3. Normal shock jump conditions
  4. Nozzle throat conditions
  5. Stagnation pressure loss across shock
  6. Area-Mach relation

Usage:
  python 6.8_compressible.py --count 12 --seed 42
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

GAMMA = 1.4

def gen_speed_of_sound(rng: random.Random) -> Problem:
    T = rng.randint(200, 400)
    R = 287.0
    c = math.sqrt(GAMMA * R * T)
    stmt = f"Compute the speed of sound in air ($\\gamma=1.4$, $R=287$ J/(kg·K)) at $T={T}$ K."
    sol = f"$c = \\sqrt{{\\gamma RT}} = \\sqrt{{1.4\\times287\\times{T}}} = {c:.1f}$ m/s."
    return Problem("Speed of sound", stmt, sol)

def gen_isentropic(rng: random.Random) -> Problem:
    M = rng.choice([0.5, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0])
    T0 = rng.randint(300, 600)
    p0 = rng.randint(100, 500)
    T_ratio = 1 + (GAMMA-1)/2 * M**2
    T = T0 / T_ratio
    p = p0 / T_ratio**(GAMMA/(GAMMA-1))
    stmt = (f"Isentropic flow: $M={M}$, $T_0={T0}$ K, $p_0={p0}$ kPa. Find static $T$ and $p$.")
    sol = (f"$T_0/T = 1 + (\\gamma-1)M^2/2 = {T_ratio:.4f}$.\n\n"
           f"$T = {T0}/{T_ratio:.4f} = {T:.1f}$ K.\n\n"
           f"$p = {p0}/({T_ratio:.4f})^{{3.5}} = {p:.2f}$ kPa.")
    return Problem("Isentropic relations", stmt, sol)

def gen_normal_shock(rng: random.Random) -> Problem:
    M1 = rng.choice([1.5, 2.0, 2.5, 3.0, 4.0])
    gm1 = GAMMA - 1
    gp1 = GAMMA + 1
    M2_sq = (M1**2 + 2/gm1) / (2*GAMMA/gm1 * M1**2 - 1)
    M2 = math.sqrt(M2_sq)
    p_ratio = 1 + 2*GAMMA/gp1 * (M1**2 - 1)
    rho_ratio = gp1*M1**2 / (gm1*M1**2 + 2)
    T_ratio = p_ratio / rho_ratio
    stmt = f"Normal shock at $M_1={M1}$ in air ($\\gamma=1.4$). Find $M_2$, $p_2/p_1$, $T_2/T_1$."
    sol = (f"$M_2 = {M2:.4f}$.\n\n"
           f"$p_2/p_1 = {p_ratio:.4f}$.\n\n"
           f"$\\rho_2/\\rho_1 = {rho_ratio:.4f}$.\n\n"
           f"$T_2/T_1 = {T_ratio:.4f}$.")
    return Problem("Normal shock relations", stmt, sol)

def gen_throat(rng: random.Random) -> Problem:
    T0 = rng.randint(300, 800)
    p0 = rng.randint(200, 1000)
    T_star = T0 * 2 / (GAMMA + 1)
    p_star = p0 * (2/(GAMMA+1))**(GAMMA/(GAMMA-1))
    c_star = math.sqrt(GAMMA * 287 * T_star)
    stmt = (f"Nozzle with $T_0={T0}$ K, $p_0={p0}$ kPa. Find critical (throat) conditions "
            f"$T^*$, $p^*$, and $c^*$.")
    sol = (f"$T^* = 2T_0/(\\gamma+1) = {T_star:.1f}$ K.\n\n"
           f"$p^* = p_0(2/(\\gamma+1))^{{\\gamma/(\\gamma-1)}} = {p_star:.1f}$ kPa.\n\n"
           f"$c^* = \\sqrt{{\\gamma R T^*}} = {c_star:.1f}$ m/s.")
    return Problem("Nozzle throat conditions", stmt, sol)

def gen_p0_loss(rng: random.Random) -> Problem:
    M1 = rng.choice([1.5, 2.0, 2.5, 3.0])
    gm1 = GAMMA - 1
    gp1 = GAMMA + 1
    M2_sq = (M1**2 + 2/gm1) / (2*GAMMA/gm1 * M1**2 - 1)
    M2 = math.sqrt(M2_sq)
    p_ratio = 1 + 2*GAMMA/gp1 * (M1**2 - 1)
    p02_p2 = (1 + gm1/2*M2_sq)**(GAMMA/gm1)
    p01_p1 = (1 + gm1/2*M1**2)**(GAMMA/gm1)
    p02_p01 = p_ratio * p02_p2 / p01_p1
    stmt = f"Find stagnation pressure ratio $p_{{02}}/p_{{01}}$ across a normal shock at $M_1={M1}$."
    sol = (f"$p_2/p_1 = {p_ratio:.4f}$, $M_2 = {M2:.4f}$.\n\n"
           f"$p_{{02}}/p_2 = (1+0.2M_2^2)^{{3.5}} = {p02_p2:.4f}$.\n\n"
           f"$p_{{01}}/p_1 = (1+0.2M_1^2)^{{3.5}} = {p01_p1:.4f}$.\n\n"
           f"$p_{{02}}/p_{{01}} = {p02_p01:.4f}$ ({(1-p02_p01)*100:.1f}% loss).")
    return Problem("Stagnation pressure loss", stmt, sol)

def gen_area_mach(rng: random.Random) -> Problem:
    M = rng.choice([0.5, 1.5, 2.0, 2.5, 3.0])
    gp1 = GAMMA + 1
    gm1 = GAMMA - 1
    A_ratio = (1/M) * ((2/gp1)*(1 + gm1/2*M**2))**((gp1)/(2*gm1))
    stmt = f"Find $A/A^*$ for $M={M}$ in air ($\\gamma=1.4$)."
    sol = (f"$A/A^* = (1/M)[2/(\\gamma+1)(1+(\\gamma-1)M^2/2)]^{{(\\gamma+1)/(2(\\gamma-1))}}$\n\n"
           f"$= (1/{M})[{2/gp1:.4f}\\times(1+{gm1/2:.1f}\\times{M}^2)]^{{3}} = {A_ratio:.4f}$.")
    return Problem("Area-Mach relation", stmt, sol)

GENERATORS = [gen_speed_of_sound, gen_isentropic, gen_normal_shock, gen_throat, gen_p0_loss, gen_area_mach]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.8 Practice — Compressible Flow & Shock Waves\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

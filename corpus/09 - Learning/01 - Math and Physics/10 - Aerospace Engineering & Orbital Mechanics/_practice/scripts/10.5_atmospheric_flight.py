#!/usr/bin/env python3
"""
10.5_atmospheric_flight.py — Practice problem generator for Chapter 10.5
(Atmospheric Flight Dynamics).

Archetypes:
  1. Lift and drag from flight conditions
  2. Maximum L/D and optimal CL
  3. Stall speed computation
  4. Breguet range equation
  5. Rate of climb / specific excess power

Usage:
  python 10.5_atmospheric_flight.py --count 12 --seed 7
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
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_lift_drag(rng: random.Random) -> Problem:
    rho = round(rng.uniform(0.4, 1.225), 3)
    v = rng.randint(60, 250)
    S = rng.randint(20, 120)
    CL = round(rng.uniform(0.2, 1.2), 3)
    CD0 = round(rng.uniform(0.015, 0.035), 4)
    K = round(rng.uniform(0.03, 0.06), 4)
    CD = CD0 + K * CL**2
    q = 0.5 * rho * v**2
    L = q * S * CL
    D = q * S * CD
    stmt = (f"Given: $\\rho = {rho}$ kg/m³, $v = {v}$ m/s, $S = {S}$ m², $C_L = {CL}$, "
            f"$C_{{D_0}} = {CD0}$, $K = {K}$. Compute lift, drag, and L/D.")
    sol = (f"$C_D = C_{{D_0}} + KC_L^2 = {CD0} + {K}({CL})^2 = {CD:.5f}$\n\n"
           f"$q = \\frac{{1}}{{2}}\\rho v^2 = 0.5\\times{rho}\\times{v}^2 = {q:.1f}$ Pa\n\n"
           f"$L = qSC_L = {L:.0f}$ N, $D = qSC_D = {D:.0f}$ N\n\n"
           f"$L/D = {CL}/{CD:.5f} = {CL/CD:.2f}$")
    return Problem("Lift, drag, and L/D", stmt, sol)

def gen_max_ld(rng: random.Random) -> Problem:
    CD0 = round(rng.uniform(0.015, 0.035), 4)
    K = round(rng.uniform(0.03, 0.06), 4)
    CL_opt = math.sqrt(CD0 / K)
    LD_max = 1 / (2 * math.sqrt(K * CD0))
    stmt = f"For a drag polar with $C_{{D_0}} = {CD0}$ and $K = {K}$, find $(L/D)_{{\\max}}$ and the optimal $C_L$."
    sol = (f"$C_L^* = \\sqrt{{C_{{D_0}}/K}} = \\sqrt{{{CD0}/{K}}} = {CL_opt:.4f}$\n\n"
           f"$(L/D)_{{\\max}} = 1/(2\\sqrt{{KC_{{D_0}}}}) = 1/(2\\sqrt{{{K}\\times{CD0}}}) = {LD_max:.2f}$")
    return Problem("Maximum L/D", stmt, sol)

def gen_stall(rng: random.Random) -> Problem:
    W = rng.randint(30000, 300000)
    S = rng.randint(20, 150)
    CLmax = round(rng.uniform(1.4, 2.2), 2)
    rho = round(rng.uniform(0.9, 1.225), 3)
    vs = math.sqrt(2*W / (rho * S * CLmax))
    stmt = (f"Aircraft: $W = {W}$ N, $S = {S}$ m², $C_{{L,\\max}} = {CLmax}$, $\\rho = {rho}$ kg/m³. "
            f"Find stall speed.")
    sol = (f"$$\nv_{{\\text{{stall}}}} = \\sqrt{{\\frac{{2W}}{{\\rho S C_{{L,\\max}}}}}} = "
           f"\\sqrt{{\\frac{{2\\times{W}}}{{{rho}\\times{S}\\times{CLmax}}}}} = {vs:.2f} \\text{{ m/s}}\n$$\n")
    return Problem("Stall speed", stmt, sol)

def gen_breguet(rng: random.Random) -> Problem:
    v = rng.randint(200, 260)
    cT = round(rng.uniform(1.5e-5, 2.5e-5), 7)
    LD = rng.randint(14, 20)
    fuel_frac = round(rng.uniform(0.2, 0.4), 2)
    R = v / cT * LD * math.log(1/(1-fuel_frac))
    stmt = (f"Jet aircraft: $v = {v}$ m/s, $c_T = {cT}$ s⁻¹, $L/D = {LD}$, fuel fraction = {fuel_frac}. "
            f"Compute range.")
    sol = (f"$W_i/W_f = 1/(1-{fuel_frac}) = {1/(1-fuel_frac):.4f}$\n\n"
           f"$$\nR = \\frac{{v}}{{c_T}}\\frac{{L}}{{D}}\\ln\\frac{{W_i}}{{W_f}} = "
           f"\\frac{{{v}}}{{{cT}}}\\times{LD}\\times{math.log(1/(1-fuel_frac)):.4f} = {R:.0f} \\text{{ m}} = {R/1000:.0f} \\text{{ km}}\n$$\n")
    return Problem("Breguet range equation", stmt, sol)

def gen_roc(rng: random.Random) -> Problem:
    W = rng.randint(50000, 200000)
    T = rng.randint(int(W*0.2), int(W*0.5))
    v = rng.randint(80, 200)
    S = rng.randint(25, 80)
    CD0 = 0.025
    K = 0.04
    rho = 1.225
    CL = 2*W/(rho*v**2*S)
    CD = CD0 + K*CL**2
    D = 0.5*rho*v**2*S*CD
    RC = (T - D)*v / W
    stmt = (f"Aircraft: $W={W}$ N, $T={T}$ N, $v={v}$ m/s, $S={S}$ m², "
            f"$C_{{D_0}}=0.025$, $K=0.04$, $\\rho=1.225$ kg/m³. Find rate of climb.")
    sol = (f"$C_L = 2W/(\\rho v^2 S) = {CL:.4f}$\n\n"
           f"$C_D = {CD0}+{K}({CL:.4f})^2 = {CD:.5f}$\n\n"
           f"$D = qSC_D = {D:.0f}$ N\n\n"
           f"$RC = (T-D)v/W = ({T}-{D:.0f})\\times{v}/{W} = {RC:.2f}$ m/s = {RC*60:.0f} ft/min")
    return Problem("Rate of climb", stmt, sol)

GENERATORS = [gen_lift_drag, gen_max_ld, gen_stall, gen_breguet, gen_roc]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, atmospheric-flight]\n---\n",
             "# 10.5 Practice — Atmospheric Flight Dynamics\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

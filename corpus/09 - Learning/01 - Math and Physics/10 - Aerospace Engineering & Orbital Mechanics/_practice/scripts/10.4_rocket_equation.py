#!/usr/bin/env python3
"""
10.4_rocket_equation.py — Practice problem generator for Chapter 10.4
(Rocket Equation & Propulsion Systems).

Archetypes:
  1. Tsiolkovsky ΔV from mass ratio and Isp
  2. Required propellant mass for given ΔV
  3. Mass ratio for multi-stage rocket
  4. Optimal staging (equal mass ratios)
  5. Thrust and burn time computation

Usage:
  python 10.4_rocket_equation.py --count 15 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

G0 = 9.80665e-3  # km/s^2

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_tsiolkovsky(rng: random.Random) -> Problem:
    isp = rng.choice([260, 300, 320, 350, 420, 450, 3000])
    ve = isp * G0
    m0 = rng.randint(5000, 500000)
    mf = rng.randint(int(m0*0.1), int(m0*0.6))
    R = m0 / mf
    dv = ve * math.log(R)
    stmt = (f"A rocket stage has $I_{{sp}} = {isp}$ s, initial mass $m_0 = {m0}$ kg, "
            f"final mass $m_f = {mf}$ kg. Compute ΔV.")
    sol = (f"$v_e = I_{{sp}} g_0 = {isp}\\times{G0:.5f} = {ve:.4f}$ km/s\n\n"
           f"$R = m_0/m_f = {m0}/{mf} = {R:.4f}$\n\n"
           f"$$\n\\Delta V = v_e\\ln R = {ve:.4f}\\times\\ln({R:.4f}) = {dv:.4f} \\text{{ km/s}}\n$$\n")
    return Problem("Tsiolkovsky rocket equation", stmt, sol)

def gen_propellant_mass(rng: random.Random) -> Problem:
    isp = rng.choice([310, 320, 350, 450])
    ve = isp * G0
    dv = round(rng.uniform(1.0, 6.0), 2)
    mf = rng.randint(500, 10000)
    R = math.exp(dv / ve)
    m0 = mf * R
    mp = m0 - mf
    stmt = (f"A spacecraft with dry mass {mf} kg needs ΔV = {dv} km/s. Engine $I_{{sp}} = {isp}$ s. "
            f"How much propellant is required?")
    sol = (f"$v_e = {ve:.4f}$ km/s\n\n"
           f"$R = e^{{\\Delta V/v_e}} = e^{{{dv}/{ve:.4f}}} = {R:.4f}$\n\n"
           f"$m_0 = m_f \\times R = {mf}\\times{R:.4f} = {m0:.0f}$ kg\n\n"
           f"$m_p = m_0 - m_f = {mp:.0f}$ kg\n\n"
           f"Propellant fraction: ${mp/m0*100:.1f}\\%$")
    return Problem("Required propellant mass", stmt, sol)

def gen_multistage(rng: random.Random) -> Problem:
    N = rng.choice([2, 3])
    isp = rng.choice([300, 350, 450])
    ve = isp * G0
    dv = round(rng.uniform(8.0, 12.0), 2)
    eps = round(rng.uniform(0.06, 0.12), 3)
    mL = rng.randint(1000, 10000)
    Rstar = math.exp(dv / (N * ve))
    lam = (1 - eps*Rstar) / (Rstar - 1)
    pf_stage = lam / (1 + lam)
    pf_total = pf_stage**N
    m0 = mL / pf_total
    stmt = (f"Design a {N}-stage rocket: ΔV = {dv} km/s, $I_{{sp}} = {isp}$ s, $\\epsilon = {eps}$, "
            f"payload $m_L = {mL}$ kg. Find optimal mass ratio and total liftoff mass.")
    sol = (f"$v_e = {ve:.4f}$ km/s\n\n"
           f"$R^* = e^{{\\Delta V/(Nv_e)}} = e^{{{dv}/({N}\\times{ve:.4f})}} = {Rstar:.4f}$\n\n"
           f"$\\lambda = (1-\\epsilon R^*)/(R^*-1) = (1-{eps}\\times{Rstar:.4f})/({Rstar:.4f}-1) = {lam:.4f}$\n\n"
           f"Payload fraction/stage: ${pf_stage:.4f}$, overall: ${pf_total:.6f}$\n\n"
           f"$m_0 = {mL}/{pf_total:.6f} = {m0:.0f}$ kg")
    return Problem(f"{N}-stage optimal rocket", stmt, sol)

def gen_thrust_burn(rng: random.Random) -> Problem:
    F = rng.randint(50, 2000) * 1000  # Newtons
    isp = rng.choice([300, 320, 350, 450])
    ve = isp * G0 * 1000  # m/s
    mdot = F / ve
    mp = rng.randint(10000, 200000)
    tb = mp / mdot
    stmt = (f"An engine produces {F/1000:.0f} kN thrust with $I_{{sp}} = {isp}$ s. "
            f"If it burns {mp} kg of propellant, what is the burn time?")
    sol = (f"$v_e = {isp}\\times9.807 = {ve:.1f}$ m/s\n\n"
           f"$\\dot{{m}} = F/v_e = {F}/{ve:.1f} = {mdot:.2f}$ kg/s\n\n"
           f"$t_b = m_p/\\dot{{m}} = {mp}/{mdot:.2f} = {tb:.1f}$ s $= {tb/60:.1f}$ min")
    return Problem("Thrust and burn time", stmt, sol)

def gen_structural_coeff(rng: random.Random) -> Problem:
    ms = rng.randint(1000, 20000)
    mp = rng.randint(ms*5, ms*20)
    mL = rng.randint(500, 10000)
    eps = ms / (ms + mp)
    lam = mL / (ms + mp)
    R = (1 + lam) / (eps + lam)
    stmt = (f"A stage has structure $m_s = {ms}$ kg, propellant $m_p = {mp}$ kg, payload $m_L = {mL}$ kg. "
            f"Find $\\epsilon$, $\\lambda$, and mass ratio $R$.")
    sol = (f"$\\epsilon = m_s/(m_s+m_p) = {ms}/({ms}+{mp}) = {eps:.5f}$\n\n"
           f"$\\lambda = m_L/(m_s+m_p) = {mL}/{ms+mp} = {lam:.5f}$\n\n"
           f"$R = (1+\\lambda)/(\\epsilon+\\lambda) = {(1+lam):.5f}/{(eps+lam):.5f} = {R:.4f}$")
    return Problem("Structural coefficient & mass ratio", stmt, sol)

GENERATORS = [gen_tsiolkovsky, gen_propellant_mass, gen_multistage, gen_thrust_burn, gen_structural_coeff]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, rocket-equation, propulsion]\n---\n",
             "# 10.4 Practice — Rocket Equation & Propulsion\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

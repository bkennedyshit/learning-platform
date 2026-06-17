#!/usr/bin/env python3
"""
12.4_axial_torsion.py — Practice problem generator for Chapter 12.4
(Axial Loading & Torsion).

Archetypes:
  1. Axial deformation (stepped bar)
  2. Thermal stress in constrained bar
  3. Angle of twist (solid shaft)
  4. Angle of twist (hollow shaft)
  5. Power transmission design
  6. Statically indeterminate shaft

Usage:
  python 12.4_axial_torsion.py --count 15 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_axial_stepped(rng: random.Random) -> Problem:
    P = rng.choice([20, 30, 40, 50, 60, 80])
    L1 = rng.choice([400, 500, 600, 800])
    L2 = rng.choice([400, 600, 800, 1000])
    A1 = rng.choice([400, 500, 600, 800])
    A2 = rng.choice([800, 1000, 1200, 1500])
    E1 = rng.choice([200, 210])
    E2 = rng.choice([70, 100, 200])
    d1 = P * 1000 * (L1/1000) / (A1 * 1e-6 * E1 * 1e9)
    d2 = P * 1000 * (L2/1000) / (A2 * 1e-6 * E2 * 1e9)
    dt = d1 + d2
    stmt = (f"A stepped bar carries $P = {P}$ kN. Segment 1: $L_1={L1}$ mm, $A_1={A1}$ mm², $E_1={E1}$ GPa. "
            f"Segment 2: $L_2={L2}$ mm, $A_2={A2}$ mm², $E_2={E2}$ GPa. Find total elongation.")
    sol = (f"$\\delta_1 = \\frac{{PL_1}}{{A_1 E_1}} = \\frac{{{P}\\times10^3 \\times {L1/1000}}}{{{A1}\\times10^{{-6}} \\times {E1}\\times10^9}} = {d1*1000:.4f}$ mm\n\n"
           f"$\\delta_2 = \\frac{{PL_2}}{{A_2 E_2}} = \\frac{{{P}\\times10^3 \\times {L2/1000}}}{{{A2}\\times10^{{-6}} \\times {E2}\\times10^9}} = {d2*1000:.4f}$ mm\n\n"
           f"$\\delta_{{total}} = {(d1+d2)*1000:.4f}$ mm")
    return Problem("Axial deformation (stepped bar)", stmt, sol)

def gen_thermal_stress(rng: random.Random) -> Problem:
    E = rng.choice([70, 100, 200, 210])
    alpha = rng.choice([12, 17, 23])  # ×10^-6 /°C
    dT = rng.choice([30, 40, 50, 60, 80, 100])
    sigma = -alpha * 1e-6 * dT * E * 1e3  # MPa
    stmt = (f"A bar ($E={E}$ GPa, $\\alpha = {alpha}\\times10^{{-6}}$/°C) is fixed at both ends. "
            f"Temperature increases by $\\Delta T = {dT}$°C. Find the thermal stress.")
    sol = (f"$\\sigma = -\\alpha \\Delta T \\cdot E = -{alpha}\\times10^{{-6}} \\times {dT} \\times {E}\\times10^3$\n\n"
           f"$= {sigma:.1f}$ MPa (compression)\n\n"
           f"Note: Independent of length and area!")
    return Problem("Thermal stress (constrained bar)", stmt, sol)

def gen_twist_solid(rng: random.Random) -> Problem:
    d = rng.choice([30, 40, 50, 60, 80])  # mm
    L = rng.choice([500, 800, 1000, 1500, 2000])  # mm
    T = rng.choice([200, 500, 800, 1000, 1500, 2000, 3000])  # N·m
    G = rng.choice([40, 60, 80])  # GPa
    c = d / 2000  # m
    J = math.pi * (d/2000)**4 / 2
    tau_max = T * c / J
    phi = T * (L/1000) / (G * 1e9 * J)
    stmt = (f"Solid shaft: $d = {d}$ mm, $L = {L}$ mm, $G = {G}$ GPa, $T = {T}$ N·m. "
            f"Find $\\tau_{{\\max}}$ and angle of twist $\\phi$.")
    sol = (f"$J = \\pi d^4/32 = \\pi({d})^4/32 = {J*1e12:.1f}\\times10^{{-12}}$ m⁴\n\n"
           f"$\\tau_{{\\max}} = Tc/J = {T} \\times {c:.4f} / {J:.4e} = {tau_max/1e6:.1f}$ MPa\n\n"
           f"$\\phi = TL/(GJ) = {T} \\times {L/1000} / ({G}\\times10^9 \\times {J:.4e}) = {phi:.5f}$ rad = ${math.degrees(phi):.3f}°$")
    return Problem("Torsion — solid shaft", stmt, sol)

def gen_twist_hollow(rng: random.Random) -> Problem:
    do = rng.choice([60, 80, 100, 120])
    di = rng.choice([int(do*0.5), int(do*0.6), int(do*0.7)])
    L = rng.choice([800, 1000, 1500, 2000])
    T = rng.choice([1000, 2000, 3000, 5000, 8000])
    G = 80
    co, ci = do/2000, di/2000
    J = math.pi/2 * (co**4 - ci**4)
    tau_max = T * co / J
    phi = T * (L/1000) / (G * 1e9 * J)
    stmt = (f"Hollow shaft: $d_o = {do}$ mm, $d_i = {di}$ mm, $L = {L}$ mm, $G = {G}$ GPa, $T = {T}$ N·m. "
            f"Find $\\tau_{{\\max}}$ and $\\phi$.")
    sol = (f"$J = \\frac{{\\pi}}{{2}}(c_o^4 - c_i^4) = \\frac{{\\pi}}{{2}}(({co:.4f})^4 - ({ci:.4f})^4) = {J:.4e}$ m⁴\n\n"
           f"$\\tau_{{\\max}} = Tc_o/J = {T} \\times {co:.4f} / {J:.4e} = {tau_max/1e6:.1f}$ MPa\n\n"
           f"$\\phi = TL/(GJ) = {phi:.5f}$ rad = ${math.degrees(phi):.3f}°$")
    return Problem("Torsion — hollow shaft", stmt, sol)

def gen_power_transmission(rng: random.Random) -> Problem:
    P_kW = rng.choice([50, 75, 100, 150, 200])
    rpm = rng.choice([200, 300, 500, 600, 900, 1200, 1800])
    tau_allow = rng.choice([40, 50, 60, 80])
    omega = rpm * 2 * math.pi / 60
    T = P_kW * 1000 / omega
    c = (2*T / (math.pi * tau_allow * 1e6))**(1/3)
    d = 2 * c * 1000
    stmt = (f"Design a solid shaft to transmit ${P_kW}$ kW at ${rpm}$ rpm. "
            f"Allowable shear stress $\\tau_{{allow}} = {tau_allow}$ MPa. Find minimum diameter.")
    sol = (f"$\\omega = {rpm} \\times 2\\pi/60 = {omega:.2f}$ rad/s\n\n"
           f"$T = P/\\omega = {P_kW*1000}/{omega:.2f} = {T:.1f}$ N·m\n\n"
           f"$\\tau = 2T/(\\pi c^3)$: $c^3 = 2T/(\\pi\\tau_{{allow}}) = 2({T:.1f})/(\\pi \\times {tau_allow}\\times10^6) = {2*T/(math.pi*tau_allow*1e6):.4e}$ m³\n\n"
           f"$c = {c*1000:.2f}$ mm → $d = {d:.1f}$ mm (round up to next standard size)")
    return Problem("Power transmission shaft design", stmt, sol)

def gen_indeterminate_shaft(rng: random.Random) -> Problem:
    L = rng.choice([600, 800, 1000, 1200])
    a = rng.randint(int(L*0.3), int(L*0.7))
    b = L - a
    T0 = rng.choice([500, 800, 1000, 1500, 2000])
    TA = sp.Rational(T0 * b, L)
    TB = sp.Rational(T0 * a, L)
    stmt = (f"A shaft fixed at both ends (length $L={L}$ mm). Torque $T_0 = {T0}$ N·m applied at "
            f"$a = {a}$ mm from left end. Find reactions $T_A$ and $T_B$.")
    sol = (f"Equilibrium: $T_A + T_B = {T0}$\n\n"
           f"Compatibility ($\\phi_{{total}} = 0$): $T_A \\cdot a = T_B \\cdot b$\n\n"
           f"$T_A \\cdot {a} = T_B \\cdot {b}$\n\n"
           f"Solving: $T_A = T_0 \\cdot b/L = {T0} \\times {b}/{L} = {sp.latex(TA)}$ N·m\n\n"
           f"$T_B = T_0 \\cdot a/L = {T0} \\times {a}/{L} = {sp.latex(TB)}$ N·m")
    return Problem("Statically indeterminate shaft", stmt, sol)

GENERATORS = [gen_axial_stepped, gen_thermal_stress, gen_twist_solid,
              gen_twist_hollow, gen_power_transmission, gen_indeterminate_shaft]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.4 Axial/Torsion problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.4 Axial Loading & Torsion — Practice Problems\n",
             f"#review/mechanics  Generated {args.count} problems\n\n---\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("\n---\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Written {len(text)} bytes → {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()

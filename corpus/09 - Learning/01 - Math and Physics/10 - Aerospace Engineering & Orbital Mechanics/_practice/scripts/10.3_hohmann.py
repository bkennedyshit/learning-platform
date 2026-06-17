#!/usr/bin/env python3
"""
10.3_hohmann.py — Practice problem generator for Chapter 10.3
(Orbital Maneuvers — Hohmann Transfers).

Archetypes:
  1. Hohmann transfer ΔV₁, ΔV₂, total ΔV
  2. Transfer time
  3. Phase angle for rendezvous
  4. Plane change ΔV
  5. Combined maneuver (altitude + plane change)
  6. Bi-elliptic vs Hohmann comparison

Usage:
  python 10.3_hohmann.py --count 18 --seed 99
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

MU = 398600.4418
R_EARTH = 6371.0

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_hohmann_dv(rng: random.Random) -> Problem:
    h1 = rng.randint(200, 1000)
    h2 = rng.randint(5000, 36000)
    r1 = R_EARTH + h1
    r2 = R_EARTH + h2
    vc1 = math.sqrt(MU / r1)
    vc2 = math.sqrt(MU / r2)
    at = (r1 + r2) / 2
    dv1 = vc1 * (math.sqrt(2*r2/(r1+r2)) - 1)
    dv2 = vc2 * (1 - math.sqrt(2*r1/(r1+r2)))
    stmt = (f"Compute the Hohmann transfer ΔV from a circular orbit at {h1} km altitude "
            f"to a circular orbit at {h2} km altitude.")
    sol = (f"$r_1 = {r1:.0f}$ km, $r_2 = {r2:.0f}$ km\n\n"
           f"$v_{{c,1}} = {vc1:.4f}$ km/s, $v_{{c,2}} = {vc2:.4f}$ km/s\n\n"
           f"$$\n\\Delta V_1 = v_{{c,1}}\\left(\\sqrt{{\\frac{{2r_2}}{{r_1+r_2}}}}-1\\right) = {dv1:.4f} \\text{{ km/s}}\n$$\n\n"
           f"$$\n\\Delta V_2 = v_{{c,2}}\\left(1-\\sqrt{{\\frac{{2r_1}}{{r_1+r_2}}}}\\right) = {dv2:.4f} \\text{{ km/s}}\n$$\n\n"
           f"$\\Delta V_{{\\text{{total}}}} = {dv1+dv2:.4f}$ km/s")
    return Problem("Hohmann transfer ΔV", stmt, sol)

def gen_transfer_time(rng: random.Random) -> Problem:
    r1 = R_EARTH + rng.randint(200, 1000)
    r2 = R_EARTH + rng.randint(10000, 42000)
    at = (r1 + r2) / 2
    tH = math.pi * math.sqrt(at**3 / MU)
    stmt = f"Find the transfer time for a Hohmann transfer from $r_1 = {r1:.0f}$ km to $r_2 = {r2:.0f}$ km."
    sol = (f"$a_t = (r_1+r_2)/2 = {at:.1f}$ km\n\n"
           f"$$\nt_H = \\pi\\sqrt{{\\frac{{a_t^3}}{{\\mu}}}} = \\pi\\sqrt{{\\frac{{{at:.1f}^3}}{{{MU}}}}} = {tH:.1f} \\text{{ s}} = {tH/3600:.2f} \\text{{ hr}}\n$$\n")
    return Problem("Hohmann transfer time", stmt, sol)

def gen_phase_angle(rng: random.Random) -> Problem:
    r1 = R_EARTH + rng.randint(200, 800)
    r2 = R_EARTH + rng.randint(5000, 35000)
    at = (r1 + r2) / 2
    tH = math.pi * math.sqrt(at**3 / MU)
    T2 = 2 * math.pi * math.sqrt(r2**3 / MU)
    omega2 = 2 * math.pi / T2
    phi = math.pi - omega2 * tH
    stmt = (f"A chaser at $r_1 = {r1:.0f}$ km performs a Hohmann transfer to rendezvous with a target at $r_2 = {r2:.0f}$ km. "
            f"What phase angle must the target have at departure?")
    sol = (f"$t_H = {tH:.1f}$ s, $T_2 = {T2:.1f}$ s, $\\omega_2 = {omega2:.6e}$ rad/s\n\n"
           f"$\\phi = \\pi - \\omega_2 t_H = {math.pi:.4f} - {omega2*tH:.4f} = {phi:.4f}$ rad $= {math.degrees(phi):.2f}°$")
    return Problem("Phase angle for rendezvous", stmt, sol)

def gen_plane_change(rng: random.Random) -> Problem:
    alt = rng.randint(200, 35786)
    r = R_EARTH + alt
    v = math.sqrt(MU / r)
    di = rng.randint(5, 60)
    dv = 2 * v * math.sin(math.radians(di/2))
    stmt = f"Compute the ΔV for a {di}° plane change at altitude {alt} km (circular orbit)."
    sol = (f"$v = \\sqrt{{\\mu/r}} = {v:.4f}$ km/s\n\n"
           f"$$\n\\Delta V = 2v\\sin(\\Delta i/2) = 2({v:.4f})\\sin({di/2}°) = {dv:.4f} \\text{{ km/s}}\n$$\n")
    return Problem("Simple plane change ΔV", stmt, sol)

def gen_combined(rng: random.Random) -> Problem:
    r1 = R_EARTH + rng.randint(200, 500)
    r2 = R_EARTH + rng.randint(20000, 42000)
    di = rng.randint(10, 30)
    at = (r1 + r2) / 2
    vta = math.sqrt(MU * (2/r2 - 1/at))
    vc2 = math.sqrt(MU / r2)
    dv_comb = math.sqrt(vta**2 + vc2**2 - 2*vta*vc2*math.cos(math.radians(di)))
    dv_sep = abs(vc2 - vta) + 2*vc2*math.sin(math.radians(di/2))
    stmt = (f"A spacecraft transfers from {r1-R_EARTH:.0f} km to {r2-R_EARTH:.0f} km altitude with a {di}° plane change at the second burn. "
            f"Compare combined vs separate ΔV₂.")
    sol = (f"$v_{{t,a}} = {vta:.4f}$ km/s, $v_{{c,2}} = {vc2:.4f}$ km/s\n\n"
           f"Combined: $\\Delta V_2 = \\sqrt{{v_{{t,a}}^2 + v_c^2 - 2v_{{t,a}}v_c\\cos\\Delta i}} = {dv_comb:.4f}$ km/s\n\n"
           f"Separate: $|v_c - v_{{t,a}}| + 2v_c\\sin(\\Delta i/2) = {dv_sep:.4f}$ km/s\n\n"
           f"Savings: {dv_sep - dv_comb:.4f} km/s ({(dv_sep-dv_comb)/dv_sep*100:.1f}%)")
    return Problem("Combined altitude + plane change", stmt, sol)

def gen_bielliptic(rng: random.Random) -> Problem:
    r1 = R_EARTH + rng.randint(200, 500)
    ratio = rng.uniform(12, 20)
    r2 = r1 * ratio
    rb = r2 * rng.uniform(1.5, 3.0)
    # Hohmann
    vc1 = math.sqrt(MU/r1)
    dv1_h = vc1*(math.sqrt(2*r2/(r1+r2))-1)
    vc2 = math.sqrt(MU/r2)
    dv2_h = vc2*(1-math.sqrt(2*r1/(r1+r2)))
    dvH = dv1_h + dv2_h
    # Bi-elliptic
    dv1_b = math.sqrt(2*MU*rb/(r1*(r1+rb))) - vc1
    vb1 = math.sqrt(2*MU*r1/(rb*(r1+rb)))
    vb2 = math.sqrt(2*MU*r2/(rb*(r2+rb)))
    dv2_b = abs(vb2 - vb1)
    vp2 = math.sqrt(2*MU*rb/(r2*(r2+rb)))
    dv3_b = abs(vp2 - vc2)
    dvBE = dv1_b + dv2_b + dv3_b
    stmt = (f"Compare Hohmann vs bi-elliptic transfer from $r_1={r1:.0f}$ km to $r_2={r2:.0f}$ km "
            f"(ratio {ratio:.1f}) with intermediate $r_b={rb:.0f}$ km.")
    sol = (f"**Hohmann:** $\\Delta V = {dvH:.4f}$ km/s\n\n"
           f"**Bi-elliptic:** $\\Delta V_1={dv1_b:.4f}$, $\\Delta V_2={dv2_b:.4f}$, $\\Delta V_3={dv3_b:.4f}$, total $= {dvBE:.4f}$ km/s\n\n"
           f"{'Bi-elliptic wins' if dvBE < dvH else 'Hohmann wins'} by {abs(dvH-dvBE):.4f} km/s")
    return Problem("Bi-elliptic vs Hohmann", stmt, sol)

GENERATORS = [gen_hohmann_dv, gen_transfer_time, gen_phase_angle, gen_plane_change, gen_combined, gen_bielliptic]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, hohmann, orbital-maneuvers]\n---\n",
             "# 10.3 Practice — Orbital Maneuvers (Hohmann Transfers)\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

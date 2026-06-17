#!/usr/bin/env python3
"""
10.7_patched_conics.py — Practice problem generator for Chapter 10.7
(Interplanetary Trajectories — Patched Conics).

Archetypes:
  1. Sphere of influence radius
  2. Heliocentric transfer velocities and v_infinity
  3. Departure ΔV from parking orbit
  4. Gravity-assist turn angle and velocity gain
  5. Synodic period and launch windows
  6. Complete interplanetary transfer (Earth to target)

Usage:
  python 10.7_patched_conics.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

MU_SUN = 1.327e11  # km^3/s^2

PLANETS = {
    "Venus":  {"a": 1.082e8, "mu": 324859, "R": 6052, "mass_ratio": 2.447e-6},
    "Earth":  {"a": 1.496e8, "mu": 398600.4, "R": 6371, "mass_ratio": 3.003e-6},
    "Mars":   {"a": 2.279e8, "mu": 42828.4, "R": 3390, "mass_ratio": 3.227e-7},
    "Jupiter":{"a": 7.783e8, "mu": 1.267e8, "R": 71492, "mass_ratio": 9.545e-4},
    "Saturn": {"a": 1.427e9, "mu": 3.793e7, "R": 60268, "mass_ratio": 2.857e-4},
}

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_soi(rng: random.Random) -> Problem:
    name = rng.choice(list(PLANETS.keys()))
    p = PLANETS[name]
    r_soi = p["a"] * (p["mass_ratio"])**(2/5)
    stmt = f"Compute the sphere of influence radius for {name}. ($a = {p['a']:.3e}$ km, $m_p/M_\\odot = {p['mass_ratio']:.3e}$)"
    sol = (f"$$\nr_{{SOI}} = a\\left(\\frac{{m_p}}{{M_\\odot}}\\right)^{{2/5}} = "
           f"{p['a']:.3e}\\times({p['mass_ratio']:.3e})^{{0.4}} = {r_soi:.0f} \\text{{ km}}\n$$\n\n"
           f"$= {r_soi/p['R']:.0f}$ planet radii")
    return Problem("Sphere of influence", stmt, sol)

def gen_helio_transfer(rng: random.Random) -> Problem:
    names = list(PLANETS.keys())
    p1_name = rng.choice(["Earth", "Venus"])
    p2_name = rng.choice([n for n in names if PLANETS[n]["a"] > PLANETS[p1_name]["a"]])
    R1 = PLANETS[p1_name]["a"]
    R2 = PLANETS[p2_name]["a"]
    vp1 = math.sqrt(MU_SUN / R1)
    vp2 = math.sqrt(MU_SUN / R2)
    vt1 = math.sqrt(MU_SUN * (2/R1 - 2/(R1+R2)))
    vt2 = math.sqrt(MU_SUN * (2/R2 - 2/(R1+R2)))
    vinf_dep = abs(vt1 - vp1)
    vinf_arr = abs(vp2 - vt2)
    tH = math.pi * math.sqrt((R1+R2)**3 / (8*MU_SUN))
    stmt = (f"Compute the Hohmann transfer from {p1_name} to {p2_name}. "
            f"Find $v_\\infty$ at departure and arrival, and transfer time.")
    sol = (f"$R_1 = {R1:.3e}$ km, $R_2 = {R2:.3e}$ km\n\n"
           f"$v_{{p,1}} = {vp1:.3f}$ km/s, $v_{{p,2}} = {vp2:.3f}$ km/s\n\n"
           f"$v_{{t,1}} = {vt1:.3f}$ km/s, $v_{{t,2}} = {vt2:.3f}$ km/s\n\n"
           f"$v_{{\\infty,dep}} = |v_{{t,1}}-v_{{p,1}}| = {vinf_dep:.3f}$ km/s\n\n"
           f"$v_{{\\infty,arr}} = |v_{{p,2}}-v_{{t,2}}| = {vinf_arr:.3f}$ km/s\n\n"
           f"$t_H = {tH:.0f}$ s $= {tH/86400:.0f}$ days")
    return Problem(f"Heliocentric transfer ({p1_name}→{p2_name})", stmt, sol)

def gen_departure_dv(rng: random.Random) -> Problem:
    vinf = round(rng.uniform(2.0, 8.0), 2)
    alt = rng.randint(200, 500)
    planet = rng.choice(["Earth", "Mars"])
    mu = PLANETS[planet]["mu"]
    Rp = PLANETS[planet]["R"]
    r0 = Rp + alt
    vdep = math.sqrt(vinf**2 + 2*mu/r0)
    vcirc = math.sqrt(mu/r0)
    dv = vdep - vcirc
    stmt = (f"Compute departure ΔV from a {alt} km altitude parking orbit around {planet} "
            f"with $v_\\infty = {vinf}$ km/s.")
    sol = (f"$r_0 = {Rp}+{alt} = {r0}$ km, $\\mu = {mu}$ km³/s²\n\n"
           f"$v_{{dep}} = \\sqrt{{v_\\infty^2 + 2\\mu/r_0}} = \\sqrt{{{vinf}^2 + 2\\times{mu}/{r0}}} = {vdep:.4f}$ km/s\n\n"
           f"$v_{{circ}} = \\sqrt{{\\mu/r_0}} = {vcirc:.4f}$ km/s\n\n"
           f"$\\Delta V = {vdep:.4f} - {vcirc:.4f} = {dv:.4f}$ km/s")
    return Problem("Departure ΔV from parking orbit", stmt, sol)

def gen_gravity_assist(rng: random.Random) -> Problem:
    planet = rng.choice(["Venus", "Earth", "Jupiter", "Saturn"])
    mu = PLANETS[planet]["mu"]
    Rp = PLANETS[planet]["R"]
    vinf = round(rng.uniform(3.0, 15.0), 2)
    alt = rng.randint(int(Rp*0.1), int(Rp*3))
    rp = Rp + alt
    e = 1 + rp * vinf**2 / mu
    delta = 2 * math.asin(1/e)
    dv = 2 * vinf * math.sin(delta/2)
    stmt = (f"Flyby of {planet}: $v_\\infty = {vinf}$ km/s, periapsis altitude {alt} km. "
            f"Find turn angle and max velocity change.")
    sol = (f"$r_p = {Rp}+{alt} = {rp}$ km\n\n"
           f"$e = 1 + r_p v_\\infty^2/\\mu = 1 + {rp}\\times{vinf}^2/{mu} = {e:.4f}$\n\n"
           f"$\\delta = 2\\arcsin(1/e) = 2\\arcsin(1/{e:.4f}) = {math.degrees(delta):.2f}°$\n\n"
           f"$|\\Delta v| = 2v_\\infty\\sin(\\delta/2) = {dv:.3f}$ km/s")
    return Problem(f"Gravity assist ({planet})", stmt, sol)

def gen_synodic(rng: random.Random) -> Problem:
    p2 = rng.choice(["Venus", "Mars", "Jupiter"])
    T1 = 365.25  # Earth days
    T2_map = {"Venus": 224.7, "Mars": 687.0, "Jupiter": 4333.0}
    T2 = T2_map[p2]
    Tsyn = abs(1/(1/T1 - 1/T2)) if T2 != T1 else float('inf')
    stmt = f"Compute the synodic period for Earth and {p2}. ($T_E = {T1}$ d, $T_{{{p2[0]}}} = {T2}$ d)"
    sol = (f"$$\nT_{{syn}} = \\frac{{1}}{{|1/T_1 - 1/T_2|}} = \\frac{{1}}{{|1/{T1} - 1/{T2}|}} = {Tsyn:.1f} \\text{{ days}} = {Tsyn/365.25:.3f} \\text{{ years}}\n$$\n")
    return Problem("Synodic period", stmt, sol)

GENERATORS = [gen_soi, gen_helio_transfer, gen_departure_dv, gen_gravity_assist, gen_synodic]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, interplanetary, patched-conics]\n---\n",
             "# 10.7 Practice — Interplanetary Trajectories (Patched Conics)\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

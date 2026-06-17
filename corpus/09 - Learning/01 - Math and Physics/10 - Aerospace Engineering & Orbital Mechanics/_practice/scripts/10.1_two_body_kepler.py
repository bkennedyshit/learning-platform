#!/usr/bin/env python3
"""
10.1_two_body_kepler.py — Practice problem generator for Chapter 10.1
(Two-Body Problem & Kepler's Laws).

Generates randomized drill problems across 5 archetypes:
  1. Orbital period from altitude (Kepler's 3rd Law)
  2. Circular orbital velocity
  3. Escape velocity from given radius
  4. Vis-Viva equation (speed at a point on elliptical orbit)
  5. Eccentricity and energy from periapsis/apoapsis

Usage:
  python 10.1_two_body_kepler.py
  python 10.1_two_body_kepler.py --count 20 --seed 42
  python 10.1_two_body_kepler.py --count 20 --seed 42 --out /tmp/_101.md
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

MU_EARTH = 398600.4418  # km^3/s^2
R_EARTH = 6371.0  # km

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_period(rng: random.Random) -> Problem:
    alt = rng.randint(200, 36000)
    a = R_EARTH + alt
    T = 2 * math.pi * math.sqrt(a**3 / MU_EARTH)
    stmt = (f"A satellite orbits Earth at altitude $h = {alt}$ km. "
            f"Compute the orbital period $T$. ($R_E = {R_EARTH}$ km, $\\mu_E = 398600.4$ km³/s²)")
    sol = (f"$a = R_E + h = {R_EARTH} + {alt} = {a:.1f}$ km\n\n"
           f"$$\nT = 2\\pi\\sqrt{{\\frac{{a^3}}{{\\mu}}}} = 2\\pi\\sqrt{{\\frac{{{a:.1f}^3}}{{{MU_EARTH}}}}} = {T:.1f} \\text{{ s}} = {T/60:.1f} \\text{{ min}}\n$$\n")
    return Problem("Orbital period (Kepler's 3rd Law)", stmt, sol)

def gen_circular_v(rng: random.Random) -> Problem:
    alt = rng.randint(150, 2000)
    r = R_EARTH + alt
    vc = math.sqrt(MU_EARTH / r)
    stmt = (f"Compute the circular orbital velocity at altitude $h = {alt}$ km above Earth.")
    sol = (f"$r = {R_EARTH} + {alt} = {r:.1f}$ km\n\n"
           f"$$\nv_c = \\sqrt{{\\frac{{\\mu}}{{r}}}} = \\sqrt{{\\frac{{{MU_EARTH}}}{{{r:.1f}}}}} = {vc:.4f} \\text{{ km/s}}\n$$\n")
    return Problem("Circular orbital velocity", stmt, sol)

def gen_escape_v(rng: random.Random) -> Problem:
    alt = rng.randint(0, 5000)
    r = R_EARTH + alt
    vesc = math.sqrt(2 * MU_EARTH / r)
    stmt = (f"Compute the escape velocity from altitude $h = {alt}$ km above Earth's surface.")
    sol = (f"$r = {r:.1f}$ km\n\n"
           f"$$\nv_{{\\text{{esc}}}} = \\sqrt{{\\frac{{2\\mu}}{{r}}}} = \\sqrt{{\\frac{{2 \\times {MU_EARTH}}}{{{r:.1f}}}}} = {vesc:.4f} \\text{{ km/s}}\n$$\n\n"
           f"Check: $v_{{\\text{{esc}}}} = \\sqrt{{2}}\\,v_c = \\sqrt{{2}} \\times {math.sqrt(MU_EARTH/r):.4f} = {vesc:.4f}$ km/s ✓")
    return Problem("Escape velocity", stmt, sol)

def gen_vis_viva(rng: random.Random) -> Problem:
    rp = R_EARTH + rng.randint(200, 1000)
    ra = R_EARTH + rng.randint(5000, 40000)
    a = (rp + ra) / 2
    r = rp if rng.random() < 0.5 else ra
    label = "periapsis" if r == rp else "apoapsis"
    v = math.sqrt(MU_EARTH * (2/r - 1/a))
    stmt = (f"An elliptical orbit has perigee radius $r_p = {rp:.0f}$ km and apogee radius $r_a = {ra:.0f}$ km. "
            f"Find the speed at {label}.")
    sol = (f"$a = (r_p + r_a)/2 = ({rp:.0f} + {ra:.0f})/2 = {a:.1f}$ km\n\n"
           f"At {label} ($r = {r:.0f}$ km):\n\n"
           f"$$\nv = \\sqrt{{\\mu\\left(\\frac{{2}}{{r}} - \\frac{{1}}{{a}}\\right)}} = "
           f"\\sqrt{{{MU_EARTH}\\left(\\frac{{2}}{{{r:.0f}}} - \\frac{{1}}{{{a:.1f}}}\\right)}} = {v:.4f} \\text{{ km/s}}\n$$\n")
    return Problem("Vis-Viva equation", stmt, sol)

def gen_eccentricity(rng: random.Random) -> Problem:
    rp = R_EARTH + rng.randint(200, 2000)
    ra = R_EARTH + rng.randint(3000, 50000)
    a = (rp + ra) / 2
    e = (ra - rp) / (ra + rp)
    eps = -MU_EARTH / (2 * a)
    stmt = (f"An orbit has perigee radius $r_p = {rp:.0f}$ km and apogee radius $r_a = {ra:.0f}$ km. "
            f"Find the eccentricity $e$ and specific energy $\\varepsilon$.")
    sol = (f"$$\ne = \\frac{{r_a - r_p}}{{r_a + r_p}} = \\frac{{{ra:.0f} - {rp:.0f}}}{{{ra:.0f} + {rp:.0f}}} = {e:.6f}\n$$\n\n"
           f"$a = {a:.1f}$ km\n\n"
           f"$$\n\\varepsilon = -\\frac{{\\mu}}{{2a}} = -\\frac{{{MU_EARTH}}}{{2 \\times {a:.1f}}} = {eps:.4f} \\text{{ km}}^2/\\text{{s}}^2\n$$\n")
    return Problem("Eccentricity & energy", stmt, sol)

GENERATORS = [gen_period, gen_circular_v, gen_escape_v, gen_vis_viva, gen_eccentricity]

def main():
    parser = argparse.ArgumentParser(description="Generate Two-Body & Kepler practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, two-body, kepler]\n---\n",
             "# 10.1 Practice — Two-Body Problem & Kepler's Laws\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()

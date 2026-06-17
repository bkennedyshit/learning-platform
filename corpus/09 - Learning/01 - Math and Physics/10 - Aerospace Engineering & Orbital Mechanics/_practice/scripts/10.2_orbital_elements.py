#!/usr/bin/env python3
"""
10.2_orbital_elements.py — Practice problem generator for Chapter 10.2
(Orbital Elements & Conic Sections).

Archetypes:
  1. Compute orbital elements from r_p, r_a
  2. Solve Kepler's equation (Newton-Raphson)
  3. True anomaly from eccentric anomaly
  4. Perifocal position/velocity from elements
  5. Flight path angle computation

Usage:
  python 10.2_orbital_elements.py --count 15 --seed 7
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

MU = 398600.4418

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_elements_from_apsides(rng: random.Random) -> Problem:
    rp = 6371 + rng.randint(200, 2000)
    ra = 6371 + rng.randint(5000, 42000)
    a = (rp + ra) / 2
    e = (ra - rp) / (ra + rp)
    p = a * (1 - e**2)
    T = 2 * math.pi * math.sqrt(a**3 / MU)
    stmt = f"Given perigee radius $r_p = {rp}$ km and apogee radius $r_a = {ra}$ km, find $a$, $e$, $p$, and $T$."
    sol = (f"$a = (r_p+r_a)/2 = {a:.1f}$ km\n\n"
           f"$e = (r_a-r_p)/(r_a+r_p) = {e:.6f}$\n\n"
           f"$p = a(1-e^2) = {p:.1f}$ km\n\n"
           f"$T = 2\\pi\\sqrt{{a^3/\\mu}} = {T:.1f}$ s = {T/3600:.2f} hr")
    return Problem("Elements from apsides", stmt, sol)

def gen_kepler_equation(rng: random.Random) -> Problem:
    e = round(rng.uniform(0.1, 0.8), 4)
    M = round(rng.uniform(0.5, 5.5), 4)
    # Solve by Newton-Raphson
    E = M
    for _ in range(20):
        f = E - e * math.sin(E) - M
        fp = 1 - e * math.cos(E)
        E = E - f / fp
        if abs(f) < 1e-12:
            break
    stmt = (f"Solve Kepler's equation $M = E - e\\sin E$ for $E$ given $e = {e}$ and $M = {M}$ rad. "
            f"Use Newton-Raphson with $E_0 = M$.")
    sol = (f"After Newton-Raphson iteration:\n\n"
           f"$$\nE = {E:.8f} \\text{{ rad}} = {math.degrees(E):.4f}°\n$$\n\n"
           f"Verify: $E - e\\sin E = {E:.8f} - {e}\\times\\sin({E:.8f}) = {E - e*math.sin(E):.10f} \\approx M = {M}$ ✓")
    return Problem("Kepler's equation (Newton-Raphson)", stmt, sol)

def gen_true_from_eccentric(rng: random.Random) -> Problem:
    e = round(rng.uniform(0.05, 0.7), 4)
    E = round(rng.uniform(0, 2*math.pi), 4)
    nu = 2 * math.atan2(math.sqrt(1+e) * math.sin(E/2), math.sqrt(1-e) * math.cos(E/2))
    if nu < 0: nu += 2*math.pi
    stmt = f"Given $e = {e}$ and eccentric anomaly $E = {E}$ rad, compute true anomaly $\\nu$."
    sol = (f"$$\n\\tan\\frac{{\\nu}}{{2}} = \\sqrt{{\\frac{{1+e}}{{1-e}}}}\\tan\\frac{{E}}{{2}} = "
           f"\\sqrt{{\\frac{{{1+e:.4f}}}{{{1-e:.4f}}}}}\\tan({E/2:.4f})\n$$\n\n"
           f"$\\nu = {nu:.6f}$ rad $= {math.degrees(nu):.2f}°$")
    return Problem("True anomaly from eccentric anomaly", stmt, sol)

def gen_perifocal(rng: random.Random) -> Problem:
    a = rng.randint(7000, 30000)
    e = round(rng.uniform(0.01, 0.6), 4)
    nu = round(rng.uniform(0, 2*math.pi), 4)
    p = a * (1 - e**2)
    r = p / (1 + e * math.cos(nu))
    h = math.sqrt(MU * p)
    rx, ry = r * math.cos(nu), r * math.sin(nu)
    vx, vy = -MU/h * math.sin(nu), MU/h * (e + math.cos(nu))
    stmt = (f"Given $a = {a}$ km, $e = {e}$, $\\nu = {math.degrees(nu):.1f}°$. "
            f"Compute position and velocity in the perifocal frame.")
    sol = (f"$p = a(1-e^2) = {p:.1f}$ km, $r = p/(1+e\\cos\\nu) = {r:.1f}$ km, $h = \\sqrt{{\\mu p}} = {h:.1f}$ km²/s\n\n"
           f"$\\mathbf{{r}}_{{pqw}} = ({rx:.1f},\\; {ry:.1f},\\; 0)$ km\n\n"
           f"$\\mathbf{{v}}_{{pqw}} = ({vx:.4f},\\; {vy:.4f},\\; 0)$ km/s")
    return Problem("Perifocal position & velocity", stmt, sol)

def gen_flight_path(rng: random.Random) -> Problem:
    e = round(rng.uniform(0.1, 0.7), 4)
    nu = round(rng.uniform(0.2, 5.8), 4)
    gamma = math.atan2(e * math.sin(nu), 1 + e * math.cos(nu))
    stmt = f"For an orbit with $e = {e}$ at true anomaly $\\nu = {math.degrees(nu):.1f}°$, compute the flight path angle $\\gamma$."
    sol = (f"$$\n\\tan\\gamma = \\frac{{e\\sin\\nu}}{{1+e\\cos\\nu}} = "
           f"\\frac{{{e}\\times{math.sin(nu):.4f}}}{{1+{e}\\times{math.cos(nu):.4f}}} = {math.tan(gamma):.6f}\n$$\n\n"
           f"$\\gamma = {math.degrees(gamma):.4f}°$")
    return Problem("Flight path angle", stmt, sol)

GENERATORS = [gen_elements_from_apsides, gen_kepler_equation, gen_true_from_eccentric, gen_perifocal, gen_flight_path]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, orbital-elements]\n---\n",
             "# 10.2 Practice — Orbital Elements & Conic Sections\n\n"]
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

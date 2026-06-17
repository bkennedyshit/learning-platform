#!/usr/bin/env python3
"""
6.3_euler.py — Practice problem generator for Chapter 6.3
(Inviscid Fluids — Euler's Equation).

Archetypes:
  1. Bernoulli equation along a streamline
  2. Pitot tube velocity calculation
  3. Torricelli's theorem (draining tank)
  4. Pressure field from given velocity (irrotational)
  5. Venturi meter flow rate

Usage:
  python 6.3_euler.py --count 12 --seed 42
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

def gen_bernoulli(rng: random.Random) -> Problem:
    v1 = rng.randint(2, 10)
    p1 = rng.randint(100, 300) * 1000
    rho = 1000
    z1, z2 = 0, rng.randint(1, 5)
    g = 9.81
    B = p1 + 0.5*rho*v1**2 + rho*g*z1
    v2 = rng.randint(v1+2, v1+10)
    p2 = B - 0.5*rho*v2**2 - rho*g*z2
    stmt = (f"Water ($\\rho={rho}$ kg/m³) flows along a streamline. At point 1: "
            f"$v_1={v1}$ m/s, $p_1={p1/1000:.0f}$ kPa, $z_1={z1}$ m. "
            f"At point 2: $v_2={v2}$ m/s, $z_2={z2}$ m. Find $p_2$.")
    sol = (f"Bernoulli: $p_1 + \\frac{{1}}{{2}}\\rho v_1^2 + \\rho g z_1 = p_2 + \\frac{{1}}{{2}}\\rho v_2^2 + \\rho g z_2$.\n\n"
           f"$p_2 = {p1/1000:.0f}\\times10^3 + \\frac{{1}}{{2}}(1000)({v1}^2-{v2}^2) + 1000(9.81)({z1}-{z2})$\n\n"
           f"$p_2 = {p2:.0f}$ Pa $= {p2/1000:.2f}$ kPa.")
    return Problem("Bernoulli along streamline", stmt, sol)

def gen_pitot(rng: random.Random) -> Problem:
    rho = rng.choice([1.225, 1.0, 0.9])
    dp = rng.randint(500, 5000)
    v = math.sqrt(2*dp/rho)
    stmt = (f"A Pitot tube measures $\\Delta p = p_0 - p = {dp}$ Pa in air ($\\rho={rho}$ kg/m³). Find airspeed.")
    sol = (f"$v = \\sqrt{{2\\Delta p/\\rho}} = \\sqrt{{2\\times{dp}/{rho}}} = {v:.2f}$ m/s.")
    return Problem("Pitot tube", stmt, sol)

def gen_torricelli(rng: random.Random) -> Problem:
    h = rng.randint(1, 20)
    v = math.sqrt(2*9.81*h)
    stmt = f"A large tank has water level $h={h}$ m above an orifice. Find exit velocity (Torricelli)."
    sol = f"$v = \\sqrt{{2gh}} = \\sqrt{{2(9.81)({h})}} = {v:.2f}$ m/s."
    return Problem("Torricelli's theorem", stmt, sol)

def gen_pressure_vortex(rng: random.Random) -> Problem:
    Gamma = rng.randint(1, 10)
    r = rng.choice([0.5, 1.0, 2.0])
    rho = 1000
    p_inf = 101325
    v_theta = Gamma / (2*math.pi*r)
    p = p_inf - 0.5*rho*v_theta**2
    stmt = (f"An irrotational vortex has $\\Gamma={Gamma}$ m²/s in water ($\\rho={rho}$). "
            f"Find pressure at $r={r}$ m if $p_\\infty={p_inf}$ Pa.")
    sol = (f"$v_\\theta = \\Gamma/(2\\pi r) = {Gamma}/(2\\pi\\times{r}) = {v_theta:.4f}$ m/s.\n\n"
           f"$p = p_\\infty - \\frac{{1}}{{2}}\\rho v^2 = {p_inf} - 0.5({rho})({v_theta:.4f})^2 = {p:.2f}$ Pa.")
    return Problem("Pressure in irrotational vortex", stmt, sol)

def gen_venturi(rng: random.Random) -> Problem:
    D1 = rng.choice([0.1, 0.15, 0.2])
    D2 = round(D1 * rng.choice([0.5, 0.6, 0.7]), 3)
    dp = rng.randint(5000, 50000)
    rho = 1000
    A1, A2 = math.pi*D1**2/4, math.pi*D2**2/4
    v2 = math.sqrt(2*dp/(rho*(1-(A2/A1)**2)))
    Q = v2 * A2
    stmt = (f"A Venturi meter has $D_1={D1}$ m, $D_2={D2}$ m. Pressure drop $\\Delta p={dp}$ Pa. "
            f"Find volume flow rate ($\\rho={rho}$ kg/m³).")
    sol = (f"$v_2 = \\sqrt{{\\frac{{2\\Delta p}}{{\\rho(1-(A_2/A_1)^2)}}}} = {v2:.3f}$ m/s.\n\n"
           f"$Q = v_2 A_2 = {v2:.3f}\\times{A2:.6f} = {Q:.5f}$ m³/s = {Q*1000:.2f} L/s.")
    return Problem("Venturi meter", stmt, sol)

GENERATORS = [gen_bernoulli, gen_pitot, gen_torricelli, gen_pressure_vortex, gen_venturi]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.3 Practice — Euler's Equation & Bernoulli\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

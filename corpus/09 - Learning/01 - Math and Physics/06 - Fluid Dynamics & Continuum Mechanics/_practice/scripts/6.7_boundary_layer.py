#!/usr/bin/env python3
"""
6.7_boundary_layer.py — Practice problem generator for Chapter 6.7
(Boundary Layer Theory — Blasius Solution).

Archetypes:
  1. Boundary layer thickness (Blasius)
  2. Skin friction coefficient
  3. Drag on a flat plate
  4. Displacement and momentum thickness
  5. Von Kármán integral method

Usage:
  python 6.7_boundary_layer.py --count 12 --seed 42
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

def gen_bl_thickness(rng: random.Random) -> Problem:
    U = rng.randint(5, 50)
    nu = rng.choice([1.5e-5, 1e-6, 1e-4])
    x_val = rng.choice([0.5, 1.0, 2.0, 5.0])
    Re_x = U * x_val / nu
    delta = 5.0 * x_val / math.sqrt(Re_x)
    stmt = (f"Air flows at $U={U}$ m/s over a flat plate ($\\nu={nu}$ m²/s). "
            f"Find $\\delta_{{99}}$ at $x={x_val}$ m.")
    sol = (f"$\\text{{Re}}_x = Ux/\\nu = {U}\\times{x_val}/{nu} = {Re_x:.0f}$.\n\n"
           f"$\\delta_{{99}} = 5.0x/\\sqrt{{\\text{{Re}}_x}} = 5.0\\times{x_val}/\\sqrt{{{Re_x:.0f}}} = {delta*1000:.2f}$ mm.")
    return Problem("Boundary layer thickness", stmt, sol)

def gen_cf(rng: random.Random) -> Problem:
    Re_x = rng.choice([1e5, 5e5, 1e6, 5e6])
    cf = 0.664 / math.sqrt(Re_x)
    stmt = f"Find the local skin friction coefficient at $\\text{{Re}}_x = {Re_x:.0e}$ (Blasius)."
    sol = f"$c_f = 0.664/\\sqrt{{\\text{{Re}}_x}} = 0.664/\\sqrt{{{Re_x:.0e}}} = {cf:.6f}$."
    return Problem("Skin friction coefficient", stmt, sol)

def gen_plate_drag(rng: random.Random) -> Problem:
    U = rng.randint(10, 50)
    L = rng.choice([1.0, 2.0, 5.0])
    b = rng.choice([0.5, 1.0, 2.0])
    rho = rng.choice([1.225, 1.0])
    nu = 1.5e-5
    Re_L = U * L / nu
    CD = 1.328 / math.sqrt(Re_L)
    FD = CD * 0.5 * rho * U**2 * b * L
    stmt = (f"Flat plate: $L={L}$ m, $b={b}$ m, $U={U}$ m/s, $\\rho={rho}$ kg/m³, "
            f"$\\nu={nu}$ m²/s. Find total drag (one side, laminar).")
    sol = (f"$\\text{{Re}}_L = {Re_L:.0f}$.\n\n"
           f"$C_D = 1.328/\\sqrt{{\\text{{Re}}_L}} = {CD:.6f}$.\n\n"
           f"$F_D = C_D \\cdot \\frac{{1}}{{2}}\\rho U^2 bL = {FD:.4f}$ N.")
    return Problem("Flat plate drag", stmt, sol)

def gen_thicknesses(rng: random.Random) -> Problem:
    U = rng.randint(10, 40)
    nu = 1.5e-5
    x_val = rng.choice([0.5, 1.0, 2.0])
    Re_x = U * x_val / nu
    delta_star = 1.7208 * x_val / math.sqrt(Re_x)
    theta = 0.6641 * x_val / math.sqrt(Re_x)
    H = delta_star / theta
    stmt = (f"At $x={x_val}$ m on a flat plate ($U={U}$ m/s, $\\nu={nu}$ m²/s), "
            f"find $\\delta^*$, $\\theta$, and shape factor $H$.")
    sol = (f"$\\text{{Re}}_x = {Re_x:.0f}$.\n\n"
           f"$\\delta^* = 1.7208x/\\sqrt{{\\text{{Re}}_x}} = {delta_star*1000:.3f}$ mm.\n\n"
           f"$\\theta = 0.6641x/\\sqrt{{\\text{{Re}}_x}} = {theta*1000:.3f}$ mm.\n\n"
           f"$H = \\delta^*/\\theta = {H:.3f}$ (Blasius: 2.59).")
    return Problem("Displacement & momentum thickness", stmt, sol)

def gen_karman(rng: random.Random) -> Problem:
    stmt = ("Using the linear profile $u/U = y/\\delta$ in the von Kármán equation for a flat plate, "
            "derive $\\delta(x)$.")
    sol = ("$\\delta^* = \\delta/2$, $\\theta = \\delta/6$.\n\n"
           "$\\tau_w = \\mu U/\\delta$, $c_f/2 = \\nu/(U\\delta)$.\n\n"
           "Von Kármán: $d\\theta/dx = c_f/2$ → $(1/6)d\\delta/dx = \\nu/(U\\delta)$.\n\n"
           "$\\delta\\,d\\delta = 6\\nu/U\\,dx$ → $\\delta^2/2 = 6\\nu x/U$ → $\\delta = \\sqrt{12\\nu x/U} = 3.46x/\\sqrt{\\text{Re}_x}$.\n\n"
           "Compare Blasius: 5.0. Linear profile underestimates by ~30%.")
    return Problem("Von Kármán integral (linear profile)", stmt, sol)

GENERATORS = [gen_bl_thickness, gen_cf, gen_plate_drag, gen_thicknesses, gen_karman]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.7 Practice — Boundary Layer Theory\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

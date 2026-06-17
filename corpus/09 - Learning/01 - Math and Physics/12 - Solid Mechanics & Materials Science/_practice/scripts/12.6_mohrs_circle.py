#!/usr/bin/env python3
"""
12.6_mohrs_circle.py — Practice problem generator for Chapter 12.6
(Principal Stresses & Mohr's Circle).

Archetypes:
  1. Compute σ₁, σ₂, τ_max from given σ_x, σ_y, τ_xy
  2. Find stress on arbitrary plane (given θ)
  3. Principal directions (angle θ_p)
  4. 3D principal stresses (eigenvalue of 3×3)
  5. Combined bending + torsion → principal stresses

Usage:
  python 12.6_mohrs_circle.py --count 15 --seed 42
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

def gen_principal_2d(rng: random.Random) -> Problem:
    sxx = rng.randint(-100, 150)
    syy = rng.randint(-100, 150)
    txy = rng.randint(-80, 80)
    while txy == 0 and sxx == syy:
        txy = rng.randint(-80, 80)
    C = (sxx + syy) / 2
    R = math.sqrt(((sxx - syy) / 2)**2 + txy**2)
    s1, s2 = C + R, C - R
    tau_max = R
    tp = 0.5 * math.degrees(math.atan2(2*txy, sxx - syy))
    stmt = (f"Given: $\\sigma_x = {sxx}$, $\\sigma_y = {syy}$, $\\tau_{{xy}} = {txy}$ MPa. "
            f"Find $\\sigma_1$, $\\sigma_2$, $\\tau_{{\\max}}$, and $\\theta_p$.")
    sol = (f"$C = ({sxx}+{syy})/2 = {C:.1f}$ MPa\n\n"
           f"$R = \\sqrt{{({(sxx-syy)/2:.1f})^2 + {txy}^2}} = {R:.2f}$ MPa\n\n"
           f"$\\sigma_1 = {s1:.2f}$ MPa, $\\sigma_2 = {s2:.2f}$ MPa\n\n"
           f"$\\tau_{{\\max}} = R = {tau_max:.2f}$ MPa\n\n"
           f"$\\theta_p = \\frac{{1}}{{2}}\\arctan\\frac{{2({txy})}}{{{sxx}-{syy}}} = {tp:.2f}°$")
    return Problem("Principal stresses (Mohr's Circle)", stmt, sol)

def gen_stress_on_plane(rng: random.Random) -> Problem:
    sxx = rng.randint(-60, 120)
    syy = rng.randint(-60, 120)
    txy = rng.randint(-50, 50)
    theta = rng.choice([20, 25, 30, 35, 40, 45, 50, 55, 60])
    c2 = math.cos(math.radians(2*theta))
    s2 = math.sin(math.radians(2*theta))
    avg = (sxx + syy) / 2
    diff = (sxx - syy) / 2
    sx_new = avg + diff*c2 + txy*s2
    tau_new = -diff*s2 + txy*c2
    stmt = (f"Given: $\\sigma_x={sxx}$, $\\sigma_y={syy}$, $\\tau_{{xy}}={txy}$ MPa. "
            f"Find stresses on plane at $\\theta = {theta}°$.")
    sol = (f"$\\sigma_{{x'}} = {avg:.1f} + {diff:.1f}\\cos{2*theta}° + {txy}\\sin{2*theta}° = {sx_new:.2f}$ MPa\n\n"
           f"$\\tau_{{x'y'}} = -{diff:.1f}\\sin{2*theta}° + {txy}\\cos{2*theta}° = {tau_new:.2f}$ MPa")
    return Problem("Stress on arbitrary plane", stmt, sol)

def gen_3d_principal(rng: random.Random) -> Problem:
    sxx = rng.randint(20, 150)
    syy = rng.randint(-50, 100)
    txy = rng.randint(-60, 60)
    szz = rng.randint(-40, 80)
    # Assume τ_xz = τ_yz = 0 so z is already principal
    C = (sxx + syy) / 2
    R = math.sqrt(((sxx - syy)/2)**2 + txy**2)
    s1 = C + R
    s2 = C - R
    s3 = szz
    ordered = sorted([s1, s2, s3], reverse=True)
    tau_abs = (ordered[0] - ordered[2]) / 2
    stmt = (f"3D stress: $\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\sigma_{{zz}}={szz}$, "
            f"$\\tau_{{xy}}={txy}$, $\\tau_{{xz}}=\\tau_{{yz}}=0$ MPa. "
            f"Find all principal stresses and absolute max shear.")
    sol = (f"$z$ is already principal ($\\sigma_3' = {szz}$ MPa).\n\n"
           f"In-plane: $C = {C:.1f}$, $R = {R:.2f}$ MPa\n\n"
           f"$\\sigma_1 = {ordered[0]:.2f}$, $\\sigma_2 = {ordered[1]:.2f}$, $\\sigma_3 = {ordered[2]:.2f}$ MPa\n\n"
           f"$\\tau_{{abs\\,max}} = (\\sigma_1 - \\sigma_3)/2 = ({ordered[0]:.2f} - {ordered[2]:.2f})/2 = {tau_abs:.2f}$ MPa")
    return Problem("3D principal stresses", stmt, sol)

def gen_combined_loading(rng: random.Random) -> Problem:
    d = rng.choice([30, 40, 50, 60, 80])
    M = rng.choice([500, 800, 1000, 1500, 2000, 3000])
    T = rng.choice([300, 500, 800, 1000, 1500, 2000])
    c = d / 2000
    I = math.pi * (d/2000)**4 / 4
    J = 2 * I
    sigma = M * c / I / 1e6  # MPa
    tau = T * c / J / 1e6
    C = sigma / 2
    R = math.sqrt(C**2 + tau**2)
    s1, s2 = C + R, C - R
    stmt = (f"Shaft $d={d}$ mm under $M={M}$ N·m and $T={T}$ N·m. "
            f"Find principal stresses at the surface.")
    sol = (f"$\\sigma = Mc/I = {sigma:.1f}$ MPa, $\\tau = Tc/J = {tau:.1f}$ MPa\n\n"
           f"$C = \\sigma/2 = {C:.1f}$ MPa, $R = \\sqrt{{C^2 + \\tau^2}} = {R:.1f}$ MPa\n\n"
           f"$\\sigma_1 = {s1:.1f}$ MPa, $\\sigma_2 = {s2:.1f}$ MPa\n\n"
           f"$\\tau_{{\\max}} = R = {R:.1f}$ MPa")
    return Problem("Combined bending + torsion", stmt, sol)

GENERATORS = [gen_principal_2d, gen_stress_on_plane, gen_3d_principal, gen_combined_loading]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.6 Mohr's Circle problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.6 Principal Stresses & Mohr's Circle — Practice Problems\n",
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

#!/usr/bin/env python3
"""
12.2_stress_strain.py — Practice problem generator for Chapter 12.2
(Stress & Strain Tensors).

Archetypes:
  1. Traction vector on inclined plane
  2. Strain from displacement field
  3. Hydrostatic-deviatoric decomposition
  4. Stress transformation (2D rotation)
  5. Principal stresses (2D eigenvalue)

Usage:
  python 12.2_stress_strain.py --count 15 --seed 7
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

def gen_traction(rng: random.Random) -> Problem:
    sxx = rng.randint(-80, 120)
    syy = rng.randint(-80, 120)
    txy = rng.randint(-60, 60)
    angle = rng.choice([30, 45, 60, 120, 135, 150])
    nx = round(math.cos(math.radians(angle)), 4)
    ny = round(math.sin(math.radians(angle)), 4)
    tx = sxx * nx + txy * ny
    ty = txy * nx + syy * ny
    sn = tx * nx + ty * ny
    tau = math.sqrt(tx**2 + ty**2 - sn**2)
    stmt = (f"Given $\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\tau_{{xy}}={txy}$ MPa. "
            f"A plane has outward normal at ${angle}°$ from $x$-axis. "
            f"Find the traction vector, normal stress, and shear stress on this plane.")
    sol = (f"$\\hat{{n}} = ({nx:.4f},\\,{ny:.4f})$\n\n"
           f"$t_x = \\sigma_{{xx}}n_x + \\tau_{{xy}}n_y = {sxx}({nx:.4f}) + {txy}({ny:.4f}) = {tx:.2f}$ MPa\n\n"
           f"$t_y = \\tau_{{xy}}n_x + \\sigma_{{yy}}n_y = {txy}({nx:.4f}) + {syy}({ny:.4f}) = {ty:.2f}$ MPa\n\n"
           f"$\\sigma_n = t_x n_x + t_y n_y = {sn:.2f}$ MPa\n\n"
           f"$\\tau = \\sqrt{{|\\mathbf{{t}}|^2 - \\sigma_n^2}} = {tau:.2f}$ MPa")
    return Problem("Traction vector on inclined plane", stmt, sol)

def gen_strain_field(rng: random.Random) -> Problem:
    a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]
    x0, y0 = rng.randint(1, 3), rng.randint(1, 3)
    # u_x = a*x^2 + b*x*y, u_y = c*x*y + d*y^2 (×10^-4)
    exx = 2*a*x0 + b*y0
    eyy = c*x0 + 2*d*y0
    gxy = b*x0 + c*y0
    exy = sp.Rational(gxy, 2)
    stmt = (f"Displacement field: $u_x = ({a}x^2 + {b}xy)\\times10^{{-4}}$, "
            f"$u_y = ({c}xy + {d}y^2)\\times10^{{-4}}$. "
            f"Find strain components at $({x0},{y0})$.")
    sol = (f"$\\varepsilon_{{xx}} = \\partial u_x/\\partial x = (2\\cdot{a}\\cdot x + {b}y)\\times10^{{-4}}$"
           f" → at $({x0},{y0})$: ${exx}\\times10^{{-4}}$\n\n"
           f"$\\varepsilon_{{yy}} = \\partial u_y/\\partial y = ({c}x + 2\\cdot{d}\\cdot y)\\times10^{{-4}}$"
           f" → at $({x0},{y0})$: ${eyy}\\times10^{{-4}}$\n\n"
           f"$\\gamma_{{xy}} = \\partial u_x/\\partial y + \\partial u_y/\\partial x = ({b}x + {c}y)\\times10^{{-4}}$"
           f" → at $({x0},{y0})$: ${gxy}\\times10^{{-4}}$\n\n"
           f"$\\varepsilon_{{xy}} = \\gamma_{{xy}}/2 = {sp.latex(exy)}\\times10^{{-4}}$")
    return Problem("Strain from displacement field", stmt, sol)

def gen_decomposition(rng: random.Random) -> Problem:
    sxx = rng.randint(-50, 150)
    syy = rng.randint(-50, 150)
    szz = rng.randint(-50, 150)
    sm = sp.Rational(sxx + syy + szz, 3)
    stmt = (f"Given $\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\sigma_{{zz}}={szz}$ MPa "
            f"(all shear = 0). Decompose into hydrostatic and deviatoric parts.")
    sol = (f"$\\sigma_m = ({sxx}+{syy}+{szz})/3 = {sp.latex(sm)}$ MPa\n\n"
           f"Deviatoric: $s_{{xx}} = {sxx} - {sp.latex(sm)} = {sp.latex(sxx - sm)}$ MPa\n\n"
           f"$s_{{yy}} = {syy} - {sp.latex(sm)} = {sp.latex(syy - sm)}$ MPa\n\n"
           f"$s_{{zz}} = {szz} - {sp.latex(sm)} = {sp.latex(szz - sm)}$ MPa\n\n"
           f"Check: $s_{{xx}}+s_{{yy}}+s_{{zz}} = {sp.latex(sxx-sm+syy-sm+szz-sm)} = 0$ ✓")
    return Problem("Hydrostatic-deviatoric decomposition", stmt, sol)

def gen_transform_2d(rng: random.Random) -> Problem:
    sxx = rng.randint(-60, 100)
    syy = rng.randint(-60, 100)
    txy = rng.randint(-50, 50)
    theta = rng.choice([15, 25, 30, 40, 45, 60])
    c2 = math.cos(math.radians(2*theta))
    s2 = math.sin(math.radians(2*theta))
    avg = (sxx + syy) / 2
    diff = (sxx - syy) / 2
    sx_new = avg + diff*c2 + txy*s2
    tau_new = -diff*s2 + txy*c2
    stmt = (f"Given $\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\tau_{{xy}}={txy}$ MPa. "
            f"Find stresses on a plane at $\\theta={theta}°$ from $x$-axis.")
    sol = (f"$\\sigma_{{x'}} = \\frac{{{sxx}+{syy}}}{{2}} + \\frac{{{sxx}-{syy}}}{{2}}\\cos{2*theta}° + {txy}\\sin{2*theta}°$\n\n"
           f"$= {avg:.1f} + {diff:.1f}({c2:.4f}) + {txy}({s2:.4f}) = {sx_new:.2f}$ MPa\n\n"
           f"$\\tau_{{x'y'}} = -\\frac{{{sxx}-{syy}}}{{2}}\\sin{2*theta}° + {txy}\\cos{2*theta}°$\n\n"
           f"$= -{diff:.1f}({s2:.4f}) + {txy}({c2:.4f}) = {tau_new:.2f}$ MPa")
    return Problem("2D stress transformation", stmt, sol)

def gen_principal_2d(rng: random.Random) -> Problem:
    sxx = rng.randint(-80, 120)
    syy = rng.randint(-80, 120)
    txy = rng.randint(-60, 60)
    while txy == 0 and sxx == syy:
        txy = rng.randint(-60, 60)
    C = (sxx + syy) / 2
    R = math.sqrt(((sxx - syy)/2)**2 + txy**2)
    s1 = C + R
    s2 = C - R
    theta_p = 0.5 * math.degrees(math.atan2(2*txy, sxx - syy))
    stmt = (f"Given $\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\tau_{{xy}}={txy}$ MPa. "
            f"Find principal stresses and maximum shear stress.")
    sol = (f"$C = ({sxx}+{syy})/2 = {C:.1f}$ MPa\n\n"
           f"$R = \\sqrt{{(({sxx}-{syy})/2)^2 + {txy}^2}} = \\sqrt{{{((sxx-syy)/2)**2:.1f} + {txy**2}}} = {R:.2f}$ MPa\n\n"
           f"$\\sigma_1 = C + R = {s1:.2f}$ MPa\n\n"
           f"$\\sigma_2 = C - R = {s2:.2f}$ MPa\n\n"
           f"$\\tau_{{\\max}} = R = {R:.2f}$ MPa\n\n"
           f"$\\theta_p = {theta_p:.2f}°$")
    return Problem("Principal stresses (2D)", stmt, sol)

GENERATORS = [gen_traction, gen_strain_field, gen_decomposition, gen_transform_2d, gen_principal_2d]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.2 Stress/Strain problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.2 Stress & Strain Tensors — Practice Problems\n",
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

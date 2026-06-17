#!/usr/bin/env python3
"""
6.1_stress_strain.py — Practice problem generator for Chapter 6.1
(Stress & Strain Tensors in Continua).

Generates randomized drill problems across 6 archetypes:
  1. Traction vector on an inclined plane (Cauchy's formula)
  2. Principal stresses (2D eigenvalue problem)
  3. Strain-rate tensor from velocity field
  4. Hydrostatic/deviatoric decomposition
  5. Maximum shear stress computation
  6. Mohr's circle radius and center

Usage:
  python 6.1_stress_strain.py
  python 6.1_stress_strain.py --count 12 --seed 42
  python 6.1_stress_strain.py --count 12 --seed 42 --out /tmp/_61.md
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
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )

def gen_traction(rng: random.Random) -> Problem:
    s = [[rng.randint(-50,50) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i+1,3):
            s[j][i] = s[i][j]
    ang = rng.choice([30,45,60])
    rad = math.radians(ang)
    n1, n2, n3 = round(math.cos(rad),4), round(math.sin(rad),4), 0
    t = [sum(s[i][j]*(n1 if j==0 else n2 if j==1 else n3) for j in range(3)) for i in range(3)]
    sig_n = sum(t[i]*(n1 if i==0 else n2 if i==1 else n3) for i in range(3))
    tau = math.sqrt(sum(ti**2 for ti in t) - sig_n**2)
    S = sp.Matrix(3,3,lambda i,j: s[i][j])
    stmt = (f"Given stress tensor $\\boldsymbol{{\\sigma}} = {sp.latex(S)}$ MPa and surface normal "
            f"$\\hat{{n}} = (\\cos{ang}°,\\sin{ang}°,0)$, compute the traction vector, "
            f"normal stress $\\sigma_n$, and shear stress $\\tau$.")
    sol = (f"$\\mathbf{{t}} = \\boldsymbol{{\\sigma}}\\hat{{n}} = ({t[0]:.2f},\\;{t[1]:.2f},\\;{t[2]:.2f})$ MPa.\n\n"
           f"$\\sigma_n = \\mathbf{{t}}\\cdot\\hat{{n}} = {sig_n:.2f}$ MPa.\n\n"
           f"$\\tau = \\sqrt{{|\\mathbf{{t}}|^2 - \\sigma_n^2}} = {tau:.2f}$ MPa.")
    return Problem("Traction on inclined plane", stmt, sol)

def gen_principal_2d(rng: random.Random) -> Problem:
    s11, s22, s12 = rng.randint(-80,80), rng.randint(-80,80), rng.randint(-40,40)
    avg = (s11+s22)/2
    R = math.sqrt(((s11-s22)/2)**2 + s12**2)
    sig1, sig2 = avg+R, avg-R
    theta = 0.5*math.degrees(math.atan2(2*s12, s11-s22))
    stmt = (f"Find the principal stresses and principal angle for the 2D stress state "
            f"$\\sigma_{{11}}={s11}$, $\\sigma_{{22}}={s22}$, $\\sigma_{{12}}={s12}$ MPa.")
    sol = (f"Center $= (\\sigma_{{11}}+\\sigma_{{22}})/2 = {avg:.1f}$ MPa.\n\n"
           f"Radius $R = \\sqrt{{((\\sigma_{{11}}-\\sigma_{{22}})/2)^2 + \\sigma_{{12}}^2}} = {R:.2f}$ MPa.\n\n"
           f"$\\sigma_1 = {sig1:.2f}$ MPa, $\\sigma_2 = {sig2:.2f}$ MPa.\n\n"
           f"$\\theta_p = \\frac{{1}}{{2}}\\arctan\\frac{{2\\sigma_{{12}}}}{{\\sigma_{{11}}-\\sigma_{{22}}}} = {theta:.2f}°$.")
    return Problem("Principal stresses (2D)", stmt, sol)

def gen_strain_rate(rng: random.Random) -> Problem:
    a,b,c = rng.randint(1,5), rng.randint(1,5), rng.randint(1,5)
    stmt = (f"For velocity field $\\mathbf{{v}} = ({a}xy,\\;-{b}y^2,\\;{c}z)$, "
            f"compute the strain-rate tensor $S_{{ij}}$ and verify the trace equals $\\nabla\\cdot\\mathbf{{v}}$.")
    L = [[f"{a}y",f"{a}x","0"],[f"0",f"-{2*b}y","0"],["0","0",f"{c}"]]
    div_v = f"{a}y - {2*b}y + {c}"
    sol = (f"$L_{{ij}} = \\partial v_i/\\partial x_j$:\n\n"
           f"$L = \\begin{{pmatrix}} {a}y & {a}x & 0 \\\\ 0 & -{2*b}y & 0 \\\\ 0 & 0 & {c} \\end{{pmatrix}}$\n\n"
           f"$S_{{ij}} = (L_{{ij}}+L_{{ji}})/2$:\n\n"
           f"$S = \\begin{{pmatrix}} {a}y & {a}x/2 & 0 \\\\ {a}x/2 & -{2*b}y & 0 \\\\ 0 & 0 & {c} \\end{{pmatrix}}$\n\n"
           f"Trace: $S_{{kk}} = {a}y - {2*b}y + {c} = \\nabla\\cdot\\mathbf{{v}}$. ✓")
    return Problem("Strain-rate tensor computation", stmt, sol)

def gen_decomposition(rng: random.Random) -> Problem:
    diag = [rng.randint(-100,100) for _ in range(3)]
    off = [rng.randint(-30,30) for _ in range(3)]
    p = -sum(diag)/3
    stmt = (f"Decompose $\\boldsymbol{{\\sigma}} = \\text{{diag}}({diag[0]},{diag[1]},{diag[2]})$ + "
            f"off-diagonal $\\sigma_{{12}}={off[0]}$, $\\sigma_{{13}}={off[1]}$, $\\sigma_{{23}}={off[2]}$ MPa "
            f"into hydrostatic and deviatoric parts.")
    sol = (f"$p = -\\sigma_{{kk}}/3 = -({diag[0]}+{diag[1]}+{diag[2]})/3 = {p:.2f}$ MPa.\n\n"
           f"Hydrostatic: $\\sigma^{{(h)}}_{{ij}} = -p\\delta_{{ij}} = {-p:.2f}\\,\\delta_{{ij}}$.\n\n"
           f"Deviatoric diagonal: $({diag[0]-(-p):.2f},\\;{diag[1]-(-p):.2f},\\;{diag[2]-(-p):.2f})$.\n\n"
           f"Off-diagonal unchanged: $\\tau_{{12}}={off[0]},\\tau_{{13}}={off[1]},\\tau_{{23}}={off[2]}$.\n\n"
           f"Verify trace-free: ${diag[0]-(-p):.2f}+{diag[1]-(-p):.2f}+{diag[2]-(-p):.2f} = 0$. ✓")
    return Problem("Hydrostatic/deviatoric decomposition", stmt, sol)

def gen_max_shear(rng: random.Random) -> Problem:
    s1,s2,s3 = sorted([rng.randint(-60,60) for _ in range(3)], reverse=True)
    tau_max = (s1-s3)/2
    stmt = (f"Given principal stresses $\\sigma_1={s1}$, $\\sigma_2={s2}$, $\\sigma_3={s3}$ MPa, "
            f"find the maximum shear stress and the plane on which it acts.")
    sol = (f"$\\tau_{{\\max}} = (\\sigma_1 - \\sigma_3)/2 = ({s1}-({s3}))/2 = {tau_max:.1f}$ MPa.\n\n"
           f"Acts on planes at 45° to the $\\sigma_1$ and $\\sigma_3$ principal directions.")
    return Problem("Maximum shear stress", stmt, sol)

def gen_mohr(rng: random.Random) -> Problem:
    s11,s22,s12 = rng.randint(-50,50), rng.randint(-50,50), rng.randint(-30,30)
    C = (s11+s22)/2
    R = math.sqrt(((s11-s22)/2)**2+s12**2)
    stmt = (f"Draw Mohr's circle for $\\sigma_{{11}}={s11}$, $\\sigma_{{22}}={s22}$, "
            f"$\\sigma_{{12}}={s12}$ MPa. State center and radius.")
    sol = (f"Center: $C = (\\sigma_{{11}}+\\sigma_{{22}})/2 = {C:.1f}$ MPa.\n\n"
           f"Radius: $R = \\sqrt{{((\\sigma_{{11}}-\\sigma_{{22}})/2)^2+\\sigma_{{12}}^2}} = {R:.2f}$ MPa.\n\n"
           f"$\\sigma_1 = C+R = {C+R:.2f}$ MPa, $\\sigma_2 = C-R = {C-R:.2f}$ MPa.")
    return Problem("Mohr's circle", stmt, sol)

GENERATORS = [gen_traction, gen_principal_2d, gen_strain_rate, gen_decomposition, gen_max_shear, gen_mohr]

def main():
    parser = argparse.ArgumentParser(description="Generate 6.1 Stress & Strain practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n",
             "# 6.1 Practice — Stress & Strain Tensors\n\n"]
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

#!/usr/bin/env python3
"""
6.2_continuity.py — Practice problem generator for Chapter 6.2
(Mass Conservation — The Continuity Equation).

Archetypes:
  1. Verify divergence-free condition for a given velocity field
  2. Find missing velocity component from continuity
  3. Converging duct velocity calculation
  4. Find streamfunction from velocity field
  5. Unsteady density from compressible continuity

Usage:
  python 6.2_continuity.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

x, y, z = sp.symbols('x y z')

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

def gen_verify_div(rng: random.Random) -> Problem:
    a,b = rng.randint(1,4), rng.randint(1,4)
    vx = a*x*y
    vy = -a*y**2/2 + b*x
    div_v = sp.diff(vx,x) + sp.diff(vy,y)
    stmt = (f"Verify whether $\\mathbf{{v}} = ({sp.latex(vx)},\\;{sp.latex(vy)})$ "
            f"satisfies the incompressible continuity equation $\\nabla\\cdot\\mathbf{{v}}=0$.")
    sol = (f"$\\partial v_x/\\partial x = {sp.latex(sp.diff(vx,x))}$\n\n"
           f"$\\partial v_y/\\partial y = {sp.latex(sp.diff(vy,y))}$\n\n"
           f"$\\nabla\\cdot\\mathbf{{v}} = {sp.latex(div_v)}$"
           + (" = 0. ✓ Incompressible." if div_v==0 else f" ≠ 0. NOT incompressible."))
    return Problem("Verify divergence-free", stmt, sol)

def gen_missing_component(rng: random.Random) -> Problem:
    a,b = rng.randint(1,5), rng.randint(1,5)
    vx = a*x**2 + b*x*y
    dvx_dx = sp.diff(vx, x)
    vy_expr = sp.integrate(-dvx_dx, y)
    stmt = (f"Given $v_x = {sp.latex(vx)}$ for a 2D incompressible flow, find $v_y(x,y)$ "
            f"assuming $v_y(x,0)=0$.")
    sol = (f"From $\\nabla\\cdot\\mathbf{{v}}=0$: $\\partial v_y/\\partial y = -\\partial v_x/\\partial x = {sp.latex(-dvx_dx)}$.\n\n"
           f"Integrate: $v_y = \\int ({sp.latex(-dvx_dx)})\\,dy = {sp.latex(vy_expr)} + f(x)$.\n\n"
           f"BC $v_y(x,0)=0$ gives $f(x)=0$. So $v_y = {sp.latex(vy_expr)}$.")
    return Problem("Find missing velocity component", stmt, sol)

def gen_duct(rng: random.Random) -> Problem:
    A1 = rng.choice([0.05, 0.1, 0.2, 0.5])
    A2 = round(A1 * rng.choice([0.25, 0.5, 0.1]), 4)
    v1 = rng.randint(1, 10)
    v2 = v1 * A1 / A2
    stmt = (f"Water flows steadily through a duct from area $A_1={A1}$ m² to $A_2={A2}$ m². "
            f"Inlet velocity is $v_1={v1}$ m/s. Find exit velocity.")
    sol = (f"Continuity: $v_1 A_1 = v_2 A_2$.\n\n"
           f"$v_2 = v_1 A_1/A_2 = {v1}\\times{A1}/{A2} = {v2:.2f}$ m/s.")
    return Problem("Converging duct", stmt, sol)

def gen_streamfunction(rng: random.Random) -> Problem:
    a = rng.randint(1,4)
    vx_expr = a*y
    vy_expr = -a*x
    psi = sp.integrate(vx_expr, y)
    f_x = sp.integrate(vy_expr + sp.diff(psi, x), x)
    stmt = (f"Find the streamfunction $\\psi(x,y)$ for $\\mathbf{{v}}=({sp.latex(vx_expr)},\\;{sp.latex(vy_expr)})$.")
    sol = (f"From $v_x = \\partial\\psi/\\partial y = {sp.latex(vx_expr)}$: "
           f"$\\psi = \\int {sp.latex(vx_expr)}\\,dy = {sp.latex(psi)} + f(x)$.\n\n"
           f"From $v_y = -\\partial\\psi/\\partial x$: $-f'(x) = {sp.latex(vy_expr)}$ → $f(x) = {sp.latex(a*x**2/2)}$.\n\n"
           f"$\\psi = {sp.latex(psi + a*x**2/2)} + C = \\frac{{{a}}}{{2}}(x^2+y^2)+C$.")
    return Problem("Find streamfunction", stmt, sol)

def gen_unsteady_density(rng: random.Random) -> Problem:
    alpha = rng.randint(1,5)
    stmt = (f"A 1D flow has $v_x = {alpha}x$. If density is initially uniform $\\rho_0$, "
            f"find $\\rho(t)$ following a fluid particle.")
    sol = (f"$D\\rho/Dt + \\rho\\nabla\\cdot\\mathbf{{v}} = 0$.\n\n"
           f"$\\nabla\\cdot\\mathbf{{v}} = {alpha}$.\n\n"
           f"$D\\rho/Dt = -{alpha}\\rho$ → $\\rho(t) = \\rho_0 e^{{-{alpha}t}}$.")
    return Problem("Unsteady density (compressible)", stmt, sol)

GENERATORS = [gen_verify_div, gen_missing_component, gen_duct, gen_streamfunction, gen_unsteady_density]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.2 Practice — Continuity Equation\n\n"]
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

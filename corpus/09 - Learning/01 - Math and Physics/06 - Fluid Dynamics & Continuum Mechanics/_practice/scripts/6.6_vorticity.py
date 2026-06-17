#!/usr/bin/env python3
"""
6.6_vorticity.py — Practice problem generator for Chapter 6.6
(Vorticity & Potential Flow).

Archetypes:
  1. Compute vorticity from velocity field
  2. Verify irrotationality and find velocity potential
  3. Complex potential — velocity on cylinder surface
  4. Kutta-Joukowski lift calculation
  5. Rankine half-body stagnation point
  6. Circulation from vortex strength

Usage:
  python 6.6_vorticity.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

x, y = sp.symbols('x y')

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

def gen_vorticity(rng: random.Random) -> Problem:
    a, b, c = rng.randint(1,5), rng.randint(1,5), rng.randint(1,5)
    vx = a*x**2 - b*y
    vy = c*x*y
    omega_z = sp.diff(vy, x) - sp.diff(vx, y)
    stmt = (f"Compute the vorticity $\\omega_z$ for $\\mathbf{{v}} = ({sp.latex(vx)},\\;{sp.latex(vy)})$. "
            f"Is the flow irrotational?")
    irr = "Yes, irrotational." if omega_z == 0 else "No, rotational."
    sol = (f"$\\omega_z = \\partial v_y/\\partial x - \\partial v_x/\\partial y = "
           f"{sp.latex(sp.diff(vy,x))} - ({sp.latex(sp.diff(vx,y))}) = {sp.latex(omega_z)}$.\n\n{irr}")
    return Problem("Compute vorticity", stmt, sol)

def gen_potential(rng: random.Random) -> Problem:
    a = rng.randint(1,4)
    vx_e = a*(x**2 - y**2)
    vy_e = 2*a*x*y
    omega = sp.diff(vy_e, x) - sp.diff(vx_e, y)
    phi = sp.integrate(vx_e, x)
    stmt = (f"For $\\mathbf{{v}} = ({sp.latex(vx_e)},\\;{sp.latex(vy_e)})$, verify irrotationality "
            f"and find the velocity potential $\\phi$.")
    sol = (f"$\\omega_z = {sp.latex(sp.diff(vy_e,x))} - ({sp.latex(sp.diff(vx_e,y))}) = {sp.latex(omega)}$. "
           f"{'Irrotational ✓' if omega==0 else 'Rotational ✗'}\n\n"
           f"$\\phi = \\int v_x\\,dx = {sp.latex(phi)} + f(y)$.\n\n"
           f"From $\\partial\\phi/\\partial y = v_y$: determine $f(y)$.")
    return Problem("Velocity potential", stmt, sol)

def gen_cylinder_speed(rng: random.Random) -> Problem:
    U = rng.randint(5, 30)
    a = rng.choice([0.5, 1.0, 2.0])
    theta = rng.choice([30, 45, 60, 90])
    speed = 2 * U * abs(math.sin(math.radians(theta)))
    stmt = (f"Potential flow past a cylinder (radius $a={a}$ m, $U_\\infty={U}$ m/s). "
            f"Find the surface speed at $\\theta={theta}°$.")
    sol = (f"$|v| = 2U_\\infty|\\sin\\theta| = 2({U})|\\sin{theta}°| = "
           f"2({U})({abs(math.sin(math.radians(theta))):.4f}) = {speed:.2f}$ m/s.")
    return Problem("Cylinder surface speed", stmt, sol)

def gen_kj_lift(rng: random.Random) -> Problem:
    rho = rng.choice([1.225, 1.0])
    U = rng.randint(20, 100)
    Gamma = rng.randint(5, 50)
    L = rho * U * Gamma
    stmt = (f"Compute lift per unit span (Kutta-Joukowski) for $\\rho={rho}$ kg/m³, "
            f"$U_\\infty={U}$ m/s, $\\Gamma={Gamma}$ m²/s.")
    sol = f"$L' = \\rho U_\\infty \\Gamma = {rho}\\times{U}\\times{Gamma} = {L:.2f}$ N/m."
    return Problem("Kutta-Joukowski lift", stmt, sol)

def gen_rankine(rng: random.Random) -> Problem:
    m = rng.randint(1, 10)
    U = rng.randint(1, 10)
    x_stag = -m / (2 * math.pi * U)
    half_width = m / (2 * U)
    stmt = (f"Source strength $m={m}$ m²/s in uniform flow $U={U}$ m/s. "
            f"Find stagnation point and asymptotic half-body width.")
    sol = (f"Stagnation: $x_s = -m/(2\\pi U) = -{m}/(2\\pi\\times{U}) = {x_stag:.4f}$ m.\n\n"
           f"Half-width: $m/(2U) = {m}/(2\\times{U}) = {half_width:.4f}$ m.")
    return Problem("Rankine half-body", stmt, sol)

def gen_circulation(rng: random.Random) -> Problem:
    Gamma = rng.randint(1, 20)
    r = rng.choice([0.5, 1.0, 2.0, 5.0])
    v_theta = Gamma / (2 * math.pi * r)
    stmt = (f"A point vortex has $\\Gamma={Gamma}$ m²/s. Find $v_\\theta$ at $r={r}$ m "
            f"and verify $\\oint \\mathbf{{v}}\\cdot d\\mathbf{{r}} = \\Gamma$.")
    sol = (f"$v_\\theta = \\Gamma/(2\\pi r) = {Gamma}/(2\\pi\\times{r}) = {v_theta:.4f}$ m/s.\n\n"
           f"$\\oint v_\\theta\\,r\\,d\\theta = v_\\theta \\cdot 2\\pi r = {v_theta:.4f}\\times{2*math.pi*r:.4f} = {Gamma:.2f}$ m²/s = $\\Gamma$. ✓")
    return Problem("Circulation", stmt, sol)

GENERATORS = [gen_vorticity, gen_potential, gen_cylinder_speed, gen_kj_lift, gen_rankine, gen_circulation]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.6 Practice — Vorticity & Potential Flow\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

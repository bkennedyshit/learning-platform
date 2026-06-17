#!/usr/bin/env python3
"""
6.4_navier_stokes.py — Practice problem generator for Chapter 6.4
(Viscous Fluids — The Navier-Stokes Equations).

Archetypes:
  1. Reynolds number computation
  2. Couette flow velocity profile
  3. Poiseuille flow (plane) — flow rate and max velocity
  4. Hagen-Poiseuille (pipe) — Q and wall shear
  5. Stokes first problem (diffusion scaling)
  6. Dimensional analysis of N-S terms

Usage:
  python 6.4_navier_stokes.py --count 12 --seed 42
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

def gen_reynolds(rng: random.Random) -> Problem:
    rho = rng.choice([1.225, 1000, 900, 800])
    mu = rng.choice([1.8e-5, 1e-3, 0.1, 0.5])
    U = rng.randint(1, 50)
    L = rng.choice([0.01, 0.05, 0.1, 1.0, 10.0])
    Re = rho * U * L / mu
    regime = "laminar" if Re < 2300 else "transitional" if Re < 4000 else "turbulent"
    stmt = (f"Compute Re for $\\rho={rho}$ kg/m³, $\\mu={mu}$ Pa·s, $U={U}$ m/s, $L={L}$ m. "
            f"State the flow regime.")
    sol = (f"$\\text{{Re}} = \\rho UL/\\mu = {rho}\\times{U}\\times{L}/{mu} = {Re:.0f}$.\n\n"
           f"Flow regime: **{regime}**.")
    return Problem("Reynolds number", stmt, sol)

def gen_couette(rng: random.Random) -> Problem:
    U = rng.randint(1, 20)
    h = rng.choice([0.001, 0.005, 0.01, 0.05])
    mu = rng.choice([0.001, 0.01, 0.1, 1.0])
    tau = mu * U / h
    stmt = (f"Plane Couette flow: top plate moves at $U={U}$ m/s, gap $h={h}$ m, $\\mu={mu}$ Pa·s. "
            f"Find velocity at $y=h/4$ and wall shear stress.")
    sol = (f"$u(y) = Uy/h$. At $y=h/4$: $u = {U}/4 = {U/4:.2f}$ m/s.\n\n"
           f"$\\tau = \\mu U/h = {mu}\\times{U}/{h} = {tau:.2f}$ Pa.")
    return Problem("Couette flow", stmt, sol)

def gen_poiseuille_plane(rng: random.Random) -> Problem:
    G = rng.randint(100, 10000)
    h = rng.choice([0.005, 0.01, 0.02, 0.05])
    mu = rng.choice([0.001, 0.01, 0.1])
    u_max = G * h**2 / (8 * mu)
    Q = G * h**3 / (12 * mu)
    stmt = (f"Plane Poiseuille flow: $G=-dp/dx={G}$ Pa/m, gap $h={h}$ m, $\\mu={mu}$ Pa·s. "
            f"Find $u_{{\\max}}$ and volume flow rate per unit width $Q/b$.")
    sol = (f"$u_{{\\max}} = Gh^2/(8\\mu) = {G}\\times{h}^2/(8\\times{mu}) = {u_max:.4f}$ m/s.\n\n"
           f"$Q/b = Gh^3/(12\\mu) = {G}\\times{h}^3/(12\\times{mu}) = {Q:.6f}$ m²/s.")
    return Problem("Plane Poiseuille flow", stmt, sol)

def gen_pipe_flow(rng: random.Random) -> Problem:
    R = rng.choice([0.01, 0.025, 0.05, 0.1])
    G = rng.randint(100, 50000)
    mu = rng.choice([0.001, 0.01, 0.1, 0.5])
    Q = math.pi * G * R**4 / (8 * mu)
    tau_w = G * R / 2
    v_max = G * R**2 / (4 * mu)
    stmt = (f"Hagen-Poiseuille: pipe radius $R={R}$ m, $G={G}$ Pa/m, $\\mu={mu}$ Pa·s. "
            f"Find $Q$, $v_{{\\max}}$, and wall shear $\\tau_w$.")
    sol = (f"$Q = \\pi GR^4/(8\\mu) = {Q:.6f}$ m³/s.\n\n"
           f"$v_{{\\max}} = GR^2/(4\\mu) = {v_max:.4f}$ m/s.\n\n"
           f"$\\tau_w = GR/2 = {tau_w:.2f}$ Pa.")
    return Problem("Hagen-Poiseuille pipe flow", stmt, sol)

def gen_stokes_diffusion(rng: random.Random) -> Problem:
    nu = rng.choice([1e-6, 1.5e-5, 1e-4])
    t = rng.choice([1, 10, 60, 600])
    delta = math.sqrt(nu * t)
    stmt = (f"A plate is suddenly set in motion. With $\\nu={nu}$ m²/s, estimate the "
            f"momentum penetration depth after $t={t}$ s.")
    sol = (f"$\\delta \\sim \\sqrt{{\\nu t}} = \\sqrt{{{nu}\\times{t}}} = {delta:.5f}$ m "
           f"= {delta*1000:.2f} mm.")
    return Problem("Stokes diffusion scaling", stmt, sol)

def gen_ns_terms(rng: random.Random) -> Problem:
    U, L = rng.randint(1,50), rng.choice([0.01, 0.1, 1.0])
    rho = rng.choice([1.225, 1000])
    mu = rng.choice([1.8e-5, 1e-3])
    inertial = rho * U**2 / L
    viscous = mu * U / L**2
    Re = inertial / viscous
    stmt = (f"Estimate inertial and viscous force scales for $U={U}$ m/s, $L={L}$ m, "
            f"$\\rho={rho}$ kg/m³, $\\mu={mu}$ Pa·s. Compute Re.")
    sol = (f"Inertial: $\\rho U^2/L = {inertial:.2f}$ N/m³.\n\n"
           f"Viscous: $\\mu U/L^2 = {viscous:.4f}$ N/m³.\n\n"
           f"$\\text{{Re}} = {inertial:.2f}/{viscous:.4f} = {Re:.0f}$.")
    return Problem("N-S term scaling", stmt, sol)

GENERATORS = [gen_reynolds, gen_couette, gen_poiseuille_plane, gen_pipe_flow, gen_stokes_diffusion, gen_ns_terms]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/math]\n---\n", "# 6.4 Practice — Navier-Stokes Equations\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.6_gauge.py — Practice problem generator for Chapter 7.6
(Potential Formulations & Gauge Transformations).

Archetypes:
  1. Verify gauge transformation leaves fields unchanged
  2. Check Lorenz gauge condition
  3. Compute E and B from given potentials
  4. Retarded time calculation

Usage: python 7.6_gauge.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import symbols, diff, latex, cos, sin, exp, simplify, Function

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

x, y, z, t, c = symbols('x y z t c', real=True)

def gen_gauge_verify(rng: random.Random) -> Problem:
    lambdas = [x*t, x**2 - c**2*t**2, sin(x)*cos(c*t)]
    lam = rng.choice(lambdas)
    stmt = (f"Given gauge function $\\lambda = {latex(lam)}$, write the gauge-transformed "
            "potentials $\\phi'$ and $\\mathbf{{A}}'$ starting from $\\phi = 0$, $\\mathbf{{A}} = 0$. "
            "Verify $\\mathbf{{E}}' = \\mathbf{{E}} = 0$.")
    phi_new = -diff(lam, t)
    Ax_new = diff(lam, x)
    E_check = -diff(phi_new, x) - diff(Ax_new, t)
    sol = (f"$\\phi' = -\\partial\\lambda/\\partial t = {latex(-diff(lam, t))}$\n\n"
           f"$A'_x = \\partial\\lambda/\\partial x = {latex(diff(lam, x))}$\n\n"
           f"$E'_x = -\\partial\\phi'/\\partial x - \\partial A'_x/\\partial t = {latex(simplify(E_check))}$ ✓")
    return Problem("Gauge transformation verification", stmt, sol)

def gen_lorenz_check(rng: random.Random) -> Problem:
    k = rng.randint(1, 5)
    omega = k  # dispersion relation omega = kc
    phi = cos(k*x - omega*c*t)
    Ax = cos(k*x - omega*c*t) / c
    div_A = diff(Ax, x)
    dphi_dt = diff(phi, t) / c**2
    lorenz = simplify(div_A + dphi_dt)
    stmt = (f"Check whether $\\phi = \\cos({k}x - {omega}ct)$ and $A_x = \\cos({k}x - {omega}ct)/c$ "
            "satisfy the Lorenz gauge condition $\\nabla\\cdot\\mathbf{{A}} + (1/c^2)\\partial\\phi/\\partial t = 0$.")
    sol = (f"$\\nabla\\cdot\\mathbf{{A}} = \\partial A_x/\\partial x = {latex(div_A)}$\n\n"
           f"$(1/c^2)\\partial\\phi/\\partial t = {latex(dphi_dt)}$\n\n"
           f"Sum $= {latex(lorenz)}$\n\n"
           + ("Lorenz condition **satisfied**. ✓" if lorenz == 0 else "Lorenz condition **not satisfied**. ✗"))
    return Problem("Lorenz gauge condition check", stmt, sol)

def gen_fields_from_potentials(rng: random.Random) -> Problem:
    E0 = rng.randint(1, 5)
    choices = [
        (0, -E0*t*x, f"$\\phi = 0$, $A_x = {-E0}t$", f"E_x = {E0}", "B = 0"),
        (-E0*x, sp.Integer(0), f"$\\phi = {-E0}x$, $\\mathbf{{A}} = 0$", f"E_x = {E0}", "B = 0"),
    ]
    phi_val, A_val, desc, E_ans, B_ans = rng.choice(choices)
    stmt = f"Given {desc}, compute $\\mathbf{{E}}$ and $\\mathbf{{B}}$."
    sol = (f"$\\mathbf{{E}} = -\\nabla\\phi - \\partial\\mathbf{{A}}/\\partial t$\n\n"
           f"Result: ${E_ans}$ V/m, ${B_ans}$.")
    return Problem("Fields from potentials", stmt, sol)

def gen_retarded_time(rng: random.Random) -> Problem:
    r = rng.randint(1, 10) * 100  # meters
    t_obs = rng.randint(1, 10)  # microseconds
    t_r = t_obs - r / 3e8 * 1e6  # in microseconds
    stmt = (f"An observer at distance $r = {r}$ m detects a signal at $t = {t_obs}$ μs. "
            "What is the retarded time $t_r$?")
    sol = (f"$$t_r = t - r/c = {t_obs}\\text{{ μs}} - \\frac{{{r}}}{{3\\times10^8}}\\text{{ s}}$$\n\n"
           f"$$= {t_obs}\\text{{ μs}} - {r/3e8*1e6:.4f}\\text{{ μs}} = {t_r:.4f}\\text{{ μs}}$$")
    return Problem("Retarded time calculation", stmt, sol)

GENERATORS = [gen_gauge_verify, gen_lorenz_check, gen_fields_from_potentials, gen_retarded_time]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, gauge-theory, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.6 Gauge Transformations — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

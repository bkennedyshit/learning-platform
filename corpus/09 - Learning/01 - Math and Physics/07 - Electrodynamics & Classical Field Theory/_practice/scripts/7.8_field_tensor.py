#!/usr/bin/env python3
"""
7.8_field_tensor.py — Practice problem generator for Chapter 7.8
(The Electromagnetic Field Tensor & Gauge Fields).

Archetypes:
  1. Construct F^μν from given E and B
  2. Compute F_μν F^μν invariant
  3. Verify Bianchi identity for given fields
  4. Stress-energy tensor components

Usage: python 7.8_field_tensor.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import Matrix, Rational, latex, symbols, simplify

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

c = sp.Symbol('c', positive=True)

def gen_construct_tensor(rng: random.Random) -> Problem:
    Ex = rng.randint(-5, 5) * 100
    Ey = rng.randint(-5, 5) * 100
    Ez = rng.randint(-5, 5) * 100
    Bx = Rational(rng.randint(-3, 3), 1000)
    By = Rational(rng.randint(-3, 3), 1000)
    Bz = Rational(rng.randint(-3, 3), 1000)
    F = Matrix([
        [0, -Ex, -Ey, -Ez],
        [Ex, 0, -Bz, By],
        [Ey, Bz, 0, -Bx],
        [Ez, -By, Bx, 0]
    ])
    stmt = (f"Given $\\mathbf{{E}} = ({Ex}, {Ey}, {Ez})$ V/m and "
            f"$\\mathbf{{B}} = ({latex(Bx)}, {latex(By)}, {latex(Bz)})$ T, "
            "write $F^{\\mu\\nu}$ (with $c=1$ units for display).")
    sol = f"$$F^{{\\mu\\nu}} = {latex(F)}$$\n\n(with $E_i/c$ in the $0i$ positions for SI units)"
    return Problem("Construct field tensor", stmt, sol)

def gen_scalar_invariant(rng: random.Random) -> Problem:
    Ex = rng.randint(1, 5) * 100
    By = Rational(rng.randint(1, 5), 1000)
    E2 = Ex**2
    B2 = By**2
    inv = -2 * (E2 - (3e8)**2 * float(By)**2)
    stmt = (f"For $E_x = {Ex}$ V/m, $B_y = {latex(By)}$ T (all others zero), "
            "compute $F_{{\\mu\\nu}}F^{{\\mu\\nu}}$.")
    sol = (f"$F_{{\\mu\\nu}}F^{{\\mu\\nu}} = -2(E^2 - c^2B^2)/c^2$\n\n"
           f"$E^2 = {Ex}^2 = {E2}$ (V/m)²\n\n"
           f"$c^2B^2 = (3\\times10^8)^2({latex(By)})^2 = {(3e8)**2 * float(By)**2:.2e}$ (V/m)²\n\n"
           f"$F_{{\\mu\\nu}}F^{{\\mu\\nu}} = {inv/((3e8)**2):.4e}$ (T²)")
    return Problem("Scalar invariant F²", stmt, sol)

def gen_energy_density(rng: random.Random) -> Problem:
    E = rng.randint(100, 1000)
    B = Rational(rng.randint(1, 5), 1000000)
    eps0 = sp.Float(8.854e-12)
    mu0 = sp.Float(4e-7 * float(sp.pi))
    u = 0.5 * (float(eps0) * E**2 + float(B)**2 / float(mu0))
    stmt = (f"Compute the electromagnetic energy density $T^{{00}}$ for "
            f"$|\\mathbf{{E}}| = {E}$ V/m and $|\\mathbf{{B}}| = {latex(B)}$ T.")
    sol = (f"$$u = T^{{00}} = \\frac{{1}}{{2}}\\left(\\varepsilon_0 E^2 + \\frac{{B^2}}{{\\mu_0}}\\right)$$\n\n"
           f"$$= \\frac{{1}}{{2}}\\left((8.854\\times10^{{-12}})({E})^2 + \\frac{{({latex(B)})^2}}{{4\\pi\\times10^{{-7}}}}\\right)$$\n\n"
           f"$$= {u:.6e} \\text{{ J/m}}^3$$")
    return Problem("Stress-energy tensor T⁰⁰", stmt, sol)

def gen_bianchi(rng: random.Random) -> Problem:
    stmt = ("State the Bianchi identity for the electromagnetic field tensor and explain "
            "which Maxwell equations it encodes.")
    sol = ("$$\\partial_\\alpha F_{\\beta\\gamma} + \\partial_\\beta F_{\\gamma\\alpha} + \\partial_\\gamma F_{\\alpha\\beta} = 0$$\n\n"
           "Equivalently: $\\partial_\\mu\\tilde{F}^{\\mu\\nu} = 0$.\n\n"
           "This encodes the **homogeneous** Maxwell equations:\n"
           "- $\\nu = 0$: $\\nabla\\cdot\\mathbf{B} = 0$ (no monopoles)\n"
           "- $\\nu = i$: $\\nabla\\times\\mathbf{E} + \\partial\\mathbf{B}/\\partial t = 0$ (Faraday's Law)\n\n"
           "It is an identity (automatically satisfied by $F_{\\mu\\nu} = \\partial_\\mu A_\\nu - \\partial_\\nu A_\\mu$).")
    return Problem("Bianchi identity", stmt, sol)

GENERATORS = [gen_construct_tensor, gen_scalar_invariant, gen_energy_density, gen_bianchi]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = (f"---\ntags: [practice, field-tensor, review/math]\ngenerated_seed: {seed}\n---\n\n"
              "# 7.8 Field Tensor — Practice Problems\n\n---\n\n")
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
9.4_spin.py — Practice problems for Chapter 9.4 (Angular Momentum, Spin & Fine Structure).

Archetypes:
  1. Eigenvalue equation for spin-1/2 along arbitrary axis
  2. Measurement probabilities for spin
  3. Addition of angular momenta (two spin-1/2)
  4. Commutator of angular momentum components
  5. Expectation value of S·n̂
  6. Fine structure energy splitting
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_spin_eigenvalue(rng: random.Random) -> Problem:
    axis = rng.choice(['x', 'y'])
    stmt = f"Find the eigenvalues and normalized eigenvectors of $\\hat{{S}}_{axis}$ for spin-1/2."
    if axis == 'x':
        sol = ("Eigenvalues: $\\pm\\hbar/2$.\n\n"
               "$\\vert+\\rangle_x = \\frac{1}{\\sqrt{2}}\\binom{1}{1}$, "
               "$\\vert-\\rangle_x = \\frac{1}{\\sqrt{2}}\\binom{1}{-1}$.")
    else:
        sol = ("Eigenvalues: $\\pm\\hbar/2$.\n\n"
               "$\\vert+\\rangle_y = \\frac{1}{\\sqrt{2}}\\binom{1}{i}$, "
               "$\\vert-\\rangle_y = \\frac{1}{\\sqrt{2}}\\binom{1}{-i}$.")
    return Problem("Spin eigenvalue problem", stmt, sol)

def gen_spin_probability(rng: random.Random) -> Problem:
    theta = rng.choice([30, 45, 60, 90, 120])
    stmt = (f"An electron is in $\\vert\\uparrow\\rangle_z$. What is the probability of measuring "
            f"spin-up along an axis tilted $\\theta = {theta}°$ from $z$?")
    prob = sp.cos(sp.rad(theta)/2)**2
    sol = f"$P(+) = \\cos^2(\\theta/2) = \\cos^2({theta}°/2) = {sp.latex(sp.simplify(prob))}$."
    return Problem("Spin measurement probability", stmt, sol)

def gen_addition(rng: random.Random) -> Problem:
    stmt = ("Two spin-1/2 particles are in state $\\vert\\uparrow\\downarrow\\rangle$. "
            "Express this in the $\\vert S, M\\rangle$ basis.")
    sol = ("$\\vert\\uparrow\\downarrow\\rangle = \\frac{1}{\\sqrt{2}}\\vert 1,0\\rangle + \\frac{1}{\\sqrt{2}}\\vert 0,0\\rangle$.\n\n"
           "Verify: $\\frac{1}{\\sqrt{2}}\\cdot\\frac{1}{\\sqrt{2}}(\\vert\\uparrow\\downarrow\\rangle + \\vert\\downarrow\\uparrow\\rangle) "
           "+ \\frac{1}{\\sqrt{2}}\\cdot\\frac{1}{\\sqrt{2}}(\\vert\\uparrow\\downarrow\\rangle - \\vert\\downarrow\\uparrow\\rangle) = \\vert\\uparrow\\downarrow\\rangle$. ✓")
    return Problem("Addition of angular momenta", stmt, sol)

def gen_am_commutator(rng: random.Random) -> Problem:
    stmt = "Compute $[\\hat{J}_+, \\hat{J}_-]$ using $\\hat{J}_\\pm = \\hat{J}_x \\pm i\\hat{J}_y$."
    sol = ("$[\\hat{J}_+, \\hat{J}_-] = [\\hat{J}_x+i\\hat{J}_y, \\hat{J}_x-i\\hat{J}_y]$\n\n"
           "$= [\\hat{J}_x,\\hat{J}_x] - i[\\hat{J}_x,\\hat{J}_y] + i[\\hat{J}_y,\\hat{J}_x] + [\\hat{J}_y,\\hat{J}_y]$\n\n"
           "$= 0 - i(i\\hbar\\hat{J}_z) + i(-i\\hbar\\hat{J}_z) + 0 = \\hbar\\hat{J}_z + \\hbar\\hat{J}_z = 2\\hbar\\hat{J}_z$.")
    return Problem("Angular momentum commutator", stmt, sol)

def gen_spin_expectation(rng: random.Random) -> Problem:
    stmt = ("For $\\vert\\psi\\rangle = \\cos(\\pi/8)\\vert\\uparrow\\rangle + \\sin(\\pi/8)\\vert\\downarrow\\rangle$, "
            "compute $\\langle S_x\\rangle$.")
    sol = ("Using $\\langle S_x\\rangle = (\\hbar/2)\\sin\\theta\\cos\\phi$ with $\\theta = \\pi/4$, $\\phi = 0$:\n\n"
           "$\\langle S_x\\rangle = \\frac{\\hbar}{2}\\sin(\\pi/4) = \\frac{\\hbar}{2\\sqrt{2}}$.")
    return Problem("Spin expectation value", stmt, sol)

def gen_fine_structure(rng: random.Random) -> Problem:
    n = rng.choice([2, 3])
    stmt = f"How many distinct fine-structure energy levels exist for hydrogen $n = {n}$?"
    levels = n  # fine structure levels = n (j = 1/2, 3/2, ..., n-1/2)
    sol = (f"For $n = {n}$: $\\ell = 0, 1, ..., {n-1}$. Possible $j$ values: $1/2, 3/2, ..., {n}-1/2$.\n\n"
           f"There are ${n}$ distinct fine-structure levels (degenerate in $j$ only).")
    return Problem("Fine structure level counting", stmt, sol)

GENERATORS = [gen_spin_eigenvalue, gen_spin_probability, gen_addition,
              gen_am_commutator, gen_spin_expectation, gen_fine_structure]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.4 Practice — Angular Momentum, Spin & Fine Structure\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

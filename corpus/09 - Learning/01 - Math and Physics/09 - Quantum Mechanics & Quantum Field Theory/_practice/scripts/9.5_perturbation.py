#!/usr/bin/env python3
"""
9.5_perturbation.py — Practice problems for Chapter 9.5 (Perturbation Theory).

Archetypes:
  1. First-order energy correction E_n^(1)
  2. Second-order energy correction E_n^(2)
  3. First-order state correction |n^(1)⟩
  4. Degenerate perturbation theory (diagonalize W)
  5. Variational bound on ground state energy
  6. Anharmonic oscillator correction
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

def gen_first_order_energy(rng: random.Random) -> Problem:
    n = rng.randint(1, 3)
    stmt = (f"For the infinite well with perturbation $H' = V_0$ (constant) inside the well, "
            f"compute $E_{n}^{{(1)}}$.")
    sol = (f"$E_{n}^{{(1)}} = \\langle\\psi_{n}\\vert H'\\vert\\psi_{n}\\rangle = V_0\\int_0^L|\\psi_{n}|^2 dx = V_0$.\n\n"
           "A constant perturbation shifts all levels equally.")
    return Problem("First-order energy correction", stmt, sol)

def gen_second_order(rng: random.Random) -> Problem:
    stmt = ("For the oscillator ground state with $H' = \\lambda x^3$, show $E_0^{(1)} = 0$ "
            "and find which states contribute to $E_0^{(2)}$.")
    sol = ("$E_0^{(1)} = \\lambda\\langle 0\\vert x^3\\vert 0\\rangle = 0$ (odd function, parity).\n\n"
           "$x^3 \\propto (a+a^\\dagger)^3$: connects $\\vert 0\\rangle$ to $\\vert 1\\rangle$ and $\\vert 3\\rangle$.\n\n"
           "$E_0^{(2)} = \\frac{|\\langle 1|H'|0\\rangle|^2}{E_0-E_1} + \\frac{|\\langle 3|H'|0\\rangle|^2}{E_0-E_3}$.")
    return Problem("Second-order energy correction", stmt, sol)

def gen_state_correction(rng: random.Random) -> Problem:
    stmt = ("For the well with $H' = V_0\\sin(\\pi x/L)$, find the first-order correction to $\\vert\\psi_2\\rangle$.")
    sol = ("$\\vert 2^{(1)}\\rangle = \\sum_{m\\neq 2}\\frac{\\langle m|H'|2\\rangle}{E_2-E_m}\\vert m\\rangle$.\n\n"
           "Need $\\langle m|H'|2\\rangle = \\frac{2V_0}{L}\\int_0^L\\sin(m\\pi x/L)\\sin(\\pi x/L)\\sin(2\\pi x/L)dx$.\n\n"
           "By selection rules (product-to-sum), only $m = 1$ and $m = 3$ contribute.")
    return Problem("First-order state correction", stmt, sol)

def gen_degenerate(rng: random.Random) -> Problem:
    stmt = ("Two degenerate states $\\vert a\\rangle$, $\\vert b\\rangle$ have $W = \\begin{pmatrix}0&\\Delta\\\\\\Delta&0\\end{pmatrix}$. "
            "Find the first-order corrections and good zeroth-order states.")
    sol = ("Eigenvalues of $W$: $E^{(1)} = \\pm\\Delta$.\n\n"
           "Eigenvectors: $\\frac{1}{\\sqrt{2}}(\\vert a\\rangle \\pm \\vert b\\rangle)$.\n\n"
           "The degeneracy is lifted; the splitting is $2\\Delta$.")
    return Problem("Degenerate perturbation theory", stmt, sol)

def gen_variational(rng: random.Random) -> Problem:
    stmt = ("Use trial function $\\psi(x) = A(a^2-x^2)$ for $|x|<a$ to estimate the ground-state "
            "energy of the harmonic oscillator. Minimize over $a$.")
    sol = ("Normalize: $A^2\\int_{-a}^a(a^2-x^2)^2dx = A^2\\cdot\\frac{16a^5}{15} = 1$.\n\n"
           "$\\langle T\\rangle = \\frac{\\hbar^2}{2m}\\cdot\\frac{5}{2a^2}$, "
           "$\\langle V\\rangle = \\frac{m\\omega^2}{2}\\cdot\\frac{a^2}{7}$.\n\n"
           "Minimize $E(a) = \\frac{5\\hbar^2}{4ma^2} + \\frac{m\\omega^2 a^2}{14}$: "
           "gives $E_{\\min} = \\frac{\\hbar\\omega}{2}\\sqrt{\\frac{10}{7}} \\approx 0.598\\hbar\\omega > 0.5\\hbar\\omega$. ✓")
    return Problem("Variational estimate", stmt, sol)

def gen_anharmonic(rng: random.Random) -> Problem:
    stmt = "Compute $E_1^{(1)}$ for the oscillator with $H' = \\lambda x^4$."
    sol = ("$E_1^{(1)} = \\lambda\\langle 1|x^4|1\\rangle = \\lambda(\\hbar/2m\\omega)^2\\langle 1|(a+a^\\dagger)^4|1\\rangle$.\n\n"
           "$\\langle 1|(a+a^\\dagger)^4|1\\rangle = 6(1)^2 + 6(1) + 3 = 15$.\n\n"
           "$E_1^{(1)} = \\frac{15\\lambda\\hbar^2}{4m^2\\omega^2}$.")
    return Problem("Anharmonic oscillator", stmt, sol)

GENERATORS = [gen_first_order_energy, gen_second_order, gen_state_correction,
              gen_degenerate, gen_variational, gen_anharmonic]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.5 Practice — Perturbation Theory\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

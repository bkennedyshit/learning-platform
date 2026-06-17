#!/usr/bin/env python3
"""
9.3_well_oscillator.py — Practice problems for Chapter 9.3
(Infinite Square Well & Harmonic Oscillator).

Archetypes:
  1. Compute energy of nth state (well)
  2. Transition matrix element ⟨m|x|n⟩ (oscillator)
  3. Expectation values ⟨x⟩, ⟨x²⟩ in well
  4. Uncertainty product ΔxΔp for oscillator state |n⟩
  5. Construct |n⟩ from ladder operators
  6. Expansion coefficients for initial state

Usage: python 9.3_well_oscillator.py --count 12 --seed 42
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

def gen_well_energy(rng: random.Random) -> Problem:
    n = rng.randint(1, 6)
    stmt = f"Compute $E_{n}$ for the infinite square well of width $L$. Express in terms of $E_1$."
    sol = (f"$E_n = \\frac{{n^2\\pi^2\\hbar^2}}{{2mL^2}}$.\n\n"
           f"$E_{n} = {n**2}E_1$ where $E_1 = \\pi^2\\hbar^2/(2mL^2)$.")
    return Problem("Well energy level", stmt, sol)

def gen_matrix_element(rng: random.Random) -> Problem:
    m_val = rng.randint(0, 4)
    n_val = m_val + rng.choice([-1, 1]) if m_val > 0 else 1
    if abs(m_val - n_val) == 1:
        coeff = sp.sqrt(max(m_val, n_val))
        result = f"$\\sqrt{{\\hbar/(2m\\omega)}} \\cdot \\sqrt{{{max(m_val,n_val)}}}$"
    else:
        result = "$0$ (selection rule: $\\Delta n = \\pm 1$ only)"
    stmt = f"Compute $\\langle {m_val}\\vert\\hat{{x}}\\vert {n_val}\\rangle$ for the harmonic oscillator."
    sol = (f"$\\hat{{x}} = \\sqrt{{\\hbar/(2m\\omega)}}(\\hat{{a}} + \\hat{{a}}^\\dagger)$.\n\n"
           f"$\\langle {m_val}\\vert\\hat{{x}}\\vert {n_val}\\rangle = {result}$.")
    return Problem("Oscillator matrix element", stmt, sol)

def gen_well_expectation(rng: random.Random) -> Problem:
    n = rng.randint(1, 4)
    stmt = f"Compute $\\langle x^2\\rangle$ for $\\psi_{n}(x)$ in the infinite well of width $L$."
    sol = (f"$\\langle x^2\\rangle = L^2\\left(\\frac{{1}}{{3}} - \\frac{{1}}{{2\\cdot{n}^2\\pi^2}}\\right) "
           f"= L^2\\left(\\frac{{1}}{{3}} - \\frac{{1}}{{{2*n**2}\\pi^2}}\\right)$.")
    return Problem("Well ⟨x²⟩", stmt, sol)

def gen_oscillator_uncertainty(rng: random.Random) -> Problem:
    n = rng.randint(0, 3)
    stmt = f"Compute $\\Delta x \\cdot \\Delta p$ for the oscillator state $\\vert {n}\\rangle$."
    sol = (f"$\\langle x^2\\rangle = \\frac{{\\hbar}}{{2m\\omega}}(2{n}+1)$, "
           f"$\\langle p^2\\rangle = \\frac{{m\\omega\\hbar}}{{2}}(2{n}+1)$.\n\n"
           f"$\\Delta x\\Delta p = \\frac{{\\hbar}}{{2}}(2{n}+1) = \\frac{{{2*n+1}\\hbar}}{{2}}$.\n\n"
           f"This exceeds $\\hbar/2$ for $n > 0$. Only $n=0$ saturates the bound.")
    return Problem("Oscillator uncertainty product", stmt, sol)

def gen_ladder_construct(rng: random.Random) -> Problem:
    n = rng.randint(2, 4)
    factorial = sp.factorial(n)
    stmt = f"Express $\\vert {n}\\rangle$ in terms of $\\hat{{a}}^\\dagger$ acting on $\\vert 0\\rangle$."
    sol = f"$\\vert {n}\\rangle = \\frac{{(\\hat{{a}}^\\dagger)^{n}}}{{\\sqrt{{{n}!}}}}\\vert 0\\rangle = \\frac{{(\\hat{{a}}^\\dagger)^{n}}}{{\\sqrt{{{factorial}}}}}\\vert 0\\rangle$."
    return Problem("Ladder operator construction", stmt, sol)

def gen_expansion(rng: random.Random) -> Problem:
    stmt = ("A particle in the well starts in $\\Psi(x,0) = \\sqrt{30/L^5}\\,x(L-x)$. "
            "Find $c_1 = \\langle\\psi_1\\vert\\Psi\\rangle$.")
    sol = ("$c_1 = \\sqrt{60/L^5}\\int_0^L x(L-x)\\sin(\\pi x/L)\\,dx$.\n\n"
           "Integration by parts (twice) gives $c_1 = \\frac{4\\sqrt{30}}{\\pi^3} \\approx 0.9986$.\n\n"
           "The state is $\\approx 99.7\\%$ in the ground state!")
    return Problem("Expansion coefficients", stmt, sol)

GENERATORS = [gen_well_energy, gen_matrix_element, gen_well_expectation,
              gen_oscillator_uncertainty, gen_ladder_construct, gen_expansion]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.3 Practice — Infinite Well & Harmonic Oscillator\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

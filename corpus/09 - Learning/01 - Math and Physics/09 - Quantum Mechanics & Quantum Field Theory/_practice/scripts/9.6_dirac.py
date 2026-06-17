#!/usr/bin/env python3
"""
9.6_dirac.py — Practice problems for Chapter 9.6 (Relativistic QM).

Archetypes:
  1. Verify Clifford algebra {γᵘ,γᵛ} = 2gᵘᵛ
  2. Solve free Dirac equation for given momentum
  3. Compute Dirac adjoint and bilinear ψ̄ψ
  4. Klein-Gordon from squaring Dirac
  5. Non-relativistic limit / Pauli equation
  6. Gamma matrix trace identities
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

def gen_clifford(rng: random.Random) -> Problem:
    mu, nu = rng.sample(range(4), 2)
    stmt = f"Verify $\\{{\\gamma^{mu}, \\gamma^{nu}\\}} = 2g^{{{mu}{nu}}}I_4$ in the Dirac representation."
    sol = (f"For $\\mu \\neq \\nu$: $g^{{{mu}{nu}}} = 0$, so need $\\gamma^{mu}\\gamma^{nu} + \\gamma^{nu}\\gamma^{mu} = 0$.\n\n"
           f"Direct matrix multiplication confirms the anticommutation. ✓")
    return Problem("Clifford algebra verification", stmt, sol)

def gen_dirac_solution(rng: random.Random) -> Problem:
    stmt = ("Find the positive-energy Dirac spinor $u^{(1)}(p)$ for an electron with "
            "$\\mathbf{p} = p\\hat{z}$ (momentum along z-axis).")
    sol = ("$u^{(1)} = \\sqrt{E+m}\\begin{pmatrix}1\\\\0\\\\p/(E+m)\\\\0\\end{pmatrix}$.\n\n"
           "Verify: $(\\gamma^\\mu p_\\mu - m)u = 0$ with $E = \\sqrt{p^2+m^2}$.")
    return Problem("Free Dirac spinor", stmt, sol)

def gen_dirac_adjoint(rng: random.Random) -> Problem:
    stmt = "Show that $\\bar{\\psi}\\psi = \\psi^\\dagger\\gamma^0\\psi$ is Lorentz invariant (scalar)."
    sol = ("Under Lorentz: $\\psi \\to S\\psi$ where $S^{-1}\\gamma^\\mu S = \\Lambda^\\mu_\\nu\\gamma^\\nu$.\n\n"
           "$\\bar{\\psi}\\psi \\to \\psi^\\dagger S^\\dagger\\gamma^0 S\\psi$.\n\n"
           "Using $S^\\dagger\\gamma^0 = \\gamma^0 S^{-1}$: $\\bar{\\psi}\\psi \\to \\psi^\\dagger\\gamma^0 S^{-1}S\\psi = \\bar{\\psi}\\psi$. ✓")
    return Problem("Dirac adjoint & Lorentz scalar", stmt, sol)

def gen_kg_from_dirac(rng: random.Random) -> Problem:
    stmt = "Starting from $(i\\gamma^\\mu\\partial_\\mu - m)\\psi = 0$, derive the Klein-Gordon equation."
    sol = ("Apply $(i\\gamma^\\nu\\partial_\\nu + m)$ from the left:\n\n"
           "$(-\\gamma^\\nu\\gamma^\\mu\\partial_\\nu\\partial_\\mu - m^2)\\psi = 0$.\n\n"
           "Symmetric part: $\\frac{1}{2}\\{\\gamma^\\nu,\\gamma^\\mu\\}\\partial_\\nu\\partial_\\mu = g^{\\nu\\mu}\\partial_\\nu\\partial_\\mu = \\Box$.\n\n"
           "Result: $(\\Box + m^2)\\psi = 0$. Each component satisfies Klein-Gordon. ✓")
    return Problem("Klein-Gordon from Dirac", stmt, sol)

def gen_pauli_limit(rng: random.Random) -> Problem:
    stmt = "In the non-relativistic limit of the Dirac equation, what is the electron's magnetic moment?"
    sol = ("The Pauli equation gives $H_{\\text{mag}} = -\\frac{e\\hbar}{2mc}\\vec{\\sigma}\\cdot\\mathbf{B}$.\n\n"
           "Magnetic moment: $\\vec{\\mu} = -g\\frac{e}{2mc}\\hat{\\mathbf{S}}$ with $g = 2$.\n\n"
           "This is the Dirac prediction. QED corrections give $g = 2.00232...$")
    return Problem("Non-relativistic limit", stmt, sol)

def gen_trace_identity(rng: random.Random) -> Problem:
    stmt = "Compute $\\text{Tr}(\\gamma^\\mu\\gamma^\\nu\\gamma^\\rho\\gamma^\\sigma)$."
    sol = ("$\\text{Tr}(\\gamma^\\mu\\gamma^\\nu\\gamma^\\rho\\gamma^\\sigma) = "
           "4(g^{\\mu\\nu}g^{\\rho\\sigma} - g^{\\mu\\rho}g^{\\nu\\sigma} + g^{\\mu\\sigma}g^{\\nu\\rho})$.\n\n"
           "This is the fundamental 4-gamma trace identity used in all QED calculations.")
    return Problem("Gamma matrix trace", stmt, sol)

GENERATORS = [gen_clifford, gen_dirac_solution, gen_dirac_adjoint,
              gen_kg_from_dirac, gen_pauli_limit, gen_trace_identity]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.6 Practice — Relativistic QM: Klein-Gordon & Dirac\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

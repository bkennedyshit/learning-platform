#!/usr/bin/env python3
"""
9.2_bra_ket.py — Practice problem generator for Chapter 9.2
(Hilbert Space & Bra-Ket Formalism).

Archetypes:
  1. Compute inner product ⟨φ|ψ⟩
  2. Normalize a ket and find measurement probabilities
  3. Compute expectation value ⟨ψ|A|ψ⟩ for matrix operator
  4. Verify Hermiticity of a matrix
  5. Compute trace of an outer product
  6. Change of basis (spin-1/2)

Usage:
  python 9.2_bra_ket.py --count 12 --seed 42
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
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_inner_product(rng: random.Random) -> Problem:
    a = [complex(rng.randint(-2,2), rng.randint(-2,2)) for _ in range(2)]
    b = [complex(rng.randint(-2,2), rng.randint(-2,2)) for _ in range(2)]
    ip = sum(x.conjugate()*y for x,y in zip(a,b))
    stmt = (f"Compute $\\langle\\phi\\vert\\psi\\rangle$ where "
            f"$\\vert\\phi\\rangle = {sp.latex(sp.Matrix([sp.nsimplify(x) for x in a]))}$ and "
            f"$\\vert\\psi\\rangle = {sp.latex(sp.Matrix([sp.nsimplify(x) for x in b]))}$.")
    sol = (f"$\\langle\\phi\\vert\\psi\\rangle = \\overline{{({sp.nsimplify(a[0])})}}({sp.nsimplify(b[0])}) + "
           f"\\overline{{({sp.nsimplify(a[1])})}}({sp.nsimplify(b[1])}) = {sp.nsimplify(ip)}$.")
    return Problem("Inner product computation", stmt, sol)

def gen_normalize_ket(rng: random.Random) -> Problem:
    c1, c2 = rng.randint(1,3), rng.randint(1,3)
    norm = sp.sqrt(c1**2 + c2**2)
    stmt = (f"Normalize $\\vert\\psi\\rangle = {c1}\\vert+\\rangle + {c2}\\vert-\\rangle$ and find "
            f"$P(+)$ and $P(-)$.")
    sol = (f"$\\|\\psi\\| = \\sqrt{{{c1**2}+{c2**2}}} = {sp.latex(norm)}$.\n\n"
           f"Normalized: $\\vert\\psi\\rangle_N = \\frac{{{c1}}}{{{sp.latex(norm)}}}\\vert+\\rangle + "
           f"\\frac{{{c2}}}{{{sp.latex(norm)}}}\\vert-\\rangle$.\n\n"
           f"$P(+) = {c1**2}/{c1**2+c2**2}$, $P(-) = {c2**2}/{c1**2+c2**2}$.")
    return Problem("Normalize ket & probabilities", stmt, sol)

def gen_expectation_matrix(rng: random.Random) -> Problem:
    entries = [rng.randint(-2,2) for _ in range(4)]
    A = sp.Matrix(2, 2, entries)
    if A != A.H:
        A = A + A.H  # make Hermitian
    psi = sp.Matrix([1, 0])
    exp_val = (psi.H * A * psi)[0,0]
    stmt = (f"Compute $\\langle+\\vert\\hat{{A}}\\vert+\\rangle$ for $A = {sp.latex(A)}$.")
    sol = f"$\\langle+\\vert A\\vert+\\rangle = A_{{11}} = {exp_val}$."
    return Problem("Matrix expectation value", stmt, sol)

def gen_hermiticity(rng: random.Random) -> Problem:
    a, b = rng.randint(-3,3), rng.randint(1,3)
    A = sp.Matrix([[a, b*sp.I], [-b*sp.I, a]])
    stmt = f"Is $A = {sp.latex(A)}$ Hermitian? Compute $A^\\dagger$ and compare."
    is_herm = (A == A.H)
    sol = (f"$A^\\dagger = {sp.latex(A.H)}$.\n\n"
           f"{'$A = A^\\dagger$ ✓ — Hermitian.' if is_herm else '$A \\neq A^\\dagger$ — NOT Hermitian.'}")
    return Problem("Verify Hermiticity", stmt, sol)

def gen_trace_outer(rng: random.Random) -> Problem:
    a1, a2 = rng.randint(-2,2), rng.randint(-2,2)
    b1, b2 = rng.randint(-2,2), rng.randint(-2,2)
    ip = a1*b1 + a2*b2
    stmt = (f"Compute $\\text{{Tr}}(\\vert\\alpha\\rangle\\langle\\beta\\vert)$ where "
            f"$\\vert\\alpha\\rangle = \\binom{{{a1}}}{{{a2}}}$, $\\vert\\beta\\rangle = \\binom{{{b1}}}{{{b2}}}$.")
    sol = f"$\\text{{Tr}}(\\vert\\alpha\\rangle\\langle\\beta\\vert) = \\langle\\beta\\vert\\alpha\\rangle = {ip}$."
    return Problem("Trace of outer product", stmt, sol)

def gen_change_basis(rng: random.Random) -> Problem:
    stmt = ("Express $\\vert+\\rangle_z$ in the $S_y$ eigenbasis. The $S_y$ eigenstates are "
            "$\\vert+\\rangle_y = \\frac{1}{\\sqrt{2}}\\binom{1}{i}$, "
            "$\\vert-\\rangle_y = \\frac{1}{\\sqrt{2}}\\binom{1}{-i}$.")
    sol = ("$\\vert+\\rangle_z = \\binom{1}{0} = c_+\\vert+\\rangle_y + c_-\\vert-\\rangle_y$.\n\n"
           "$c_+ = {}_y\\langle+\\vert+\\rangle_z = \\frac{1}{\\sqrt{2}}(1\\cdot1 + (-i)\\cdot0) = \\frac{1}{\\sqrt{2}}$.\n\n"
           "$c_- = {}_y\\langle-\\vert+\\rangle_z = \\frac{1}{\\sqrt{2}}(1\\cdot1 + i\\cdot0) = \\frac{1}{\\sqrt{2}}$.\n\n"
           "$\\vert+\\rangle_z = \\frac{1}{\\sqrt{2}}(\\vert+\\rangle_y + \\vert-\\rangle_y)$.")
    return Problem("Change of basis (spin-1/2)", stmt, sol)

GENERATORS = [gen_inner_product, gen_normalize_ket, gen_expectation_matrix,
              gen_hermiticity, gen_trace_outer, gen_change_basis]

def main():
    parser = argparse.ArgumentParser(description="QM Chapter 9.2 practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.2 Practice — Hilbert Space & Bra-Ket Formalism\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

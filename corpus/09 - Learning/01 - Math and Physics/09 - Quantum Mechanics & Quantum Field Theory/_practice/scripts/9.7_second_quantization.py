#!/usr/bin/env python3
"""
9.7_second_quantization.py — Practice problems for Chapter 9.7 (Second Quantization).

Archetypes:
  1. Commutation relations for creation/annihilation operators
  2. Fock state energy computation
  3. Normal ordering an operator expression
  4. Vacuum expectation value of field products
  5. Anticommutation relations for fermions
  6. Number operator eigenvalues
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_commutation(rng: random.Random) -> Problem:
    stmt = "Compute $[\\hat{a}_\\mathbf{k}, \\hat{a}^\\dagger_\\mathbf{k'}\\hat{a}_\\mathbf{k'}]$ for bosonic operators."
    sol = ("Using $[A, BC] = [A,B]C + B[A,C]$:\n\n"
           "$[\\hat{a}_k, \\hat{a}^\\dagger_{k'}\\hat{a}_{k'}] = [\\hat{a}_k, \\hat{a}^\\dagger_{k'}]\\hat{a}_{k'} + \\hat{a}^\\dagger_{k'}[\\hat{a}_k, \\hat{a}_{k'}]$\n\n"
           "$= (2\\pi)^3\\delta^{(3)}(k-k')\\hat{a}_{k'} + 0 = (2\\pi)^3\\delta^{(3)}(k-k')\\hat{a}_k$.")
    return Problem("Bosonic commutation relation", stmt, sol)

def gen_fock_energy(rng: random.Random) -> Problem:
    n1, n2 = rng.randint(1,3), rng.randint(1,3)
    stmt = (f"What is the energy of the Fock state with {n1} particles of momentum $k_1$ "
            f"and {n2} particles of momentum $k_2$?")
    sol = f"$E = {n1}\\omega_{{k_1}} + {n2}\\omega_{{k_2}} = {n1}\\sqrt{{k_1^2+m^2}} + {n2}\\sqrt{{k_2^2+m^2}}$."
    return Problem("Fock state energy", stmt, sol)

def gen_normal_order(rng: random.Random) -> Problem:
    stmt = "Normal-order $:\\hat{a}\\hat{a}^\\dagger\\hat{a}\\hat{a}^\\dagger:$ for a single mode."
    sol = ("Move all $\\hat{a}^\\dagger$ to the left, ignoring commutators:\n\n"
           "$:\\hat{a}\\hat{a}^\\dagger\\hat{a}\\hat{a}^\\dagger: = (\\hat{a}^\\dagger)^2\\hat{a}^2$.\n\n"
           "Verify: $\\hat{a}\\hat{a}^\\dagger = \\hat{a}^\\dagger\\hat{a} + 1 = \\hat{N}+1$, so "
           "$\\hat{a}\\hat{a}^\\dagger\\hat{a}\\hat{a}^\\dagger = (\\hat{N}+1)\\hat{a}\\hat{a}^\\dagger = (\\hat{N}+1)(\\hat{N}+1)$, "
           "while $:(\\hat{a}^\\dagger)^2\\hat{a}^2: = \\hat{N}(\\hat{N}-1)$.")
    return Problem("Normal ordering", stmt, sol)

def gen_vacuum_vev(rng: random.Random) -> Problem:
    stmt = "Compute $\\langle 0|\\hat{\\phi}(x)\\hat{\\phi}(y)|0\\rangle$ for the free scalar field (state the result)."
    sol = ("Only the $\\hat{a}_k\\hat{a}^\\dagger_{k'}$ term survives:\n\n"
           "$\\langle 0|\\hat{\\phi}(x)\\hat{\\phi}(y)|0\\rangle = \\int\\frac{d^3k}{(2\\pi)^3}\\frac{1}{2\\omega_k}e^{-ik\\cdot(x-y)}$.\n\n"
           "This is the positive-frequency Wightman function $D^+(x-y)$.")
    return Problem("Vacuum two-point function", stmt, sol)

def gen_anticommutation(rng: random.Random) -> Problem:
    stmt = "Show that $\\{\\hat{b}^\\dagger_k, \\hat{b}^\\dagger_k\\} = 0$ implies $(\\hat{b}^\\dagger_k)^2 = 0$ (Pauli exclusion)."
    sol = ("$\\{\\hat{b}^\\dagger_k, \\hat{b}^\\dagger_k\\} = 2(\\hat{b}^\\dagger_k)^2 = 0$.\n\n"
           "Therefore $(\\hat{b}^\\dagger_k)^2 = 0$: cannot create two fermions in the same state.\n\n"
           "This is the Pauli exclusion principle from the algebra alone!")
    return Problem("Fermionic anticommutation", stmt, sol)

def gen_number_op(rng: random.Random) -> Problem:
    n = rng.randint(1, 4)
    stmt = f"Verify $\\hat{{N}}|{n}\\rangle = {n}|{n}\\rangle$ where $|{n}\\rangle = (\\hat{{a}}^\\dagger)^{n}/\\sqrt{{{n}!}}|0\\rangle$."
    sol = (f"$\\hat{{N}}|{n}\\rangle = \\hat{{a}}^\\dagger\\hat{{a}}|{n}\\rangle$.\n\n"
           f"$\\hat{{a}}|{n}\\rangle = \\sqrt{{{n}}}|{n-1}\\rangle$, then "
           f"$\\hat{{a}}^\\dagger\\sqrt{{{n}}}|{n-1}\\rangle = \\sqrt{{{n}}}\\cdot\\sqrt{{{n}}}|{n}\\rangle = {n}|{n}\\rangle$. ✓")
    return Problem("Number operator eigenvalue", stmt, sol)

GENERATORS = [gen_commutation, gen_fock_energy, gen_normal_order,
              gen_vacuum_vev, gen_anticommutation, gen_number_op]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.7 Practice — Second Quantization & Quantum Fields\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

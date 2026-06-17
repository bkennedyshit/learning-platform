#!/usr/bin/env python3
"""
11.8_state_space.py — Practice problem generator for Chapter 11.8
(Modern Control - State-Space Representation).

Archetypes:
  1. State-space to transfer function
  2. Controllability check
  3. Observability check
  4. Pole placement via Ackermann
  5. Matrix exponential (2x2 diagonalizable)
  6. Observer gain design

Usage:
  python 11.8_state_space.py --count 10 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

s = sp.Symbol('s')

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_ss_to_tf(rng: random.Random) -> Problem:
    # 2x2 system with distinct eigenvalues
    a = -rng.randint(1, 5)
    b = -rng.randint(a+6, 10) if a > -5 else -rng.randint(6, 10)
    A = sp.Matrix([[a, 1], [0, b]])
    B = sp.Matrix([0, 1])
    C = sp.Matrix([[1, 0]])
    sI_A = s*sp.eye(2) - A
    G = sp.simplify(C * sI_A.inv() * B)
    G_scalar = G[0, 0]
    stmt = (f"Find $G(s) = C(sI-A)^{{-1}}B$ for $A = {sp.latex(A)}$, "
            f"$B = {sp.latex(B)}$, $C = {sp.latex(C)}$.")
    sol = (f"$sI - A = {sp.latex(sI_A)}$\n\n"
           f"$\\det(sI-A) = {sp.latex(sI_A.det())}$\n\n"
           f"$G(s) = {sp.latex(G_scalar)}$")
    return Problem("State-space → transfer function", stmt, sol)

def gen_controllability(rng: random.Random) -> Problem:
    a11 = -rng.randint(1, 5)
    a22 = -rng.randint(1, 5)
    a12 = rng.choice([0, 1, rng.randint(-3, 3)])
    b1 = rng.choice([0, 1])
    b2 = rng.randint(1, 3)
    A = sp.Matrix([[a11, a12], [0, a22]])
    B = sp.Matrix([b1, b2])
    AB = A * B
    C_mat = sp.Matrix([[B[0], AB[0]], [B[1], AB[1]]])
    det_C = C_mat.det()
    controllable = det_C != 0
    stmt = (f"Check controllability for $A = {sp.latex(A)}$, $B = {sp.latex(B)}$.")
    sol = (f"$\\mathcal{{C}} = [B \\; AB] = {sp.latex(C_mat)}$\n\n"
           f"$\\det(\\mathcal{{C}}) = {det_C}$ → **{'Controllable' if controllable else 'NOT controllable'}**")
    return Problem("Controllability check", stmt, sol)

def gen_observability(rng: random.Random) -> Problem:
    a11 = -rng.randint(1, 5)
    a22 = -rng.randint(1, 5)
    a21 = rng.choice([0, rng.randint(-3, 3)])
    c1 = rng.randint(1, 3)
    c2 = rng.choice([0, 1])
    A = sp.Matrix([[a11, 0], [a21, a22]])
    C = sp.Matrix([[c1, c2]])
    CA = C * A
    O_mat = sp.Matrix([[C[0, 0], C[0, 1]], [CA[0, 0], CA[0, 1]]])
    det_O = O_mat.det()
    observable = det_O != 0
    stmt = (f"Check observability for $A = {sp.latex(A)}$, $C = {sp.latex(C)}$.")
    sol = (f"$\\mathcal{{O}} = [C; CA]^T = {sp.latex(O_mat)}$\n\n"
           f"$\\det(\\mathcal{{O}}) = {det_O}$ → **{'Observable' if observable else 'NOT observable'}**")
    return Problem("Observability check", stmt, sol)

def gen_pole_placement(rng: random.Random) -> Problem:
    # Controllable canonical form for easy verification
    a0 = rng.randint(1, 6)
    a1 = rng.randint(1, 6)
    A = sp.Matrix([[0, 1], [-a0, -a1]])
    B = sp.Matrix([0, 1])
    # Desired poles
    p1 = -rng.randint(3, 8)
    p2 = -rng.randint(3, 8)
    desired_poly = sp.expand((s - p1)*(s - p2))
    # For CCF: K = [alpha0 - a0, alpha1 - a1]
    alpha0 = p1 * p2
    alpha1 = -(p1 + p2)
    k1 = alpha0 - a0
    k2 = alpha1 - a1
    stmt = (f"Place poles at $s = {p1}, {p2}$ for $A = {sp.latex(A)}$, $B = {sp.latex(B)}$ "
            "(controllable canonical form).")
    sol = (f"Desired char. poly: $s^2 + {alpha1}s + {alpha0}$\n\n"
           f"Current char. poly: $s^2 + {a1}s + {a0}$\n\n"
           f"$K = [{alpha0} - {a0},\\; {alpha1} - {a1}] = [{k1},\\; {k2}]$\n\n"
           f"Verify: $A - BK$ has eigenvalues ${p1}, {p2}$")
    return Problem("Pole placement (CCF)", stmt, sol)

def gen_matrix_exp(rng: random.Random) -> Problem:
    l1 = -rng.randint(1, 5)
    l2 = -rng.randint(l1+1, 8) if l1 > -5 else -rng.randint(6, 9)
    A = sp.Matrix([[l1, 0], [0, l2]])
    t = sp.Symbol('t', positive=True)
    eAt = sp.Matrix([[sp.exp(l1*t), 0], [0, sp.exp(l2*t)]])
    stmt = f"Compute $e^{{At}}$ for diagonal $A = {sp.latex(A)}$."
    sol = f"$e^{{At}} = {sp.latex(eAt)}$"
    return Problem("Matrix exponential (diagonal)", stmt, sol)

GENERATORS = [gen_ss_to_tf, gen_controllability, gen_observability, gen_pole_placement, gen_matrix_exp]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.8 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, state-space, modern-control]\n"
              "type: practice\n---\n# 11.8 Practice — State-Space Representation\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

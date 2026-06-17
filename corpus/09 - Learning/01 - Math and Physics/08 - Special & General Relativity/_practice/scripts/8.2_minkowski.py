#!/usr/bin/env python3
"""
8.2_minkowski.py — Practice problem generator for Chapter 8.2
(Minkowski Spacetime & 4-Vectors).

Archetypes:
  1. Index lowering/raising with η_μν
  2. 4-velocity normalization check
  3. Energy-momentum relation (mass-shell)
  4. Invariant mass of a multi-particle system
  5. Lorentz transformation of a 4-vector
  6. Inner product classification (timelike/spacelike/null)

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import sqrt, Rational, latex, simplify, Matrix

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

eta = Matrix([[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

def gen_index_lower(rng: random.Random) -> Problem:
    V = [Rational(rng.randint(-5,5),1) for _ in range(4)]
    V_low = [-V[0], V[1], V[2], V[3]]
    stmt = f"Lower the index of $V^\\mu = ({V[0]}, {V[1]}, {V[2]}, {V[3]})$. Compute $V_\\mu = \\eta_{{\\mu\\nu}}V^\\nu$."
    sol = (f"$V_0 = \\eta_{{00}}V^0 = (-1)({V[0]}) = {V_low[0]}$\n\n"
           f"$V_i = \\eta_{{ii}}V^i = (+1)(V^i)$ for $i=1,2,3$\n\n"
           f"$V_\\mu = ({V_low[0]}, {V_low[1]}, {V_low[2]}, {V_low[3]})$")
    return Problem("Index Lowering", stmt, sol)

def gen_4vel_norm(rng: random.Random) -> Problem:
    betas = [Rational(3,5), Rational(4,5), Rational(5,13), Rational(12,13)]
    beta = rng.choice(betas)
    gamma = 1/sqrt(1-beta**2)
    U0 = simplify(gamma)
    U1 = simplify(gamma*beta)
    norm = simplify(-(U0)**2 + U1**2)
    stmt = (f"A particle moves at $\\beta = {latex(beta)}$ along $x$. "
            f"Compute $U^\\mu$ and verify $U_\\mu U^\\mu = -c^2$ (using $c=1$).")
    sol = (f"$\\gamma = {latex(gamma)}$\n\n"
           f"$U^\\mu = \\gamma(1, \\beta, 0, 0) = ({latex(U0)}, {latex(U1)}, 0, 0)$\n\n"
           f"$U_\\mu U^\\mu = -({latex(U0)})^2 + ({latex(U1)})^2 = {latex(simplify(-U0**2+U1**2))}$\n\n"
           f"$= -1$ ✓ (i.e., $-c^2$ with $c=1$)")
    assert simplify(norm + 1) == 0
    return Problem("4-Velocity Normalization", stmt, sol)

def gen_mass_shell(rng: random.Random) -> Problem:
    m = Rational(rng.randint(1,10),1)
    gamma = Rational(rng.choice([2,3,4,5]),1)
    E = m*gamma
    p = simplify(sqrt(E**2 - m**2))
    stmt = (f"A particle has rest mass $m = {latex(m)}$ GeV/$c^2$ and Lorentz factor $\\gamma = {latex(gamma)}$. "
            "Compute $E$, $|\\mathbf{{p}}|$, and verify $E^2 = p^2c^2 + m^2c^4$ (using $c=1$).")
    sol = (f"$E = \\gamma m = {latex(gamma)} \\times {latex(m)} = {latex(E)}$ GeV\n\n"
           f"$p^2 = E^2 - m^2 = {latex(E**2)} - {latex(m**2)} = {latex(E**2-m**2)}$\n\n"
           f"$p = {latex(p)}$ GeV/$c$\n\n"
           f"Check: $E^2 = {latex(E**2)} = p^2 + m^2 = {latex(p**2)} + {latex(m**2)} = {latex(p**2+m**2)}$ ✓")
    assert simplify(E**2 - p**2 - m**2) == 0
    return Problem("Mass-Shell Condition", stmt, sol)

def gen_invariant_mass(rng: random.Random) -> Problem:
    E1 = Rational(rng.randint(1,10),1)
    E2 = Rational(rng.randint(1,10),1)
    angle = rng.choice([0, 1])  # 0=opposite, 1=same direction
    if angle == 0:
        p_tot = E1 - E2
        label = "opposite directions"
    else:
        p_tot = E1 + E2
        label = "same direction"
    E_tot = E1 + E2
    M2 = simplify(E_tot**2 - p_tot**2)
    M = simplify(sqrt(M2))
    stmt = (f"Two photons have energies $E_1 = {latex(E1)}$ GeV and $E_2 = {latex(E2)}$ GeV, "
            f"traveling in **{label}**. Find the invariant mass of the system.")
    sol = (f"$P^\\mu = ({latex(E_tot)}, {latex(p_tot)}, 0, 0)$\n\n"
           f"$M^2 = -P_\\mu P^\\mu = E_{{tot}}^2 - p_{{tot}}^2 = {latex(E_tot**2)} - {latex(p_tot**2)} = {latex(M2)}$\n\n"
           f"$M = {latex(M)}$ GeV/$c^2$")
    return Problem("Invariant Mass", stmt, sol)

def gen_inner_product(rng: random.Random) -> Problem:
    A = [Rational(rng.randint(-5,5),1) for _ in range(4)]
    ip = -A[0]**2 + A[1]**2 + A[2]**2 + A[3]**2
    if ip < 0: cls = "Timelike"
    elif ip > 0: cls = "Spacelike"
    else: cls = "Null (lightlike)"
    stmt = f"Classify the 4-vector $A^\\mu = ({A[0]}, {A[1]}, {A[2]}, {A[3]})$."
    sol = (f"$A_\\mu A^\\mu = -({A[0]})^2 + ({A[1]})^2 + ({A[2]})^2 + ({A[3]})^2 = {latex(ip)}$\n\n"
           f"Classification: **{cls}**")
    return Problem("4-Vector Classification", stmt, sol)

GENERATORS = [gen_index_lower, gen_4vel_norm, gen_mass_shell, gen_invariant_mass, gen_inner_product]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=15)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, minkowski, four-vectors]\nseed: {seed}\n---\n\n# 8.2 Practice — Minkowski Spacetime & 4-Vectors\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8"); print(f"Written to {args.out}")
    else: print(output)

if __name__ == "__main__":
    main()

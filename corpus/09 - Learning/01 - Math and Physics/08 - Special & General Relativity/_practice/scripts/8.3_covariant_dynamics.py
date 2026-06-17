#!/usr/bin/env python3
"""
8.3_covariant_dynamics.py — Practice problems for Chapter 8.3
(Covariant Relativistic Dynamics).

Archetypes:
  1. Relativistic momentum calculation
  2. Threshold energy for particle production
  3. Hyperbolic motion kinematics
  4. 4-force from electromagnetic field
  5. Relativistic kinetic energy
  6. Center-of-momentum frame velocity

#review/physics
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp
from sympy import sqrt, Rational, latex, simplify

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                f"<details>\n\n<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_rel_momentum(rng: random.Random) -> Problem:
    betas = [Rational(3,5), Rational(4,5), Rational(12,13), Rational(24,25)]
    beta = rng.choice(betas)
    gamma = 1/sqrt(1-beta**2)
    m = Rational(rng.randint(1,10),1)
    p = simplify(gamma*m*beta)
    E = simplify(gamma*m)
    K = simplify(E - m)
    stmt = f"A particle of mass $m={latex(m)}$ GeV/$c^2$ moves at $\\beta={latex(beta)}$. Find $p$, $E$, $K$."
    sol = (f"$\\gamma={latex(gamma)}$, $p=\\gamma m\\beta={latex(p)}$ GeV/$c$, "
           f"$E=\\gamma m={latex(E)}$ GeV, $K=E-m={latex(K)}$ GeV")
    return Problem("Relativistic Momentum & Energy", stmt, sol)

def gen_threshold(rng: random.Random) -> Problem:
    m_a = Rational(rng.choice([1,2,5]),1)
    m_b = m_a
    n_products = rng.choice([3,4])
    M_f = n_products * m_a
    K_th = simplify((M_f**2 - (m_a+m_b)**2)/(2*m_b))
    stmt = (f"Find threshold KE for $a+b\\to {n_products}$ particles, all mass $m={latex(m_a)}$ GeV/$c^2$, "
            f"with target $b$ at rest.")
    sol = (f"$M_f = {n_products}m = {latex(M_f)}$, "
           f"$K_{{th}} = \\frac{{M_f^2-(m_a+m_b)^2}}{{2m_b}} = "
           f"\\frac{{{latex(M_f**2)}-{latex((m_a+m_b)**2)}}}{{{latex(2*m_b)}}} = {latex(K_th)}$ GeV")
    return Problem("Threshold Energy", stmt, sol)

def gen_hyperbolic(rng: random.Random) -> Problem:
    g = Rational(10,1)  # m/s^2 simplified
    tau = Rational(rng.randint(1,5),1)  # years
    beta_final = sp.tanh(g*tau)
    stmt = f"Proper acceleration $g={latex(g)}$ (units where $c=1$). After proper time $\\tau={latex(tau)}$, find $\\beta$."
    sol = f"$\\beta = \\tanh(g\\tau) = \\tanh({latex(g*tau)}) = {latex(simplify(beta_final))}$"
    return Problem("Hyperbolic Motion", stmt, sol)

def gen_kinetic_energy(rng: random.Random) -> Problem:
    betas = [Rational(3,5), Rational(4,5), Rational(5,13)]
    beta = rng.choice(betas)
    gamma = 1/sqrt(1-beta**2)
    m = Rational(rng.randint(1,5),1)
    K = simplify((gamma-1)*m)
    K_classical = simplify(m*beta**2/2)
    stmt = f"Particle mass $m={latex(m)}$, $\\beta={latex(beta)}$. Compare relativistic and classical KE."
    sol = (f"$K_{{rel}} = (\\gamma-1)m = ({latex(gamma)}-1)\\times{latex(m)} = {latex(K)}$\n\n"
           f"$K_{{class}} = \\frac{{1}}{{2}}m\\beta^2 = {latex(K_classical)}$\n\n"
           f"Ratio: ${latex(simplify(K/K_classical))}$")
    return Problem("Relativistic vs Classical KE", stmt, sol)

GENERATORS = [gen_rel_momentum, gen_threshold, gen_hyperbolic, gen_kinetic_energy]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed else random.randint(0,2**31)
    rng = random.Random(seed)
    problems = [GENERATORS[i%len(GENERATORS)](rng) for i in range(args.count)]
    header = f"---\ntags: [practice, relativistic-dynamics]\nseed: {seed}\n---\n\n# 8.3 Practice — Covariant Dynamics\n\n---\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i,p in enumerate(problems))
    output = header + body
    if args.out: Path(args.out).write_text(output, encoding="utf-8")
    else: print(output)

if __name__ == "__main__":
    main()

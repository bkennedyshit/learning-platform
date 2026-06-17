#!/usr/bin/env python3
"""
11.2_block_diagrams.py — Practice problem generator for Chapter 11.2
(Block Diagrams & Feedback).

Archetypes:
  1. Closed-loop TF from forward/feedback paths
  2. Series/parallel reduction
  3. Steady-state error (system type)
  4. Mason's Gain Formula (2 loops)
  5. Sensitivity function computation

Usage:
  python 11.2_block_diagrams.py --count 10 --seed 42
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

def gen_closed_loop(rng: random.Random) -> Problem:
    K = rng.randint(2, 20)
    p1 = rng.randint(1, 6)
    p2 = rng.randint(p1+1, 10)
    G = sp.Rational(K, 1) / ((s+p1)*(s+p2))
    H = sp.Rational(1, 1)
    T = sp.simplify(G / (1 + G*H))
    stmt = (f"Find the closed-loop TF $T(s)$ for unity feedback with "
            f"$G(s) = \\dfrac{{{K}}}{{(s+{p1})(s+{p2})}}$.")
    sol = (f"$T(s) = \\dfrac{{G}}{{1+G}} = \\dfrac{{{K}}}{{(s+{p1})(s+{p2})+{K}}} "
           f"= \\dfrac{{{K}}}{{s^2+{p1+p2}s+{p1*p2+K}}}$\n\n"
           f"Simplified: ${sp.latex(T)}$")
    return Problem("Closed-loop transfer function", stmt, sol)

def gen_series_parallel(rng: random.Random) -> Problem:
    a, b, c = [rng.randint(1, 8) for _ in range(3)]
    G1 = sp.Rational(a, 1) / (s + b)
    G2 = sp.Rational(c, 1) / (s + a)
    series = sp.simplify(G1 * G2)
    parallel = sp.simplify(G1 + G2)
    stmt = (f"Given $G_1 = \\dfrac{{{a}}}{{s+{b}}}$ and $G_2 = \\dfrac{{{c}}}{{s+{a}}}$, "
            "find (a) series and (b) parallel combinations.")
    sol = (f"(a) Series: $G_1 G_2 = {sp.latex(series)}$\n\n"
           f"(b) Parallel: $G_1 + G_2 = {sp.latex(parallel)}$")
    return Problem("Series/parallel reduction", stmt, sol)

def gen_steady_state_error(rng: random.Random) -> Problem:
    K = rng.randint(5, 50)
    p = rng.randint(1, 8)
    sys_type = rng.choice([0, 1])
    if sys_type == 0:
        L = sp.Rational(K, 1) / (s + p)
        Kp = sp.Rational(K, p)
        ess = 1 / (1 + Kp)
        stmt = f"Find $e_{{ss}}$ to a unit step for $L(s) = \\dfrac{{{K}}}{{s+{p}}}$ (unity feedback)."
        sol = f"Type 0. $K_p = L(0) = {K}/{p} = {Kp}$. $e_{{ss}} = 1/(1+{Kp}) = {ess}$"
    else:
        L = sp.Rational(K, 1) / (s * (s + p))
        Kv = sp.Rational(K, p)
        ess = 1 / Kv
        stmt = f"Find $e_{{ss}}$ to a unit ramp for $L(s) = \\dfrac{{{K}}}{{s(s+{p})}}$ (unity feedback)."
        sol = f"Type 1. $K_v = \\lim_{{s\\to 0}} sL(s) = {K}/{p} = {Kv}$. $e_{{ss}} = 1/{Kv} = {ess}$"
    return Problem("Steady-state error", stmt, sol)

def gen_sensitivity(rng: random.Random) -> Problem:
    K = rng.randint(5, 30)
    p = rng.randint(1, 6)
    G0 = sp.Rational(K, p)
    S = 1 / (1 + G0)
    stmt = (f"A plant $G(s)={K}/(s+{p})$ has unity feedback with $C=1$. "
            "Compute the sensitivity $S$ at DC.")
    sol = f"$S = 1/(1+CG(0)) = 1/(1+{K}/{p}) = 1/(1+{G0}) = {S}$. A {float(S)*100:.1f}% sensitivity."
    return Problem("Sensitivity function", stmt, sol)

GENERATORS = [gen_closed_loop, gen_series_parallel, gen_steady_state_error, gen_sensitivity]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.2 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, block-diagrams, feedback]\n"
              "type: practice\n---\n# 11.2 Practice — Block Diagrams & Feedback\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(output)} bytes to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

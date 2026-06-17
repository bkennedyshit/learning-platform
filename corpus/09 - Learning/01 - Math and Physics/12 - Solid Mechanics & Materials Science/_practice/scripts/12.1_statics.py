#!/usr/bin/env python3
"""
12.1_statics.py — Practice problem generator for Chapter 12.1
(Statics & Equilibrium).

Generates randomized drill problems across 5 archetypes:
  1. Simply-supported beam reactions (point load)
  2. Cantilever beam reactions (distributed load)
  3. Moment about a point (cross product)
  4. Truss member force (method of joints)
  5. Overhanging beam reactions

Usage:
  python 12.1_statics.py
  python 12.1_statics.py --count 20 --seed 42
  python 12.1_statics.py --count 20 --seed 42 --out /tmp/_121.md
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
from fractions import Fraction
import sympy as sp

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )

def gen_simply_supported(rng: random.Random) -> Problem:
    L = rng.choice([4, 5, 6, 8, 10])
    a = rng.randint(1, L - 1)
    P = rng.choice([5, 8, 10, 12, 15, 20, 24, 30])
    b = L - a
    By = sp.Rational(P * a, L)
    Ay = P - By
    stmt = (f"A simply-supported beam of length $L = {L}$ m has a pin at $A$ (left) "
            f"and roller at $B$ (right). A concentrated load $P = {P}$ kN acts downward "
            f"at $x = {a}$ m from $A$. Find all support reactions.")
    sol = (f"$\\sum M_A = 0$: $B_y \\cdot {L} - {P} \\cdot {a} = 0 \\Rightarrow B_y = {sp.latex(By)}$ kN\n\n"
           f"$\\sum F_y = 0$: $A_y = {P} - {sp.latex(By)} = {sp.latex(Ay)}$ kN\n\n"
           f"$A_x = 0$ (no horizontal loads).\n\n"
           f"**Answers:** $A_y = {sp.latex(Ay)}$ kN, $B_y = {sp.latex(By)}$ kN")
    return Problem("Simply-supported beam reactions", stmt, sol)

def gen_cantilever_distributed(rng: random.Random) -> Problem:
    L = rng.choice([2, 3, 4, 5, 6])
    w = rng.choice([3, 4, 5, 6, 8, 10])
    FR = w * L
    MA = sp.Rational(w * L**2, 2)
    stmt = (f"A cantilever beam (fixed at $A$, free at $B$) of length $L = {L}$ m "
            f"carries a uniform distributed load $w = {w}$ kN/m over its entire length. "
            f"Find the fixed-end reactions $A_y$ and $M_A$.")
    sol = (f"Resultant: $F_R = wL = {w} \\times {L} = {FR}$ kN at $\\bar{{x}} = L/2 = {sp.Rational(L,2)}$ m\n\n"
           f"$\\sum F_y = 0$: $A_y = {FR}$ kN\n\n"
           f"$\\sum M_A = 0$: $M_A = F_R \\cdot \\bar{{x}} = {FR} \\times {sp.Rational(L,2)} = {sp.latex(MA)}$ kN·m (CCW)\n\n"
           f"**Answers:** $A_y = {FR}$ kN ↑, $M_A = {sp.latex(MA)}$ kN·m ↺")
    return Problem("Cantilever beam with distributed load", stmt, sol)

def gen_moment_cross_product(rng: random.Random) -> Problem:
    rx, ry = rng.randint(-4, 4), rng.randint(-4, 4)
    Fx, Fy = rng.randint(-10, 10), rng.randint(-10, 10)
    while Fx == 0 and Fy == 0:
        Fx, Fy = rng.randint(-10, 10), rng.randint(-10, 10)
    Mz = rx * Fy - ry * Fx
    stmt = (f"A force $\\mathbf{{F}} = {Fx}\\hat{{\\mathbf{{i}}}} + {Fy}\\hat{{\\mathbf{{j}}}}$ N "
            f"acts at point $P$ with position vector $\\mathbf{{r}} = {rx}\\hat{{\\mathbf{{i}}}} + {ry}\\hat{{\\mathbf{{j}}}}$ m "
            f"from point $O$. Compute the moment $\\mathbf{{M}}_O = \\mathbf{{r}} \\times \\mathbf{{F}}$.")
    sol = (f"$M_z = r_x F_y - r_y F_x = ({rx})({Fy}) - ({ry})({Fx}) = {rx*Fy} - {ry*Fx} = {Mz}$ N·m\n\n"
           f"$\\mathbf{{M}}_O = {Mz}\\hat{{\\mathbf{{k}}}}$ N·m "
           f"({'CCW' if Mz > 0 else 'CW' if Mz < 0 else 'zero'})")
    return Problem("Moment via cross product (2D)", stmt, sol)

def gen_truss_joint(rng: random.Random) -> Problem:
    h = rng.choice([3, 4, 5, 6])
    w = rng.choice([3, 4, 5, 6])
    P = rng.choice([10, 12, 15, 20, 24, 30])
    hyp = sp.sqrt(h**2 + w**2)
    sin_a = sp.Rational(h, 1) / hyp
    cos_a = sp.Rational(w, 1) / hyp
    F_diag = -sp.Rational(P, 1) / (2 * sin_a)
    F_bot = -F_diag * cos_a
    stmt = (f"A symmetric triangular truss has span $2w = {2*w}$ m and height $h = {h}$ m. "
            f"A vertical load $P = {P}$ kN acts at the apex. Pin at left, roller at right. "
            f"Find the force in one diagonal member and the bottom chord using method of joints at the left support.")
    sol = (f"By symmetry: $A_y = B_y = P/2 = {sp.Rational(P,2)}$ kN\n\n"
           f"Diagonal length: $\\sqrt{{{h}^2 + {w}^2}} = {sp.latex(hyp)}$ m\n\n"
           f"$\\sin\\alpha = {h}/{sp.latex(hyp)}$, $\\cos\\alpha = {w}/{sp.latex(hyp)}$\n\n"
           f"At left joint, $\\sum F_y = 0$: $A_y + F_{{diag}}\\sin\\alpha = 0$\n\n"
           f"$F_{{diag}} = {sp.latex(F_diag)}$ kN (compression)\n\n"
           f"$\\sum F_x = 0$: $F_{{bot}} = -F_{{diag}}\\cos\\alpha = {sp.latex(F_bot)}$ kN (tension)")
    return Problem("Truss — method of joints", stmt, sol)

def gen_overhanging_beam(rng: random.Random) -> Problem:
    L = rng.choice([4, 5, 6, 8])
    a = rng.randint(1, L - 2)
    overhang = rng.choice([1, 2, 3])
    P = rng.choice([5, 8, 10, 12, 15, 20])
    total = L + overhang
    By = sp.Rational(P * (a), L)  # moment about A, roller at B=L
    # Actually: P at distance 'a' from A, roller at B at distance L from A, overhang beyond B
    # Let's put load at overhang tip for more interest
    By_val = sp.Rational(P * total, L)
    Ay_val = P - By_val  # will be negative (downward) for overhang load
    stmt = (f"Beam $AC$: pin at $A$, roller at $B$ ($x = {L}$ m from $A$), overhang to $C$ "
            f"($x = {total}$ m). A load $P = {P}$ kN acts at $C$. Find reactions.")
    sol = (f"$\\sum M_A = 0$: $B_y({L}) - P({total}) = 0 \\Rightarrow B_y = {sp.latex(By_val)}$ kN ↑\n\n"
           f"$\\sum F_y = 0$: $A_y = P - B_y = {P} - {sp.latex(By_val)} = {sp.latex(Ay_val)}$ kN\n\n"
           f"(Negative $A_y$ means the pin pulls **down** — the beam lifts at $A$.)\n\n"
           f"**Answers:** $A_y = {sp.latex(Ay_val)}$ kN, $B_y = {sp.latex(By_val)}$ kN")
    return Problem("Overhanging beam reactions", stmt, sol)

GENERATORS = [gen_simply_supported, gen_cantilever_distributed,
              gen_moment_cross_product, gen_truss_joint, gen_overhanging_beam]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.1 Statics problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.1 Statics & Equilibrium — Practice Problems\n",
             f"#review/mechanics  Generated {args.count} problems\n\n---\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("\n---\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Written {len(text)} bytes → {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()

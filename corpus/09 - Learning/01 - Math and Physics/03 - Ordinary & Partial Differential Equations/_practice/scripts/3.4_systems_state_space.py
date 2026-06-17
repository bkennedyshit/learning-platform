#!/usr/bin/env python3
"""
3.4_systems_state_space.py — Practice problem generator for Chapter 3.4
(Systems of Linear ODEs & State Space).

Archetypes:
  1. 2×2 system with distinct real eigenvalues
  2. 2×2 system with complex eigenvalues
  3. Phase portrait classification
  4. Convert 2nd-order ODE to system
  5. Matrix exponential (2×2 diagonal)
  6. IVP for 2×2 system

Usage:
  python 3.4_systems_state_space.py --count 8
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

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
            "?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_real_system(rng: random.Random) -> Problem:
    l1 = rng.randint(-4, -1)
    l2 = rng.randint(1, 4)
    # Build A = S D S^-1 with simple S
    S = sp.Matrix([[1, 1], [1, -1]])
    D = sp.diag(l1, l2)
    A = S * D * S.inv()
    stmt = f"Solve $\\mathbf{{x}}' = {sp.latex(A)}\\mathbf{{x}}$."
    sol = (
        f"Eigenvalues: $\\lambda_1 = {l1}$, $\\lambda_2 = {l2}$.\n\n"
        f"Eigenvectors from $(A - \\lambda I)\\mathbf{{v}} = 0$.\n\n"
        f"General solution: $\\mathbf{{x}}(t) = c_1 e^{{{l1}t}}\\mathbf{{v}}_1 + c_2 e^{{{l2}t}}\\mathbf{{v}}_2$.\n\n"
        f"Phase portrait: **saddle point** ($\\lambda_1 < 0 < \\lambda_2$)."
    )
    return Problem("2×2 system (real eigenvalues)", stmt, sol)


def gen_complex_system(rng: random.Random) -> Problem:
    alpha = rng.randint(-3, -1)
    beta = rng.randint(1, 3)
    A = sp.Matrix([[alpha, -beta], [beta, alpha]])
    stmt = f"Solve $\\mathbf{{x}}' = {sp.latex(A)}\\mathbf{{x}}$ and classify the phase portrait."
    sol = (
        f"$\\det(A - \\lambda I) = (\\lambda - {alpha})^2 + {beta**2} = 0$.\n\n"
        f"$\\lambda = {alpha} \\pm {beta}i$.\n\n"
        f"General solution: $\\mathbf{{x}}(t) = e^{{{alpha}t}}(c_1[\\cos {beta}t\\,\\mathbf{{a}} - \\sin {beta}t\\,\\mathbf{{b}}] "
        f"+ c_2[\\sin {beta}t\\,\\mathbf{{a}} + \\cos {beta}t\\,\\mathbf{{b}}])$.\n\n"
        f"Phase portrait: **stable spiral** (Re $< 0$)."
    )
    return Problem("2×2 system (complex eigenvalues)", stmt, sol)


def gen_classify(rng: random.Random) -> Problem:
    tr = rng.randint(-6, 6)
    det = rng.randint(-8, 8)
    disc = tr**2 - 4 * det
    if det < 0:
        ptype = "saddle point"
    elif det > 0 and disc > 0 and tr < 0:
        ptype = "stable node"
    elif det > 0 and disc > 0 and tr > 0:
        ptype = "unstable node"
    elif det > 0 and disc < 0 and tr < 0:
        ptype = "stable spiral"
    elif det > 0 and disc < 0 and tr > 0:
        ptype = "unstable spiral"
    elif det > 0 and tr == 0:
        ptype = "center"
    else:
        ptype = "degenerate/borderline case"
    stmt = (
        f"A $2\\times 2$ matrix $A$ has $\\text{{tr}}(A) = {tr}$ and $\\det(A) = {det}$. "
        f"Classify the equilibrium."
    )
    sol = (
        f"$\\Delta = \\text{{tr}}^2 - 4\\det = {tr**2} - {4*det} = {disc}$.\n\n"
        f"Classification: **{ptype}**."
    )
    return Problem("Phase portrait classification", stmt, sol)


def gen_convert(rng: random.Random) -> Problem:
    a1 = rng.randint(1, 5)
    a0 = rng.randint(1, 6)
    stmt = f"Convert $y'' + {a1}y' + {a0}y = 0$ to a first-order system $\\mathbf{{x}}' = A\\mathbf{{x}}$."
    sol = (
        f"Let $x_1 = y$, $x_2 = y'$.\n\n"
        f"$$\nA = \\begin{{pmatrix}} 0 & 1 \\\\ -{a0} & -{a1} \\end{{pmatrix}}\n$$\n\n"
        f"Eigenvalues of $A$ satisfy $\\lambda^2 + {a1}\\lambda + {a0} = 0$."
    )
    return Problem("Convert ODE to system", stmt, sol)


def gen_mat_exp(rng: random.Random) -> Problem:
    l1 = rng.randint(-3, 3)
    l2 = rng.randint(-3, 3)
    D = sp.diag(l1, l2)
    stmt = f"Compute $e^{{Dt}}$ for $D = {sp.latex(D)}$."
    sol = (
        f"$e^{{Dt}} = \\text{{diag}}(e^{{{l1}t}}, e^{{{l2}t}})$."
    )
    return Problem("Matrix exponential (diagonal)", stmt, sol)


def gen_ivp_system(rng: random.Random) -> Problem:
    l1, l2 = -1, -3
    x0 = sp.Matrix([rng.randint(1, 4), rng.randint(-3, 3)])
    stmt = (
        f"Solve $\\mathbf{{x}}' = \\begin{{pmatrix}}-1&0\\\\0&-3\\end{{pmatrix}}\\mathbf{{x}}$, "
        f"$\\mathbf{{x}}(0) = {sp.latex(x0)}$."
    )
    sol = (
        f"$\\mathbf{{x}}(t) = \\begin{{pmatrix}}{x0[0]}e^{{-t}}\\\\{x0[1]}e^{{-3t}}\\end{{pmatrix}}$."
    )
    return Problem("IVP for diagonal system", stmt, sol)


GENERATORS = [gen_real_system, gen_complex_system, gen_classify, gen_convert, gen_mat_exp, gen_ivp_system]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.4 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / f"3.4_systems_{today}.md"

    lines = [
        "#review/math\n",
        "# 3.4 Practice — Systems of Linear ODEs\n",
        f"Generated: {today} | Seed: {seed} | Count: {args.count}\n\n---\n",
    ]
    for idx, p in enumerate(problems, 1):
        lines.append(p.render(idx))
        lines.append("\n---\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Wrote {args.count} problems to {out_path}")


if __name__ == "__main__":
    main()

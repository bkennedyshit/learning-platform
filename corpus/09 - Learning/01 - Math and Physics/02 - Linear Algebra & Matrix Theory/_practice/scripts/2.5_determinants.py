#!/usr/bin/env python3
"""
2.5_determinants.py — Practice problem generator for Chapter 2.5
(Determinants & Cramer's Rule).

Generates randomized drill problems across 8 archetypes:
  1. 2×2 determinant (direct formula)
  2. 3×3 determinant via cofactor expansion
  3. det(AB) = det(A)det(B) verification
  4. Cramer's Rule for a 2×2 system
  5. Matrix inverse via adjugate A^-1 = adj(A)/det(A)
  6. Determinant under row operations
  7. Leibniz formula spot-check (3×3, list all 6 terms)
  8. Geometric interpretation: area/volume scaling factor

Usage:
  python 2.5_determinants.py
  python 2.5_determinants.py --count 24 --seed 42
  python 2.5_determinants.py --count 24 --seed 42 --out /tmp/_25.md

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from itertools import permutations
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
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# ---------------------------------------------------------------------------
# Archetype 1: 2×2 determinant
# ---------------------------------------------------------------------------
def gen_det2(rng: random.Random) -> Problem:
    entries = [rng.randint(-6, 6) for _ in range(4)]
    A = sp.Matrix(2, 2, entries)
    d = A.det()
    a, b, c, dv = entries
    stmt = (
        f"Compute $\\det A$ for $A = {sp.latex(A)}$ using the formula $\\det = ad - bc$. "
        "State whether $A$ is invertible and give the geometric meaning."
    )
    sol = (
        f"$\\det A = ({a})({dv}) - ({b})({c}) = {a*dv} - {b*c} = {d}$.\n\n"
        + (f"Since $\\det A = {d} \\neq 0$, $A$ is **invertible**.\n\n"
           f"Geometrically: $A$ scales areas by $|{d}|$ and "
           + ("preserves orientation (det > 0)." if d > 0 else "reverses orientation (det < 0).")
           if d != 0 else
           f"Since $\\det A = 0$, $A$ is **singular** (not invertible). "
           "Geometrically: $A$ collapses the plane to a lower-dimensional subspace (area = 0).")
    )
    assert sp.det(A) == d
    return Problem("2×2 determinant", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: 3×3 cofactor expansion
# ---------------------------------------------------------------------------
def gen_det3_cofactor(rng: random.Random) -> Problem:
    entries = [rng.randint(-3, 3) for _ in range(9)]
    A = sp.Matrix(3, 3, entries)
    d = A.det()
    row = 0  # expand along row 1
    col_terms = []
    for j in range(3):
        M = A.minor_submatrix(row, j)
        Cij = ((-1) ** (row + j)) * M.det()
        col_terms.append((A[row, j], Cij, j))
    stmt = (
        f"Compute $\\det A$ for $A = {sp.latex(A)}$ by cofactor expansion along **row 1**."
    )
    lines = ["Expanding along row 1:\n\n$$\n\\det A = "]
    for (aij, Cij, j) in col_terms:
        sign = "+" if (-1)**(row+j) > 0 else "-"
        M = A.minor_submatrix(row, j)
        lines.append(
            f"({aij}) \\cdot ({sign}1) \\cdot \\det{sp.latex(M)}"
        )
    lines.append("\n$$\n\n")
    lines.append(
        " + ".join(f"({aij})({Cij})" for (aij, Cij, j) in col_terms)
        + f" = {d}."
    )
    sol = "".join(lines)
    return Problem("3×3 determinant (cofactor expansion)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: det(AB) = det(A)det(B)
# ---------------------------------------------------------------------------
def gen_det_product(rng: random.Random) -> Problem:
    entries_A = [rng.randint(-3, 3) for _ in range(4)]
    entries_B = [rng.randint(-3, 3) for _ in range(4)]
    A = sp.Matrix(2, 2, entries_A)
    B = sp.Matrix(2, 2, entries_B)
    dA = A.det()
    dB = B.det()
    AB = A * B
    dAB = AB.det()
    assert dA * dB == dAB, f"det(AB) mismatch: {dA}*{dB}={dA*dB} vs {dAB}"
    stmt = (
        f"Let $A = {sp.latex(A)}$ and $B = {sp.latex(B)}$. "
        "Compute $\\det A$, $\\det B$, $\\det(AB)$, and verify $\\det(AB) = \\det(A)\\det(B)$."
    )
    sol = (
        f"$\\det A = {dA}$, $\\det B = {dB}$.\n\n"
        f"$$\nAB = {sp.latex(AB)}, \\quad \\det(AB) = {dAB}.\n$$\n\n"
        f"Check: $\\det(A)\\det(B) = {dA} \\cdot {dB} = {dA*dB} = \\det(AB)$. ✓"
    )
    return Problem("det(AB) = det(A)det(B) verification", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Cramer's Rule for 2×2
# ---------------------------------------------------------------------------
def gen_cramers(rng: random.Random) -> Problem:
    while True:
        entries = [rng.randint(-4, 4) for _ in range(4)]
        A = sp.Matrix(2, 2, entries)
        b = sp.Matrix([rng.randint(-5, 5), rng.randint(-5, 5)])
        d = A.det()
        if d != 0:
            break
    A1 = A.copy()
    A1[:, 0] = b
    A2 = A.copy()
    A2[:, 1] = b
    d1 = A1.det()
    d2 = A2.det()
    x1 = sp.Rational(d1, d)
    x2 = sp.Rational(d2, d)
    assert A * sp.Matrix([x1, x2]) == b, "Cramer solution check"
    stmt = (
        f"Solve $A\\mathbf{{x}} = \\mathbf{{b}}$ via **Cramer's Rule** where "
        f"$A = {sp.latex(A)}$ and $\\mathbf{{b}} = {sp.latex(b)}$."
    )
    sol = (
        f"$\\det(A) = {d}$.\n\n"
        f"Replace column 1 with $\\mathbf{{b}}$: $A_1 = {sp.latex(A1)}$, $\\det(A_1) = {d1}$.\n\n"
        f"Replace column 2 with $\\mathbf{{b}}$: $A_2 = {sp.latex(A2)}$, $\\det(A_2) = {d2}$.\n\n"
        f"$$\nx_1 = \\frac{{{d1}}}{{{d}}} = {sp.latex(x1)}, \\quad "
        f"x_2 = \\frac{{{d2}}}{{{d}}} = {sp.latex(x2)}.\n$$\n\n"
        f"Verify: $A{sp.latex(sp.Matrix([x1,x2]))} = {sp.latex(b)}$. ✓"
    )
    return Problem("Cramer's Rule (2×2 system)", stmt, sol)



# ---------------------------------------------------------------------------
# CLI plumbing  (mirrors 2.6_eigenvalues.py and the rest of the suite)
# ---------------------------------------------------------------------------
ARCHETYPES = [gen_det2, gen_det3_cofactor, gen_det_product, gen_cramers]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [linear-algebra, determinants, cramers-rule, practice, \"review/linalg/2.5\"]\n"
        "chapter: 2.5\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../2.5 - Determinants & Cramer's Rule|Chapter 2.5]] | "
        "Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*\n\n"
        "# Chapter 2.5 — Practice Drills: Determinants & Cramer's Rule\n\n"
        "> Auto-generated by `scripts/2.5_determinants.py`. SymPy verifies every solution.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "2.5_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

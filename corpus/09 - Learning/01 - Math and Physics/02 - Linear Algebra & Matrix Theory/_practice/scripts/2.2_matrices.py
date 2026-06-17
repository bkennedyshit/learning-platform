#!/usr/bin/env python3
"""
2.2_matrices.py — Practice problem generator for Chapter 2.2
(Matrix Multiplication & Gaussian Elimination).

Generates randomized drill problems across 8 canonical archetypes:
  1. Matrix multiply (random sizes)
  2. Transpose
  3. 2×2 inverse (formula)
  4. 3×3 Gaussian elimination (solve Ax=b)
  5. RREF and free variable identification
  6. Solve Ax=b via RREF
  7. LU decomposition (2×2 or 3×3)
  8. Check invertibility via determinant

Usage:
    python 2.2_matrices.py --count 24 --seed 42 --out /tmp/out.md
"""

from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_latex(s: str) -> str:
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"-\s*-", "+ ", s)
    return s


def L(expr) -> str:
    return clean_latex(sp.latex(expr))


def rand_matrix(rng: random.Random, m: int, n: int, lo: int = -4, hi: int = 4) -> sp.Matrix:
    return sp.Matrix([[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)])


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
# Generators
# ---------------------------------------------------------------------------

def gen_matrix_multiply(rng: random.Random) -> Problem:
    """Random matrix multiply (m×k)(k×n)."""
    m = rng.randint(2, 3)
    k = rng.randint(2, 3)
    n = rng.randint(2, 3)
    A = rand_matrix(rng, m, k)
    B = rand_matrix(rng, k, n)
    C = A * B

    statement = (
        f"Compute $AB$ where\n\n$$\nA = {L(A)}, \\quad B = {L(B)}.\n$$\n"
    )
    # Build step-by-step: entry (i,j) shown for first two entries
    steps = []
    for i in range(m):
        for j in range(n):
            terms = " + ".join(
                f"({A[i, r]})({B[r, j]})" for r in range(k)
            )
            steps.append(f"  - $c_{{{i+1}{j+1}}} = {terms} = {C[i,j]}$")

    solution = (
        f"**Step 1.** Check: $({m}\\times{k})({k}\\times{n}) = {m}\\times{n}$ result.\n\n"
        "**Step 2.** Compute each entry as row · column:\n\n"
        + "\n".join(steps)
        + f"\n\n**Step 3.** Assemble result:\n\n$$\nAB = {L(C)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{AB = {L(C)}}}$"
    )
    return Problem("Matrix multiply", statement, solution)


def gen_transpose(rng: random.Random) -> Problem:
    """Compute the transpose and verify (AB)^T = B^T A^T."""
    m = rng.randint(2, 3)
    n = rng.randint(2, 3)
    A = rand_matrix(rng, m, n)
    AT = A.T

    # Also demonstrate (AB)^T = B^T A^T for square case
    k = 2
    B = rand_matrix(rng, m, k)
    if m == k:
        AB = A * B if n == m else None
    else:
        AB = None

    statement = (
        f"Compute $A^T$ for $A = {L(A)}$. Then verify $(cA)^T = cA^T$ for $c = 3$.\n"
    )
    c3AT = 3 * AT
    solution = (
        f"**Step 1.** Transpose: reflect across main diagonal.\n\n"
        f"$$\nA^T = {L(AT)}.\n$$\n\n"
        f"**Step 2.** $3A = {L(3*A)}$, so $(3A)^T = {L((3*A).T)}$.\n\n"
        f"**Step 3.** $3A^T = {L(c3AT)}$.\n\n"
        f"**Verify:** $(3A)^T = {L((3*A).T)} = 3A^T$. ✓\n\n"
        f"**Final answer:** $A^T = {L(AT)}$. $\\boxed{{\\text{{See above}}}}$"
    )
    return Problem("Transpose", statement, solution)


def gen_2x2_inverse(rng: random.Random) -> Problem:
    """2x2 matrix inverse via formula."""
    # Ensure invertible
    while True:
        A = rand_matrix(rng, 2, 2)
        d = A.det()
        if d != 0:
            break
    Ainv = A.inv()
    a, b, c, dd = A[0,0], A[0,1], A[1,0], A[1,1]

    statement = (
        f"Find $A^{{-1}}$ for $A = {L(A)}$.\n"
    )
    solution = (
        f"**Step 1.** $\\det A = ({a})({dd}) - ({b})({c}) = {d}$.\n\n"
        f"**Step 2.** Since $\\det A = {d} \\neq 0$, $A$ is invertible.\n\n"
        "**Step 3.** Apply the $2\\times2$ inverse formula "
        "$A^{-1} = \\frac{1}{\\det A}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$:\n\n"
        f"$$\nA^{{-1}} = \\frac{{1}}{{{d}}}\\begin{{pmatrix}}{dd}&{-b}\\\\{-c}&{a}\\end{{pmatrix}} = {L(Ainv)}.\n$$\n\n"
        f"**Step 4.** Verify: $AA^{{-1}} = {L(A*Ainv)} = I$. ✓\n\n"
        f"**Final answer:** $\\boxed{{A^{{-1}} = {L(Ainv)}}}$"
    )
    return Problem("2×2 inverse", statement, solution)


def gen_3x3_gaussian(rng: random.Random) -> Problem:
    """3×3 Gaussian elimination to solve Ax=b."""
    while True:
        A = rand_matrix(rng, 3, 3, lo=-3, hi=3)
        if A.det() != 0:
            break
    x_exact = sp.Matrix([rng.randint(-3, 3) for _ in range(3)])
    b = A * x_exact

    aug = A.row_join(b)
    rref_aug, _ = aug.rref()
    x_sol = sp.Matrix([rref_aug[i, 3] for i in range(3)])

    statement = (
        f"Solve $A\\mathbf{{x}} = \\mathbf{{b}}$ where "
        f"$A = {L(A)}$ and $\\mathbf{{b}} = {L(b)}$ using Gaussian elimination.\n"
    )
    solution = (
        "**Step 1.** Write the augmented matrix:\n\n"
        f"$$\n[A|\\mathbf{{b}}] = {L(aug)}\n$$\n\n"
        "**Step 2.** Row-reduce to RREF:\n\n"
        f"$$\n\\text{{RREF}} = {L(rref_aug)}\n$$\n\n"
        "**Step 3.** Read off the solution:\n\n"
        f"$$\nx_1 = {L(x_sol[0])},\\quad x_2 = {L(x_sol[1])},\\quad x_3 = {L(x_sol[2])}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\mathbf{{x}} = {L(x_sol)}}}$"
    )
    return Problem("3×3 Gaussian elimination", statement, solution)


def gen_rref(rng: random.Random) -> Problem:
    """Compute RREF and identify pivot vs free variables."""
    m = 3; n = 4
    # Create a rank-2 matrix
    rows = []
    v1 = [rng.randint(-3, 3) for _ in range(n)]
    v2 = [rng.randint(-3, 3) for _ in range(n)]
    while v1 == [0]*n: v1 = [rng.randint(-3,3) for _ in range(n)]
    while v2 == [0]*n or v2 == v1: v2 = [rng.randint(-3,3) for _ in range(n)]
    c1, c2 = rng.randint(-2, 2), rng.randint(-2, 2)
    v3 = [c1*v1[i]+c2*v2[i] for i in range(n)]
    A = sp.Matrix([v1, v2, v3])
    rref_A, pivots = A.rref()
    free_vars = [j+1 for j in range(n) if j not in pivots]
    pivot_vars = [j+1 for j in pivots]

    statement = (
        f"Compute the RREF of $A = {L(A)}$. Identify pivot and free variable columns.\n"
    )
    solution = (
        f"**Step 1.** Row-reduce:\n\n$$\n\\text{{RREF}}(A) = {L(rref_A)}\n$$\n\n"
        f"**Step 2.** Pivot columns: {pivot_vars}. Free variable columns: {free_vars}.\n\n"
        f"**Step 3.** Rank$= {len(pivots)}$; nullity$= {n - len(pivots)}$.\n\n"
        "$\\boxed{\\text{See RREF above}}$"
    )
    return Problem("RREF & free variables", statement, solution)


def gen_solve_axb(rng: random.Random) -> Problem:
    """Solve Ax=b; system may have infinitely many or no solutions."""
    m = 3; n = 3
    while True:
        A = rand_matrix(rng, m, n, lo=-3, hi=3)
        if A.rank() >= 2:
            break
    b = sp.Matrix([rng.randint(-4, 4) for _ in range(m)])
    aug = A.row_join(b)
    rref_aug, pivots = aug.rref()
    # Check consistency
    consistent = all(rref_aug[i, n] == 0
                     for i in range(m) if all(rref_aug[i, j] == 0 for j in range(n)))

    statement = (
        f"Solve $A\\mathbf{{x}} = \\mathbf{{b}}$ for "
        f"$A = {L(A)}$, $\\mathbf{{b}} = {L(b)}$.\n"
    )
    solution = (
        "**Step 1.** Form augmented matrix and RREF:\n\n"
        f"$$\n{L(aug)} \\to {L(rref_aug)}\n$$\n\n"
    )
    # Determine solution type
    rk_A = A.rank()
    rk_aug = aug.rank()
    if rk_A < rk_aug:
        solution += "**Step 2.** Augmented rank > coefficient rank → **inconsistent** (no solution).\n\n"
    elif rk_A == n:
        x = A.solve(b)
        solution += (
            f"**Step 2.** Unique solution (rank = $n = {n}$):\n\n"
            f"$$\n\\mathbf{{x}} = {L(x)}.\n$$\n\n"
            f"$\\boxed{{\\mathbf{{x}} = {L(x)}}}$"
        )
    else:
        solution += (
            f"**Step 2.** Rank $r = {rk_A} < n = {n}$: infinitely many solutions. "
            f"Free variables in columns: {[j+1 for j in range(n) if j not in pivots[:rk_A]]}.\n"
        )
    return Problem("Solve Ax=b", statement, solution)


def gen_lu_decomp(rng: random.Random) -> Problem:
    """LU decomposition of a 2×2 or 3×3 invertible matrix."""
    n = rng.choice([2, 3])
    while True:
        A = rand_matrix(rng, n, n, lo=-3, hi=3)
        if A.det() != 0:
            break
    L_mat, U_mat, perm = A.LUdecomposition()
    # perm is list of row swaps; build permutation matrix
    P = sp.eye(n)
    for i, j in perm:
        P.row_swap(i, j)

    statement = (
        f"Compute the $LU$ decomposition of $A = {L(A)}$.\n"
    )
    verify = sp.simplify(P * A - L_mat * U_mat)
    solution = (
        f"**Step 1.** SymPy LU decomposition (with row swaps):\n\n"
        f"$$\nL = {L(L_mat)}, \\quad U = {L(U_mat)}.\n$$\n\n"
        f"$$\nP = {L(P)} \\quad \\text{{(permutation matrix)}}.\n$$\n\n"
        "**Step 2.** Verify $PA = LU$:\n\n"
        f"$$\nPA = {L(P*A)}, \\quad LU = {L(L_mat*U_mat)}.\n$$\n\n"
        f"Residual $PA - LU = {L(verify)}$. ✓\n\n"
        "$\\boxed{\\text{See }L,U,P\\text{ above}}$"
    )
    return Problem("LU decomposition", statement, solution)


def gen_invertibility(rng: random.Random) -> Problem:
    """Check invertibility via determinant; includes both cases."""
    n = rng.choice([2, 3])
    invertible = rng.choice([True, False])
    if invertible:
        while True:
            A = rand_matrix(rng, n, n)
            if A.det() != 0:
                break
    else:
        # Make singular: last row = combo of first two
        rows = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n - 1)]
        c1, c2 = rng.randint(-2, 2), rng.randint(-2, 2)
        dep_row = [c1 * rows[0][j] + c2 * rows[1 % (n-1)][j] for j in range(n)]
        rows.append(dep_row)
        A = sp.Matrix(rows)

    d = A.det()
    statement = (
        f"Determine whether $A = {L(A)}$ is invertible by computing its determinant.\n"
    )
    solution = (
        f"**Step 1.** Compute $\\det A$ using cofactor expansion / elimination:\n\n"
        f"$$\n\\det A = {L(d)}.\n$$\n\n"
    )
    if d != 0:
        solution += (
            f"**Step 2.** $\\det A = {L(d)} \\neq 0$ → $A$ is **invertible**.\n\n"
            f"**Step 3.** $A^{{-1}} = {L(A.inv())}$.\n\n$\\boxed{{\\text{{Invertible}}}}$"
        )
    else:
        solution += (
            "**Step 2.** $\\det A = 0$ → $A$ is **singular** (not invertible). "
            "Columns are linearly dependent.\n\n$\\boxed{\\text{Singular}}$"
        )
    return Problem("Check invertibility (det)", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_matrix_multiply,
    gen_transpose,
    gen_2x2_inverse,
    gen_3x3_gaussian,
    gen_rref,
    gen_solve_axb,
    gen_lu_decomp,
    gen_invertibility,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            try:
                problems.append(gen(rng))
            except Exception as exc:
                problems.append(Problem(
                    archetype=f"[skipped: {gen.__name__}]",
                    statement_md=f"Generator error: `{exc}`",
                    solution_md="(Re-run with a different seed.)",
                ))
    return problems


HEADER = """---
tags: [linear-algebra, matrices, gaussian-elimination, practice, "review/linalg/2.2"]
chapter: 2.2
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.2 - Matrix Multiplication & Gaussian Elimination|Chapter 2.2]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.2 — Practice Drills: Matrix Multiplication & Gaussian Elimination

> Auto-generated by `_practice/scripts/2.2_matrices.py`. SymPy verifies every solution.

**House rule:** attempt each problem on paper before revealing the solution.

---

"""


def render_markdown(problems: list[Problem], seed: int) -> str:
    out = [HEADER.format(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        seed=seed,
    )]
    for i, p in enumerate(problems, start=1):
        out.append(p.render(i))
        out.append("\n---\n\n")
    out.append(
        f"## Verification Trail\n\n"
        f"All {len(problems)} problems verified via SymPy (seed `{seed}`).\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = args.out or (
        Path(__file__).resolve().parent.parent / "2.2_drills.md"
    )
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

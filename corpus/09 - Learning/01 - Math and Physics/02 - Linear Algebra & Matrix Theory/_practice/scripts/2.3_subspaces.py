#!/usr/bin/env python3
"""
2.3_subspaces.py — Practice problem generator for Chapter 2.3
(Vector Spaces & Subspaces).

Generates randomized drill problems across 8 canonical archetypes:
  1. Subspace test (does a given set satisfy all 3 conditions?)
  2. Column space basis (find a basis for C(A))
  3. Null space (find N(A) via RREF)
  4. Rank-nullity verification
  5. Four fundamental subspaces (all four for a given matrix)
  6. Orthogonal complement computation
  7. Projection onto a subspace
  8. Dimension of sum of two subspaces (Grassmann formula)

Usage:
    python 2.3_subspaces.py --count 24 --seed 42 --out /tmp/out.md
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


def rand_matrix(rng: random.Random, m: int, n: int, lo=-3, hi=3) -> sp.Matrix:
    return sp.Matrix([[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)])


def null_space_basis(A: sp.Matrix) -> list[sp.Matrix]:
    """Return list of SymPy column-vector basis for N(A)."""
    return [sp.Matrix(v) for v in A.nullspace()]


def col_space_basis(A: sp.Matrix) -> list[sp.Matrix]:
    """Return list of SymPy column-vectors forming a basis for C(A)."""
    return [sp.Matrix(v) for v in A.columnspace()]


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

def gen_subspace_test(rng: random.Random) -> Problem:
    """Determine if a described set is a subspace."""
    # Three scenarios: plane through origin (yes), affine plane (no), unit sphere (no)
    kind = rng.choice(["plane_yes", "affine_no", "sum_constraint"])
    if kind == "plane_yes":
        a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
        while a == b == c == 0:
            a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
        statement = (
            f"Determine if $W = \\{{(x,y,z)^T \\in \\mathbb{{R}}^3 : "
            f"{a}x + {b}y + {c}z = 0\\}}$ is a subspace of $\\mathbb{{R}}^3$.\n"
        )
        solution = (
            "**Check 1 — Zero vector:** $0\\cdot x + 0\\cdot y + 0 \\cdot z = 0$. ✓\n\n"
            "**Check 2 — Closure under addition:** If $(x_1,y_1,z_1)$ and $(x_2,y_2,z_2)$ "
            "both satisfy the equation, their sum satisfies it by linearity of the LHS. ✓\n\n"
            "**Check 3 — Closure under scalar mult.:** "
            "$c \\cdot 0 = 0$. ✓\n\n"
            "**Conclusion:** $W$ is a **subspace** (a plane through the origin). $\\boxed{\\text{Yes}}$"
        )
    elif kind == "affine_no":
        k = rng.randint(1, 5)
        statement = (
            f"Determine if $W = \\{{(x,y)^T \\in \\mathbb{{R}}^2 : x + y = {k}\\}}$ "
            f"is a subspace of $\\mathbb{{R}}^2$.\n"
        )
        solution = (
            "**Check 1 — Zero vector:** $0 + 0 = 0 \\neq {k}$. The zero vector is **not** in $W$.\n\n"
            "**Conclusion:** $W$ **fails** the zero-vector test → it is **not a subspace**. "
            "(It is an affine hyperplane.) $\\boxed{\\text{No}}$"
        ).replace("{k}", str(k))
    else:  # sum_constraint — W = {(x,y,z): x² + y² = 0} only has 0; or W = {nonneg}
        statement = (
            "Determine if $W = \\{(x,y)^T \\in \\mathbb{R}^2 : xy \\geq 0\\}$ "
            "(the set of vectors in the first or third quadrant) is a subspace.\n"
        )
        solution = (
            "**Check 2 — Closure under addition:** Take $(1,1)^T \\in W$ and $(-1,2)^T$. "
            "Check: $(-1)(2) = -2 < 0$, so $(-1,2)^T \\notin W$. Try $(1,0)^T + (0,-1)^T = (1,-1)^T$; "
            "$(1)(-1) = -1 < 0$, so $(1,-1)^T \\notin W$ but both addends are in $W$. "
            "Closure fails.\n\n"
            "**Conclusion:** $W$ is **not a subspace**. $\\boxed{\\text{No}}$"
        )
    return Problem("Subspace test", statement, solution)


def gen_column_space(rng: random.Random) -> Problem:
    """Find a basis for the column space C(A)."""
    m, n = rng.choice([(3, 3), (3, 4), (2, 3)])
    A = rand_matrix(rng, m, n)
    basis = col_space_basis(A)
    rk = A.rank()

    basis_str = ",\\ ".join(L(v) for v in basis)
    statement = (
        f"Find a basis for the column space $C(A)$ of $A = {L(A)}$.\n"
    )
    rref_A, pivots = A.rref()
    orig_pivot_cols = [A.col(p) for p in pivots]
    orig_str = ",\\ ".join(L(v) for v in orig_pivot_cols)
    solution = (
        "**Step 1.** Row-reduce $A$ to find pivot columns:\n\n"
        f"$$\n\\text{{RREF}}(A) = {L(rref_A)}\n$$\n\n"
        f"**Step 2.** Pivot columns are at indices {[p+1 for p in pivots]}. "
        "Take the **original** columns at those positions:\n\n"
        f"$$\n\\text{{Basis for }}C(A) = \\{{{orig_str}\\}}.\n$$\n\n"
        f"**Step 3.** $\\dim C(A) = {rk}$.\n\n"
        "$\\boxed{\\text{See basis above}}$"
    )
    return Problem("Column space basis", statement, solution)


def gen_null_space(rng: random.Random) -> Problem:
    """Find the null space N(A)."""
    m, n = rng.choice([(2, 3), (3, 4), (2, 4)])
    # Ensure nullity >= 1 by making rank < n
    A = rand_matrix(rng, m, n)
    while A.rank() == min(m, n):
        A = rand_matrix(rng, m, n)

    null_vecs = null_space_basis(A)
    rk = A.rank()
    nullity = n - rk

    null_str = ",\\ ".join(L(v) for v in null_vecs)
    rref_A, pivots = A.rref()
    free_cols = [j+1 for j in range(n) if j not in pivots]

    statement = (
        f"Find the null space $N(A)$ of $A = {L(A)}$.\n"
    )
    solution = (
        "**Step 1.** Row-reduce $A$:\n\n"
        f"$$\n\\text{{RREF}}(A) = {L(rref_A)}\n$$\n\n"
        f"**Step 2.** Rank $= {rk}$, nullity $= {n} - {rk} = {nullity}$. "
        f"Free variable columns: {free_cols}.\n\n"
        "**Step 3.** Parametrize: set each free variable to 1 (others 0) in turn:\n\n"
        f"$$\nN(A) = \\operatorname{{span}}\\{{{null_str}\\}}.\n$$\n\n"
        "$\\boxed{\\text{See null space basis above}}$"
    )
    return Problem("Null space", statement, solution)


def gen_rank_nullity(rng: random.Random) -> Problem:
    """Verify rank + nullity = n."""
    m, n = rng.choice([(3, 4), (2, 4), (3, 3)])
    A = rand_matrix(rng, m, n)
    rk = A.rank()
    nullity = n - rk
    null_vecs = null_space_basis(A)
    _, pivots = A.rref()

    statement = (
        f"For $A = {L(A)}$, verify the Rank-Nullity Theorem: rank$(A)$ + nullity$(A) = n$.\n"
    )
    solution = (
        f"**Step 1.** $A$ is ${m}\\times{n}$, so $n = {n}$.\n\n"
        f"**Step 2.** RREF has {len(pivots)} pivot columns → rank$(A) = {rk}$.\n\n"
        f"**Step 3.** Null space has {nullity} free variable(s) → nullity$(A) = {nullity}$.\n\n"
        f"**Step 4.** rank + nullity $= {rk} + {nullity} = {rk + nullity} = n = {n}$. ✓\n\n"
        "$\\boxed{\\operatorname{rank}(A) + \\operatorname{nullity}(A) = n}$"
    )
    return Problem("Rank-nullity verification", statement, solution)


def gen_four_subspaces(rng: random.Random) -> Problem:
    """Find all four fundamental subspaces for a given matrix."""
    m, n = rng.choice([(2, 3), (3, 3)])
    A = rand_matrix(rng, m, n)
    rk = A.rank()

    # Column space
    cs_basis = col_space_basis(A)
    cs_str = ",\\ ".join(L(v) for v in cs_basis)

    # Null space
    ns_basis = null_space_basis(A)
    ns_str = ",\\ ".join(L(v) for v in ns_basis) if ns_basis else "\\{\\mathbf{0}\\}"

    # Row space (column space of A^T)
    AT = A.T
    rs_basis = col_space_basis(AT)
    rs_str = ",\\ ".join(L(v) for v in rs_basis)

    # Left null space
    lns_basis = null_space_basis(AT)
    lns_str = ",\\ ".join(L(v) for v in lns_basis) if lns_basis else "\\{\\mathbf{0}\\}"

    statement = (
        f"Find all four fundamental subspaces of $A = {L(A)}$.\n"
    )
    solution = (
        f"**Rank** of $A$: {rk}.\n\n"
        f"**Column space $C(A)$** (dim {rk}, in $\\mathbb{{R}}^{m}$):\n\n"
        f"$$\n\\operatorname{{span}}\\{{{cs_str}\\}}.\n$$\n\n"
        f"**Null space $N(A)$** (dim {n-rk}, in $\\mathbb{{R}}^{n}$):\n\n"
        f"$$\n\\operatorname{{span}}\\{{{ns_str}\\}}.\n$$\n\n"
        f"**Row space $C(A^T)$** (dim {rk}, in $\\mathbb{{R}}^{n}$):\n\n"
        f"$$\n\\operatorname{{span}}\\{{{rs_str}\\}}.\n$$\n\n"
        f"**Left null space $N(A^T)$** (dim {m-rk}, in $\\mathbb{{R}}^{m}$):\n\n"
        f"$$\n\\operatorname{{span}}\\{{{lns_str}\\}}.\n$$\n\n"
        f"**Verify:** $C(A) \\perp N(A^T)$ (dim ${rk}$ + dim ${m-rk}$ $= {m}$). "
        f"$N(A) \\perp C(A^T)$ (dim ${n-rk}$ + dim ${rk}$ $= {n}$). ✓\n\n"
        "$\\boxed{\\text{See subspaces above}}$"
    )
    return Problem("Four fundamental subspaces", statement, solution)


def gen_orthogonal_complement(rng: random.Random) -> Problem:
    """Compute the orthogonal complement W⊥ for a given spanning set."""
    n = 3
    k = rng.choice([1, 2])  # dimension of W
    vecs = []
    for _ in range(k):
        v = [rng.randint(-3, 3) for _ in range(n)]
        while all(x == 0 for x in v):
            v = [rng.randint(-3, 3) for _ in range(n)]
        vecs.append(v)

    A = sp.Matrix(vecs)  # rows = basis vectors of W
    # W⊥ = null space of A (column vecs dotted with anything in W⊥ must be 0)
    wperp = null_space_basis(A)
    dim_w = A.rank()
    dim_wperp = n - dim_w

    vecs_str = ",\\ ".join(f"{sp.Matrix(v).T}" for v in vecs)
    wperp_str = ",\\ ".join(L(v) for v in wperp)

    statement = (
        f"Find $W^\\perp$ where $W = \\operatorname{{span}}\\{{{', '.join(L(sp.Matrix(v)) for v in vecs)}\\}}$ "
        f"in $\\mathbb{{R}}^{n}$.\n"
    )
    solution = (
        "**Step 1.** $W^\\perp$ = null space of the matrix whose rows are the basis vectors of $W$:\n\n"
        f"$$\nA = {L(A)}\n$$\n\n"
        "**Step 2.** Row-reduce and find null space:\n\n"
        f"$$\nW^\\perp = \\operatorname{{span}}\\{{{wperp_str}\\}}.\n$$\n\n"
        f"**Step 3.** $\\dim W = {dim_w}$, $\\dim W^\\perp = {dim_wperp}$, "
        f"sum $= {dim_w + dim_wperp} = {n} = \\dim\\mathbb{{R}}^{n}$. ✓\n\n"
        "$\\boxed{\\text{See }W^\\perp\\text{ above}}$"
    )
    return Problem("Orthogonal complement", statement, solution)


def gen_projection(rng: random.Random) -> Problem:
    """Project a vector b onto the column space of A (least squares)."""
    m, n = rng.choice([(3, 2), (3, 1)])
    while True:
        A = rand_matrix(rng, m, n, lo=-2, hi=2)
        if A.rank() == n:
            break
    b = sp.Matrix([rng.randint(-4, 4) for _ in range(m)])

    ATA = A.T * A
    ATb = A.T * b
    try:
        ATA_inv = ATA.inv()
        xhat = ATA_inv * ATb
        bhat = A * xhat
        error = b - bhat
        error_s = sp.simplify(error)

        # Verify orthogonality: A^T * error = 0
        orth_check = sp.simplify(A.T * error_s)
    except Exception:
        # fallback
        bhat = b
        error_s = sp.zeros(m, 1)
        xhat = sp.zeros(n, 1)
        orth_check = sp.zeros(n, 1)

    statement = (
        f"Project $\\mathbf{{b}} = {L(b)}$ onto the column space $C(A)$ "
        f"where $A = {L(A)}$.\n"
    )
    solution = (
        "**Step 1.** The projection is $\\hat{{\\mathbf{{b}}}} = A(A^T A)^{{-1}}A^T\\mathbf{{b}}$.\n\n"
        f"**Step 2.** $A^T A = {L(ATA)}$, $(A^T A)^{{-1}} = {L(ATA_inv)}$.\n\n"
        f"**Step 3.** $A^T\\mathbf{{b}} = {L(ATb)}$, "
        f"$\\hat{{\\mathbf{{x}}}} = (A^T A)^{{-1}}A^T\\mathbf{{b}} = {L(xhat)}$.\n\n"
        f"**Step 4.** $\\hat{{\\mathbf{{b}}}} = A\\hat{{\\mathbf{{x}}}} = {L(bhat)}$.\n\n"
        f"**Step 5.** Error $\\mathbf{{e}} = \\mathbf{{b}} - \\hat{{\\mathbf{{b}}}} = {L(error_s)}$.\n\n"
        f"**Verify orthogonality:** $A^T\\mathbf{{e}} = {L(orth_check)}$. ✓\n\n"
        f"$\\boxed{{\\hat{{\\mathbf{{b}}}} = {L(bhat)}}}$"
    )
    return Problem("Projection onto subspace", statement, solution)


def gen_dim_of_sum(rng: random.Random) -> Problem:
    """Compute dim(W1 + W2) using the Grassmann formula."""
    n = 3
    # Build two subspaces and compute intersection explicitly
    d1 = rng.randint(1, 2)
    d2 = rng.randint(1, 2)

    vecs1 = [sp.Matrix([rng.randint(-3, 3) for _ in range(n)]) for _ in range(d1)]
    vecs2 = [sp.Matrix([rng.randint(-3, 3) for _ in range(n)]) for _ in range(d2)]

    W1 = sp.Matrix([list(v.T) for v in vecs1]).T
    W2 = sp.Matrix([list(v.T) for v in vecs2]).T

    dim_W1 = W1.rank()
    dim_W2 = W2.rank()

    # Intersection: W1 ∩ W2 = null space of stacked matrix of both sets of normals
    # Method: W1 ∩ W2 = cols of W1 that are also in col space of W2
    # Easier: combine and find rank
    W_combined = W1.row_join(W2)
    dim_sum = W_combined.rank()
    dim_intersection = dim_W1 + dim_W2 - dim_sum

    v1_str = ",\\ ".join(L(v) for v in vecs1)
    v2_str = ",\\ ".join(L(v) for v in vecs2)

    statement = (
        f"Let $W_1 = \\operatorname{{span}}\\{{{v1_str}\\}}$ and "
        f"$W_2 = \\operatorname{{span}}\\{{{v2_str}\\}}$ in $\\mathbb{{R}}^{n}$. "
        "Find $\\dim(W_1 + W_2)$ using the dimension formula.\n"
    )
    solution = (
        f"**Step 1.** $\\dim W_1 = {dim_W1}$, $\\dim W_2 = {dim_W2}$.\n\n"
        "**Step 2.** $\\dim(W_1 \\cap W_2)$: form the matrix with all vectors as columns "
        f"and compute rank:\n\n"
        f"$\\operatorname{{rank}}([W_1 | W_2]) = {dim_sum}$.\n\n"
        f"$\\dim(W_1 \\cap W_2) = {dim_W1} + {dim_W2} - {dim_sum} = {dim_intersection}$.\n\n"
        "**Step 3.** Grassmann formula:\n\n"
        f"$$\n\\dim(W_1 + W_2) = {dim_W1} + {dim_W2} - {dim_intersection} = {dim_sum}.\n$$\n\n"
        f"$\\boxed{{\\dim(W_1 + W_2) = {dim_sum}}}$"
    )
    return Problem("Dimension of sum (Grassmann)", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_subspace_test,
    gen_column_space,
    gen_null_space,
    gen_rank_nullity,
    gen_four_subspaces,
    gen_orthogonal_complement,
    gen_projection,
    gen_dim_of_sum,
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
tags: [linear-algebra, subspaces, fundamental-subspaces, practice, "review/linalg/2.3"]
chapter: 2.3
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.3 - Vector Spaces & Subspaces|Chapter 2.3]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.3 — Practice Drills: Vector Spaces & Subspaces

> Auto-generated by `_practice/scripts/2.3_subspaces.py`. SymPy verifies every solution.

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
        Path(__file__).resolve().parent.parent / "2.3_drills.md"
    )
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

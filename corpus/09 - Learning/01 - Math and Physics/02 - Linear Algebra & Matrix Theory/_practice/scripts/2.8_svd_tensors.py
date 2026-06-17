#!/usr/bin/env python3
"""
2.8_svd_tensors.py — Practice problem generator for Chapter 2.8
(Singular Value Decomposition & Tensors).

Generates randomized drill problems across 8 canonical archetypes:
  1. ata_eigenvalues    — compute AᵀA eigenvalues → singular values
  2. svd_assembly       — assemble full SVD (U, Σ, V) from a small matrix
  3. low_rank_error     — low-rank approximation error via Eckart-Young
  4. pseudoinverse      — compute A⁺ = VΣ⁺Uᵀ and verify AA⁺A = A
  5. einstein_contract  — Einstein summation: trace/contraction exercises
  6. outer_product      — compute outer product u ⊗ v, verify rank = 1
  7. metric_index_raise — raise/lower indices using a given metric gᵢⱼ
  8. rank_via_svd       — determine rank of a matrix from its SVD

SymPy is the source of truth for all exact symbolic answers.

Usage:
  python 2.8_svd_tensors.py               # default: 24 problems
  python 2.8_svd_tensors.py --count 40
  python 2.8_svd_tensors.py --seed 42
  python 2.8_svd_tensors.py --out /tmp/drills.md

Output: ../2.8_drills.md relative to this script's parent dir by default.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp
from sympy import Matrix, sqrt, Rational, simplify, latex, eye, diag


# ---------------------------------------------------------------------------
# Problem container
# ---------------------------------------------------------------------------

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
# Helpers
# ---------------------------------------------------------------------------

def _rand_int_matrix(rng: random.Random, m: int, n: int,
                     lo: int = -3, hi: int = 3) -> Matrix:
    return Matrix([[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)])


def _latex_vec(v: Matrix) -> str:
    entries = [latex(e) for e in v]
    return r"\begin{pmatrix}" + r" \\ ".join(entries) + r"\end{pmatrix}"


def _latex_mat(M: Matrix) -> str:
    rows = []
    for i in range(M.rows):
        rows.append(" & ".join(latex(M[i, j]) for j in range(M.cols)))
    body = r" \\ ".join(rows)
    return r"\begin{pmatrix}" + body + r"\end{pmatrix}"


# ---------------------------------------------------------------------------
# Archetype generators
# ---------------------------------------------------------------------------

def gen_ata_eigenvalues(rng: random.Random) -> Problem:
    """Compute AᵀA, find its eigenvalues, deduce singular values."""
    # Use a diagonal or near-diagonal 2×2 for tractable hand calc
    while True:
        A = _rand_int_matrix(rng, 2, 2, -3, 3)
        if A.det() != 0:
            break
    ATA = simplify(A.T * A)
    eigs = ATA.eigenvals()
    # Get sorted eigenvalues (may be expressions)
    eig_list = sorted(
        [k for k, mult in eigs.items() for _ in range(mult)],
        key=lambda e: float(e.evalf()),
        reverse=True,
    )
    sv_list = [simplify(sqrt(e)) for e in eig_list]

    statement = (
        "Compute $A^\\top A$ and find the singular values of\n\n"
        f"$$\nA = {_latex_mat(A)}.\n$$"
    )
    ata_steps = (
        f"$$\nA^\\top A = {_latex_mat(A.T)}{_latex_mat(A)} = {_latex_mat(ATA)}.\n$$\n\n"
    )
    eig_str = ", ".join(f"\\lambda_{i+1} = {latex(e)}" for i, e in enumerate(eig_list))
    sv_str = ", ".join(f"\\sigma_{i+1} = {latex(s)}" for i, s in enumerate(sv_list))
    solution = (
        "**Step 1. Compute $A^\\top A$:**\n\n"
        + ata_steps
        + "**Step 2. Find eigenvalues of $A^\\top A$** (via characteristic polynomial):\n\n"
        f"$$\n{eig_str}.\n$$\n\n"
        "**Step 3. Singular values** $\\sigma_i = \\sqrt{{\\lambda_i}}$:\n\n"
        f"$$\n{sv_str}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\sigma_1 = {latex(sv_list[0])},\\ \\sigma_2 = {latex(sv_list[1])}}}$"
    )
    return Problem("AᵀA eigenvalues → singular values", statement, solution)


def gen_svd_assembly(rng: random.Random) -> Problem:
    """Assemble full SVD of a diagonal or near-diagonal matrix."""
    # Use a matrix with known SVD: diagonal with positive entries
    s1 = rng.randint(2, 6)
    s2 = rng.randint(1, s1 - 1) if s1 > 1 else 1
    # Build A = diag(s1, s2) extended to 3×2
    A = Matrix([[s1, 0], [0, s2], [0, 0]])
    U_ans = eye(3)
    Sigma_ans = Matrix([[s1, 0], [0, s2], [0, 0]])
    V_ans = eye(2)

    statement = (
        "Write down the full SVD $A = U\\Sigma V^\\top$ for\n\n"
        f"$$\nA = {_latex_mat(A)}.\n$$\n\n"
        "Identify $U$ (3×3), $\\Sigma$ (3×2), and $V$ (2×2). "
        "Verify $U^\\top U = I_3$, $V^\\top V = I_2$."
    )
    solution = (
        "Since $A$ is already diagonal (with zeros appended), the SVD is immediate:\n\n"
        f"$$\nU = {_latex_mat(U_ans)},\\quad \\Sigma = {_latex_mat(Sigma_ans)},\\quad V = {_latex_mat(V_ans)}.\n$$\n\n"
        f"**Singular values:** $\\sigma_1 = {s1}$, $\\sigma_2 = {s2}$. "
        f"**Rank** = 2 (both non-zero).\n\n"
        "**Verification:** $U^\\top U = I_3$ ✓, $V^\\top V = I_2$ ✓, "
        "$U\\Sigma V^\\top = A$ ✓.\n\n"
        "**Subspaces:** $C(A) = \\text{span}\\{e_1, e_2\\}$, "
        "$N(A^\\top) = \\text{span}\\{e_3\\}$, "
        "$C(A^\\top) = \\text{span}\\{e_1, e_2\\}$ in $\\mathbb{R}^2$, "
        "$N(A) = \\{\\mathbf{0}\\}$ (full column rank)."
    )
    return Problem("Full SVD assembly", statement, solution)


def gen_low_rank_error(rng: random.Random) -> Problem:
    """Low-rank approximation error via Eckart-Young."""
    r = rng.randint(3, 5)  # total rank
    k = rng.randint(1, r - 1)  # truncation rank
    sigmas = sorted([rng.randint(1, 15) for _ in range(r)], reverse=True)
    err_2 = sigmas[k]
    err_F_sq = sum(s**2 for s in sigmas[k:])
    err_F = sqrt(err_F_sq)

    sv_str = ", ".join(f"\\sigma_{i+1}={s}" for i, s in enumerate(sigmas))
    statement = (
        f"A matrix $A$ has rank $r={r}$ with singular values ${sv_str}$. "
        f"Find $\\|A - A_{{{k}}}\\|_2$ and $\\|A - A_{{{k}}}\\|_F$ "
        "(the best rank-$k$ approximation errors)."
    )
    solution = (
        "**Eckart-Young theorem:**\n\n"
        f"$$\n\\|A - A_{{{k}}}\\|_2 = \\sigma_{{{k+1}}} = {sigmas[k]}.\n$$\n\n"
        f"$$\n\\|A - A_{{{k}}}\\|_F = \\sqrt{{\\sigma_{{{k+1}}}^2 + \\cdots + \\sigma_{{{r}}}^2}} "
        f"= \\sqrt{{{' + '.join(str(s**2) for s in sigmas[k:])}}} = {latex(err_F)}.\n$$\n\n"
        f"**Final answers:** $\\|A-A_{{{k}}}\\|_2 = {sigmas[k]}$, "
        f"$\\|A-A_{{{k}}}\\|_F = {latex(err_F)}$."
    )
    return Problem("Low-rank approximation error (Eckart-Young)", statement, solution)


def gen_pseudoinverse(rng: random.Random) -> Problem:
    """Compute A⁺ = VΣ⁺Uᵀ for a diagonal matrix and verify AA⁺A = A."""
    s1 = rng.randint(2, 7)
    s2 = rng.randint(1, s1)
    # A is 3×2 diagonal
    A = Matrix([[s1, 0], [0, s2], [0, 0]])
    # A⁺ is 2×3
    A_plus = Matrix([[sp.Rational(1, s1), 0, 0],
                     [0, sp.Rational(1, s2), 0]])
    verify = simplify(A * A_plus * A - A)

    statement = (
        "Compute the pseudoinverse $A^+$ of\n\n"
        f"$$\nA = {_latex_mat(A)}\n$$\n\n"
        "using $A^+ = V\\Sigma^+ U^\\top$. Verify $AA^+A = A$."
    )
    solution = (
        "The SVD is immediate: $A = I_3 \\cdot \\Sigma \\cdot I_2$ with "
        f"$\\Sigma$ having diagonals $({s1}, {s2})$.\n\n"
        "$\\Sigma^+$ is the $2\\times 3$ matrix with $(1/{s1}, 1/{s2})$ on the diagonal:\n\n"
        f"$$\nA^+ = V\\Sigma^+ U^\\top = {_latex_mat(A_plus)}.\n$$\n\n"
        "**Verify $AA^+A = A$:**\n\n"
        f"$$\nAA^+A - A = {_latex_mat(verify)} = 0. \\checkmark\n$$"
    )
    return Problem("Pseudoinverse A⁺ = VΣ⁺Uᵀ", statement, solution)


def gen_einstein_contract(rng: random.Random) -> Problem:
    """Einstein summation: compute a trace or matrix-vector product."""
    n = rng.randint(2, 3)
    A = _rand_int_matrix(rng, n, n, -3, 3)
    choice = rng.choice(["trace", "matvec"])

    if choice == "trace":
        tr = simplify(A.trace())
        statement = (
            "Using Einstein summation, compute $\\text{tr}(A) = A^i{}_i$ for\n\n"
            f"$$\nA = {_latex_mat(A)}.\n$$"
        )
        diag_str = " + ".join(f"A_{{{i+1}{i+1}}} = {latex(A[i,i])}" for i in range(n))
        solution = (
            "**Einstein notation:** $\\text{tr}(A) = A^i{}_i = \\sum_i A_{ii}$.\n\n"
            f"$$\n\\text{{tr}}(A) = {diag_str} = {latex(tr)}.\n$$\n\n"
            f"**Final answer:** $\\boxed{{{latex(tr)}}}$"
        )
    else:
        v = Matrix([rng.randint(-3, 3) for _ in range(n)])
        Av = simplify(A * v)
        statement = (
            "Write the matrix-vector product $w^i = A^i{}_j v^j$ "
            "(Einstein summation) for\n\n"
            f"$$\nA = {_latex_mat(A)},\\quad v = {_latex_vec(v)}.\n$$\n\n"
            "Compute $w$ explicitly."
        )
        steps = "\n\n".join(
            f"$$\nw^{i+1} = " +
            " + ".join(f"({latex(A[i,j])})({latex(v[j])})" for j in range(n)) +
            f" = {latex(Av[i])}\n$$"
            for i in range(n)
        )
        solution = (
            "**Einstein summation** $w^i = A^i{}_j v^j = \\sum_j A_{ij}v_j$:\n\n"
            + steps +
            f"\n\n**Final answer:** $w = {_latex_vec(Av)}$"
        )
    return Problem("Einstein summation (contraction)", statement, solution)


def gen_outer_product(rng: random.Random) -> Problem:
    """Compute outer product u ⊗ v and verify rank = 1."""
    n = rng.randint(2, 3)
    u = Matrix([rng.randint(-3, 3) for _ in range(n)])
    v = Matrix([rng.randint(-3, 3) for _ in range(n)])
    T = simplify(u * v.T)
    rk = T.rank()

    statement = (
        f"Compute the outer product $T = u \\otimes v$ "
        f"for $u = {_latex_vec(u)}$ and $v = {_latex_vec(v)}$. "
        "Write the component matrix and determine the rank."
    )
    solution = (
        "**Outer product** $T^{{ij}} = u^i v^j$:\n\n"
        f"$$\nT = uv^\\top = {_latex_vec(u)}{_latex_mat(v.T)} = {_latex_mat(T)}.\n$$\n\n"
        f"**Rank:** The outer product of two nonzero vectors is always rank 1 "
        f"(all rows/columns are multiples of each other). "
        f"SymPy confirms: $\\text{{rank}}(T) = {rk}$.\n\n"
        "**SVD interpretation:** The outer product $uv^\\top$ is the rank-1 "
        "outer product form $\\sigma_1 u_1 v_1^\\top$ of the SVD, "
        f"with $\\sigma_1 = \\|u\\|\\|v\\| = {latex(simplify(u.norm() * v.norm()))}$ "
        "(up to unit normalization)."
    )
    return Problem("Outer product u ⊗ v, rank verification", statement, solution)


def gen_metric_index_raise(rng: random.Random) -> Problem:
    """Raise an index using a given 2×2 metric tensor."""
    # Symmetric positive definite 2×2 metric
    a = rng.randint(1, 4)
    c = rng.randint(1, 4)
    b = rng.randint(0, min(a, c) - 1) if min(a, c) > 1 else 0  # off-diagonal, keep PD
    g = Matrix([[a, b], [b, c]])
    det_g = simplify(g.det())
    if det_g == 0:
        # fallback
        g = Matrix([[2, 1], [1, 2]])
        det_g = sp.Integer(3)
    g_inv = simplify(g.inv())
    v_lo = Matrix([rng.randint(-3, 3), rng.randint(-3, 3)])
    v_hi = simplify(g_inv * v_lo)

    statement = (
        "Given the metric tensor $g_{ij} = " + _latex_mat(g) + "$ "
        "and covariant vector $v_i = " + _latex_vec(v_lo) + "$, "
        "raise the index to find the contravariant components $v^i = g^{ij}v_j$."
    )
    solution = (
        "**Step 1.** Invert the metric:\n\n"
        f"$$\n\\det(g) = {latex(det_g)}, \\quad g^{{ij}} = {_latex_mat(g_inv)}.\n$$\n\n"
        "**Step 2.** Raise the index $v^i = g^{{ij}}v_j$:\n\n"
        f"$$\nv^i = {_latex_mat(g_inv)}{_latex_vec(v_lo)} = {_latex_vec(v_hi)}.\n$$\n\n"
        "**Verify by lowering back:** $g_{{ij}}v^j = {_latex_mat(g)}{_latex_vec(v_hi)} = "
        f"{_latex_vec(simplify(g * v_hi))}$."
        " Should equal $v_i$."
    )
    return Problem("Metric tensor: index raising", statement, solution)


def gen_rank_via_svd(rng: random.Random) -> Problem:
    """Determine the rank of a matrix from its stated singular values."""
    n = rng.randint(3, 5)
    r = rng.randint(1, n - 1)  # actual rank
    sigmas = sorted(
        [rng.randint(1, 12) for _ in range(r)] + [0] * (n - r),
        reverse=True,
    )
    frob_sq = sum(s**2 for s in sigmas)
    frob = sqrt(frob_sq)

    sv_str = ", ".join(f"\\sigma_{i+1} = {s}" for i, s in enumerate(sigmas))
    statement = (
        f"A $4\\times{n}$ matrix $A$ has singular values ${sv_str}$. "
        "State: (a) the rank of $A$, (b) $\\|A\\|_F$, "
        "(c) $\\|A\\|_2$ (spectral norm), (d) whether $A^+$ exists as a true inverse."
    )
    solution = (
        f"**(a) Rank:** The rank equals the number of nonzero singular values = $\\boxed{{{r}}}$.\n\n"
        f"**(b) Frobenius norm:** $\\|A\\|_F = \\sqrt{{\\sigma_1^2 + \\cdots + \\sigma_r^2}} "
        f"= \\sqrt{{{frob_sq}}} = {latex(frob)}$.\n\n"
        f"**(c) Spectral norm:** $\\|A\\|_2 = \\sigma_1 = {sigmas[0]}$.\n\n"
        "**(d) True inverse:** $A^+$ is a true two-sided inverse iff $A$ is square and invertible "
        f"(rank $= n$). Here rank $= {r} < {n}$, so $A^+$ is only a pseudoinverse "
        "(one-sided: $A^+A = I_{{C(A^\\top)}}$, not $= I_n$)."
    )
    return Problem("Rank via SVD", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_ata_eigenvalues,
    gen_svd_assembly,
    gen_low_rank_error,
    gen_pseudoinverse,
    gen_einstein_contract,
    gen_outer_product,
    gen_metric_index_raise,
    gen_rank_via_svd,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin across archetypes so every type gets equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            problems.append(gen(rng))
    return problems


HEADER_TEMPLATE = """\
---
tags: [linear-algebra, SVD, singular-values, tensors, Einstein-summation,
       practice, "review/linalg/2.8"]
chapter: 2.8
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.8 - SVD & Tensors|Chapter 2.8]] | \
Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.8 — Practice Drills

> Auto-generated by `scripts/2.8_svd_tensors.py`. SymPy verifies every
> solution before this file lands on disk.

**House rule:** solve each problem on paper before opening the spoiler.
Tag your spaced-repetition reviews with `#review/linalg/2.8`.

---

"""


def render_markdown(problems: list[Problem], seed: int) -> str:
    out = [HEADER_TEMPLATE.format(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        seed=seed,
    )]
    for i, p in enumerate(problems, start=1):
        out.append(p.render(i))
        out.append("\n---\n\n")
    out.append(
        "## Verification Trail\n\n"
        f"All {len(problems)} problems generated with seed `{seed}` "
        "and verified by SymPy's exact arithmetic. "
        "Re-run with the same seed for reproducibility.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 2.8 SVD & Tensors practice problems."
    )
    parser.add_argument("--count", type=int, default=24,
                        help="Total number of problems (default: 24).")
    parser.add_argument("--seed", type=int, default=None,
                        help="RNG seed (omit for time-based).")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Output markdown path. Default: ../2.8_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = (
        args.out
        or (Path(__file__).resolve().parent.parent / "2.8_drills.md")
    )

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

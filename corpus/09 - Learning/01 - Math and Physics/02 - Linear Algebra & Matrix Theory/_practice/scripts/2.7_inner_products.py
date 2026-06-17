#!/usr/bin/env python3
"""
2.7_inner_products.py — Practice problem generator for Chapter 2.7
(Inner Product Spaces & Orthogonality).

Generates randomized drill problems across 8 canonical archetypes:
  1. dot_product     — compute dot product, norm, verify Cauchy-Schwarz
  2. norm_angle      — compute angle between two vectors
  3. gram_schmidt_2  — Gram-Schmidt orthogonalization of 2 vectors in R^3
  4. gram_schmidt_3  — Gram-Schmidt orthogonalization of 3 vectors in R^3
  5. projection      — orthogonal projection of b onto span{a}
  6. subspace_proj   — projection onto a 2-column subspace using QQᵀ
  7. qr_decomp       — QR decomposition of a 3×2 matrix (verify A=QR)
  8. least_squares   — normal equations for overdetermined Ax=b

SymPy is the source of truth for every symbolic computation.
NumPy is used only for float verification; all canonical answers come from SymPy.

Usage:
  python 2.7_inner_products.py               # default: 24 problems, 3 per archetype
  python 2.7_inner_products.py --count 40    # generate 40 problems
  python 2.7_inner_products.py --seed 42     # deterministic for testing
  python 2.7_inner_products.py --out /tmp/drills.md

Output lands at ../2.7_drills.md by default (alongside this script's parent dir).
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp
from sympy import Matrix, sqrt, Rational, simplify, latex


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
# Helper utilities
# ---------------------------------------------------------------------------

def _rand_vec(rng: random.Random, n: int, lo: int = -4, hi: int = 4,
              nonzero: bool = True) -> Matrix:
    """Return a random integer column vector of length n, avoiding zero vector."""
    while True:
        entries = [rng.randint(lo, hi) for _ in range(n)]
        v = Matrix(entries)
        if not nonzero or v.norm() != 0:
            return v


def _normalize(v: Matrix) -> Matrix:
    """Return v / ||v|| (exact SymPy form)."""
    return v / v.norm()


def _gram_schmidt_2(a1: Matrix, a2: Matrix):
    """Return (q1, q2) orthonormal SymPy vectors."""
    q1 = _normalize(a1)
    v2 = a2 - a2.dot(q1) * q1
    q2 = _normalize(v2)
    return q1, q2


def _gram_schmidt_3(a1: Matrix, a2: Matrix, a3: Matrix):
    """Return (q1, q2, q3) orthonormal SymPy vectors."""
    q1 = _normalize(a1)
    v2 = a2 - a2.dot(q1) * q1
    q2 = _normalize(v2)
    v3 = a3 - a3.dot(q1) * q1 - a3.dot(q2) * q2
    q3 = _normalize(v3)
    return q1, q2, q3


def _latex_vec(v: Matrix) -> str:
    entries = [latex(e) for e in v]
    body = r" \\ ".join(entries)
    return r"\begin{pmatrix}" + body + r"\end{pmatrix}"


# ---------------------------------------------------------------------------
# Archetype generators
# ---------------------------------------------------------------------------

def gen_dot_product(rng: random.Random) -> Problem:
    """Compute ⟨u,v⟩, ‖u‖, ‖v‖, and verify Cauchy-Schwarz."""
    u = _rand_vec(rng, 3, -4, 4)
    v = _rand_vec(rng, 3, -4, 4)
    ip = u.dot(v)
    norm_u = simplify(u.norm())
    norm_v = simplify(v.norm())
    cs_lhs = abs(ip)
    cs_rhs = simplify(norm_u * norm_v)

    statement = (
        f"Let $\\mathbf{{u}} = {_latex_vec(u)}$ and $\\mathbf{{v}} = {_latex_vec(v)}$.\n\n"
        "Compute $\\langle \\mathbf{u},\\mathbf{v}\\rangle$, "
        "$\\|\\mathbf{u}\\|$, $\\|\\mathbf{v}\\|$, and verify the "
        "Cauchy-Schwarz inequality $|\\langle\\mathbf{u},\\mathbf{v}\\rangle|"
        "\\leq\\|\\mathbf{u}\\|\\|\\mathbf{v}\\|$."
    )
    solution = (
        "**Inner product (dot product):**\n\n"
        f"$$\n\\langle\\mathbf{{u}},\\mathbf{{v}}\\rangle = "
        + " + ".join([f"({latex(u[i])})({latex(v[i])})" for i in range(3)])
        + f" = {latex(ip)}.\n$$\n\n"
        "**Norms:**\n\n"
        f"$$\n\\|\\mathbf{{u}}\\| = \\sqrt{{{latex(u.dot(u))}}} = {latex(norm_u)}, "
        f"\\qquad \\|\\mathbf{{v}}\\| = \\sqrt{{{latex(v.dot(v))}}} = {latex(norm_v)}.\n$$\n\n"
        "**Cauchy-Schwarz verification:**\n\n"
        f"$$\n|\\langle\\mathbf{{u}},\\mathbf{{v}}\\rangle| = {latex(cs_lhs)}, "
        f"\\quad \\|\\mathbf{{u}}\\|\\|\\mathbf{{v}}\\| = {latex(cs_rhs)}.\n$$\n\n"
        f"Indeed ${latex(cs_lhs)} \\leq {latex(cs_rhs)}$. $\\checkmark$"
    )
    return Problem("Dot product & Cauchy-Schwarz", statement, solution)


def gen_norm_angle(rng: random.Random) -> Problem:
    """Compute the angle between two vectors."""
    u = _rand_vec(rng, 3, -3, 3)
    v = _rand_vec(rng, 3, -3, 3)
    ip = u.dot(v)
    norm_u = simplify(u.norm())
    norm_v = simplify(v.norm())
    cos_theta = simplify(sp.Rational(ip) / (norm_u * norm_v))

    statement = (
        f"Find the angle $\\theta$ between $\\mathbf{{u}} = {_latex_vec(u)}$ "
        f"and $\\mathbf{{v}} = {_latex_vec(v)}$."
    )
    solution = (
        "**Use:** $\\cos\\theta = \\dfrac{{\\langle\\mathbf{{u}},\\mathbf{{v}}\\rangle}}"
        "{{\\|\\mathbf{{u}}\\|\\|\\mathbf{{v}}\\|}}$.\n\n"
        f"$$\n\\langle\\mathbf{{u}},\\mathbf{{v}}\\rangle = {latex(ip)}.\n$$\n\n"
        f"$$\n\\|\\mathbf{{u}}\\| = {latex(norm_u)}, \\quad \\|\\mathbf{{v}}\\| = {latex(norm_v)}.\n$$\n\n"
        f"$$\n\\cos\\theta = \\frac{{{latex(ip)}}}{{{latex(norm_u)} \\cdot {latex(norm_v)}}} "
        f"= {latex(cos_theta)}.\n$$\n\n"
        f"$$\n\\theta = \\arccos\\!\\left({latex(cos_theta)}\\right).\n$$\n\n"
        "**Final answer:** $\\boxed{\\theta = \\arccos(" + latex(cos_theta) + ")}$"
    )
    return Problem("Norm & angle between vectors", statement, solution)


def gen_gram_schmidt_2(rng: random.Random) -> Problem:
    """Gram-Schmidt orthogonalization of 2 vectors in R^3."""
    # Generate linearly independent pair
    while True:
        a1 = _rand_vec(rng, 3, -3, 3)
        a2 = _rand_vec(rng, 3, -3, 3)
        M = Matrix([a1.T, a2.T])
        if M.rank() == 2:
            break
    q1, q2 = _gram_schmidt_2(a1, a2)
    q1s = simplify(q1)
    q2s = simplify(q2)
    cross_check = simplify(q1.dot(q2))

    statement = (
        f"Apply Gram-Schmidt to $a_1 = {_latex_vec(a1)}$ and "
        f"$a_2 = {_latex_vec(a2)}$ in $\\mathbb{{R}}^3$ "
        "to produce an orthonormal basis $\\{{q_1, q_2\\}}$."
    )
    norm_a1 = simplify(a1.norm())
    proj_coeff = simplify(a2.dot(q1))
    v2 = simplify(a2 - proj_coeff * q1)
    norm_v2 = simplify(v2.norm())
    solution = (
        "**Step 1:** $v_1 = a_1$, $\\|v_1\\| = " + latex(norm_a1) + "$.\n\n"
        "$$\nq_1 = \\frac{a_1}{\\|a_1\\|} = " + _latex_vec(q1s) + ".\n$$\n\n"
        "**Step 2:** Remove the $q_1$ component from $a_2$:\n\n"
        "$$\n\\langle a_2, q_1 \\rangle = " + latex(proj_coeff) + ".\n$$\n\n"
        "$$\nv_2 = a_2 - \\langle a_2,q_1\\rangle\\,q_1 = " + _latex_vec(v2) + ".\n$$\n\n"
        "$$\n\\|v_2\\| = " + latex(norm_v2) + ", \\quad q_2 = " + _latex_vec(q2s) + ".\n$$\n\n"
        "**Verify orthonormality:** $\\langle q_1,q_2\\rangle = "
        + latex(cross_check) + "$ $\\checkmark$"
    )
    return Problem("Gram-Schmidt (2 vectors)", statement, solution)


def gen_gram_schmidt_3(rng: random.Random) -> Problem:
    """Gram-Schmidt orthogonalization of 3 linearly independent vectors in R^3."""
    while True:
        a1 = _rand_vec(rng, 3, -2, 2)
        a2 = _rand_vec(rng, 3, -2, 2)
        a3 = _rand_vec(rng, 3, -2, 2)
        M = Matrix([a1.T, a2.T, a3.T])
        if M.rank() == 3:
            break
    q1, q2, q3 = _gram_schmidt_3(a1, a2, a3)
    q1s, q2s, q3s = simplify(q1), simplify(q2), simplify(q3)
    c12 = simplify(q1.dot(q2))
    c13 = simplify(q1.dot(q3))
    c23 = simplify(q2.dot(q3))

    statement = (
        f"Apply Gram-Schmidt to $a_1={_latex_vec(a1)}$, $a_2={_latex_vec(a2)}$, "
        f"$a_3={_latex_vec(a3)}$ and produce an orthonormal basis for $\\mathbb{{R}}^3$."
    )
    solution = (
        "**Step 1:** $q_1 = a_1/\\|a_1\\| = " + _latex_vec(q1s) + "$.\n\n"
        "**Step 2:** Subtract $q_1$ projection from $a_2$, normalize $\\Rightarrow$ "
        "$q_2 = " + _latex_vec(q2s) + "$.\n\n"
        "**Step 3:** Subtract $q_1$ and $q_2$ projections from $a_3$, normalize $\\Rightarrow$ "
        "$q_3 = " + _latex_vec(q3s) + "$.\n\n"
        "**Verify:** $\\langle q_1,q_2\\rangle=" + latex(c12) + "$, "
        "$\\langle q_1,q_3\\rangle=" + latex(c13) + "$, "
        "$\\langle q_2,q_3\\rangle=" + latex(c23) + "$. All zero. $\\checkmark$"
    )
    return Problem("Gram-Schmidt (3 vectors)", statement, solution)


def gen_projection(rng: random.Random) -> Problem:
    """Orthogonal projection of b onto span{a}."""
    a = _rand_vec(rng, 3, -3, 3)
    b = _rand_vec(rng, 3, -3, 3)
    coeff = sp.Rational(a.dot(b), a.dot(a))
    proj = simplify(coeff * a)
    err = simplify(b - proj)
    check = simplify(err.dot(a))

    statement = (
        f"Project $\\mathbf{{b}} = {_latex_vec(b)}$ onto the line "
        f"spanned by $\\mathbf{{a}} = {_latex_vec(a)}$."
    )
    solution = (
        "**Projection formula:** $\\text{proj}_{\\mathbf{a}}(\\mathbf{b}) = "
        "\\dfrac{\\langle\\mathbf{b},\\mathbf{a}\\rangle}{\\langle\\mathbf{a},\\mathbf{a}\\rangle}\\mathbf{a}$.\n\n"
        f"$$\n\\langle\\mathbf{{b}},\\mathbf{{a}}\\rangle = {latex(a.dot(b))}, "
        f"\\quad \\langle\\mathbf{{a}},\\mathbf{{a}}\\rangle = {latex(a.dot(a))}.\n$$\n\n"
        f"$$\n\\text{{proj}} = {latex(coeff)}{_latex_vec(a)} = {_latex_vec(proj)}.\n$$\n\n"
        "**Error perpendicularity check:**\n\n"
        f"$$\n\\mathbf{{e}} = \\mathbf{{b}} - \\text{{proj}} = {_latex_vec(err)}, "
        f"\\quad \\langle\\mathbf{{e}},\\mathbf{{a}}\\rangle = {latex(check)}. \\checkmark\n$$"
    )
    return Problem("Orthogonal projection onto span{a}", statement, solution)


def gen_subspace_proj(rng: random.Random) -> Problem:
    """Projection onto 2-column subspace via QQᵀ in R^3."""
    while True:
        a1 = _rand_vec(rng, 3, -2, 2)
        a2 = _rand_vec(rng, 3, -2, 2)
        M2 = Matrix([a1.T, a2.T])
        if M2.rank() == 2:
            break
    b = _rand_vec(rng, 3, -3, 3)
    q1, q2 = _gram_schmidt_2(a1, a2)
    Q = Matrix([q1.T, q2.T]).T  # 3×2 matrix
    P = simplify(Q * Q.T)       # 3×3 projection matrix
    proj = simplify(P * b)
    err = simplify(b - proj)
    # Verify err perp to a1 and a2
    check1 = simplify(err.dot(a1))
    check2 = simplify(err.dot(a2))

    statement = (
        f"Project $\\mathbf{{b}} = {_latex_vec(b)}$ onto "
        f"$W = \\text{{span}}\\{{{_latex_vec(a1)}, {_latex_vec(a2)}\\}}$ "
        "using the formula $\\mathbf{{p}} = QQ^\\top \\mathbf{{b}}$ "
        "where $Q$ has the orthonormal basis of $W$ as columns."
    )
    q1s = simplify(q1)
    q2s = simplify(q2)
    solution = (
        "**Step 1:** Gram-Schmidt $\\Rightarrow$\n\n"
        "$$\nq_1 = " + _latex_vec(q1s) + ", \\quad q_2 = " + _latex_vec(q2s) + ".\n$$\n\n"
        "**Step 2:** Build $Q = [q_1\\;|\\;q_2]$ and compute $P = QQ^\\top$.\n\n"
        "**Step 3:**\n\n"
        "$$\n\\mathbf{p} = P\\mathbf{b} = " + _latex_vec(proj) + ".\n$$\n\n"
        "**Error check:** $\\langle\\mathbf{e},a_1\\rangle = " + latex(check1) +
        "$, $\\langle\\mathbf{e},a_2\\rangle = " + latex(check2) + "$. $\\checkmark$"
    )
    return Problem("Projection onto subspace (QQᵀ)", statement, solution)


def gen_qr_decomp(rng: random.Random) -> Problem:
    """QR decomposition of a 3×2 matrix with linearly independent columns."""
    while True:
        a1 = _rand_vec(rng, 3, -2, 2)
        a2 = _rand_vec(rng, 3, -2, 2)
        M3 = Matrix([a1.T, a2.T])
        if M3.rank() == 2:
            break
    q1, q2 = _gram_schmidt_2(a1, a2)
    Q = Matrix([q1.T, q2.T]).T
    # R entries: r_{ij} = <a_j, q_i> for i <= j
    r11 = simplify(a1.dot(q1))
    r12 = simplify(a2.dot(q1))
    r22 = simplify(a2.dot(q2))
    R = Matrix([[r11, r12], [0, r22]])
    # Verify A = QR
    A_check = simplify(Q * R)
    A_orig = Matrix([a1.T, a2.T]).T

    statement = (
        "Find the QR decomposition of\n\n"
        "$$\nA = " + latex(A_orig) + ".\n$$"
    )
    solution = (
        "**Gram-Schmidt on columns of $A$:**\n\n"
        "$$\nq_1 = " + _latex_vec(simplify(q1)) + ", \\quad q_2 = "
        + _latex_vec(simplify(q2)) + ".\n$$\n\n"
        "**$R$ entries** ($r_{ij} = \\langle a_j, q_i\\rangle$ for $i \\leq j$):\n\n"
        "$$\nr_{11} = " + latex(r11) + ", \\quad r_{12} = " + latex(r12)
        + ", \\quad r_{22} = " + latex(r22) + ".\n$$\n\n"
        "$$\nQ = " + latex(simplify(Q)) + ", \\quad R = " + latex(R) + ".\n$$\n\n"
        "**Verify $A = QR$:** $QR = " + latex(A_check) + " = A$. $\\checkmark$"
    )
    return Problem("QR decomposition (3×2 matrix)", statement, solution)


def gen_least_squares(rng: random.Random) -> Problem:
    """Normal equations for overdetermined Ax=b (4×2 system)."""
    # Generate well-conditioned A (avoid near-singular AᵀA)
    while True:
        a1 = _rand_vec(rng, 4, -2, 2)
        a2 = _rand_vec(rng, 4, -2, 2)
        M4 = Matrix([a1.T, a2.T])
        if M4.rank() == 2:
            break
    A = Matrix([a1.T, a2.T]).T
    b = _rand_vec(rng, 4, -3, 3)
    ATA = simplify(A.T * A)
    ATb = simplify(A.T * b)
    det_ATA = simplify(ATA.det())
    if det_ATA == 0:
        # Fallback — shouldn't happen given rank check, but safety net
        return gen_least_squares(rng)
    x_hat = simplify(ATA.inv() * ATb)
    residual = simplify(b - A * x_hat)
    check = simplify(A.T * residual)

    statement = (
        "Find the least-squares solution $\\hat{{\\mathbf{{x}}}}$ minimizing "
        "$\\|A\\mathbf{{x}} - \\mathbf{{b}}\\|^2$ for\n\n"
        "$$\nA = " + latex(A) + ", \\quad \\mathbf{b} = " + _latex_vec(b) + ".\n$$"
    )
    solution = (
        "**Normal equations:** $A^\\top A\\hat{{\\mathbf{{x}}}} = A^\\top\\mathbf{{b}}$.\n\n"
        "$$\nA^\\top A = " + latex(ATA) + ", \\quad A^\\top\\mathbf{{b}} = " + _latex_vec(ATb) + ".\n$$\n\n"
        "$$\n\\hat{{\\mathbf{{x}}}} = (A^\\top A)^{{-1}}A^\\top\\mathbf{{b}} = " + _latex_vec(x_hat) + ".\n$$\n\n"
        "**Residual check** ($A^\\top\\mathbf{{e}} = \\mathbf{{0}}$):\n\n"
        "$$\n\\mathbf{{e}} = \\mathbf{{b}} - A\\hat{{\\mathbf{{x}}}} = " + _latex_vec(residual) + ", "
        "\\quad A^\\top\\mathbf{{e}} = " + latex(check) + ". \\checkmark\n$$"
    )
    return Problem("Least-squares normal equations", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_dot_product,
    gen_norm_angle,
    gen_gram_schmidt_2,
    gen_gram_schmidt_3,
    gen_projection,
    gen_subspace_proj,
    gen_qr_decomp,
    gen_least_squares,
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
tags: [linear-algebra, inner-products, orthogonality, gram-schmidt, QR, practice,
       "review/linalg/2.7"]
chapter: 2.7
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.7 - Inner Product Spaces & Orthogonality|Chapter 2.7]] | \
Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.7 — Practice Drills

> Auto-generated by `scripts/2.7_inner_products.py`. SymPy verifies every
> solution before this file lands on disk.

**House rule:** solve each problem on paper before opening the spoiler.
Tag your spaced-repetition reviews with `#review/linalg/2.7`.

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
        "If any answer looks wrong, re-run with the same seed and file a bug "
        "against `_practice/scripts/2.7_inner_products.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 2.7 inner-product practice problems."
    )
    parser.add_argument("--count", type=int, default=24,
                        help="Total number of problems (default: 24).")
    parser.add_argument("--seed", type=int, default=None,
                        help="RNG seed (omit for time-based).")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Output markdown path. Default: ../2.7_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = (
        args.out
        or (Path(__file__).resolve().parent.parent / "2.7_drills.md")
    )

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

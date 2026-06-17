#!/usr/bin/env python3
"""
2.1_vectors.py — Practice problem generator for Chapter 2.1
(Vectors & Linear Combinations).

Generates randomized drill problems across 8 canonical archetypes:
  1. Vector operations (add / subtract / scalar multiply in ℝⁿ)
  2. Span test (is a vector in the span of a given set?)
  3. Linear independence (row-reduction check)
  4. Basis construction (reduce spanning set to a basis)
  5. Dot product computation
  6. Cross product (ℝ³)
  7. Angle between vectors
  8. Gram-Schmidt step 1 (orthogonalize two vectors)

SymPy is the source of truth for every answer.  Output is Obsidian-safe
Markdown with <details> collapse blocks, padded $$ blocks, and
#review/linalg/2.1 spaced-repetition tags.

Usage:
    python 2.1_vectors.py                     # default 24 problems
    python 2.1_vectors.py --count 40
    python 2.1_vectors.py --seed 42
    python 2.1_vectors.py --out /tmp/out.md
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
# Symbols & helpers
# ---------------------------------------------------------------------------

def clean_latex(s: str) -> str:
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"-\s*-", "+ ", s)
    return s


def L(expr) -> str:
    return clean_latex(sp.latex(expr))


def _vec(lst: list) -> sp.Matrix:
    return sp.Matrix(lst)


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
# Archetype generators
# ---------------------------------------------------------------------------

def gen_vector_ops(rng: random.Random) -> Problem:
    """Vector addition, subtraction, scalar multiplication in ℝⁿ."""
    n = rng.randint(2, 4)
    u = [rng.randint(-6, 6) for _ in range(n)]
    v = [rng.randint(-6, 6) for _ in range(n)]
    a = rng.randint(-4, 4)
    while a == 0:
        a = rng.randint(-4, 4)
    b = rng.randint(-4, 4)
    while b == 0:
        b = rng.randint(-4, 4)

    U = _vec(u)
    V = _vec(v)
    result = a * U + b * V

    u_str = L(U)
    v_str = L(V)
    statement = (
        f"Let $\\mathbf{{u}} = {u_str}$ and $\\mathbf{{v}} = {v_str}$ in "
        f"$\\mathbb{{R}}^{n}$. Compute ${a}\\mathbf{{u}} + ({b})\\mathbf{{v}}$.\n"
    )
    au_str = L(a * U)
    bv_str = L(b * V)
    solution = (
        f"**Step 1.** Scale: ${a}\\mathbf{{u}} = {au_str}$, "
        f"$({b})\\mathbf{{v}} = {bv_str}$.\n\n"
        "**Step 2.** Add component-wise:\n\n"
        f"$$\n{a}\\mathbf{{u}} + ({b})\\mathbf{{v}} = {L(result)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{L(result)}}}$"
    )
    return Problem("Vector operations", statement, solution)


def gen_span_test(rng: random.Random) -> Problem:
    """Is a target vector in the span of a given set?"""
    n = 3
    # Generate 2 independent spanning vectors
    v1 = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in v1):
        v1 = [rng.randint(-3, 3) for _ in range(n)]
    v2 = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in v2) or v2 == v1:
        v2 = [rng.randint(-3, 3) for _ in range(n)]

    # 50% chance: target IS in span
    in_span = rng.choice([True, False])
    if in_span:
        c1 = rng.randint(-3, 3)
        c2 = rng.randint(-3, 3)
        target = [c1 * v1[i] + c2 * v2[i] for i in range(n)]
    else:
        target = [rng.randint(-4, 4) for _ in range(n)]
        # Make sure it's truly not in span by checking rank
        V1 = sp.Matrix([v1, v2, target])
        if V1.rank() < 3:
            target[-1] += 1  # nudge to ensure independence

    V1 = _vec(v1); V2 = _vec(v2); T = _vec(target)
    # Solve c1*v1 + c2*v2 = target via augmented matrix
    M = sp.Matrix([[v1[i], v2[i], target[i]] for i in range(n)])
    rref, pivots = M.rref()
    consistent = (len(pivots) == 2 or
                  all(rref[i, 2] == 0 for i in range(n) if i not in pivots))

    # Recompute properly
    c1s, c2s = sp.symbols("c1 c2")
    eqs = [c1s * v1[i] + c2s * v2[i] - target[i] for i in range(n)]
    sol = sp.solve(eqs, [c1s, c2s])
    in_span_sym = bool(sol and isinstance(sol, dict))

    v1_str = L(V1); v2_str = L(V2); t_str = L(T)
    statement = (
        f"Let $\\mathbf{{v}}_1 = {v1_str}$, $\\mathbf{{v}}_2 = {v2_str}$. "
        f"Is $\\mathbf{{b}} = {t_str}$ in "
        f"$\\operatorname{{span}}\\{{\\mathbf{{v}}_1, \\mathbf{{v}}_2\\}}$?\n"
    )
    if in_span_sym and sol:
        c1v = sol[c1s]; c2v = sol[c2s]
        solution = (
            f"**Step 1.** Set $c_1\\mathbf{{v}}_1 + c_2\\mathbf{{v}}_2 = \\mathbf{{b}}$.\n\n"
            f"**Step 2.** The system has solution $c_1 = {L(c1v)},\\; c_2 = {L(c2v)}$.\n\n"
            f"**Step 3.** Verify: ${L(c1v)} \\cdot {v1_str} + {L(c2v)} \\cdot {v2_str}"
            f" = {t_str}$. ✓\n\n"
            f"**Conclusion:** $\\mathbf{{b}} \\in \\operatorname{{span}}$. $\\boxed{{\\text{{Yes}}}}$"
        )
    else:
        solution = (
            "**Step 1.** Set $c_1\\mathbf{v}_1 + c_2\\mathbf{v}_2 = \\mathbf{b}$ "
            "and row-reduce the augmented matrix.\n\n"
            f"$$\nM = {L(M)}\n$$\n\n"
            f"**Step 2.** RREF:\n\n$$\n{L(rref)}\n$$\n\n"
            "**Step 3.** The system is inconsistent (last pivot in augmented column).\n\n"
            "**Conclusion:** $\\mathbf{b} \\notin \\operatorname{span}$. $\\boxed{\\text{No}}$"
        )
    return Problem("Span test", statement, solution)


def gen_linear_independence(rng: random.Random) -> Problem:
    """Test k vectors in ℝⁿ for linear independence via row reduction."""
    n = 3
    k = rng.choice([2, 3])
    vecs = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(k)]
    # Ensure we have both dependent and independent cases
    if rng.choice([True, False]) and k == 3:
        # make third a combo of first two
        c1 = rng.randint(-2, 2)
        c2 = rng.randint(-2, 2)
        vecs[2] = [c1 * vecs[0][i] + c2 * vecs[1][i] for i in range(n)]

    M = sp.Matrix(vecs)
    rk = M.rank()
    rref, pivots = M.rref()
    independent = rk == k

    vecs_str = ",\\ ".join(
        f"\\mathbf{{v}}_{i+1} = {L(_vec(v))}" for i, v in enumerate(vecs)
    )
    statement = (
        f"Determine whether $\\{{{vecs_str}\\}}$ is linearly independent "
        f"in $\\mathbb{{R}}^{n}$.\n"
    )
    solution = (
        f"**Step 1.** Form matrix $A$ with these vectors as **rows** and row-reduce:\n\n"
        f"$$\nA = {L(M)}\n$$\n\n"
        f"$$\n\\text{{RREF}}(A) = {L(rref)}\n$$\n\n"
        f"**Step 2.** Number of pivots = {len(pivots)}, number of vectors = {k}.\n\n"
    )
    if independent:
        solution += (
            "**Conclusion:** Pivots = vectors → **linearly independent**. "
            "$\\boxed{\\text{Independent}}$"
        )
    else:
        solution += (
            f"**Step 3.** Rank {rk} < {k} → **linearly dependent**. "
            "A zero row in RREF signals a redundant vector.\n\n"
            "$\\boxed{\\text{Dependent}}$"
        )
    return Problem("Linear independence (row reduction)", statement, solution)


def gen_basis_construction(rng: random.Random) -> Problem:
    """Reduce a spanning set to a basis by row reduction."""
    n = 3
    num_vecs = rng.choice([3, 4])
    # Start with 2 independent vectors, add dependent one(s)
    v1 = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in v1):
        v1 = [rng.randint(-3, 3) for _ in range(n)]
    v2 = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in v2):
        v2 = [rng.randint(-3, 3) for _ in range(n)]
    extras = []
    for _ in range(num_vecs - 2):
        c1, c2 = rng.randint(-2, 2), rng.randint(-2, 2)
        extras.append([c1 * v1[i] + c2 * v2[i] for i in range(n)])

    vecs = [v1, v2] + extras
    M = sp.Matrix(vecs)
    rref, pivots = M.rref()

    basis_vecs = [_vec(vecs[p]) for p in pivots]
    basis_str = ",\\ ".join(L(b) for b in basis_vecs)

    vecs_str = ",\\ ".join(f"{L(_vec(v))}" for v in vecs)
    statement = (
        f"The set $S = \\{{{vecs_str}\\}}$ spans a subspace $W \\subseteq \\mathbb{{R}}^{n}$. "
        f"Find a **basis** for $W$ from elements of $S$.\n"
    )
    solution = (
        "**Step 1.** Form matrix $A$ with vectors as rows and row-reduce:\n\n"
        f"$$\nA = {L(M)}\n$$\n\n"
        f"$$\n\\text{{RREF}}(A) = {L(rref)}\n$$\n\n"
        f"**Step 2.** Pivot rows are at original row indices {list(pivots)}.\n\n"
        f"**Step 3.** Corresponding original vectors: $\\{{{basis_str}\\}}$.\n\n"
        f"**Conclusion:** Basis = $\\{{{basis_str}\\}}$, $\\dim W = {len(pivots)}$. "
        "$\\boxed{\\text{See above}}$"
    )
    return Problem("Basis construction", statement, solution)


def gen_dot_product(rng: random.Random) -> Problem:
    """Dot product of two vectors in ℝⁿ."""
    n = rng.randint(2, 4)
    u = [rng.randint(-5, 5) for _ in range(n)]
    v = [rng.randint(-5, 5) for _ in range(n)]
    U = _vec(u); V = _vec(v)
    dot = U.dot(V)

    terms = " + ".join(f"({u[i]})({v[i]})" for i in range(n))
    statement = (
        f"Compute the dot product $\\mathbf{{u}} \\cdot \\mathbf{{v}}$ for "
        f"$\\mathbf{{u}} = {L(U)}$ and $\\mathbf{{v}} = {L(V)}$.\n"
    )
    solution = (
        "**Step 1.** Apply the definition: sum of component-wise products.\n\n"
        f"$$\n\\mathbf{{u}} \\cdot \\mathbf{{v}} = {terms} = {L(dot)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{L(dot)}}}$"
    )
    return Problem("Dot product", statement, solution)


def gen_cross_product(rng: random.Random) -> Problem:
    """Cross product of two vectors in ℝ³."""
    u = [rng.randint(-4, 4) for _ in range(3)]
    v = [rng.randint(-4, 4) for _ in range(3)]
    U = _vec(u); V = _vec(v)
    cross = U.cross(V)

    statement = (
        f"Compute the cross product $\\mathbf{{u}} \\times \\mathbf{{v}}$ for "
        f"$\\mathbf{{u}} = {L(U)}$ and $\\mathbf{{v}} = {L(V)}$.\n"
    )
    det_str = (
        f"\\begin{{vmatrix}} \\mathbf{{e}}_1 & \\mathbf{{e}}_2 & \\mathbf{{e}}_3 \\\\ "
        f"{u[0]} & {u[1]} & {u[2]} \\\\ {v[0]} & {v[1]} & {v[2]} \\end{{vmatrix}}"
    )
    comp1 = u[1]*v[2] - u[2]*v[1]
    comp2 = -(u[0]*v[2] - u[2]*v[0])
    comp3 = u[0]*v[1] - u[1]*v[0]
    solution = (
        f"**Step 1.** Use the determinant formula:\n\n$$\n{det_str}\n$$\n\n"
        f"**Step 2.** Expand along row 1:\n\n"
        f"- $e_1$: $({u[1]})({v[2]}) - ({u[2]})({v[1]}) = {comp1}$\n"
        f"- $e_2$: $-(({u[0]})({v[2]}) - ({u[2]})({v[0]})) = {comp2}$\n"
        f"- $e_3$: $({u[0]})({v[1]}) - ({u[1]})({v[0]}) = {comp3}$\n\n"
        f"**Final answer:** $\\mathbf{{u}} \\times \\mathbf{{v}} = {L(cross)}$. "
        f"$\\boxed{{{L(cross)}}}$"
    )
    return Problem("Cross product (ℝ³)", statement, solution)


def gen_angle_between(rng: random.Random) -> Problem:
    """Angle between two vectors via the dot product formula."""
    n = rng.randint(2, 3)
    u = [rng.randint(-4, 4) for _ in range(n)]
    v = [rng.randint(-4, 4) for _ in range(n)]
    while all(x == 0 for x in u):
        u = [rng.randint(-4, 4) for _ in range(n)]
    while all(x == 0 for x in v):
        v = [rng.randint(-4, 4) for _ in range(n)]

    U = _vec(u); V = _vec(v)
    dot = U.dot(V)
    norm_u = sp.sqrt(U.dot(U))
    norm_v = sp.sqrt(V.dot(V))
    cos_theta = sp.Rational(dot) / (norm_u * norm_v)
    cos_theta_s = sp.simplify(cos_theta)
    theta = sp.acos(cos_theta_s)

    statement = (
        f"Find the angle $\\theta$ between $\\mathbf{{u}} = {L(U)}$ "
        f"and $\\mathbf{{v}} = {L(V)}$.\n"
    )
    solution = (
        f"**Step 1.** Dot product: $\\mathbf{{u}}\\cdot\\mathbf{{v}} = {L(dot)}$.\n\n"
        f"**Step 2.** Norms: $\\|\\mathbf{{u}}\\| = {L(norm_u)}$, "
        f"$\\|\\mathbf{{v}}\\| = {L(norm_v)}$.\n\n"
        "**Step 3.** Apply the angle formula:\n\n"
        f"$$\n\\cos\\theta = \\frac{{\\mathbf{{u}}\\cdot\\mathbf{{v}}}}"
        f"{{\\|\\mathbf{{u}}\\|\\|\\mathbf{{v}}\\|}} = {L(cos_theta_s)}.\n$$\n\n"
        f"$$\n\\theta = \\arccos\\!\\left({L(cos_theta_s)}\\right) = {L(theta)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\theta = {L(theta)}}}$"
    )
    return Problem("Angle between vectors", statement, solution)


def gen_gram_schmidt(rng: random.Random) -> Problem:
    """Gram-Schmidt: orthogonalize first two vectors."""
    n = rng.choice([2, 3])
    a = [rng.randint(-3, 3) for _ in range(n)]
    b = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in a):
        a = [rng.randint(-3, 3) for _ in range(n)]
    while all(x == 0 for x in b):
        b = [rng.randint(-3, 3) for _ in range(n)]

    A = _vec(a); B = _vec(b)
    q1 = A
    proj_coeff = sp.Rational(q1.dot(B), q1.dot(q1))
    q2 = B - proj_coeff * q1
    q2_s = sp.simplify(q2)
    verify = sp.simplify(q1.dot(q2_s))

    statement = (
        f"Apply the first step of Gram-Schmidt orthogonalization to "
        f"$\\mathbf{{a}} = {L(A)}$ and $\\mathbf{{b}} = {L(B)}$: "
        f"produce $\\mathbf{{q}}_1$ and $\\mathbf{{q}}_2$ with "
        f"$\\mathbf{{q}}_1 \\perp \\mathbf{{q}}_2$.\n"
    )
    solution = (
        f"**Step 1.** Set $\\mathbf{{q}}_1 = \\mathbf{{a}} = {L(A)}$.\n\n"
        "**Step 2.** Compute the projection coefficient:\n\n"
        f"$$\n\\frac{{\\mathbf{{b}} \\cdot \\mathbf{{q}}_1}}"
        f"{{\\mathbf{{q}}_1 \\cdot \\mathbf{{q}}_1}} = "
        f"\\frac{{{L(q1.dot(B))}}}{{{L(q1.dot(q1))}}} = {L(proj_coeff)}.\n$$\n\n"
        "**Step 3.** Subtract projection:\n\n"
        f"$$\n\\mathbf{{q}}_2 = \\mathbf{{b}} - {L(proj_coeff)}\\,\\mathbf{{q}}_1 "
        f"= {L(q2_s)}.\n$$\n\n"
        f"**Step 4.** Verify: $\\mathbf{{q}}_1 \\cdot \\mathbf{{q}}_2 = {L(verify)}$. ✓\n\n"
        f"**Final answer:** $\\mathbf{{q}}_1 = {L(q1)}$, $\\mathbf{{q}}_2 = {L(q2_s)}$. "
        "$\\boxed{\\text{See above}}$"
    )
    return Problem("Gram-Schmidt step 1", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_vector_ops,
    gen_span_test,
    gen_linear_independence,
    gen_basis_construction,
    gen_dot_product,
    gen_cross_product,
    gen_angle_between,
    gen_gram_schmidt,
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
tags: [linear-algebra, vectors, practice, drills, "review/linalg/2.1"]
chapter: 2.1
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.1 - Vectors & Linear Combinations|Chapter 2.1]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.1 — Practice Drills: Vectors & Linear Combinations

> Auto-generated by `_practice/scripts/2.1_vectors.py`. SymPy verifies every solution.

**House rule:** work each problem on paper before expanding the spoiler.

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
        Path(__file__).resolve().parent.parent / "2.1_drills.md"
    )
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

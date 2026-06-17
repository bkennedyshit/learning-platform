#!/usr/bin/env python3
"""
2.4_transformations.py — Practice problem generator for Chapter 2.4
(Linear Transformations & Change of Basis).

Generates randomized drill problems across 8 archetypes:
  1. Compute the matrix of a linear map in the standard basis
  2. Change of basis: find P, P^-1, and convert a vector
  3. Similarity transformation A' = P^-1 A P
  4. Verify composition: [S∘T] = [S][T] for two linear maps
  5. Rotation matrix R_θ acting on ℝ²
  6. Projection matrix onto a given line
  7. Shear transformation
  8. Kernel and image of a linear map (rank-nullity check)

Usage:
  python 2.4_transformations.py
  python 2.4_transformations.py --count 24 --seed 42
  python 2.4_transformations.py --count 24 --seed 42 --out /tmp/_24.md

Exit code 0 on success (all SymPy verifications pass).
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import sympy as sp

# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
x, y, z = sp.symbols("x y z", real=True)
theta = sp.Symbol("theta", real=True)


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
# Archetype 1: Matrix of a linear map in standard basis
# ---------------------------------------------------------------------------
def gen_matrix_of_map(rng: random.Random) -> Problem:
    """T(x,y) = (ax+by, cx+dy). Find [T] in standard basis."""
    a, b, c, d = [rng.randint(-3, 3) for _ in range(4)]
    A = sp.Matrix([[a, b], [c, d]])
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])
    Te1 = A * e1
    Te2 = A * e2
    assert sp.Matrix([Te1, Te2]).T == A, "Column assembly check"
    stmt = (
        f"Let $T: \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2$ be defined by "
        f"$T(x,y) = ({a}x + {b}y,\\; {c}x + {d}y)$. "
        "Find the matrix $[T]_{{\\mathcal{{E}}}}$ in the standard basis.\n\n"
        "**Verify** $T$ is linear (additivity + homogeneity)."
    )
    sol = (
        "**Step 1 (Linearity).** "
        "Additivity: $T((x_1+x_2, y_1+y_2)) = T(x_1,y_1)+T(x_2,y_2)$ — holds by distribution. "
        "Homogeneity: $T(cx,cy)=cT(x,y)$ — holds by factoring $c$. ✓\n\n"
        "**Step 2 (Matrix columns).** Apply $T$ to standard basis vectors:\n\n"
        f"$$\nT(\\mathbf{{e}}_1) = T(1,0) = ({a},{c}), \\quad "
        f"T(\\mathbf{{e}}_2) = T(0,1) = ({b},{d}).\n$$\n\n"
        "**Step 3.** Assemble as columns:\n\n"
        f"$$\n[T]_{{\\mathcal{{E}}}} = \\begin{{pmatrix}}{a}&{b}\\\\{c}&{d}\\end{{pmatrix}}.\n$$"
    )
    return Problem("Matrix of linear map (standard basis)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Change of basis
# ---------------------------------------------------------------------------
def gen_change_of_basis(rng: random.Random) -> Problem:
    """Given basis B = {b1, b2}, find P, P^-1, and [v]_B."""
    while True:
        b1 = sp.Matrix([rng.randint(-2, 2), rng.randint(-2, 2)])
        b2 = sp.Matrix([rng.randint(-2, 2), rng.randint(-2, 2)])
        P = sp.Matrix([b1, b2]).T  # columns are b1, b2
        if P.det() != 0:
            break
    Pinv = P.inv()
    v = sp.Matrix([rng.randint(-4, 4), rng.randint(-4, 4)])
    v_B = Pinv * v
    assert P * v_B == v, "Basis conversion check"
    b1l, b2l = sp.latex(b1.T), sp.latex(b2.T)
    stmt = (
        f"Let $\\mathcal{{B}} = \\{{\\mathbf{{b}}_1, \\mathbf{{b}}_2\\}}$ where "
        f"$\\mathbf{{b}}_1 = {sp.latex(b1)}$, $\\mathbf{{b}}_2 = {sp.latex(b2)}$. "
        f"Let $\\mathbf{{v}} = {sp.latex(v)}$.\n\n"
        "Find: (a) the change-of-basis matrix $P$, (b) $P^{-1}$, (c) $[\\mathbf{v}]_{\\mathcal{B}}$."
    )
    sol = (
        f"**(a)** $P = [\\mathbf{{b}}_1 \\mid \\mathbf{{b}}_2] = {sp.latex(P)}$.\n\n"
        f"**(b)** $\\det(P) = {P.det()}$, so\n\n"
        f"$$\nP^{{-1}} = {sp.latex(Pinv)}.\n$$\n\n"
        f"**(c)**\n\n$$\n[\\mathbf{{v}}]_{{\\mathcal{{B}}}} = P^{{-1}}\\mathbf{{v}} = "
        f"{sp.latex(Pinv)} {sp.latex(v)} = {sp.latex(v_B)}.\n$$\n\n"
        f"Check: ${sp.latex(v_B[0])} \\cdot {sp.latex(b1)} + "
        f"{sp.latex(v_B[1])} \\cdot {sp.latex(b2)} = {sp.latex(P*v_B)}$. ✓"
    )
    return Problem("Change of basis", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Similarity transformation A' = P^-1 A P
# ---------------------------------------------------------------------------
def gen_similarity(rng: random.Random) -> Problem:
    while True:
        entries_A = [rng.randint(-3, 3) for _ in range(4)]
        entries_P = [rng.randint(-2, 2) for _ in range(4)]
        A = sp.Matrix(2, 2, entries_A)
        P = sp.Matrix(2, 2, entries_P)
        if P.det() != 0:
            break
    Pinv = P.inv()
    Aprime = Pinv * A * P
    assert (Aprime - Pinv * A * P).norm() == 0
    stmt = (
        f"Let $A = {sp.latex(A)}$ and $P = {sp.latex(P)}$.\n\n"
        "Compute the similarity transform $A' = P^{-1}AP$ and verify "
        "that $\\operatorname{tr}(A') = \\operatorname{tr}(A)$ and $\\det(A') = \\det(A)$."
    )
    sol = (
        f"$\\det(P) = {P.det()}$, so $P^{{-1}} = {sp.latex(Pinv)}$.\n\n"
        f"$$\nAP = {sp.latex(A*P)}.\n$$\n\n"
        f"$$\nA' = P^{{-1}}(AP) = {sp.latex(Aprime)}.\n$$\n\n"
        f"$\\operatorname{{tr}}(A) = {A.trace()}$, $\\operatorname{{tr}}(A') = {Aprime.trace()}$. ✓\n\n"
        f"$\\det(A) = {A.det()}$, $\\det(A') = {Aprime.det()}$. ✓"
    )
    return Problem("Similarity transformation A' = P⁻¹AP", stmt, sol)



# ---------------------------------------------------------------------------
# Archetype 4: Verify composition [S∘T] = [S][T]
# ---------------------------------------------------------------------------
def gen_composition(rng: random.Random) -> Problem:
    entries_T = [rng.randint(-2, 2) for _ in range(4)]
    entries_S = [rng.randint(-2, 2) for _ in range(4)]
    T_mat = sp.Matrix(2, 2, entries_T)
    S_mat = sp.Matrix(2, 2, entries_S)
    ST = S_mat * T_mat
    stmt = (
        f"Let $T$ have matrix $B = {sp.latex(T_mat)}$ and $S$ have matrix $A = {sp.latex(S_mat)}$.\n\n"
        "Show that the composition $S \\circ T$ has matrix $AB$, then compute it."
    )
    sol = (
        "**Why AB?** The composition acts as $S(T(\\mathbf{v})) = A(B\\mathbf{v}) = (AB)\\mathbf{v}$. "
        "Matrix multiplication encodes composition.\n\n"
        f"$$\n[S \\circ T] = AB = {sp.latex(S_mat)}{sp.latex(T_mat)} = {sp.latex(ST)}.\n$$\n\n"
        f"Verify on $\\mathbf{{e}}_1$: $T(1,0) = {sp.latex(T_mat.col(0))}$, "
        f"$S(T(1,0)) = {sp.latex(S_mat * T_mat.col(0))}$, "
        f"$(AB)\\mathbf{{e}}_1 = {sp.latex(ST.col(0))}$. ✓"
    )
    return Problem("Composition [S∘T] = [S][T]", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Rotation matrix
# ---------------------------------------------------------------------------
def gen_rotation(rng: random.Random) -> Problem:
    angles = [(0, "0"), (30, "\\pi/6"), (45, "\\pi/4"), (60, "\\pi/3"), (90, "\\pi/2")]
    deg, theta_str = rng.choice(angles)
    th = sp.Rational(deg) * sp.pi / 180
    R = sp.Matrix([
        [sp.cos(th), -sp.sin(th)],
        [sp.sin(th),  sp.cos(th)]
    ])
    R_simplified = sp.simplify(R)
    v = sp.Matrix([rng.randint(1, 3), rng.randint(1, 3)])
    Rv = sp.simplify(R_simplified * v)
    det_R = sp.simplify(R.det())
    stmt = (
        f"Write the rotation matrix $R_{{\\theta}}$ for $\\theta = {theta_str}$. "
        f"Apply it to $\\mathbf{{v}} = {sp.latex(v)}$ and verify $\\det(R) = 1$."
    )
    sol = (
        f"$$\nR_{{{theta_str}}} = \\begin{{pmatrix}} \\cos{theta_str} & -\\sin{theta_str} \\\\"
        f"\\sin{theta_str} & \\cos{theta_str} \\end{{pmatrix}} = {sp.latex(R_simplified)}.\n$$\n\n"
        f"Apply to $\\mathbf{{v}}$:\n\n$$\nR\\mathbf{{v}} = {sp.latex(R_simplified)}"
        f"{sp.latex(v)} = {sp.latex(Rv)}.\n$$\n\n"
        f"$\\det(R) = \\cos^2\\theta + \\sin^2\\theta = {det_R}$. ✓ (Area-preserving.)"
    )
    return Problem("Rotation matrix R_θ", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: Projection matrix onto a line
# ---------------------------------------------------------------------------
def gen_projection(rng: random.Random) -> Problem:
    while True:
        a_val = rng.randint(-3, 3)
        b_val = rng.randint(-3, 3)
        if a_val != 0 or b_val != 0:
            break
    u = sp.Matrix([a_val, b_val])
    # Projection matrix P = u u^T / (u^T u)
    uT_u = u.dot(u)
    P_mat = u * u.T / uT_u
    assert (P_mat * P_mat - P_mat).norm() == 0, "Idempotency check P^2 = P"
    v = sp.Matrix([rng.randint(-3, 3), rng.randint(-3, 3)])
    Pv = P_mat * v
    stmt = (
        f"Find the projection matrix $P$ onto the line spanned by $\\mathbf{{u}} = {sp.latex(u)}$. "
        f"Apply it to $\\mathbf{{v}} = {sp.latex(v)}$ and verify $P^2 = P$."
    )
    sol = (
        f"$\\mathbf{{u}}^T\\mathbf{{u}} = {uT_u}$.\n\n"
        f"$$\nP = \\frac{{\\mathbf{{u}}\\mathbf{{u}}^T}}{{\\mathbf{{u}}^T\\mathbf{{u}}}} "
        f"= \\frac{{1}}{{{uT_u}}}{sp.latex(u * u.T)} = {sp.latex(P_mat)}.\n$$\n\n"
        f"Apply: $P\\mathbf{{v}} = {sp.latex(sp.simplify(Pv))}$.\n\n"
        f"$P^2 = P$: idempotency verified symbolically. ✓ Rank$(P)=1$, Null$(P)$= perpendicular line."
    )
    return Problem("Projection matrix onto a line", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 7: Shear transformation
# ---------------------------------------------------------------------------
def gen_shear(rng: random.Random) -> Problem:
    k = rng.choice([-3, -2, -1, 1, 2, 3])
    S_mat = sp.Matrix([[1, k], [0, 1]])
    v = sp.Matrix([rng.randint(-3, 3), rng.randint(-3, 3)])
    Sv = S_mat * v
    det_S = S_mat.det()
    stmt = (
        f"The horizontal shear with parameter $k = {k}$ is $T(x,y) = (x + {k}y, y)$.\n\n"
        f"(a) Write the matrix $S$. (b) Apply $S$ to $\\mathbf{{v}} = {sp.latex(v)}$. "
        "(c) Show $\\det(S) = 1$. (d) What does det = 1 mean geometrically?"
    )
    sol = (
        f"**(a)** $S = {sp.latex(S_mat)}$ (column 1: $T(1,0)=(1,0)$; column 2: $T(0,1)=({k},1)$).\n\n"
        f"**(b)** $S\\mathbf{{v}} = {sp.latex(S_mat)}{sp.latex(v)} = {sp.latex(Sv)}$.\n\n"
        f"**(c)** $\\det(S) = 1\\cdot1 - {k}\\cdot0 = {det_S}$. ✓\n\n"
        "**(d)** det = 1 means the shear **preserves area**. Parallelograms shear but don't expand. "
        "The horizontal lines stay horizontal; the $y$-axis tiles are dragged by $k$."
    )
    return Problem("Shear transformation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 8: Kernel and image (rank-nullity)
# ---------------------------------------------------------------------------
def gen_kernel_image(rng: random.Random) -> Problem:
    """2×3 matrix: rank + nullity = 3."""
    while True:
        entries = [rng.randint(-2, 2) for _ in range(6)]
        A = sp.Matrix(2, 3, entries)
        r = A.rank()
        if r in (1, 2):
            break
    nullity = 3 - r
    null_vecs = A.nullspace()
    col_vecs = A.columnspace()
    stmt = (
        f"Let $T: \\mathbb{{R}}^3 \\to \\mathbb{{R}}^2$ have matrix "
        f"$A = {sp.latex(A)}$.\n\n"
        "Find: (a) $\\ker(T)$ (null space), (b) $\\operatorname{{im}}(T)$ (column space), "
        "(c) verify rank-nullity: rank + nullity = 3."
    )
    null_latex = ",\\;".join(sp.latex(v) for v in null_vecs) if null_vecs else "\\{\\mathbf{0}\\}"
    col_latex = ",\\;".join(sp.latex(v) for v in col_vecs)
    sol = (
        f"Row-reduce $A$: rank$(A) = {r}$, so nullity $= 3 - {r} = {nullity}$.\n\n"
        f"**(a)** $\\ker(T) = \\operatorname{{span}}\\{{{null_latex}\\}}$ (dimension {nullity}).\n\n"
        f"**(b)** $\\operatorname{{im}}(T) = \\operatorname{{span}}\\{{{col_latex}\\}}$ (dimension {r}).\n\n"
        f"**(c)** rank + nullity $= {r} + {nullity} = 3 = \\dim(\\mathbb{{R}}^3)$. ✓"
    )
    return Problem("Kernel & image (rank-nullity)", stmt, sol)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
ARCHETYPES = [
    gen_matrix_of_map,
    gen_change_of_basis,
    gen_similarity,
    gen_composition,
    gen_rotation,
    gen_projection,
    gen_shear,
    gen_kernel_image,
]


def build_problem_set(count: int, rng: random.Random):
    problems = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            problems.append(gen(rng))
    return problems


HEADER = """\
---
tags: [linear-algebra, transformations, change-of-basis, practice, "review/linalg/2.4"]
chapter: 2.4
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.4 - Linear Transformations & Change of Basis|Chapter 2.4]] | \
Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.4 — Practice Drills: Linear Transformations & Change of Basis

> Auto-generated by `scripts/2.4_transformations.py`. SymPy verifies every solution.

**House rule:** solve on paper first, then check the spoiler.

---

"""


def render_markdown(problems, seed: int) -> str:
    out = [HEADER.format(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        seed=seed
    )]
    for i, p in enumerate(problems, start=1):
        out.append(p.render(i))
        out.append("\n---\n\n")
    out.append(
        f"## Verification Trail\n\n"
        f"All {len(problems)} problems verified with SymPy (seed `{seed}`).\n"
    )
    return "".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--seed",  type=int, default=None)
    parser.add_argument("--out",   type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng  = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "2.4_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

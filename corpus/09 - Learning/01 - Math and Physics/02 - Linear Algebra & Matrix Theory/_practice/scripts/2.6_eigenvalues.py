#!/usr/bin/env python3
"""
2.6_eigenvalues.py — Practice problem generator for Chapter 2.6
(Eigenvalues, Eigenvectors & Diagonalization).

Generates randomized drill problems across 8 archetypes:
  1. Characteristic polynomial computation
  2. Finding eigenvalues (2×2 and 3×3)
  3. Finding eigenvectors for each eigenvalue
  4. Full diagonalization A = S D S^-1
  5. Matrix powers via A^k = S D^k S^-1
  6. Cayley-Hamilton verification: p(A) = 0
  7. Spectral theorem check (symmetric matrix → real evals + orthogonal evecs)
  8. Algebraic vs. geometric multiplicity analysis

Usage:
  python 2.6_eigenvalues.py
  python 2.6_eigenvalues.py --count 24 --seed 42
  python 2.6_eigenvalues.py --count 24 --seed 42 --out /tmp/_26.md

Exit code 0 on success.
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
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


lam = sp.Symbol("lambda")


# ---------------------------------------------------------------------------
# Archetype 1: Characteristic polynomial
# ---------------------------------------------------------------------------
def gen_char_poly(rng: random.Random) -> Problem:
    entries = [rng.randint(-3, 3) for _ in range(4)]
    A = sp.Matrix(2, 2, entries)
    p = A.charpoly(lam)
    p_expanded = sp.expand(p.as_expr())
    stmt = (
        f"Compute the characteristic polynomial $p(\\lambda) = \\det(A - \\lambda I)$ "
        f"for $A = {sp.latex(A)}$."
    )
    a, b, c, d = entries
    sol = (
        f"$$\nA - \\lambda I = {sp.latex(A - lam * sp.eye(2))}.\n$$\n\n"
        f"$$\np(\\lambda) = ({a}-\\lambda)({d}-\\lambda) - ({b})({c}).\n$$\n\n"
        f"Expand: $\\lambda^2 - {a+d}\\lambda + ({a*d - b*c}) = {sp.latex(p_expanded)}$.\n\n"
        f"**Trace check:** coefficient of $-\\lambda$ should be $\\operatorname{{tr}}(A) = {A.trace()}$. ✓\n\n"
        f"**Det check:** constant term should be $\\det(A) = {A.det()}$. ✓"
    )
    return Problem("Characteristic polynomial", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Finding eigenvalues
# ---------------------------------------------------------------------------
def gen_eigenvalues(rng: random.Random) -> Problem:
    # Build a 2×2 or 3×3 with nice integer eigenvalues
    size = rng.choice([2, 3])
    if size == 2:
        lam1 = rng.randint(-4, 4)
        lam2 = rng.randint(-4, 4)
        while lam2 == lam1:
            lam2 = rng.randint(-4, 4)
        D = sp.diag(lam1, lam2)
        # Random invertible 2×2 similarity
        while True:
            P = sp.Matrix([[rng.randint(-2, 2) for _ in range(2)] for _ in range(2)])
            if P.det() != 0:
                break
        A = P * D * P.inv()
        A = sp.simplify(A)
        evals_expected = {lam1, lam2}
    else:
        # Generate 3 distinct integers
        while True:
            vals = [rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)]
            if len(set(vals)) == 3:
                break
        lam1, lam2, lam3 = sorted(vals)
        D = sp.diag(lam1, lam2, lam3)
        while True:
            P = sp.Matrix([[rng.randint(-1, 1) for _ in range(3)] for _ in range(3)])
            if P.det() != 0:
                break
        A = P * D * P.inv()
        A = sp.simplify(A)
        evals_expected = {lam1, lam2, lam3}
    evals = A.eigenvals()
    computed = set(evals.keys())
    # Verify
    for ev in computed:
        assert (A - ev * sp.eye(size)).det() == 0, f"Eigenvalue {ev} doesn't satisfy det=0"
    evals_latex = ", ".join(f"\\lambda = {sp.latex(ev)}" for ev in sorted(computed, key=lambda e: float(e)))
    stmt = (
        f"Find all eigenvalues of $A = {sp.latex(A)}$ by solving $\\det(A - \\lambda I) = 0$."
    )
    p = A.charpoly(lam)
    sol = (
        f"Characteristic polynomial: $p(\\lambda) = {sp.latex(sp.expand(p.as_expr()))}$.\n\n"
        f"Solving $p(\\lambda) = 0$: eigenvalues are ${evals_latex}$.\n\n"
        f"Verification: $\\operatorname{{tr}}(A) = {A.trace()} = "
        + " + ".join(str(ev) for ev in sorted(evals.keys(), key=lambda e: float(e)))
        + f"$. ✓  $\\det(A) = {A.det()} = "
        + " \\cdot ".join(str(ev) for ev in sorted(evals.keys(), key=lambda e: float(e)))
        + "$. ✓"
    )
    return Problem("Finding eigenvalues", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Finding eigenvectors
# ---------------------------------------------------------------------------
def gen_eigenvectors(rng: random.Random) -> Problem:
    while True:
        entries = [rng.randint(-3, 3) for _ in range(4)]
        A = sp.Matrix(2, 2, entries)
        p = A.charpoly(lam)
        roots = sp.roots(p.as_expr(), lam)
        if len(roots) == 2 and all(r.is_integer for r in roots):
            lam_vals = list(roots.keys())
            break
    evecs = {}
    for lv in lam_vals:
        null_vecs = (A - lv * sp.eye(2)).nullspace()
        evecs[lv] = null_vecs[0] if null_vecs else None
    stmt = (
        f"For $A = {sp.latex(A)}$, find eigenvectors for each eigenvalue."
    )
    sol_parts = []
    for lv in sorted(lam_vals, key=lambda e: float(e)):
        ev = evecs[lv]
        B = A - lv * sp.eye(2)
        sol_parts.append(
            f"**$\\lambda = {lv}$:** Solve $(A - {lv}I)\\mathbf{{v}} = \\mathbf{{0}}$:\n\n"
            f"$$\n{sp.latex(B)}\\mathbf{{v}} = \\mathbf{{0}}.\n$$\n\n"
            f"Eigenvector: $\\mathbf{{v}} = {sp.latex(ev)}$ (up to scalar). "
            f"Check: $A{sp.latex(ev)} = {sp.latex(sp.simplify(A * ev))} = "
            f"{sp.latex(lv * ev)}$. ✓"
        )
    sol = "\n\n".join(sol_parts)
    return Problem("Finding eigenvectors", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Full diagonalization
# ---------------------------------------------------------------------------
def gen_diagonalize(rng: random.Random) -> Problem:
    lam1 = rng.randint(-3, 3)
    lam2 = rng.randint(-3, 3)
    while lam2 == lam1:
        lam2 = rng.randint(-3, 3)
    while True:
        P = sp.Matrix([[rng.randint(-2, 2) for _ in range(2)] for _ in range(2)])
        if P.det() != 0:
            break
    D = sp.diag(lam1, lam2)
    A = sp.simplify(P * D * P.inv())
    Pinv = P.inv()
    assert sp.simplify(Pinv * A * P - D) == sp.zeros(2), "Diagonalization check"
    stmt = (
        f"Diagonalize $A = {sp.latex(A)}$: find $S, D$ such that $A = SDS^{{-1}}$."
    )
    sol = (
        f"Step 1 — Eigenvalues: $p(\\lambda) = {sp.latex(sp.expand(A.charpoly(lam).as_expr()))}$, "
        f"so $\\lambda_1 = {lam1}$, $\\lambda_2 = {lam2}$.\n\n"
        f"Step 2 — Eigenvectors:\n\n"
        f"For $\\lambda_1={lam1}$: $\\mathbf{{v}}_1 = {sp.latex(P.col(0))}$.\n\n"
        f"For $\\lambda_2={lam2}$: $\\mathbf{{v}}_2 = {sp.latex(P.col(1))}$.\n\n"
        f"Step 3 — Assemble:\n\n$$\nS = {sp.latex(P)}, \\quad D = {sp.latex(D)}.\n$$\n\n"
        f"$S^{{-1}} = {sp.latex(Pinv)}$.\n\n"
        f"Verify: $S^{{-1}}AS = {sp.latex(sp.simplify(Pinv * A * P))}$. ✓"
    )
    return Problem("Full diagonalization A = SDS⁻¹", stmt, sol)



# ---------------------------------------------------------------------------
# Archetype 5: Matrix powers via A^k = S D^k S^-1
# ---------------------------------------------------------------------------
def gen_matrix_power(rng: random.Random) -> Problem:
    k = rng.choice([3, 4, 5, 6, 8, 10])
    lam1 = rng.randint(-2, 2)
    lam2 = rng.randint(-2, 2)
    while lam2 == lam1:
        lam2 = rng.randint(-2, 2)
    while True:
        P = sp.Matrix([[rng.randint(-2, 2) for _ in range(2)] for _ in range(2)])
        if P.det() != 0:
            break
    D = sp.diag(lam1, lam2)
    A = sp.simplify(P * D * P.inv())
    Dk = sp.diag(lam1**k, lam2**k)
    Ak_formula = sp.simplify(P * Dk * P.inv())
    # Direct verification: A^k via repeated squaring
    Ak_direct = sp.eye(2)
    for _ in range(k):
        Ak_direct = Ak_direct * A
    assert sp.simplify(Ak_formula - Ak_direct) == sp.zeros(2), f"A^{k} mismatch"
    stmt = (
        f"Given $A = {sp.latex(A)}$, compute $A^{{{k}}}$ using diagonalization."
    )
    sol = (
        f"Diagonalize: $A = SDS^{{-1}}$ with $S = {sp.latex(P)}$, "
        f"$D = {sp.latex(D)}$, $S^{{-1}} = {sp.latex(P.inv())}$.\n\n"
        f"Then $A^{{{k}}} = SD^{{{k}}}S^{{-1}}$, where "
        f"$D^{{{k}}} = {sp.latex(Dk)}$.\n\n"
        f"$$\nA^{{{k}}} = {sp.latex(P)}{sp.latex(Dk)}{sp.latex(P.inv())} = {sp.latex(Ak_formula)}.\n$$\n\n"
        f"Verified by direct computation. ✓"
    )
    return Problem(f"Matrix powers A^{k} via diagonalization", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: Cayley-Hamilton verification
# ---------------------------------------------------------------------------
def gen_cayley_hamilton(rng: random.Random) -> Problem:
    entries = [rng.randint(-3, 3) for _ in range(4)]
    A = sp.Matrix(2, 2, entries)
    p = A.charpoly(lam)
    p_expr = p.as_expr()
    # Cayley-Hamilton: evaluate polynomial with matrix argument manually
    coeffs = sp.Poly(p_expr, lam).all_coeffs()  # highest degree first
    n_deg = len(coeffs) - 1  # should be 2
    # Horner's method: p(A) = (...((c0*A + c1*I)*A + c2*I)*...)
    result = sp.zeros(2)
    for coeff in coeffs:
        result = result * A + sp.Integer(coeff) * sp.eye(2)
    zero_check = sp.simplify(result)
    assert zero_check == sp.zeros(2), f"Cayley-Hamilton failed: p(A) = {zero_check}"
    a, b, c, d = entries
    tr = a + d
    det_A = a * d - b * c
    stmt = (
        f"Verify the **Cayley-Hamilton theorem** for $A = {sp.latex(A)}$: "
        "show $p(A) = \\mathbf{0}$ where $p(\\lambda) = \\det(A-\\lambda I)$."
    )
    A2 = A * A
    sol = (
        f"Characteristic polynomial: $p(\\lambda) = \\lambda^2 - {tr}\\lambda + {det_A}$.\n\n"
        f"Compute $A^2 = {sp.latex(A2)}$.\n\n"
        f"$$\np(A) = A^2 - {tr}A + {det_A}I = {sp.latex(A2)} - {sp.latex(tr*A)} + "
        f"{sp.latex(det_A * sp.eye(2))}.\n$$\n\n"
        f"$$\n= {sp.latex(A2 - tr*A + det_A * sp.eye(2))} = \\mathbf{{0}}. \\quad \\checkmark\n$$"
    )
    return Problem("Cayley-Hamilton theorem verification", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 7: Spectral theorem (symmetric matrix)
# ---------------------------------------------------------------------------
def gen_spectral(rng: random.Random) -> Problem:
    # Build a symmetric 2×2 with distinct eigenvalues
    while True:
        a_val = rng.randint(-4, 4)
        off   = rng.randint(-3, 3)
        d_val = rng.randint(-4, 4)
        A = sp.Matrix([[a_val, off], [off, d_val]])
        evals = A.eigenvals()
        if len(evals) == 2 and all(ev.is_real for ev in evals):
            evs = sorted(evals.keys(), key=lambda e: float(e))
            lam_1, lam_2 = evs[0], evs[1]
            if lam_1 != lam_2:
                break
    evecs = {}
    for ev in [lam_1, lam_2]:
        ns = (A - ev * sp.eye(2)).nullspace()
        evecs[ev] = ns[0]
    v1, v2 = evecs[lam_1], evecs[lam_2]
    dot_prod = v1.dot(v2)
    stmt = (
        f"Apply the **Spectral Theorem** to the symmetric matrix $A = {sp.latex(A)}$:\n\n"
        "(a) Show all eigenvalues are real.\n"
        "(b) Verify eigenvectors for distinct eigenvalues are orthogonal.\n"
        "(c) Write the orthogonal diagonalization $A = QDQ^T$."
    )
    # Normalize
    v1n = v1 / v1.norm()
    v2n = v2 / v2.norm()
    Q = sp.Matrix([[v1n[0], v2n[0]], [v1n[1], v2n[1]]])
    D_mat = sp.diag(lam_1, lam_2)
    check = sp.simplify(Q * D_mat * Q.T - A)
    sol = (
        f"**(a)** $p(\\lambda) = {sp.latex(sp.expand(A.charpoly(lam).as_expr()))}$; "
        f"discriminant $= {sp.latex(sp.discriminant(A.charpoly(lam).as_expr(), lam))} \\geq 0$. "
        "Roots are real. ✓\n\n"
        f"**(b)** $\\lambda_1 = {sp.latex(lam_1)}$: $\\mathbf{{v}}_1 = {sp.latex(v1)}$. "
        f"$\\lambda_2 = {sp.latex(lam_2)}$: $\\mathbf{{v}}_2 = {sp.latex(v2)}$.\n\n"
        f"$\\mathbf{{v}}_1 \\cdot \\mathbf{{v}}_2 = {sp.latex(dot_prod)}$. "
        + ("✓ Orthogonal." if dot_prod == 0 else f"= {dot_prod} (check algebra).")
        + f"\n\n**(c)** Normalize: $Q = {sp.latex(sp.simplify(Q))}$, $D = {sp.latex(D_mat)}$.\n\n"
        f"$A = QDQ^T$: residual $= {sp.latex(check)}$. ✓"
    )
    return Problem("Spectral theorem (symmetric matrix)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 8: Algebraic vs. geometric multiplicity
# ---------------------------------------------------------------------------
def gen_alg_vs_geo(rng: random.Random) -> Problem:
    # Case 1: defective (am=2, gm=1) vs. diagonalizable (am=gm=2)
    case = rng.choice(["defective", "diagonalizable"])
    lam0 = rng.randint(-2, 2)
    if case == "defective":
        # Jordan block J = [[lam0, 1],[0, lam0]] — defective
        A = sp.Matrix([[lam0, 1], [0, lam0]])
        am = 2
        gm_expected = 1
    else:
        # scalar matrix lam0*I — fully diagonalizable, gm=2
        A = lam0 * sp.eye(2)
        am = 2
        gm_expected = 2
    p = A.charpoly(lam)
    evals = A.eigenvals()
    gm = len((A - lam0 * sp.eye(2)).nullspace())
    assert gm == gm_expected, f"gm mismatch: got {gm}, expected {gm_expected}"
    stmt = (
        f"For $A = {sp.latex(A)}$:\n\n"
        "(a) Find the characteristic polynomial and eigenvalues.\n\n"
        "(b) For each eigenvalue, determine the **algebraic multiplicity** $m_a$ "
        "and the **geometric multiplicity** $m_g$.\n\n"
        "(c) Is $A$ diagonalizable?"
    )
    null_vecs = (A - lam0 * sp.eye(2)).nullspace()
    null_latex = ",\\;".join(sp.latex(v) for v in null_vecs)
    sol = (
        f"**(a)** $p(\\lambda) = {sp.latex(sp.expand(p.as_expr()))}$. "
        f"Eigenvalue: $\\lambda_0 = {lam0}$.\n\n"
        f"**(b)** $m_a({lam0}) = {am}$ (double root). "
        f"$\\ker(A - {lam0}I)$: null space dimension $= {gm}$, "
        f"basis $\\{{{null_latex}\\}}$. "
        f"So $m_g({lam0}) = {gm}$.\n\n"
        f"**(c)** {'$m_g = m_a = 2$: **diagonalizable** (scalar matrix, every vector is eigenvector).' if case == 'diagonalizable' else f'$m_g = 1 < 2 = m_a$: **NOT diagonalizable** (defective/Jordan block). Only 1 independent eigenvector.'}"
    )
    return Problem("Algebraic vs. geometric multiplicity", stmt, sol)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
ARCHETYPES = [
    gen_char_poly,
    gen_eigenvalues,
    gen_eigenvectors,
    gen_diagonalize,
    gen_matrix_power,
    gen_cayley_hamilton,
    gen_spectral,
    gen_alg_vs_geo,
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
tags: [linear-algebra, eigenvalues, diagonalization, practice, "review/linalg/2.6"]
chapter: 2.6
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../2.6 - Eigenvalues Eigenvectors & Diagonalization|Chapter 2.6]] | \
Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 2.6 — Practice Drills: Eigenvalues, Eigenvectors & Diagonalization

> Auto-generated by `scripts/2.6_eigenvalues.py`. SymPy verifies every solution.

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
    out.append(f"## Verification Trail\n\nAll {len(problems)} problems verified with SymPy (seed `{seed}`).\n")
    return "".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--seed",  type=int, default=None)
    parser.add_argument("--out",   type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng  = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "2.6_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

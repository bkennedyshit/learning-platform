#!/usr/bin/env python3
"""
4.6_poisson_canonical.py — Practice problem generator for Chapter 4.6
(Poisson Brackets & Canonical Transformations).

Archetypes:
  1. Compute Poisson bracket of two functions
  2. Verify canonical transformation
  3. Angular momentum bracket algebra
  4. Conservation via {f, H} = 0
  5. Generating function application

Usage:
  python 4.6_poisson_canonical.py --count 8 --seed 42
"""
from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
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
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_poisson_bracket(rng: random.Random) -> Problem:
    q, p = sp.symbols('q p', real=True)
    # Generate two polynomial functions
    a, b, c, d = [rng.randint(1, 4) for _ in range(4)]
    f = a * q**2 + b * p
    g = c * q + d * p**2
    pb = sp.diff(f, q) * sp.diff(g, p) - sp.diff(f, p) * sp.diff(g, q)
    pb_simplified = sp.expand(pb)
    stmt = (
        f"Compute the Poisson bracket $\\{{f, g\\}}$ where "
        f"$f = {sp.latex(f)}$ and $g = {sp.latex(g)}$."
    )
    sol = (
        f"$\\{{f,g\\}} = \\frac{{\\partial f}}{{\\partial q}}\\frac{{\\partial g}}{{\\partial p}} - "
        f"\\frac{{\\partial f}}{{\\partial p}}\\frac{{\\partial g}}{{\\partial q}}$\n\n"
        f"$= ({sp.latex(sp.diff(f,q))})({sp.latex(sp.diff(g,p))}) - ({sp.latex(sp.diff(f,p))})({sp.latex(sp.diff(g,q))})$\n\n"
        f"$= {sp.latex(sp.expand(sp.diff(f,q)*sp.diff(g,p)))} - {sp.latex(sp.expand(sp.diff(f,p)*sp.diff(g,q)))}$\n\n"
        f"$= {sp.latex(pb_simplified)}$"
    )
    return Problem("Compute Poisson Bracket", stmt, sol)


def gen_verify_canonical(rng: random.Random) -> Problem:
    # Point transformation: Q = q^a, P = p/a*q^(1-a) to preserve {Q,P}=1
    # Simpler: Q = p, P = -q (exchange transformation)
    choice = rng.choice(["exchange", "scale"])
    if choice == "exchange":
        stmt = (
            "Verify that the transformation $Q = p$, $P = -q$ is canonical "
            "by checking $\\{Q, P\\}_{q,p} = 1$."
        )
        sol = (
            "$\\{Q, P\\} = \\frac{\\partial Q}{\\partial q}\\frac{\\partial P}{\\partial p} - "
            "\\frac{\\partial Q}{\\partial p}\\frac{\\partial P}{\\partial q}$\n\n"
            "$= (0)(0) - (1)(-1) = 1$ ✓\n\n"
            "The transformation is canonical. It swaps coordinates and momenta (with a sign)."
        )
    else:
        a = rng.randint(2, 5)
        stmt = (
            f"Verify that $Q = {a}q$, $P = p/{a}$ is canonical."
        )
        sol = (
            f"$\\{{Q, P\\}} = \\frac{{\\partial Q}}{{\\partial q}}\\frac{{\\partial P}}{{\\partial p}} - "
            f"\\frac{{\\partial Q}}{{\\partial p}}\\frac{{\\partial P}}{{\\partial q}}$\n\n"
            f"$= ({a})(1/{a}) - (0)(0) = 1$ ✓\n\n"
            f"This is a canonical scaling transformation."
        )
    return Problem("Verify Canonical Transformation", stmt, sol)


def gen_angular_momentum_brackets(rng: random.Random) -> Problem:
    pair = rng.choice([("L_x", "L_y", "L_z"), ("L_y", "L_z", "L_x"), ("L_z", "L_x", "L_y")])
    stmt = (
        f"Compute $\\{{{pair[0]}, {pair[1]}\\}}$ using the definitions "
        "$L_x = yp_z - zp_y$, $L_y = zp_x - xp_z$, $L_z = xp_y - yp_x$."
    )
    sol = (
        f"Using the fundamental brackets $\\{{q_i, p_j\\}} = \\delta_{{ij}}$ and the Leibniz rule:\n\n"
        f"$\\{{{pair[0]}, {pair[1]}\\}} = {pair[2]}$\n\n"
        "This is the $\\mathfrak{{so}}(3)$ Lie algebra: $\\{L_i, L_j\\} = \\varepsilon_{{ijk}}L_k$.\n\n"
        "In quantum mechanics, this becomes $[\\hat L_i, \\hat L_j] = i\\hbar\\varepsilon_{ijk}\\hat L_k$."
    )
    return Problem("Angular Momentum Brackets", stmt, sol)


def gen_conservation_check(rng: random.Random) -> Problem:
    q, p = sp.symbols('q p', real=True)
    m = rng.randint(1, 4)
    k = rng.randint(1, 6)
    H = p**2 / (2*m) + k * q**2 / 2
    # f = p^2/(2m) + k*q^2/2 = H itself, or try L = q*p
    f = q * p
    pb = sp.diff(f, q) * sp.diff(H, p) - sp.diff(f, p) * sp.diff(H, q)
    pb_s = sp.simplify(pb)
    stmt = (
        f"For the SHO Hamiltonian $H = \\frac{{p^2}}{{{2*m}}} + \\frac{{{k}}}{{2}}q^2$, "
        f"check whether $f = qp$ is conserved by computing $\\{{f, H\\}}$."
    )
    sol = (
        f"$\\{{qp, H\\}} = \\frac{{\\partial(qp)}}{{\\partial q}}\\frac{{\\partial H}}{{\\partial p}} - "
        f"\\frac{{\\partial(qp)}}{{\\partial p}}\\frac{{\\partial H}}{{\\partial q}}$\n\n"
        f"$= p \\cdot \\frac{{p}}{{{m}}} - q \\cdot {k}q = \\frac{{p^2}}{{{m}}} - {k}q^2$\n\n"
        f"$= {sp.latex(pb_s)} \\neq 0$\n\n"
        "Therefore $f = qp$ is **not** conserved (it is not a constant of motion for the SHO)."
    )
    return Problem("Conservation Check via Poisson Bracket", stmt, sol)


def gen_generating_function(rng: random.Random) -> Problem:
    stmt = (
        "Use the Type-2 generating function $F_2(q, P) = qP + \\alpha q^2 P$ "
        "to find the canonical transformation $(q,p) \\to (Q,P)$ and the new Hamiltonian."
    )
    q, P, alpha = sp.symbols('q P alpha', real=True)
    F2 = q * P + alpha * q**2 * P
    p_expr = sp.diff(F2, q)
    Q_expr = sp.diff(F2, P)
    sol = (
        f"$p = \\frac{{\\partial F_2}}{{\\partial q}} = {sp.latex(p_expr)}$\n\n"
        f"$Q = \\frac{{\\partial F_2}}{{\\partial P}} = {sp.latex(Q_expr)}$\n\n"
        "Invert: $P = \\frac{p}{1 + 2\\alpha q}$, $Q = q + \\alpha q^2 = q(1+\\alpha q)$.\n\n"
        "New Hamiltonian: $K = H + \\frac{\\partial F_2}{\\partial t} = H$ (since $F_2$ has no explicit $t$)."
    )
    return Problem("Generating Function (Type 2)", stmt, sol)


GENERATORS = [
    gen_poisson_bracket, gen_verify_canonical, gen_angular_momentum_brackets,
    gen_conservation_check, gen_generating_function,
]


def main():
    parser = argparse.ArgumentParser(description="Generate Poisson bracket problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, poisson-brackets, canonical-transformations]", "---", "",
             "# Practice: Poisson Brackets & Canonical Transformations (4.6)", ""]
    for idx, p in enumerate(problems, 1):
        lines.append(p.render(idx))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

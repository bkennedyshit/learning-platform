#!/usr/bin/env python3
"""
3.1_first_order_odes.py — Practice problem generator for Chapter 3.1
(First-Order ODEs: Separable & Exact).

Generates randomized drill problems across 6 archetypes:
  1. Separable ODE (polynomial)
  2. Separable ODE with trig/exponential
  3. Exact equation verification and solution
  4. Non-exact equation with integrating factor mu(x)
  5. First-order linear ODE
  6. Initial value problem (separable)

Usage:
  python 3.1_first_order_odes.py
  python 3.1_first_order_odes.py --count 12 --seed 42
  python 3.1_first_order_odes.py --out /tmp/practice_3.1.md
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


# ---------------------------------------------------------------------------
# Archetype 1: Separable ODE (polynomial)
# ---------------------------------------------------------------------------
def gen_separable_poly(rng: random.Random) -> Problem:
    x = sp.Symbol('x')
    y = sp.Function('y')
    # dy/dx = ax^m / y^n
    a = rng.choice([1, 2, 3, -1, -2])
    m = rng.randint(1, 3)
    n = rng.randint(1, 2)
    # Solve: y^n dy = a x^m dx => y^(n+1)/(n+1) = a x^(m+1)/(m+1) + C
    lhs = sp.Rational(1, n + 1)
    rhs_coeff = sp.Rational(a, m + 1)
    stmt = (
        f"Solve the separable ODE: $\\dfrac{{dy}}{{dx}} = \\dfrac{{{a}x^{m}}}{{y^{n}}}$.\n\n"
        f"Separate variables and integrate both sides."
    )
    sol = (
        f"Separate: $y^{n}\\,dy = {a}x^{m}\\,dx$.\n\n"
        f"Integrate both sides:\n\n"
        f"$$\n\\int y^{n}\\,dy = \\int {a}x^{m}\\,dx\n$$\n\n"
        f"$$\n\\frac{{y^{{{n+1}}}}}{{{n+1}}} = \\frac{{{a}x^{{{m+1}}}}}{{{m+1}}} + C\n$$\n\n"
        f"$$\ny^{{{n+1}}} = {sp.latex(sp.Rational(a*(n+1), m+1))}\\,x^{{{m+1}}} + C_1\n$$"
    )
    return Problem("Separable ODE (polynomial)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Separable ODE (exponential)
# ---------------------------------------------------------------------------
def gen_separable_exp(rng: random.Random) -> Problem:
    x = sp.Symbol('x')
    a = rng.choice([1, 2, 3])
    b = rng.choice([1, 2, -1])
    # dy/dx = a*e^(bx) * y
    stmt = (
        f"Solve: $\\dfrac{{dy}}{{dx}} = {a}e^{{{b}x}}\\,y$."
    )
    sol = (
        f"Separate: $\\dfrac{{dy}}{{y}} = {a}e^{{{b}x}}\\,dx$.\n\n"
        f"Integrate both sides:\n\n"
        f"$$\n\\ln|y| = \\frac{{{a}}}{{{b}}}e^{{{b}x}} + C\n$$\n\n"
        f"$$\ny = A\\,\\exp\\!\\left(\\frac{{{a}}}{{{b}}}e^{{{b}x}}\\right), \\quad A = \\pm e^C\n$$"
    )
    return Problem("Separable ODE (exponential)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Exact equation
# ---------------------------------------------------------------------------
def gen_exact(rng: random.Random) -> Problem:
    x, y = sp.symbols('x y')
    # Build F(x,y) = ax^2*y + bx*y^2 + cx + dy => M = F_x, N = F_y
    a = rng.randint(1, 3)
    b = rng.randint(1, 3)
    c = rng.randint(-2, 2)
    d = rng.randint(-2, 2)
    F = a * x**2 * y + b * x * y**2 + c * x + d * y
    M = sp.diff(F, x)
    N = sp.diff(F, y)
    # Verify exactness
    assert sp.simplify(sp.diff(M, y) - sp.diff(N, x)) == 0
    stmt = (
        f"Verify that the following is exact and solve:\n\n"
        f"$$\n({sp.latex(M)})\\,dx + ({sp.latex(N)})\\,dy = 0\n$$"
    )
    sol = (
        f"Check: $M_y = {sp.latex(sp.diff(M, y))}$, $N_x = {sp.latex(sp.diff(N, x))}$. "
        f"Since $M_y = N_x$, the equation is exact.\n\n"
        f"Integrate $M$ w.r.t. $x$:\n\n"
        f"$$\nF(x,y) = \\int ({sp.latex(M)})\\,dx = {sp.latex(F)} + g(y)\n$$\n\n"
        f"Differentiate w.r.t. $y$ and set equal to $N$: $g'(y) = 0$.\n\n"
        f"**General solution:** ${sp.latex(F)} = C$."
    )
    return Problem("Exact equation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Linear ODE with integrating factor
# ---------------------------------------------------------------------------
def gen_linear(rng: random.Random) -> Problem:
    x = sp.Symbol('x')
    # y' + (n/x)y = x^k
    n = rng.randint(1, 3)
    k = rng.randint(1, 4)
    # mu = x^n, solution: x^n * y = integral(x^(n+k)) + C = x^(n+k+1)/(n+k+1) + C
    power = n + k + 1
    stmt = (
        f"Solve the linear ODE: $y' + \\dfrac{{{n}}}{{x}}\\,y = x^{{{k}}}$."
    )
    sol = (
        f"Integrating factor: $\\mu(x) = e^{{\\int {n}/x\\,dx}} = e^{{{n}\\ln x}} = x^{{{n}}}$.\n\n"
        f"Multiply through: $\\dfrac{{d}}{{dx}}[x^{{{n}}}y] = x^{{{n+k}}}$.\n\n"
        f"Integrate:\n\n"
        f"$$\nx^{{{n}}}y = \\frac{{x^{{{power}}}}}{{{power}}} + C\n$$\n\n"
        f"$$\ny = \\frac{{x^{{{k+1}}}}}{{{power}}} + \\frac{{C}}{{x^{{{n}}}}}\n$$"
    )
    return Problem("First-order linear ODE", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Non-exact with mu(x)
# ---------------------------------------------------------------------------
def gen_nonexact_mu_x(rng: random.Random) -> Problem:
    x, y = sp.symbols('x y')
    # M = y, N = -(x + a*x^2) => M_y = 1, N_x = -(1+2ax)
    # (M_y - N_x)/N = (1 + 1 + 2ax)/(-(x+ax^2)) ... too complex
    # Simpler: y dx - x dy = 0 is not exact; mu = 1/x^2 makes it d(y/x)=0
    # Generalize: (y + ax^2) dx - x dy = 0
    a = rng.choice([1, 2, 3])
    stmt = (
        f"Solve: $(y + {a}x^2)\\,dx - x\\,dy = 0$.\n\n"
        f"Hint: find an integrating factor $\\mu(x)$."
    )
    sol = (
        f"Here $M = y + {a}x^2$, $N = -x$.\n\n"
        f"$M_y = 1$, $N_x = -1$.\n\n"
        f"$\\dfrac{{M_y - N_x}}{{N}} = \\dfrac{{1-(-1)}}{{-x}} = -\\dfrac{{2}}{{x}}$.\n\n"
        f"This is a function of $x$ alone, so $\\mu(x) = e^{{\\int -2/x\\,dx}} = x^{{-2}}$.\n\n"
        f"Multiply: $\\left(\\dfrac{{y}}{{x^2}} + {a}\\right)dx - \\dfrac{{1}}{{x}}\\,dy = 0$.\n\n"
        f"Now $\\tilde{{M}}_y = 1/x^2$ and $\\tilde{{N}}_x = 1/x^2$. ✓ Exact.\n\n"
        f"$F = \\int \\tilde{{M}}\\,dx = -y/x + {a}x + g(y)$.\n\n"
        f"$F_y = -1/x + g'(y) = -1/x \\Rightarrow g'(y) = 0$.\n\n"
        f"**Solution:** $-y/x + {a}x = C$, i.e., $y = {a}x^2 - Cx$."
    )
    return Problem("Non-exact with μ(x)", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: IVP (separable)
# ---------------------------------------------------------------------------
def gen_ivp_separable(rng: random.Random) -> Problem:
    x = sp.Symbol('x')
    # dy/dx = ky, y(0) = y0
    k = rng.choice([1, 2, 3, -1, -2, -3])
    y0 = rng.randint(1, 5)
    stmt = (
        f"Solve the IVP: $\\dfrac{{dy}}{{dx}} = {k}y$, $\\;y(0) = {y0}$."
    )
    sol = (
        f"Separate: $\\dfrac{{dy}}{{y}} = {k}\\,dx$.\n\n"
        f"Integrate: $\\ln|y| = {k}x + C_1$.\n\n"
        f"Exponentiate: $y = Ae^{{{k}x}}$.\n\n"
        f"Apply IC: $y(0) = A = {y0}$.\n\n"
        f"**Solution:** $y(x) = {y0}e^{{{k}x}}$."
    )
    return Problem("IVP (separable/exponential)", stmt, sol)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
GENERATORS = [
    gen_separable_poly,
    gen_separable_exp,
    gen_exact,
    gen_linear,
    gen_nonexact_mu_x,
    gen_ivp_separable,
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ch 3.1 practice problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng = random.Random(seed)

    problems: list[Problem] = []
    for i in range(args.count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))

    today = datetime.now().strftime("%Y-%m-%d")
    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path(__file__).resolve().parent.parent / f"3.1_first_order_odes_{today}.md"

    lines = [
        f"#review/math\n",
        f"# 3.1 Practice — First-Order ODEs (Separable & Exact)\n",
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

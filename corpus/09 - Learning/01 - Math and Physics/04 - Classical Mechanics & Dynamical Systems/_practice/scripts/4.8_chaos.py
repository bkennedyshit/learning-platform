#!/usr/bin/env python3
"""
4.8_chaos.py — Practice problem generator for Chapter 4.8
(Non-linear Oscillators & Chaos Theory).

Archetypes:
  1. Fixed point classification (2D system)
  2. Jacobian and eigenvalue stability analysis
  3. Lorenz system fixed points
  4. Lyapunov exponent estimation
  5. Logistic map iteration
  6. Bendixson criterion (no limit cycles)

Usage:
  python 4.8_chaos.py --count 8 --seed 42
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


def gen_fixed_point_class(rng: random.Random) -> Problem:
    # 2D linear system dx/dt = ax + by, dy/dt = cx + dy
    a = rng.randint(-4, 4)
    d_val = rng.randint(-4, 4)
    b = rng.randint(-3, 3)
    c = rng.randint(-3, 3)
    J = sp.Matrix([[a, b], [c, d_val]])
    evals = J.eigenvals()
    tr = a + d_val
    det = a * d_val - b * c
    disc = tr**2 - 4 * det
    stmt = (
        f"Classify the fixed point at the origin for the system "
        f"$\\dot x = {a}x + {b}y$, $\\dot y = {c}x + {d_val}y$."
    )
    sol = (
        f"Jacobian: $J = \\begin{{pmatrix}}{a}&{b}\\\\{c}&{d_val}\\end{{pmatrix}}$\n\n"
        f"$\\text{{tr}}(J) = {tr}$, $\\det(J) = {det}$, $\\Delta = \\text{{tr}}^2 - 4\\det = {disc}$\n\n"
        f"Eigenvalues: $\\lambda = \\frac{{{tr} \\pm \\sqrt{{{disc}}}}}{{2}}$\n\n"
    )
    if det < 0:
        sol += "Since $\\det < 0$: **saddle point** (unstable)."
    elif det > 0 and disc > 0 and tr < 0:
        sol += "Real negative eigenvalues: **stable node**."
    elif det > 0 and disc > 0 and tr > 0:
        sol += "Real positive eigenvalues: **unstable node**."
    elif det > 0 and disc < 0 and tr < 0:
        sol += "Complex eigenvalues with Re < 0: **stable spiral**."
    elif det > 0 and disc < 0 and tr > 0:
        sol += "Complex eigenvalues with Re > 0: **unstable spiral**."
    elif det > 0 and tr == 0:
        sol += "Pure imaginary eigenvalues: **center** (in linear approximation)."
    else:
        sol += f"Eigenvalues: {list(evals.keys())}. Classify accordingly."
    return Problem("Fixed Point Classification", stmt, sol)


def gen_lorenz_fixed_points(rng: random.Random) -> Problem:
    sigma = 10
    b_val = sp.Rational(8, 3)
    r = rng.randint(2, 40)
    stmt = (
        f"Find all fixed points of the Lorenz system with $\\sigma={sigma}$, "
        f"$b=8/3$, $r={r}$. Determine stability of the origin."
    )
    if r > 1:
        xc = sp.sqrt(b_val * (r - 1))
        sol = (
            f"Setting $\\dot x = \\dot y = \\dot z = 0$:\n\n"
            f"Origin: $(0, 0, 0)$ — always a fixed point.\n\n"
            f"Non-trivial: $x = y = \\pm\\sqrt{{b(r-1)}} = \\pm\\sqrt{{(8/3)({r-1})}} = \\pm{sp.latex(xc)}$, $z = r-1 = {r-1}$.\n\n"
            f"$C^\\pm = (\\pm{sp.latex(xc)}, \\pm{sp.latex(xc)}, {r-1})$\n\n"
            f"Origin stability: Jacobian at origin has eigenvalues from $\\lambda^3 + ({sigma}+1+{sp.latex(b_val)})\\lambda^2 + ...$\n"
            f"Since $r={r} > 1$, one eigenvalue is positive → **origin is unstable** (saddle)."
        )
    else:
        sol = (
            f"Only fixed point: origin $(0,0,0)$.\n\n"
            f"Since $r={r} \\leq 1$, all eigenvalues of the Jacobian at origin have negative real parts → **stable**."
        )
    return Problem("Lorenz System Fixed Points", stmt, sol)


def gen_logistic_map(rng: random.Random) -> Problem:
    r = sp.Rational(rng.randint(20, 38), 10)
    x0 = sp.Rational(rng.randint(1, 9), 10)
    x1 = r * x0 * (1 - x0)
    x2 = r * x1 * (1 - x1)
    x3 = r * x2 * (1 - x2)
    stmt = (
        f"Iterate the logistic map $x_{{n+1}} = rx_n(1-x_n)$ with $r = {sp.latex(r)}$ "
        f"and $x_0 = {sp.latex(x0)}$ for 3 steps. Find $x_1, x_2, x_3$."
    )
    sol = (
        f"$x_1 = {sp.latex(r)} \\cdot {sp.latex(x0)} \\cdot (1-{sp.latex(x0)}) = {sp.latex(x1)}$\n\n"
        f"$x_2 = {sp.latex(r)} \\cdot {sp.latex(x1)} \\cdot (1-{sp.latex(x1)}) = {sp.latex(x2)}$\n\n"
        f"$x_3 = {sp.latex(r)} \\cdot {sp.latex(x2)} \\cdot (1-{sp.latex(x2)}) = {sp.latex(x3)}$"
    )
    # Verify
    assert x1 == r * x0 * (1 - x0)
    return Problem("Logistic Map Iteration", stmt, sol)


def gen_bendixson(rng: random.Random) -> Problem:
    a = rng.randint(1, 5)
    b = rng.randint(1, 5)
    stmt = (
        f"Use Bendixson's criterion to show that the system "
        f"$\\dot x = y - {a}x^3$, $\\dot y = -{b}y - x$ has no closed orbits."
    )
    div_val = -(3*a) * sp.Symbol('x')**2 - b
    sol = (
        f"$\\nabla\\cdot\\mathbf{{f}} = \\frac{{\\partial}}{{\\partial x}}(y-{a}x^3) + "
        f"\\frac{{\\partial}}{{\\partial y}}(-{b}y-x)$\n\n"
        f"$= -{3*a}x^2 + (-{b}) = -{3*a}x^2 - {b}$\n\n"
        f"This is always $< 0$ for all $(x,y)$ (since ${3*a}x^2 \\geq 0$ and ${b} > 0$).\n\n"
        "Since $\\nabla\\cdot\\mathbf{f}$ does not change sign, by Bendixson's criterion, "
        "there are **no closed orbits** in the entire plane."
    )
    return Problem("Bendixson's Criterion", stmt, sol)


def gen_lyapunov_estimate(rng: random.Random) -> Problem:
    # Simple 1D map: x_{n+1} = f(x), lambda = <ln|f'(x)|>
    r = sp.Rational(4, 1)  # logistic map at r=4 has lambda = ln(2)
    stmt = (
        "For the logistic map $x_{n+1} = 4x_n(1-x_n)$ (fully chaotic regime), "
        "the maximal Lyapunov exponent is known analytically. State its value and explain its meaning."
    )
    sol = (
        "For $r=4$, the logistic map is conjugate to the tent map, and:\n\n"
        "$\\lambda = \\ln 2 \\approx 0.693$\n\n"
        "This means nearby trajectories diverge exponentially: "
        "$|\\delta x_n| \\sim |\\delta x_0| \\cdot e^{\\lambda n} = |\\delta x_0| \\cdot 2^n$.\n\n"
        "After $n$ iterations, initial uncertainty is amplified by factor $2^n$. "
        "This is maximal chaos for the logistic map."
    )
    return Problem("Lyapunov Exponent (Logistic Map r=4)", stmt, sol)


GENERATORS = [
    gen_fixed_point_class, gen_lorenz_fixed_points, gen_logistic_map,
    gen_bendixson, gen_lyapunov_estimate, gen_fixed_point_class,
]


def main():
    parser = argparse.ArgumentParser(description="Generate chaos theory problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, chaos, nonlinear-dynamics, lyapunov]", "---", "",
             "# Practice: Non-linear Oscillators & Chaos Theory (4.8)", ""]
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

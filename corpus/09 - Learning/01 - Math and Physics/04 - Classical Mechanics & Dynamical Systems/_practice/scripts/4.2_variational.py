#!/usr/bin/env python3
"""
4.2_variational.py — Practice problem generator for Chapter 4.2
(Variational Calculus & Hamilton's Principle).

Archetypes:
  1. Euler-Lagrange for given integrand F(y, y')
  2. Beltrami identity application
  3. Brachistochrone parameter calculation
  4. Geodesic on a surface
  5. Functional with constraint (isoperimetric)
  6. Verify a given extremal satisfies E-L

Usage:
  python 4.2_variational.py --count 8 --seed 42
"""
from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

x, y, yp = sp.symbols('x y y\'', real=True)
ypp = sp.Symbol("y''", real=True)


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


def gen_euler_lagrange(rng: random.Random) -> Problem:
    """Generate E-L equation for a polynomial integrand."""
    a = rng.randint(1, 5)
    b = rng.randint(1, 4)
    # F = a*y'^2 + b*y^2
    ys, yps = sp.symbols('y yp', real=True)
    F = a * yps**2 + b * ys**2
    dFdy = sp.diff(F, ys)
    dFdyp = sp.diff(F, yps)
    # E-L: dF/dy - d/dx(dF/dy') = 0 => 2by - d/dx(2a*y') = 2by - 2a*y'' = 0
    stmt = (
        f"Find the Euler-Lagrange equation for the functional "
        f"$J[y] = \\int_a^b ({a}y'^2 + {b}y^2)\\,dx$."
    )
    sol = (
        f"$F = {a}y'^2 + {b}y^2$\n\n"
        f"$\\frac{{\\partial F}}{{\\partial y}} = {2*b}y$\n\n"
        f"$\\frac{{\\partial F}}{{\\partial y'}} = {2*a}y'$\n\n"
        f"$\\frac{{d}}{{dx}}\\frac{{\\partial F}}{{\\partial y'}} = {2*a}y''$\n\n"
        f"Euler-Lagrange: ${2*b}y - {2*a}y'' = 0 \\implies y'' - \\frac{{{b}}}{{{a}}}y = 0$\n\n"
        f"Solution: $y = C_1 e^{{\\sqrt{{{b}/{a}}}\\,x}} + C_2 e^{{-\\sqrt{{{b}/{a}}}\\,x}}$"
    )
    return Problem("Euler-Lagrange Equation", stmt, sol)


def gen_beltrami(rng: random.Random) -> Problem:
    """Beltrami identity for F = sqrt(1 + y'^2) / y^n."""
    n = rng.choice([1, 2])
    stmt = (
        f"Apply the Beltrami identity to find the first integral of "
        f"$J[y] = \\int \\frac{{\\sqrt{{1+y'^2}}}}{{y^{n}}}\\,dx$ "
        f"(no explicit $x$-dependence)."
    )
    sol = (
        f"Since $\\partial F/\\partial x = 0$, Beltrami gives $F - y'\\frac{{\\partial F}}{{\\partial y'}} = C$.\n\n"
        f"$F = (1+y'^2)^{{1/2}} / y^{n}$\n\n"
        f"$\\frac{{\\partial F}}{{\\partial y'}} = \\frac{{y'}}{{y^{n}\\sqrt{{1+y'^2}}}}$\n\n"
        f"$F - y'F_{{y'}} = \\frac{{\\sqrt{{1+y'^2}}}}{{y^{n}}} - \\frac{{y'^2}}{{y^{n}\\sqrt{{1+y'^2}}}} = \\frac{{1}}{{y^{n}\\sqrt{{1+y'^2}}}} = C$\n\n"
        f"Therefore $y^{n}\\sqrt{{1+y'^2}} = 1/C = \\text{{const}}$."
    )
    return Problem("Beltrami Identity", stmt, sol)


def gen_brachistochrone_time(rng: random.Random) -> Problem:
    """Compute brachistochrone descent time for given height."""
    h = rng.randint(2, 10)
    g_val = sp.Rational(98, 10)
    # For brachistochrone from (0,0) to (x1, h) with y downward:
    # R = h/2 (for drop straight down, theta=pi), T = pi*sqrt(R/g) = pi*sqrt(h/(2g))
    # Actually for vertical drop: x1=0 is degenerate. Use general formula.
    # Time on cycloid: T = sqrt(2R/g) * theta_f where y_f = R(1-cos(theta_f))
    # For simplicity: full half-cycle (theta=pi), y=2R=h, so R=h/2
    R = sp.Rational(h, 2)
    T = sp.pi * sp.sqrt(R / g_val)
    stmt = (
        f"A bead slides from rest down a brachistochrone (cycloid) through a "
        f"vertical drop of $h = {h}$ m (to the lowest point, half-cycle). "
        f"Find the descent time. Use $g = 9.8$ m/s²."
    )
    sol = (
        f"For a half-cycle cycloid with vertical drop $h = 2R$: $R = h/2 = {sp.latex(R)}$ m.\n\n"
        f"Descent time: $T = \\pi\\sqrt{{R/g}} = \\pi\\sqrt{{{sp.latex(R)}/9.8}}$\n\n"
        f"$T = {sp.latex(T)} \\approx {float(T):.3f}$ s"
    )
    return Problem("Brachistochrone Descent Time", stmt, sol)


def gen_geodesic_sphere(rng: random.Random) -> Problem:
    """Show geodesics on a sphere are great circles."""
    stmt = (
        "Using the calculus of variations, show that the shortest path "
        "between two points on a sphere of radius $R$ is a great circle. "
        "Set up the arc-length functional in spherical coordinates $(\\theta, \\phi)$."
    )
    sol = (
        "Arc length on sphere: $ds^2 = R^2(d\\theta^2 + \\sin^2\\theta\\,d\\phi^2)$.\n\n"
        "Parameterize by $\\theta$: $s = R\\int\\sqrt{1 + \\sin^2\\theta\\,(d\\phi/d\\theta)^2}\\,d\\theta$.\n\n"
        "$F = \\sqrt{1 + \\sin^2\\theta\\,\\phi'^2}$ has no explicit $\\phi$ dependence (if we use $\\theta$ as parameter).\n\n"
        "Wait — $F$ depends on $\\theta$ explicitly. Use E-L directly:\n\n"
        "$\\frac{\\partial F}{\\partial \\phi} = 0$ (cyclic!), so $\\frac{\\partial F}{\\partial \\phi'} = \\frac{\\sin^2\\theta\\,\\phi'}{\\sqrt{1+\\sin^2\\theta\\,\\phi'^2}} = C$.\n\n"
        "This gives $\\sin^2\\theta\\,\\phi' = C\\sqrt{1+\\sin^2\\theta\\,\\phi'^2}$.\n\n"
        "Squaring and solving: the solution is a great circle (plane through center intersects sphere)."
    )
    return Problem("Geodesic on a Sphere", stmt, sol)


def gen_verify_extremal(rng: random.Random) -> Problem:
    """Verify that y = cosh(x/c) satisfies E-L for catenary."""
    c = rng.randint(1, 5)
    stmt = (
        f"Verify that $y(x) = {c}\\cosh(x/{c})$ is an extremal of "
        f"$J[y] = \\int y\\sqrt{{1+y'^2}}\\,dx$."
    )
    sol = (
        f"$y = {c}\\cosh(x/{c})$, $y' = \\sinh(x/{c})$, $y'' = \\frac{{1}}{{{c}}}\\cosh(x/{c})$.\n\n"
        f"$F = y\\sqrt{{1+y'^2}}$. Since no explicit $x$: use Beltrami.\n\n"
        f"$\\frac{{y}}{{\\sqrt{{1+y'^2}}}} = C$.\n\n"
        f"Check: $\\frac{{{c}\\cosh(x/{c})}}{{\\sqrt{{1+\\sinh^2(x/{c})}}}} = "
        f"\\frac{{{c}\\cosh(x/{c})}}{{\\cosh(x/{c})}} = {c} = C$ ✓"
    )
    return Problem("Verify Extremal (Catenary)", stmt, sol)


def gen_isoperimetric(rng: random.Random) -> Problem:
    """Isoperimetric problem: max area for given perimeter."""
    stmt = (
        "Find the curve $y(x)$ of fixed length $\\ell$ connecting $(0,0)$ to $(a,0)$ "
        "that encloses maximum area with the x-axis. Set up the constrained variational problem."
    )
    sol = (
        "Maximize $A = \\int_0^a y\\,dx$ subject to $\\int_0^a \\sqrt{1+y'^2}\\,dx = \\ell$.\n\n"
        "Lagrange multiplier: minimize $J = \\int_0^a [y - \\lambda\\sqrt{1+y'^2}]\\,dx$.\n\n"
        "$F = y - \\lambda\\sqrt{1+y'^2}$. E-L: $1 - \\frac{d}{dx}\\frac{-\\lambda y'}{\\sqrt{1+y'^2}} = 0$.\n\n"
        "$\\frac{d}{dx}\\frac{\\lambda y'}{\\sqrt{1+y'^2}} = 1$. Integrate: $\\frac{\\lambda y'}{\\sqrt{1+y'^2}} = x - x_0$.\n\n"
        "Solving: $(x-x_0)^2 + (y-y_0)^2 = \\lambda^2$ — a **circular arc**.\n\n"
        "The curve of maximum enclosed area for fixed perimeter is an arc of a circle."
    )
    return Problem("Isoperimetric Problem", stmt, sol)


GENERATORS = [
    gen_euler_lagrange, gen_beltrami, gen_brachistochrone_time,
    gen_geodesic_sphere, gen_verify_extremal, gen_isoperimetric,
]


def main():
    parser = argparse.ArgumentParser(description="Generate variational calculus problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, variational-calculus, hamiltons-principle]", "---", "",
             "# Practice: Variational Calculus & Hamilton's Principle (4.2)", ""]
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

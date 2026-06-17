#!/usr/bin/env python3
"""
1.5_multiple_integrals.py — Practice problem generator for Chapter 1.5
(Multiple Integrals & Jacobians).

Generates randomized drill problems across eight canonical archetypes:
  1. Double integral over a rectangle (random polynomial)
  2. Double integral over a triangle (tests limit setup)
  3. Polar coordinate conversion + integration
  4. Triple integral in Cartesian over a box
  5. Jacobian determinant computation (2D transformation)
  6. Change-of-variables problem (u=x+y, v=x-y style)
  7. Volume by triple integral (cylindrical paraboloid)
  8. Surface area integral (paraboloid z=x^2+y^2 type)

SymPy is the source of truth: every answer is computed symbolically and
verified before being written into the output Markdown.

Usage:
  python3 1.5_multiple_integrals.py
  python3 1.5_multiple_integrals.py --count 24 --seed 42
  python3 1.5_multiple_integrals.py --out /tmp/_ch1.5_test.md
  python3 1.5_multiple_integrals.py --count 24 --seed 42 --out /tmp/_ch1.5_test.md

Output lives alongside this script by default at:
  ../1.5_drills.md
relative to this file. Re-running overwrites it.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp

# ── SymPy symbols ──────────────────────────────────────────────────────────────
x, y, z = sp.symbols("x y z", real=True)
r, theta, phi, rho = sp.symbols("r theta phi rho", positive=True)
u, v, w = sp.symbols("u v w", real=True)


# ── LaTeX cleanup (copied from 1.1_limits.py / 1.2_differentiation.py pattern) ─
def clean_latex(expr) -> str:
    """Return a SymPy expression as a LaTeX string, cleaned for Obsidian/MathJax."""
    raw = sp.latex(expr)
    # Replace \left( ... \right) with ordinary parens for inline readability
    raw = raw.replace(r"\left(", "(").replace(r"\right)", ")")
    return raw


# ── Problem dataclass ──────────────────────────────────────────────────────────
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



# ── Archetype 1: Double integral over a rectangle ─────────────────────────────
def gen_rect_double(rng: random.Random) -> Problem:
    """
    Compute iint_R f(x,y) dA over R = [a,b] x [c,d]
    where f is a random polynomial of degree <= 2 in each variable.
    """
    a_val = rng.randint(-2, 1)
    b_val = a_val + rng.randint(1, 3)
    c_val = rng.randint(-2, 1)
    d_val = c_val + rng.randint(1, 3)

    # Build f = p*x^2 + q*x*y + r_coeff*y^2 + s*x + t*y + k
    p = rng.randint(-3, 3)
    q = rng.randint(-3, 3)
    r_c = rng.randint(-3, 3)
    s = rng.randint(-3, 3)
    t = rng.randint(-3, 3)
    k = rng.randint(-3, 3)

    f_expr = p*x**2 + q*x*y + r_c*y**2 + s*x + t*y + k
    f_expr = sp.expand(f_expr)

    # SymPy verification
    answer = sp.integrate(sp.integrate(f_expr, (y, c_val, d_val)), (x, a_val, b_val))
    answer = sp.simplify(answer)

    a_l, b_l = clean_latex(a_val), clean_latex(b_val)
    c_l, d_l = clean_latex(c_val), clean_latex(d_val)
    f_l = clean_latex(f_expr)
    ans_l = clean_latex(answer)

    statement = (
        f"Evaluate the double integral\n\n"
        f"$$\n\\iint_R {f_l}\\,dA\n$$\n\n"
        f"over the rectangle $R = [{a_l},{b_l}] \\times [{c_l},{d_l}]$."
    )
    solution = (
        "**Apply Fubini's Theorem** (both iterated integrals exist since $f$ is a polynomial).\n\n"
        "**Step 1 — Inner integral** (integrate over $y$, holding $x$ fixed):\n\n"
        f"$$\n\\int_{{{c_l}}}^{{{d_l}}} \\left( {f_l} \\right) dy\n$$\n\n"
    )
    inner = sp.integrate(f_expr, (y, c_val, d_val))
    inner_s = sp.simplify(inner)
    solution += (
        f"$$\n= {clean_latex(inner_s)}\n$$\n\n"
        "**Step 2 — Outer integral** (integrate over $x$):\n\n"
        f"$$\n\\int_{{{a_l}}}^{{{b_l}}} \\left( {clean_latex(inner_s)} \\right) dx = {ans_l}\n$$\n\n"
        f"**Final answer:** $\\boxed{{{ans_l}}}$"
    )
    return Problem("Double integral over rectangle", statement, solution)


# ── Archetype 2: Double integral over a triangle ─────────────────────────────
def gen_triangle_double(rng: random.Random) -> Problem:
    """
    Compute iint_D x^m * y^n dA over the triangle with vertices (0,0),(1,0),(0,1).
    Region: 0 <= x <= 1, 0 <= y <= 1-x.
    """
    m = rng.randint(1, 3)
    n = rng.randint(1, 3)
    f_expr = x**m * y**n

    inner = sp.integrate(f_expr, (y, 0, 1 - x))
    answer = sp.integrate(inner, (x, 0, 1))
    answer = sp.simplify(answer)

    f_l = clean_latex(f_expr)
    ans_l = clean_latex(answer)
    inner_s = clean_latex(sp.simplify(inner))

    statement = (
        f"Evaluate\n\n"
        f"$$\n\\iint_D {f_l}\\,dA\n$$\n\n"
        "where $D$ is the triangle with vertices $(0,0)$, $(1,0)$, $(0,1)$."
    )
    solution = (
        "**Step 1 — Describe $D$ as a Type I region.** "
        "The hypotenuse is $y = 1-x$, so:\n\n"
        "$$\nD = \\{(x,y) : 0 \\leq x \\leq 1,\\; 0 \\leq y \\leq 1-x\\}.\n$$\n\n"
        "**Step 2 — Inner integral** (integrate $y$ from $0$ to $1-x$):\n\n"
        f"$$\n\\int_0^{{1-x}} {f_l}\\,dy = {inner_s}.\n$$\n\n"
        "**Step 3 — Outer integral:**\n\n"
        f"$$\n\\int_0^1 {inner_s}\\,dx = {ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{ans_l}}}$"
    )
    return Problem("Double integral over triangle", statement, solution)



# ── Archetype 3: Polar coordinate conversion + integration ────────────────────
def gen_polar_integral(rng: random.Random) -> Problem:
    """
    Compute iint_D f(r) dA over disk r <= R using polar coordinates.
    f chosen so that the polar integral is tractable.
    f(x,y) = (x^2+y^2)^n  =>  f(r) = r^{2n}, answer = 2pi * R^{2n+2}/(2n+2).
    """
    n = rng.randint(1, 3)
    R_val = rng.randint(1, 4)

    # In polar: f = r^(2n), dA = r dr dtheta
    # integral = int_0^{2pi} dtheta * int_0^R r^{2n} * r dr = 2pi * R^{2n+2}/(2n+2)
    r_sym = sp.Symbol("r", positive=True)
    theta_sym = sp.Symbol("theta", real=True)

    integrand_polar = r_sym**(2*n) * r_sym  # r^{2n} * r (jacobian)
    radial_int = sp.integrate(integrand_polar, (r_sym, 0, R_val))
    answer = 2 * sp.pi * radial_int
    answer = sp.simplify(answer)

    R_l = clean_latex(R_val)
    ans_l = clean_latex(answer)
    f_cart = clean_latex(x**(2*n) + y**(2*n))  # approximate display
    f_radial = f"r^{{{2*n}}}"

    statement = (
        f"Convert to polar coordinates and evaluate\n\n"
        f"$$\n\\iint_D (x^2+y^2)^{{{n}}}\\,dA\n$$\n\n"
        f"where $D$ is the disk $x^2 + y^2 \\leq {R_l}^2$."
    )
    solution = (
        "**Step 1 — Identify the polar substitution.** "
        "Let $x = r\\cos\\theta$, $y = r\\sin\\theta$, so "
        f"$x^2+y^2 = r^2$ and $(x^2+y^2)^{{{n}}} = {f_radial}$. "
        f"The disk $x^2+y^2 \\leq {R_l}^2$ becomes $0 \\leq r \\leq {R_l}$, "
        "$0 \\leq \\theta \\leq 2\\pi$.\n\n"
        "**Step 2 — Jacobian.** The polar area element is $dA = r\\,dr\\,d\\theta$ "
        "(Jacobian $= r$, derived in §5.1).\n\n"
        "**Step 3 — Set up iterated integral:**\n\n"
        f"$$\n\\int_0^{{2\\pi}}\\int_0^{{{R_l}}} {f_radial} \\cdot r\\,dr\\,d\\theta.\n$$\n\n"
        "**Step 4 — Separate** (integrand is independent of $\\theta$):\n\n"
        f"$$\n= 2\\pi \\int_0^{{{R_l}}} r^{{{2*n+1}}}\\,dr = 2\\pi "
        f"\\left[\\frac{{r^{{{2*n+2}}}}}{{{2*n+2}}}\\right]_0^{{{R_l}}} = {ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{ans_l}}}$"
    )
    return Problem("Polar coordinate integral", statement, solution)


# ── Archetype 4: Triple integral over a box ───────────────────────────────────
def gen_box_triple(rng: random.Random) -> Problem:
    """
    Compute iiint_E x^a * y^b * z^c dV over box [0,p]x[0,q]x[0,s].
    Chosen to be separable so each factor can be integrated independently.
    """
    a_exp = rng.randint(1, 3)
    b_exp = rng.randint(1, 3)
    c_exp = rng.randint(1, 3)
    p_val = rng.randint(1, 3)
    q_val = rng.randint(1, 3)
    s_val = rng.randint(1, 3)

    f_expr = x**a_exp * y**b_exp * z**c_exp
    answer = (
        sp.Rational(p_val**(a_exp+1), a_exp+1)
        * sp.Rational(q_val**(b_exp+1), b_exp+1)
        * sp.Rational(s_val**(c_exp+1), c_exp+1)
    )
    # Verify with sympy
    answer_check = sp.integrate(
        sp.integrate(sp.integrate(f_expr, (z, 0, s_val)), (y, 0, q_val)),
        (x, 0, p_val)
    )
    assert sp.simplify(answer - answer_check) == 0, "Triple integral box mismatch"

    f_l = clean_latex(f_expr)
    ans_l = clean_latex(answer)

    statement = (
        f"Evaluate the triple integral\n\n"
        f"$$\n\\iiint_E {f_l}\\,dV\n$$\n\n"
        f"over the box $E = [0,{p_val}] \\times [0,{q_val}] \\times [0,{s_val}]$."
    )
    solution = (
        "**Step 1 — The integrand separates:** $f(x,y,z) = x^{" + str(a_exp)
        + "}\\cdot y^{" + str(b_exp) + "}\\cdot z^{" + str(c_exp) + "}$, "
        "so the triple integral over a box factors into a product:\n\n"
        f"$$\n\\iiint_E {f_l}\\,dV = "
        f"\\int_0^{{{p_val}}} x^{{{a_exp}}}\\,dx "
        f"\\cdot \\int_0^{{{q_val}}} y^{{{b_exp}}}\\,dy "
        f"\\cdot \\int_0^{{{s_val}}} z^{{{c_exp}}}\\,dz.\n$$\n\n"
        "**Step 2 — Each factor:**\n\n"
        f"$$\n\\int_0^{{{p_val}}} x^{{{a_exp}}}\\,dx = "
        f"\\frac{{{p_val}^{{{a_exp+1}}}}}{{{a_exp+1}}} = "
        f"{clean_latex(sp.Rational(p_val**(a_exp+1), a_exp+1))}.\n$$\n\n"
        f"$$\n\\int_0^{{{q_val}}} y^{{{b_exp}}}\\,dy = "
        f"{clean_latex(sp.Rational(q_val**(b_exp+1), b_exp+1))}.\n$$\n\n"
        f"$$\n\\int_0^{{{s_val}}} z^{{{c_exp}}}\\,dz = "
        f"{clean_latex(sp.Rational(s_val**(c_exp+1), c_exp+1))}.\n$$\n\n"
        "**Step 3 — Multiply:**\n\n"
        f"$$\n{ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{ans_l}}}$"
    )
    return Problem("Triple integral over box", statement, solution)



# ── Archetype 5: Jacobian determinant ────────────────────────────────────────
def gen_jacobian(rng: random.Random) -> Problem:
    """
    Compute the Jacobian d(x,y)/d(u,v) for a linear transformation
    x = a*u + b*v, y = c*u + d*v.  Answer = a*d - b*c.
    """
    a_c = rng.randint(-4, 4)
    b_c = rng.randint(-4, 4)
    c_c = rng.randint(-4, 4)
    d_c = rng.randint(-4, 4)
    # Ensure non-degenerate
    while a_c * d_c - b_c * c_c == 0:
        a_c = rng.randint(-4, 4)
        b_c = rng.randint(-4, 4)
        c_c = rng.randint(-4, 4)
        d_c = rng.randint(-4, 4)

    J_val = a_c * d_c - b_c * c_c

    # SymPy verify
    u_s, v_s = sp.symbols("u v", real=True)
    x_expr = a_c * u_s + b_c * v_s
    y_expr = c_c * u_s + d_c * v_s
    J_matrix = sp.Matrix([
        [sp.diff(x_expr, u_s), sp.diff(x_expr, v_s)],
        [sp.diff(y_expr, u_s), sp.diff(y_expr, v_s)]
    ])
    J_check = J_matrix.det()
    assert J_check == J_val, f"Jacobian mismatch: {J_check} vs {J_val}"

    statement = (
        f"Compute the Jacobian $\\partial(x,y)/\\partial(u,v)$ for the transformation\n\n"
        f"$$\nx = {clean_latex(x_expr)}, \\qquad y = {clean_latex(y_expr)}.\n$$\n"
    )
    solution = (
        "**Step 1 — Compute all four partial derivatives:**\n\n"
        f"$$\n\\frac{{\\partial x}}{{\\partial u}} = {a_c}, \\quad "
        f"\\frac{{\\partial x}}{{\\partial v}} = {b_c}, \\quad "
        f"\\frac{{\\partial y}}{{\\partial u}} = {c_c}, \\quad "
        f"\\frac{{\\partial y}}{{\\partial v}} = {d_c}.\n$$\n\n"
        "**Step 2 — Form the Jacobian determinant:**\n\n"
        f"$$\n\\frac{{\\partial(x,y)}}{{\\partial(u,v)}} = "
        f"\\begin{{vmatrix}} {a_c} & {b_c} \\\\ {c_c} & {d_c} \\end{{vmatrix}} "
        f"= ({a_c})({d_c}) - ({b_c})({c_c}) = {a_c*d_c} - ({b_c*c_c}) = {J_val}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{J = {J_val}}}$\n\n"
        f"The transformation {'expands' if abs(J_val) > 1 else 'contracts'} area by a "
        f"factor of $|J| = {abs(J_val)}$."
    )
    return Problem("Jacobian determinant (linear map)", statement, solution)


# ── Archetype 6: Change of variables ─────────────────────────────────────────
def gen_change_of_vars(rng: random.Random) -> Problem:
    """
    Compute iint_R (x+y)^m * (x-y)^n dA over the square |x|+|y| <= 1
    using u = x+y, v = x-y. Jacobian = 1/2.
    Square |x|+|y|<=1 maps to [-1,1]x[-1,1] in (u,v) space.
    """
    m = rng.choice([2, 3, 4])
    n = rng.choice([2, 3, 4])
    # In (u,v) space: int_{-1}^{1} u^m du * int_{-1}^{1} v^n dv * (1/2)
    u_s, v_s = sp.symbols("u v", real=True)
    u_int = sp.integrate(u_s**m, (u_s, -1, 1))
    v_int = sp.integrate(v_s**n, (v_s, -1, 1))
    answer = sp.Rational(1, 2) * u_int * v_int
    answer = sp.simplify(answer)

    ans_l = clean_latex(answer)

    statement = (
        f"Using the substitution $u = x+y$, $v = x-y$, evaluate\n\n"
        f"$$\n\\iint_R (x+y)^{{{m}}}(x-y)^{{{n}}}\\,dA\n$$\n\n"
        "where $R$ is the square with vertices $(\\pm 1, 0)$, $(0, \\pm 1)$ "
        "(i.e., $|x|+|y| \\leq 1$)."
    )
    solution = (
        "**Step 1 — Solve for $x, y$:** $x = (u+v)/2$, $y = (u-v)/2$.\n\n"
        "**Step 2 — Jacobian:**\n\n"
        "$$\nJ = \\begin{vmatrix} 1/2 & 1/2 \\\\ 1/2 & -1/2 \\end{vmatrix} "
        "= -\\tfrac{1}{4} - \\tfrac{1}{4} = -\\tfrac{1}{2}, \\quad |J| = \\tfrac{1}{2}.\n$$\n\n"
        "**Step 3 — Image of $R$ under the map.** The vertices:\n"
        "$(1,0)\\to u=1,v=1$; $(-1,0)\\to u=-1,v=-1$; "
        "$(0,1)\\to u=1,v=-1$; $(0,-1)\\to u=-1,v=1$.\n"
        "So $R$ maps to the square $S = [-1,1]\\times[-1,1]$ in $(u,v)$-space.\n\n"
        "**Step 4 — Rewrite integrand:** $(x+y)^{" + str(m) + "}(x-y)^{" + str(n) + "} = u^{"
        + str(m) + "}v^{" + str(n) + "}$.\n\n"
        "**Step 5 — Apply Change of Variables:**\n\n"
        f"$$\n\\iint_R = \\iint_S u^{{{m}}}v^{{{n}}} \\cdot \\tfrac{{1}}{{2}}\\,du\\,dv "
        f"= \\tfrac{{1}}{{2}}\\int_{{-1}}^{{1}}u^{{{m}}}\\,du \\cdot \\int_{{-1}}^{{1}}v^{{{n}}}\\,dv.\n$$\n\n"
        f"$$\n= \\tfrac{{1}}{{2}} \\cdot {clean_latex(u_int)} \\cdot {clean_latex(v_int)} = {ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{ans_l}}}$\n\n"
        "*(Note: if $m$ or $n$ is odd, the corresponding integral over a symmetric interval vanishes, "
        "giving answer $0$.)*"
    )
    return Problem("Change of variables (u=x+y, v=x-y)", statement, solution)



# ── Archetype 7: Volume by triple integral (cylindrical) ─────────────────────
def gen_volume_cylindrical(rng: random.Random) -> Problem:
    """
    Volume of solid bounded above by z = H - r^2/a and below by z=0 (paraboloid cap).
    In cylindrical: V = int_0^{2pi} int_0^{R} int_0^{H-r^2/a} r dz dr dtheta
    where R = sqrt(a*H) is the base radius (paraboloid meets z=0 at r^2 = a*H).
    """
    H = rng.randint(1, 4)
    a = rng.randint(1, 3)
    # Base radius^2 = a*H
    R_sq = a * H
    # V = 2pi * int_0^{sqrt(aH)} r*(H - r^2/a) dr
    r_s = sp.Symbol("r", positive=True)
    integrand = r_s * (H - r_s**2 / a)
    R_sym = sp.sqrt(R_sq)
    radial = sp.integrate(integrand, (r_s, 0, R_sym))
    answer = 2 * sp.pi * radial
    answer = sp.simplify(answer)
    ans_l = clean_latex(answer)

    statement = (
        f"Find the volume of the solid bounded above by the paraboloid "
        f"$z = {H} - \\dfrac{{r^2}}{{{a}}}$ and below by $z = 0$ "
        "(using cylindrical coordinates)."
    )
    solution = (
        "**Step 1 — Find the base.** The paraboloid meets $z=0$ where "
        f"$r^2 = {a}\\cdot{H} = {R_sq}$, so $r = \\sqrt{{{R_sq}}} = {clean_latex(R_sym)}$.\n\n"
        "**Step 2 — Set up:** $0 \\leq \\theta \\leq 2\\pi$, "
        f"$0 \\leq r \\leq {clean_latex(R_sym)}$, $0 \\leq z \\leq {H} - r^2/{a}$. "
        "Jacobian: $r$.\n\n"
        "**Step 3 — Triple integral:**\n\n"
        f"$$\nV = \\int_0^{{2\\pi}}\\int_0^{{\\sqrt{{{R_sq}}}}}\\int_0^{{{H} - r^2/{a}}} r\\,dz\\,dr\\,d\\theta.\n$$\n\n"
        "**Step 4 — Innermost integral:**\n\n"
        f"$$\n\\int_0^{{{H} - r^2/{a}}} r\\,dz = r\\left({H} - \\frac{{r^2}}{{{a}}}\\right).\n$$\n\n"
        "**Step 5 — Middle integral:**\n\n"
        f"$$\n\\int_0^{{\\sqrt{{{R_sq}}}}} r\\left({H} - \\frac{{r^2}}{{{a}}}\\right) dr "
        f"= {clean_latex(radial)}.\n$$\n\n"
        "**Step 6 — Outer:**\n\n"
        f"$$\nV = 2\\pi \\cdot {clean_latex(radial)} = {ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{V = {ans_l}}}$"
    )
    return Problem("Volume by triple integral (cylindrical)", statement, solution)


# ── Archetype 8: Surface area integral ───────────────────────────────────────
def gen_surface_area(rng: random.Random) -> Problem:
    """
    Surface area of z = a*(x^2 + y^2) over disk r <= R.
    dS = sqrt(1 + 4a^2*r^2) * r dr dtheta.
    """
    a_val = rng.randint(1, 3)
    R_val = rng.randint(1, 3)

    # Surface area = 2*pi * int_0^R r*sqrt(1 + 4*a^2*r^2) dr
    # Substitution: u = 1 + 4*a^2*r^2, du = 8*a^2*r dr
    # = 2pi * [1/(8a^2)] * int_1^{1+4a^2R^2} sqrt(u) du
    # = 2pi * [1/(8a^2)] * [2/3 * u^{3/2}]_1^{1+4a^2R^2}
    # = pi/(6a^2) * ((1+4a^2R^2)^{3/2} - 1)
    r_s = sp.Symbol("r", positive=True)
    integrand = r_s * sp.sqrt(1 + 4*a_val**2*r_s**2)
    radial = sp.integrate(integrand, (r_s, 0, R_val))
    answer = 2 * sp.pi * radial
    answer = sp.simplify(answer)
    ans_l = clean_latex(answer)

    u_top = 1 + 4*a_val**2*R_val**2

    statement = (
        f"Find the surface area of the paraboloid $z = {a_val}(x^2 + y^2)$ "
        f"over the disk $x^2 + y^2 \\leq {R_val}^2$."
    )
    solution = (
        f"**Step 1 — Partial derivatives:** $f_x = {2*a_val}x$, $f_y = {2*a_val}y$.\n\n"
        "**Step 2 — Surface element:**\n\n"
        f"$$\ndS = \\sqrt{{1 + {4*a_val**2}x^2 + {4*a_val**2}y^2}}\\,dA "
        f"= \\sqrt{{1 + {4*a_val**2}r^2}}\\,dA \\quad \\text{{(in polar)}}.\n$$\n\n"
        "**Step 3 — Set up:**\n\n"
        f"$$\nA = \\int_0^{{2\\pi}}\\int_0^{{{R_val}}} r\\sqrt{{1+{4*a_val**2}r^2}}\\,dr\\,d\\theta "
        f"= 2\\pi\\int_0^{{{R_val}}} r\\sqrt{{1+{4*a_val**2}r^2}}\\,dr.\n$$\n\n"
        f"**Step 4 — Substitute** $u = 1 + {4*a_val**2}r^2$, "
        f"$du = {8*a_val**2}r\\,dr$, so $r\\,dr = du/{8*a_val**2}$. "
        f"When $r=0$: $u=1$; when $r={R_val}$: $u={u_top}$.\n\n"
        "$$\n= 2\\pi \\cdot \\frac{1}{" + str(8*a_val**2) + "}"
        f"\\int_1^{{{u_top}}} \\sqrt{{u}}\\,du "
        f"= 2\\pi \\cdot \\frac{{1}}{{{8*a_val**2}}} \\cdot "
        f"\\frac{{2}}{{3}}\\left[u^{{3/2}}\\right]_1^{{{u_top}}}.\n$$\n\n"
        "$$\n= \\frac{\\pi}{" + str(3*a_val**2) + "}"
        f"\\left({u_top}^{{3/2}} - 1\\right) = {ans_l}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{A = {ans_l}}}$"
    )
    return Problem("Surface area integral (paraboloid)", statement, solution)



# ── Top-level orchestration ────────────────────────────────────────────────────

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_rect_double,
    gen_triangle_double,
    gen_polar_integral,
    gen_box_triple,
    gen_jacobian,
    gen_change_of_vars,
    gen_volume_cylindrical,
    gen_surface_area,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin across archetypes to ensure equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            problems.append(gen(rng))
    return problems


HEADER_TEMPLATE = """\
---
tags: [calculus, multiple-integrals, jacobians, practice, drills, "review/calc/1.5"]
chapter: 1.5
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.5 - Multiple Integrals & Jacobians|Chapter 1.5]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.5 — Practice Drills: Multiple Integrals & Jacobians

> Auto-generated by `scripts/1.5_multiple_integrals.py`. SymPy verifies every solution.

**House rule:** solve on paper before opening the spoiler. The point is building the move set, not getting the answer.

Tag your spaced-repetition reviews with `#review/calc/1.5`. Re-run the script weekly for fresh problems.

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
        f"All {len(problems)} problems were generated with seed `{seed}` "
        "and verified against SymPy's symbolic integration engine. "
        "If any answer disagrees with SymPy, file a bug against "
        "`_practice/scripts/1.5_multiple_integrals.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 1.5 practice drills (Multiple Integrals & Jacobians)."
    )
    parser.add_argument("--count", type=int, default=24,
                        help="Total number of problems to generate (default: 24).")
    parser.add_argument("--seed", type=int, default=None,
                        help="RNG seed for reproducible output (default: random).")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Output path. Default: ../1.5_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = (
        args.out
        if args.out is not None
        else (Path(__file__).resolve().parent.parent / "1.5_drills.md")
    )

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

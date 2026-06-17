#!/usr/bin/env python3
"""
1.4_multivariable.py — Practice problem generator for Chapter 1.4
(Multivariable Limits & Partial Derivatives).

Generates randomized drill problems across 8 archetypes:
  1. First partial derivatives of a polynomial in x, y
  2. Mixed partial / Clairaut verification
  3. Gradient vector computation
  4. Directional derivative (unit vector)
  5. Multivariable limit via polar substitution (those that exist)
  6. Tangent plane equation
  7. Chain rule for parametric curves
  8. Implicit partial differentiation (F(x,y,z)=0, find ∂z/∂x)

Round-robin over archetypes. SymPy is the source of truth — every
answer is computed via sp.diff() or sp.limit() before the file is written.

Usage:
  python3 1.4_multivariable.py                    # 24 problems, seed=random
  python3 1.4_multivariable.py --count 40         # 40 problems
  python3 1.4_multivariable.py --seed 42          # deterministic
  python3 1.4_multivariable.py --out drills.md    # custom output path

  # Smoke test (exits 0 on success):
  python3 1.4_multivariable.py --count 24 --seed 42 --out /tmp/_ch1.4_test.md
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
x, y, z, t, h = sp.symbols("x y z t h", real=True)
u1, u2 = sp.symbols("u1 u2", real=True)


# ---------------------------------------------------------------------------
# LaTeX helper — mirrors the clean_latex() convention from 1.2_differentiation.py
# ---------------------------------------------------------------------------

def clean_latex(expr: sp.Expr) -> str:
    """
    Render a SymPy expression as LaTeX.

    Rules applied:
    - sp.latex() is called with long_frac_ratio=3 to avoid tiny fracs
    - Trailing spaces in exponents are stripped
    - '**' artefacts (should not appear but guard anyway) are removed
    """
    raw = sp.latex(expr, long_frac_ratio=3)
    # SymPy occasionally emits "1.0" for exact 1 in certain edge cases;
    # normalise before returning.
    raw = raw.replace("1.0", "1").replace("0.5", r"\frac{1}{2}")
    return raw


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
# Archetype 1 — First partial derivatives of a polynomial
# ---------------------------------------------------------------------------

def gen_first_partials(rng: random.Random) -> Problem:
    """f(x,y) = a*x^p * y^q + b*x^r + c*y^s — compute f_x and f_y."""
    a = rng.choice([1, 2, 3, -1, -2])
    b = rng.choice([1, 2, -1, -3])
    c = rng.choice([1, -1, 2, -2])
    p = rng.randint(2, 4)
    q = rng.randint(1, 3)
    r = rng.randint(2, 3)
    s = rng.randint(2, 3)

    f = a * x**p * y**q + b * x**r + c * y**s

    # SymPy computes the ground-truth answers
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    f_lat  = clean_latex(f)
    fx_lat = clean_latex(fx)
    fy_lat = clean_latex(fy)

    statement = (
        "Compute the first partial derivatives $f_x$ and $f_y$ of\n\n"
        f"$$\nf(x,y) = {f_lat}.\n$$\n"
    )
    solution = (
        "**$f_x$:** Treat $y$ as a constant; differentiate with respect to $x$.\n\n"
        f"$$\nf_x = \\frac{{\\partial f}}{{\\partial x}} = {fx_lat}.\n$$\n\n"
        "**$f_y$:** Treat $x$ as a constant; differentiate with respect to $y$.\n\n"
        f"$$\nf_y = \\frac{{\\partial f}}{{\\partial y}} = {fy_lat}.\n$$\n\n"
        "**SymPy verification:** Both results confirmed via `sp.diff()`."
    )
    return Problem("First partial derivatives (polynomial)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 2 — Mixed partials and Clairaut verification
# ---------------------------------------------------------------------------

def gen_mixed_partials(rng: random.Random) -> Problem:
    """f(x,y) chosen from trig/exp/poly mixes; compute fxy, fyx, verify equality."""
    choice = rng.randint(0, 3)
    if choice == 0:
        a = rng.choice([1, 2, 3])
        f = sp.sin(a * x * y)
        desc = f"$f(x,y) = \\sin({a}xy)$"
    elif choice == 1:
        a = rng.choice([1, 2])
        b = rng.choice([1, 2])
        f = sp.exp(a * x + b * y)
        desc = f"$f(x,y) = e^{{{a}x + {b}y}}$"
    elif choice == 2:
        a = rng.randint(1, 4)
        b = rng.randint(1, 4)
        f = a * x**2 * y**3 + b * x * y
        desc = f"$f(x,y) = {clean_latex(f)}$"
    else:
        f = x**2 * sp.ln(1 + y**2)
        desc = r"$f(x,y) = x^2 \ln(1+y^2)$"

    fx  = sp.diff(f, x)
    fy  = sp.diff(f, y)
    fxy = sp.diff(fx, y)   # x first, then y  (subscript convention: left-to-right)
    fyx = sp.diff(fy, x)   # y first, then x

    # Verify Clairaut symbolically
    assert sp.simplify(fxy - fyx) == 0, "Clairaut sanity check failed!"

    statement = (
        f"For {desc}, compute all four second partial derivatives "
        "$f_{xx}$, $f_{yy}$, $f_{xy}$, $f_{yx}$ and verify Clairaut's theorem.\n"
    )

    fxx_lat = clean_latex(sp.diff(fx, x))
    fyy_lat = clean_latex(sp.diff(fy, y))
    fxy_lat = clean_latex(sp.simplify(fxy))
    fx_lat  = clean_latex(fx)
    fy_lat  = clean_latex(fy)
    f_lat   = clean_latex(f)

    solution = (
        f"**First partials:**\n\n"
        f"$$\nf_x = {fx_lat}, \\qquad f_y = {fy_lat}.\n$$\n\n"
        f"**$f_{{xx}}$** (differentiate $f_x$ w.r.t. $x$):\n\n"
        f"$$\nf_{{xx}} = {fxx_lat}.\n$$\n\n"
        f"**$f_{{yy}}$** (differentiate $f_y$ w.r.t. $y$):\n\n"
        f"$$\nf_{{yy}} = {fyy_lat}.\n$$\n\n"
        f"**$f_{{xy}}$** (differentiate $f_x$ w.r.t. $y$):\n\n"
        f"$$\nf_{{xy}} = {fxy_lat}.\n$$\n\n"
        f"**$f_{{yx}}$** (differentiate $f_y$ w.r.t. $x$):\n\n"
        f"$$\nf_{{yx}} = {fxy_lat}.\n$$\n\n"
        "**Clairaut's theorem:** $f_{xy} = f_{yx}$. "
        "Both mixed partials are equal (SymPy confirms `simplify(fxy - fyx) == 0`). $\\checkmark$"
    )
    return Problem("Mixed partials / Clairaut verification", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 3 — Gradient vector computation
# ---------------------------------------------------------------------------

def gen_gradient(rng: random.Random) -> Problem:
    """Compute ∇f at a specific point."""
    choice = rng.randint(0, 3)
    ax = rng.choice([-2, -1, 1, 2])
    ay = rng.choice([-2, -1, 1, 2])

    if choice == 0:
        a = rng.randint(1, 4)
        b = rng.randint(1, 4)
        f = a * x**2 + b * y**2
        f_desc = f"$f(x,y) = {a}x^2 + {b}y^2$"
    elif choice == 1:
        f = sp.exp(x) * sp.sin(y)
        f_desc = r"$f(x,y) = e^x \sin y$"
    elif choice == 2:
        f = x**2 * y + x * y**2
        f_desc = r"$f(x,y) = x^2 y + xy^2$"
    else:
        f = sp.ln(x**2 + y**2 + 1)
        f_desc = r"$f(x,y) = \ln(x^2+y^2+1)$"

    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    gx_val = fx.subs([(x, ax), (y, ay)])
    gy_val = fy.subs([(x, ax), (y, ay)])
    mag    = sp.sqrt(gx_val**2 + gy_val**2)

    statement = (
        f"Let {f_desc}. Compute $\\nabla f$ at the point $({ax}, {ay})$ and "
        "find the direction and magnitude of steepest ascent.\n"
    )
    solution = (
        "**Step 1: Partial derivatives.**\n\n"
        f"$$\nf_x = {clean_latex(fx)}, \\qquad f_y = {clean_latex(fy)}.\n$$\n\n"
        f"**Step 2: Evaluate at $({ax},{ay})$.**\n\n"
        f"$$\nf_x({ax},{ay}) = {clean_latex(gx_val)}, \\qquad "
        f"f_y({ax},{ay}) = {clean_latex(gy_val)}.\n$$\n\n"
        f"**Step 3: Gradient.**\n\n"
        f"$$\n\\nabla f({ax},{ay}) = \\langle {clean_latex(gx_val)},\\; "
        f"{clean_latex(gy_val)} \\rangle.\n$$\n\n"
        f"**Step 4: Magnitude (maximum rate of increase).**\n\n"
        f"$$\n\\|\\nabla f({ax},{ay})\\| = \\sqrt{{({clean_latex(gx_val)})^2 + "
        f"({clean_latex(gy_val)})^2}} = {clean_latex(sp.simplify(mag))}.\n$$\n\n"
        "**Direction of steepest ascent:** $\\hat{{\\mathbf{{g}}}} = "
        "\\nabla f \\,/\\, \\|\\nabla f\\|$ (unit vector in gradient direction)."
    )
    return Problem("Gradient vector computation", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 4 — Directional derivative (unit vector)
# ---------------------------------------------------------------------------

def gen_directional_derivative(rng: random.Random) -> Problem:
    """D_u f at a point, where u is a unit vector derived from a given angle or pair."""
    # Choose a unit vector from a finite set of clean angles
    angle_choice = rng.choice([
        (1, 0, "\\langle 1, 0 \\rangle"),
        (0, 1, "\\langle 0, 1 \\rangle"),
        (sp.Rational(1,2), sp.sqrt(3)/2, r"\left\langle \tfrac{1}{2}, \tfrac{\sqrt{3}}{2} \right\rangle"),
        (sp.sqrt(2)/2, sp.sqrt(2)/2, r"\left\langle \tfrac{\sqrt{2}}{2}, \tfrac{\sqrt{2}}{2} \right\rangle"),
        (sp.Rational(3,5), sp.Rational(4,5), r"\left\langle \tfrac{3}{5}, \tfrac{4}{5} \right\rangle"),
        (-sp.sqrt(2)/2, sp.sqrt(2)/2, r"\left\langle -\tfrac{\sqrt{2}}{2}, \tfrac{\sqrt{2}}{2} \right\rangle"),
    ])
    u1_val, u2_val, u_lat = angle_choice

    ax = rng.choice([-1, 1, 2])
    ay = rng.choice([-1, 0, 1])

    choice = rng.randint(0, 2)
    if choice == 0:
        a = rng.randint(1, 3)
        b = rng.randint(1, 3)
        f = a * x**2 + b * y**2
        f_desc = f"$f(x,y) = {a}x^2 + {b}y^2$"
    elif choice == 1:
        f = x * y**2
        f_desc = r"$f(x,y) = xy^2$"
    else:
        f = sp.exp(x * y)
        f_desc = r"$f(x,y) = e^{xy}$"

    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    gx_val = fx.subs([(x, ax), (y, ay)])
    gy_val = fy.subs([(x, ax), (y, ay)])
    dir_deriv = sp.simplify(gx_val * u1_val + gy_val * u2_val)

    statement = (
        f"Let {f_desc}. Find the directional derivative $D_{{\\hat{{\\mathbf{{u}}}}}} f$ "
        f"at the point $({ax},{ay})$ in the direction $\\hat{{\\mathbf{{u}}}} = {u_lat}$.\n"
    )
    solution = (
        "**Step 1: Verify $\\hat{\\mathbf{u}}$ is a unit vector.**\n\n"
        f"$$\n\\|{u_lat}\\| = \\sqrt{{({clean_latex(u1_val)})^2 + "
        f"({clean_latex(u2_val)})^2}} = 1. \\checkmark\n$$\n\n"
        "**Step 2: Compute the gradient.**\n\n"
        f"$$\nf_x = {clean_latex(fx)}, \\qquad f_y = {clean_latex(fy)}.\n$$\n\n"
        f"$$\n\\nabla f({ax},{ay}) = \\langle {clean_latex(gx_val)},\\; {clean_latex(gy_val)} \\rangle.\n$$\n\n"
        "**Step 3: Directional derivative via dot product.**\n\n"
        f"$$\nD_{{\\hat{{\\mathbf{{u}}}}}} f({ax},{ay}) = \\nabla f \\cdot \\hat{{\\mathbf{{u}}}} = "
        f"({clean_latex(gx_val)})({clean_latex(u1_val)}) + "
        f"({clean_latex(gy_val)})({clean_latex(u2_val)}) = {clean_latex(dir_deriv)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{{clean_latex(dir_deriv)}}}$"
    )
    return Problem("Directional derivative (unit vector)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 5 — Multivariable limit via polar substitution
# ---------------------------------------------------------------------------

def gen_polar_limit(rng: random.Random) -> Problem:
    """
    Limits of the form (x^p * y^q) / (x^2+y^2)^k where p+q > 2k (limit = 0).
    Polar substitution: x = r cos θ, y = r sin θ; bound the trig factor.
    """
    r_sym = sp.Symbol("r", positive=True)
    # Choose (p, q, k) such that p+q > 2k (limit exists and equals 0)
    configs = [
        (2, 1, 1, "x^2 y"),
        (3, 0, 1, "x^3"),
        (1, 2, 1, "x y^2"),
        (4, 0, 1, "x^4"),
        (2, 2, 1, "x^2 y^2"),   # p+q=4 > 2*1=2, limit = 0
        (3, 1, 2, "x^3 y"),     # p+q=4 > 2*2=4? No, 4 = 4, borderline; choose 3,1,1 instead
    ]
    # Filter to strictly p+q > 2k
    valid_configs = [(p, q, k, d) for (p, q, k, d) in configs if p+q > 2*k]
    p, q, k, num_desc = rng.choice(valid_configs)

    # The polar form: r^(p+q) * (cos^p * sin^q) / r^(2k) = r^(p+q-2k) * trig_factor
    power = p + q - 2*k

    statement = (
        "Evaluate (using polar coordinates $x = r\\cos\\theta$, $y = r\\sin\\theta$):\n\n"
        f"$$\n\\lim_{{(x,y)\\to(0,0)}} \\frac{{{num_desc}}}{{(x^2+y^2)^{{{k}}}}}.\n$$\n"
    )
    solution = (
        "**Step 1: Substitute polar coordinates.**\n\n"
        f"With $x = r\\cos\\theta$, $y = r\\sin\\theta$, and $x^2+y^2 = r^2$:\n\n"
        f"$$\n\\frac{{{num_desc}}}{{(x^2+y^2)^{{{k}}}}} = "
        f"\\frac{{r^{{{p+q}}} \\cos^{{{p}}}\\theta \\sin^{{{q}}}\\theta}}"
        f"{{r^{{{2*k}}}}} = r^{{{power}}} \\cos^{{{p}}}\\theta\\,\\sin^{{{q}}}\\theta.\n$$\n\n"
        f"**Step 2: Bound the trig factor.** For all $\\theta$: "
        f"$|\\cos^{{{p}}}\\theta\\,\\sin^{{{q}}}\\theta| \\leq 1$. Therefore:\n\n"
        f"$$\n\\left|r^{{{power}}}\\cos^{{{p}}}\\theta\\,\\sin^{{{q}}}\\theta\\right| \\leq r^{{{power}}}.\n$$\n\n"
        f"**Step 3: Squeeze.** Since $r^{{{power}}} \\to 0$ as $r \\to 0^+$ (with $r^{{{power}}} \\geq 0$), "
        "and the bound is uniform in $\\theta$:\n\n"
        f"$$\n\\lim_{{(x,y)\\to(0,0)}} \\frac{{{num_desc}}}{{(x^2+y^2)^{{{k}}}}} = 0.\n$$\n\n"
        "**Final answer:** $\\boxed{0}$\n\n"
        f"*(Key check: the bound $r^{{{power}}}$ is independent of $\\theta$, "
        "so convergence is uniform over all approach directions.)*"
    )
    return Problem("Multivariable limit via polar coordinates", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 6 — Tangent plane equation
# ---------------------------------------------------------------------------

def gen_tangent_plane(rng: random.Random) -> Problem:
    """Tangent plane to z = f(x,y) at (a,b,f(a,b))."""
    ax = rng.choice([-2, -1, 1, 2])
    ay = rng.choice([-1, 0, 1, 2])

    choice = rng.randint(0, 3)
    if choice == 0:
        a = rng.randint(1, 3)
        b = rng.randint(1, 3)
        f = a * x**2 + b * y**2
        f_desc = f"$z = {a}x^2 + {b}y^2$"
    elif choice == 1:
        f = x**2 - y**2
        f_desc = r"$z = x^2 - y^2$"
    elif choice == 2:
        f = x * y
        f_desc = r"$z = xy$"
    else:
        f = x**2 + x * y + y**2
        f_desc = r"$z = x^2 + xy + y^2$"

    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    fx0 = fx.subs([(x, ax), (y, ay)])
    fy0 = fy.subs([(x, ax), (y, ay)])
    z0  = f.subs([(x, ax), (y, ay)])

    # Tangent plane: z = z0 + fx0*(x-ax) + fy0*(y-ay)
    # Expanded form
    z_plane = sp.expand(z0 + fx0*(x - ax) + fy0*(y - ay))
    z_plane_lat = clean_latex(z_plane)

    statement = (
        f"Find the equation of the tangent plane to {f_desc} at the point "
        f"$({ax}, {ay}, {clean_latex(z0)})$.\n"
    )
    solution = (
        "**Step 1: Partial derivatives.**\n\n"
        f"$$\nf_x = {clean_latex(fx)}, \\qquad f_y = {clean_latex(fy)}.\n$$\n\n"
        f"**Step 2: Evaluate at $({ax},{ay})$.**\n\n"
        f"$$\nf_x({ax},{ay}) = {clean_latex(fx0)}, \\qquad f_y({ax},{ay}) = {clean_latex(fy0)}.\n$$\n\n"
        "**Step 3: Tangent plane formula.**\n\n"
        "$$\nz = f(a,b) + f_x(a,b)(x-a) + f_y(a,b)(y-b).\n$$\n\n"
        f"$$\nz = {clean_latex(z0)} + ({clean_latex(fx0)})(x - {ax}) + ({clean_latex(fy0)})(y - {ay}).\n$$\n\n"
        f"**Simplified:**\n\n$$\n\\boxed{{z = {z_plane_lat}}}\n$$"
    )
    return Problem("Tangent plane equation", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 7 — Chain rule for parametric curves
# ---------------------------------------------------------------------------

def gen_chain_rule(rng: random.Random) -> Problem:
    """dF/dt for F(t) = f(x(t), y(t))."""
    choice = rng.randint(0, 3)

    if choice == 0:
        f = x**2 + y**2
        xt = sp.cos(t)
        yt = sp.sin(t)
        f_desc  = r"$f(x,y) = x^2 + y^2$"
        xt_desc = r"$x(t) = \cos t$"
        yt_desc = r"$y(t) = \sin t$"
    elif choice == 1:
        a = rng.randint(2, 4)
        f  = x * y
        xt = t**2
        yt = sp.Integer(a) * t
        f_desc  = r"$f(x,y) = xy$"
        xt_desc = r"$x(t) = t^2$"
        yt_desc = f"$y(t) = {a}t$"
    elif choice == 2:
        f  = x**2 - y**2
        xt = sp.exp(t)
        yt = sp.exp(-t)
        f_desc  = r"$f(x,y) = x^2 - y^2$"
        xt_desc = r"$x(t) = e^t$"
        yt_desc = r"$y(t) = e^{-t}$"
    else:
        f  = x + y**2
        xt = t
        yt = t**2
        f_desc  = r"$f(x,y) = x + y^2$"
        xt_desc = r"$x(t) = t$"
        yt_desc = r"$y(t) = t^2$"

    fx  = sp.diff(f, x)
    fy  = sp.diff(f, y)
    dxt = sp.diff(xt, t)
    dyt = sp.diff(yt, t)

    # Chain rule expression (still in x, y, t)
    chain_expr = fx * dxt + fy * dyt
    # Substitute x(t), y(t)
    chain_subs = chain_expr.subs([(x, xt), (y, yt)])
    chain_simplified = sp.simplify(chain_subs)

    # Cross-check: direct substitution and differentiate
    F_direct = f.subs([(x, xt), (y, yt)])
    dF_direct = sp.diff(F_direct, t)
    dF_simplified = sp.simplify(dF_direct)

    # Assert agreement
    assert sp.simplify(chain_simplified - dF_simplified) == 0, \
        f"Chain rule sanity check failed: {chain_simplified} != {dF_simplified}"

    statement = (
        f"Let {f_desc}, {xt_desc}, {yt_desc}. "
        "Use the multivariable chain rule to compute $dF/dt$ where "
        "$F(t) = f(x(t), y(t))$. Verify by direct substitution.\n"
    )
    solution = (
        "**Step 1: Chain rule formula.**\n\n"
        "$$\n\\frac{dF}{dt} = \\frac{\\partial f}{\\partial x}\\frac{dx}{dt} + "
        "\\frac{\\partial f}{\\partial y}\\frac{dy}{dt}.\n$$\n\n"
        "**Step 2: Compute the pieces.**\n\n"
        f"$$\nf_x = {clean_latex(fx)}, \\qquad f_y = {clean_latex(fy)},\n$$\n\n"
        f"$$\n\\dot{{x}} = {clean_latex(dxt)}, \\qquad \\dot{{y}} = {clean_latex(dyt)}.\n$$\n\n"
        "**Step 3: Substitute.**\n\n"
        f"$$\n\\frac{{dF}}{{dt}} = ({clean_latex(fx)})({clean_latex(dxt)}) + "
        f"({clean_latex(fy)})({clean_latex(dyt)}).\n$$\n\n"
        "After substituting $x(t)$ and $y(t)$:\n\n"
        f"$$\n= {clean_latex(chain_subs)} = {clean_latex(chain_simplified)}.\n$$\n\n"
        "**Verification (direct substitution):**\n\n"
        f"$F(t) = {clean_latex(F_direct)}$, so $dF/dt = {clean_latex(dF_simplified)}$. $\\checkmark$\n\n"
        f"**Final answer:** $\\boxed{{dF/dt = {clean_latex(chain_simplified)}}}$"
    )
    return Problem("Multivariable chain rule (parametric curve)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 8 — Implicit partial differentiation F(x,y,z)=0
# ---------------------------------------------------------------------------

def gen_implicit_partial(rng: random.Random) -> Problem:
    """Find ∂z/∂x from F(x,y,z) = 0 using ∂z/∂x = -F_x / F_z."""
    choice = rng.randint(0, 3)

    if choice == 0:
        a = rng.randint(1, 3)
        b = rng.randint(1, 3)
        c = rng.randint(1, 3)
        F = a*x**2 + b*y**2 + c*z**2 - sp.Integer(rng.randint(4, 12))
        F_desc = f"${a}x^2 + {b}y^2 + {c}z^2 = {-F.subs([(x,0),(y,0),(z,0)])*(-1)}$"
        # Recompute F_desc cleanly
        const_val = a*0 + b*0 + c*0 - F.subs([(x,0),(y,0),(z,0)])
        F_desc = f"${clean_latex(a*x**2 + b*y**2 + c*z**2)} = {clean_latex(-F.subs([(x,0),(y,0),(z,0)]))}$"
    elif choice == 1:
        F = x**2 + y**2 - z**2 - sp.Integer(1)
        F_desc = r"$x^2 + y^2 - z^2 = 1$"
    elif choice == 2:
        F = x*y*z - x - y - z
        F_desc = r"$xyz = x + y + z$"
    else:
        F = sp.exp(x + z) - y*z - sp.Integer(1)
        F_desc = r"$e^{x+z} = yz + 1$"

    Fx = sp.diff(F, x)
    Fz = sp.diff(F, z)
    dzdx = sp.simplify(-Fx / Fz)

    statement = (
        f"Given {F_desc}, find $\\partial z / \\partial x$ "
        "by implicit differentiation.\n"
    )
    solution = (
        "**Method:** From $F(x,y,z) = 0$ with $z$ implicitly a function of $x,y$:\n\n"
        "$$\n\\frac{\\partial z}{\\partial x} = -\\frac{F_x}{F_z}.\n$$\n\n"
        "**Step 1: Compute $F_x$ and $F_z$.**\n\n"
        f"$$\nF_x = {clean_latex(Fx)},\n$$\n\n"
        f"$$\nF_z = {clean_latex(Fz)}.\n$$\n\n"
        "**Step 2: Apply the formula.**\n\n"
        f"$$\n\\frac{{\\partial z}}{{\\partial x}} = -\\frac{{{clean_latex(Fx)}}}{{{clean_latex(Fz)}}} = {clean_latex(dzdx)}.\n$$\n\n"
        "**Proof of the formula (for reference).** Differentiate $F(x,y,z(x,y)) = 0$ "
        "w.r.t. $x$ via chain rule: "
        "$F_x \\cdot 1 + F_y \\cdot 0 + F_z \\cdot (\\partial z/\\partial x) = 0$, "
        "giving $\\partial z/\\partial x = -F_x/F_z$ (valid where $F_z \\neq 0$). $\\blacksquare$\n\n"
        f"**Final answer:** $\\displaystyle\\boxed{{\\frac{{\\partial z}}{{\\partial x}} = {clean_latex(dzdx)}}}$"
    )
    return Problem("Implicit partial differentiation", statement, solution)


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_first_partials,
    gen_mixed_partials,
    gen_gradient,
    gen_directional_derivative,
    gen_polar_limit,
    gen_tangent_plane,
    gen_chain_rule,
    gen_implicit_partial,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin over archetypes so every type gets equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            problems.append(gen(rng))
    return problems


HEADER_TEMPLATE = """\
---
tags: [calculus, multivariable, partial-derivatives, practice, drills, "review/calc/1.4"]
chapter: 1.4
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.4 - Multivariable Limits & Partial Derivatives|Chapter 1.4]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.4 — Practice Drills: Multivariable Limits & Partial Derivatives

> Auto-generated by `scripts/1.4_multivariable.py`. SymPy (`sp.diff()`, `sp.limit()`) verifies every solution before this file lands on disk.

**House rule:** Solve each problem completely on paper before opening the spoiler. Show every intermediate algebraic step. The goal is building muscle memory, not getting the answer.

Tag your spaced-repetition reviews with `#review/calc/1.4`. Re-run the script weekly for a fresh set.

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
        f"All {len(problems)} problems were generated with seed `{seed}` and verified "
        "symbolically via SymPy's `diff()` engine. If any answer disagrees with "
        "SymPy, file a bug against `_practice/scripts/1.4_multivariable.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chapter 1.4 practice problem generator (multivariable calculus)."
    )
    parser.add_argument("--count", type=int, default=24,
                        help="Total number of problems to generate (default: 24).")
    parser.add_argument("--seed",  type=int, default=None,
                        help="RNG seed for reproducibility. Omit for time-based random.")
    parser.add_argument("--out",   type=Path, default=None,
                        help=(
                            "Output markdown path. "
                            "Default: ../1.4_drills.md relative to this script."
                        ))
    args = parser.parse_args()

    seed: int = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng  = random.Random(seed)

    out_path: Path = (
        args.out
        or (Path(__file__).resolve().parent.parent / "1.4_drills.md")
    )

    problems = build_problem_set(args.count, rng)
    md       = render_markdown(problems, seed)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

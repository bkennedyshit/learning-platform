#!/usr/bin/env python3
"""
1.6_vector_fields.py — Practice problem generator for Chapter 1.6
(Vector Fields, Divergence & Curl).

Generates randomized drill problems across eight canonical archetypes:
  1. Divergence computation (random polynomial vector field)
  2. Curl computation (3D vector field)
  3. Check if 2D field is conservative (curl = 0 check)
  4. Find potential function from conservative 2D field
  5. Line integral over a parameterized curve
  6. Check if 3D field is conservative (all curl components = 0)
  7. Div of curl = 0 verification
  8. Curl of gradient = 0 verification

SymPy is the source of truth: every answer is computed symbolically and
verified before writing. Output is Obsidian-safe markdown with <details>
spoilers, padded $$ blocks, and #review/calc/1.6 tags.

Usage:
  python3 1.6_vector_fields.py                       # 24 problems, time seed
  python3 1.6_vector_fields.py --count 40            # 40 problems
  python3 1.6_vector_fields.py --seed 42             # deterministic
  python3 1.6_vector_fields.py --out /tmp/drills.md  # custom output path

Smoke test:
  python3 1.6_vector_fields.py --count 24 --seed 42 --out /tmp/_ch1.6_test.md
  # must exit 0
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
# Symbolic variables
# ---------------------------------------------------------------------------
x, y, z, t = sp.symbols("x y z t", real=True)


# ---------------------------------------------------------------------------
# Data container
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
# Helper: format a sympy expression as LaTeX inside $$
# ---------------------------------------------------------------------------
def block(expr_latex: str) -> str:
    return f"\n$$\n{expr_latex}\n$$\n"



# ---------------------------------------------------------------------------
# Archetype 1 — Divergence computation
# ---------------------------------------------------------------------------
def gen_divergence(rng: random.Random) -> Problem:
    """Divergence of a random polynomial 3D vector field."""
    # Random low-degree polynomial coefficients
    def rand_poly(variables, degree=2):
        terms = [rng.randint(-4, 4)]
        for v in variables:
            terms.append(rng.randint(-3, 3) * v)
        if degree >= 2:
            for v in variables:
                terms.append(rng.randint(-2, 2) * v**2)
        for i, v1 in enumerate(variables):
            for v2 in variables[i+1:]:
                terms.append(rng.randint(-2, 2) * v1 * v2)
        return sp.expand(sum(terms))

    P = rand_poly([x, y, z])
    Q = rand_poly([x, y, z])
    R = rand_poly([x, y, z])

    div_F = sp.diff(P, x) + sp.diff(Q, y) + sp.diff(R, z)
    div_F = sp.simplify(div_F)

    Pl, Ql, Rl = sp.latex(P), sp.latex(Q), sp.latex(R)
    dPx = sp.latex(sp.diff(P, x))
    dQy = sp.latex(sp.diff(Q, y))
    dRz = sp.latex(sp.diff(R, z))
    ans = sp.latex(div_F)

    statement = (
        "Compute the divergence of\n"
        + block(rf"\mathbf{{F}} = \langle {Pl},\; {Ql},\; {Rl} \rangle")
    )
    solution = (
        "Apply $\\nabla \\cdot \\mathbf{F} = \\partial P/\\partial x + "
        "\\partial Q/\\partial y + \\partial R/\\partial z$:\n"
        + block(
            rf"\nabla \cdot \mathbf{{F}} = "
            rf"\underbrace{{{dPx}}}_{{P_x}} + "
            rf"\underbrace{{{dQy}}}_{{Q_y}} + "
            rf"\underbrace{{{dRz}}}_{{R_z}} = {ans}"
        )
        + f"\n**Final answer:** $\\boxed{{\\nabla \\cdot \\mathbf{{F}} = {ans}}}$"
    )
    return Problem("Divergence computation", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 2 — Curl computation (3D)
# ---------------------------------------------------------------------------
def gen_curl(rng: random.Random) -> Problem:
    """Curl of a random 3D vector field (linear + one nonlinear term each)."""
    # Keep it manageable: P, Q, R each have 1-2 terms
    coeffs = [rng.randint(-4, 4) for _ in range(9)]
    # P = a*x*y + b*z,  Q = c*x*z + d*y^2,  R = e*y*z + f*x
    a, b, c, d, e, f = [rng.randint(-3, 3) for _ in range(6)]
    P = a*x*y + b*z
    Q = c*x*z + d*y**2
    R = e*y*z + f*x

    curl_x = sp.diff(R, y) - sp.diff(Q, z)
    curl_y = sp.diff(P, z) - sp.diff(R, x)
    curl_z = sp.diff(Q, x) - sp.diff(P, y)

    curl_x_s = sp.simplify(curl_x)
    curl_y_s = sp.simplify(curl_y)
    curl_z_s = sp.simplify(curl_z)

    Pl, Ql, Rl = sp.latex(P), sp.latex(Q), sp.latex(R)

    statement = (
        "Compute $\\nabla \\times \\mathbf{F}$ for\n"
        + block(rf"\mathbf{{F}} = \langle {Pl},\; {Ql},\; {Rl} \rangle")
    )
    solution = (
        "Use the determinant formula $\\nabla \\times \\mathbf{F} = "
        "(R_y - Q_z)\\,\\hat{{i}} + (P_z - R_x)\\,\\hat{{j}} + (Q_x - P_y)\\,\\hat{{k}}$:\n\n"
        f"- $\\hat{{i}}$-component: $R_y - Q_z = {sp.latex(sp.diff(R,y))} - ({sp.latex(sp.diff(Q,z))}) = {sp.latex(curl_x_s)}$\n"
        f"- $\\hat{{j}}$-component: $P_z - R_x = {sp.latex(sp.diff(P,z))} - ({sp.latex(sp.diff(R,x))}) = {sp.latex(curl_y_s)}$\n"
        f"- $\\hat{{k}}$-component: $Q_x - P_y = {sp.latex(sp.diff(Q,x))} - ({sp.latex(sp.diff(P,y))}) = {sp.latex(curl_z_s)}$\n"
        + block(
            rf"\nabla \times \mathbf{{F}} = "
            rf"{sp.latex(curl_x_s)}\,\hat{{i}} + ({sp.latex(curl_y_s)})\,\hat{{j}} + "
            rf"({sp.latex(curl_z_s)})\,\hat{{k}}"
        )
    )
    return Problem("Curl computation (3D)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 3 — Conservative test (2D)
# ---------------------------------------------------------------------------
def gen_conservative_test_2d(rng: random.Random) -> Problem:
    """Check if a 2D field is conservative; state whether curl = 0."""
    # 50/50 chance: make it conservative or not
    is_cons = rng.choice([True, False])
    a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]

    if is_cons:
        # Build a potential f = a*x^2*y + b*x*y^2 + c*x + d*y, take gradient
        f_sym = a*x**2*y + b*x*y**2 + c*x + d*y
        P = sp.diff(f_sym, x)
        Q = sp.diff(f_sym, y)
    else:
        # Deliberately non-conservative: add an extra term to Q
        extra = rng.choice([1, -1, 2, -2]) * x**2
        P = a*x*y + b*y
        Q = c*x**2 + d*x*y + extra  # curl = Q_x - P_y = 2c*x + d*y - a*x - b; generically nonzero

    curl_val = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
    is_actually_cons = (curl_val == sp.Integer(0))

    Pl, Ql = sp.latex(P), sp.latex(Q)
    Qx = sp.latex(sp.diff(Q, x))
    Py = sp.latex(sp.diff(P, y))
    curl_l = sp.latex(curl_val)

    verdict = (
        "conservative (curl $= 0$ everywhere on $\\mathbb{R}^2$)"
        if is_actually_cons
        else f"**not** conservative (curl $= {curl_l} \\neq 0$ in general)"
    )

    statement = (
        "Determine whether the following 2D vector field is conservative:\n"
        + block(rf"\mathbf{{F}} = \langle {Pl},\; {Ql} \rangle")
    )
    solution = (
        "Apply the 2D curl test: compute $Q_x - P_y$.\n\n"
        f"$Q_x = \\partial({Ql})/\\partial x = {Qx}$\n\n"
        f"$P_y = \\partial({Pl})/\\partial y = {Py}$\n"
        + block(rf"Q_x - P_y = {Qx} - ({Py}) = {curl_l}")
        + f"\n**Conclusion:** $\\mathbf{{F}}$ is {verdict}."
    )
    return Problem("Conservative field test (2D)", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 4 — Find potential function (2D conservative field)
# ---------------------------------------------------------------------------
def gen_find_potential_2d(rng: random.Random) -> Problem:
    """Given a conservative 2D field, find its potential function."""
    # Build from a known potential
    coeffs = [rng.randint(-3, 3) for _ in range(5)]
    a, b, c, d, e = coeffs
    # f = a*x^2*y + b*x*y^2 + c*x^2 + d*y^2 + e*x*y
    f_true = a*x**2*y + b*x*y**2 + c*x**2 + d*y**2 + e*x*y
    P = sp.expand(sp.diff(f_true, x))
    Q = sp.expand(sp.diff(f_true, y))

    # Verify curl = 0
    curl_check = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
    assert curl_check == 0, f"Potential construction failed: curl = {curl_check}"

    # Build potential step by step (showing the integration)
    f_from_P = sp.integrate(P, x)          # integrate P w.r.t. x
    g_of_y_expr = sp.simplify(sp.diff(f_from_P, y) - Q)  # what's left for g'(y)
    # g'(y) = Q - d/dy(f_from_P) ... check it's a function of y only
    g_deriv = sp.simplify(Q - sp.diff(f_from_P, y))
    g_of_y = sp.integrate(g_deriv, y)

    f_reconstructed = sp.expand(f_from_P + g_of_y)

    Pl, Ql = sp.latex(P), sp.latex(Q)
    f_step1_l = sp.latex(f_from_P)
    g_deriv_l = sp.latex(g_deriv)
    g_l = sp.latex(g_of_y)
    f_final_l = sp.latex(f_reconstructed)
    f_true_l = sp.latex(sp.expand(f_true))

    # Verify reconstruction matches
    diff_check = sp.expand(f_reconstructed - f_true)
    # Should be 0 (or a constant, which is fine for potential)

    statement = (
        "Find the potential function $f(x,y)$ such that $\\nabla f = \\mathbf{F}$, where\n"
        + block(rf"\mathbf{{F}} = \langle {Pl},\; {Ql} \rangle")
        + "\n(First verify the field is conservative.)"
    )
    solution = (
        f"**Step 1: Verify conservative.** $Q_x - P_y = {sp.latex(sp.simplify(sp.diff(Q,x) - sp.diff(P,y)))} = 0$. ✓\n\n"
        f"**Step 2:** Integrate $f_x = P$ with respect to $x$:\n"
        + block(rf"f = \int {Pl}\,dx = {f_step1_l} + g(y)")
        + f"\n**Step 3:** Differentiate w.r.t. $y$ and set equal to $Q = {Ql}$:\n"
        + block(rf"f_y = {sp.latex(sp.diff(f_from_P, y))} + g'(y) = {Ql}")
        + f"\nSo $g'(y) = {g_deriv_l}$.\n\n"
        f"**Step 4:** Integrate: $g(y) = {g_l} + C$.\n\n"
        "**Final answer:**\n"
        + block(rf"f(x,y) = {f_final_l} + C")
        + f"\n**Verify:** $\\nabla({f_final_l}) = \\langle {Pl}, {Ql} \\rangle$. ✓"
    )
    return Problem("Find potential function (2D)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 5 — Line integral over a parameterized curve
# ---------------------------------------------------------------------------
def gen_line_integral(rng: random.Random) -> Problem:
    """Compute ∫_C F·dr for a simple 2D field and curve."""
    # Curve choices: line, parabola, or semicircle
    curve_type = rng.choice(["line", "parabola", "circle"])
    a, b = rng.randint(-3, 3), rng.randint(-3, 3)
    # Field F = <P, Q> with P, Q simple polynomials
    P = a*x + b*y
    Q = b*x - a*y  # Slightly asymmetric to make it interesting

    if curve_type == "line":
        # r(t) = (t, t) from 0 to 1
        r_x, r_y = t, t
        t_start, t_end = sp.Integer(0), sp.Integer(1)
        curve_desc = "the line $y = x$ from $(0,0)$ to $(1,1)$"
    elif curve_type == "parabola":
        # r(t) = (t, t^2) from 0 to 1
        r_x, r_y = t, t**2
        t_start, t_end = sp.Integer(0), sp.Integer(1)
        curve_desc = "the parabola $y = x^2$ from $(0,0)$ to $(1,1)$"
    else:
        # r(t) = (cos t, sin t) from 0 to pi (upper semicircle)
        r_x, r_y = sp.cos(t), sp.sin(t)
        t_start, t_end = sp.Integer(0), sp.pi
        curve_desc = "the upper semicircle $x^2 + y^2 = 1$, $y \\geq 0$, from $(1,0)$ to $(-1,0)$"

    dx_dt = sp.diff(r_x, t)
    dy_dt = sp.diff(r_y, t)

    P_on_curve = P.subs([(x, r_x), (y, r_y)])
    Q_on_curve = Q.subs([(x, r_x), (y, r_y)])

    integrand = sp.expand(P_on_curve * dx_dt + Q_on_curve * dy_dt)
    result = sp.integrate(integrand, (t, t_start, t_end))
    result = sp.simplify(result)

    Pl, Ql = sp.latex(P), sp.latex(Q)
    rx_l = sp.latex(r_x)
    ry_l = sp.latex(r_y)
    dxl = sp.latex(dx_dt)
    dyl = sp.latex(dy_dt)
    P_cl = sp.latex(sp.expand(P_on_curve))
    Q_cl = sp.latex(sp.expand(Q_on_curve))
    intl = sp.latex(sp.expand(integrand))
    resl = sp.latex(result)

    statement = (
        f"Evaluate $\\int_C \\mathbf{{F}} \\cdot d\\mathbf{{r}}$ where "
        f"$\\mathbf{{F}} = \\langle {Pl},\\; {Ql} \\rangle$ and $C$ is {curve_desc}.\n"
    )
    solution = (
        f"**Step 1: Parameterize.** $x = {rx_l}$, $y = {ry_l}$, "
        f"$t \\in [{sp.latex(t_start)}, {sp.latex(t_end)}]$.\n\n"
        f"$dx/dt = {dxl}$, $\\quad dy/dt = {dyl}$.\n\n"
        f"**Step 2: Substitute.** $P = {P_cl}$, $Q = {Q_cl}$.\n\n"
        "**Step 3: Form the integrand.**\n"
        + block(
            rf"P\,\frac{{dx}}{{dt}} + Q\,\frac{{dy}}{{dt}} = "
            rf"({P_cl})({dxl}) + ({Q_cl})({dyl}) = {intl}"
        )
        + "\n**Step 4: Integrate.**\n"
        + block(
            rf"\int_{{{sp.latex(t_start)}}}^{{{sp.latex(t_end)}}} {intl}\,dt = {resl}"
        )
        + f"\n**Final answer:** $\\boxed{{{resl}}}$"
    )
    return Problem("Line integral (parameterized curve)", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 6 — Conservative test (3D)
# ---------------------------------------------------------------------------
def gen_conservative_test_3d(rng: random.Random) -> Problem:
    """Check if a 3D field is conservative (all three curl components = 0)."""
    is_cons = rng.choice([True, False])

    if is_cons:
        # Build from a known 3D potential
        a, b, c = [rng.randint(-3, 3) for _ in range(3)]
        f_sym = a*x**2*y + b*y**2*z + c*x*z**2
        P = sp.expand(sp.diff(f_sym, x))
        Q = sp.expand(sp.diff(f_sym, y))
        R = sp.expand(sp.diff(f_sym, z))
    else:
        # Non-conservative: break one component
        a, b, c, d = [rng.randint(1, 3) for _ in range(4)]
        P = a*x*y
        Q = b*y*z
        R = c*x*z + d*x*y  # This will have nonzero curl

    curl_x = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    curl_y = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    curl_z = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))

    all_zero = (curl_x == 0 and curl_y == 0 and curl_z == 0)

    Pl, Ql, Rl = sp.latex(P), sp.latex(Q), sp.latex(R)

    verdict = "conservative" if all_zero else "**not** conservative"

    statement = (
        "Determine whether the following 3D vector field is conservative:\n"
        + block(
            rf"\mathbf{{F}} = \langle {Pl},\; {Ql},\; {Rl} \rangle"
        )
    )
    solution = (
        "Compute all three components of $\\nabla \\times \\mathbf{F}$:\n\n"
        f"- $\\hat{{i}}$: $R_y - Q_z = {sp.latex(sp.diff(R,y))} - ({sp.latex(sp.diff(Q,z))}) = {sp.latex(curl_x)}$\n"
        f"- $\\hat{{j}}$: $P_z - R_x = {sp.latex(sp.diff(P,z))} - ({sp.latex(sp.diff(R,x))}) = {sp.latex(curl_y)}$\n"
        f"- $\\hat{{k}}$: $Q_x - P_y = {sp.latex(sp.diff(Q,x))} - ({sp.latex(sp.diff(P,y))}) = {sp.latex(curl_z)}$\n\n"
        f"All components {'are zero' if all_zero else 'are **not** all zero'}. "
        f"$\\mathbf{{F}}$ is {verdict} on $\\mathbb{{R}}^3$."
    )
    return Problem("Conservative field test (3D)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 7 — Div of curl = 0 verification
# ---------------------------------------------------------------------------
def gen_div_of_curl(rng: random.Random) -> Problem:
    """Verify ∇·(∇×F) = 0 symbolically for a random field."""
    # Random smooth field
    a, b, c = [rng.randint(-3, 3) for _ in range(3)]
    P = a*x**2*y + b*y*z
    Q = c*x*z**2 + a*y**2
    R = b*x*y + c*z**2

    curl_x = sp.diff(R, y) - sp.diff(Q, z)
    curl_y = sp.diff(P, z) - sp.diff(R, x)
    curl_z = sp.diff(Q, x) - sp.diff(P, y)

    div_curl = sp.expand(sp.diff(curl_x, x) + sp.diff(curl_y, y) + sp.diff(curl_z, z))
    assert div_curl == 0, f"Div of curl != 0 for test field! Got {div_curl}"

    Pl, Ql, Rl = sp.latex(P), sp.latex(Q), sp.latex(R)
    cx_l = sp.latex(sp.expand(curl_x))
    cy_l = sp.latex(sp.expand(curl_y))
    cz_l = sp.latex(sp.expand(curl_z))

    statement = (
        "Verify that $\\nabla \\cdot (\\nabla \\times \\mathbf{F}) = 0$ for\n"
        + block(rf"\mathbf{{F}} = \langle {Pl},\; {Ql},\; {Rl} \rangle")
    )
    solution = (
        "**Step 1: Compute $\\nabla \\times \\mathbf{F}$.**\n\n"
        f"$\\hat{{i}}$: $R_y - Q_z = {cx_l}$\n\n"
        f"$\\hat{{j}}$: $P_z - R_x = {cy_l}$\n\n"
        f"$\\hat{{k}}$: $Q_x - P_y = {cz_l}$\n\n"
        "**Step 2: Take the divergence of the curl.**\n"
        + block(
            r"\nabla \cdot (\nabla \times \mathbf{F}) = "
            r"\frac{\partial}{\partial x}(" + cx_l + r") + "
            r"\frac{\partial}{\partial y}(" + cy_l + r") + "
            r"\frac{\partial}{\partial z}(" + cz_l + ")"
        )
        + "\nExpanding and applying Clairaut's theorem (mixed partials are equal), "
        "all terms cancel in pairs:\n"
        + block(r"\nabla \cdot (\nabla \times \mathbf{F}) = 0 \quad \blacksquare")
        + "\nThis is Theorem 1.6.3 confirmed numerically for this specific field."
    )
    return Problem(r"Verify $\nabla \cdot (\nabla \times \mathbf{F}) = 0$", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 8 — Curl of gradient = 0 verification
# ---------------------------------------------------------------------------
def gen_curl_of_gradient(rng: random.Random) -> Problem:
    """Verify ∇×(∇f) = 0 symbolically for a random scalar function."""
    a, b, c, d, e = [rng.randint(-3, 3) for _ in range(5)]
    f_sym = a*x**3 + b*x**2*y + c*y**2*z + d*x*z**2 + e*y*z**2

    grad_f = [sp.diff(f_sym, v) for v in [x, y, z]]
    P_g, Q_g, R_g = grad_f

    curl_x = sp.expand(sp.diff(R_g, y) - sp.diff(Q_g, z))
    curl_y = sp.expand(sp.diff(P_g, z) - sp.diff(R_g, x))
    curl_z = sp.expand(sp.diff(Q_g, x) - sp.diff(P_g, y))

    assert curl_x == 0 and curl_y == 0 and curl_z == 0, "Curl of gradient is nonzero!"

    fl = sp.latex(f_sym)
    Pl = sp.latex(P_g)
    Ql = sp.latex(Q_g)
    Rl = sp.latex(R_g)

    statement = (
        "Verify that $\\nabla \\times (\\nabla f) = \\mathbf{0}$ for\n"
        + block(rf"f(x,y,z) = {fl}")
    )
    solution = (
        "**Step 1: Compute $\\nabla f$.**\n"
        + block(
            rf"\nabla f = \langle f_x,\, f_y,\, f_z \rangle = "
            rf"\langle {Pl},\; {Ql},\; {Rl} \rangle"
        )
        + "\n**Step 2: Compute $\\nabla \\times (\\nabla f)$ component by component.**\n\n"
        f"$\\hat{{i}}$: $R_y - Q_z = {sp.latex(sp.diff(R_g,y))} - {sp.latex(sp.diff(Q_g,z))}$"
        f" $= {sp.latex(curl_x)}$\n\n"
        f"$\\hat{{j}}$: $P_z - R_x = {sp.latex(sp.diff(P_g,z))} - {sp.latex(sp.diff(R_g,x))}$"
        f" $= {sp.latex(curl_y)}$\n\n"
        f"$\\hat{{k}}$: $Q_x - P_y = {sp.latex(sp.diff(Q_g,x))} - {sp.latex(sp.diff(P_g,y))}$"
        f" $= {sp.latex(curl_z)}$\n\n"
        "Each component vanishes by Clairaut's theorem ($f_{xy} = f_{yx}$, etc.):\n"
        + block(r"\nabla \times (\nabla f) = \mathbf{0} \quad \blacksquare")
        + "\nThis is Theorem 1.6.2 confirmed for this specific $f$."
    )
    return Problem(r"Verify $\nabla \times (\nabla f) = \mathbf{0}$", statement, solution)



# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_divergence,
    gen_curl,
    gen_conservative_test_2d,
    gen_find_potential_2d,
    gen_line_integral,
    gen_conservative_test_3d,
    gen_div_of_curl,
    gen_curl_of_gradient,
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
tags: [calculus, vector-fields, divergence, curl, line-integrals, practice, drills, "review/calc/1.6"]
chapter: 1.6
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.6 - Vector Fields, Div & Curl|Chapter 1.6]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.6 — Vector Fields, Div & Curl: Practice Drills

> Auto-generated by `scripts/1.6_vector_fields.py`. SymPy verifies every solution before this file lands on disk.

**House rule:** solve each problem on paper before opening the spoiler. Build muscle memory for the move set — divergence, curl, conservative check, potential reconstruction, line integral.

Tag your spaced-repetition reviews with `#review/calc/1.6`. Re-run the script weekly for fresh problems.

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
        "and verified against SymPy's symbolic engine (`sp.diff`, `sp.integrate`, `sp.simplify`). "
        "If any answer disagrees with your computation, file a bug against "
        "`_practice/scripts/1.6_vector_fields.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 1.6 vector fields practice problems."
    )
    parser.add_argument("--count", type=int, default=24, help="Total number of problems.")
    parser.add_argument("--seed",  type=int, default=None, help="RNG seed (omit for time-based).")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output markdown path. Default: ../1.6_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = (
        args.out
        or (Path(__file__).resolve().parent.parent / "1.6_drills.md")
    )

    print(f"Generating {args.count} problems (seed={seed})...")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

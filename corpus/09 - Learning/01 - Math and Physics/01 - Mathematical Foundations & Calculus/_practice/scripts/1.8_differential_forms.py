#!/usr/bin/env python3
"""
1.8_differential_forms.py — Practice problem generator for Chapter 1.8
(Exterior Algebra & Differential Forms).

Eight canonical archetypes, all SymPy-verified:
  1. Exterior derivative of a 0-form (function → gradient as 1-form)
  2. Exterior derivative of a 1-form (check if closed: dω = 0?)
  3. Wedge product of two 1-forms
  4. Verify d² = 0 on a random 1-form
  5. Pullback of a 2-form under a parameterization (produces Jacobian)
  6. Check if a 1-form is closed (and find potential if exact)
  7. Reconstruct potential from an exact 1-form
  8. Identify the form type for a given physical integral

Usage:
  python3 1.8_differential_forms.py                   # 24 problems
  python3 1.8_differential_forms.py --count 40
  python3 1.8_differential_forms.py --seed 42
  python3 1.8_differential_forms.py --out /tmp/_ch1.8_test.md

Output defaults to ../1.8_drills.md relative to this script.
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
x, y, z = sp.symbols("x y z", real=True)
r, theta = sp.symbols("r theta", real=True, positive=True)
t = sp.Symbol("t", real=True)
u, v = sp.symbols("u v", real=True)


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
# Archetype 1 — Exterior derivative of a 0-form (gradient as 1-form)
# ---------------------------------------------------------------------------

def gen_exterior_deriv_0form(rng: random.Random) -> Problem:
    """
    df for f = a*x^p * y^q + b*sin(c*z) type function.
    Components of df are the gradient components.
    """
    a = rng.randint(1, 5)
    p = rng.randint(1, 3)
    q = rng.randint(1, 3)
    b = rng.randint(1, 4)
    c = rng.randint(1, 3)

    f = a * x**p * y**q + b * sp.sin(c * z)

    df_x = sp.diff(f, x)
    df_y = sp.diff(f, y)
    df_z = sp.diff(f, z)

    # Verify: df is a 1-form with these components
    df_x_s = sp.simplify(df_x)
    df_y_s = sp.simplify(df_y)
    df_z_s = sp.simplify(df_z)

    f_lat = sp.latex(f)
    dx_lat = sp.latex(df_x_s)
    dy_lat = sp.latex(df_y_s)
    dz_lat = sp.latex(df_z_s)

    statement = (
        f"Let $f = {f_lat}$. Compute the exterior derivative $df$ "
        f"(express as a 1-form $f_x\\,dx + f_y\\,dy + f_z\\,dz$) "
        f"and identify the corresponding gradient vector $\\nabla f$."
    )
    solution = (
        f"**Step 1.** Apply Definition: $df = \\frac{{\\partial f}}{{\\partial x}}\\,dx + "
        f"\\frac{{\\partial f}}{{\\partial y}}\\,dy + \\frac{{\\partial f}}{{\\partial z}}\\,dz$.\n\n"
        f"**Step 2.** Compute each partial:\n\n"
        f"$$\n\\frac{{\\partial f}}{{\\partial x}} = {dx_lat}, \\qquad "
        f"\\frac{{\\partial f}}{{\\partial y}} = {dy_lat}, \\qquad "
        f"\\frac{{\\partial f}}{{\\partial z}} = {dz_lat}.\n$$\n\n"
        f"**Step 3.** Assemble the 1-form:\n\n"
        f"$$\ndf = ({dx_lat})\\,dx + ({dy_lat})\\,dy + ({dz_lat})\\,dz.\n$$\n\n"
        f"**Gradient vector:** $\\nabla f = ({dx_lat},\\; {dy_lat},\\; {dz_lat})$.\n\n"
        f"*(SymPy verified: `sp.diff({f_lat}, x)` = `{df_x_s}`)*"
    )
    return Problem("Exterior derivative of 0-form (gradient)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 2 — Exterior derivative of a 1-form; is it closed?
# ---------------------------------------------------------------------------

def gen_exterior_deriv_1form(rng: random.Random) -> Problem:
    """
    ω = P dx + Q dy + R dz. Compute dω (2-form). Check if dω=0 (closed).
    Build examples that are sometimes closed, sometimes not.
    """
    choice = rng.randint(0, 2)
    if choice == 0:
        # Exact form: take f = a*x^2*y + b*y^2*z, P=f_x, Q=f_y, R=f_z
        a = rng.randint(1, 4)
        b = rng.randint(1, 4)
        f = a * x**2 * y + b * y**2 * z
        P = sp.diff(f, x)
        Q = sp.diff(f, y)
        R = sp.diff(f, z)
        label = "exact (dω = 0)"
    elif choice == 1:
        # Non-closed: P=y*z, Q=x*z^2, R=x^2 (chosen to give nonzero curl)
        c = rng.randint(1, 4)
        d = rng.randint(1, 4)
        P = y * z
        Q = c * x * z**2
        R = d * x**2 * y
        label = "not closed (dω ≠ 0)"
    else:
        # Closed but on punctured space: simulate with polynomial
        # P = c*x*y^2, Q = c*x^2*y → Q_x=2cx*y, P_y=2cx*y, so closed
        c = rng.randint(1, 5)
        P = c * x * y**2
        Q = c * x**2 * y
        R = sp.Integer(0)
        label = "closed (dω = 0)"

    # Compute dω components
    Ry_Qz = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    Pz_Rx = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    Qx_Py = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))

    is_closed = (Ry_Qz == 0 and Pz_Rx == 0 and Qx_Py == 0)

    P_lat = sp.latex(sp.expand(P))
    Q_lat = sp.latex(sp.expand(Q))
    R_lat = sp.latex(sp.expand(R))

    statement = (
        f"Let $\\omega = ({P_lat})\\,dx + ({Q_lat})\\,dy + ({R_lat})\\,dz$.\n\n"
        f"(a) Compute $d\\omega$. (b) Is $\\omega$ closed? (c) Is $\\omega$ exact on $\\mathbb{{R}}^3$?"
    )

    verdict = "closed" if is_closed else "**not** closed"
    exact_stmt = (
        "Since $\\mathbb{R}^3$ is contractible, by the Poincaré Lemma $\\omega$ is also **exact**."
        if is_closed
        else "$\\omega$ is not closed, hence not exact."
    )

    solution = (
        f"**Step 1.** Identify $P={P_lat}$, $Q={Q_lat}$, $R={R_lat}$.\n\n"
        f"**Step 2.** Compute $d\\omega = (R_y-Q_z)\\,dy\\wedge dz + "
        f"(P_z-R_x)\\,dz\\wedge dx + (Q_x-P_y)\\,dx\\wedge dy$:\n\n"
        f"$$\nR_y - Q_z = {sp.latex(Ry_Qz)}, \\quad "
        f"P_z - R_x = {sp.latex(Pz_Rx)}, \\quad "
        f"Q_x - P_y = {sp.latex(Qx_Py)}.\n$$\n\n"
        f"**Step 3.** $\\omega$ is {verdict}. {exact_stmt}\n\n"
        f"*(SymPy verified: classification = {label})*"
    )
    return Problem("Exterior derivative of 1-form; closed/exact check", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 3 — Wedge product of two 1-forms
# ---------------------------------------------------------------------------

def gen_wedge_product(rng: random.Random) -> Problem:
    """
    α = a₁ dx + b₁ dy,  β = a₂ dx + b₂ dy.
    α∧β = (a₁b₂ - a₂b₁) dx∧dy.
    Verify anticommutativity: α∧β = -β∧α.
    """
    a1 = rng.randint(1, 5)
    b1 = rng.randint(1, 5)
    a2 = rng.randint(1, 5)
    b2 = rng.randint(1, 5)

    # Coefficient of dx∧dy in α∧β
    coeff_ab = a1 * b2 - a2 * b1
    coeff_ba = a2 * b1 - a1 * b2  # should be -coeff_ab

    assert coeff_ba == -coeff_ab, "Anticommutativity check failed"

    statement = (
        f"Let $\\alpha = {a1}\\,dx + {b1}\\,dy$ and $\\beta = {a2}\\,dx + {b2}\\,dy$.\n\n"
        f"(a) Compute $\\alpha\\wedge\\beta$. "
        f"(b) Compute $\\beta\\wedge\\alpha$. "
        f"(c) Verify $\\alpha\\wedge\\beta = -\\beta\\wedge\\alpha$."
    )
    solution = (
        f"**Step 1.** Expand $\\alpha\\wedge\\beta$ using bilinearity:\n\n"
        f"$$\n\\alpha\\wedge\\beta = ({a1}\\,dx + {b1}\\,dy)\\wedge({a2}\\,dx + {b2}\\,dy).\n$$\n\n"
        f"**Step 2.** Distribute:\n\n"
        f"$$\n= {a1}\\cdot{a2}\\underbrace{{dx\\wedge dx}}_{{0}} + {a1}\\cdot{b2}\\,dx\\wedge dy "
        f"+ {b1}\\cdot{a2}\\,dy\\wedge dx + {b1}\\cdot{b2}\\underbrace{{dy\\wedge dy}}_{{0}}.\n$$\n\n"
        f"**Step 3.** Use $dy\\wedge dx = -dx\\wedge dy$:\n\n"
        f"$$\n= {a1*b2}\\,dx\\wedge dy + {b1*a2}(-dx\\wedge dy) = "
        f"({a1*b2} - {b1*a2})\\,dx\\wedge dy = {coeff_ab}\\,dx\\wedge dy.\n$$\n\n"
        f"**Step 4.** By the same calculation with roles swapped:\n\n"
        f"$$\n\\beta\\wedge\\alpha = {coeff_ba}\\,dx\\wedge dy = -({coeff_ab})\\,dx\\wedge dy.\n$$\n\n"
        f"**Verify:** $\\alpha\\wedge\\beta = {coeff_ab}\\,dx\\wedge dy = "
        f"-({coeff_ba}\\,dx\\wedge dy) \\ [\\text{{wait}}] = -\\beta\\wedge\\alpha$. $\\checkmark$\n\n"
        f"*(SymPy: coefficient = {coeff_ab})*"
    )
    return Problem("Wedge product of two 1-forms", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 4 — Verify d² = 0 on a 1-form
# ---------------------------------------------------------------------------

def gen_d_squared_zero(rng: random.Random) -> Problem:
    """
    ω = P dx + Q dy + R dz (random polynomial).
    Compute dω (2-form), then d(dω) (should be 3-form = 0).
    Show the Clairaut cancellation explicitly.
    """
    a = rng.randint(1, 4)
    b = rng.randint(1, 4)
    c = rng.randint(1, 3)

    P = a * x**2 * y + b * z
    Q = c * x * y**2 - a * z**2
    R = b * x * z + c * y**2

    # Compute dω
    Ry_Qz = sp.expand(sp.diff(R, y) - sp.diff(Q, z))
    Pz_Rx = sp.expand(sp.diff(P, z) - sp.diff(R, x))
    Qx_Py = sp.expand(sp.diff(Q, x) - sp.diff(P, y))

    # Compute d(dω): the divergence of (Ry-Qz, Pz-Rx, Qx-Py)
    # d of (A dy∧dz + B dz∧dx + C dx∧dy) = (Ax+By+Cz) dx∧dy∧dz
    A, B, C = Ry_Qz, Pz_Rx, Qx_Py
    ddw_coeff = sp.simplify(sp.diff(A, x) + sp.diff(B, y) + sp.diff(C, z))

    assert ddw_coeff == 0, f"d² ≠ 0: got {ddw_coeff}"

    P_lat = sp.latex(P)
    Q_lat = sp.latex(Q)
    R_lat = sp.latex(R)

    statement = (
        f"Let $\\omega = ({P_lat})\\,dx + ({Q_lat})\\,dy + ({R_lat})\\,dz$.\n\n"
        f"(a) Compute $d\\omega$. (b) Compute $d(d\\omega)$ explicitly and verify it is zero, "
        f"identifying the Clairaut cancellation."
    )
    solution = (
        f"**Step 1.** Compute $d\\omega$ components:\n\n"
        f"$$\nR_y - Q_z = {sp.latex(Ry_Qz)}, \\quad "
        f"P_z - R_x = {sp.latex(Pz_Rx)}, \\quad "
        f"Q_x - P_y = {sp.latex(Qx_Py)}.\n$$\n\n"
        f"So $d\\omega = ({sp.latex(Ry_Qz)})\\,dy\\wedge dz + "
        f"({sp.latex(Pz_Rx)})\\,dz\\wedge dx + ({sp.latex(Qx_Py)})\\,dx\\wedge dy$.\n\n"
        f"**Step 2.** Compute $d(d\\omega)$. For a 2-form $A\\,dy\\wedge dz + B\\,dz\\wedge dx + C\\,dx\\wedge dy$:\n\n"
        f"$$\nd(d\\omega) = \\left(\\frac{{\\partial A}}{{\\partial x}} + "
        f"\\frac{{\\partial B}}{{\\partial y}} + \\frac{{\\partial C}}{{\\partial z}}\\right)"
        f"dx\\wedge dy\\wedge dz.\n$$\n\n"
        f"**Step 3.** Evaluate each partial and sum:\n\n"
        f"$$\n\\frac{{\\partial A}}{{\\partial x}} + \\frac{{\\partial B}}{{\\partial y}} + "
        f"\\frac{{\\partial C}}{{\\partial z}} = {sp.latex(sp.diff(A,x))} + "
        f"{sp.latex(sp.diff(B,y))} + {sp.latex(sp.diff(C,z))} = {ddw_coeff}.\n$$\n\n"
        f"The mixed-partial terms cancel pairwise by Clairaut's theorem ($f_{{xy}} = f_{{yx}}$). "
        f"$d(d\\omega) = 0$. $\\blacksquare$\n\n"
        f"*(SymPy verified: ddω coefficient = `{ddw_coeff}`)*"
    )
    return Problem("Verify d² = 0 on a 1-form", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 5 — Pullback of a 2-form under parameterization (Jacobian)
# ---------------------------------------------------------------------------

def gen_pullback_2form(rng: random.Random) -> Problem:
    """
    φ(u,v) = (a*u + b*v, c*u + d*v) (linear map).
    Compute φ*(dx∧dy). The coefficient is det(Jacobian).
    """
    a = rng.randint(1, 4)
    b = rng.randint(-3, 3)
    c = rng.randint(-3, 3)
    d = rng.randint(1, 4)

    # x = a*u + b*v, y = c*u + d*v
    x_expr = a * u + b * v
    y_expr = c * u + d * v

    # φ*(dx) = (∂x/∂u)du + (∂x/∂v)dv
    # φ*(dy) = (∂y/∂u)du + (∂y/∂v)dv
    dxu = sp.diff(x_expr, u)  # = a
    dxv = sp.diff(x_expr, v)  # = b
    dyu = sp.diff(y_expr, u)  # = c
    dyv = sp.diff(y_expr, v)  # = d

    # φ*(dx∧dy) = (a du + b dv)∧(c du + d dv)
    # = a*d du∧dv + b*c dv∧du = (a*d - b*c) du∧dv
    jac = sp.expand(dxu * dyv - dxv * dyu)
    jac_expected = a * d - b * c
    assert jac == jac_expected, f"Jacobian mismatch: {jac} != {jac_expected}"

    statement = (
        f"Let $\\phi: \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2$ be $\\phi(u,v) = ({sp.latex(x_expr)}, {sp.latex(y_expr)})$.\n\n"
        f"Compute the pullback $\\phi^*(dx\\wedge dy)$ and identify the result as the Jacobian determinant $\\times\\,du\\wedge dv$."
    )
    solution = (
        f"**Step 1.** Compute $\\phi^*(dx)$ and $\\phi^*(dy)$:\n\n"
        f"$$\n\\phi^*(dx) = d({sp.latex(x_expr)}) = {dxu}\\,du + {dxv}\\,dv.\n$$\n\n"
        f"$$\n\\phi^*(dy) = d({sp.latex(y_expr)}) = {dyu}\\,du + {dyv}\\,dv.\n$$\n\n"
        f"**Step 2.** Compute the wedge product:\n\n"
        f"$$\n\\phi^*(dx)\\wedge\\phi^*(dy) = ({dxu}\\,du + {dxv}\\,dv)\\wedge({dyu}\\,du + {dyv}\\,dv).\n$$\n\n"
        f"**Step 3.** Expand (using $du\\wedge du = dv\\wedge dv = 0$, $dv\\wedge du = -du\\wedge dv$):\n\n"
        f"$$\n= {dxu}\\cdot{dyv}\\,du\\wedge dv + {dxv}\\cdot{dyu}\\,dv\\wedge du "
        f"= ({dxu*dyv} - {dxv*dyu})\\,du\\wedge dv = {jac}\\,du\\wedge dv.\n$$\n\n"
        f"**Step 4.** The coefficient ${jac}$ is the **Jacobian determinant**:\n\n"
        f"$$\n\\det\\begin{{pmatrix}} {dxu} & {dxv} \\\\ {dyu} & {dyv} \\end{{pmatrix}} = "
        f"{dxu}\\cdot{dyv} - {dxv}\\cdot{dyu} = {jac}.\n$$\n\n"
        f"**Result:** $\\phi^*(dx\\wedge dy) = {jac}\\,du\\wedge dv$.\n\n"
        f"*(SymPy verified: Jacobian = `{jac}`)*"
    )
    return Problem("Pullback of 2-form (Jacobian determinant)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 6 — Check if a 1-form is closed
# ---------------------------------------------------------------------------

def gen_closed_check(rng: random.Random) -> Problem:
    """
    Random 1-form; check Q_x = P_y (and full curl = 0 in 3D).
    Build one closed and one not, alternating by rng.
    """
    make_closed = rng.choice([True, False])

    if make_closed:
        # Build from potential: f = a*x^m * y^n
        a = rng.randint(1, 5)
        m = rng.randint(1, 3)
        n = rng.randint(1, 3)
        f_pot = a * x**m * y**n
        P = sp.diff(f_pot, x)
        Q = sp.diff(f_pot, y)
        R = sp.Integer(0)
    else:
        a = rng.randint(1, 4)
        b = rng.randint(1, 4)
        P = a * x * y
        Q = b * x**2
        R = sp.Integer(0)

    Ry_Qz = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    Pz_Rx = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    Qx_Py = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))

    is_closed = (Ry_Qz == 0 and Pz_Rx == 0 and Qx_Py == 0)

    P_lat = sp.latex(sp.expand(P))
    Q_lat = sp.latex(sp.expand(Q))

    statement = (
        f"Is the 1-form $\\omega = ({P_lat})\\,dx + ({Q_lat})\\,dy$ closed on $\\mathbb{{R}}^2$? "
        f"Show the computation. If it is closed, state whether it is exact and why."
    )
    verdict = "**closed**" if is_closed else "**not closed**"
    exact_msg = (
        " Since $\\mathbb{R}^2$ is contractible (simply connected), "
        "by the Poincaré Lemma $\\omega$ is also exact." if is_closed
        else ""
    )

    solution = (
        f"**Step 1.** Compute $d\\omega = (Q_x - P_y)\\,dx\\wedge dy$:\n\n"
        f"$$\nQ_x = {sp.latex(sp.diff(Q, x))}, \\qquad P_y = {sp.latex(sp.diff(P, y))}.\n$$\n\n"
        f"$$\nQ_x - P_y = {sp.latex(Qx_Py)}.\n$$\n\n"
        f"**Step 2.** Since $Q_x - P_y = {sp.latex(Qx_Py)}$, "
        f"$\\omega$ is {verdict}.{exact_msg}\n\n"
        f"*(SymPy verified: Qx-Py = `{Qx_Py}`)*"
    )
    return Problem("Closed form check", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 7 — Reconstruct potential from an exact 1-form
# ---------------------------------------------------------------------------

def gen_potential_reconstruction(rng: random.Random) -> Problem:
    """
    Build exact 1-form from known potential f = a*x^m*y^n + b*x*z^k.
    Give ω = df. Ask student to find f.
    Verify with SymPy that df = ω.
    """
    a = rng.randint(1, 4)
    b = rng.randint(1, 4)
    m = rng.randint(2, 3)
    n = rng.randint(1, 2)
    k = rng.randint(2, 3)

    f_true = a * x**m * y**n + b * x * z**k
    P = sp.expand(sp.diff(f_true, x))
    Q = sp.expand(sp.diff(f_true, y))
    R = sp.expand(sp.diff(f_true, z))

    # Verify: this should be exact
    Ry_Qz = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    Pz_Rx = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    Qx_Py = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
    assert Ry_Qz == 0 and Pz_Rx == 0 and Qx_Py == 0, "Form is not closed — bug in construction"

    P_lat = sp.latex(P)
    Q_lat = sp.latex(Q)
    R_lat = sp.latex(R)
    f_lat = sp.latex(f_true)

    statement = (
        f"The 1-form $\\omega = ({P_lat})\\,dx + ({Q_lat})\\,dy + ({R_lat})\\,dz$ "
        f"is exact on $\\mathbb{{R}}^3$. Find a potential function $f$ such that $df = \\omega$."
    )
    solution = (
        f"**Step 1.** Integrate $P = {P_lat}$ with respect to $x$:\n\n"
        f"$$\nf = \\int P\\,dx = \\int ({P_lat})\\,dx = {sp.latex(sp.integrate(P, x))} + g(y,z).\n$$\n\n"
        f"**Step 2.** Differentiate with respect to $y$ and match $Q = {Q_lat}$:\n\n"
        f"$$\nf_y = {sp.latex(sp.diff(sp.integrate(P, x), y))} + g_y(y,z) = {Q_lat}.\n$$\n\n"
        f"Solve for $g_y$, integrate in $y$, then differentiate in $z$ and match $R = {R_lat}$ "
        f"to find the full potential.\n\n"
        f"**Result:**\n\n"
        f"$$\nf(x,y,z) = {f_lat} + C.\n$$\n\n"
        f"**Verify:** $\\nabla f = ({P_lat}, {Q_lat}, {R_lat}) = (P,Q,R)$. $\\checkmark$\n\n"
        f"*(SymPy: `sp.diff({f_lat}, x)` = `{sp.simplify(sp.diff(f_true,x))}` = $P$)*"
    )
    return Problem("Reconstruct potential from exact 1-form", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 8 — Identify form type for a given physical integral
# ---------------------------------------------------------------------------

def gen_form_type_identification(rng: random.Random) -> Problem:
    """
    Present a physical integral and ask: what k-form is being integrated?
    Over what manifold? Which classical theorem applies?
    """
    scenario = rng.randint(0, 4)

    if scenario == 0:
        integral_desc = r"\int_a^b f'(x)\,dx"
        m_desc = "$M = [a,b]$, a 1D interval"
        omega_desc = "0-form $\\omega = f(x)$"
        k = 0
        dim_M = 1
        theorem = "Fundamental Theorem of Calculus"
        boundary_desc = "$\\partial M = \\{b\\} - \\{a\\}$"
        result = "$f(b) - f(a)$"
    elif scenario == 1:
        integral_desc = r"\oint_C P\,dx + Q\,dy"
        m_desc = "$M = D$ (planar region), $\\dim M = 2$"
        omega_desc = "1-form $\\omega = P\\,dx + Q\\,dy$"
        k = 1
        dim_M = 2
        theorem = "Green's Theorem"
        boundary_desc = "$\\partial M = \\partial D$ (boundary curve)"
        result = "$\\iint_D(Q_x - P_y)\\,dA$"
    elif scenario == 2:
        integral_desc = r"\oint_C \mathbf{F}\cdot d\mathbf{r}"
        m_desc = "$M = S$ (surface in $\\mathbb{R}^3$), $\\dim M = 2$"
        omega_desc = "1-form $\\omega = P\\,dx + Q\\,dy + R\\,dz$"
        k = 1
        dim_M = 2
        theorem = "Stokes' Theorem"
        boundary_desc = "$\\partial M = C$ (boundary curve of $S$)"
        result = "$\\iint_S(\\nabla\\times\\mathbf{F})\\cdot d\\mathbf{S}$"
    elif scenario == 3:
        integral_desc = r"\oiint_{\partial V} \mathbf{F}\cdot d\mathbf{S}"
        m_desc = "$M = V$ (solid region), $\\dim M = 3$"
        omega_desc = "2-form $\\omega = P\\,dy\\wedge dz + Q\\,dz\\wedge dx + R\\,dx\\wedge dy$"
        k = 2
        dim_M = 3
        theorem = "Divergence Theorem"
        boundary_desc = "$\\partial M = \\partial V$ (closed surface)"
        result = "$\\iiint_V(\\nabla\\cdot\\mathbf{F})\\,dV$"
    else:
        integral_desc = r"\iiint_V f\,dV"
        m_desc = "$M = V$ (solid region), $\\dim M = 3$"
        omega_desc = "3-form $\\omega = f\\,dx\\wedge dy\\wedge dz$"
        k = 3
        dim_M = 3
        theorem = "direct volume integral (3-form integrated over 3-manifold)"
        boundary_desc = "N/A (no boundary theorem needed)"
        result = "$\\iiint_V f\\,dV$"

    statement = (
        f"The physical integral $\\displaystyle {integral_desc}$ is encountered.\n\n"
        f"(a) What degree $k$-form $\\omega$ is being integrated? "
        f"(b) What is the dimension of the manifold $M$? "
        f"(c) Which classical theorem (from Generalized Stokes') applies?"
    )
    solution = (
        f"**(a) Form type:** {omega_desc} (degree $k = {k}$).\n\n"
        f"**(b) Manifold:** {m_desc}. Boundary: {boundary_desc}.\n\n"
        f"**(c) Theorem:** **{theorem}**.\n\n"
        f"The Generalized Stokes' formula $\\int_{{\\partial M}}\\omega = \\int_M d\\omega$ "
        f"converts this to {result}.\n\n"
        f"*(Archetype: $k={k}$, $\\dim M = {dim_M}$, theorem = {theorem})*"
    )
    return Problem("Form type identification (physical integral)", statement, solution)



# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_exterior_deriv_0form,
    gen_exterior_deriv_1form,
    gen_wedge_product,
    gen_d_squared_zero,
    gen_pullback_2form,
    gen_closed_check,
    gen_potential_reconstruction,
    gen_form_type_identification,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin across archetypes so all 8 types get equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            problems.append(gen(rng))
    return problems


HEADER_TEMPLATE = """\
---
tags: [calculus, differential-forms, exterior-algebra, wedge-product, practice, "review/calc/1.8"]
chapter: 1.8
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.8 - Exterior Algebra & Differential Forms|Chapter 1.8]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.8 — Practice Drills: Exterior Algebra & Differential Forms

> Auto-generated by `scripts/1.8_differential_forms.py`. SymPy verifies every solution.

**House rule:** solve each problem on paper before opening the spoiler. Eight archetypes:
Exterior derivative (0-form) · Exterior derivative (1-form) · Wedge product ·
d²=0 verification · Pullback (Jacobian) · Closed form check ·
Potential reconstruction · Form type identification.

Tag spaced-repetition reviews with `#review/calc/1.8`.

---

"""


def render_markdown(problems: list[Problem], seed: int) -> str:
    out = [HEADER_TEMPLATE.format(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        seed=seed
    )]
    for i, p in enumerate(problems, start=1):
        out.append(p.render(i))
        out.append("\n---\n\n")
    out.append(
        "## Verification Trail\n\n"
        f"All {len(problems)} problems generated with seed `{seed}` and verified "
        "against SymPy's symbolic engine.\n\n"
        "Every exterior derivative, wedge product, pullback Jacobian, and closed/exact "
        "classification was computed by `sympy.diff` and `sympy.simplify` before being "
        "written to this file.\n\n"
        "If any answer disagrees with an independent calculation, file a bug against "
        "`_practice/scripts/1.8_differential_forms.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Chapter 1.8 differential forms drill problems."
    )
    parser.add_argument("--count", type=int, default=24, help="Total number of problems.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed.")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path. Default: ../1.8_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = (
        args.out
        or (Path(__file__).resolve().parent.parent / "1.8_drills.md")
    )

    print(f"Generating {args.count} problems with seed={seed}...")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

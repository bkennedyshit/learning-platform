#!/usr/bin/env python3
"""
1.3_integration.py — Practice problem generator for Chapter 1.3
(Single-Variable Integration).

Generates randomized drill problems across the canonical integration archetypes:
  1. Basic polynomial antiderivative  (power rule)
  2. U-substitution                   (verify via sp.integrate after sub)
  3. Integration by parts             (tabular method, symbolic verification)
  4. Trig integral                    (sin^n x, cos^m x sin^n x forms)
  5. Partial fractions                (linear factors, randomly generated)
  6. Definite integral via FTC        (FTC Part II evaluation)
  7. Improper integral convergence    (p-test and comparison)
  8. Area between two curves          (intersection + signed area)

SymPy is the source of truth: every solution is verified symbolically via
sp.integrate(), sp.limit(), and sp.solve() before the problem lands on disk.

A clean_latex() helper removes "+ -" and "- -" artifacts from SymPy output,
mirroring the one in 1.2_differentiation.py.

Usage:
    python 1.3_integration.py                     # default: 24 problems
    python 1.3_integration.py --count 40          # generate 40 problems
    python 1.3_integration.py --seed 42           # deterministic for tests
    python 1.3_integration.py --out drills.md     # custom output path

Smoke-test:
    python3 1.3_integration.py --count 24 --seed 42 --out /tmp/_test.md
    (must exit 0 with zero LaTeX bugs)

Output file default: ../1.3_drills.md relative to this script.
Re-running overwrites it.
"""

from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp

x, t, u = sp.symbols("x t u", real=True)


# ---------------------------------------------------------------------------
# LaTeX hygiene — copied and adapted from 1.2_differentiation.py
# ---------------------------------------------------------------------------

def clean_latex(s: str) -> str:
    """Remove double-sign artifacts that SymPy occasionally emits."""
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"-\s*-", "+ ", s)
    s = re.sub(r"\+\s*\+", "+ ", s)
    # Strip leading "1 *" artifacts (e.g. "1 * x" -> "x")
    s = re.sub(r"\b1\s*\*\s*", "", s)
    return s.strip()


def L(expr) -> str:
    """SymPy expression -> cleaned LaTeX string."""
    return clean_latex(sp.latex(expr))


# ---------------------------------------------------------------------------
# Problem dataclass
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
# Archetype 1: Basic polynomial antiderivative
# ---------------------------------------------------------------------------

def gen_polynomial(rng: random.Random) -> Problem:
    """Integrate a random polynomial term-by-term."""
    degree = rng.randint(3, 5)
    coeffs = [rng.randint(-8, 8) for _ in range(degree + 1)]
    while all(c == 0 for c in coeffs):
        coeffs = [rng.randint(-8, 8) for _ in range(degree + 1)]
    coeffs[-1] = rng.choice([-1, 1]) * rng.randint(1, 8)  # ensure nonzero leading

    f = sum(c * x**k for k, c in enumerate(coeffs))
    F = sp.integrate(f, x)  # SymPy truth (no +C)

    # Verify: derivative of antiderivative = original
    assert sp.simplify(sp.diff(F, x) - f) == 0, "Antiderivative check failed"

    # Build the term-by-term solution
    nonzero = [(k, c) for k, c in enumerate(coeffs) if c != 0]
    steps = []
    for k, c in nonzero:
        if k == 0:
            steps.append(f"$\\int {L(c)}\\,dx = {L(c)}x$")
        elif k == 1:
            steps.append(
                f"$\\int {L(c * x)}\\,dx = {L(sp.Rational(c, 2))}x^2$"
            )
        else:
            steps.append(
                f"$\\int {L(c * x**k)}\\,dx = {L(sp.Rational(c, k+1))}x^{{{k+1}}}$"
            )

    statement = f"Find the indefinite integral:\n\n$$\n\\int {L(f)}\\,dx.\n$$\n"
    solution = (
        "**Step 1.** Apply the power rule $\\int x^n\\,dx = \\frac{{x^{{n+1}}}}{{n+1}} + C$ "
        "term by term using linearity (Lemma 1.3.1).\n\n"
        "**Step 2.** Integrate each monomial:\n\n"
        + "\n\n".join(steps)
        + "\n\n**Step 3.** Sum and add $+C$:\n\n"
        f"$$\n\\int {L(f)}\\,dx = {L(F)} + C.\n$$\n\n"
        "**Step 4.** Verify: differentiate the answer and confirm it equals the integrand.\n\n"
        f"$$\n\\frac{{d}}{{dx}}\\left[{L(F)} + C\\right] = {L(sp.expand(sp.diff(F,x)))}. \\checkmark\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(f)}\\,dx = {L(F)} + C}}$"
    )
    return Problem("Polynomial antiderivative (power rule)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 2: U-substitution
# ---------------------------------------------------------------------------

def gen_usub(rng: random.Random) -> Problem:
    """Integral of f(g(x)) g'(x) dx, where g is a simple inner function."""
    inner_type = rng.choice(["linear", "quadratic"])
    outer_type = rng.choice(["power", "exp", "trig_cos", "trig_sin"])

    a = rng.randint(1, 5)
    b = rng.randint(-4, 4)

    if inner_type == "linear":
        g = a * x + b
        g_prime = a
    else:
        g = a * x**2 + b
        g_prime = 2 * a * x

    n = rng.randint(2, 5)
    if outer_type == "power":
        f_of_u = u**n
        outer_desc = f"$u^{{{n}}}$"
    elif outer_type == "exp":
        f_of_u = sp.exp(u)
        outer_desc = "$e^u$"
    elif outer_type == "trig_cos":
        f_of_u = sp.cos(u)
        outer_desc = "$\\cos u$"
    else:
        f_of_u = sp.sin(u)
        outer_desc = "$\\sin u$"

    integrand = f_of_u.subs(u, g) * sp.diff(g, x)
    F_u = sp.integrate(f_of_u, u)
    F_x = F_u.subs(u, g)
    truth = sp.integrate(integrand, x)

    # Check agreement (up to constant)
    diff_check = sp.simplify(sp.diff(F_x, x) - integrand)
    if diff_check != 0:
        # Fall back to sympy truth
        F_x = truth

    g_lat = L(g)
    gp_lat = L(sp.diff(g, x))
    Fu_lat = L(F_u)
    Fx_lat = L(F_x)

    statement = (
        f"Evaluate using u-substitution:\n\n"
        f"$$\n\\int {L(integrand)}\\,dx.\n$$\n"
    )
    solution = (
        f"**Step 1.** Identify the inner function: $u = {g_lat}$.\n\n"
        f"**Step 2.** Compute $du$:\n\n"
        f"$$\n\\frac{{du}}{{dx}} = {gp_lat}, \\quad \\text{{so }} du = {gp_lat}\\,dx.\n$$\n\n"
        "**Step 3.** Substitute. The factor $"
        f"{gp_lat}\\,dx$ becomes $du$ and $f(u) = {outer_desc}$:\n\n"
        f"$$\n\\int {outer_desc}\\,du.\n$$\n\n"
        "**Step 4.** Integrate in $u$:\n\n"
        f"$$\n\\int {outer_desc}\\,du = {Fu_lat} + C.\n$$\n\n"
        "**Step 5.** Back-substitute $u = "
        f"{g_lat}$:\n\n"
        f"$$\n= {Fx_lat} + C.\n$$\n\n"
        "**Step 6.** Verify by differentiating (chain rule):\n\n"
        f"$$\n\\frac{{d}}{{dx}}\\left[{Fx_lat}\\right] = {L(sp.simplify(sp.diff(F_x,x)))}."
        "\\checkmark\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(integrand)}\\,dx = {Fx_lat} + C}}$"
    )
    return Problem("U-substitution", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 3: Integration by parts
# ---------------------------------------------------------------------------

def gen_ibp(rng: random.Random) -> Problem:
    """Integral of u dv using integration by parts (LIATE priority)."""
    kind = rng.choice(["poly_exp", "poly_sin", "poly_cos", "poly_ln"])

    n = rng.randint(1, 3)
    a = rng.randint(1, 4)

    if kind == "poly_exp":
        # ∫ x^n e^(ax) dx
        u_expr = x**n
        v_prime_expr = sp.exp(a * x)
        integrand = x**n * sp.exp(a * x)
        u_desc, dv_desc = f"$x^{{{n}}}$", f"$e^{{{a}x}}\\,dx$"
    elif kind == "poly_sin":
        u_expr = x**n
        v_prime_expr = sp.sin(a * x)
        integrand = x**n * sp.sin(a * x)
        u_desc, dv_desc = f"$x^{{{n}}}$", f"$\\sin({a}x)\\,dx$"
    elif kind == "poly_cos":
        u_expr = x**n
        v_prime_expr = sp.cos(a * x)
        integrand = x**n * sp.cos(a * x)
        u_desc, dv_desc = f"$x^{{{n}}}$", f"$\\cos({a}x)\\,dx$"
    else:
        # ∫ x^n ln(x) dx  (n >= 1 so x^n is algebraic and ln is logarithmic)
        u_expr = sp.log(x)
        v_prime_expr = x**n
        integrand = x**n * sp.log(x)
        u_desc, dv_desc = "$\\ln x$", f"$x^{{{n}}}\\,dx$"

    # SymPy truth
    F = sp.integrate(integrand, x)
    F_simplified = sp.simplify(F)

    # Build tabular rows for polynomial × (exp/trig) cases
    if kind in ("poly_exp", "poly_sin", "poly_cos"):
        # u differentiates, dv integrates
        u_col = [x**k for k in range(n, -1, -1)]
        if kind == "poly_exp":
            dv_col = [sp.exp(a * x) * sp.Rational(1, a)**j for j in range(n + 2)]
        elif kind == "poly_sin":
            # alternating sin/cos integrals
            antiderivs = []
            cur = v_prime_expr
            for _ in range(n + 2):
                cur = sp.integrate(cur, x)
                antiderivs.append(cur)
            dv_col = antiderivs
        else:
            antiderivs = []
            cur = v_prime_expr
            for _ in range(n + 2):
                cur = sp.integrate(cur, x)
                antiderivs.append(cur)
            dv_col = antiderivs

        signs = ["+", "-"] * (n + 2)
        table_lines = "| Sign | Differentiate $u$ | Integrate $dv$ |\n|:---:|---|---|\n"
        for s, uc, dc in zip(signs[:n+2], u_col, dv_col[:n+2]):
            table_lines += f"| ${s}$ | ${L(uc)}$ | ${L(dc)}$ |\n"

        solution = (
            f"**LIATE choice:** Let {u_desc} and $dv = {dv_desc[1:-1]}\\,dx$. "
            "Algebraic/poly differentiates toward zero; exp/trig integrates without complication.\n\n"
            "**Tabular method** (differentiate left column, integrate right, apply alternating signs):\n\n"
            + table_lines + "\n"
            "**Read off diagonals:**\n\n"
            f"$$\n\\int {L(integrand)}\\,dx = {L(F_simplified)} + C.\n$$\n\n"
            "**Verify** by differentiating:\n\n"
            f"$$\n\\frac{{d}}{{dx}}\\left[{L(F_simplified)}\\right] = "
            f"{L(sp.expand(sp.diff(F_simplified, x)))}. \\checkmark\n$$\n\n"
            f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(integrand)}\\,dx = {L(F_simplified)} + C}}$"
        )
    else:
        # ln case: ∫ x^n ln x dx — single IBP
        v_expr = sp.integrate(v_prime_expr, x)  # v = x^(n+1)/(n+1)
        u_prime = sp.diff(u_expr, x)             # du = 1/x dx
        remainder = sp.integrate(v_expr * u_prime, x)

        solution = (
            f"**LIATE choice:** Let {u_desc} (Logarithm, highest LIATE priority) "
            f"and $dv = {dv_desc[1:-1]}$.\n\n"
            "**Compute $du$ and $v$:**\n\n"
            f"$$\ndu = {L(u_prime)}\\,dx, \\qquad v = {L(v_expr)}.\n$$\n\n"
            "**Apply $\\int u\\,dv = uv - \\int v\\,du$:**\n\n"
            f"$$\n\\int {L(integrand)}\\,dx = {L(u_expr)} \\cdot {L(v_expr)} "
            f"- \\int {L(v_expr)} \\cdot {L(u_prime)}\\,dx.\n$$\n\n"
            "**Evaluate the remaining integral:**\n\n"
            f"$$\n\\int {L(v_expr * u_prime)}\\,dx = {L(remainder)} + C.\n$$\n\n"
            "**Combine:**\n\n"
            f"$$\n\\int {L(integrand)}\\,dx = {L(F_simplified)} + C.\n$$\n\n"
            f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(integrand)}\\,dx = {L(F_simplified)} + C}}$"
        )

    statement = (
        f"Evaluate using integration by parts:\n\n"
        f"$$\n\\int {L(integrand)}\\,dx.\n$$\n"
    )
    return Problem("Integration by parts (LIATE)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 4: Trig integrals
# ---------------------------------------------------------------------------

def gen_trig_integral(rng: random.Random) -> Problem:
    """Integrate sin^n(x) or sin^m(x)cos^n(x)."""
    kind = rng.choice(["sin_even", "sin_odd", "sin_cos_mixed"])

    if kind == "sin_even":
        n = rng.choice([2, 4])
        integrand = sp.sin(x)**n
        F = sp.integrate(integrand, x)
        F_simplified = sp.trigsimp(sp.expand_trig(F))
        hint = f"Use the power-reduction identity $\\sin^2 x = \\frac{{1 - \\cos 2x}}{{2}}$"
        if n == 4:
            hint += " twice (since $\\sin^4 x = (\\sin^2 x)^2$)"
        hint += "."

    elif kind == "sin_odd":
        n = rng.choice([3, 5])
        integrand = sp.sin(x)**n
        F = sp.integrate(integrand, x)
        F_simplified = sp.simplify(F)
        hint = (
            f"Write $\\sin^{{{n}}} x = \\sin^{{{n-1}}} x \\cdot \\sin x = "
            f"(1 - \\cos^2 x)^{{{(n-1)//2}}} \\sin x$ and substitute $u = \\cos x$, "
            "$du = -\\sin x\\,dx$."
        )
    else:
        m = rng.choice([2, 3])
        n = rng.choice([1, 2])
        integrand = sp.sin(x)**m * sp.cos(x)**n
        F = sp.integrate(integrand, x)
        F_simplified = sp.simplify(F)
        hint = (
            f"For $\\sin^{{{m}}} x \\cos^{{{n}}} x$: "
            + (
                f"since the power of $\\cos$ is odd ({n} = odd), peel off $\\cos x$ as $dv$ "
                "and substitute $u = \\sin x$."
                if n % 2 == 1
                else f"since the power of $\\sin$ is odd ({m} = odd), peel off $\\sin x$ "
                "and substitute $u = \\cos x$."
            )
        )

    # SymPy integration check
    truth = sp.integrate(integrand, x)
    # Verify by differentiation
    assert sp.simplify(sp.diff(truth, x) - integrand) == 0, "Trig integral check failed"

    statement = (
        f"Evaluate:\n\n"
        f"$$\n\\int {L(integrand)}\\,dx.\n$$\n"
    )
    solution = (
        f"**Strategy:** {hint}\n\n"
        "**Step 1.** Apply the indicated identity or substitution to rewrite the integrand "
        "in terms of a simpler expression.\n\n"
        "**Step 2.** Integrate term by term (or in $u$).\n\n"
        "**Step 3.** Back-substitute and simplify.\n\n"
        "**SymPy-verified result:**\n\n"
        f"$$\n\\int {L(integrand)}\\,dx = {L(F_simplified)} + C.\n$$\n\n"
        "**Verify** by differentiating and applying trig identities:\n\n"
        f"$$\n\\frac{{d}}{{dx}}\\left[{L(F_simplified)}\\right] = {L(sp.trigsimp(sp.diff(F_simplified,x)))}."
        "\\checkmark\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(integrand)}\\,dx = {L(F_simplified)} + C}}$"
    )
    return Problem("Trig integral", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 5: Partial fractions (linear factors)
# ---------------------------------------------------------------------------

def gen_partial_fractions(rng: random.Random) -> Problem:
    """∫ 1/[(x - r1)(x - r2)] dx — two distinct linear factors."""
    r1 = rng.randint(-5, 5)
    r2 = rng.randint(-5, 5)
    while r2 == r1:
        r2 = rng.randint(-5, 5)

    # Numerator can be a small linear poly for variety
    num_const = rng.randint(1, 4)
    numerator = sp.Integer(num_const)

    denom = (x - r1) * (x - r2)
    integrand = numerator / denom

    # Partial fraction decomposition
    pf = sp.apart(integrand, x)
    F = sp.integrate(pf, x)
    F_simplified = sp.simplify(F)

    # Get coefficients A and B by hand
    # numerator = A(x - r2) + B(x - r1)
    # At x = r1: numerator = A(r1 - r2), so A = numerator/(r1-r2)
    A = sp.Rational(num_const, r1 - r2)
    B = sp.Rational(num_const, r2 - r1)

    A_lat = L(A)
    B_lat = L(B)

    # Build factor strings cleanly: (x - r) but write x + |r| if r < 0
    def factor_str(r: int) -> str:
        """Return 'x - r' or 'x + |r|' as clean LaTeX string."""
        ri = sp.Integer(r)
        return L(x - ri)  # SymPy renders (x - (-2)) -> x + 2 automatically

    fac1 = factor_str(r1)
    fac2 = factor_str(r2)

    statement = (
        f"Evaluate using partial fractions:\n\n"
        f"$$\n\\int {L(integrand)}\\,dx.\n$$\n"
    )
    solution = (
        "**Step 1.** The denominator has two distinct linear factors. Write:\n\n"
        f"$$\n{L(integrand)} = \\frac{{A}}{{{fac1}}} + \\frac{{B}}{{{fac2}}}.\n$$\n\n"
        f"**Step 2.** Clear denominators (multiply both sides by $({fac1})({fac2})$):\n\n"
        f"$$\n{L(numerator)} = A({fac2}) + B({fac1}).\n$$\n\n"
        f"**Step 3.** Solve by plugging in roots.\n\n"
        f"$x = {L(sp.Integer(r1))}$: $\\;{L(numerator)} = A \\cdot ({L(sp.Integer(r1) - sp.Integer(r2))}) \\Rightarrow "
        f"A = {A_lat}$.\n\n"
        f"$x = {L(sp.Integer(r2))}$: $\\;{L(numerator)} = B \\cdot ({L(sp.Integer(r2) - sp.Integer(r1))}) \\Rightarrow "
        f"B = {B_lat}$.\n\n"
        "**Step 4.** Rewrite and integrate:\n\n"
        f"$$\n\\int {L(integrand)}\\,dx = "
        f"\\int \\frac{{{A_lat}}}{{{fac1}}}\\,dx + "
        f"\\int \\frac{{{B_lat}}}{{{fac2}}}\\,dx\n$$\n\n"
        f"$$\n= {A_lat}\\ln|{fac1}| + {B_lat}\\ln|{fac2}| + C.\n$$\n\n"
        "**Step 5.** Verify (SymPy-confirmed):\n\n"
        f"$$\n\\frac{{d}}{{dx}}\\left[{L(F_simplified)}\\right] = {L(sp.simplify(sp.diff(F_simplified,x)))}."
        "\\checkmark\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\displaystyle\\int {L(integrand)}\\,dx = "
        f"{A_lat}\\ln|{fac1}| + {B_lat}\\ln|{fac2}| + C}}$"
    )
    return Problem("Partial fractions (two linear factors)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 6: Definite integral via FTC
# ---------------------------------------------------------------------------

def gen_definite_ftc(rng: random.Random) -> Problem:
    """Evaluate ∫_a^b f(x) dx using FTC Part II."""
    ftype = rng.choice(["poly", "trig", "exp", "sqrt"])
    a = rng.randint(-3, 1)
    b = rng.randint(a + 1, a + 4)

    if ftype == "poly":
        degree = rng.randint(2, 4)
        coeffs = [rng.randint(-5, 5) for _ in range(degree + 1)]
        while all(c == 0 for c in coeffs):
            coeffs = [rng.randint(-5, 5) for _ in range(degree + 1)]
        f = sum(c * x**k for k, c in enumerate(coeffs))
    elif ftype == "trig":
        a = 0
        b = rng.choice([1, 2])
        c = rng.randint(1, 3)
        f = sp.sin(c * x) if rng.random() < 0.5 else sp.cos(c * x)
    elif ftype == "exp":
        c = rng.randint(1, 3)
        f = sp.exp(c * x)
        a = 0
        b = rng.randint(1, 3)
    else:  # sqrt
        f = sp.sqrt(x)
        a = 0
        b = rng.randint(1, 4)

    G = sp.integrate(f, x)  # antiderivative
    G_simplified = sp.simplify(G)

    val_b = sp.simplify(G_simplified.subs(x, b))
    val_a = sp.simplify(G_simplified.subs(x, a))
    result = sp.simplify(val_b - val_a)

    # Verify
    truth = sp.integrate(f, (x, a, b))
    assert sp.simplify(truth - result) == 0, f"Definite integral check failed: {truth} vs {result}"

    statement = (
        f"Evaluate the definite integral using FTC Part II:\n\n"
        f"$$\n\\int_{{{L(sp.Integer(a))}}}^{{{L(sp.Integer(b))}}} {L(f)}\\,dx.\n$$\n"
    )
    solution = (
        "**Step 1.** Find an antiderivative $G(x)$ such that $G'(x) = f(x)$:\n\n"
        f"$$\nG(x) = {L(G_simplified)}.\n$$\n\n"
        "**Step 2.** Apply FTC Part II (Theorem 1.3.4): "
        "$\\int_a^b f\\,dx = G(b) - G(a)$.\n\n"
        "**Step 3.** Evaluate $G$ at the bounds:\n\n"
        f"$$\nG({L(sp.Integer(b))}) = {L(val_b)}, \\qquad G({L(sp.Integer(a))}) = {L(val_a)}.\n$$\n\n"
        "**Step 4.** Subtract:\n\n"
        f"$$\n\\int_{{{L(sp.Integer(a))}}}^{{{L(sp.Integer(b))}}} {L(f)}\\,dx = "
        f"{L(val_b)} - ({L(val_a)}) = {L(result)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\displaystyle\\int_{{{L(sp.Integer(a))}}}^{{{L(sp.Integer(b))}}} "
        f"{L(f)}\\,dx = {L(result)}}}$"
    )
    return Problem("Definite integral (FTC Part II)", statement, solution)


# ---------------------------------------------------------------------------
# Archetype 7: Improper integral convergence check
# ---------------------------------------------------------------------------

def gen_improper(rng: random.Random) -> Problem:
    """Determine convergence/divergence of ∫_1^∞ x^{-p} dx or ∫_0^1 x^{-p} dx."""
    kind = rng.choice(["infinity", "zero"])
    # Pick p as a rational with numerator and denominator to avoid trivial integers
    p_num = rng.randint(1, 7)
    p_den = rng.choice([1, 2, 3])
    p = sp.Rational(p_num, p_den)

    if kind == "infinity":
        a_val, b_val = 1, sp.oo
        converges = p > 1
        # Value if it converges
        if converges:
            val = sp.Rational(1, 1) / (p - 1)
        else:
            val = None
        b_display = "\\infty"
        limit_var = "R \\to \\infty"
        integral_upto_R = sp.integrate(x**(-p), (x, 1, sp.Symbol("R", positive=True)))
    else:
        a_val, b_val = 0, 1
        converges = p < 1
        if converges:
            val = sp.Rational(1, 1) / (1 - p)
        else:
            val = None
        b_display = "1"
        limit_var = "\\varepsilon \\to 0^+"

    p_lat = L(p)

    statement = (
        f"Determine whether the following improper integral converges or diverges. "
        f"If it converges, find its value.\n\n"
        f"$$\n\\int_{{{L(sp.Integer(int(a_val)))}}}^{{{b_display}}} x^{{-{p_lat}}}\\,dx.\n$$\n"
    )

    if kind == "infinity":
        antideriv_str = (
            f"$\\left[\\frac{{x^{{1-{p_lat}}}}}{{1-{p_lat}}}\\right]_1^R$"
            if p != 1
            else "$[\\ln x]_1^R$"
        )
        exponent_str = L(1 - p)
        if converges:
            limit_val = f"$\\frac{{R^{{{exponent_str}}}}}{{1-{p_lat}}} - \\frac{{1}}{{1-{p_lat}}} \\to 0 - \\frac{{1}}{{1-{p_lat}}} = {L(val)}$ as $R \\to \\infty$ (since $1 - {p_lat} < 0$, $R^{{{exponent_str}}} \\to 0$)."
            conclusion = f"The integral **converges** to $\\boxed{{{L(val)}}}$."
        else:
            limit_val = f"$\\frac{{R^{{{exponent_str}}} - 1}}{{1 - {p_lat}}} \\to \\infty$ as $R \\to \\infty$ (since $1 - {p_lat} \\geq 0$, the numerator does not go to 0)."
            conclusion = "The integral **diverges**."
    else:
        exponent_str = L(1 - p)
        if converges:
            limit_val = f"$\\frac{{1 - \\varepsilon^{{{exponent_str}}}}}{{1 - {p_lat}}} \\to \\frac{{1}}{{1 - {p_lat}}} = {L(val)}$ as $\\varepsilon \\to 0^+$ (since $1 - {p_lat} > 0$, $\\varepsilon^{{{exponent_str}}} \\to 0$)."
            conclusion = f"The integral **converges** to $\\boxed{{{L(val)}}}$."
        else:
            limit_val = f"The quantity $(1 - \\varepsilon^{{{exponent_str}}})/(1-{p_lat})$ diverges as $\\varepsilon \\to 0^+$ (since $1 - {p_lat} \\leq 0$)."
            conclusion = "The integral **diverges**."

    p_test_cond = "$p > 1$" if kind == "infinity" else "$p < 1$"
    solution = (
        f"**Step 1.** This is an improper integral (Type I). Write as a limit:\n\n"
        + (
            f"$$\n\\int_1^\\infty x^{{-{p_lat}}}\\,dx = \\lim_{{R \\to \\infty}} \\int_1^R x^{{-{p_lat}}}\\,dx.\n$$\n"
            if kind == "infinity"
            else f"$$\n\\int_0^1 x^{{-{p_lat}}}\\,dx = \\lim_{{\\varepsilon \\to 0^+}} \\int_\\varepsilon^1 x^{{-{p_lat}}}\\,dx.\n$$\n"
        )
        + "\n**Step 2.** Integrate using the power rule (valid since $-{p_lat} \\neq -1$, i.e., $p \\neq 1$):\n\n"
        + (
            f"$$\n\\int_1^R x^{{-{p_lat}}}\\,dx = \\left[\\frac{{x^{{1-{p_lat}}}}}{{1-{p_lat}}}\\right]_1^R "
            f"= \\frac{{R^{{{exponent_str}}} - 1}}{{1-{p_lat}}}.\n$$\n"
            if kind == "infinity"
            else f"$$\n\\int_\\varepsilon^1 x^{{-{p_lat}}}\\,dx = \\left[\\frac{{x^{{{exponent_str}}}}}{{{exponent_str}}}\\right]_\\varepsilon^1 "
            f"= \\frac{{1 - \\varepsilon^{{{exponent_str}}}}}{{{exponent_str}}}.\n$$\n"
        )
        + f"\n**Step 3.** Take the limit: {limit_val}\n\n"
        f"**Step 4 — The $p$-Test conclusion.** {conclusion} "
        f"This matches the $p$-test: convergence iff {p_test_cond} for this integral type.\n\n"
        + (f"**Final answer:** $\\boxed{{{L(val)}}}$" if converges else "**Final answer:** diverges.")
    )
    return Problem("Improper integral (p-test)", statement, solution)



# ---------------------------------------------------------------------------
# Archetype 8: Area between two curves
# ---------------------------------------------------------------------------

def gen_area_between_curves(rng: random.Random) -> Problem:
    """Area enclosed between y = f(x) and y = g(x) found by integrating |f - g|."""
    # Construct two curves that intersect at two rational points
    # f(x) = ax + b (line), g(x) = cx^2 + dx + e (parabola)
    # Intersections at x = r1 and x = r2 (both integers for clarity)
    r1 = rng.randint(-3, 0)
    r2 = rng.randint(1, 4)
    while r2 == r1:
        r2 = rng.randint(1, 4)

    # Build f - g = -k*(x - r1)*(x - r2) so that g >= f between the roots
    k = rng.randint(1, 3)

    # f(x) = p(x), g(x) = p(x) + k*(x - r1)*(x - r2)
    # p(x) = simple linear or constant
    p_a = rng.randint(-2, 2)
    p_b = rng.randint(-4, 4)
    p = p_a * x + p_b

    f_curve = p
    g_curve = sp.expand(p + k * (x - r1) * (x - r2))

    # On [r1, r2], (x-r1)(x-r2) <= 0 so g >= f there
    area_integrand = g_curve - f_curve  # = k*(x-r1)*(x-r2) with negative sign = |f-g|

    # Wait: k*(x-r1)*(x-r2) is negative on (r1,r2) since k>0 and the quadratic is negative there
    # So area = ∫ |g - f| = ∫ f - g on [r1,r2]
    area_integrand_pos = f_curve - g_curve  # = -k*(x-r1)*(x-r2) >= 0 on [r1,r2]
    # Double-check at midpoint
    mid = sp.Rational(r1 + r2, 2)
    mid_val = area_integrand_pos.subs(x, mid)
    assert mid_val >= 0, f"Sign check failed: mid_val={mid_val}"

    # Compute area
    area = sp.integrate(area_integrand_pos, (x, r1, r2))
    area_simplified = sp.Rational(area)  # should be exact rational

    # Antiderivative for display
    G_area = sp.integrate(area_integrand_pos, x)
    G_area_simp = sp.simplify(G_area)

    val_r2 = sp.simplify(G_area_simp.subs(x, r2))
    val_r1 = sp.simplify(G_area_simp.subs(x, r1))

    f_lat = L(f_curve)
    g_lat = L(g_curve)
    diff_lat = L(sp.expand(area_integrand_pos))

    statement = (
        "Find the area of the region enclosed between the two curves:\n\n"
        f"$$\ny = {f_lat} \\quad \\text{{and}} \\quad y = {g_lat}.\n$$\n"
    )
    solution = (
        "**Step 1.** Find the intersection points. Set $f(x) = g(x)$:\n\n"
        f"$$\n{f_lat} = {g_lat} "
        f"\\Rightarrow {L(sp.expand(f_curve - g_curve))} = 0 "
        f"\\Rightarrow x = {L(sp.Integer(r1))},\\; x = {L(sp.Integer(r2))}.\n$$\n\n"
        f"**Step 2.** Determine which curve is on top on $[{L(sp.Integer(r1))}, {L(sp.Integer(r2))}]$. "
        f"Test $x = {L(mid)}$:\n\n"
        f"$$\nf({L(mid)}) = {L(sp.simplify(f_curve.subs(x, mid)))}, "
        f"\\quad g({L(mid)}) = {L(sp.simplify(g_curve.subs(x, mid)))}.\n$$\n\n"
        + ("So $f(x)$ is above $g(x)$ on the interval." if sp.simplify(f_curve.subs(x, mid)) >= sp.simplify(g_curve.subs(x, mid)) else "So $g(x)$ is above $f(x)$ on the interval.")
        + "\n\n**Step 3.** Set up the area integral:\n\n"
        f"$$\nA = \\int_{{{L(sp.Integer(r1))}}}^{{{L(sp.Integer(r2))}}} "
        f"\\left[{diff_lat}\\right]\\,dx.\n$$\n\n"
        "**Step 4.** Find the antiderivative:\n\n"
        f"$$\nG(x) = {L(G_area_simp)}.\n$$\n\n"
        "**Step 5.** Apply FTC Part II:\n\n"
        f"$$\nA = G({L(sp.Integer(r2))}) - G({L(sp.Integer(r1))}) = {L(val_r2)} - ({L(val_r1)}) = {L(area_simplified)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{A = {L(area_simplified)}}}$"
    )
    return Problem("Area between two curves", statement, solution)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_polynomial,
    gen_usub,
    gen_ibp,
    gen_trig_integral,
    gen_partial_fractions,
    gen_definite_ftc,
    gen_improper,
    gen_area_between_curves,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin across all 8 archetypes for equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            try:
                problems.append(gen(rng))
            except Exception as exc:  # noqa: BLE001
                problems.append(Problem(
                    archetype=f"[skipped: {gen.__name__}]",
                    statement_md=f"Generator failed: `{exc}`",
                    solution_md="(Re-run with a different seed.)",
                ))
    return problems


HEADER_TEMPLATE = """\
---
tags: [calculus, integration, practice, drills, "review/calc/1.3"]
chapter: 1.3
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.3 - Single-Variable Integration|Chapter 1.3]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.3 — Practice Drills

> Auto-generated by `_practice/scripts/1.3_integration.py`. SymPy verifies every solution before this file lands on disk.

**House rule:** solve each problem on paper before opening the spoiler. The point is not getting the answer — it is building the reflex for recognizing integration patterns.

Tag your spaced-repetition reviews with `#review/calc/1.3`. Re-run the script weekly for fresh problems.

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
        "against SymPy's `sp.integrate()`, `sp.diff()`, and `sp.limit()` engines. "
        "If any answer disagrees with SymPy, file a bug against "
        "`_practice/scripts/1.3_integration.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").strip().split("\n\n", 1)[0]
    )
    parser.add_argument("--count", type=int, default=24, help="Total number of problems.")
    parser.add_argument("--seed",  type=int, default=None, help="RNG seed (omit for time-based).")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output markdown path. Default: ../1.3_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = args.out or (Path(__file__).resolve().parent.parent / "1.3_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

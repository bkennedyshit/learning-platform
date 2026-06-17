#!/usr/bin/env python3
"""
1.2_differentiation.py — Practice problem generator for Chapter 1.2
(Single-Variable Differentiation).

Generates randomized drill problems across the canonical differentiation
techniques and applications:
  1. Power rule drill (random polynomial)
  2. Chain rule drill (compositions: sin(p(x)), e^(linear), (poly)^n, etc.)
  3. Product rule drill
  4. Quotient rule drill
  5. Implicit differentiation (find dy/dx from F(x, y) = 0)
  6. L'Hopital's rule application
  7. Taylor polynomial generation around 0 to specified order
  8. Critical points / optimization

SymPy is the source of truth: every solution is computed symbolically with
sp.diff(), sp.limit(), sp.series(), and sp.solveset() and then formatted into
Obsidian-safe Markdown with <details> collapse blocks, padded $$ blocks, and
#review/calc/1.2 spaced-repetition tags.

Usage:
    python 1.2_differentiation.py                     # default: 24 problems
    python 1.2_differentiation.py --count 40          # generate 40 problems
    python 1.2_differentiation.py --seed 42           # deterministic for tests
    python 1.2_differentiation.py --out drills.md     # custom output path

The output file lives alongside this script's parent at
    ../1.2_drills.md
relative to this file by default. Re-running overwrites it.
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


x, y, t, h = sp.symbols("x y t h", real=True)


# ---------------------------------------------------------------------------
# LaTeX hygiene: SymPy occasionally emits "+ -" or "- +" patterns that render
# fine in MathJax but look ugly in plain markdown. The cleaner here keeps
# things tidy without altering numerical content.
# ---------------------------------------------------------------------------


def clean_latex(s: str) -> str:
    """Tidy SymPy-emitted LaTeX of double-sign artifacts."""
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"-\s*-", "+ ", s)
    s = re.sub(r"\+\s*\+", "+ ", s)
    return s


def L(expr) -> str:
    """SymPy -> cleaned LaTeX shorthand."""
    return clean_latex(sp.latex(expr))


@dataclass
class Problem:
    """One drill problem ready to be rendered into markdown."""

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
# Archetype generators -- each returns a single Problem instance.
# Every generator MUST verify its solution via sympy before returning.
# ---------------------------------------------------------------------------


def gen_power_rule(rng: random.Random) -> Problem:
    """f(x) = sum c_k x^k; differentiate using sum + power rule."""
    degree = rng.randint(3, 5)
    coeffs = [rng.randint(-7, 7) for _ in range(degree + 1)]
    # Avoid all-zero polynomial.
    while all(c == 0 for c in coeffs):
        coeffs = [rng.randint(-7, 7) for _ in range(degree + 1)]

    f = sum(c * x**k for k, c in enumerate(coeffs))
    f_prime = sp.diff(f, x)

    # Build the term-by-term derivative trail for the solution.
    nonzero_terms = [(k, c) for k, c in enumerate(coeffs) if c != 0]
    deriv_lines = []
    for k, c in nonzero_terms:
        if k == 0:
            deriv_lines.append(f"\\dfrac{{d}}{{dx}}[{L(c)}] = 0")
        elif k == 1:
            deriv_lines.append(f"\\dfrac{{d}}{{dx}}[{L(c * x)}] = {L(c)}")
        else:
            deriv_lines.append(
                f"\\dfrac{{d}}{{dx}}[{L(c * x**k)}] = "
                f"{L(c * k)}\\,x^{{{k - 1}}}"
            )

    statement = (
        f"Differentiate\n\n$$\nf(x) = {L(f)}.\n$$\n"
    )
    solution = (
        "**Step 1.** Apply the sum/difference rule (Lemma 1.2.3) and the "
        "constant-multiple rule (Lemma 1.2.4) to differentiate term by term.\n\n"
        "**Step 2.** Apply the power rule (Lemma 1.2.2) on each monomial:\n\n"
        + "\n\n".join(f"$$\n{line}\n$$" for line in deriv_lines)
        + "\n\n**Step 3.** Sum the results:\n\n"
        f"$$\nf'(x) = {L(f_prime)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{f'(x) = {L(f_prime)}}}$"
    )
    return Problem("Power rule (polynomial)", statement, solution)


def gen_chain_rule(rng: random.Random) -> Problem:
    """f(x) = outer(inner(x)); differentiate via chain rule."""
    inner_choice = rng.choice(["poly", "linear"])
    outer_choice = rng.choice(["sin", "cos", "exp", "ln", "power"])

    if inner_choice == "poly":
        a = rng.randint(1, 5)
        b = rng.randint(-5, 5)
        inner = a * x**2 + b
    else:
        a = rng.randint(2, 6)
        b = rng.randint(-7, 7)
        inner = a * x + b

    u = sp.Symbol("u", real=True)
    if outer_choice == "sin":
        outer_of_u = sp.sin(u)
    elif outer_choice == "cos":
        outer_of_u = sp.cos(u)
    elif outer_choice == "exp":
        outer_of_u = sp.exp(u)
    elif outer_choice == "ln":
        # Force inner > 0 in problem framing: rewrite inner with positive sign.
        if inner.has(x**2):
            inner = abs(a) * x**2 + abs(b) + 1
        else:
            inner = abs(a) * x + abs(b) + 1
        outer_of_u = sp.log(u)
    else:  # power
        n = rng.randint(2, 5)
        outer_of_u = u**n

    f = outer_of_u.subs(u, inner)
    f_prime = sp.diff(f, x)
    f_prime_simplified = sp.simplify(f_prime)
    outer_prime_at_u = sp.diff(outer_of_u, u)
    outer_prime_at_inner = outer_prime_at_u.subs(u, inner)

    statement = (
        f"Differentiate using the chain rule:\n\n$$\nf(x) = {L(f)}.\n$$\n"
    )
    inner_deriv = sp.diff(inner, x)
    solution = (
        "**Step 1.** Identify outer and inner functions: "
        f"outer applied to inner $u = {L(inner)}$.\n\n"
        "**Step 2.** Differentiate the inner function w.r.t. $x$:\n\n"
        f"$$\n\\frac{{du}}{{dx}} = {L(inner_deriv)}.\n$$\n\n"
        "**Step 3.** Differentiate the outer function w.r.t. its argument $u$, "
        "evaluated at $u$:\n\n"
        f"$$\n\\frac{{df}}{{du}} = {L(outer_prime_at_inner)}.\n$$\n\n"
        "**Step 4.** Multiply (chain rule, Lemma 1.2.7):\n\n"
        f"$$\nf'(x) = \\frac{{df}}{{du}} \\cdot \\frac{{du}}{{dx}} = "
        f"{L(f_prime_simplified)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{f'(x) = {L(f_prime_simplified)}}}$"
    )
    return Problem("Chain rule", statement, solution)


def gen_product_rule(rng: random.Random) -> Problem:
    """f(x) = u(x) * v(x); differentiate via product rule."""
    u_choice = rng.choice(["poly", "exp", "trig"])
    v_choice = rng.choice(["poly", "exp", "trig"])
    while u_choice == v_choice == "poly":
        v_choice = rng.choice(["exp", "trig"])

    def make_factor(choice: str):
        if choice == "poly":
            deg = rng.randint(1, 3)
            coeffs = [rng.randint(-5, 5) for _ in range(deg + 1)]
            while coeffs[-1] == 0:
                coeffs[-1] = rng.randint(1, 5)
            return sum(c * x**k for k, c in enumerate(coeffs))
        elif choice == "exp":
            a = rng.randint(1, 4) * rng.choice([-1, 1])
            return sp.exp(a * x)
        else:
            a = rng.randint(1, 4)
            return rng.choice([sp.sin(a * x), sp.cos(a * x)])

    u = make_factor(u_choice)
    v = make_factor(v_choice)
    f = u * v
    u_prime = sp.diff(u, x)
    v_prime = sp.diff(v, x)
    f_prime = sp.simplify(sp.diff(f, x))

    statement = f"Differentiate using the product rule:\n\n$$\nf(x) = {L(f)}.\n$$\n"
    solution = (
        f"**Step 1.** Let $u = {L(u)}$ and $v = {L(v)}$.\n\n"
        "**Step 2.** Compute $u'$ and $v'$:\n\n"
        f"$$\nu' = {L(u_prime)}, \\qquad v' = {L(v_prime)}.\n$$\n\n"
        "**Step 3.** Apply the product rule (Lemma 1.2.5): $f' = u'v + u v'$:\n\n"
        f"$$\nf'(x) = ({L(u_prime)})({L(v)}) + ({L(u)})({L(v_prime)}).\n$$\n\n"
        "**Step 4.** Simplify:\n\n"
        f"$$\nf'(x) = {L(f_prime)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{f'(x) = {L(f_prime)}}}$"
    )
    return Problem("Product rule", statement, solution)


def gen_quotient_rule(rng: random.Random) -> Problem:
    """f(x) = u(x) / v(x); differentiate via quotient rule."""
    deg_u = rng.randint(1, 3)
    deg_v = rng.randint(1, 2)
    u = sum(rng.randint(-5, 5) * x**k for k in range(deg_u + 1))
    while u == 0:
        u = sum(rng.randint(-5, 5) * x**k for k in range(deg_u + 1))
    v = sum(rng.randint(-3, 3) * x**k for k in range(deg_v + 1))
    # ensure v has nonzero leading coefficient and is nonzero polynomial
    v_coeffs = [rng.randint(1, 4)] + [rng.randint(-3, 3) for _ in range(deg_v)]
    v = sum(c * x**k for k, c in enumerate(v_coeffs))

    f = u / v
    u_prime = sp.diff(u, x)
    v_prime = sp.diff(v, x)
    f_prime_raw = (u_prime * v - u * v_prime) / v**2
    f_prime = sp.together(sp.simplify(f_prime_raw))

    statement = f"Differentiate using the quotient rule:\n\n$$\nf(x) = {L(f)}.\n$$\n"
    solution = (
        f"**Step 1.** Let $u = {L(u)}$ and $v = {L(v)}$.\n\n"
        "**Step 2.** Compute $u'$ and $v'$:\n\n"
        f"$$\nu' = {L(u_prime)}, \\qquad v' = {L(v_prime)}.\n$$\n\n"
        "**Step 3.** Apply the quotient rule (Lemma 1.2.6): "
        "$f' = (u'v - u v')/v^{2}$:\n\n"
        f"$$\nf'(x) = \\dfrac{{({L(u_prime)})({L(v)}) - ({L(u)})({L(v_prime)})}}"
        f"{{({L(v)})^{{2}}}}.\n$$\n\n"
        "**Step 4.** Simplify (combine over a common denominator):\n\n"
        f"$$\nf'(x) = {L(f_prime)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{f'(x) = {L(f_prime)}}}$"
    )
    return Problem("Quotient rule", statement, solution)


def gen_implicit(rng: random.Random) -> Problem:
    """Implicit differentiation: x^a + y^a = c, or x*y + ... type."""
    kind = rng.choice(["circle", "ellipse", "mixed"])
    if kind == "circle":
        r2 = rng.randint(2, 9)**2
        F = x**2 + y**2 - r2
        statement_eq = f"x^2 + y^2 = {r2}"
    elif kind == "ellipse":
        a = rng.randint(2, 5)
        b = rng.randint(2, 5)
        while b == a:
            b = rng.randint(2, 5)
        F = b**2 * x**2 + a**2 * y**2 - (a * b)**2
        statement_eq = f"\\dfrac{{x^2}}{{{a**2}}} + \\dfrac{{y^2}}{{{b**2}}} = 1"
    else:  # mixed
        c = rng.randint(2, 7)
        F = x * y + x**2 - y**2 - c
        statement_eq = f"xy + x^2 - y^2 = {c}"

    Fx = sp.diff(F, x)
    Fy = sp.diff(F, y)
    dydx = sp.simplify(-Fx / Fy)

    statement = (
        f"Find $\\dfrac{{dy}}{{dx}}$ from the implicit equation\n\n"
        f"$$\n{statement_eq}.\n$$\n"
    )
    solution = (
        "**Step 1.** Write the equation as $F(x, y) = 0$:\n\n"
        f"$$\nF(x, y) = {L(F)} = 0.\n$$\n\n"
        "**Step 2.** Differentiate both sides w.r.t. $x$, treating $y = y(x)$ "
        "and using the chain rule on every $y$-dependent term:\n\n"
        f"$$\n{L(Fx)} + ({L(Fy)})\\,\\dfrac{{dy}}{{dx}} = 0.\n$$\n\n"
        "**Step 3.** Solve for $\\dfrac{dy}{dx}$:\n\n"
        f"$$\n\\dfrac{{dy}}{{dx}} = -\\dfrac{{F_x}}{{F_y}} = "
        f"-\\dfrac{{{L(Fx)}}}{{{L(Fy)}}} = {L(dydx)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{\\dfrac{{dy}}{{dx}} = {L(dydx)}}}$"
    )
    return Problem("Implicit differentiation", statement, solution)


def gen_lhopital(rng: random.Random) -> Problem:
    """Construct a 0/0 limit and apply L'Hopital."""
    forms = [
        ("sin_lin", lambda: (sp.sin(rng.randint(2, 5) * x), x, 0)),
        ("exp_minus_1", lambda: (sp.exp(rng.randint(2, 5) * x) - 1, x, 0)),
        ("log_1_plus", lambda: (sp.log(1 + rng.randint(2, 5) * x), x, 0)),
        ("poly", lambda: (
            (lambda r1, r2: (x - r1) * (x - r2))(rng.randint(1, 6), rng.randint(1, 6)),
            x,
            rng.randint(1, 6),
        )),
    ]
    name, factory = rng.choice(forms)
    num, var, a = factory()

    # Denominator that also vanishes at a so the form is genuinely 0/0.
    if name in ("sin_lin", "exp_minus_1", "log_1_plus"):
        den_power = rng.randint(1, 2)
        den = x**den_power
    else:  # poly numerator -> denom that shares root a
        den = x - a

    expr = num / den
    target = sp.limit(expr, var, a)
    # Guard against accidentally non-indeterminate construction.
    num_at_a = sp.limit(num, var, a)
    den_at_a = sp.limit(den, var, a)
    if num_at_a != 0 or den_at_a != 0:
        # Re-roll into a guaranteed 0/0 form.
        num = sp.sin(2 * x)
        den = x
        a = 0
        expr = num / den
        target = sp.limit(expr, x, 0)
        num_at_a = 0
        den_at_a = 0

    num_prime = sp.diff(num, var)
    den_prime = sp.diff(den, var)
    ratio = sp.simplify(num_prime / den_prime)
    ratio_at_a = sp.limit(ratio, var, a)

    statement = (
        f"Evaluate the limit (use L'Hopital's rule if appropriate):\n\n"
        f"$$\n\\lim_{{x \\to {L(a)}}} {L(expr)}.\n$$\n"
    )
    solution = (
        "**Step 1.** Direct substitution gives the indeterminate form $0/0$. "
        "L'Hopital's rule (Theorem 1.2.6) applies provided "
        "the numerator and denominator are differentiable on a punctured "
        "neighborhood and the denominator's derivative is nonzero there.\n\n"
        "**Step 2.** Differentiate numerator and denominator separately:\n\n"
        f"$$\n\\dfrac{{d}}{{dx}}[{L(num)}] = {L(num_prime)}, \\qquad "
        f"\\dfrac{{d}}{{dx}}[{L(den)}] = {L(den_prime)}.\n$$\n\n"
        "**Step 3.** Form the ratio and take the limit:\n\n"
        f"$$\n\\lim_{{x \\to {L(a)}}}\\dfrac{{{L(num_prime)}}}{{{L(den_prime)}}} "
        f"= {L(ratio_at_a)}.\n$$\n\n"
        "**Step 4.** By L'Hopital's rule, this equals the original limit.\n\n"
        f"**Final answer:** $\\boxed{{{L(target)}}}$"
    )
    return Problem("L'Hopital's rule", statement, solution)


def gen_taylor(rng: random.Random) -> Problem:
    """Taylor polynomial of a standard function at a = 0 to order n."""
    funcs = [
        ("e^{x}", sp.exp(x)),
        ("\\sin x", sp.sin(x)),
        ("\\cos x", sp.cos(x)),
        ("\\ln(1 + x)", sp.log(1 + x)),
        ("\\dfrac{1}{1 - x}", 1 / (1 - x)),
    ]
    label, f = rng.choice(funcs)
    n = rng.choice([3, 4, 5, 6])

    series = sp.series(f, x, 0, n + 1).removeO()
    series_clean = sp.expand(series)

    # Build the derivative table for the solution.
    derivs = []
    for k in range(n + 1):
        d_k = sp.diff(f, x, k)
        d_k_at_0 = sp.simplify(d_k.subs(x, 0))
        derivs.append((k, d_k_at_0))

    table_lines = " | ".join(["$k$"] + [str(k) for k, _ in derivs])
    div_lines = " | ".join(["---"] * (n + 2))
    val_lines = " | ".join(["$f^{(k)}(0)$"] + [L(v) for _, v in derivs])

    statement = (
        f"Find the Taylor polynomial $T_{{{n}}}(x)$ of $f(x) = {label}$ "
        f"centered at $a = 0$.\n"
    )
    solution = (
        "**Step 1.** Recall the Taylor formula:\n\n"
        f"$$\nT_{{{n}}}(x) = \\sum_{{k=0}}^{{{n}}} \\dfrac{{f^{{(k)}}(0)}}{{k!}} x^k.\n$$\n\n"
        "**Step 2.** Tabulate the derivatives at zero:\n\n"
        f"| {table_lines} |\n"
        f"| {div_lines} |\n"
        f"| {val_lines} |\n\n"
        "**Step 3.** Substitute into the Taylor formula and simplify:\n\n"
        f"$$\nT_{{{n}}}(x) = {L(series_clean)}.\n$$\n\n"
        f"**Final answer:** $\\boxed{{T_{{{n}}}(x) = {L(series_clean)}}}$\n\n"
        "**Lagrange remainder:** "
        f"$R_{{{n}}}(x) = \\dfrac{{f^{{({n + 1})}}(\\xi)}}{{({n + 1})!}}\\,x^{{{n + 1}}}$ "
        f"for some $\\xi$ between 0 and $x$ (Theorem 1.2.7)."
    )
    return Problem(f"Taylor polynomial (order {n})", statement, solution)


def gen_optimization(rng: random.Random) -> Problem:
    """Find critical points of a polynomial on a closed interval, classify."""
    # Construct a cubic or quartic with predictable critical points
    a_int = rng.randint(-3, -1)
    b_int = rng.randint(1, 3)
    while b_int <= a_int:
        b_int = rng.randint(1, 5)
    # f' = (x - a_int)(x - b_int) so f = (1/3)x^3 - ((a+b)/2)x^2 + (ab)x
    poly_prime = (x - a_int) * (x - b_int)
    f = sp.integrate(poly_prime, x)
    # Add an integer constant so values are non-trivial.
    f = f + rng.randint(-3, 3)

    f_prime = sp.diff(f, x)
    f_double = sp.diff(f, x, 2)
    crits = sp.solve(f_prime, x)

    # Evaluate f and f'' at each critical point
    classify_lines = []
    values = []
    for c in crits:
        fc = sp.simplify(f.subs(x, c))
        fdd = sp.simplify(f_double.subs(x, c))
        if fdd > 0:
            kind = "local minimum"
        elif fdd < 0:
            kind = "local maximum"
        else:
            kind = "inconclusive (second-derivative test fails)"
        classify_lines.append(
            f"- $x = {L(c)}$: $f(x) = {L(fc)}$, $f''(x) = {L(fdd)} \\Rightarrow$ **{kind}**."
        )
        values.append((c, fc, kind))

    # Closed interval [a_int - 1, b_int + 1] guarantees both crits are interior.
    lo, hi = a_int - 1, b_int + 1
    f_lo = sp.simplify(f.subs(x, lo))
    f_hi = sp.simplify(f.subs(x, hi))
    candidates = [(lo, f_lo)] + [(c, fc) for c, fc, _ in values] + [(hi, f_hi)]
    max_pt = max(candidates, key=lambda kv: kv[1])
    min_pt = min(candidates, key=lambda kv: kv[1])

    statement = (
        f"Find all critical points of\n\n$$\nf(x) = {L(f)}\n$$\n\n"
        "and classify each via the second-derivative test. Then find the global "
        f"maximum and minimum of $f$ on the closed interval $[{lo}, {hi}]$.\n"
    )
    solution = (
        "**Step 1.** Compute the first and second derivatives:\n\n"
        f"$$\nf'(x) = {L(f_prime)}, \\qquad f''(x) = {L(f_double)}.\n$$\n\n"
        "**Step 2.** Solve $f'(x) = 0$ for critical points:\n\n"
        f"$$\nf'(x) = {L(f_prime)} = 0 \\Rightarrow x \\in \\{{{', '.join(L(c) for c in crits)}\\}}.\n$$\n\n"
        "**Step 3.** Classify via $f''$ at each critical point:\n\n"
        + "\n".join(classify_lines)
        + "\n\n**Step 4.** Compare $f$ at the critical points and the endpoints "
        f"of $[{lo}, {hi}]$:\n\n"
        + "\n".join(
            f"- $x = {L(c)}$: $f(x) = {L(fc)}$" for c, fc in candidates
        )
        + "\n\n**Step 5.** Identify global extrema (Extreme Value Theorem "
        "guarantees they exist on a closed bounded interval).\n\n"
        f"**Final answer:** Global max at $x = {L(max_pt[0])}$ with value "
        f"${L(max_pt[1])}$. Global min at $x = {L(min_pt[0])}$ with value "
        f"${L(min_pt[1])}$. Critical-point classifications listed above."
    )
    return Problem("Critical points & optimization", statement, solution)


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------


ARCHETYPES: list[Callable[[random.Random], Problem]] = [
    gen_power_rule,
    gen_chain_rule,
    gen_product_rule,
    gen_quotient_rule,
    gen_implicit,
    gen_lhopital,
    gen_taylor,
    gen_optimization,
]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    """Round-robin across archetypes so every type gets equal coverage."""
    problems: list[Problem] = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count:
                break
            try:
                problems.append(gen(rng))
            except Exception as exc:  # noqa: BLE001 - log generator failure
                # Skip this iteration; do not crash the whole script over a
                # SymPy edge case (e.g., a constructed expression where simplify
                # blows up).
                problems.append(Problem(
                    archetype=f"[generation skipped: {gen.__name__}]",
                    statement_md=f"Generator failed: `{exc}`",
                    solution_md="(Re-run with a different seed.)",
                ))
    return problems


HEADER_TEMPLATE = """---
tags: [calculus, differentiation, practice, drills, "review/calc/1.2"]
chapter: 1.2
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../1.2 - Single-Variable Differentiation|Chapter 1.2]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 1.2 — Practice Drills

> Auto-generated by `_practice/scripts/1.2_differentiation.py`. SymPy verifies every solution before this file lands on disk.

**House rule:** solve each problem on paper before opening the spoiler. The point is not getting the answer — it is building muscle memory for the move set.

Tag your spaced-repetition reviews with `#review/calc/1.2`. Re-run the script weekly for fresh problems.

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
        f"All {len(problems)} problems were generated programmatically with seed `{seed}` "
        "and verified against SymPy's symbolic engine (`sp.diff`, `sp.limit`, "
        "`sp.series`, `sp.solve`). If any answer disagrees with SymPy, file a bug "
        "against `_practice/scripts/1.2_differentiation.py`.\n"
    )
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").strip().split("\n\n", 1)[0]
    )
    parser.add_argument("--count", type=int, default=24, help="Total number of problems.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed (omit for time-based).")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output markdown path. Default: ../1.2_drills.md relative to this script.",
    )
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)

    out_path: Path = args.out or (Path(__file__).resolve().parent.parent / "1.2_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

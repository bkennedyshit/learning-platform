#!/usr/bin/env python3
"""
8.1_lorentz_boosts.py — Practice problem generator for Chapter 8.1
(Special Relativity Postulates & Lorentz Boosts).

Generates randomized drill problems across 8 archetypes:
  1. Time dilation calculation
  2. Length contraction calculation
  3. Relativistic velocity addition
  4. Invariant interval classification
  5. Lorentz boost matrix multiplication
  6. Relativistic Doppler shift
  7. Rapidity composition
  8. Twin paradox proper-time comparison

Usage:
  python 8.1_lorentz_boosts.py
  python 8.1_lorentz_boosts.py --count 24 --seed 42
  python 8.1_lorentz_boosts.py --count 24 --seed 42 --out /tmp/_81.md

Exit code 0 on success.
#review/physics
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import sympy as sp
from sympy import sqrt, Rational, atanh, cosh, sinh, tanh, simplify, latex


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
# Archetype 1: Time dilation
# ---------------------------------------------------------------------------
def gen_time_dilation(rng: random.Random) -> Problem:
    betas = [Rational(3, 5), Rational(4, 5), Rational(12, 13), Rational(5, 13),
             Rational(7, 25), Rational(24, 25)]
    beta = rng.choice(betas)
    gamma = 1 / sqrt(1 - beta**2)
    tau = Rational(rng.randint(1, 10), 1)  # proper time in microseconds
    dt = simplify(gamma * tau)
    stmt = (
        f"A particle moves at $\\beta = {latex(beta)}$ relative to the lab. "
        f"Its proper lifetime is $\\tau_0 = {latex(tau)}\\,\\mu\\text{{s}}$. "
        "Compute the dilated lifetime $\\Delta t$ measured in the lab frame."
    )
    sol = (
        f"$\\gamma = \\frac{{1}}{{\\sqrt{{1 - ({latex(beta)})^2}}}} = {latex(gamma)}$.\n\n"
        f"$$\n\\Delta t = \\gamma \\tau_0 = {latex(gamma)} \\times {latex(tau)} = {latex(dt)}\\,\\mu\\text{{s}}\n$$\n"
    )
    assert simplify(gamma**2 * (1 - beta**2) - 1) == 0
    return Problem("Time Dilation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Length contraction
# ---------------------------------------------------------------------------
def gen_length_contraction(rng: random.Random) -> Problem:
    betas = [Rational(3, 5), Rational(4, 5), Rational(5, 13), Rational(12, 13)]
    beta = rng.choice(betas)
    gamma = 1 / sqrt(1 - beta**2)
    L0 = Rational(rng.randint(5, 50), 1)  # proper length in meters
    L = simplify(L0 / gamma)
    stmt = (
        f"A spacecraft of proper length $L_0 = {latex(L0)}$ m moves at $\\beta = {latex(beta)}$. "
        "Compute the contracted length $L$ as measured by a stationary observer."
    )
    sol = (
        f"$\\gamma = {latex(gamma)}$.\n\n"
        f"$$\nL = \\frac{{L_0}}{{\\gamma}} = \\frac{{{latex(L0)}}}{{{latex(gamma)}}} = {latex(L)}\\,\\text{{m}}\n$$\n"
    )
    return Problem("Length Contraction", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Relativistic velocity addition
# ---------------------------------------------------------------------------
def gen_velocity_addition(rng: random.Random) -> Problem:
    betas_v = [Rational(1, 2), Rational(3, 5), Rational(4, 5), Rational(3, 4)]
    betas_u = [Rational(1, 2), Rational(3, 5), Rational(4, 5), Rational(2, 3)]
    beta_v = rng.choice(betas_v)
    beta_u = rng.choice(betas_u)
    # u_total = (u + v) / (1 + uv/c^2) in units of c
    u_total = simplify((beta_u + beta_v) / (1 + beta_u * beta_v))
    stmt = (
        f"Frame $S'$ moves at $v = {latex(beta_v)}c$ relative to $S$. "
        f"An object moves at $u' = {latex(beta_u)}c$ in $S'$ (same direction). "
        "Find the object's velocity $u$ in frame $S$."
    )
    sol = (
        f"$$\nu = \\frac{{u' + v}}{{1 + u'v/c^2}} = "
        f"\\frac{{{latex(beta_u)}c + {latex(beta_v)}c}}{{1 + ({latex(beta_u)})({latex(beta_v)})}} = "
        f"\\frac{{{latex(beta_u + beta_v)}c}}{{{latex(1 + beta_u*beta_v)}}} = {latex(u_total)}c\n$$\n\n"
        f"Verify: $|u| = {latex(u_total)}c < c$ ✓"
    )
    assert u_total < 1
    return Problem("Relativistic Velocity Addition", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Invariant interval classification
# ---------------------------------------------------------------------------
def gen_interval(rng: random.Random) -> Problem:
    ct = Rational(rng.randint(-10, 10), 1)
    dx = Rational(rng.randint(-10, 10), 1)
    s2 = -ct**2 + dx**2
    if s2 < 0:
        classification = "Timelike"
    elif s2 > 0:
        classification = "Spacelike"
    else:
        classification = "Lightlike (null)"
    stmt = (
        f"Two events are separated by $c\\Delta t = {latex(ct)}$ m and $\\Delta x = {latex(dx)}$ m. "
        "Compute $\\Delta s^2$ and classify the interval."
    )
    sol = (
        f"$$\n\\Delta s^2 = -(c\\Delta t)^2 + (\\Delta x)^2 = -({latex(ct)})^2 + ({latex(dx)})^2 = "
        f"{latex(-ct**2)} + {latex(dx**2)} = {latex(s2)}\\,\\text{{m}}^2\n$$\n\n"
        f"Classification: **{classification}** ($\\Delta s^2 {'< 0' if s2 < 0 else '> 0' if s2 > 0 else '= 0'}$)."
    )
    return Problem("Invariant Interval Classification", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Lorentz boost matrix multiplication
# ---------------------------------------------------------------------------
def gen_boost_matrix(rng: random.Random) -> Problem:
    betas = [Rational(3, 5), Rational(4, 5), Rational(5, 13)]
    beta = rng.choice(betas)
    gamma = 1 / sqrt(1 - beta**2)
    ct = Rational(rng.randint(1, 15), 1)
    x = Rational(rng.randint(-10, 10), 1)
    ct_prime = simplify(gamma * (ct - beta * x))
    x_prime = simplify(gamma * (x - beta * ct))
    stmt = (
        f"Apply the Lorentz boost ($\\beta = {latex(beta)}$) to the event "
        f"$(ct, x) = ({latex(ct)}, {latex(x)})$ m. Find $(ct', x')$."
    )
    sol = (
        f"$\\gamma = {latex(gamma)}$, $\\beta\\gamma = {latex(simplify(beta*gamma))}$.\n\n"
        f"$$\nct' = \\gamma(ct - \\beta x) = {latex(gamma)}({latex(ct)} - {latex(beta)} \\cdot {latex(x)}) = "
        f"{latex(gamma)} \\cdot {latex(ct - beta*x)} = {latex(ct_prime)}\n$$\n\n"
        f"$$\nx' = \\gamma(x - \\beta\\, ct) = {latex(gamma)}({latex(x)} - {latex(beta)} \\cdot {latex(ct)}) = "
        f"{latex(gamma)} \\cdot {latex(x - beta*ct)} = {latex(x_prime)}\n$$\n\n"
        f"Interval check: $-(ct')^2 + (x')^2 = {latex(simplify(-ct_prime**2 + x_prime**2))}$ = "
        f"$-(ct)^2 + x^2 = {latex(-ct**2 + x**2)}$ ✓"
    )
    assert simplify(-ct_prime**2 + x_prime**2 - (-ct**2 + x**2)) == 0
    return Problem("Lorentz Boost Matrix", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: Relativistic Doppler shift
# ---------------------------------------------------------------------------
def gen_doppler(rng: random.Random) -> Problem:
    betas = [Rational(1, 3), Rational(3, 5), Rational(4, 5), Rational(1, 2)]
    beta = rng.choice(betas)
    receding = rng.choice([True, False])
    if receding:
        ratio = sqrt((1 - beta) / (1 + beta))
        direction = "receding"
    else:
        ratio = sqrt((1 + beta) / (1 - beta))
        direction = "approaching"
    f_source = Rational(rng.choice([100, 200, 500, 1000]), 1)  # MHz
    f_obs = simplify(f_source * ratio)
    stmt = (
        f"A source emits at $f_{{\\text{{source}}}} = {latex(f_source)}$ MHz and is "
        f"**{direction}** at $\\beta = {latex(beta)}$. Compute $f_{{\\text{{obs}}}}$."
    )
    sol = (
        f"For a {direction} source:\n\n"
        f"$$\nf_{{\\text{{obs}}}} = f_{{\\text{{source}}}} \\sqrt{{\\frac{{1 {'- ' if receding else '+ '}"
        f"\\beta}}{{1 {'+ ' if receding else '- '}\\beta}}}} = "
        f"{latex(f_source)} \\sqrt{{\\frac{{{latex(1-beta if receding else 1+beta)}}}"
        f"{{{latex(1+beta if receding else 1-beta)}}}}} = {latex(f_obs)}\\,\\text{{MHz}}\n$$\n"
    )
    return Problem("Relativistic Doppler Shift", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 7: Rapidity composition
# ---------------------------------------------------------------------------
def gen_rapidity(rng: random.Random) -> Problem:
    betas = [Rational(3, 5), Rational(4, 5), Rational(1, 2), Rational(5, 13)]
    b1 = rng.choice(betas)
    b2 = rng.choice(betas)
    # Composed beta
    b_total = simplify((b1 + b2) / (1 + b1 * b2))
    stmt = (
        f"Frame $S'$ moves at $\\beta_1 = {latex(b1)}$ relative to $S$, and $S''$ moves at "
        f"$\\beta_2 = {latex(b2)}$ relative to $S'$ (same direction). "
        "Verify that rapidities add: $\\phi = \\phi_1 + \\phi_2$, and find $\\beta_{{\\text{{total}}}}$."
    )
    sol = (
        f"$\\phi_1 = \\tanh^{{-1}}({latex(b1)})$, $\\phi_2 = \\tanh^{{-1}}({latex(b2)})$.\n\n"
        f"$\\phi = \\phi_1 + \\phi_2 \\implies \\beta_{{\\text{{total}}}} = \\tanh(\\phi_1 + \\phi_2)$.\n\n"
        f"By velocity addition: $\\beta_{{\\text{{total}}}} = \\frac{{{latex(b1)} + {latex(b2)}}}"
        f"{{1 + {latex(b1)} \\cdot {latex(b2)}}} = \\frac{{{latex(b1+b2)}}}{{{latex(1+b1*b2)}}} = {latex(b_total)}$.\n\n"
        f"Verify $|\\beta_{{\\text{{total}}}}| = {latex(b_total)} < 1$ ✓"
    )
    assert b_total < 1
    return Problem("Rapidity Composition", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 8: Twin paradox proper time
# ---------------------------------------------------------------------------
def gen_twin_paradox(rng: random.Random) -> Problem:
    betas = [Rational(3, 5), Rational(4, 5), Rational(12, 13), Rational(24, 25)]
    beta = rng.choice(betas)
    gamma = 1 / sqrt(1 - beta**2)
    L = Rational(rng.randint(2, 20), 1)  # light-years
    t_A = simplify(2 * L / beta)  # years (Earth twin)
    tau_B = simplify(t_A / gamma)  # years (traveling twin)
    stmt = (
        f"Twin B travels to a star $L = {latex(L)}$ light-years away at $\\beta = {latex(beta)}$ "
        "and returns at the same speed. Twin A stays on Earth. "
        "Compute the elapsed time for each twin."
    )
    sol = (
        f"$\\gamma = {latex(gamma)}$.\n\n"
        f"Twin A (Earth): $\\Delta t_A = \\frac{{2L}}{{v}} = \\frac{{2 \\times {latex(L)}}}{{{latex(beta)}}} = "
        f"{latex(t_A)}$ years.\n\n"
        f"Twin B (traveler): $\\Delta\\tau_B = \\frac{{\\Delta t_A}}{{\\gamma}} = "
        f"\\frac{{{latex(t_A)}}}{{{latex(gamma)}}} = {latex(tau_B)}$ years.\n\n"
        f"Age difference: ${latex(simplify(t_A - tau_B))}$ years — Twin B is younger."
    )
    assert simplify(tau_B - t_A / gamma) == 0
    return Problem("Twin Paradox Proper Time", stmt, sol)


# ---------------------------------------------------------------------------
# Generator registry & main
# ---------------------------------------------------------------------------
GENERATORS = [
    gen_time_dilation,
    gen_length_contraction,
    gen_velocity_addition,
    gen_interval,
    gen_boost_matrix,
    gen_doppler,
    gen_rapidity,
    gen_twin_paradox,
]


def generate_problem_set(count: int, seed: int) -> list[Problem]:
    rng = random.Random(seed)
    problems = []
    for i in range(count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))
    return problems


def main():
    parser = argparse.ArgumentParser(description="SR Lorentz Boost practice problems")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    problems = generate_problem_set(args.count, seed)

    header = (
        "---\n"
        "tags: [practice, special-relativity, lorentz-boost, time-dilation]\n"
        f"seed: {seed}\n"
        "---\n\n"
        "# 8.1 Practice — Lorentz Boosts & SR Kinematics\n\n"
        f"Generated {args.count} problems (seed={seed}).\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

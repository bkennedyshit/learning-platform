#!/usr/bin/env python3
"""
9.1_schrodinger.py — Practice problem generator for Chapter 9.1
(Wave Functions & The Schrödinger Equation).

Generates randomized drill problems across 6 archetypes:
  1. Normalize a given wave function
  2. Compute expectation value ⟨x⟩ or ⟨p⟩
  3. Verify the uncertainty principle ΔxΔp ≥ ℏ/2
  4. Compute probability of finding particle in [a,b]
  5. Evaluate a commutator [A, B]
  6. Time evolution of a superposition state

Usage:
  python 9.1_schrodinger.py
  python 9.1_schrodinger.py --count 12 --seed 42
  python 9.1_schrodinger.py --count 12 --seed 42 --out /tmp/_91.md
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

x, hbar, m, L, n, a_sym = sp.symbols('x hbar m L n a', positive=True)

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

def gen_normalize(rng: random.Random) -> Problem:
    power = rng.choice([1, 2, 3])
    psi_expr = sp.Symbol('A') * x**power * sp.exp(-a_sym * x)
    norm_sq = sp.integrate(x**(2*power) * sp.exp(-2*a_sym*x), (x, 0, sp.oo))
    A_val = 1 / sp.sqrt(norm_sq)
    stmt = (f"Normalize $\\Psi(x) = Ax^{{{power}}}e^{{-ax}}$ for $x \\geq 0$ (with $a > 0$). "
            "Find the normalization constant $A$.")
    sol = (f"$\\int_0^\\infty |A|^2 x^{{{2*power}}} e^{{-2ax}}\\,dx = 1$.\n\n"
           f"Using $\\int_0^\\infty x^n e^{{-\\alpha x}}dx = n!/\\alpha^{{n+1}}$:\n\n"
           f"$$\n|A|^2 \\cdot \\frac{{{sp.factorial(2*power)}}}{{(2a)^{{{2*power+1}}}}} = 1\n$$\n\n"
           f"$$\nA = {sp.latex(sp.simplify(A_val))}\n$$")
    return Problem("Normalize a wave function", stmt, sol)

def gen_expectation(rng: random.Random) -> Problem:
    n_val = rng.randint(1, 4)
    stmt = (f"For the infinite square well eigenstate $\\psi_{n_val}(x) = \\sqrt{{2/L}}\\sin({n_val}\\pi x/L)$, "
            f"compute $\\langle x \\rangle$ and $\\langle x^2 \\rangle$.")
    x_exp = sp.Rational(1, 2)
    x2_exp = sp.Rational(1, 3) - sp.Rational(1, 2*n_val**2 * sp.pi**2)
    sol = (f"$\\langle x\\rangle = L/2$ (by symmetry of $\\sin^2$ about $L/2$).\n\n"
           f"$\\langle x^2\\rangle = L^2\\left(\\frac{{1}}{{3}} - \\frac{{1}}{{2\\cdot{n_val**2}\\pi^2}}\\right)"
           f" = L^2\\left(\\frac{{1}}{{3}} - \\frac{{1}}{{{2*n_val**2}\\pi^2}}\\right)$.")
    return Problem("Expectation value in infinite well", stmt, sol)

def gen_uncertainty(rng: random.Random) -> Problem:
    stmt = ("For the Gaussian wave packet $\\Psi(x) = (2a/\\pi)^{1/4}e^{-ax^2}$, "
            "compute $\\Delta x$ and $\\Delta p$ and verify $\\Delta x\\Delta p = \\hbar/2$.")
    sol = ("$\\langle x\\rangle = 0$, $\\langle x^2\\rangle = 1/(4a)$, so $\\Delta x = 1/(2\\sqrt{a})$.\n\n"
           "$\\langle p\\rangle = 0$, $\\langle p^2\\rangle = a\\hbar^2$, so $\\Delta p = \\hbar\\sqrt{a}$.\n\n"
           "$\\Delta x \\cdot \\Delta p = \\frac{1}{2\\sqrt{a}}\\cdot\\hbar\\sqrt{a} = \\frac{\\hbar}{2}$. ✓ (minimum uncertainty)")
    return Problem("Uncertainty principle verification", stmt, sol)

def gen_probability(rng: random.Random) -> Problem:
    n_val = rng.choice([1, 2, 3])
    a_frac = rng.choice([(0, sp.Rational(1,4)), (sp.Rational(1,4), sp.Rational(1,2))])
    stmt = (f"For $\\psi_{n_val}(x) = \\sqrt{{2/L}}\\sin({n_val}\\pi x/L)$ in a well of width $L$, "
            f"find $P({a_frac[0]}L \\leq x \\leq {a_frac[1]}L)$.")
    t = sp.Symbol('t')
    integral = sp.integrate(sp.sin(n_val*sp.pi*t)**2, (t, float(a_frac[0]), float(a_frac[1])))
    prob = 2 * integral
    sol = (f"$P = \\frac{{2}}{{L}}\\int_{{{a_frac[0]}L}}^{{{a_frac[1]}L}} \\sin^2({n_val}\\pi x/L)\\,dx "
           f"= 2\\int_{{{float(a_frac[0])}}}^{{{float(a_frac[1])}}} \\sin^2({n_val}\\pi t)\\,dt = {sp.latex(sp.nsimplify(prob))}$.")
    return Problem("Probability in an interval", stmt, sol)

def gen_commutator(rng: random.Random) -> Problem:
    power = rng.randint(2, 4)
    stmt = (f"Compute the commutator $[\\hat{{x}}^{power}, \\hat{{p}}]$ and verify it equals $i{power}\\hbar\\hat{{x}}^{{{power-1}}}$.")
    sol = (f"Using $[\\hat{{x}}^n, \\hat{{p}}] = in\\hbar\\hat{{x}}^{{n-1}}$ (proved by induction):\n\n"
           f"$[\\hat{{x}}^{power}, \\hat{{p}}] = i\\cdot{power}\\cdot\\hbar\\cdot\\hat{{x}}^{{{power-1}}}$.\n\n"
           f"Direct verification: act on test function $f(x)$:\n\n"
           f"$[\\hat{{x}}^{power}, \\hat{{p}}]f = x^{power}(-i\\hbar f') - (-i\\hbar)(x^{power} f)' "
           f"= -i\\hbar x^{power} f' + i\\hbar({power}x^{{{power-1}}}f + x^{power} f') = i{power}\\hbar x^{{{power-1}}}f$. ✓")
    return Problem("Commutator computation", stmt, sol)

def gen_time_evolution(rng: random.Random) -> Problem:
    stmt = ("A particle in an infinite well starts in $\\Psi(x,0) = \\frac{1}{\\sqrt{2}}(\\psi_1 + \\psi_3)$. "
            "Write $\\Psi(x,t)$ and compute $\\langle\\hat{H}\\rangle$.")
    sol = ("$\\Psi(x,t) = \\frac{1}{\\sqrt{2}}\\psi_1 e^{-iE_1t/\\hbar} + \\frac{1}{\\sqrt{2}}\\psi_3 e^{-iE_3t/\\hbar}$.\n\n"
           "$\\langle\\hat{H}\\rangle = \\frac{1}{2}E_1 + \\frac{1}{2}E_3 = \\frac{1}{2}\\frac{\\pi^2\\hbar^2}{2mL^2}(1+9) = \\frac{5\\pi^2\\hbar^2}{2mL^2}$.\n\n"
           "Note: $\\langle H\\rangle$ is time-independent (energy is conserved).")
    return Problem("Time evolution of superposition", stmt, sol)

GENERATORS = [gen_normalize, gen_expectation, gen_uncertainty, gen_probability, gen_commutator, gen_time_evolution]

def main():
    parser = argparse.ArgumentParser(description="QM Chapter 9.1 practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = []
    for i in range(args.count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))
    header = "# 9.1 Practice — Wave Functions & Schrödinger Equation\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

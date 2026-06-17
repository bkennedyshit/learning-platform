#!/usr/bin/env python3
"""
9.8_path_integrals.py — Practice problems for Chapter 9.8 (Feynman Path Integrals & QED).

Archetypes:
  1. Free-particle propagator from path integral
  2. Gaussian functional integral evaluation
  3. Feynman rules application (draw diagram, write amplitude)
  4. Mandelstam variables computation
  5. Cross section from |M|²
  6. Wick's theorem contraction counting
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_free_propagator(rng: random.Random) -> Problem:
    stmt = ("Derive the free-particle propagator $K(x_f,T;x_i,0)$ from the path integral "
            "by evaluating the classical action and the fluctuation determinant.")
    sol = ("Classical path: $x_{cl}(t) = x_i + (x_f-x_i)t/T$.\n\n"
           "$S_{cl} = \\frac{m(x_f-x_i)^2}{2T}$.\n\n"
           "Fluctuation integral: $\\sqrt{m/(2\\pi i\\hbar T)}$.\n\n"
           "$K = \\sqrt{\\frac{m}{2\\pi i\\hbar T}}\\exp\\left[\\frac{im(x_f-x_i)^2}{2\\hbar T}\\right]$.")
    return Problem("Free-particle propagator", stmt, sol)

def gen_gaussian_integral(rng: random.Random) -> Problem:
    stmt = ("Evaluate the Gaussian integral $\\int_{-\\infty}^{\\infty}dx\\,e^{-ax^2+bx}$ "
            "and state the result for the generating functional $Z_0[J]$.")
    sol = ("Complete the square: $-ax^2+bx = -a(x-b/2a)^2 + b^2/4a$.\n\n"
           "$\\int dx\\,e^{-ax^2+bx} = \\sqrt{\\pi/a}\\,e^{b^2/4a}$.\n\n"
           "For the field theory: $Z_0[J] = Z_0[0]\\exp\\left[\\frac{1}{2}\\int d^4x\\,d^4y\\,J(x)D_F(x-y)J(y)\\right]$.")
    return Problem("Gaussian functional integral", stmt, sol)

def gen_feynman_rules(rng: random.Random) -> Problem:
    process = rng.choice(["e⁺e⁻ → μ⁺μ⁻", "e⁻γ → e⁻γ (Compton)"])
    if "μ" in process:
        sol = ("Single s-channel diagram. Amplitude:\n\n"
               "$i\\mathcal{M} = [\\bar{v}(p_2)(-ie\\gamma^\\mu)u(p_1)]\\frac{-ig_{\\mu\\nu}}{s}[\\bar{u}(p_3)(-ie\\gamma^\\nu)v(p_4)]$\n\n"
               "$= \\frac{-ie^2}{s}[\\bar{v}_2\\gamma^\\mu u_1][\\bar{u}_3\\gamma_\\mu v_4]$.")
    else:
        sol = ("Two diagrams: s-channel and u-channel.\n\n"
               "s-channel: photon absorbed then emitted.\n"
               "u-channel: photon emitted then absorbed (crossed diagram).\n\n"
               "Total: $i\\mathcal{M} = -ie^2\\bar{u}(p')\\left[\\frac{\\gamma^\\nu\\not{k}\\gamma^\\mu + 2m\\gamma^\\nu g^{\\mu0}}{s-m^2} + (s\\leftrightarrow u)\\right]u(p)\\epsilon_\\mu\\epsilon^*_\\nu$.")
    stmt = f"Write the tree-level Feynman amplitude for {process} using QED Feynman rules."
    return Problem("Feynman rules application", stmt, sol)

def gen_mandelstam(rng: random.Random) -> Problem:
    stmt = ("For $2\\to2$ scattering with all particles massless, show $s + t + u = 0$ "
            "and express $t$ in terms of $s$ and scattering angle $\\theta$.")
    sol = ("$s = (p_1+p_2)^2$, $t = (p_1-p_3)^2$, $u = (p_1-p_4)^2$.\n\n"
           "$s+t+u = \\sum m_i^2 = 0$ (massless).\n\n"
           "In CM frame: $t = -\\frac{s}{2}(1-\\cos\\theta)$, $u = -\\frac{s}{2}(1+\\cos\\theta)$.")
    return Problem("Mandelstam variables", stmt, sol)

def gen_cross_section(rng: random.Random) -> Problem:
    stmt = ("Given $\\frac{1}{4}\\sum|\\mathcal{M}|^2 = e^4(1+\\cos^2\\theta)$ for $e^+e^-\\to\\mu^+\\mu^-$, "
            "compute $d\\sigma/d\\Omega$ and $\\sigma_{\\text{total}}$.")
    sol = ("$\\frac{d\\sigma}{d\\Omega} = \\frac{|\\mathcal{M}|^2}{64\\pi^2 s} = \\frac{\\alpha^2}{4s}(1+\\cos^2\\theta)$.\n\n"
           "$\\sigma = \\int\\frac{d\\sigma}{d\\Omega}d\\Omega = \\frac{\\alpha^2}{4s}\\int_0^\\pi(1+\\cos^2\\theta)2\\pi\\sin\\theta\\,d\\theta$\n\n"
           "$= \\frac{\\alpha^2\\pi}{2s}\\cdot\\frac{8}{3} = \\frac{4\\pi\\alpha^2}{3s}$.")
    return Problem("Cross section computation", stmt, sol)

def gen_wick(rng: random.Random) -> Problem:
    n = rng.choice([4, 6])
    pairings = {4: 3, 6: 15}
    stmt = f"How many distinct Wick contractions exist for $\\langle 0|T\\phi(x_1)\\cdots\\phi(x_{n})|0\\rangle$?"
    sol = (f"Number of pairings of {n} objects = $(2n-1)!! = {pairings[n]}$.\n\n"
           f"For $n={n}$: ${n-1}!! = {pairings[n]}$ distinct contractions, each giving a product of {n//2} propagators.")
    return Problem("Wick's theorem counting", stmt, sol)

GENERATORS = [gen_free_propagator, gen_gaussian_integral, gen_feynman_rules,
              gen_mandelstam, gen_cross_section, gen_wick]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]
    header = "# 9.8 Practice — Feynman Path Integrals & QED\n\n#review/physics\n\n"
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()

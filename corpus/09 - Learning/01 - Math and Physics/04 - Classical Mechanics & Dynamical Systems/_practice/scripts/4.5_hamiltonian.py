#!/usr/bin/env python3
"""
4.5_hamiltonian.py — Practice problem generator for Chapter 4.5
(Hamiltonian Mechanics: Canonical Equations).

Archetypes:
  1. Legendre transform L -> H
  2. Hamilton's equations for SHO
  3. Phase portrait classification
  4. Hamiltonian for central force
  5. Verify Liouville (divergence = 0)
  6. Identify when H ≠ E

Usage:
  python 4.5_hamiltonian.py --count 8 --seed 42
"""
from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp


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


def gen_legendre_transform(rng: random.Random) -> Problem:
    m = rng.randint(1, 5)
    k = rng.randint(1, 8)
    stmt = (
        f"Given $L = \\frac{{1}}{{2}}({m})\\dot q^2 - \\frac{{1}}{{2}}({k})q^2$, "
        "perform the Legendre transform to find $H(q, p)$."
    )
    sol = (
        f"$p = \\frac{{\\partial L}}{{\\partial\\dot q}} = {m}\\dot q \\implies \\dot q = \\frac{{p}}{{{m}}}$\n\n"
        f"$H = p\\dot q - L = p\\cdot\\frac{{p}}{{{m}}} - \\frac{{{m}}}{{2}}\\cdot\\frac{{p^2}}{{{m}^2}} + \\frac{{{k}}}{{2}}q^2$\n\n"
        f"$H = \\frac{{p^2}}{{{m}}} - \\frac{{p^2}}{{{2*m}}} + \\frac{{{k}}}{{2}}q^2 = \\frac{{p^2}}{{{2*m}}} + \\frac{{{k}}}{{2}}q^2$\n\n"
        f"This equals $T + U$ as expected for a natural system."
    )
    return Problem("Legendre Transform (L → H)", stmt, sol)


def gen_hamilton_eqs(rng: random.Random) -> Problem:
    a = rng.randint(1, 4)
    b = rng.randint(1, 6)
    c = rng.randint(1, 3)
    stmt = (
        f"Given $H = \\frac{{p^2}}{{{2*a}}} + {b}q^{c}$, write Hamilton's equations "
        "and identify the type of motion."
    )
    sol = (
        f"$\\dot q = \\frac{{\\partial H}}{{\\partial p}} = \\frac{{p}}{{{a}}}$\n\n"
        f"$\\dot p = -\\frac{{\\partial H}}{{\\partial q}} = -{b*c}q^{{{c-1}}}$\n\n"
    )
    if c == 2:
        sol += f"This is a harmonic oscillator with $\\omega = \\sqrt{{{2*b}/{a}}}$."
    elif c == 1:
        sol += "This is uniform acceleration (constant force)."
    else:
        sol += f"This is a nonlinear oscillator (anharmonic potential $\\propto q^{c}$)."
    return Problem("Hamilton's Equations", stmt, sol)


def gen_phase_portrait(rng: random.Random) -> Problem:
    system = rng.choice(["SHO", "pendulum", "free_particle"])
    if system == "SHO":
        stmt = "Sketch the phase portrait for $H = \\frac{p^2}{2m} + \\frac{1}{2}kq^2$. What are the level curves?"
        sol = (
            "Level curves $H = E$: $\\frac{p^2}{2mE} + \\frac{kq^2}{2E} = 1$ — **ellipses** centered at origin.\n\n"
            "All trajectories are closed (periodic). The origin is a **center** (stable equilibrium).\n\n"
            "Flow direction: clockwise (since $\\dot q = p/m > 0$ when $p > 0$, and $\\dot p = -kq < 0$ when $q > 0$)."
        )
    elif system == "pendulum":
        stmt = "Sketch the phase portrait for a simple pendulum $H = \\frac{p^2}{2ml^2} - mgl\\cos\\theta$. Identify the separatrix."
        sol = (
            "For $E < mgl$: closed orbits (libration) around $\\theta=0$.\n\n"
            "For $E > mgl$: open curves (rotation, $\\theta$ increases monotonically).\n\n"
            "Separatrix: $E = mgl$ passes through the unstable equilibrium $(\\theta=\\pi, p=0)$.\n\n"
            "The separatrix divides phase space into oscillation and rotation regions."
        )
    else:
        stmt = "Sketch the phase portrait for a free particle $H = p^2/(2m)$. Describe the trajectories."
        sol = (
            "Hamilton's equations: $\\dot q = p/m$, $\\dot p = 0$.\n\n"
            "Trajectories: horizontal lines $p = \\text{const}$ in $(q,p)$ space.\n\n"
            "Each line represents uniform motion at constant velocity $v = p/m$."
        )
    return Problem("Phase Portrait Analysis", stmt, sol)


def gen_liouville_check(rng: random.Random) -> Problem:
    a = rng.randint(1, 5)
    b = rng.randint(1, 5)
    stmt = (
        f"Verify Liouville's theorem for $H = {a}qp + {b}q^2$. "
        "Compute the phase-space divergence of the Hamiltonian flow."
    )
    sol = (
        f"$\\dot q = \\frac{{\\partial H}}{{\\partial p}} = {a}q$\n\n"
        f"$\\dot p = -\\frac{{\\partial H}}{{\\partial q}} = -{a}p - {2*b}q$\n\n"
        f"Divergence: $\\frac{{\\partial\\dot q}}{{\\partial q}} + \\frac{{\\partial\\dot p}}{{\\partial p}} = {a} + (-{a}) = 0$ ✓\n\n"
        "Liouville's theorem is satisfied: phase-space volume is conserved."
    )
    return Problem("Liouville's Theorem Verification", stmt, sol)


def gen_h_neq_e(rng: random.Random) -> Problem:
    stmt = (
        "A bead slides on a wire rotating at angular velocity $\\Omega$. "
        "The Lagrangian is $L = \\frac{1}{2}m(\\dot r^2 + r^2\\Omega^2) - U(r)$. "
        "Show that $H \\neq T + U$ and find what $H$ equals."
    )
    sol = (
        "$p_r = m\\dot r$, so $\\dot r = p_r/m$.\n\n"
        "$H = p_r\\dot r - L = \\frac{p_r^2}{m} - \\frac{1}{2}m\\frac{p_r^2}{m^2} - \\frac{1}{2}mr^2\\Omega^2 + U(r)$\n\n"
        "$H = \\frac{p_r^2}{2m} - \\frac{1}{2}mr^2\\Omega^2 + U(r)$\n\n"
        "But $T = \\frac{1}{2}m\\dot r^2 + \\frac{1}{2}mr^2\\Omega^2 = \\frac{p_r^2}{2m} + \\frac{1}{2}mr^2\\Omega^2$.\n\n"
        "So $H = T - mr^2\\Omega^2 + U = T + U - mr^2\\Omega^2 \\neq E$.\n\n"
        "$H$ is the **Jacobi integral** (energy in rotating frame), not total energy. "
        "This happens because the constraint is rheonomic (time-dependent)."
    )
    return Problem("H ≠ E (Rheonomic System)", stmt, sol)


GENERATORS = [
    gen_legendre_transform, gen_hamilton_eqs, gen_phase_portrait,
    gen_liouville_check, gen_h_neq_e, gen_legendre_transform,
]


def main():
    parser = argparse.ArgumentParser(description="Generate Hamiltonian mechanics problems")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    lines = ["---", "tags: [review/math, hamiltonian-mechanics, phase-space]", "---", "",
             "# Practice: Hamiltonian Mechanics (4.5)", ""]
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

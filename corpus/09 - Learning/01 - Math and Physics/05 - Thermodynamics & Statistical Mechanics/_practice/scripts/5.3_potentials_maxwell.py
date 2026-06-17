#!/usr/bin/env python3
"""
5.3_potentials_maxwell.py — Practice problem generator for Chapter 5.3
(Thermodynamic Potentials & Maxwell Relations).

Archetypes:
  1. Maxwell relation identification and application
  2. Derive equation of state from a given potential
  3. Compute (∂U/∂V)_T using energy equation
  4. Gibbs-Helmholtz equation application
  5. Cp - Cv computation for non-ideal gas
  6. Legendre transform construction
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sympy as sp

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx):
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

T, P, V, S, n, R = sp.symbols('T P V S n R', positive=True)

def gen_maxwell_id(rng: random.Random) -> Problem:
    choices = [
        ("U", "dU = TdS - PdV", "(∂T/∂V)_S = -(∂P/∂S)_V"),
        ("H", "dH = TdS + VdP", "(∂T/∂P)_S = (∂V/∂S)_P"),
        ("F", "dF = -SdT - PdV", "(∂S/∂V)_T = (∂P/∂T)_V"),
        ("G", "dG = -SdT + VdP", "-(∂S/∂P)_T = (∂V/∂T)_P"),
    ]
    pot, diff, maxwell = rng.choice(choices)
    stmt = (f"Starting from ${diff}$, derive the corresponding Maxwell relation by applying "
            f"Clairaut's theorem to the potential ${pot}$.")
    sol = (f"From ${diff}$, identify the coefficients of the two differentials.\n\n"
           f"Apply $\\partial^2 {pot}/\\partial x\\partial y = \\partial^2 {pot}/\\partial y\\partial x$.\n\n"
           f"**Result:** ${maxwell}$. $\\blacksquare$")
    return Problem("Maxwell relation derivation", stmt, sol)

def gen_eos_from_potential(rng: random.Random) -> Problem:
    a, b = sp.symbols('a b', positive=True)
    # F = nRT[ln(V-nb) + a/(RTV)] type potentials
    case = rng.choice(["ideal", "vdw"])
    if case == "ideal":
        F_expr = -n*R*T*sp.ln(V) + n*R*T*(sp.ln(n*R*T) - 1)
        P_derived = sp.simplify(-sp.diff(F_expr, V))
        stmt = f"Given $F = -nRT\\ln V + nRT(\\ln(nRT) - 1)$, derive the equation of state $P(T,V)$."
        sol = (f"$P = -(\\partial F/\\partial V)_T = nRT/V$.\n\n"
               f"This is the ideal gas law: $PV = nRT$. ✓")
    else:
        F_expr = -n*R*T*sp.ln(V - n*b) - a*n**2/V
        P_derived = sp.simplify(-sp.diff(F_expr, V))
        stmt = f"Given $F = -nRT\\ln(V - nb) - an^2/V$, derive $P(T,V)$."
        sol = (f"$P = -(\\partial F/\\partial V)_T = \\frac{{nRT}}{{V-nb}} - \\frac{{an^2}}{{V^2}}$.\n\n"
               f"This is the van der Waals equation. ✓")
    return Problem("EOS from potential", stmt, sol)

def gen_energy_eq(rng: random.Random) -> Problem:
    case = rng.choice(["ideal", "vdw", "photon"])
    if case == "ideal":
        stmt = "Using the energy equation $(\\partial U/\\partial V)_T = T(\\partial P/\\partial T)_V - P$, show that $U$ of an ideal gas is independent of $V$."
        sol = ("For ideal gas: $P = nRT/V$, so $(\\partial P/\\partial T)_V = nR/V = P/T$.\n\n"
               "$(\\partial U/\\partial V)_T = T(P/T) - P = P - P = 0$. ✓")
    elif case == "vdw":
        stmt = "For a van der Waals gas $P = nRT/(V-nb) - an^2/V^2$, find $(\\partial U/\\partial V)_T$."
        sol = ("$(\\partial P/\\partial T)_V = nR/(V-nb)$.\n\n"
               "$(\\partial U/\\partial V)_T = T \\cdot nR/(V-nb) - [nRT/(V-nb) - an^2/V^2] = an^2/V^2$.")
    else:
        stmt = "For a photon gas with $P = U/(3V)$, use the energy equation to derive $U \\propto T^4$."
        sol = ("Let $u = U/V$. Then $P = u/3$ and $(\\partial P/\\partial T)_V = (1/3)(du/dT)$.\n\n"
               "Energy eq: $u = T(1/3)(du/dT) - u/3 \\Rightarrow 4u/3 = (T/3)(du/dT)$.\n\n"
               "$du/u = 4dT/T \\Rightarrow u = aT^4$ (Stefan-Boltzmann). $\\blacksquare$")
    return Problem("Energy equation application", stmt, sol)

def gen_gibbs_helmholtz(rng: random.Random) -> Problem:
    H_val = rng.choice([-50, -100, -200, 100, 200])
    T_val = rng.choice([300, 400, 500])
    stmt = (f"A reaction has $\\Delta H = {H_val}\\,\\text{{kJ/mol}}$ at $T = {T_val}\\,\\text{{K}}$. "
            f"Using the Gibbs-Helmholtz equation, find $\\partial(\\Delta G/T)/\\partial T$ at constant $P$.")
    result = -H_val*1000/T_val**2
    sol = (f"Gibbs-Helmholtz: $[\\partial(\\Delta G/T)/\\partial T]_P = -\\Delta H/T^2$.\n\n"
           f"$= -{H_val}\\times10^3/{T_val}^2 = {result:.2f}\\,\\text{{J/(mol·K}}^2\\text{{)}}$.")
    return Problem("Gibbs-Helmholtz equation", stmt, sol)

def gen_cp_cv(rng: random.Random) -> Problem:
    alpha_val = rng.choice([1.0e-4, 2.1e-4, 3.0e-4, 1.2e-3])
    kT_val = rng.choice([4.5e-10, 1.0e-10, 5.0e-11])
    V_val = rng.choice([18e-6, 25e-6, 50e-6])  # m^3/mol
    T_val = rng.choice([300, 400, 500])
    diff = T_val * V_val * alpha_val**2 / kT_val
    stmt = (f"A substance has $\\alpha = {alpha_val:.1e}\\,\\text{{K}}^{{-1}}$, "
            f"$\\kappa_T = {kT_val:.1e}\\,\\text{{Pa}}^{{-1}}$, "
            f"$V_m = {V_val*1e6:.0f}\\,\\text{{cm}}^3/\\text{{mol}}$, $T = {T_val}\\,\\text{{K}}$. "
            f"Find $C_P - C_V$ per mole.")
    sol = (f"$C_P - C_V = TV\\alpha^2/\\kappa_T = {T_val} \\times {V_val:.2e} \\times ({alpha_val:.1e})^2 / ({kT_val:.1e})$\n\n"
           f"$= {diff:.2f}\\,\\text{{J/(mol·K)}}$.")
    return Problem("Cp - Cv relation", stmt, sol)

def gen_legendre(rng: random.Random) -> Problem:
    stmt = ("Starting from $U(S,V)$ with $dU = TdS - PdV$, construct the Legendre transform "
            "that replaces $S$ with $T$ as independent variable. Name the resulting potential and verify its differential.")
    sol = ("Replace $S$ by its conjugate $T = (\\partial U/\\partial S)_V$:\n\n"
           "$F = U - TS$ (Helmholtz free energy).\n\n"
           "$dF = dU - TdS - SdT = (TdS - PdV) - TdS - SdT = -SdT - PdV$.\n\n"
           "Natural variables: $(T, V)$. $\\blacksquare$")
    return Problem("Legendre transform", stmt, sol)

ARCHETYPES = [gen_maxwell_id, gen_eos_from_potential, gen_energy_eq, gen_gibbs_helmholtz, gen_cp_cv, gen_legendre]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.3_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [thermodynamics, potentials, maxwell-relations, practice, \"#review/math\"]\nchapter: 5.3\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.3 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

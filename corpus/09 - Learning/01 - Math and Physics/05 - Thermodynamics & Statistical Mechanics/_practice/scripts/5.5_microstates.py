#!/usr/bin/env python3
"""
5.5_microstates.py — Practice problem generator for Chapter 5.5
(Classical Statistical Mechanics - Microstates & Ensembles).

Archetypes:
  1. Multiplicity of two-state system (binomial)
  2. Stirling approximation computation
  3. Statistical temperature from Ω(E)
  4. Entropy of ideal gas (Sackur-Tetrode)
  5. Thermal equilibrium condition
"""
from __future__ import annotations
import argparse, random, math
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

kB = 1.381e-23

def gen_multiplicity(rng: random.Random) -> Problem:
    N = rng.choice([20, 50, 100])
    n_up = rng.randint(N//4, 3*N//4)
    # Use Stirling for ln(Omega)
    lnO = N*math.log(N) - n_up*math.log(n_up) - (N-n_up)*math.log(N-n_up)
    S = kB * lnO
    stmt = (f"A system of $N = {N}$ two-state particles has ${n_up}$ in state 'up' and ${N-n_up}$ in state 'down'. "
            f"Compute $\\ln\\Omega$ using Stirling's approximation and find $S$.")
    sol = (f"$\\Omega = \\binom{{{N}}}{{{n_up}}}$. Using Stirling ($\\ln n! \\approx n\\ln n - n$):\n\n"
           f"$\\ln\\Omega \\approx {N}\\ln{N} - {n_up}\\ln{n_up} - {N-n_up}\\ln{N-n_up}$\n\n"
           f"$= {N*math.log(N):.2f} - {n_up*math.log(n_up):.2f} - {(N-n_up)*math.log(N-n_up):.2f} = {lnO:.2f}$\n\n"
           f"$S = k_B\\ln\\Omega = {kB:.3e} \\times {lnO:.2f} = {S:.3e}\\,\\text{{J/K}}$.")
    return Problem("Multiplicity (Stirling)", stmt, sol)

def gen_stirling(rng: random.Random) -> Problem:
    N = rng.choice([10, 50, 100, 1000])
    exact = sum(math.log(k) for k in range(1, N+1))
    approx1 = N*math.log(N) - N
    approx2 = N*math.log(N) - N + 0.5*math.log(2*math.pi*N)
    stmt = f"Compute $\\ln({N}!)$ exactly and compare with both forms of Stirling's approximation."
    sol = (f"Exact: $\\ln({N}!) = {exact:.4f}$.\n\n"
           f"Stirling (basic): $N\\ln N - N = {approx1:.4f}$ (error: {abs(exact-approx1)/exact*100:.2f}%).\n\n"
           f"Stirling (full): $N\\ln N - N + \\frac{{1}}{{2}}\\ln(2\\pi N) = {approx2:.4f}$ (error: {abs(exact-approx2)/exact*100:.4f}%).")
    return Problem("Stirling's approximation", stmt, sol)

def gen_stat_temp(rng: random.Random) -> Problem:
    N = 100
    eps = rng.choice([0.01, 0.05, 0.1])  # eV
    n_up = rng.randint(55, 80)
    n_dn = N - n_up
    # 1/T = (kB/(2*eps)) * ln(n_dn/n_up) ... for two-state
    # Actually: 1/T = -(kB/(2eps))*ln(n_dn/n_up) when E = -(2n_up - N)*eps
    beta_inv = 2*eps*1.602e-19 / (kB * math.log(n_up/n_dn))
    stmt = (f"$N = {N}$ spins with energy $\\pm\\epsilon$ ($\\epsilon = {eps}\\,\\text{{eV}}$). "
            f"If ${n_up}$ are in the lower state, find the temperature.")
    sol = (f"$1/T = (k_B/(2\\epsilon))\\ln(n_\\uparrow/n_\\downarrow) = "
           f"({kB:.3e}/(2\\times{eps}\\times1.602\\times10^{{-19}}))\\ln({n_up}/{n_dn})$\n\n"
           f"$= {kB/(2*eps*1.602e-19):.4e} \\times {math.log(n_up/n_dn):.4f}$\n\n"
           f"$T = {beta_inv:.0f}\\,\\text{{K}}$.")
    return Problem("Statistical temperature", stmt, sol)

def gen_sackur_tetrode(rng: random.Random) -> Problem:
    N = rng.choice([1e23, 6.022e23])
    m = rng.choice([6.64e-27, 4.65e-26, 3.35e-26])  # He, N2, Ne
    T = rng.choice([300, 500])
    V = rng.choice([0.001, 0.01, 0.0224])
    h = 6.626e-34
    lam = h/math.sqrt(2*math.pi*m*kB*T)
    S_per_particle = kB*(math.log(V/(N*lam**3)) + 5/2)
    S_total = N * S_per_particle
    stmt = (f"Compute the entropy of $N = {N:.2e}$ atoms (mass $m = {m:.2e}\\,\\text{{kg}}$) "
            f"in volume $V = {V}\\,\\text{{m}}^3$ at $T = {T}\\,\\text{{K}}$ using Sackur-Tetrode.")
    sol = (f"$\\lambda = h/\\sqrt{{2\\pi mk_BT}} = {lam:.3e}\\,\\text{{m}}$.\n\n"
           f"$S/N = k_B[\\ln(V/(N\\lambda^3)) + 5/2] = {kB:.3e}[\\ln({V/(N*lam**3):.2e}) + 2.5]$\n\n"
           f"$= {kB:.3e} \\times {math.log(V/(N*lam**3))+2.5:.2f} = {S_per_particle:.3e}\\,\\text{{J/K per particle}}$\n\n"
           f"$S_{{\\text{{total}}}} = {S_total:.2f}\\,\\text{{J/K}}$.")
    return Problem("Sackur-Tetrode entropy", stmt, sol)

def gen_equilibrium(rng: random.Random) -> Problem:
    EA = rng.choice([100, 200, 500])
    EB = rng.choice([300, 400, 600])
    E = EA + EB
    # Simple model: S = c*sqrt(E) for each
    cA = rng.choice([1.0, 2.0])
    cB = rng.choice([1.0, 1.5, 2.0])
    # At equilibrium: dSA/dEA = dSB/dEB => cA/(2*sqrt(EA_eq)) = cB/(2*sqrt(EB_eq))
    # cA^2 * EB_eq = cB^2 * EA_eq, EA_eq + EB_eq = E
    EA_eq = E * cA**2 / (cA**2 + cB**2)
    EB_eq = E - EA_eq
    stmt = (f"Two systems with $S_A = {cA}\\sqrt{{E_A}}$ and $S_B = {cB}\\sqrt{{E_B}}$ share total energy $E = {E}$. "
            f"Find the equilibrium energy partition.")
    sol = (f"At equilibrium: $\\partial S_A/\\partial E_A = \\partial S_B/\\partial E_B$.\n\n"
           f"${cA}/(2\\sqrt{{E_A}}) = {cB}/(2\\sqrt{{E_B}})$ → ${cA}^2 E_B = {cB}^2 E_A$.\n\n"
           f"With $E_A + E_B = {E}$: $E_A = {E} \\times {cA}^2/({cA}^2+{cB}^2) = {EA_eq:.1f}$, $E_B = {EB_eq:.1f}$.")
    return Problem("Thermal equilibrium", stmt, sol)

ARCHETYPES = [gen_multiplicity, gen_stirling, gen_stat_temp, gen_sackur_tetrode, gen_equilibrium]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.5_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [statistical-mechanics, microstates, ensembles, practice, \"#review/math\"]\nchapter: 5.5\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.5 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
5.8_quantum_statistics.py — Practice problem generator for Chapter 5.8
(Quantum Statistics - Bose-Einstein & Fermi-Dirac).

Archetypes:
  1. Fermi energy computation for a metal
  2. Planck distribution / Wien's law
  3. Stefan-Boltzmann total power
  4. BEC critical temperature
  5. Electronic heat capacity (Sommerfeld)
  6. Debye T^3 law
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Problem:
    archetype: str; statement_md: str; solution_md: str
    def render(self, idx):
        return (f"### Problem {idx} — {self.archetype}\n\n{self.statement_md}\n\n"
                "<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

kB = 1.381e-23; hbar = 1.055e-34; me = 9.109e-31; h = 6.626e-34; c = 3e8

def gen_fermi_energy(rng: random.Random) -> Problem:
    metals = {"Cu":(8.49e28,1),"Al":(18.1e28,3),"Na":(2.65e28,1),"Ag":(5.86e28,1)}
    name, (n, z) = rng.choice(list(metals.items()))
    eF = (hbar**2/(2*me))*(3*math.pi**2*n)**(2/3)
    TF = eF/kB
    stmt = f"Compute the Fermi energy and Fermi temperature for {name} (conduction electron density $n = {n:.2e}\\,\\text{{m}}^{{-3}}$)."
    sol = (f"$\\epsilon_F = (\\hbar^2/2m_e)(3\\pi^2 n)^{{2/3}} = ({hbar:.3e})^2/(2\\times{me:.3e}) \\times (3\\pi^2\\times{n:.2e})^{{2/3}}$\n\n"
           f"$= {eF:.3e}\\,\\text{{J}} = {eF/1.602e-19:.2f}\\,\\text{{eV}}$.\n\n"
           f"$T_F = \\epsilon_F/k_B = {TF:.0f}\\,\\text{{K}}$.")
    return Problem("Fermi energy", stmt, sol)

def gen_wien(rng: random.Random) -> Problem:
    T = rng.choice([3000, 5000, 5778, 6000, 10000])
    lam_max = 2.898e-3/T
    stmt = f"Find the peak wavelength of blackbody radiation at $T = {T}\\,\\text{{K}}$ (Wien's law)."
    sol = (f"$\\lambda_{{\\max}} = 2.898\\times10^{{-3}}/T = 2.898\\times10^{{-3}}/{T} = {lam_max:.3e}\\,\\text{{m}}$\n\n"
           f"$= {lam_max*1e9:.0f}\\,\\text{{nm}}$"
           + (f" (visible {'red' if lam_max > 600e-9 else 'green' if lam_max > 500e-9 else 'blue/UV'})." if 380e-9 < lam_max < 780e-9 else " (infrared)." if lam_max > 780e-9 else " (ultraviolet)."))
    return Problem("Wien's displacement law", stmt, sol)

def gen_stefan_boltzmann(rng: random.Random) -> Problem:
    T = rng.choice([300, 1000, 3000, 5778])
    sigma = 5.67e-8
    A = rng.choice([1, 0.01, 4*math.pi*(6.96e8)**2])  # 1m^2, 1cm^2, or Sun
    P = sigma*T**4*A
    desc = "1 m²" if A == 1 else ("1 cm²" if A == 0.01 else "the Sun (R=6.96×10⁸ m)")
    stmt = f"Compute the total radiated power from a blackbody at $T = {T}\\,\\text{{K}}$ with surface area of {desc}."
    sol = (f"$P = \\sigma T^4 A = (5.67\\times10^{{-8}})({T})^4({A:.3e})$\n\n"
           f"$= {sigma*T**4:.3e} \\times {A:.3e} = {P:.3e}\\,\\text{{W}}$.")
    return Problem("Stefan-Boltzmann power", stmt, sol)

def gen_bec(rng: random.Random) -> Problem:
    atoms = {"⁸⁷Rb":(87*1.66e-27, 2.5e18),"²³Na":(23*1.66e-27, 1.5e19),"⁷Li":(7*1.66e-27, 1e18)}
    name, (m, n) = rng.choice(list(atoms.items()))
    zeta32 = 2.612
    Tc = (2*math.pi*hbar**2/(m*kB))*(n/zeta32)**(2/3)
    stmt = f"Compute the BEC critical temperature for {name} atoms at density $n = {n:.2e}\\,\\text{{m}}^{{-3}}$."
    sol = (f"$T_c = (2\\pi\\hbar^2/(mk_B))(n/\\zeta(3/2))^{{2/3}}$\n\n"
           f"$= (2\\pi({hbar:.3e})^2/({m:.2e}\\times{kB:.3e}))({n:.2e}/{zeta32})^{{2/3}}$\n\n"
           f"$= {2*math.pi*hbar**2/(m*kB):.3e} \\times {(n/zeta32)**(2/3):.3e} = {Tc:.2e}\\,\\text{{K}} = {Tc*1e9:.0f}\\,\\text{{nK}}$.")
    return Problem("BEC critical temperature", stmt, sol)

def gen_sommerfeld(rng: random.Random) -> Problem:
    TF = rng.choice([50000, 80000, 100000])
    T = rng.choice([100, 200, 300])
    N = 6.022e23
    Cv = (math.pi**2/2)*N*kB*T/TF
    stmt = (f"Metal with $T_F = {TF}\\,\\text{{K}}$. Find the electronic heat capacity per mole at $T = {T}\\,\\text{{K}}$.")
    sol = (f"$C_V^{{\\text{{el}}}} = (\\pi^2/2)(N_Ak_B)(T/T_F) = (\\pi^2/2)({N:.3e})({kB:.3e})({T}/{TF})$\n\n"
           f"$= {Cv:.3f}\\,\\text{{J/(mol·K)}}$.\n\n"
           f"Compare classical: $3R/2 = {1.5*8.314:.1f}\\,\\text{{J/(mol·K)}}$. "
           f"Ratio: {Cv/(1.5*8.314):.4f} — quantum suppression by factor $T/T_F = {T/TF:.5f}$.")
    return Problem("Electronic heat capacity", stmt, sol)

def gen_debye(rng: random.Random) -> Problem:
    theta_D = rng.choice([215, 343, 428, 470, 630])  # Ag, Cu, Fe, Al, C
    T = rng.choice([10, 20, 50])
    N = 6.022e23
    Cv = (12*math.pi**4/5)*N*kB*(T/theta_D)**3
    stmt = (f"Debye solid ($\\Theta_D = {theta_D}\\,\\text{{K}}$) at $T = {T}\\,\\text{{K}}$. "
            f"Compute $C_V$ per mole using the $T^3$ law.")
    sol = (f"$C_V = (12\\pi^4/5)Nk_B(T/\\Theta_D)^3 = (12\\pi^4/5)({N:.3e})({kB:.3e})({T}/{theta_D})^3$\n\n"
           f"$= {12*math.pi**4/5*N*kB:.3f} \\times ({T/theta_D:.5f})^3 = {Cv:.4f}\\,\\text{{J/(mol·K)}}$.\n\n"
           f"Compare Dulong-Petit: $3R = {3*8.314:.1f}\\,\\text{{J/(mol·K)}}$. Ratio: {Cv/(3*8.314):.5f}.")
    return Problem("Debye T³ law", stmt, sol)

ARCHETYPES = [gen_fermi_energy, gen_wien, gen_stefan_boltzmann, gen_bec, gen_sommerfeld, gen_debye]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.8_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [quantum-statistics, bose-einstein, fermi-dirac, practice, \"#review/math\"]\nchapter: 5.8\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.8 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

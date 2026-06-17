#!/usr/bin/env python3
"""
5.6_partition_function.py — Practice problem generator for Chapter 5.6
(The Partition Function & Free Energy).

Archetypes:
  1. Two-state system Z, <E>, Cv
  2. Harmonic oscillator Z and <E>
  3. Ideal gas Z and pressure derivation
  4. Equipartition theorem application
  5. Energy fluctuations from Z
  6. Einstein solid heat capacity
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

def gen_two_state(rng: random.Random) -> Problem:
    eps_eV = rng.choice([0.01, 0.02, 0.05, 0.1])
    eps = eps_eV * 1.602e-19
    T = rng.choice([100, 200, 300, 500, 1000])
    beta_eps = eps/(kB*T)
    Z = 1 + math.exp(-beta_eps)
    E_avg = eps/(math.exp(beta_eps)+1)
    stmt = (f"A two-state system has levels $0$ and $\\epsilon = {eps_eV}\\,\\text{{eV}}$ at $T = {T}\\,\\text{{K}}$. "
            f"Compute $Z$, $\\langle E\\rangle$, and the occupation probability of the excited state.")
    P_exc = math.exp(-beta_eps)/Z
    sol = (f"$\\beta\\epsilon = {eps_eV}\\times1.602\\times10^{{-19}}/({kB:.3e}\\times{T}) = {beta_eps:.4f}$.\n\n"
           f"$Z = 1 + e^{{-\\beta\\epsilon}} = 1 + e^{{-{beta_eps:.4f}}} = 1 + {math.exp(-beta_eps):.6f} = {Z:.6f}$.\n\n"
           f"$\\langle E\\rangle = \\epsilon/(e^{{\\beta\\epsilon}}+1) = {eps:.3e}/({math.exp(beta_eps):.4f}+1) = {E_avg:.3e}\\,\\text{{J}} = {E_avg/1.602e-19:.4f}\\,\\text{{eV}}$.\n\n"
           f"$P_{{\\text{{exc}}}} = e^{{-\\beta\\epsilon}}/Z = {P_exc:.4f}$.")
    return Problem("Two-state partition function", stmt, sol)

def gen_harmonic(rng: random.Random) -> Problem:
    hw_eV = rng.choice([0.01, 0.02, 0.05, 0.1, 0.2])
    T = rng.choice([100, 300, 500, 1000, 3000])
    hw = hw_eV * 1.602e-19
    x = hw/(kB*T)
    Z = 1/(2*math.sinh(x/2))
    E_avg = hw*(0.5 + 1/(math.exp(x)-1))
    stmt = (f"Quantum harmonic oscillator with $\\hbar\\omega = {hw_eV}\\,\\text{{eV}}$ at $T = {T}\\,\\text{{K}}$. "
            f"Find $Z$ and $\\langle E\\rangle$.")
    sol = (f"$x = \\hbar\\omega/(k_BT) = {x:.4f}$.\n\n"
           f"$Z = 1/(2\\sinh(x/2)) = 1/(2\\sinh({x/2:.4f})) = {Z:.4f}$.\n\n"
           f"$\\langle E\\rangle = \\hbar\\omega(1/2 + 1/(e^x-1)) = {hw:.3e}(0.5 + {1/(math.exp(x)-1):.4f}) = {E_avg:.3e}\\,\\text{{J}}$.\n\n"
           f"High-T check: if $x \\ll 1$, $\\langle E\\rangle \\approx k_BT = {kB*T:.3e}\\,\\text{{J}}$.")
    return Problem("Harmonic oscillator Z", stmt, sol)

def gen_ideal_gas_Z(rng: random.Random) -> Problem:
    m_amu = rng.choice([4, 28, 32, 40])
    m = m_amu * 1.66e-27
    T = rng.choice([300, 500, 1000])
    V = rng.choice([0.001, 0.01, 0.0224])
    N = rng.choice([100, 1000])
    h = 6.626e-34
    lam = h/math.sqrt(2*math.pi*m*kB*T)
    Z1 = V/lam**3
    stmt = (f"Compute the single-particle translational partition function for a gas "
            f"(mass ${m_amu}\\,\\text{{amu}}$) in volume $V = {V*1000:.1f}\\,\\text{{L}}$ at $T = {T}\\,\\text{{K}}$.")
    sol = (f"$\\lambda = h/\\sqrt{{2\\pi mk_BT}} = {h:.3e}/\\sqrt{{2\\pi({m:.2e})({kB:.3e})({T})}} = {lam:.3e}\\,\\text{{m}}$.\n\n"
           f"$Z_1 = V/\\lambda^3 = {V:.4f}/({lam:.3e})^3 = {Z1:.3e}$.\n\n"
           f"Since $Z_1 \\gg 1$, the classical approximation is valid.")
    return Problem("Ideal gas Z₁", stmt, sol)

def gen_equipartition(rng: random.Random) -> Problem:
    dof = rng.choice([3, 5, 6, 7])
    desc = {3:"monatomic gas (3 translational)",5:"diatomic gas (3 trans + 2 rot)",
            6:"solid (3 KE + 3 PE)",7:"diatomic with vibration (3+2+2)"}[dof]
    T = rng.choice([300, 500, 1000])
    N = rng.choice([1, 6.022e23])
    E = 0.5*dof*kB*T*N
    Cv = 0.5*dof*kB*N
    stmt = (f"Apply equipartition to a {desc} system with $N = {N:.3g}$ particles at $T = {T}\\,\\text{{K}}$. "
            f"Find $\\langle E\\rangle$ and $C_V$.")
    sol = (f"Degrees of freedom: $f = {dof}$.\n\n"
           f"$\\langle E\\rangle = (f/2)Nk_BT = ({dof}/2)({N:.3g})({kB:.3e})({T}) = {E:.3e}\\,\\text{{J}}$.\n\n"
           f"$C_V = (f/2)Nk_B = {Cv:.3e}\\,\\text{{J/K}}$"
           + (f" $= {Cv/8.314:.1f}R$ per mole." if N > 1e20 else "."))
    return Problem("Equipartition theorem", stmt, sol)

def gen_fluctuations(rng: random.Random) -> Problem:
    N = rng.choice([100, 1000, 10000, int(6.022e23)])
    T = rng.choice([300, 500])
    Cv = 1.5*N*kB  # monatomic
    var_E = kB*T**2*Cv
    rel = math.sqrt(var_E)/(1.5*N*kB*T)
    stmt = (f"For $N = {N:.3g}$ monatomic ideal gas particles at $T = {T}\\,\\text{{K}}$, "
            f"compute the relative energy fluctuation $\\sqrt{{\\langle(\\Delta E)^2\\rangle}}/\\langle E\\rangle$.")
    sol = (f"$\\langle(\\Delta E)^2\\rangle = k_BT^2 C_V = {kB:.3e}\\times{T}^2\\times(3/2)({N:.3g})({kB:.3e}) = {var_E:.3e}\\,\\text{{J}}^2$.\n\n"
           f"$\\sqrt{{\\langle(\\Delta E)^2\\rangle}}/\\langle E\\rangle = \\sqrt{{2/(3N)}} = {rel:.3e}$.\n\n"
           + (f"For macroscopic $N$, fluctuations are negligible ($\\sim 10^{{-12}}$)." if N > 1e20 else
              f"For small $N$, fluctuations are significant ({rel*100:.1f}%)."))
    return Problem("Energy fluctuations", stmt, sol)

def gen_einstein_solid(rng: random.Random) -> Problem:
    theta_E = rng.choice([200, 300, 500, 1000])
    T = rng.choice([50, 100, 200, 500, 1000])
    x = theta_E/T
    Cv_over_3NkB = x**2 * math.exp(x)/(math.exp(x)-1)**2
    stmt = (f"Einstein solid with $\\Theta_E = {theta_E}\\,\\text{{K}}$ at $T = {T}\\,\\text{{K}}$. "
            f"Compute $C_V/(3Nk_B)$.")
    sol = (f"$x = \\Theta_E/T = {theta_E}/{T} = {x:.3f}$.\n\n"
           f"$C_V/(3Nk_B) = x^2 e^x/(e^x-1)^2 = {x:.3f}^2 \\times {math.exp(x):.4f}/({math.exp(x)-1:.4f})^2 = {Cv_over_3NkB:.4f}$.\n\n"
           + (f"High-T limit ($x\\ll1$): $C_V \\to 3Nk_B$ (Dulong-Petit). Here ratio = {Cv_over_3NkB:.2f}." if x < 1 else
              f"Low-T regime ($x\\gg1$): $C_V$ exponentially suppressed."))
    return Problem("Einstein solid Cv", stmt, sol)

ARCHETYPES = [gen_two_state, gen_harmonic, gen_ideal_gas_Z, gen_equipartition, gen_fluctuations, gen_einstein_solid]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.6_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [statistical-mechanics, partition-function, practice, \"#review/math\"]\nchapter: 5.6\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.6 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
5.7_maxwell_boltzmann.py — Practice problem generator for Chapter 5.7
(Maxwell-Boltzmann Distribution & Kinetic Theory).

Archetypes:
  1. Characteristic speeds (v_p, <v>, v_rms)
  2. Mean free path computation
  3. Effusion rate
  4. Pressure from kinetic theory
  5. Fraction of molecules above speed v
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

kB = 1.381e-23

def gen_speeds(rng: random.Random) -> Problem:
    gases = {"He":(4,6.64e-27),"Ne":(20,3.32e-26),"N2":(28,4.65e-26),"O2":(32,5.31e-26),"Ar":(40,6.64e-26)}
    name, (amu, m) = rng.choice(list(gases.items()))
    T = rng.choice([200, 300, 400, 500, 1000])
    vp = math.sqrt(2*kB*T/m)
    vmean = math.sqrt(8*kB*T/(math.pi*m))
    vrms = math.sqrt(3*kB*T/m)
    stmt = f"Compute $v_p$, $\\langle v\\rangle$, and $v_{{\\text{{rms}}}}$ for {name} ($m = {amu}\\,\\text{{amu}}$) at $T = {T}\\,\\text{{K}}$."
    sol = (f"$v_p = \\sqrt{{2k_BT/m}} = \\sqrt{{2({kB:.3e})({T})/({m:.2e})}} = {vp:.1f}\\,\\text{{m/s}}$.\n\n"
           f"$\\langle v\\rangle = \\sqrt{{8k_BT/(\\pi m)}} = {vmean:.1f}\\,\\text{{m/s}}$.\n\n"
           f"$v_{{\\text{{rms}}}} = \\sqrt{{3k_BT/m}} = {vrms:.1f}\\,\\text{{m/s}}$.\n\n"
           f"Ratio check: $v_p : \\langle v\\rangle : v_{{\\text{{rms}}}} = 1 : {vmean/vp:.3f} : {vrms/vp:.3f}$ "
           f"(theory: $1 : 1.128 : 1.225$). ✓")
    return Problem("Characteristic speeds", stmt, sol)

def gen_mfp(rng: random.Random) -> Problem:
    T = rng.choice([273, 300, 500])
    P = rng.choice([101325, 10000, 1000, 100])
    d = rng.choice([3.0e-10, 3.7e-10, 4.0e-10])
    n = P/(kB*T)
    sigma = math.pi*d**2
    ell = 1/(math.sqrt(2)*n*sigma)
    stmt = (f"Gas at $T = {T}\\,\\text{{K}}$, $P = {P}\\,\\text{{Pa}}$, molecular diameter $d = {d*1e10:.1f}\\,\\text{{Å}}$. "
            f"Find the mean free path.")
    sol = (f"$n = P/(k_BT) = {P}/({kB:.3e}\\times{T}) = {n:.3e}\\,\\text{{m}}^{{-3}}$.\n\n"
           f"$\\sigma = \\pi d^2 = {sigma:.3e}\\,\\text{{m}}^2$.\n\n"
           f"$\\ell = 1/(\\sqrt{{2}}\\,n\\sigma) = 1/({math.sqrt(2):.3f}\\times{n:.3e}\\times{sigma:.3e}) = {ell:.3e}\\,\\text{{m}}$"
           + (f" $= {ell*1e9:.1f}\\,\\text{{nm}}$." if ell < 1e-6 else f" $= {ell*1e3:.2f}\\,\\text{{mm}}$."))
    return Problem("Mean free path", stmt, sol)

def gen_effusion(rng: random.Random) -> Problem:
    m_amu = rng.choice([4, 28, 32])
    m = m_amu * 1.66e-27
    T = rng.choice([300, 500, 1000])
    P = rng.choice([1, 10, 100])
    A = rng.choice([1e-6, 1e-8, 1e-4])
    n = P/(kB*T)
    vmean = math.sqrt(8*kB*T/(math.pi*m))
    Phi = 0.25*n*vmean*A
    stmt = (f"Gas ($m = {m_amu}\\,\\text{{amu}}$) at $T = {T}\\,\\text{{K}}$, $P = {P}\\,\\text{{Pa}}$ "
            f"effuses through hole of area $A = {A:.1e}\\,\\text{{m}}^2$. Find the effusion rate.")
    sol = (f"$n = {n:.3e}\\,\\text{{m}}^{{-3}}$, $\\langle v\\rangle = {vmean:.1f}\\,\\text{{m/s}}$.\n\n"
           f"$\\Phi = (1/4)n\\langle v\\rangle A = 0.25\\times{n:.3e}\\times{vmean:.1f}\\times{A:.1e} = {Phi:.3e}\\,\\text{{particles/s}}$.")
    return Problem("Effusion rate", stmt, sol)

def gen_pressure_kinetic(rng: random.Random) -> Problem:
    n = rng.choice([1e25, 2.5e25, 5e25])
    m = rng.choice([4.65e-26, 5.31e-26, 6.64e-27])
    vrms = rng.choice([400, 500, 600, 1000])
    P = n*m*vrms**2/3
    T = m*vrms**2/(3*kB)
    stmt = (f"A gas has number density $n = {n:.2e}\\,\\text{{m}}^{{-3}}$, molecular mass $m = {m:.2e}\\,\\text{{kg}}$, "
            f"and $v_{{\\text{{rms}}}} = {vrms}\\,\\text{{m/s}}$. Find $P$ and $T$.")
    sol = (f"$P = (1/3)nm v_{{\\text{{rms}}}}^2 = (1/3)({n:.2e})({m:.2e})({vrms})^2 = {P:.0f}\\,\\text{{Pa}}$.\n\n"
           f"$T = mv_{{\\text{{rms}}}}^2/(3k_B) = {m:.2e}\\times{vrms}^2/(3\\times{kB:.3e}) = {T:.0f}\\,\\text{{K}}$.")
    return Problem("Kinetic theory pressure", stmt, sol)

def gen_fraction_above(rng: random.Random) -> Problem:
    # Fraction above v = alpha*v_p uses incomplete gamma
    alpha = rng.choice([1.5, 2.0, 2.5, 3.0])
    # Approximate: for large alpha, fraction ~ (4/sqrt(pi))*alpha^2*exp(-alpha^2)
    frac_approx = (4/math.sqrt(math.pi))*alpha**2*math.exp(-alpha**2)
    stmt = (f"Estimate the fraction of molecules with speed $v > {alpha}v_p$ using the "
            f"high-speed tail approximation $f(v > \\alpha v_p) \\approx (4/\\sqrt{{\\pi}})\\alpha^2 e^{{-\\alpha^2}}$.")
    sol = (f"$f(v > {alpha}v_p) \\approx (4/\\sqrt{{\\pi}})({alpha})^2 e^{{-{alpha}^2}} "
           f"= {4/math.sqrt(math.pi):.3f}\\times{alpha**2:.2f}\\times e^{{-{alpha**2:.2f}}}$\n\n"
           f"$= {4/math.sqrt(math.pi)*alpha**2:.3f}\\times{math.exp(-alpha**2):.6f} = {frac_approx:.6f}$ "
           f"({frac_approx*100:.4f}% of molecules).")
    return Problem("Fraction above speed", stmt, sol)

ARCHETYPES = [gen_speeds, gen_mfp, gen_effusion, gen_pressure_kinetic, gen_fraction_above]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.7_drills.md")
    problems = []
    while len(problems) < args.count:
        for gen in ARCHETYPES:
            if len(problems) >= args.count: break
            problems.append(gen(rng))
    hdr = f"---\ntags: [maxwell-boltzmann, kinetic-theory, practice, \"#review/math\"]\nchapter: 5.7\ntype: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n# Chapter 5.7 — Practice Drills\n\n---\n\n"
    out = [hdr] + [p.render(i)+"\n---\n\n" for i,p in enumerate(problems,1)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

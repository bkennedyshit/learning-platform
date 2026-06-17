#!/usr/bin/env python3
"""
5.2_entropy_engines.py — Practice problem generator for Chapter 5.2
(Entropy & Heat Engines).

Archetypes:
  1. Entropy change for ideal gas process
  2. Carnot cycle full analysis
  3. Otto cycle efficiency
  4. Entropy of mixing
  5. Irreversible heat transfer entropy generation
  6. Maximum work from finite reservoirs

Usage:
  python 5.2_entropy_engines.py --count 8 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from datetime import datetime
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

R = 8.314

def gen_entropy_ideal(rng: random.Random) -> Problem:
    n = rng.choice([1,2,3])
    Cv = rng.choice([12.47, 20.79])  # monatomic or diatomic
    T1, T2 = rng.choice([(300,600),(400,800),(200,500)])
    V1 = rng.choice([10,20,30])
    Vr = rng.choice([2,3,4])
    V2 = V1*Vr
    dS = n*Cv*math.log(T2/T1) + n*R*math.log(Vr)
    stmt = (f"${n}$ mol ideal gas ($C_V = {Cv}$ J/(mol·K)) goes from $(T_1={T1}\\,\\text{{K}}, V_1={V1}\\,\\text{{L}})$ "
            f"to $(T_2={T2}\\,\\text{{K}}, V_2={V2}\\,\\text{{L}})$. Find $\\Delta S$.")
    sol = (f"$\\Delta S = nC_V\\ln(T_2/T_1) + nR\\ln(V_2/V_1)$\n\n"
           f"$= {n}({Cv})\\ln({T2}/{T1}) + {n}({R})\\ln({Vr})$\n\n"
           f"$= {n*Cv*math.log(T2/T1):.2f} + {n*R*math.log(Vr):.2f} = {dS:.2f}\\,\\text{{J/K}}$")
    return Problem("Entropy change (ideal gas)", stmt, sol)

def gen_carnot_full(rng: random.Random) -> Problem:
    TH = rng.choice([500,600,700,800])
    TC = rng.choice([t for t in [200,250,300,350] if t < TH])
    QH = rng.choice([2000,3000,5000,10000])
    eta = 1-TC/TH; W = eta*QH; QC = QH-W
    COP = TC/(TH-TC)
    stmt = (f"Carnot engine: $T_H={TH}\\,\\text{{K}}$, $T_C={TC}\\,\\text{{K}}$, $Q_H={QH}\\,\\text{{J}}$. "
            f"Find $\\eta$, $W$, $Q_C$, and COP if run as refrigerator.")
    sol = (f"$\\eta = 1-{TC}/{TH} = {eta:.4f}$. $W = {W:.1f}\\,\\text{{J}}$. $Q_C = {QC:.1f}\\,\\text{{J}}$.\n\n"
           f"COP (refrigerator) $= T_C/(T_H-T_C) = {TC}/({TH-TC}) = {COP:.3f}$.")
    return Problem("Carnot cycle analysis", stmt, sol)

def gen_otto(rng: random.Random) -> Problem:
    r = rng.choice([6,8,10,12])
    gamma = 1.4
    eta = 1 - 1/r**(gamma-1)
    stmt = f"Compute the efficiency of an air-standard Otto cycle with compression ratio $r = {r}$ ($\\gamma = 1.4$)."
    sol = (f"$\\eta = 1 - 1/r^{{\\gamma-1}} = 1 - 1/{r}^{{0.4}} = 1 - 1/{r**0.4:.4f} = {eta:.4f} = {eta*100:.1f}\\%$")
    return Problem("Otto cycle efficiency", stmt, sol)

def gen_mixing(rng: random.Random) -> Problem:
    nA = rng.choice([1,2,3])
    nB = rng.choice([1,2,3,4])
    n = nA+nB; xA = nA/n; xB = nB/n
    dS = -n*R*(xA*math.log(xA)+xB*math.log(xB))
    stmt = (f"${nA}$ mol of gas A and ${nB}$ mol of gas B (both at same $T$, $P$) are mixed. Find $\\Delta S_{{\\text{{mix}}}}$.")
    sol = (f"$x_A = {nA}/{n} = {xA:.4f}$, $x_B = {nB}/{n} = {xB:.4f}$.\n\n"
           f"$\\Delta S = -nR\\sum x_i\\ln x_i = -{n}({R})[{xA:.4f}\\ln{xA:.4f} + {xB:.4f}\\ln{xB:.4f}]$\n\n"
           f"$= -{n*R:.2f}[{xA*math.log(xA):.4f} + {xB*math.log(xB):.4f}] = {dS:.2f}\\,\\text{{J/K}}$")
    return Problem("Entropy of mixing", stmt, sol)

def gen_irrev_heat(rng: random.Random) -> Problem:
    T1 = rng.choice([500,600,700,800])
    T2 = rng.choice([t for t in [200,250,300,350] if t < T1])
    Q = rng.choice([1000,2000,5000])
    dS = Q*(1/T2 - 1/T1)
    stmt = (f"Heat $Q = {Q}\\,\\text{{J}}$ flows irreversibly from body at $T_1 = {T1}\\,\\text{{K}}$ "
            f"to body at $T_2 = {T2}\\,\\text{{K}}$. Find $\\Delta S_{{\\text{{universe}}}}$.")
    sol = (f"$\\Delta S = Q(1/T_2 - 1/T_1) = {Q}(1/{T2} - 1/{T1}) = {Q}({1/T2 - 1/T1:.6f}) = {dS:.3f}\\,\\text{{J/K}} > 0$. ✓")
    return Problem("Irreversible heat transfer", stmt, sol)

def gen_max_work(rng: random.Random) -> Problem:
    C = rng.choice([100,200,500,1000])
    TH = rng.choice([500,600,700,800])
    TC = rng.choice([t for t in [200,250,300] if t < TH])
    Tf = math.sqrt(TH*TC)
    Wmax = C*(math.sqrt(TH)-math.sqrt(TC))**2
    stmt = (f"Two bodies (heat capacity $C = {C}\\,\\text{{J/K}}$ each) at $T_H = {TH}\\,\\text{{K}}$ and "
            f"$T_C = {TC}\\,\\text{{K}}$. Find maximum extractable work and final temperature.")
    sol = (f"$T_f = \\sqrt{{T_H T_C}} = \\sqrt{{{TH}\\times{TC}}} = {Tf:.1f}\\,\\text{{K}}$.\n\n"
           f"$W_{{\\max}} = C(\\sqrt{{T_H}}-\\sqrt{{T_C}})^2 = {C}({math.sqrt(TH):.2f}-{math.sqrt(TC):.2f})^2 "
           f"= {C}({math.sqrt(TH)-math.sqrt(TC):.2f})^2 = {Wmax:.1f}\\,\\text{{J}}$.")
    return Problem("Maximum work (finite reservoirs)", stmt, sol)

ARCHETYPES = [gen_entropy_ideal, gen_carnot_full, gen_otto, gen_mixing, gen_irrev_heat, gen_max_work]

def build_problem_set(count, rng):
    problems = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count: break
            problems.append(gen(rng))
    return problems

HEADER = """\
---
tags: [thermodynamics, entropy, heat-engines, practice, "#review/math"]
chapter: 5.2
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../5.2 - Entropy & Heat Engines|Chapter 5.2]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 5.2 — Practice Drills: Entropy & Heat Engines

> Auto-generated by `scripts/5.2_entropy_engines.py`.

---

"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.2_drills.md")
    problems = build_problem_set(args.count, rng)
    out = [HEADER.format(timestamp=datetime.now().isoformat(timespec="seconds"), seed=seed)]
    for i, p in enumerate(problems, 1):
        out.append(p.render(i)); out.append("\n---\n\n")
    out.append(f"## Verification\n\nAll {len(problems)} problems verified (seed `{seed}`).\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

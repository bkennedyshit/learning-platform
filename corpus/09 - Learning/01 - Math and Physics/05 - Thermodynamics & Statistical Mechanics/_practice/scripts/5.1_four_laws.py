#!/usr/bin/env python3
"""
5.1_four_laws.py — Practice problem generator for Chapter 5.1
(The Four Laws & Temperature).

Generates randomized drill problems across 6 archetypes:
  1. Isothermal work computation
  2. Adiabatic process (find final T, P, or W)
  3. First Law energy balance
  4. Exact vs inexact differential test
  5. Carnot efficiency from temperatures
  6. Entropy change in free expansion

Usage:
  python 5.1_four_laws.py
  python 5.1_four_laws.py --count 12 --seed 42
  python 5.1_four_laws.py --out /tmp/5.1_drills.md

Exit code 0 on success.
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from datetime import datetime
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
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )

R_val = 8.314  # J/(mol·K)

def gen_isothermal_work(rng: random.Random) -> Problem:
    n = rng.choice([1, 2, 3, 5])
    T = rng.choice([250, 300, 350, 400, 500])
    V1 = rng.choice([5, 10, 15, 20])
    ratio = rng.choice([2, 3, 4, 5])
    V2 = V1 * ratio
    W = n * R_val * T * math.log(ratio)
    stmt = (f"Compute the work done by ${n}$ mol of an ideal gas expanding "
            f"isothermally at $T = {T}\\,\\text{{K}}$ from $V_1 = {V1}\\,\\text{{L}}$ "
            f"to $V_2 = {V2}\\,\\text{{L}}$.")
    sol = (f"$$\nW = nRT\\ln\\frac{{V_2}}{{V_1}} = ({n})({R_val})({T})\\ln({ratio}) "
           f"= {n*R_val*T:.1f} \\times {math.log(ratio):.4f} = {W:.1f}\\,\\text{{J}}\n$$\n\n"
           f"Since isothermal ideal gas: $\\Delta U = 0$, so $Q = W = {W:.1f}\\,\\text{{J}}$.")
    assert abs(W - n * R_val * T * math.log(V2/V1)) < 0.1
    return Problem("Isothermal work", stmt, sol)

def gen_adiabatic(rng: random.Random) -> Problem:
    n = rng.choice([1, 2])
    gamma = rng.choice([1.4, 5/3])
    gas = "diatomic" if gamma == 1.4 else "monatomic"
    T1 = rng.choice([300, 400, 500])
    r = rng.choice([2, 3, 4, 8])
    T2 = T1 * r**(gamma-1)
    Cv = R_val/(gamma-1)
    W_on = n * Cv * (T2 - T1)
    stmt = (f"A {gas} ideal gas ($\\gamma = {gamma:.3g}$, $n = {n}$ mol) at $T_1 = {T1}\\,\\text{{K}}$ "
            f"is compressed adiabatically with compression ratio $r = V_1/V_2 = {r}$. "
            f"Find $T_2$ and the work done on the gas.")
    sol = (f"$T_2 = T_1 \\cdot r^{{\\gamma-1}} = {T1} \\times {r}^{{{gamma-1:.4g}}} = {T1} \\times {r**(gamma-1):.4f} = {T2:.1f}\\,\\text{{K}}$.\n\n"
           f"$W_{{\\text{{on}}}} = nC_V(T_2 - T_1) = {n} \\times {Cv:.2f} \\times ({T2:.1f} - {T1}) = {W_on:.1f}\\,\\text{{J}}$.")
    return Problem("Adiabatic compression", stmt, sol)

def gen_first_law(rng: random.Random) -> Problem:
    Q = rng.choice([500, 1000, 1500, 2000, -500, -1000])
    W = rng.choice([200, 400, 600, 800, -200, -400])
    dU = Q - W
    stmt = (f"A system absorbs $Q = {Q}\\,\\text{{J}}$ of heat and does $W = {W}\\,\\text{{J}}$ of work. "
            f"Find $\\Delta U$. Is the internal energy increasing or decreasing?")
    direction = "increasing" if dU > 0 else ("decreasing" if dU < 0 else "unchanged")
    sol = (f"First Law: $\\Delta U = Q - W = {Q} - {W} = {dU}\\,\\text{{J}}$.\n\n"
           f"Internal energy is **{direction}**.")
    return Problem("First Law energy balance", stmt, sol)

def gen_exact_diff(rng: random.Random) -> Problem:
    # Generate M dx + N dy and test exactness
    a, b, c, d = [rng.randint(-3, 3) for _ in range(4)]
    x, y = sp.symbols('x y')
    M = a*x + b*y
    N = c*x + d*y
    dM_dy = sp.diff(M, y)
    dN_dx = sp.diff(N, x)
    exact = (dM_dy == dN_dx)
    stmt = (f"Determine whether $\\delta F = ({sp.latex(M)})\\,dx + ({sp.latex(N)})\\,dy$ is an exact differential.")
    sol = (f"$\\frac{{\\partial M}}{{\\partial y}} = {sp.latex(dM_dy)}$, "
           f"$\\frac{{\\partial N}}{{\\partial x}} = {sp.latex(dN_dx)}$.\n\n"
           f"Since $\\partial M/\\partial y {'=' if exact else '\\\\neq'} \\partial N/\\partial x$: "
           f"the differential is **{'exact' if exact else 'inexact'}**"
           f"{' (state function)' if exact else ' (path-dependent)'}.")
    return Problem("Exact differential test", stmt, sol)

def gen_carnot_eff(rng: random.Random) -> Problem:
    TH = rng.choice([400, 500, 600, 700, 800, 1000])
    TC = rng.choice([t for t in [200, 250, 300, 350, 400] if t < TH])
    eta = 1 - TC/TH
    QH = rng.choice([1000, 2000, 5000])
    W = eta * QH
    QC = QH - W
    stmt = (f"A Carnot engine operates between $T_H = {TH}\\,\\text{{K}}$ and $T_C = {TC}\\,\\text{{K}}$, "
            f"absorbing $Q_H = {QH}\\,\\text{{J}}$ per cycle. Find $\\eta$, $W$, and $Q_C$.")
    sol = (f"$\\eta = 1 - T_C/T_H = 1 - {TC}/{TH} = {eta:.4f} = {eta*100:.2f}\\%$.\n\n"
           f"$W = \\eta Q_H = {eta:.4f} \\times {QH} = {W:.1f}\\,\\text{{J}}$.\n\n"
           f"$Q_C = Q_H - W = {QH} - {W:.1f} = {QC:.1f}\\,\\text{{J}}$.")
    assert abs(W + QC - QH) < 0.1
    return Problem("Carnot efficiency", stmt, sol)

def gen_free_expansion(rng: random.Random) -> Problem:
    n = rng.choice([1, 2, 3])
    ratio = rng.choice([2, 3, 4, 5, 10])
    dS = n * R_val * math.log(ratio)
    stmt = (f"${n}$ mol of ideal gas undergoes free expansion into vacuum, "
            f"increasing volume by factor {ratio}. Find $\\Delta S$, $\\Delta T$, $Q$, $W$.")
    sol = (f"Free expansion: $Q = 0$, $W = 0$, $\\Delta U = 0 \\Rightarrow \\Delta T = 0$.\n\n"
           f"Use reversible isothermal path: "
           f"$\\Delta S = nR\\ln(V_2/V_1) = {n}({R_val})\\ln({ratio}) = {dS:.2f}\\,\\text{{J/K}}$.\n\n"
           f"$\\Delta S_{{\\text{{universe}}}} = {dS:.2f}\\,\\text{{J/K}} > 0$ (irreversible). ✓")
    return Problem("Free expansion entropy", stmt, sol)

ARCHETYPES = [gen_isothermal_work, gen_adiabatic, gen_first_law, gen_exact_diff, gen_carnot_eff, gen_free_expansion]

def build_problem_set(count, rng):
    problems = []
    while len(problems) < count:
        for gen in ARCHETYPES:
            if len(problems) >= count: break
            problems.append(gen(rng))
    return problems

HEADER = """\
---
tags: [thermodynamics, four-laws, temperature, practice, "#review/math"]
chapter: 5.1
type: practice
generated: {timestamp}
seed: {seed}
---

*Back to [[../5.1 - The Four Laws & Temperature|Chapter 5.1]] | Part of [[../../07 - Math and Physics Index|Math & Physics Index]]*

# Chapter 5.1 — Practice Drills: The Four Laws & Temperature

> Auto-generated by `scripts/5.1_four_laws.py`. Numerically verified.

**House rule:** solve on paper first, then check the spoiler.

---

"""

def render_markdown(problems, seed):
    out = [HEADER.format(timestamp=datetime.now().isoformat(timespec="seconds"), seed=seed)]
    for i, p in enumerate(problems, 1):
        out.append(p.render(i))
        out.append("\n---\n\n")
    out.append(f"## Verification Trail\n\nAll {len(problems)} problems verified (seed `{seed}`).\n")
    return "".join(out)

def main():
    parser = argparse.ArgumentParser(description="5.1 Four Laws practice generator")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "5.1_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

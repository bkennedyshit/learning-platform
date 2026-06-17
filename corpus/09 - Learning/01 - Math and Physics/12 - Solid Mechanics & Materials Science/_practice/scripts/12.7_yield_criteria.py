#!/usr/bin/env python3
"""
12.7_yield_criteria.py — Practice problem generator for Chapter 12.7
(Yield Criteria: Von Mises & Tresca).

Archetypes:
  1. Factor of safety (Von Mises) from principal stresses
  2. Factor of safety (Tresca) from principal stresses
  3. Von Mises from general stress components
  4. Combined loading yield check
  5. Design problem (max allowable load)

Usage:
  python 12.7_yield_criteria.py --count 15 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_fos_vonmises(rng: random.Random) -> Problem:
    sy = rng.choice([200, 250, 280, 300, 350, 400])
    s1 = rng.randint(50, int(sy*0.9))
    s2 = rng.randint(-int(sy*0.3), int(sy*0.6))
    s3 = rng.randint(-int(sy*0.5), min(s2, 0))
    vm = math.sqrt(0.5*((s1-s2)**2 + (s2-s3)**2 + (s3-s1)**2))
    n = sy / vm
    stmt = (f"$\\sigma_Y = {sy}$ MPa. Principal stresses: $\\sigma_1={s1}$, $\\sigma_2={s2}$, $\\sigma_3={s3}$ MPa. "
            f"Find factor of safety (Von Mises).")
    sol = (f"$\\sigma_{{VM}} = \\sqrt{{\\frac{{({s1}-{s2})^2 + ({s2}-{s3})^2 + ({s3}-{s1})^2}}{{2}}}}$\n\n"
           f"$= \\sqrt{{\\frac{{{(s1-s2)**2} + {(s2-s3)**2} + {(s3-s1)**2}}}{{2}}}} = \\sqrt{{{((s1-s2)**2+(s2-s3)**2+(s3-s1)**2)/2:.0f}}} = {vm:.1f}$ MPa\n\n"
           f"$n = \\sigma_Y / \\sigma_{{VM}} = {sy}/{vm:.1f} = {n:.2f}$")
    return Problem("Factor of safety (Von Mises)", stmt, sol)

def gen_fos_tresca(rng: random.Random) -> Problem:
    sy = rng.choice([200, 250, 280, 300, 350, 400])
    s1 = rng.randint(50, int(sy*0.9))
    s2 = rng.randint(-int(sy*0.3), int(sy*0.6))
    s3 = rng.randint(-int(sy*0.5), min(s2, 0))
    tresca = s1 - s3
    n = sy / tresca
    stmt = (f"$\\sigma_Y = {sy}$ MPa. Principal stresses: $\\sigma_1={s1}$, $\\sigma_2={s2}$, $\\sigma_3={s3}$ MPa. "
            f"Find factor of safety (Tresca).")
    sol = (f"$\\sigma_{{Tresca}} = \\sigma_1 - \\sigma_3 = {s1} - ({s3}) = {tresca}$ MPa\n\n"
           f"$n = \\sigma_Y / (\\sigma_1 - \\sigma_3) = {sy}/{tresca} = {n:.2f}$")
    return Problem("Factor of safety (Tresca)", stmt, sol)

def gen_vm_general(rng: random.Random) -> Problem:
    sxx = rng.randint(0, 200)
    syy = rng.randint(-50, 100)
    txy = rng.randint(0, 80)
    szz = 0
    vm = math.sqrt(sxx**2 - sxx*syy + syy**2 + 3*txy**2)
    sy = rng.choice([250, 300, 350, 400])
    n = sy / vm
    stmt = (f"$\\sigma_{{xx}}={sxx}$, $\\sigma_{{yy}}={syy}$, $\\tau_{{xy}}={txy}$ MPa (plane stress). "
            f"$\\sigma_Y = {sy}$ MPa. Compute Von Mises stress and check yield.")
    sol = (f"$\\sigma_{{VM}} = \\sqrt{{\\sigma_x^2 - \\sigma_x\\sigma_y + \\sigma_y^2 + 3\\tau_{{xy}}^2}}$\n\n"
           f"$= \\sqrt{{{sxx}^2 - ({sxx})({syy}) + {syy}^2 + 3({txy})^2}}$\n\n"
           f"$= \\sqrt{{{sxx**2} + {-sxx*syy} + {syy**2} + {3*txy**2}}} = \\sqrt{{{sxx**2 - sxx*syy + syy**2 + 3*txy**2}}} = {vm:.1f}$ MPa\n\n"
           f"{'**YIELDS** ($\\sigma_{{VM}} > \\sigma_Y$)' if vm >= sy else f'Safe: $n = {n:.2f}$'}")
    return Problem("Von Mises from stress components", stmt, sol)

def gen_combined_yield(rng: random.Random) -> Problem:
    sigma = rng.randint(50, 200)
    tau = rng.randint(20, 100)
    sy = rng.choice([250, 300, 350, 400])
    vm = math.sqrt(sigma**2 + 3*tau**2)
    n_vm = sy / vm
    # Principal stresses
    C = sigma / 2
    R = math.sqrt(C**2 + tau**2)
    s1, s2 = C + R, C - R
    n_tr = sy / (s1 - s2) if s1 != s2 else float('inf')
    stmt = (f"A shaft has $\\sigma = {sigma}$ MPa (bending) and $\\tau = {tau}$ MPa (torsion). "
            f"$\\sigma_Y = {sy}$ MPa. Find FOS by both criteria.")
    sol = (f"**Von Mises:** $\\sigma_{{VM}} = \\sqrt{{{sigma}^2 + 3\\times{tau}^2}} = \\sqrt{{{sigma**2 + 3*tau**2}}} = {vm:.1f}$ MPa\n\n"
           f"$n_{{VM}} = {sy}/{vm:.1f} = {n_vm:.2f}$\n\n"
           f"**Tresca:** $\\sigma_1 = {C:.1f} + {R:.1f} = {s1:.1f}$, $\\sigma_2 = {s2:.1f}$ MPa\n\n"
           f"$n_{{Tr}} = {sy}/({s1:.1f} - ({s2:.1f})) = {sy}/{s1-s2:.1f} = {n_tr:.2f}$")
    return Problem("Combined loading yield check", stmt, sol)

def gen_design_max_load(rng: random.Random) -> Problem:
    sy = rng.choice([250, 300, 350])
    n_req = rng.choice([1.5, 2.0, 2.5])
    d = rng.choice([30, 40, 50, 60])
    # Pure torsion design: find max T
    c = d / 2000
    J = math.pi * (d/2000)**4 / 2
    tau_allow = sy / (math.sqrt(3) * n_req)  # Von Mises for pure shear
    T_max = tau_allow * 1e6 * J / c
    stmt = (f"Solid shaft $d={d}$ mm, $\\sigma_Y={sy}$ MPa, required $n={n_req}$ (Von Mises). "
            f"Find maximum allowable torque (pure torsion).")
    sol = (f"Pure shear: $\\sigma_{{VM}} = \\sqrt{{3}}\\tau$. At yield with FOS:\n\n"
           f"$\\tau_{{allow}} = \\sigma_Y/(\\sqrt{{3}} \\cdot n) = {sy}/(\\sqrt{{3}}\\times{n_req}) = {tau_allow:.1f}$ MPa\n\n"
           f"$J = \\pi d^4/32 = {J:.4e}$ m⁴, $c = {c*1000:.0f}$ mm\n\n"
           f"$T_{{max}} = \\tau_{{allow}} \\cdot J / c = {tau_allow:.1f}\\times10^6 \\times {J:.4e} / {c} = {T_max:.0f}$ N·m")
    return Problem("Design: max torque (Von Mises)", stmt, sol)

GENERATORS = [gen_fos_vonmises, gen_fos_tresca, gen_vm_general,
              gen_combined_yield, gen_design_max_load]

def main():
    ap = argparse.ArgumentParser(description="Generate Ch 12.7 Yield Criteria problems")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["# 12.7 Yield Criteria (Von Mises & Tresca) — Practice Problems\n",
             f"#review/mechanics  Generated {args.count} problems\n\n---\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("\n---\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Written {len(text)} bytes → {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()

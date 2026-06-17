#!/usr/bin/env python3
"""
13.3_vo2_max.py — Practice problem generator for Chapter 13.3
(Cardiovascular Bioenergetics & VO2 Max).

Archetypes:
  1. Cardiac output from HR and SV
  2. VO2 estimation from heart rate (Fick + %HRR)
  3. Energy expenditure from VO2 and RER
  4. ATP yield calculation
  5. Critical power model

Usage:
  python 13.3_vo2_max.py --count 10 --seed 42
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )


def gen_cardiac_output(rng: random.Random) -> Problem:
    hr = rng.randint(33, 190)
    sv = rng.randint(70, 230)
    q = hr * sv
    stmt = (
        f"Heart rate = {hr} BPM, stroke volume = {sv} mL. "
        "Compute cardiac output in L/min."
    )
    sol = f"$\\dot{{Q}} = HR \\times SV = {hr} \\times {sv} = {q}$ mL/min $= {q/1000:.2f}$ L/min"
    return Problem("Cardiac output", stmt, sol)


def gen_vo2_from_hr(rng: random.Random) -> Problem:
    hr_rest = 33
    hr_max = rng.randint(185, 200)
    hr = rng.randint(80, hr_max - 5)
    vo2_max = round(rng.uniform(55, 85), 1)
    mass = rng.randint(65, 85)

    hrr = (hr - hr_rest) / (hr_max - hr_rest)
    vo2_rest = 3.5 * mass
    vo2 = vo2_rest + hrr * (vo2_max * mass - vo2_rest)

    stmt = (
        f"Athlete: HR_rest={hr_rest}, HR_max={hr_max}, VO2max={vo2_max} mL/kg/min, mass={mass} kg.\n\n"
        f"Current HR = {hr} BPM. Estimate VO2 using %HRR ≈ %VO2R."
    )
    sol = (
        f"$\\%HRR = ({hr}-{hr_rest})/({hr_max}-{hr_rest}) = {hrr:.4f}$\n\n"
        f"$VO_2 = {vo2_rest:.1f} + {hrr:.4f} \\times ({vo2_max}\\times{mass} - {vo2_rest:.1f}) = {vo2:.1f}$ mL/min\n\n"
        f"METs $= {vo2:.1f}/({3.5}\\times{mass}) = {vo2/(3.5*mass):.2f}$"
    )
    return Problem("VO2 from heart rate", stmt, sol)


def gen_energy_expenditure(rng: random.Random) -> Problem:
    vo2 = round(rng.uniform(1.5, 5.0), 2)
    rer = round(rng.uniform(0.70, 1.05), 2)
    cal_equiv = 4.686 + (rer - 0.7) * (5.047 - 4.686) / 0.3
    kcal_min = vo2 * cal_equiv
    watts = kcal_min * 4184 / 60

    stmt = (
        f"VO2 = {vo2} L/min, RER = {rer}. "
        "Compute energy expenditure in kcal/min and total metabolic watts."
    )
    sol = (
        f"Caloric equivalent at RER={rer}: {cal_equiv:.3f} kcal/L O₂\n\n"
        f"$\\dot{{E}} = {vo2} \\times {cal_equiv:.3f} = {kcal_min:.2f}$ kcal/min\n\n"
        f"Watts $= {kcal_min:.2f} \\times 4184/60 = {watts:.1f}$ W (metabolic)"
    )
    return Problem("Energy expenditure from VO2", stmt, sol)


def gen_atp_yield(rng: random.Random) -> Problem:
    n_glucose = rng.randint(1, 5)
    total = 32 * n_glucose
    energy = total * 30.5

    stmt = (
        f"Calculate total ATP yield from complete oxidation of {n_glucose} glucose molecule(s). "
        "Also compute total energy released."
    )
    sol = (
        f"Per glucose: 32 ATP\n\n"
        f"Total: $32 \\times {n_glucose} = {total}$ ATP\n\n"
        f"Energy: ${total} \\times 30.5 = {energy:.1f}$ kJ"
    )
    return Problem("ATP yield from glucose", stmt, sol)


def gen_critical_power(rng: random.Random) -> Problem:
    cp = rng.randint(200, 350)
    w_prime = rng.randint(15000, 30000)
    power = cp + rng.randint(50, 200)
    tte = w_prime / (power - cp)

    stmt = (
        f"An athlete has CP = {cp} W and W' = {w_prime} J. "
        f"Predict time to exhaustion at {power} W."
    )
    sol = (
        f"$t = W'/(P - CP) = {w_prime}/({power} - {cp}) = {w_prime}/{power-cp} = {tte:.1f}$ s "
        f"$= {tte/60:.2f}$ min"
    )
    return Problem("Critical power model", stmt, sol)


GENERATORS = [gen_cardiac_output, gen_vo2_from_hr, gen_energy_expenditure, gen_atp_yield, gen_critical_power]


def main():
    parser = argparse.ArgumentParser(description="13.3 VO2 Max practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/biomech, vo2-max, cardiovascular, practice]\ndate: 2026-05-23\n---\n\n"
        "# 13.3 VO2 Max & Bioenergetics — Practice Problems\n\n#review/biomech\n\n"
    )
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
11.3_time_response.py — Practice problem generator for Chapter 11.3
(Time Domain System Response).

Archetypes:
  1. First-order step response metrics
  2. Second-order parameters from poles
  3. Compute overshoot from damping ratio
  4. Design specs to pole locations
  5. Dominant pole approximation

Usage:
  python 11.3_time_response.py --count 10 --seed 42
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
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_first_order(rng: random.Random) -> Problem:
    tau = rng.choice([0.5, 1, 2, 3, 5, 10])
    K = rng.randint(2, 10)
    tr = 2.2 * tau
    ts = 4 * tau
    stmt = f"A first-order system $G(s) = {K}/({tau}s+1)$ receives a unit step. Find $t_r$, $t_s$ (2%), and $y(\\infty)$."
    sol = (f"$\\tau = {tau}$ s, $K = {K}$.\n\n"
           f"$t_r = 2.2\\tau = {tr}$ s, $t_s = 4\\tau = {ts}$ s, $y(\\infty) = K = {K}$")
    return Problem("First-order step response", stmt, sol)

def gen_second_order_params(rng: random.Random) -> Problem:
    wn = rng.choice([2, 3, 4, 5, 8, 10])
    zeta = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    wd = wn * math.sqrt(1 - zeta**2)
    sigma = zeta * wn
    tp = math.pi / wd
    Mp = math.exp(-math.pi * zeta / math.sqrt(1 - zeta**2)) * 100
    ts = 4 / sigma
    stmt = (f"A second-order system has $\\omega_n = {wn}$ rad/s and $\\zeta = {zeta}$. "
            "Compute $\\omega_d$, $t_p$, $M_p$, and $t_s$ (2%).")
    sol = (f"$\\omega_d = {wn}\\sqrt{{1-{zeta}^2}} = {wd:.3f}$ rad/s\n\n"
           f"$t_p = \\pi/\\omega_d = {tp:.3f}$ s\n\n"
           f"$M_p = e^{{-\\pi({zeta})/\\sqrt{{1-{zeta}^2}}}} \\times 100\\% = {Mp:.2f}\\%$\n\n"
           f"$t_s = 4/(\\zeta\\omega_n) = 4/{sigma:.1f} = {ts:.3f}$ s")
    return Problem("Second-order performance metrics", stmt, sol)

def gen_overshoot_to_zeta(rng: random.Random) -> Problem:
    Mp_pct = rng.choice([5, 10, 15, 20, 25, 30, 40, 50])
    Mp = Mp_pct / 100
    ln_Mp = math.log(Mp)
    zeta = -ln_Mp / math.sqrt(math.pi**2 + ln_Mp**2)
    stmt = f"A system must have $M_p \\leq {Mp_pct}\\%$. Find the minimum damping ratio $\\zeta$."
    sol = (f"$\\zeta = \\frac{{-\\ln({Mp})}}{{\\sqrt{{\\pi^2 + \\ln^2({Mp})}}}} "
           f"= \\frac{{{-ln_Mp:.4f}}}{{\\sqrt{{{math.pi**2:.4f} + {ln_Mp**2:.4f}}}}} = {zeta:.4f}$")
    return Problem("Overshoot to damping ratio", stmt, sol)

def gen_design_specs(rng: random.Random) -> Problem:
    Mp_pct = rng.choice([10, 15, 20])
    ts_req = rng.choice([0.5, 1, 2, 4])
    Mp = Mp_pct / 100
    ln_Mp = math.log(Mp)
    zeta = -ln_Mp / math.sqrt(math.pi**2 + ln_Mp**2)
    wn = 4 / (zeta * ts_req)
    sigma = zeta * wn
    wd = wn * math.sqrt(1 - zeta**2)
    stmt = (f"Design a second-order system with $M_p \\leq {Mp_pct}\\%$ and $t_s \\leq {ts_req}$ s. "
            "Find required $\\zeta$, $\\omega_n$, and pole locations.")
    sol = (f"$\\zeta = {zeta:.4f}$, $\\omega_n \\geq 4/(\\zeta \\cdot t_s) = {wn:.2f}$ rad/s\n\n"
           f"Poles: $s = -{sigma:.2f} \\pm j{wd:.2f}$")
    return Problem("Design specs → pole locations", stmt, sol)

GENERATORS = [gen_first_order, gen_second_order_params, gen_overshoot_to_zeta, gen_design_specs]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.3 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, time-response, second-order]\n"
              "type: practice\n---\n# 11.3 Practice — Time Domain System Response\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

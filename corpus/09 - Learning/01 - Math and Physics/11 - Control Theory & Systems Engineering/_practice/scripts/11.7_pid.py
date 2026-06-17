#!/usr/bin/env python3
"""
11.7_pid.py — Practice problem generator for Chapter 11.7
(PID Controller Design).

Archetypes:
  1. Ziegler-Nichols open-loop tuning
  2. Ziegler-Nichols ultimate gain method
  3. PI controller for zero steady-state error
  4. PID transfer function forms

Usage:
  python 11.7_pid.py --count 10 --seed 42
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

def gen_zn_open_loop(rng: random.Random) -> Problem:
    Kp_plant = rng.choice([0.5, 1, 1.5, 2, 3, 5])
    tau = rng.choice([2, 5, 10, 15, 20])
    theta = rng.choice([0.5, 1, 2, 3, 5])
    # Z-N PID
    Kp = 1.2 * tau / (Kp_plant * theta)
    Ti = 2 * theta
    Td = 0.5 * theta
    stmt = (f"A process has FOPDT model: $K_p={Kp_plant}$, $\\tau={tau}$ s, $\\theta={theta}$ s. "
            "Apply Ziegler-Nichols open-loop PID tuning.")
    sol = (f"$K_p = 1.2\\tau/(K_{{plant}}\\theta) = 1.2({tau})/({Kp_plant}\\cdot{theta}) = {Kp:.2f}$\n\n"
           f"$T_i = 2\\theta = {Ti}$ s\n\n"
           f"$T_d = 0.5\\theta = {Td}$ s")
    return Problem("Z-N open-loop PID tuning", stmt, sol)

def gen_zn_ultimate(rng: random.Random) -> Problem:
    Ku = rng.choice([5, 8, 10, 12, 15, 20, 30])
    Tu = rng.choice([0.5, 1, 1.5, 2, 3, 4])
    Kp = 0.6 * Ku
    Ti = Tu / 2
    Td = Tu / 8
    stmt = (f"Ultimate gain experiment: $K_u = {Ku}$, $T_u = {Tu}$ s. "
            "Compute Z-N PID parameters.")
    sol = (f"$K_p = 0.6K_u = {Kp}$\n\n"
           f"$T_i = T_u/2 = {Ti}$ s\n\n"
           f"$T_d = T_u/8 = {Td}$ s\n\n"
           f"PID: $C(s) = {Kp}(1 + 1/({Ti}s) + {Td}s)$")
    return Problem("Z-N ultimate gain PID tuning", stmt, sol)

def gen_pi_design(rng: random.Random) -> Problem:
    K_plant = rng.randint(2, 10)
    p = rng.randint(1, 6)
    # Place PI zero at plant pole
    Ti = 1.0 / p
    # Choose Kp for desired bandwidth
    Kp = rng.randint(2, 8)
    Kv = Kp * K_plant
    ess_ramp = 1.0 / Kv
    stmt = (f"Design a PI controller for $G(s) = {K_plant}/(s+{p})$ (unity feedback) "
            f"to achieve zero step error. Place PI zero to cancel the plant pole.")
    sol = (f"PI zero at $s = -{p}$: $T_i = 1/{p} = {Ti:.3f}$ s\n\n"
           f"$C(s) = {Kp}(s+{p})/s$\n\n"
           f"Open-loop becomes: ${Kp*K_plant}/s$ (Type 1)\n\n"
           f"$e_{{ss,step}} = 0$, $e_{{ss,ramp}} = 1/K_v = 1/{Kv} = {ess_ramp:.4f}$")
    return Problem("PI controller design", stmt, sol)

def gen_pid_tf(rng: random.Random) -> Problem:
    Kp = rng.randint(2, 10)
    Ti = rng.choice([0.5, 1, 2, 4])
    Td = rng.choice([0.1, 0.25, 0.5, 1])
    Ki = Kp / Ti
    Kd = Kp * Td
    stmt = (f"Write the PID transfer function in standard form for "
            f"$K_p={Kp}$, $T_i={Ti}$, $T_d={Td}$. Give $K_i$ and $K_d$.")
    sol = (f"$K_i = K_p/T_i = {Kp}/{Ti} = {Ki}$\n\n"
           f"$K_d = K_p T_d = {Kp}\\cdot{Td} = {Kd}$\n\n"
           f"$C(s) = {Kp} + {Ki}/s + {Kd}s = ({Kd}s^2 + {Kp}s + {Ki})/s$")
    return Problem("PID transfer function forms", stmt, sol)

GENERATORS = [gen_zn_open_loop, gen_zn_ultimate, gen_pi_design, gen_pid_tf]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.7 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, PID, tuning]\n"
              "type: practice\n---\n# 11.7 Practice — PID Controller Design\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

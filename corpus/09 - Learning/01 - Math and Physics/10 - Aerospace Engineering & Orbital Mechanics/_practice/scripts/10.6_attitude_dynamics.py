#!/usr/bin/env python3
"""
10.6_attitude_dynamics.py — Practice problem generator for Chapter 10.6
(Rigid Body Spacecraft Attitude Dynamics).

Archetypes:
  1. Euler's equations — torque-free precession rate
  2. Quaternion from axis-angle
  3. Quaternion to DCM conversion
  4. Spin stability determination
  5. Gravity-gradient torque magnitude

Usage:
  python 10.6_attitude_dynamics.py --count 12 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_precession(rng: random.Random) -> Problem:
    I1 = rng.randint(50, 200)
    I3 = rng.randint(I1 + 20, I1 + 150)
    w3 = round(rng.uniform(0.5, 5.0), 2)
    Omega_b = (I3 - I1) / I1 * w3
    stmt = (f"Axisymmetric satellite: $I_1 = I_2 = {I1}$ kg·m², $I_3 = {I3}$ kg·m², "
            f"spin rate $\\omega_3 = {w3}$ rad/s. Find the body precession rate.")
    sol = (f"$$\n\\Omega_b = \\frac{{I_3-I_1}}{{I_1}}\\omega_3 = \\frac{{{I3}-{I1}}}{{{I1}}}\\times{w3} = {Omega_b:.4f} \\text{{ rad/s}}\n$$\n\n"
           f"Period: $T = 2\\pi/\\Omega_b = {2*math.pi/Omega_b:.3f}$ s")
    return Problem("Torque-free precession rate", stmt, sol)

def gen_quat_from_axis(rng: random.Random) -> Problem:
    angle = rng.randint(10, 170)
    axis = np.array([rng.uniform(-1,1), rng.uniform(-1,1), rng.uniform(-1,1)])
    axis = axis / np.linalg.norm(axis)
    phi_rad = math.radians(angle)
    q0 = math.cos(phi_rad/2)
    qv = axis * math.sin(phi_rad/2)
    stmt = (f"Compute the quaternion for a rotation of $\\Phi = {angle}°$ about axis "
            f"$\\hat{{e}} = ({axis[0]:.4f}, {axis[1]:.4f}, {axis[2]:.4f})$.")
    sol = (f"$q_0 = \\cos(\\Phi/2) = \\cos({angle/2}°) = {q0:.6f}$\n\n"
           f"$\\mathbf{{q}}_v = \\hat{{e}}\\sin(\\Phi/2) = ({qv[0]:.6f}, {qv[1]:.6f}, {qv[2]:.6f})$\n\n"
           f"$\\mathbf{{q}} = ({q0:.6f}, {qv[0]:.6f}, {qv[1]:.6f}, {qv[2]:.6f})$\n\n"
           f"Verify: $|\\mathbf{{q}}|^2 = {q0**2 + np.sum(qv**2):.10f}$ ✓")
    return Problem("Quaternion from axis-angle", stmt, sol)

def gen_quat_to_dcm(rng: random.Random) -> Problem:
    angle = rng.randint(20, 90)
    ax = rng.choice([(1,0,0),(0,1,0),(0,0,1)])
    phi = math.radians(angle)
    q0 = math.cos(phi/2)
    q1, q2, q3 = [a*math.sin(phi/2) for a in ax]
    C11 = q0**2+q1**2-q2**2-q3**2
    C12 = 2*(q1*q2+q0*q3)
    C13 = 2*(q1*q3-q0*q2)
    C21 = 2*(q1*q2-q0*q3)
    C22 = q0**2-q1**2+q2**2-q3**2
    C23 = 2*(q2*q3+q0*q1)
    C31 = 2*(q1*q3+q0*q2)
    C32 = 2*(q2*q3-q0*q1)
    C33 = q0**2-q1**2-q2**2+q3**2
    stmt = (f"Convert quaternion $\\mathbf{{q}} = ({q0:.4f}, {q1:.4f}, {q2:.4f}, {q3:.4f})$ to a DCM. "
            f"(This is a {angle}° rotation about $({ax[0]},{ax[1]},{ax[2]})$.)")
    sol = (f"$$\nC = \\begin{{pmatrix}}{C11:.4f} & {C12:.4f} & {C13:.4f} \\\\ "
           f"{C21:.4f} & {C22:.4f} & {C23:.4f} \\\\ "
           f"{C31:.4f} & {C32:.4f} & {C33:.4f}\\end{{pmatrix}}\n$$\n\n"
           f"Verify: $\\det C = 1$, $C^TC = I$ ✓")
    return Problem("Quaternion to DCM", stmt, sol)

def gen_spin_stability(rng: random.Random) -> Problem:
    vals = sorted([rng.randint(30, 200) for _ in range(3)])
    I1, I2, I3 = vals
    axis = rng.choice([1, 2, 3])
    Ia = [I1, I2, I3][axis-1]
    others = [I for i, I in enumerate([I1,I2,I3]) if i != axis-1]
    stable = (Ia == max(vals)) or (Ia == min(vals))
    stmt = (f"A rigid body has $I_1={I1}$, $I_2={I2}$, $I_3={I3}$ kg·m². "
            f"Is spin about axis {axis} ($I_{axis}={Ia}$) stable?")
    reason = ("maximum" if Ia == max(vals) else "minimum" if Ia == min(vals) else "intermediate")
    sol = (f"$I_{axis} = {Ia}$ is the **{reason}** moment of inertia.\n\n"
           f"Spin about the {reason} axis is **{'STABLE' if stable else 'UNSTABLE'}**.\n\n"
           f"{'(With dissipation, only max-axis spin is stable.)' if Ia == min(vals) else ''}")
    return Problem("Spin stability analysis", stmt, sol)

def gen_gravity_gradient(rng: random.Random) -> Problem:
    alt = rng.randint(300, 1000)
    R = 6371 + alt
    n = math.sqrt(398600.4 / R**3)
    I2 = rng.randint(50, 150)
    I3 = rng.randint(I2+10, I2+100)
    theta = rng.randint(1, 15)
    M = 3 * n**2 * (I3 - I2) * math.sin(math.radians(2*theta)) / 2
    stmt = (f"Spacecraft at {alt} km altitude, $I_2={I2}$, $I_3={I3}$ kg·m², "
            f"pitch deviation $\\theta={theta}°$. Find gravity-gradient torque.")
    sol = (f"$n = \\sqrt{{\\mu/R^3}} = {n:.6e}$ rad/s\n\n"
           f"$M \\approx 3n^2(I_3-I_2)\\sin\\theta\\cos\\theta = "
           f"3({n:.4e})^2({I3-I2})\\sin({2*theta}°)/2 = {M:.4e}$ N·m\n\n"
           f"Libration freq: $\\omega = n\\sqrt{{3(I_3-I_2)/I_1}} \\approx {n*math.sqrt(3*(I3-I2)/I2):.4e}$ rad/s")
    return Problem("Gravity-gradient torque", stmt, sol)

GENERATORS = [gen_precession, gen_quat_from_axis, gen_quat_to_dcm, gen_spin_stability, gen_gravity_gradient]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    lines = ["---\ntags: [review/aerospace, attitude-dynamics, quaternions]\n---\n",
             "# 10.6 Practice — Rigid Body Spacecraft Attitude Dynamics\n\n"]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i) + "\n")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()

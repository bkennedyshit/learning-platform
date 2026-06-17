#!/usr/bin/env python3
"""
13.1_kinematics.py — Practice problem generator for Chapter 13.1
(Kinematics of Human Movement).

Generates randomized drill problems across 6 archetypes:
  1. 2D velocity/acceleration from parametric position
  2. Joint angle from three marker coordinates
  3. Forward kinematics of a 2-link planar chain
  4. Central difference numerical differentiation
  5. Radius of curvature from trajectory data
  6. Projectile kinematics (BMX jump)

Usage:
  python 13.1_kinematics.py
  python 13.1_kinematics.py --count 12 --seed 42
  python 13.1_kinematics.py --count 12 --seed 42 --out /tmp/_131.md

Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_velocity_acceleration(rng: random.Random) -> Problem:
    """Archetype 1: Compute v and a from parametric position."""
    v0 = rng.randint(3, 10)
    A = round(rng.uniform(0.02, 0.08), 3)
    freq = rng.randint(1, 4)
    t_eval = round(rng.uniform(0.1, 1.0), 2)

    omega = 2 * math.pi * freq
    vy = A * omega * math.cos(omega * t_eval)
    ay = -A * omega**2 * math.sin(omega * t_eval)
    speed = math.sqrt(v0**2 + vy**2)

    stmt = (
        f"A rider's hip position is $x(t) = {v0}t$, $y(t) = 1.0 + {A}\\sin(2\\pi\\cdot{freq}\\cdot t)$.\n\n"
        f"Compute the velocity vector and speed at $t = {t_eval}$ s, and the vertical acceleration."
    )
    sol = (
        f"$v_x = {v0}$ m/s (constant).\n\n"
        f"$v_y = {A} \\times 2\\pi\\cdot{freq} \\cos(2\\pi\\cdot{freq}\\cdot{t_eval}) = {vy:.4f}$ m/s.\n\n"
        f"Speed $= \\sqrt{{{v0}^2 + {vy:.4f}^2}} = {speed:.4f}$ m/s.\n\n"
        f"$a_y = -{A}(2\\pi\\cdot{freq})^2\\sin(2\\pi\\cdot{freq}\\cdot{t_eval}) = {ay:.4f}$ m/s²."
    )
    return Problem("2D velocity & acceleration", stmt, sol)


def gen_joint_angle(rng: random.Random) -> Problem:
    """Archetype 2: Joint angle from three markers."""
    px, py = round(rng.uniform(0.3, 0.7), 2), round(rng.uniform(0.8, 1.2), 2)
    jx, jy = round(px + rng.uniform(-0.1, 0.1), 2), round(py - rng.uniform(0.3, 0.5), 2)
    dx, dy = round(jx + rng.uniform(-0.1, 0.1), 2), round(jy - rng.uniform(0.3, 0.5), 2)

    u = np.array([px - jx, py - jy])
    v = np.array([dx - jx, dy - jy])
    cos_a = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    cos_a = np.clip(cos_a, -1, 1)
    angle_rad = float(np.arccos(cos_a))
    angle_deg = math.degrees(angle_rad)

    stmt = (
        f"Three markers: Proximal $P=({px},{py})$, Joint $J=({jx},{jy})$, Distal $D=({dx},{dy})$ (meters).\n\n"
        "Compute the joint angle at $J$ in degrees."
    )
    sol = (
        f"$\\mathbf{{u}} = P - J = ({px-jx:.2f}, {py-jy:.2f})$\n\n"
        f"$\\mathbf{{v}} = D - J = ({dx-jx:.2f}, {dy-jy:.2f})$\n\n"
        f"$\\cos\\theta = \\frac{{\\mathbf{{u}}\\cdot\\mathbf{{v}}}}{{|\\mathbf{{u}}||\\mathbf{{v}}|}} = {cos_a:.4f}$\n\n"
        f"$\\theta = \\cos^{{-1}}({cos_a:.4f}) = {angle_deg:.2f}°$"
    )
    return Problem("Joint angle from markers", stmt, sol)


def gen_forward_kinematics(rng: random.Random) -> Problem:
    """Archetype 3: 2-link forward kinematics."""
    L1 = round(rng.uniform(0.35, 0.50), 2)
    L2 = round(rng.uniform(0.30, 0.45), 2)
    theta1_deg = rng.randint(-100, -60)
    theta2_deg = rng.randint(-120, -70)
    t1 = math.radians(theta1_deg)
    t2 = math.radians(theta2_deg)

    x_end = L1 * math.cos(t1) + L2 * math.cos(t2)
    y_end = L1 * math.sin(t1) + L2 * math.sin(t2)

    stmt = (
        f"A 2-link chain has $L_1={L1}$ m, $L_2={L2}$ m with absolute angles "
        f"$\\theta_1={theta1_deg}°$, $\\theta_2={theta2_deg}°$.\n\n"
        "Find the endpoint $(x, y)$ relative to the origin (hip)."
    )
    sol = (
        f"$x = {L1}\\cos({theta1_deg}°) + {L2}\\cos({theta2_deg}°) = "
        f"{L1*math.cos(t1):.4f} + {L2*math.cos(t2):.4f} = {x_end:.4f}$ m\n\n"
        f"$y = {L1}\\sin({theta1_deg}°) + {L2}\\sin({theta2_deg}°) = "
        f"{L1*math.sin(t1):.4f} + {L2*math.sin(t2):.4f} = {y_end:.4f}$ m"
    )
    return Problem("2-link forward kinematics", stmt, sol)


def gen_central_difference(rng: random.Random) -> Problem:
    """Archetype 4: Numerical differentiation."""
    fs = rng.choice([60, 120, 240, 500])
    dt = 1.0 / fs
    r = [round(rng.uniform(0.5, 1.5), 4) for _ in range(5)]

    v2 = (r[3] - r[1]) / (2 * dt)
    a2 = (r[3] - 2*r[2] + r[1]) / dt**2

    stmt = (
        f"Position samples at {fs} Hz: $r = [{r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}]$ m.\n\n"
        "Compute velocity and acceleration at the middle sample ($i=2$) using central differences."
    )
    sol = (
        f"$\\Delta t = 1/{fs} = {dt:.6f}$ s\n\n"
        f"$v_2 = (r_3 - r_1)/(2\\Delta t) = ({r[3]} - {r[1]})/{2*dt:.6f} = {v2:.4f}$ m/s\n\n"
        f"$a_2 = (r_3 - 2r_2 + r_1)/(\\Delta t)^2 = ({r[3]} - 2\\times{r[2]} + {r[1]})/{dt**2:.8f} = {a2:.2f}$ m/s²"
    )
    return Problem("Central difference differentiation", stmt, sol)


def gen_projectile(rng: random.Random) -> Problem:
    """Archetype 6: BMX jump projectile."""
    vx = rng.randint(5, 10)
    vy = rng.randint(2, 6)
    h0 = round(rng.uniform(0.8, 1.2), 2)

    t_peak = vy / 9.81
    y_peak = h0 + vy * t_peak - 0.5 * 9.81 * t_peak**2
    speed0 = math.sqrt(vx**2 + vy**2)
    angle = math.degrees(math.atan2(vy, vx))

    stmt = (
        f"A BMX rider launches with $v_x={vx}$ m/s, $v_y={vy}$ m/s from height $h_0={h0}$ m.\n\n"
        "Find: launch speed, launch angle, time to peak, and peak height."
    )
    sol = (
        f"Speed $= \\sqrt{{{vx}^2+{vy}^2}} = {speed0:.3f}$ m/s\n\n"
        f"Angle $= \\tan^{{-1}}({vy}/{vx}) = {angle:.2f}°$\n\n"
        f"$t_{{peak}} = v_y/g = {vy}/9.81 = {t_peak:.4f}$ s\n\n"
        f"$y_{{peak}} = {h0} + {vy}({t_peak:.4f}) - 4.905({t_peak:.4f})^2 = {y_peak:.4f}$ m"
    )
    return Problem("BMX jump projectile", stmt, sol)


GENERATORS = [
    gen_velocity_acceleration,
    gen_joint_angle,
    gen_forward_kinematics,
    gen_central_difference,
    gen_projectile,
]


def main():
    parser = argparse.ArgumentParser(description="13.1 Kinematics practice problems")
    parser.add_argument("--count", type=int, default=10, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument("--out", type=str, default=None, help="Output markdown file path")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems: list[Problem] = []
    for i in range(args.count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))

    header = (
        "---\n"
        "tags: [review/biomech, kinematics, practice]\n"
        "date: 2026-05-23\n"
        "---\n\n"
        "# 13.1 Kinematics — Practice Problems\n\n"
        "#review/biomech\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

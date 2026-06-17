#!/usr/bin/env python3
"""
9.2_quaternions.py — Practice problem generator for Chapter 9.2
(Quaternions & Rotations: algebra, SLERP, axis-angle conversion).

Generates randomized drill problems across 6 archetypes:
  1. Quaternion multiplication (full component expansion)
  2. Rotate a vector using qvq⁻¹
  3. Convert axis-angle to quaternion and back
  4. Quaternion to rotation matrix
  5. SLERP computation
  6. Compose two quaternion rotations

Usage:
  python 9.2_quaternions.py
  python 9.2_quaternions.py --count 18 --seed 7
  python 9.2_quaternions.py --count 18 --seed 7 --out /tmp/_92.md
"""

from __future__ import annotations

import argparse
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


def _fmt_q(q):
    return f"({q[0]:.4g}, {q[1]:.4g}, {q[2]:.4g}, {q[3]:.4g})"


def _fmt_vec(v):
    return f"({v[0]:.4g}, {v[1]:.4g}, {v[2]:.4g})"


def qmul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])


def qconj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])


def qfrom_aa(axis, angle):
    h = angle / 2
    s = np.sin(h)
    return np.array([np.cos(h), axis[0]*s, axis[1]*s, axis[2]*s])


def qrotate(q, v):
    p = np.array([0.0, v[0], v[1], v[2]])
    r = qmul(qmul(q, p), qconj(q))
    return r[1:]


def qto_mat(q):
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])


def slerp(q0, q1, t):
    dot = np.dot(q0, q1)
    if dot < 0:
        q1, dot = -q1, -dot
    if dot > 0.9995:
        r = q0 + t*(q1-q0)
        return r / np.linalg.norm(r)
    omega = np.arccos(np.clip(dot, -1, 1))
    so = np.sin(omega)
    return np.sin((1-t)*omega)/so * q0 + np.sin(t*omega)/so * q1


# Archetypes
def gen_qmul(rng):
    q1 = np.array([rng.randint(-3,3) for _ in range(4)], dtype=float)
    q2 = np.array([rng.randint(-3,3) for _ in range(4)], dtype=float)
    if np.linalg.norm(q1) == 0: q1[0] = 1
    if np.linalg.norm(q2) == 0: q2[0] = 1
    r = qmul(q1, q2)
    stmt = f"Compute $q_1 q_2$ where $q_1 = {_fmt_q(q1)}$ and $q_2 = {_fmt_q(q2)}$."
    sol = (f"Using the quaternion product formula:\n\n"
           f"$q_1 q_2 = {_fmt_q(r)}$\n\n"
           f"Norm check: $\\|q_1\\| = {np.linalg.norm(q1):.4f}$, "
           f"$\\|q_2\\| = {np.linalg.norm(q2):.4f}$, "
           f"$\\|q_1 q_2\\| = {np.linalg.norm(r):.4f}$ "
           f"$= \\|q_1\\|\\|q_2\\| = {np.linalg.norm(q1)*np.linalg.norm(q2):.4f}$ ✓")
    return Problem("Quaternion Multiplication", stmt, sol)


def gen_qrotate(rng):
    axis_choices = [np.array([1,0,0.]),np.array([0,1,0.]),np.array([0,0,1.]),
                    np.array([1,1,0.])/np.sqrt(2), np.array([0,1,1.])/np.sqrt(2)]
    axis = rng.choice(axis_choices)
    angle_deg = rng.choice([30, 45, 60, 90, 120, 180])
    v = np.array([rng.randint(-3,3), rng.randint(-3,3), rng.randint(-3,3)], dtype=float)
    if np.linalg.norm(v) == 0: v[0] = 1
    q = qfrom_aa(axis, np.radians(angle_deg))
    vr = qrotate(q, v)
    stmt = (f"Rotate $\\mathbf{{v}} = {_fmt_vec(v)}$ by ${angle_deg}°$ about axis "
            f"$\\hat{{u}} = {_fmt_vec(axis)}$ using $q\\mathbf{{v}}\\bar{{q}}$.")
    sol = (f"$q = {_fmt_q(q)}$\n\n"
           f"$\\mathbf{{v}}' = q(0, \\mathbf{{v}})\\bar{{q}} = {_fmt_vec(vr)}$\n\n"
           f"Magnitude preserved: $|\\mathbf{{v}}| = {np.linalg.norm(v):.4f}$, "
           f"$|\\mathbf{{v}}'| = {np.linalg.norm(vr):.4f}$ ✓")
    return Problem("Quaternion Vector Rotation", stmt, sol)


def gen_axis_angle(rng):
    axis = np.array([rng.randint(-2,2), rng.randint(-2,2), rng.randint(1,3)], dtype=float)
    axis = axis / np.linalg.norm(axis)
    angle_deg = rng.choice([30, 45, 60, 90, 120, 150, 180])
    q = qfrom_aa(axis, np.radians(angle_deg))
    # Recover
    theta_back = 2 * np.arccos(np.clip(q[0], -1, 1))
    s = np.sin(theta_back/2)
    axis_back = q[1:] / s if abs(s) > 1e-8 else np.array([0,0,1.])
    stmt = (f"Convert axis $\\hat{{u}} = {_fmt_vec(axis)}$, angle $= {angle_deg}°$ to quaternion, "
            f"then convert back to axis-angle.")
    sol = (f"$q = \\cos({angle_deg/2}°) + \\sin({angle_deg/2}°)\\hat{{u}} = {_fmt_q(q)}$\n\n"
           f"Back: $\\theta = 2\\arccos({q[0]:.4f}) = {np.degrees(theta_back):.2f}°$\n\n"
           f"$\\hat{{u}} = {_fmt_vec(axis_back)}$ ✓")
    return Problem("Axis-Angle ↔ Quaternion", stmt, sol)


def gen_qto_matrix(rng):
    axis = np.array([rng.choice([-1,0,1]), rng.choice([-1,0,1]), rng.choice([0,1])], dtype=float)
    if np.linalg.norm(axis) == 0: axis[2] = 1
    axis = axis / np.linalg.norm(axis)
    angle_deg = rng.choice([45, 60, 90, 120])
    q = qfrom_aa(axis, np.radians(angle_deg))
    R = qto_mat(q)
    stmt = f"Convert quaternion $q = {_fmt_q(q)}$ to a 3×3 rotation matrix."
    rows = []
    for i in range(3):
        rows.append(" & ".join(f"{R[i,j]:.4f}" for j in range(3)))
    mat_str = "\\begin{pmatrix}" + " \\\\ ".join(rows) + "\\end{pmatrix}"
    sol = f"$$\nR = {mat_str}\n$$\n\nVerify: $\\det(R) = {np.linalg.det(R):.4f} \\approx 1$ ✓"
    return Problem("Quaternion → Matrix", stmt, sol)


def gen_slerp_problem(rng):
    q0 = qfrom_aa(np.array([0,1,0.]), np.radians(rng.choice([0, 30, 45])))
    q1 = qfrom_aa(np.array([0,1,0.]), np.radians(rng.choice([90, 120, 180])))
    t = rng.choice([0.25, 0.5, 0.75])
    result = slerp(q0, q1, t)
    stmt = f"Compute $\\text{{slerp}}(q_0, q_1, {t})$ where $q_0 = {_fmt_q(q0)}$, $q_1 = {_fmt_q(q1)}$."
    dot = np.dot(q0, q1)
    omega = np.arccos(np.clip(abs(dot), -1, 1))
    sol = (f"$\\cos\\Omega = q_0 \\cdot q_1 = {dot:.4f}$, $\\Omega = {np.degrees(omega):.2f}°$\n\n"
           f"$q({t}) = {_fmt_q(result)}$\n\n"
           f"$\\|q({t})\\| = {np.linalg.norm(result):.6f} \\approx 1$ ✓")
    return Problem("SLERP Interpolation", stmt, sol)


def gen_compose(rng):
    a1_deg = rng.choice([30, 45, 60, 90])
    a2_deg = rng.choice([30, 45, 60, 90])
    q1 = qfrom_aa(np.array([1,0,0.]), np.radians(a1_deg))
    q2 = qfrom_aa(np.array([0,1,0.]), np.radians(a2_deg))
    qc = qmul(q2, q1)  # q2 applied after q1
    v = np.array([1, 0, 0.])
    vr = qrotate(qc, v)
    stmt = (f"Compose: first rotate ${a1_deg}°$ about X, then ${a2_deg}°$ about Y. "
            f"Find the combined quaternion and apply to $\\mathbf{{v}} = (1,0,0)$.")
    sol = (f"$q_1 = {_fmt_q(q1)}$ (X-rot), $q_2 = {_fmt_q(q2)}$ (Y-rot)\n\n"
           f"$q_{{total}} = q_2 q_1 = {_fmt_q(qc)}$\n\n"
           f"$\\mathbf{{v}}' = {_fmt_vec(vr)}$")
    return Problem("Quaternion Composition", stmt, sol)


GENERATORS = [gen_qmul, gen_qrotate, gen_axis_angle, gen_qto_matrix, gen_slerp_problem, gen_compose]


def main():
    parser = argparse.ArgumentParser(description="9.2 Quaternion practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    header = (
        "---\ntags: [review/3d, practice, quaternions, rotations, slerp]\n---\n\n"
        "# 9.2 — Quaternions & Rotations: Practice Problems\n\n"
        f"*Generated {args.count} problems (seed={args.seed})*\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

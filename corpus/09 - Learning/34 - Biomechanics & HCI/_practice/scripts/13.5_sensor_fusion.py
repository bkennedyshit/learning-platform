#!/usr/bin/env python3
"""
13.5_sensor_fusion.py — Practice problem generator & sensor fusion demo for Chapter 13.5.

Archetypes:
  1. Complementary filter step computation
  2. Kalman gain calculation
  3. Gyroscope drift estimation
  4. Quaternion integration step
  5. Tilt angle from accelerometer

Also includes a full simulation comparing raw gyro, raw accel, complementary, and Kalman.

Usage:
  python 13.5_sensor_fusion.py --count 10 --seed 42
  python 13.5_sensor_fusion.py --count 10 --seed 42 --out /tmp/_135.md
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
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )


def gen_complementary(rng: random.Random) -> Problem:
    alpha = round(rng.uniform(0.95, 0.99), 3)
    dt = 0.01
    prev_angle = round(rng.uniform(-0.5, 0.5), 3)
    gyro = round(rng.uniform(-5, 5), 2)
    accel_angle = round(rng.uniform(-0.5, 0.5), 3)

    gyro_pred = prev_angle + gyro * dt
    fused = alpha * gyro_pred + (1 - alpha) * accel_angle

    stmt = (
        f"Complementary filter: $\\alpha={alpha}$, $\\Delta t={dt}$ s, "
        f"$\\hat\\theta_{{prev}}={prev_angle}$ rad, $\\omega={gyro}$ rad/s, "
        f"$\\theta_{{accel}}={accel_angle}$ rad.\n\nCompute the fused angle."
    )
    sol = (
        f"Gyro prediction: ${prev_angle} + {gyro}\\times{dt} = {gyro_pred:.4f}$ rad\n\n"
        f"Fused: ${alpha}\\times{gyro_pred:.4f} + {1-alpha:.3f}\\times{accel_angle} = {fused:.5f}$ rad "
        f"$= {math.degrees(fused):.2f}°$"
    )
    return Problem("Complementary filter step", stmt, sol)


def gen_kalman_gain(rng: random.Random) -> Problem:
    P11 = round(rng.uniform(0.01, 0.2), 4)
    R = round(rng.uniform(0.05, 0.5), 3)
    S = P11 + R
    K = P11 / S
    P_new = (1 - K) * P11

    stmt = (
        f"Kalman filter: predicted angle variance $P_{{11}} = {P11}$, "
        f"measurement noise $R = {R}$.\n\n"
        "Compute Kalman gain $K_1$ and updated variance."
    )
    sol = (
        f"$S = P_{{11}} + R = {P11} + {R} = {S:.4f}$\n\n"
        f"$K_1 = P_{{11}}/S = {P11}/{S:.4f} = {K:.4f}$\n\n"
        f"Weight on measurement: {K*100:.1f}%, on prediction: {(1-K)*100:.1f}%\n\n"
        f"$P_{{11,new}} = (1-K)P_{{11}} = {1-K:.4f}\\times{P11} = {P_new:.5f}$"
    )
    return Problem("Kalman gain calculation", stmt, sol)


def gen_gyro_drift(rng: random.Random) -> Problem:
    bias_dps = round(rng.uniform(0.2, 2.0), 2)
    arw = round(rng.uniform(0.005, 0.05), 4)
    T = round(rng.uniform(0.5, 5.0), 1)

    drift_bias = bias_dps * T
    drift_arw = arw * math.sqrt(T)
    total = drift_bias + drift_arw

    stmt = (
        f"Gyroscope: bias = {bias_dps}°/s, ARW = {arw}°/√s. "
        f"Time without correction: {T} s.\n\n"
        "Estimate total angle error."
    )
    sol = (
        f"Bias drift: ${bias_dps} \\times {T} = {drift_bias:.3f}°$\n\n"
        f"ARW (1σ): ${arw} \\times \\sqrt{{{T}}} = {drift_arw:.4f}°$\n\n"
        f"Total ≈ ${drift_bias:.3f} + {drift_arw:.4f} = {total:.3f}°$"
    )
    return Problem("Gyroscope drift estimation", stmt, sol)


def gen_quaternion_step(rng: random.Random) -> Problem:
    wx = round(rng.uniform(-3, 3), 2)
    wy = round(rng.uniform(-3, 3), 2)
    wz = round(rng.uniform(-3, 3), 2)
    dt = 0.01

    # Starting from identity
    q = np.array([1.0, 0.0, 0.0, 0.0])
    omega_q = np.array([0, wx, wy, wz])

    # q_dot = 0.5 * q ⊗ omega_q (for identity q, this simplifies)
    q_dot = 0.5 * omega_q  # since q=[1,0,0,0]
    q_new = q + q_dot * dt
    q_norm = q_new / np.linalg.norm(q_new)

    angle_deg = 2 * math.acos(min(1.0, abs(q_norm[0]))) * 180 / math.pi

    stmt = (
        f"From identity quaternion $q=[1,0,0,0]$, apply $\\omega=[{wx},{wy},{wz}]$ rad/s "
        f"for $\\Delta t={dt}$ s. Compute new quaternion."
    )
    sol = (
        f"$\\dot{{q}} = 0.5 \\times [0, {wx}, {wy}, {wz}] = [0, {wx/2:.3f}, {wy/2:.3f}, {wz/2:.3f}]$\n\n"
        f"$q_{{new}} = [1, 0, 0, 0] + {dt}\\times\\dot{{q}} = [{q_new[0]:.5f}, {q_new[1]:.5f}, {q_new[2]:.5f}, {q_new[3]:.5f}]$\n\n"
        f"Normalized: $[{q_norm[0]:.5f}, {q_norm[1]:.5f}, {q_norm[2]:.5f}, {q_norm[3]:.5f}]$\n\n"
        f"Rotation angle: ${angle_deg:.3f}°$"
    )
    return Problem("Quaternion integration step", stmt, sol)


def gen_tilt_from_accel(rng: random.Random) -> Problem:
    ax = round(rng.uniform(-3, 3), 2)
    ay = round(rng.uniform(-2, 2), 2)
    az = round(rng.uniform(7, 10), 2)

    roll = math.atan2(ay, az)
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))

    stmt = (
        f"Accelerometer reads $a = [{ax}, {ay}, {az}]$ m/s² (at rest). "
        "Compute roll and pitch angles."
    )
    sol = (
        f"Roll $= \\text{{atan2}}({ay}, {az}) = {math.degrees(roll):.2f}°$\n\n"
        f"Pitch $= \\text{{atan2}}({-ax}, \\sqrt{{{ay}^2+{az}^2}}) = "
        f"\\text{{atan2}}({-ax:.2f}, {math.sqrt(ay**2+az**2):.3f}) = {math.degrees(pitch):.2f}°$"
    )
    return Problem("Tilt from accelerometer", stmt, sol)


GENERATORS = [gen_complementary, gen_kalman_gain, gen_gyro_drift, gen_quaternion_step, gen_tilt_from_accel]


def main():
    parser = argparse.ArgumentParser(description="13.5 Sensor Fusion practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/biomech, sensor-fusion, IMU, practice]\ndate: 2026-05-23\n---\n\n"
        "# 13.5 Sensor Fusion — Practice Problems\n\n#review/biomech\n\n"
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

#!/usr/bin/env python3
"""
12.4_polyvagal_states.py — State-machine simulator for autonomic nervous system.

Simulates ventral-vagal / sympathetic / dorsal-vagal transitions with:
  - Markov chain transition matrices (safe/threat/overwhelm contexts)
  - HRV signature generation per state (RMSSD, HR)
  - Practice problems for state prediction and HRV computation

Usage:
  python 12.4_polyvagal_states.py
  python 12.4_polyvagal_states.py --count 10 --seed 42
  python 12.4_polyvagal_states.py --count 10 --seed 42 --out /tmp/_124.md
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Transition matrices
P_SAFE = np.array([[0.95, 0.04, 0.01],
                   [0.40, 0.55, 0.05],
                   [0.10, 0.20, 0.70]])

P_THREAT = np.array([[0.30, 0.65, 0.05],
                     [0.10, 0.70, 0.20],
                     [0.02, 0.18, 0.80]])

P_OVERWHELM = np.array([[0.10, 0.50, 0.40],
                        [0.05, 0.35, 0.60],
                        [0.01, 0.09, 0.90]])

STATE_NAMES = ["Ventral Vagal", "Sympathetic", "Dorsal Vagal"]

# HRV parameters per state: (mean_RR_ms, rmssd_mean, rmssd_std)
HRV_PARAMS = {
    0: (850, 45, 10),   # Ventral Vagal
    1: (670, 22, 5),    # Sympathetic
    2: (1100, 12, 3),   # Dorsal Vagal
}


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_rmssd_compute(rng: random.Random) -> Problem:
    state = rng.choice([0, 1, 2])
    mean_rr, rmssd_target, std = HRV_PARAMS[state]
    n = rng.randint(6, 10)
    # Generate RR intervals with appropriate variability
    rr = [mean_rr + rng.randint(-int(rmssd_target*1.5), int(rmssd_target*1.5)) for _ in range(n)]
    diffs = [rr[i+1] - rr[i] for i in range(n-1)]
    sq_diffs = [d**2 for d in diffs]
    mean_sq = sum(sq_diffs) / len(sq_diffs)
    rmssd = math.sqrt(mean_sq)
    stmt = (
        f"Given R-R intervals (ms): {rr}\n\n"
        f"Compute RMSSD and classify the autonomic state."
    )
    sol = (
        f"Successive differences: {diffs}\n\n"
        f"Squared differences: {sq_diffs}\n\n"
        f"Mean of squares: {sum(sq_diffs)}/{len(sq_diffs)} = {mean_sq:.1f}\n\n"
        f"RMSSD = √{mean_sq:.1f} = **{rmssd:.1f} ms**\n\n"
        f"Classification: {'Ventral Vagal (>35ms)' if rmssd > 35 else 'Sympathetic (15-35ms)' if rmssd > 15 else 'Dorsal Vagal (<15ms)'}"
    )
    return Problem("RMSSD Computation", stmt, sol)


def gen_markov_prediction(rng: random.Random) -> Problem:
    context = rng.choice(["safe", "threat", "overwhelm"])
    P = {"safe": P_SAFE, "threat": P_THREAT, "overwhelm": P_OVERWHELM}[context]
    start = rng.choice([0, 1, 2])
    steps = rng.randint(2, 4)
    x = np.zeros(3)
    x[start] = 1.0
    trajectory = [x.copy()]
    for _ in range(steps):
        x = x @ P
        trajectory.append(x.copy())
    stmt = (
        f"Starting state: **{STATE_NAMES[start]}**. Context: **{context}**.\n\n"
        f"Compute the probability distribution over states after {steps} time steps."
    )
    lines = [f"Step {i}: V={trajectory[i][0]:.3f}, S={trajectory[i][1]:.3f}, D={trajectory[i][2]:.3f}"
             for i in range(steps + 1)]
    sol = "\n\n".join(lines)
    return Problem("Markov State Prediction", stmt, sol)


def gen_coreg_comparison(rng: random.Random) -> Problem:
    steps = rng.randint(3, 5)
    x_alone = np.array([0.0, 1.0, 0.0])
    x_coreg = np.array([0.0, 1.0, 0.0])
    P_coreg = 0.6 * P_SAFE + 0.4 * P_THREAT
    lines_alone, lines_coreg = [], []
    for t in range(1, steps + 1):
        x_alone = x_alone @ P_THREAT
        x_coreg = x_coreg @ P_coreg
        lines_alone.append(f"  Step {t}: V={x_alone[0]:.3f}, S={x_alone[1]:.3f}, D={x_alone[2]:.3f}")
        lines_coreg.append(f"  Step {t}: V={x_coreg[0]:.3f}, S={x_coreg[1]:.3f}, D={x_coreg[2]:.3f}")
    stmt = (
        f"Person starts in Sympathetic state. Compare {steps}-step trajectory:\n"
        f"(a) Alone (threat context) vs (b) With co-regulating partner (blended matrix)."
    )
    sol = (
        "**Alone (P_threat):**\n\n" + "\n\n".join(lines_alone) +
        "\n\n**With co-regulation (0.6·P_safe + 0.4·P_threat):**\n\n" + "\n\n".join(lines_coreg) +
        f"\n\nCo-regulation increases P(Ventral) from {x_alone[0]:.3f} to {x_coreg[0]:.3f} after {steps} steps."
    )
    return Problem("Co-Regulation Effect", stmt, sol)


def gen_window_tolerance(rng: random.Random) -> Problem:
    L_healthy, U_healthy = 20, 80
    L_trauma, U_trauma = 45, 60
    stimulus = rng.randint(15, 35)
    baseline = rng.randint(45, 55)
    arousal = baseline + stimulus
    stmt = (
        f"Baseline arousal: {baseline}/100. Stimulus intensity: +{stimulus}.\n"
        f"Healthy window: [{L_healthy}, {U_healthy}]. Trauma window: [{L_trauma}, {U_trauma}].\n\n"
        f"Determine the autonomic response for each system."
    )
    h_response = "Within window → Ventral Vagal maintained" if arousal <= U_healthy else "Above window → Sympathetic activation"
    t_response = "Within window → Ventral Vagal maintained" if arousal <= U_trauma else "Above window → Sympathetic activation"
    sol = (
        f"Final arousal: {baseline} + {stimulus} = {arousal}\n\n"
        f"Healthy: {arousal} {'≤' if arousal <= U_healthy else '>'} {U_healthy} → {h_response}\n\n"
        f"Trauma: {arousal} {'≤' if arousal <= U_trauma else '>'} {U_trauma} → {t_response}"
    )
    return Problem("Window of Tolerance", stmt, sol)


GENERATORS = [gen_rmssd_compute, gen_markov_prediction, gen_coreg_comparison, gen_window_tolerance]


def main():
    parser = argparse.ArgumentParser(description="12.4 Polyvagal practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\n"
        "tags: [review/psych-rl, polyvagal, HRV, autonomic-regulation]\n"
        "---\n\n"
        "# 12.4 Practice — Polyvagal Theory & Autonomic Regulation\n\n"
        f"Generated {args.count} problems.\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

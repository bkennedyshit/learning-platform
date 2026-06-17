#!/usr/bin/env python3
"""
12.1_conditioning.py — Practice problem generator for Chapter 12.1
(Classical & Operant Conditioning / Rescorla-Wagner).

Generates randomized drill problems across 6 archetypes:
  1. Single-CS Rescorla-Wagner acquisition (compute V after n trials)
  2. Blocking demonstration (compound conditioning)
  3. Extinction curve computation
  4. Operant Q-value update (bandit)
  5. Reinforcement schedule identification
  6. Matching Law calculation

Usage:
  python 12.1_conditioning.py
  python 12.1_conditioning.py --count 12 --seed 42
  python 12.1_conditioning.py --count 12 --seed 42 --out /tmp/_121.md
"""
from __future__ import annotations

import argparse
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
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_rw_acquisition(rng: random.Random) -> Problem:
    alpha = rng.choice([0.2, 0.3, 0.4, 0.5])
    beta = rng.choice([0.3, 0.4, 0.5, 0.6, 0.8])
    lam = 1.0
    n_trials = rng.randint(4, 10)
    eta = alpha * beta
    V = 0.0
    steps = []
    for t in range(1, n_trials + 1):
        delta = lam - V
        dV = eta * delta
        V_new = V + dV
        steps.append(f"Trial {t}: δ = {lam} − {V:.4f} = {delta:.4f}, "
                     f"ΔV = {eta} × {delta:.4f} = {dV:.4f}, V = {V_new:.4f}")
        V = V_new
    stmt = (
        f"A single CS is paired with a US over **{n_trials} trials**. "
        f"Parameters: α = {alpha}, β₁ = {beta}, λ = {lam}, V₀ = 0.\n\n"
        f"Compute V after each trial and verify with the closed form V_n = 1 − (1−αβ)^n."
    )
    closed = 1 - (1 - eta) ** n_trials
    sol = "\n\n".join(steps) + (
        f"\n\n**Closed form check:** V_{n_trials} = 1 − (1−{eta})^{n_trials} "
        f"= 1 − {(1-eta)**n_trials:.4f} = {closed:.4f} ✓"
    )
    return Problem("Rescorla-Wagner Acquisition", stmt, sol)


def gen_blocking(rng: random.Random) -> Problem:
    alpha_A = rng.choice([0.3, 0.4, 0.5])
    alpha_B = rng.choice([0.3, 0.4, 0.5])
    beta = rng.choice([0.4, 0.5, 0.6])
    phase1_trials = rng.randint(15, 25)
    phase2_trials = rng.randint(5, 10)
    eta_A = alpha_A * beta
    V_A = 1 - (1 - eta_A) ** phase1_trials
    V_B = 0.0
    lines = [f"After Phase 1 ({phase1_trials} trials): V_A = 1 − (1−{eta_A})^{phase1_trials} = {V_A:.4f}"]
    for t in range(1, phase2_trials + 1):
        delta = 1.0 - V_A - V_B
        dV_B = alpha_B * beta * delta
        V_B += dV_B
        V_A += alpha_A * beta * delta
        lines.append(f"Phase 2, Trial {t}: δ = {delta:.4f}, ΔV_B = {dV_B:.4f}, V_B = {V_B:.4f}")
    stmt = (
        f"Phase 1: CS_A alone paired with US for {phase1_trials} trials "
        f"(α_A={alpha_A}, β={beta}, λ=1).\n"
        f"Phase 2: Compound A+B paired with US for {phase2_trials} trials "
        f"(α_B={alpha_B}).\n\n"
        f"Show that B is blocked (V_B remains near 0)."
    )
    sol = "\n\n".join(lines) + f"\n\n**Conclusion:** V_B = {V_B:.4f} ≈ 0. B is blocked."
    return Problem("Blocking Demonstration", stmt, sol)


def gen_extinction(rng: random.Random) -> Problem:
    V0 = rng.choice([0.7, 0.8, 0.85, 0.9, 0.95])
    alpha = rng.choice([0.3, 0.4, 0.5])
    beta2 = rng.choice([0.2, 0.3, 0.4])
    n_trials = rng.randint(8, 15)
    decay = 1 - alpha * beta2
    V = V0
    lines = [f"Trial 0: V = {V:.4f}"]
    for t in range(1, n_trials + 1):
        V *= decay
        lines.append(f"Trial {t}: V = {V:.4f}")
    stmt = (
        f"After acquisition, V₀ = {V0}. The US is now omitted for {n_trials} extinction trials. "
        f"Parameters: α = {alpha}, β₂ = {beta2}.\n\n"
        f"Compute the extinction curve and the half-life."
    )
    import math
    half_life = -math.log(2) / math.log(decay)
    sol = "\n\n".join(lines) + (
        f"\n\n**Decay factor:** (1 − α·β₂) = {decay}\n\n"
        f"**Half-life:** n₁/₂ = −ln2 / ln({decay}) = {half_life:.2f} trials"
    )
    return Problem("Extinction Curve", stmt, sol)


def gen_operant_bandit(rng: random.Random) -> Problem:
    alpha = rng.choice([0.1, 0.15, 0.2])
    rewards = [rng.choice([-5, -3, -2, 1, 2, 3, 5]) for _ in range(6)]
    Q = 0.0
    lines = []
    for t, r in enumerate(rewards, 1):
        delta = r - Q
        Q_new = Q + alpha * delta
        lines.append(f"Trial {t}: R={r}, δ = {r} − {Q:.3f} = {delta:.3f}, "
                     f"Q = {Q:.3f} + {alpha}×{delta:.3f} = {Q_new:.3f}")
        Q = Q_new
    stmt = (
        f"An organism takes the same action 6 times receiving rewards: {rewards}. "
        f"Learning rate α = {alpha}, Q₀ = 0.\n\n"
        f"Compute Q after each trial using the bandit update Q ← Q + α(R − Q)."
    )
    sol = "\n\n".join(lines)
    return Problem("Operant Bandit Q-Update", stmt, sol)


def gen_schedule_id(rng: random.Random) -> Problem:
    schedules = [
        ("FR-5", "Every 5th lever press delivers food", "Fixed Ratio",
         "Post-reinforcement pause then rapid burst to 5 presses"),
        ("VR-10", "On average every 10th response, but unpredictable", "Variable Ratio",
         "Steady high-rate responding; most resistant to extinction"),
        ("FI-30s", "First response after 30 seconds is reinforced", "Fixed Interval",
         "Scallop pattern: slow start, accelerating near 30s mark"),
        ("VI-60s", "First response after average 60s (variable) is reinforced", "Variable Interval",
         "Steady moderate-rate responding"),
    ]
    name, desc, full_name, pattern = rng.choice(schedules)
    stmt = (
        f"A Skinner box delivers reinforcement with this rule: *\"{desc}\"*.\n\n"
        f"Identify the schedule type, give its abbreviation, and describe the expected cumulative response curve."
    )
    sol = (
        f"**Schedule:** {full_name} ({name})\n\n"
        f"**Response pattern:** {pattern}"
    )
    return Problem("Schedule Identification", stmt, sol)


def gen_matching_law(rng: random.Random) -> Problem:
    r1 = rng.randint(10, 50)
    r2 = rng.randint(10, 50)
    total_B = rng.randint(100, 500)
    B1 = round(total_B * r1 / (r1 + r2))
    B2 = total_B - B1
    stmt = (
        f"A pigeon on concurrent VI-VI schedules receives {r1} reinforcers/hr on key 1 "
        f"and {r2} reinforcers/hr on key 2. Total responses = {total_B}/hr.\n\n"
        f"Predict B₁ and B₂ using the strict Matching Law."
    )
    sol = (
        f"$$\\frac{{B_1}}{{B_1+B_2}} = \\frac{{r_1}}{{r_1+r_2}} = "
        f"\\frac{{{r1}}}{{{r1}+{r2}}} = {r1/(r1+r2):.3f}$$\n\n"
        f"B₁ = {total_B} × {r1/(r1+r2):.3f} = {B1}\n\n"
        f"B₂ = {total_B} − {B1} = {B2}"
    )
    return Problem("Matching Law", stmt, sol)


GENERATORS = [
    gen_rw_acquisition,
    gen_blocking,
    gen_extinction,
    gen_operant_bandit,
    gen_schedule_id,
    gen_matching_law,
]


def main():
    parser = argparse.ArgumentParser(description="12.1 Conditioning practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = []
    for i in range(args.count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))

    header = (
        "---\n"
        "tags: [review/psych-rl, conditioning, rescorla-wagner]\n"
        "---\n\n"
        "# 12.1 Practice — Classical & Operant Conditioning\n\n"
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

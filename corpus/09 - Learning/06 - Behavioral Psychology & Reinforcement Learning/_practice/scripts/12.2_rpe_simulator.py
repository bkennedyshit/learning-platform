#!/usr/bin/env python3
"""
12.2_rpe_simulator.py — Temporal-Difference RPE simulator matching Schultz 1997.

Simulates dopamine neuron firing patterns across three conditions:
  1. Unexpected reward (no CS, reward delivered)
  2. Expected reward (CS predicts reward, reward delivered)
  3. Omitted reward (CS predicts reward, reward withheld)

Also generates practice problems for computing TD errors.

Usage:
  python 12.2_rpe_simulator.py
  python 12.2_rpe_simulator.py --count 10 --seed 42
  python 12.2_rpe_simulator.py --count 10 --seed 42 --out /tmp/_122.md
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
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


def gen_td_error_single(rng: random.Random) -> Problem:
    V_s = rng.randint(0, 8)
    V_sp = rng.randint(0, 8)
    r = rng.choice([0, 1, 2, 5, 10])
    gamma = rng.choice([0.9, 0.95, 0.99])
    delta = r + gamma * V_sp - V_s
    stmt = (
        f"Compute the TD error δ for a transition with:\n"
        f"- V(s) = {V_s}, V(s') = {V_sp}, r = {r}, γ = {gamma}\n\n"
        f"State whether dopamine neurons would burst, pause, or maintain baseline."
    )
    if delta > 0:
        firing = "BURST (δ > 0, positive surprise)"
    elif delta < 0:
        firing = "PAUSE (δ < 0, disappointment)"
    else:
        firing = "BASELINE (δ = 0, fully predicted)"
    sol = (
        f"$$\\delta = r + \\gamma V(s') - V(s) = {r} + {gamma}({V_sp}) - {V_s} "
        f"= {r} + {gamma*V_sp:.2f} - {V_s} = {delta:.2f}$$\n\n"
        f"**Dopamine response:** {firing}"
    )
    return Problem("Single TD Error", stmt, sol)


def gen_episode_td(rng: random.Random) -> Problem:
    n_states = rng.randint(3, 5)
    values = [rng.randint(0, 6) for _ in range(n_states)] + [0]  # terminal = 0
    rewards = [0] * (n_states - 1) + [rng.choice([1, 3, 5, 10])]
    gamma = rng.choice([0.9, 0.95])
    alpha = rng.choice([0.1, 0.2])
    lines = []
    for t in range(n_states):
        delta = rewards[t] + gamma * values[t + 1] - values[t]
        new_v = values[t] + alpha * delta
        lines.append(
            f"t={t}: δ = {rewards[t]} + {gamma}×{values[t+1]} − {values[t]} = {delta:.2f}, "
            f"V(s_{t}) ← {values[t]} + {alpha}×{delta:.2f} = {new_v:.2f}"
        )
        values[t] = new_v
    stmt = (
        f"An agent traverses {n_states} states to a terminal state.\n"
        f"Initial values: {[f'V(s{i})={values[i]:.2f}' for i in range(n_states)]}\n"
        f"Rewards: {rewards}, γ={gamma}, α={alpha}.\n\n"
        f"Compute δ and updated V at each step."
    )
    sol = "\n\n".join(lines)
    return Problem("Episode TD Errors", stmt, sol)


def gen_signal_transfer(rng: random.Random) -> Problem:
    gamma = rng.choice([0.9, 0.95])
    alpha = rng.choice([0.15, 0.2, 0.25])
    n_trials = rng.randint(5, 8)
    V_cs, V_us = 0.0, 0.0
    lines = []
    for t in range(1, n_trials + 1):
        d_cs = 0 + gamma * V_us - V_cs
        V_cs_new = V_cs + alpha * d_cs
        d_us = 1 + 0 - V_us
        V_us_new = V_us + alpha * d_us
        lines.append(
            f"Trial {t}: δ_CS={d_cs:.3f}, δ_US={d_us:.3f}, "
            f"V(CS)={V_cs_new:.3f}, V(US)={V_us_new:.3f}"
        )
        V_cs, V_us = V_cs_new, V_us_new
    stmt = (
        f"Simulate {n_trials} CS→US conditioning trials (r=1 at US, γ={gamma}, α={alpha}).\n"
        f"Start: V(CS)=0, V(US)=0. Show the signal transfer from US to CS."
    )
    sol = "\n\n".join(lines) + (
        f"\n\n**Pattern:** δ_US decreases ({1.0:.1f}→{1-V_us:.3f}), "
        f"δ_CS rises then stabilizes. Burst transfers from US to CS."
    )
    return Problem("Signal Transfer Simulation", stmt, sol)


def gen_omission(rng: random.Random) -> Problem:
    V_cs = rng.choice([0.8, 0.85, 0.9, 0.95])
    V_us = rng.choice([0.9, 0.95, 1.0])
    gamma = rng.choice([0.9, 0.95])
    alpha = rng.choice([0.1, 0.2])
    d_cs = 0 + gamma * V_us - V_cs
    d_us_omit = 0 + 0 - V_us
    new_V_us = V_us + alpha * d_us_omit
    stmt = (
        f"After learning, V(CS)={V_cs}, V(US)={V_us}. On a probe trial, "
        f"the CS is presented but reward is **omitted**. γ={gamma}, α={alpha}.\n\n"
        f"Compute δ at CS time and at expected-reward time. What happens to V(US)?"
    )
    sol = (
        f"At CS: δ = 0 + {gamma}×{V_us} − {V_cs} = {d_cs:.3f} "
        f"({'small burst' if d_cs > 0.01 else 'baseline'})\n\n"
        f"At expected reward (omitted): δ = 0 + 0 − {V_us} = **{d_us_omit:.2f}** (PAUSE/DIP)\n\n"
        f"V(US) ← {V_us} + {alpha}×({d_us_omit:.2f}) = {new_V_us:.3f}\n\n"
        f"The large negative δ = {d_us_omit:.2f} corresponds to dopamine neurons "
        f"pausing below baseline — the neural signature of disappointment."
    )
    return Problem("Reward Omission (Negative RPE)", stmt, sol)


def gen_addiction_model(rng: random.Random) -> Problem:
    r_natural = rng.choice([1, 2])
    r_drug = rng.choice([8, 10, 15])
    alpha = rng.choice([0.1, 0.2])
    gamma = 0.9
    n = rng.randint(5, 10)
    V_nat = r_natural * gamma * (1 - (1 - alpha) ** n)
    V_drug = r_drug * gamma * (1 - (1 - alpha) ** n)
    stmt = (
        f"Compare value acquisition for natural reward (r={r_natural}) vs drug (r={r_drug}) "
        f"over {n} trials. α={alpha}, γ={gamma}.\n\n"
        f"Compute V(cue) for each and explain the policy distortion."
    )
    sol = (
        f"Natural: V_{{nat}} = {r_natural}×{gamma}×[1−(1−{alpha})^{n}] = "
        f"{r_natural*gamma:.1f}×{1-(1-alpha)**n:.4f} = {V_nat:.3f}\n\n"
        f"Drug: V_{{drug}} = {r_drug}×{gamma}×[1−(1−{alpha})^{n}] = "
        f"{r_drug*gamma:.1f}×{1-(1-alpha)**n:.4f} = {V_drug:.3f}\n\n"
        f"Ratio: V_drug/V_nat = {V_drug/V_nat:.1f}×\n\n"
        f"The policy becomes π*(s) = a_drug for all states because "
        f"Q(s, drug) >> Q(s, anything_else)."
    )
    return Problem("Addiction as Value Distortion", stmt, sol)


GENERATORS = [
    gen_td_error_single,
    gen_episode_td,
    gen_signal_transfer,
    gen_omission,
    gen_addiction_model,
]


def main():
    parser = argparse.ArgumentParser(description="12.2 RPE practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\n"
        "tags: [review/psych-rl, dopamine, reward-prediction-error, TD-learning]\n"
        "---\n\n"
        "# 12.2 Practice — Dopamine & Reward Prediction Error\n\n"
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

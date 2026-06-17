#!/usr/bin/env python3
"""
12.5_trauma_policy.py — RL agent demonstrating local-minimum lock-in from trauma.

Demonstrates:
  - Agent with extreme negative reward for 'trust' action
  - Local-minimum lock-in (avoidance trap)
  - Exploration-rate fix (therapy simulation)
  - Asymmetric learning rates (one betrayal undoes many positives)

Usage:
  python 12.5_trauma_policy.py
  python 12.5_trauma_policy.py --count 10 --seed 42
  python 12.5_trauma_policy.py --count 10 --seed 42 --out /tmp/_125.md
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


def simulate_bandit(n_trials, epsilon, alpha, p_pos, r_pos, r_neg, r_isolate, Q_trust_init=0, Q_iso_init=0, seed=None):
    """Simulate a 2-armed bandit (trust vs isolate)."""
    rng = random.Random(seed)
    Q_t, Q_i = Q_trust_init, Q_iso_init
    history = []
    for t in range(n_trials):
        if rng.random() < epsilon:
            action = rng.choice(["trust", "isolate"])
        else:
            action = "trust" if Q_t > Q_i else "isolate"
        if action == "trust":
            r = r_pos if rng.random() < p_pos else r_neg
            Q_t += alpha * (r - Q_t)
        else:
            r = r_isolate
            Q_i += alpha * (r - Q_i)
        history.append((t, action, r, Q_t, Q_i))
    return history


def gen_avoidance_trap(rng: random.Random) -> Problem:
    alpha = rng.choice([0.1, 0.15])
    epsilon = rng.choice([0.03, 0.05, 0.08])
    p_pos = rng.choice([0.15, 0.2, 0.25])
    r_pos, r_neg, r_iso = 3, -5, 1
    n = 50
    hist = simulate_bandit(n, epsilon, alpha, p_pos, r_pos, r_neg, r_iso, seed=rng.randint(0, 9999))
    final_Qt = hist[-1][3]
    final_Qi = hist[-1][4]
    trust_count = sum(1 for h in hist if h[1] == "trust")
    stmt = (
        f"Simulate {n} trials of a trauma-environment bandit:\n"
        f"- R(trust): +{r_pos} w.p. {p_pos}, {r_neg} w.p. {1-p_pos}\n"
        f"- R(isolate): +{r_iso} (certain)\n"
        f"- α={alpha}, ε={epsilon}\n\n"
        f"Show that the agent becomes trapped in avoidance."
    )
    sol = (
        f"After {n} trials:\n"
        f"- Trust attempted: {trust_count} times ({trust_count/n*100:.0f}%)\n"
        f"- Q(trust) = {final_Qt:.2f}\n"
        f"- Q(isolate) = {final_Qi:.2f}\n"
        f"- Gap: {final_Qi - final_Qt:.2f}\n\n"
        f"E[R|trust] = {p_pos}×{r_pos} + {1-p_pos}×{r_neg} = {p_pos*r_pos + (1-p_pos)*r_neg:.2f}\n"
        f"E[R|isolate] = {r_iso}\n\n"
        f"Agent is trapped: Q(trust) << Q(isolate), exploration too low to recover."
    )
    return Problem("Avoidance Trap Formation", stmt, sol)


def gen_exploration_fix(rng: random.Random) -> Problem:
    Q_trust_init = rng.choice([-3.0, -2.5, -2.0])
    Q_iso = 1.0
    alpha = 0.1
    eps_low = 0.05
    eps_high = rng.choice([0.20, 0.25, 0.30])
    p_pos_safe = rng.choice([0.80, 0.85, 0.90])
    r_pos, r_neg, r_iso = 5, -2, 1
    E_r = p_pos_safe * r_pos + (1 - p_pos_safe) * r_neg
    gap = Q_iso - Q_trust_init
    update_per_attempt = alpha * (E_r - Q_trust_init)
    attempts_low = gap / update_per_attempt
    trials_low = attempts_low / (eps_low / 2)
    attempts_high = gap / update_per_attempt
    trials_high = attempts_high / (eps_high / 2)
    stmt = (
        f"Agent in SAFE environment. Q(trust)={Q_trust_init}, Q(isolate)={Q_iso}.\n"
        f"Safe env: R(trust)=+{r_pos} w.p. {p_pos_safe}, {r_neg} w.p. {1-p_pos_safe}. α={alpha}.\n\n"
        f"Compare recovery time with ε={eps_low} (no therapy) vs ε={eps_high} (therapy)."
    )
    sol = (
        f"E[R|trust] in safe env = {E_r:.2f}\n"
        f"Gap to close: {Q_iso} − ({Q_trust_init}) = {gap:.1f}\n"
        f"Update per trust attempt: α×(E[R]−Q) = {alpha}×({E_r:.2f}−{Q_trust_init}) = {update_per_attempt:.3f}\n"
        f"Attempts needed: {gap:.1f}/{update_per_attempt:.3f} = {attempts_low:.1f}\n\n"
        f"**Without therapy (ε={eps_low}):** {attempts_low:.1f} attempts ÷ {eps_low/2:.3f} rate = "
        f"**{trials_low:.0f} interactions**\n\n"
        f"**With therapy (ε={eps_high}):** {attempts_high:.1f} attempts ÷ {eps_high/2:.3f} rate = "
        f"**{trials_high:.0f} interactions**\n\n"
        f"Speedup: {trials_low/trials_high:.1f}×"
    )
    return Problem("Exploration Rate Fix (Therapy)", stmt, sol)


def gen_betrayal_damage(rng: random.Random) -> Problem:
    Q_before = rng.choice([1.5, 2.0, 2.5, 3.0])
    r_betrayal = rng.choice([-8, -10, -12])
    alpha_neg = rng.choice([0.4, 0.5, 0.6])
    alpha_pos = 0.1
    r_pos = 5
    Q_after = Q_before + alpha_neg * (r_betrayal - Q_before)
    n_to_recover = (Q_before - Q_after) / (alpha_pos * (r_pos - Q_after))
    stmt = (
        f"After months of therapy, Q(trust) = {Q_before} (above Q(isolate)=1.0).\n"
        f"A betrayal occurs: r = {r_betrayal}. Trauma-sensitized α⁻ = {alpha_neg}.\n\n"
        f"Compute damage and recovery time (α⁺={alpha_pos}, r_positive={r_pos})."
    )
    sol = (
        f"Q(trust) ← {Q_before} + {alpha_neg}×({r_betrayal} − {Q_before}) = "
        f"{Q_before} + {alpha_neg}×{r_betrayal - Q_before:.1f} = **{Q_after:.2f}**\n\n"
        f"Damage: {Q_before} → {Q_after:.2f} (Δ = {Q_after - Q_before:.2f})\n\n"
        f"Recovery per positive: α⁺×(r⁺ − Q) = {alpha_pos}×({r_pos}−{Q_after:.2f}) = "
        f"{alpha_pos * (r_pos - Q_after):.3f}\n\n"
        f"Positives needed to return to {Q_before}: "
        f"{Q_before - Q_after:.2f}/{alpha_pos * (r_pos - Q_after):.3f} = **{n_to_recover:.0f}**\n\n"
        f"One betrayal = {n_to_recover:.0f} positive experiences. "
        f"This is the asymmetric learning rate problem."
    )
    return Problem("Betrayal Damage (Asymmetric α)", stmt, sol)


def gen_graduated_exposure(rng: random.Random) -> Problem:
    Q_init = rng.choice([-3.0, -2.5, -2.0])
    alpha = 0.1
    levels = [
        ("State preference", 0.95, 1, -0.5),
        ("Ask small favor", 0.90, 2, -1),
        ("Share feeling", 0.85, 3, -2),
        ("Express need", 0.80, 4, -3),
        ("Full vulnerability", 0.80, 5, -5),
    ]
    trials_per_level = rng.choice([8, 10, 12])
    Q = Q_init
    lines = [f"Start: Q = {Q:.2f}"]
    for name, p, rp, rn in levels:
        E_r = p * rp + (1 - p) * rn
        for _ in range(trials_per_level):
            Q += alpha * (E_r - Q)
        lines.append(f"After Level '{name}' ({trials_per_level} trials, E[R]={E_r:.2f}): Q = {Q:.2f}")
    stmt = (
        f"Design graduated exposure: 5 levels, {trials_per_level} trials each.\n"
        f"Start Q(trust) = {Q_init}. α = {alpha}.\n\n"
        f"Show Q-value progression through the hierarchy."
    )
    sol = "\n\n".join(lines) + f"\n\nFinal Q = {Q:.2f} (above Q(isolate)=1.0 ✓)"
    return Problem("Graduated Exposure Hierarchy", stmt, sol)


GENERATORS = [gen_avoidance_trap, gen_exploration_fix, gen_betrayal_damage, gen_graduated_exposure]


def main():
    parser = argparse.ArgumentParser(description="12.5 Trauma policy practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\n"
        "tags: [review/psych-rl, trauma, avoidance, exploration-rate, C-PTSD]\n"
        "---\n\n"
        "# 12.5 Practice — Trauma Adaptations as Reinforcement Learning\n\n"
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

#!/usr/bin/env python3
"""
12.6_rlhf_skeleton.py — Minimal RLHF reward model + PPO update skeleton.

Demonstrates:
  - Bradley-Terry preference model and reward model training
  - PPO clipped surrogate objective computation
  - KL penalty calculation
  - Preference-pair scoring

Usage:
  python 12.6_rlhf_skeleton.py
  python 12.6_rlhf_skeleton.py --count 10 --seed 42
  python 12.6_rlhf_skeleton.py --count 10 --seed 42 --out /tmp/_126.md
"""
from __future__ import annotations

import argparse
import math
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


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def gen_bt_loss(rng: random.Random) -> Problem:
    n_pairs = rng.randint(3, 5)
    pairs = [(round(rng.uniform(-1, 4), 1), round(rng.uniform(-2, 3), 1)) for _ in range(n_pairs)]
    # Ensure r_w > r_l for most pairs
    pairs = [(max(a, b), min(a, b)) if rng.random() < 0.8 else (a, b) for a, b in pairs]
    lines = []
    total_loss = 0
    for i, (rw, rl) in enumerate(pairs):
        dr = rw - rl
        sig = sigmoid(dr)
        loss = -math.log(sig) if sig > 0 else float('inf')
        total_loss += loss
        lines.append(f"Pair {i+1}: r_w={rw}, r_l={rl}, Δr={dr:.1f}, σ(Δr)={sig:.4f}, L=−log({sig:.4f})={loss:.4f}")
    avg_loss = total_loss / n_pairs
    stmt = (
        f"Compute the Bradley-Terry reward model loss for {n_pairs} preference pairs:\n\n"
        + "\n".join(f"- Pair {i+1}: r(y_w)={rw}, r(y_l)={rl}" for i, (rw, rl) in enumerate(pairs))
    )
    sol = "\n\n".join(lines) + f"\n\n**Average loss:** {total_loss:.4f}/{n_pairs} = {avg_loss:.4f}"
    return Problem("Bradley-Terry Loss", stmt, sol)


def gen_ppo_clip(rng: random.Random) -> Problem:
    pi_old = round(rng.uniform(0.1, 0.6), 2)
    pi_new = round(rng.uniform(0.1, 0.9), 2)
    A_hat = round(rng.uniform(-3, 3), 1)
    eps = rng.choice([0.1, 0.2, 0.3])
    ratio = pi_new / pi_old
    clipped_ratio = max(1 - eps, min(1 + eps, ratio))
    L_unclip = ratio * A_hat
    L_clip = clipped_ratio * A_hat
    L_ppo = min(L_unclip, L_clip) if A_hat >= 0 else max(L_unclip, L_clip)
    # Actually PPO takes min always
    L_ppo = min(L_unclip, L_clip)
    stmt = (
        f"π_old(a|s) = {pi_old}, π_θ(a|s) = {pi_new}, Â = {A_hat}, ε = {eps}.\n\n"
        f"Compute the PPO clipped surrogate objective."
    )
    sol = (
        f"Ratio: r(θ) = {pi_new}/{pi_old} = {ratio:.3f}\n\n"
        f"Clip bounds: [{1-eps}, {1+eps}]\n\n"
        f"Clipped ratio: clip({ratio:.3f}, {1-eps}, {1+eps}) = {clipped_ratio:.3f}\n\n"
        f"Unclipped: {ratio:.3f} × {A_hat} = {L_unclip:.3f}\n\n"
        f"Clipped: {clipped_ratio:.3f} × {A_hat} = {L_clip:.3f}\n\n"
        f"L^CLIP = min({L_unclip:.3f}, {L_clip:.3f}) = **{L_ppo:.3f}**\n\n"
        f"{'Clipping active (ratio exceeded bounds)' if abs(ratio - clipped_ratio) > 0.001 else 'No clipping needed (ratio within bounds)'}"
    )
    return Problem("PPO Clipped Objective", stmt, sol)


def gen_kl_divergence(rng: random.Random) -> Problem:
    n = rng.choice([3, 4, 5])
    # Generate two distributions
    raw_theta = [rng.uniform(0.5, 3) for _ in range(n)]
    raw_ref = [rng.uniform(0.5, 3) for _ in range(n)]
    s_theta = sum(raw_theta)
    s_ref = sum(raw_ref)
    pi_theta = [round(x / s_theta, 3) for x in raw_theta]
    pi_ref = [round(x / s_ref, 3) for x in raw_ref]
    # Normalize to sum to 1
    pi_theta[-1] = round(1 - sum(pi_theta[:-1]), 3)
    pi_ref[-1] = round(1 - sum(pi_ref[:-1]), 3)
    kl = sum(p * math.log(p / q) for p, q in zip(pi_theta, pi_ref) if p > 0 and q > 0)
    beta = rng.choice([0.1, 0.2, 0.5, 1.0])
    r = round(rng.uniform(1, 8), 1)
    penalized = r - beta * kl
    stmt = (
        f"π_θ = {pi_theta}, π_ref = {pi_ref}.\n"
        f"Compute D_KL(π_θ || π_ref). Then compute penalized reward with r={r}, β={beta}."
    )
    terms = [f"{p}×log({p}/{q})={p}×{math.log(p/q):.4f}={p*math.log(p/q):.4f}"
             for p, q in zip(pi_theta, pi_ref) if p > 0 and q > 0]
    sol = (
        "D_KL = " + " + ".join(terms) + f" = **{kl:.4f}** nats\n\n"
        f"Penalized reward: {r} − {beta}×{kl:.4f} = {r} − {beta*kl:.4f} = **{penalized:.4f}**"
    )
    return Problem("KL Divergence & Penalty", stmt, sol)


def gen_reward_ranking(rng: random.Random) -> Problem:
    n_responses = rng.randint(4, 6)
    rewards = sorted([round(rng.uniform(-2, 6), 2) for _ in range(n_responses)], reverse=True)
    rng.shuffle(rewards)
    correct_order = sorted(range(n_responses), key=lambda i: rewards[i], reverse=True)
    stmt = (
        f"A reward model assigns scores to {n_responses} responses:\n\n"
        + "\n".join(f"- Response {chr(65+i)}: r = {rewards[i]}" for i in range(n_responses))
        + "\n\nRank them and compute P(A ≻ B) for the top two."
    )
    top2 = correct_order[:2]
    dr = rewards[top2[0]] - rewards[top2[1]]
    p = sigmoid(dr)
    ranking = " > ".join(chr(65 + i) for i in correct_order)
    sol = (
        f"Ranking (best to worst): {ranking}\n\n"
        f"P({chr(65+top2[0])} ≻ {chr(65+top2[1])}) = σ({rewards[top2[0]]} − {rewards[top2[1]]}) "
        f"= σ({dr:.2f}) = {p:.4f}"
    )
    return Problem("Reward Model Ranking", stmt, sol)


def gen_coreg_rlhf(rng: random.Random) -> Problem:
    behaviors = ["share feelings", "deflect", "intellectualize", "withdraw"]
    pi_init = [0.05, 0.30, 0.45, 0.20]
    # Simulate preference-based updates
    # Therapist prefers: share > deflect > intellectualize > withdraw
    target_rewards = [4.0, 2.0, 1.0, -1.0]
    alpha = rng.choice([0.1, 0.15, 0.2])
    n_sessions = rng.randint(4, 8)
    pi = list(pi_init)
    lines = [f"Session 0: π = {[round(p,3) for p in pi]}"]
    for s in range(1, n_sessions + 1):
        # Softmax update toward target rewards
        logits = [math.log(p + 1e-8) + alpha * r for p, r in zip(pi, target_rewards)]
        exp_l = [math.exp(l) for l in logits]
        total = sum(exp_l)
        pi = [e / total for e in exp_l]
        lines.append(f"Session {s}: π = {[round(p,3) for p in pi]}")
    kl = sum(p * math.log(p / q) for p, q in zip(pi, pi_init) if p > 0 and q > 0)
    stmt = (
        f"Model therapy as RLHF. Client's initial policy over behaviors:\n"
        f"{dict(zip(behaviors, [round(p,2) for p in pi_init]))}\n\n"
        f"Therapist's implicit reward: share=4, deflect=2, intellectualize=1, withdraw=−1.\n"
        f"Update rate α={alpha}. Simulate {n_sessions} sessions."
    )
    sol = "\n\n".join(lines) + f"\n\nKL from initial: {kl:.3f} nats"
    return Problem("Co-Regulation as RLHF", stmt, sol)


GENERATORS = [gen_bt_loss, gen_ppo_clip, gen_kl_divergence, gen_reward_ranking, gen_coreg_rlhf]


def main():
    parser = argparse.ArgumentParser(description="12.6 RLHF practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\n"
        "tags: [review/psych-rl, RLHF, PPO, reward-model, preference-learning]\n"
        "---\n\n"
        "# 12.6 Practice — RLHF: Reinforcement Learning from Human Feedback\n\n"
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

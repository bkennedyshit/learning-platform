#!/usr/bin/env python3
"""
4.1_game_loop.py — Practice problem generator for Chapter 4.1
(Game Loop & Architecture).

Generates randomized drill problems across 4 archetypes:
  1. Frame budget calculation (target FPS → ms budget)
  2. Fixed timestep accumulator simulation
  3. ECS vs OOP cache performance estimation
  4. Object pool sizing

Usage:
  python 4.1_game_loop.py
  python 4.1_game_loop.py --count 12 --seed 42
"""

from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_frame_budget(rng: random.Random) -> Problem:
    fps = rng.choice([30, 60, 72, 90, 120, 144, 240])
    budget_ms = 1000.0 / fps
    physics_hz = rng.choice([30, 50, 60, 120])
    physics_dt = 1000.0 / physics_hz

    stmt = (
        f"Your game targets **{fps} FPS** with physics at **{physics_hz} Hz**.\n\n"
        f"1. What is the per-frame budget in milliseconds?\n"
        f"2. How many physics steps run per frame on average?\n"
        f"3. If GPU rendering takes {budget_ms * 0.6:.1f}ms, how much CPU budget remains?"
    )
    avg_physics = physics_hz / fps
    cpu_budget = budget_ms - budget_ms * 0.6  # Assuming parallel, this is wrong — explain
    sol = (
        f"1. Frame budget = $1000 / {fps} = {budget_ms:.2f}$ ms\n\n"
        f"2. Physics steps/frame = ${physics_hz} / {fps} = {avg_physics:.3f}$ average\n"
        f"   (accumulator pattern: some frames 0 steps, some frames 1 step)\n\n"
        f"3. With CPU-GPU parallelism: frame time = max(CPU, GPU).\n"
        f"   GPU = {budget_ms * 0.6:.1f}ms. CPU budget = {budget_ms:.2f}ms independently.\n"
        f"   Both must be ≤ {budget_ms:.2f}ms. CPU has full {budget_ms:.2f}ms budget\n"
        f"   (they run in parallel, not sequentially)."
    )
    return Problem("Frame Budget Calculation", stmt, sol)


def gen_accumulator(rng: random.Random) -> Problem:
    fixed_dt = rng.choice([0.01, 0.016667, 0.02, 0.033333])
    frame_times = [rng.uniform(0.014, 0.025) for _ in range(5)]

    stmt = (
        f"Fixed timestep = **{fixed_dt*1000:.2f}ms**. "
        f"The following frame times occur in sequence:\n\n"
        f"| Frame | Δt (ms) |\n|---|---|\n"
        + "\n".join(f"| {i+1} | {ft*1000:.2f} |" for i, ft in enumerate(frame_times))
        + "\n\nFor each frame, compute: accumulator value after adding Δt, "
        "number of physics steps, and remaining accumulator."
    )

    lines = []
    acc = 0.0
    for i, ft in enumerate(frame_times):
        acc += ft
        steps = 0
        while acc >= fixed_dt:
            acc -= fixed_dt
            steps += 1
        lines.append(
            f"Frame {i+1}: acc = {(acc + steps * fixed_dt)*1000:.2f}ms → "
            f"{steps} step(s) → remaining = {acc*1000:.2f}ms"
        )

    sol = "\n\n".join(lines)
    return Problem("Accumulator Simulation", stmt, sol)


def gen_pool_sizing(rng: random.Random) -> Problem:
    spawn_rate = rng.randint(50, 500)
    lifetime = rng.uniform(0.5, 5.0)
    headroom = rng.choice([1.1, 1.2, 1.5])

    max_active = spawn_rate * lifetime
    pool_size = int(max_active * headroom)

    stmt = (
        f"A particle system spawns **{spawn_rate} particles/second**. "
        f"Each particle lives **{lifetime:.1f} seconds**. "
        f"You want **{int((headroom-1)*100)}% headroom**.\n\n"
        f"1. What is the maximum number of simultaneously active particles?\n"
        f"2. What pool size should you allocate?\n"
        f"3. How much memory does the pool use if each particle is 64 bytes?"
    )
    mem_kb = pool_size * 64 / 1024
    sol = (
        f"1. Max active = spawn_rate × lifetime = {spawn_rate} × {lifetime:.1f} = "
        f"**{max_active:.0f}** particles\n\n"
        f"2. Pool size = {max_active:.0f} × {headroom} = **{pool_size}** objects\n\n"
        f"3. Memory = {pool_size} × 64 bytes = {pool_size * 64:,} bytes = "
        f"**{mem_kb:.1f} KB**"
    )
    return Problem("Object Pool Sizing", stmt, sol)


ARCHETYPES = [gen_frame_budget, gen_accumulator, gen_pool_sizing]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [game-dev, game-loop, practice, \"review/gamedev/4.1\"]\n"
        "chapter: 4.1\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../4.1 - Game Loop & Architecture|Chapter 4.1]] | "
        "Part of [[../../09 - Learning Index|Learning Index]]*\n\n"
        "# Chapter 4.1 — Practice Drills: Game Loop & Architecture\n\n"
        "> Auto-generated by `scripts/4.1_game_loop.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "4.1_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

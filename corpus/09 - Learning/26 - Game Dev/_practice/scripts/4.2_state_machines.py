#!/usr/bin/env python3
"""
4.2_state_machines.py — Practice problem generator for Chapter 4.2
(Gameplay Programming: Input, State, AI).

Generates randomized drill problems across 4 archetypes:
  1. FSM transition table design
  2. Behavior tree evaluation trace
  3. A* pathfinding on small grids
  4. Utility AI score calculation

Usage:
  python 4.2_state_machines.py
  python 4.2_state_machines.py --count 12 --seed 42
"""

from __future__ import annotations
import argparse
import heapq
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


def gen_fsm_design(rng: random.Random) -> Problem:
    scenarios = [
        ("door", ["Closed", "Opening", "Open", "Closing"],
         [("Closed", "interact", "Opening"), ("Opening", "anim_done", "Open"),
          ("Open", "interact", "Closing"), ("Closing", "anim_done", "Closed")]),
        ("enemy", ["Idle", "Patrol", "Chase", "Attack", "Dead"],
         [("Idle", "timer_expired", "Patrol"), ("Patrol", "see_player", "Chase"),
          ("Chase", "in_range", "Attack"), ("Chase", "lost_player", "Patrol"),
          ("Attack", "out_of_range", "Chase"), ("Attack", "health<=0", "Dead"),
          ("Patrol", "health<=0", "Dead"), ("Chase", "health<=0", "Dead")]),
    ]
    name, states, transitions = rng.choice(scenarios)
    
    stmt = (
        f"Design an FSM for a **{name}** with states: {', '.join(states)}.\n\n"
        f"List all valid transitions as (FromState, Condition, ToState) tuples.\n"
        f"How many transitions are there? What is the maximum possible for {len(states)} states?"
    )
    
    table = "\n".join(f"- {s1} → {s2} (on: {cond})" for s1, cond, s2 in transitions)
    max_trans = len(states) * (len(states) - 1)
    sol = (
        f"**Transitions:**\n\n{table}\n\n"
        f"**Count:** {len(transitions)} transitions\n\n"
        f"**Maximum possible:** {len(states)} × ({len(states)}-1) = {max_trans} "
        f"(every state can transition to every other state)"
    )
    return Problem("FSM Design", stmt, sol)


def gen_astar(rng: random.Random) -> Problem:
    size = 5
    grid = [[0] * size for _ in range(size)]
    # Add some walls
    num_walls = rng.randint(3, 6)
    for _ in range(num_walls):
        wx, wy = rng.randint(1, size - 2), rng.randint(1, size - 2)
        grid[wy][wx] = 1
    # Ensure start and goal are clear
    grid[0][0] = 0
    grid[size - 1][size - 1] = 0

    # Solve with A*
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start, goal = (0, 0), (size - 1, size - 1)
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < size and 0 <= ny < size and grid[ny][nx] == 0:
                ng = g_score[current] + 1
                if (nx, ny) not in g_score or ng < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = ng
                    f = ng + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

    # Reconstruct path
    path = []
    if goal in came_from or goal == start:
        node = goal
        while node != start:
            path.append(node)
            node = came_from.get(node, start)
        path.append(start)
        path.reverse()

    grid_str = ""
    for y in range(size):
        row = ""
        for x in range(size):
            if (x, y) in path:
                row += "★ "
            elif grid[y][x] == 1:
                row += "█ "
            else:
                row += "· "
        grid_str += row + "\n"

    stmt = (
        f"Find the shortest path from (0,0) to ({size-1},{size-1}) using A* "
        f"(Manhattan heuristic, cardinal moves only):\n\n```\n{grid_str}```\n"
        f"(█ = wall, · = walkable)\n\n"
        f"List the path coordinates and total cost."
    )

    if path:
        path_str = " → ".join(f"({x},{y})" for x, y in path)
        sol = f"**Path:** {path_str}\n\n**Cost:** {len(path) - 1} steps"
    else:
        sol = "**No path exists** (goal is unreachable)."

    return Problem("A* Pathfinding", stmt, sol)


def gen_utility_ai(rng: random.Random) -> Problem:
    health = rng.uniform(0.1, 1.0)
    dist = rng.uniform(2.0, 30.0)
    has_potion = rng.choice([True, False])
    visible = rng.choice([True, False])

    # Score functions
    def score_chase():
        if not visible: return 0.0
        return health * max(0, 1.0 - dist / 20.0) * 0.9

    def score_flee():
        if health > 0.3: return 0.0
        return (1.0 - health) * 0.95

    def score_potion():
        if not has_potion or health > 0.7: return 0.0
        return (1.0 - health) * 0.85

    def score_patrol():
        if visible: return 0.0
        return 0.5

    scores = {
        "Chase": score_chase(),
        "Flee": score_flee(),
        "Use Potion": score_potion(),
        "Patrol": score_patrol(),
    }
    best = max(scores, key=scores.get)

    stmt = (
        f"An enemy NPC has:\n"
        f"- Health: {health:.0%}\n"
        f"- Distance to player: {dist:.1f}m\n"
        f"- Has potion: {has_potion}\n"
        f"- Player visible: {visible}\n\n"
        f"Score functions:\n"
        f"- Chase: visible × health × max(0, 1-dist/20) × 0.9\n"
        f"- Flee: (health≤0.3) × (1-health) × 0.95\n"
        f"- Potion: (has_potion ∧ health≤0.7) × (1-health) × 0.85\n"
        f"- Patrol: (!visible) × 0.5\n\n"
        f"Which action does the Utility AI select?"
    )

    score_lines = "\n".join(f"- {k}: {v:.3f}" for k, v in scores.items())
    sol = f"**Scores:**\n\n{score_lines}\n\n**Selected:** {best} (score = {scores[best]:.3f})"
    return Problem("Utility AI Scoring", stmt, sol)


ARCHETYPES = [gen_fsm_design, gen_astar, gen_utility_ai]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [game-dev, FSM, AI, pathfinding, practice, \"review/gamedev/4.2\"]\n"
        "chapter: 4.2\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../4.2 - Gameplay Programming - Input, State, AI|Chapter 4.2]] | "
        "Part of [[../../09 - Learning Index|Learning Index]]*\n\n"
        "# Chapter 4.2 — Practice Drills: State Machines & AI\n\n"
        "> Auto-generated by `scripts/4.2_state_machines.py`.\n\n"
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
    out_path = args.out or (Path(__file__).resolve().parent.parent / "4.2_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

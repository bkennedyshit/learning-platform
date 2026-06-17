#!/usr/bin/env python3
"""
11.5_root_locus.py — Practice problem generator for Chapter 11.5
(Root Locus Analysis).

Archetypes:
  1. Identify real-axis segments
  2. Compute asymptote angles and centroid
  3. Find breakaway points
  4. Compute jω-axis crossing gain
  5. Departure angle from complex pole

Usage:
  python 11.5_root_locus.py --count 10 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

s = sp.Symbol('s')

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_asymptotes(rng: random.Random) -> Problem:
    n = rng.choice([3, 4])
    poles = sorted([-rng.randint(0, 8) for _ in range(n)])
    m = rng.choice([0, 1])
    zeros = sorted([-rng.randint(1, 6) for _ in range(m)]) if m > 0 else []
    diff = n - m
    angles = [(2*k+1)*180/diff for k in range(diff)]
    centroid = (sum(poles) - sum(zeros)) / diff
    poles_str = ", ".join(str(p) for p in poles)
    zeros_str = ", ".join(str(z) for z in zeros) if zeros else "none"
    stmt = (f"For $G(s)H(s)$ with poles at $s = {{{poles_str}}}$ and zeros at $s = {{{zeros_str}}}$, "
            "find the asymptote angles and centroid.")
    sol = (f"$n - m = {diff}$\n\n"
           f"Angles: ${', '.join(f'{a:.1f}°' for a in angles)}$\n\n"
           f"Centroid: $\\sigma_a = ({sum(poles)} - {sum(zeros)})/{diff} = {centroid:.3f}$")
    return Problem("Asymptotes (angles & centroid)", stmt, sol)

def gen_real_axis(rng: random.Random) -> Problem:
    poles = sorted([-rng.randint(0, 7) for _ in range(3)], reverse=True)
    stmt = (f"Determine which segments of the real axis are on the root locus for "
            f"poles at $s = {poles[0]}, {poles[1]}, {poles[2]}$ (no zeros).")
    # Count poles to the right of each segment
    segments = []
    test_points = [(poles[0]+1, "right of "+str(poles[0])),
                   ((poles[0]+poles[1])/2, f"between {poles[0]} and {poles[1]}"),
                   ((poles[1]+poles[2])/2, f"between {poles[1]} and {poles[2]}"),
                   (poles[2]-1, f"left of {poles[2]}")]
    for pt, desc in test_points:
        count = sum(1 for p in poles if p > pt)
        on_locus = count % 2 == 1
        segments.append(f"- {desc}: {count} poles to right → {'ON' if on_locus else 'NOT on'} locus")
    sol = "\n".join(segments)
    stmt_full = stmt
    return Problem("Real-axis locus segments", stmt_full, sol)

def gen_breakaway(rng: random.Random) -> Problem:
    p1 = 0
    p2 = -rng.randint(2, 8)
    # K = -s(s-p2) on real axis between p2 and 0
    # dK/ds = -(2s - p2) = 0 => s = p2/2
    breakaway = (p1 + p2) / 2
    stmt = (f"Find the breakaway point for $G(s) = K/(s(s+{-p2}))$.")
    sol = (f"$K = -s(s+{-p2})$ on real axis. $dK/ds = -(2s+{-p2}) = 0$\n\n"
           f"$s = {breakaway}$ (midpoint between poles at $0$ and ${p2}$)")
    return Problem("Breakaway point", stmt, sol)

def gen_jw_crossing(rng: random.Random) -> Problem:
    a = rng.randint(2, 8)
    b = rng.randint(1, 6)
    # s^3 + a*s^2 + b*s + K = 0, crossing at K = a*b
    K_crit = a * b
    omega = math.sqrt(b)
    stmt = (f"Find the gain $K$ at which the root locus of $G(s) = K/(s(s+{a-b+b}))$... "
            f"Actually: char eq $s^3 + {a}s^2 + {b}s + K = 0$. Find $K$ for $j\\omega$-axis crossing.")
    sol = (f"Routh $s^1$: $({a}\\cdot{b} - K)/{a} = 0 \\Rightarrow K = {K_crit}$\n\n"
           f"Auxiliary: ${a}s^2 + {K_crit} = 0 \\Rightarrow s = \\pm j\\sqrt{{{b}}} = \\pm j{omega:.3f}$")
    return Problem("jω-axis crossing", stmt, sol)

GENERATORS = [gen_asymptotes, gen_real_axis, gen_breakaway, gen_jw_crossing]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.5 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, root-locus]\n"
              "type: practice\n---\n# 11.5 Practice — Root Locus Analysis\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

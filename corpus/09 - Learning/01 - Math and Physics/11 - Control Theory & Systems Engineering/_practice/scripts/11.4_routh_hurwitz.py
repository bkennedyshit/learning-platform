#!/usr/bin/env python3
"""
11.4_routh_hurwitz.py — Practice problem generator for Chapter 11.4
(Stability & Routh-Hurwitz Criterion).

Archetypes:
  1. Build Routh array, count sign changes
  2. Necessary condition check (missing/negative coefficients)
  3. Find gain range K for stability
  4. Special case: zero in first column
  5. Special case: row of zeros (auxiliary polynomial)
  6. Relative stability (shifted axis)

Usage:
  python 11.4_routh_hurwitz.py --count 10 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from pathlib import Path
import sympy as sp

s = sp.Symbol('s')
K = sp.Symbol('K', positive=True)

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def build_routh(coeffs):
    """Build Routh array from polynomial coefficients [a_n, a_{n-1}, ..., a_0]."""
    n = len(coeffs) - 1
    cols = (n + 2) // 2
    arr = [[sp.S.Zero]*cols for _ in range(n+1)]
    for i, c in enumerate(coeffs):
        arr[i % 2 == 0 and 0 or 1][i // 2] = sp.S(c) if i < len(coeffs) else sp.S.Zero
    # Fill first two rows
    arr[0] = [sp.S(coeffs[i]) if i < len(coeffs) else sp.S.Zero for i in range(0, len(coeffs), 2)]
    arr[1] = [sp.S(coeffs[i]) if i < len(coeffs) else sp.S.Zero for i in range(1, len(coeffs), 2)]
    # Pad
    max_cols = max(len(arr[0]), len(arr[1]))
    arr[0] += [sp.S.Zero] * (max_cols - len(arr[0]))
    arr[1] += [sp.S.Zero] * (max_cols - len(arr[1]))
    for i in range(2, n+1):
        arr[i] = [sp.S.Zero] * max_cols
        for j in range(max_cols - 1):
            if arr[i-1][0] == 0:
                return arr, "zero_first_col"
            arr[i][j] = (arr[i-1][0]*arr[i-2][j+1] - arr[i-2][0]*arr[i-1][j+1]) / arr[i-1][0]
    return arr, "ok"

def gen_routh_basic(rng: random.Random) -> Problem:
    # Generate a 3rd or 4th order polynomial
    order = rng.choice([3, 4])
    coeffs = [1] + [rng.randint(1, 8) for _ in range(order)]
    poly_str = " + ".join(f"{c}s^{order-i}" if order-i > 1 else (f"{c}s" if order-i == 1 else str(c))
                          for i, c in enumerate(coeffs) if c != 0)
    poly_sym = sum(c * s**(order-i) for i, c in enumerate(coeffs))
    roots = sp.solve(poly_sym, s)
    rhp = sum(1 for r in roots if sp.re(r) > 0)
    arr, status = build_routh(coeffs)
    first_col = [arr[i][0] for i in range(order+1)]
    sign_changes = sum(1 for i in range(len(first_col)-1)
                       if sp.sign(first_col[i]) != sp.sign(first_col[i+1]) and first_col[i+1] != 0)
    stmt = f"Build the Routh array for $p(s) = {poly_str}$ and determine stability."
    fc_str = ", ".join(str(float(x)) if x.is_number else str(x) for x in first_col)
    sol = (f"First column: $[{fc_str}]$\n\n"
           f"Sign changes: {sign_changes} → {sign_changes} RHP root(s).\n\n"
           f"**{'Stable' if sign_changes == 0 else 'Unstable'}**")
    return Problem("Routh array construction", stmt, sol)

def gen_gain_range(rng: random.Random) -> Problem:
    a = rng.randint(2, 8)
    b = rng.randint(1, 6)
    # s^3 + a*s^2 + b*s + K = 0
    # Routh s^1: (a*b - K)/a > 0 => K < a*b
    K_max = a * b
    stmt = (f"Find the range of $K > 0$ for stability of "
            f"$s^3 + {a}s^2 + {b}s + K = 0$.")
    sol = (f"Routh array $s^1$ entry: $({a}\\cdot{b} - K)/{a} = ({K_max}-K)/{a}$\n\n"
           f"Stability: ${K_max}-K > 0$ and $K > 0$\n\n"
           f"**Stable range: $0 < K < {K_max}$**")
    return Problem("Gain range for stability", stmt, sol)

def gen_necessary_condition(rng: random.Random) -> Problem:
    order = rng.choice([3, 4])
    coeffs = [1] + [rng.randint(-2, 6) for _ in range(order)]
    # Ensure at least one is negative or zero
    idx = rng.randint(1, order)
    coeffs[idx] = rng.choice([-1, -2, 0])
    poly_str = " + ".join(f"{c}s^{order-i}" if order-i > 1 else (f"{c}s" if order-i == 1 else str(c))
                          for i, c in enumerate(coeffs))
    has_neg = any(c <= 0 for c in coeffs)
    stmt = f"Check the necessary condition for stability of $p(s) = {poly_str}$."
    sol = (f"Coefficients: {coeffs}\n\n"
           f"{'Negative or zero coefficient found' if has_neg else 'All positive'} → "
           f"**{'Necessary condition FAILS — unstable' if has_neg else 'Passes necessary condition'}**")
    return Problem("Necessary condition check", stmt, sol)

GENERATORS = [gen_routh_basic, gen_routh_basic, gen_gain_range, gen_necessary_condition]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.4 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, stability, routh-hurwitz]\n"
              "type: practice\n---\n# 11.4 Practice — Stability & Routh-Hurwitz\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

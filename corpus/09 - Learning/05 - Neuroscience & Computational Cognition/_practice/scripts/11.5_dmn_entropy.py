#!/usr/bin/env python3
"""
11.5_dmn_entropy.py — Cortical entropy estimator from synthetic time series.
Implements permutation entropy and Lempel-Ziv complexity.

Modes:
  --demo : Generate synthetic neural time series at different entropy levels, compute and plot
  default: Generate entropy calculation drill problems

Usage:
  python 11.5_dmn_entropy.py --demo
  python 11.5_dmn_entropy.py --count 10 --seed 42
"""
from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from itertools import permutations
from math import factorial, log2
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
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def permutation_entropy(x, m=3, tau=1):
    """Compute normalized permutation entropy."""
    n = len(x)
    patterns = {}
    count = 0
    for i in range(n - (m - 1) * tau):
        window = tuple(x[i + j * tau] for j in range(m))
        pattern = tuple(np.argsort(window))
        patterns[pattern] = patterns.get(pattern, 0) + 1
        count += 1
    probs = np.array(list(patterns.values())) / count
    H = -np.sum(probs * np.log2(probs))
    return H / log2(factorial(m))


def lempel_ziv_complexity(s):
    """Compute Lempel-Ziv complexity (LZ76) of binary string."""
    n = len(s)
    if n == 0:
        return 0
    c = 1
    l = 1
    k = 1
    i = 0
    while i + k <= n:
        substr = s[i + 1:i + k + 1] if i + k + 1 <= n else ""
        if s[i + k - 1:i + k] not in s[i:i + k - 1]:
            # Simplified: count distinct substrings
            pass
        k += 1
        if i + k > n:
            break
    # Use the standard sequential parsing
    i = 0
    c = 0
    while i < n:
        l = 1
        found = True
        while found and i + l <= n:
            substr = s[i:i + l]
            if substr in s[:i]:
                l += 1
            else:
                found = False
        c += 1
        i += l - 1 if l > 1 else 1
    return c * log2(n) / n if n > 0 else 0


def run_demo():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required for --demo")
        sys.exit(1)

    np.random.seed(42)
    n_samples = 1000

    # Generate signals at different entropy levels
    signals = {
        "Low entropy (sine + small noise)": np.sin(np.linspace(0, 20 * np.pi, n_samples)) + 0.1 * np.random.randn(n_samples),
        "Medium entropy (AR process)": None,
        "High entropy (white noise)": np.random.randn(n_samples),
    }
    # AR(1) process
    ar = np.zeros(n_samples)
    for i in range(1, n_samples):
        ar[i] = 0.7 * ar[i - 1] + np.random.randn()
    signals["Medium entropy (AR process)"] = ar

    fig, axes = plt.subplots(len(signals), 2, figsize=(12, 8))

    for idx, (name, sig) in enumerate(signals.items()):
        # Time series
        axes[idx, 0].plot(sig[:200], 'k', linewidth=0.8)
        axes[idx, 0].set_title(name)
        axes[idx, 0].set_ylabel("Amplitude")

        # Permutation entropy across embedding dimensions
        dims = range(3, 8)
        pe_values = [permutation_entropy(sig, m=m) for m in dims]
        axes[idx, 1].bar(list(dims), pe_values, color='steelblue', alpha=0.7)
        axes[idx, 1].set_ylim(0, 1.1)
        axes[idx, 1].set_ylabel("H_norm")
        axes[idx, 1].set_title(f"Permutation Entropy (m=3: {pe_values[0]:.3f})")

    axes[-1, 0].set_xlabel("Sample")
    axes[-1, 1].set_xlabel("Embedding dimension m")
    plt.tight_layout()
    plt.savefig("dmn_entropy_demo.png", dpi=150)
    print("Saved: dmn_entropy_demo.png")
    plt.show()


# --- Problem Generators ---
def gen_perm_entropy(rng: random.Random) -> Problem:
    seq = [rng.randint(1, 20) for _ in range(7)]
    m = 3
    # Compute
    n = len(seq)
    patterns = {}
    count = 0
    for i in range(n - m + 1):
        window = seq[i:i + m]
        pattern = tuple(int(x) for x in np.argsort(window))
        patterns[pattern] = patterns.get(pattern, 0) + 1
        count += 1
    probs = {k: v / count for k, v in patterns.items()}
    H = -sum(p * log2(p) for p in probs.values())
    H_norm = H / log2(factorial(m))

    stmt = (
        f"Compute normalized permutation entropy ($m=3$, $\\tau=1$) for:\n\n"
        f"$x = [{', '.join(str(s) for s in seq)}]$"
    )
    pattern_str = ", ".join(f"{k}: {v}/{count}" for k, v in sorted(patterns.items()))
    sol = (
        f"Embedding vectors (windows of 3): {n - m + 1} total\n\n"
        f"Pattern frequencies: {pattern_str}\n\n"
        f"$H_{{\\text{{perm}}}} = {H:.4f}$ bits\n\n"
        f"$H_{{\\text{{norm}}}} = {H:.4f} / \\log_2(6) = {H:.4f} / 2.585 = {H_norm:.4f}$"
    )
    return Problem("Permutation entropy", stmt, sol)


def gen_kramers(rng: random.Random) -> Problem:
    dE = round(rng.uniform(2.0, 8.0), 1)
    sigma_normal = round(rng.uniform(0.5, 2.0), 1)
    factor = round(rng.uniform(1.5, 4.0), 1)
    sigma_enhanced = sigma_normal * factor
    k_normal = np.exp(-dE / sigma_normal)
    k_enhanced = np.exp(-dE / sigma_enhanced)
    ratio = k_enhanced / k_normal
    stmt = (
        f"Attractor depth $\\Delta E = {dE}$. Normal noise $\\sigma^2/2 = {sigma_normal}$. "
        f"Enhanced entropy: $\\sigma^2/2 = {sigma_enhanced:.1f}$ ({factor}× increase). "
        f"Compute escape rate ratio."
    )
    sol = (
        f"$k_{{\\text{{normal}}}} \\propto e^{{-{dE}/{sigma_normal}}} = e^{{{-dE/sigma_normal:.3f}}} = {k_normal:.6f}$\n\n"
        f"$k_{{\\text{{enhanced}}}} \\propto e^{{-{dE}/{sigma_enhanced:.1f}}} = e^{{{-dE/sigma_enhanced:.3f}}} = {k_enhanced:.6f}$\n\n"
        f"Ratio: ${k_enhanced:.6f} / {k_normal:.6f} = {ratio:.1f}\\times$ faster escape"
    )
    return Problem("Kramers' escape rate", stmt, sol)


def gen_rebus_posterior(rng: random.Random) -> Problem:
    mu0 = round(rng.uniform(-5, -1), 1)
    Pi_theta = rng.randint(5, 15)
    x = round(rng.uniform(0, 5), 1)
    Pi_x = rng.randint(3, 10)
    alpha = round(rng.uniform(0.1, 0.4), 2)
    mu_normal = (Pi_x * x + Pi_theta * mu0) / (Pi_x + Pi_theta)
    mu_rebus = (Pi_x * x + alpha * Pi_theta * mu0) / (Pi_x + alpha * Pi_theta)
    stmt = (
        f"Prior: $\\mu_0 = {mu0}$, $\\Pi_\\theta = {Pi_theta}$. "
        f"Evidence: $x = {x}$, $\\Pi_x = {Pi_x}$. "
        f"Compute posterior normally and under REBUS ($\\alpha = {alpha}$)."
    )
    sol = (
        f"Normal: $\\mu_{{post}} = \\frac{{{Pi_x}({x}) + {Pi_theta}({mu0})}}{{{Pi_x} + {Pi_theta}}} = {mu_normal:.3f}$\n\n"
        f"REBUS: $\\mu_{{post}} = \\frac{{{Pi_x}({x}) + {alpha}\\times{Pi_theta}({mu0})}}{{{Pi_x} + {alpha}\\times{Pi_theta}}} = {mu_rebus:.3f}$\n\n"
        f"Shift: ${mu_rebus - mu_normal:+.3f}$ (toward evidence under REBUS)"
    )
    return Problem("REBUS precision reduction", stmt, sol)


GENERATORS = [gen_perm_entropy, gen_kramers, gen_rebus_posterior]


def main():
    parser = argparse.ArgumentParser(description="11.5 DMN entropy estimator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    rng = random.Random(seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/neuro, DMN, entropy, free-energy, practice]\n"
        f"generated: seed={seed}\n---\n\n"
        "# 11.5 Practice — Default Mode Network & Cortical Entropy\n\n"
        f"Generated {args.count} problems (seed={seed}).\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Written {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

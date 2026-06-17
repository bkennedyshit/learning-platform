#!/usr/bin/env python3
"""
10.6_diffusion.py — Practice problems for Generative Models (GANs & Diffusion).

Archetypes:
  1. Compute optimal discriminator D*(x)
  2. Forward diffusion: compute alpha_bar and x_t
  3. KL divergence between two Gaussians
  4. ELBO computation
  5. Noise schedule analysis

Usage:
  python 10.6_diffusion.py --count 10 --seed 42
  python 10.6_diffusion.py --demo
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
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
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )


def gen_optimal_disc(rng: random.Random) -> Problem:
    p_data = round(rng.uniform(0.1, 0.9), 2)
    p_g = round(rng.uniform(0.1, 0.9), 2)
    d_star = p_data / (p_data + p_g)
    stmt = f"At point $x$: $p_{{data}}(x)={p_data}$, $p_G(x)={p_g}$. Compute $D^*(x)$."
    sol = f"$D^*(x) = \\frac{{p_{{data}}}}{{p_{{data}}+p_G}} = \\frac{{{p_data}}}{{{p_data}+{p_g}}} = \\frac{{{p_data}}}{{{p_data+p_g:.2f}}} = {d_star:.4f}$"
    return Problem("Optimal discriminator", stmt, sol)


def gen_forward_diff(rng: random.Random) -> Problem:
    T = 1000
    t = rng.randint(100, 900)
    beta_start, beta_end = 1e-4, 0.02
    betas = np.linspace(beta_start, beta_end, T)
    alphas = 1 - betas
    alpha_bar = np.cumprod(alphas)
    ab_t = alpha_bar[t-1]
    stmt = (
        f"Linear noise schedule $\\beta \\in [10^{{-4}}, 0.02]$, $T={T}$. "
        f"Compute $\\bar{{\\alpha}}_{{{t}}}$ and the signal-to-noise ratio."
    )
    snr = ab_t / (1 - ab_t)
    sol = (
        f"$\\bar{{\\alpha}}_{{{t}}} = \\prod_{{s=1}}^{{{t}}}(1-\\beta_s) = {ab_t:.6f}$\n\n"
        f"Signal fraction: $\\sqrt{{\\bar{{\\alpha}}_{{{t}}}}} = {np.sqrt(ab_t):.4f}$\n\n"
        f"Noise fraction: $\\sqrt{{1-\\bar{{\\alpha}}_{{{t}}}}} = {np.sqrt(1-ab_t):.4f}$\n\n"
        f"SNR = $\\bar{{\\alpha}}_t/(1-\\bar{{\\alpha}}_t) = {snr:.4f}$"
    )
    return Problem("Forward diffusion", stmt, sol)


def gen_kl_gaussian(rng: random.Random) -> Problem:
    d = rng.randint(1, 3)
    mu = [round(rng.uniform(-2, 2), 2) for _ in range(d)]
    log_var = [round(rng.uniform(-1, 1), 2) for _ in range(d)]
    kl = -0.5 * sum(1 + lv - m**2 - np.exp(lv) for m, lv in zip(mu, log_var))
    stmt = (
        f"Compute $D_{{KL}}(\\mathcal{{N}}(\\mu, \\sigma^2) \\| \\mathcal{{N}}(0, I))$ with "
        f"$\\mu = ({', '.join(str(m) for m in mu)})$, "
        f"$\\log\\sigma^2 = ({', '.join(str(lv) for lv in log_var)})$."
    )
    terms = []
    for j, (m, lv) in enumerate(zip(mu, log_var)):
        t = 1 + lv - m**2 - np.exp(lv)
        terms.append(f"dim {j+1}: $1 + {lv} - {m}^2 - e^{{{lv}}} = {t:.4f}$")
    sol = "\n\n".join(terms) + f"\n\n$D_{{KL}} = -\\frac{{1}}{{2}}({sum(1+lv-m**2-np.exp(lv) for m,lv in zip(mu,log_var)):.4f}) = {kl:.4f}$"
    return Problem("KL divergence (Gaussian)", stmt, sol)


def gen_noise_schedule(rng: random.Random) -> Problem:
    T = rng.choice([100, 500, 1000])
    beta_end = rng.choice([0.01, 0.02, 0.05])
    betas = np.linspace(1e-4, beta_end, T)
    alphas = 1 - betas
    alpha_bar = np.cumprod(alphas)
    t_half = np.argmin(np.abs(alpha_bar - 0.5)) + 1
    stmt = (
        f"Noise schedule: linear $\\beta \\in [10^{{-4}}, {beta_end}]$, $T={T}$. "
        "At what step $t$ is the signal approximately 50% (i.e., $\\bar{\\alpha}_t \\approx 0.5$)?"
    )
    sol = f"$\\bar{{\\alpha}}_{{{t_half}}} \\approx 0.5$. At step $t={t_half}$, the image is half signal, half noise."
    return Problem("Noise schedule analysis", stmt, sol)


def run_demo():
    print("=" * 60)
    print("DEMO: Forward Diffusion Process")
    print("=" * 60)
    T = 1000
    betas = np.linspace(1e-4, 0.02, T)
    alphas = 1 - betas
    alpha_bar = np.cumprod(alphas)

    print(f"\nNoise schedule (linear, T={T}):")
    for t in [0, 100, 250, 500, 750, 999]:
        print(f"  t={t:4d}: beta={betas[t]:.5f}, alpha_bar={alpha_bar[t]:.6f}, "
              f"signal={np.sqrt(alpha_bar[t]):.4f}, noise={np.sqrt(1-alpha_bar[t]):.4f}")

    # Simulate forward diffusion on a 1D signal
    x0 = 5.0
    print(f"\nForward diffusion of x0={x0}:")
    for t in [0, 100, 250, 500, 750, 999]:
        noise = np.random.randn()
        x_t = np.sqrt(alpha_bar[t]) * x0 + np.sqrt(1-alpha_bar[t]) * noise
        print(f"  t={t:4d}: x_t = {x_t:.4f} (signal={np.sqrt(alpha_bar[t])*x0:.4f}, noise_std={np.sqrt(1-alpha_bar[t]):.4f})")

    # KL divergence demo
    print("\n--- KL Divergence Demo ---")
    mu = np.array([1.0, -0.5])
    log_var = np.array([0.0, -0.5])
    kl = -0.5 * np.sum(1 + log_var - mu**2 - np.exp(log_var))
    print(f"KL(N({mu}, diag(exp({log_var}))) || N(0,I)) = {kl:.4f}")


GENERATORS = [gen_optimal_disc, gen_forward_diff, gen_kl_gaussian, gen_noise_schedule]


def main():
    parser = argparse.ArgumentParser(description="10.6 Diffusion practice")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    lines = ["---", "tags: [review/ai, diffusion, gan, generative-models]",
             "generated: true", "---", "", "# 10.6 Generative Models — Practice Problems", ""]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()

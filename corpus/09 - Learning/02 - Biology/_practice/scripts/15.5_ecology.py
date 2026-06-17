#!/usr/bin/env python3
"""
15.5_ecology.py — Practice problem generator for Chapter 15.5
(Ecology & Ecosystems).

Generates randomized drill problems:
  1. Logistic growth (population at time t, time to K/2)
  2. Shannon diversity index
  3. Lotka-Volterra predator-prey equilibrium
  4. Ecosystem energy budget (trophic efficiency)

Usage:
  python 15.5_ecology.py
  python 15.5_ecology.py --count 12 --seed 77
"""
from __future__ import annotations
import argparse, random, math
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


def gen_logistic(rng: random.Random) -> Problem:
    r = round(rng.uniform(0.1, 0.5), 2)
    K = rng.choice([200, 500, 1000, 2000, 5000])
    N0 = rng.randint(10, K // 10)
    t = rng.randint(3, 15)
    Nt = K / (1 + ((K - N0) / N0) * math.exp(-r * t))
    t_half = math.log((K - N0) / N0) / r
    stmt = (
        f"A population has $r = {r}$/year, $K = {K}$, $N_0 = {N0}$. "
        f"(a) Find $N$ at $t = {t}$ years. (b) Find time to reach $K/2$."
    )
    sol = (
        f"(a) $N({t}) = \\frac{{{K}}}{{1 + \\frac{{{K}-{N0}}}{{{N0}}}e^{{-{r}\\times{t}}}}} "
        f"= \\frac{{{K}}}{{1 + {(K-N0)/N0:.2f} \\times e^{{{-r*t:.2f}}}}} = {Nt:.1f}$\n\n"
        f"(b) At $N = K/2 = {K//2}$: $t = \\frac{{\\ln({(K-N0)/N0:.2f})}}{{{r}}} = {t_half:.2f}$ years"
    )
    return Problem("Logistic Growth", stmt, sol)


def gen_shannon(rng: random.Random) -> Problem:
    S = rng.randint(4, 8)
    counts = [rng.randint(10, 200) for _ in range(S)]
    total = sum(counts)
    props = [c / total for c in counts]
    H = -sum(p * math.log(p) for p in props if p > 0)
    H_max = math.log(S)
    J = H / H_max
    species_names = ["Sp. A", "Sp. B", "Sp. C", "Sp. D", "Sp. E", "Sp. F", "Sp. G", "Sp. H"][:S]
    count_str = ", ".join(f"{species_names[i]}: {counts[i]}" for i in range(S))
    stmt = (
        f"A community survey finds: {count_str} (total = {total}). "
        f"Calculate Shannon diversity index $H'$ and evenness $J$."
    )
    sol = (
        f"Proportions: {', '.join(f'{p:.4f}' for p in props)}\n\n"
        f"$H' = -\\sum p_i \\ln p_i = {H:.4f}$\n\n"
        f"$H'_{{\\max}} = \\ln({S}) = {H_max:.4f}$\n\n"
        f"Evenness: $J = H'/H'_{{\\max}} = {J:.4f}$"
    )
    return Problem("Shannon Diversity Index", stmt, sol)


def gen_lotka_volterra(rng: random.Random) -> Problem:
    r = round(rng.uniform(0.2, 0.8), 2)
    a = round(rng.uniform(0.005, 0.02), 3)
    b = round(rng.uniform(0.1, 0.4), 2)
    m = round(rng.uniform(0.1, 0.5), 2)
    N_eq = m / (b * a)
    P_eq = r / a
    T = 2 * math.pi / math.sqrt(r * m)
    stmt = (
        f"Lotka-Volterra predator-prey: $r = {r}$, $a = {a}$, $b = {b}$, $m = {m}$. "
        f"Find equilibrium populations and oscillation period."
    )
    sol = (
        f"$N^* = m/(ba) = {m}/({b} \\times {a}) = {N_eq:.1f}$ prey\n\n"
        f"$P^* = r/a = {r}/{a} = {P_eq:.1f}$ predators\n\n"
        f"Period: $T \\approx 2\\pi/\\sqrt{{rm}} = 2\\pi/\\sqrt{{{r}\\times{m}}} = {T:.1f}$ time units"
    )
    return Problem("Lotka-Volterra Equilibrium", stmt, sol)


def gen_energy_budget(rng: random.Random) -> Problem:
    npp = rng.choice([5000, 8000, 10000, 15000, 20000])
    eff = [round(rng.uniform(0.08, 0.15), 2) for _ in range(3)]
    levels = [npp]
    for e in eff:
        levels.append(levels[-1] * e)
    stmt = (
        f"An ecosystem has NPP = {npp} kJ/m²/year. Trophic efficiencies: "
        f"herbivores {eff[0]*100:.0f}%, secondary consumers {eff[1]*100:.0f}%, "
        f"tertiary consumers {eff[2]*100:.0f}%. Calculate energy at each level."
    )
    sol = (
        f"- Producers: {levels[0]:.0f} kJ/m²/year\n"
        f"- Primary consumers: {levels[0]} × {eff[0]} = {levels[1]:.1f}\n"
        f"- Secondary consumers: {levels[1]:.1f} × {eff[1]} = {levels[2]:.1f}\n"
        f"- Tertiary consumers: {levels[2]:.1f} × {eff[2]} = {levels[3]:.2f}\n\n"
        f"Total reaching top: {levels[3]/levels[0]*100:.4f}% of NPP"
    )
    return Problem("Ecosystem Energy Budget", stmt, sol)


ARCHETYPES = [gen_logistic, gen_shannon, gen_lotka_volterra, gen_energy_budget]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [biology, ecology, population-dynamics, diversity, practice, \"review/bio/15.5\"]\n"
        "chapter: 15.5\ntype: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n---\n\n"
        "*Back to [[../15.5 - Ecology & Ecosystems|Chapter 15.5]] | "
        "Part of [[../../09 - Learning Index]]*\n\n"
        "# Chapter 15.5 — Practice Drills: Ecology & Ecosystems\n\n"
        "> Auto-generated by `scripts/15.5_ecology.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n---\n\n"
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
    out_path = args.out or (Path(__file__).resolve().parent.parent / "15.5_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

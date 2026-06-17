#!/usr/bin/env python3
"""
15.7_immunology.py — Practice problem generator for Chapter 15.7
(Immunology & Disease).

Generates randomized drill problems:
  1. V(D)J diversity calculation
  2. Herd immunity threshold
  3. SIR model basic reproduction number
  4. Antibody affinity / clonal expansion

Usage:
  python 15.7_immunology.py
  python 15.7_immunology.py --count 10 --seed 55
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


def gen_vdj_diversity(rng: random.Random) -> Problem:
    V = rng.randint(30, 65)
    D = rng.randint(2, 27)
    J = rng.randint(4, 13)
    junctional = rng.choice([1e4, 1e5, 1e6, 3e6])
    combinatorial = V * D * J
    total_chain = combinatorial * junctional
    light_diversity = rng.choice([1e4, 5e4, 1e5])
    total = total_chain * light_diversity
    stmt = (
        f"An immunoglobulin heavy chain locus has {V} V segments, {D} D segments, "
        f"and {J} J segments. Junctional diversity contributes a factor of {junctional:.0e}. "
        f"If light chain diversity = {light_diversity:.0e}, calculate total antibody diversity."
    )
    sol = (
        f"Combinatorial: ${V} \\times {D} \\times {J} = {combinatorial:,}$\n\n"
        f"With junctional: ${combinatorial:,} \\times {junctional:.0e} = {total_chain:.2e}$\n\n"
        f"Total (heavy × light): ${total_chain:.2e} \\times {light_diversity:.0e} = {total:.2e}$\n\n"
        f"This exceeds the actual repertoire (~$10^7$–$10^8$) because total T/B cell number is limiting."
    )
    return Problem("V(D)J Diversity Calculation", stmt, sol)


def gen_herd_immunity(rng: random.Random) -> Problem:
    R0 = round(rng.uniform(1.5, 15), 1)
    efficacy = round(rng.uniform(0.7, 0.98), 2)
    pc = 1 - 1 / R0
    vacc_needed = pc / efficacy
    stmt = (
        f"A pathogen has $R_0 = {R0}$. A vaccine has efficacy = {efficacy*100:.0f}%. "
        f"(a) Calculate herd immunity threshold. (b) What vaccination coverage is needed?"
    )
    sol = (
        f"(a) $p_c = 1 - 1/R_0 = 1 - 1/{R0} = {pc:.4f} = {pc*100:.1f}\\%$\n\n"
        f"(b) Coverage needed: $p_c / e = {pc:.4f} / {efficacy} = {vacc_needed:.4f} = {vacc_needed*100:.1f}\\%$"
        + (f"\n\n⚠️ This exceeds 100% — herd immunity is **not achievable** with this vaccine alone."
           if vacc_needed > 1 else "")
    )
    return Problem("Herd Immunity Threshold", stmt, sol)


def gen_sir_R0(rng: random.Random) -> Problem:
    beta = round(rng.uniform(0.1, 0.5), 2)
    gamma = round(rng.uniform(0.05, 0.2), 2)
    R0 = beta / gamma
    peak_S = 1 / R0
    stmt = (
        f"An SIR model has transmission rate $\\beta = {beta}$/day and recovery rate "
        f"$\\gamma = {gamma}$/day. (a) Calculate $R_0$. (b) At what fraction susceptible "
        f"does the epidemic peak? (c) What is the infectious period?"
    )
    sol = (
        f"(a) $R_0 = \\beta/\\gamma = {beta}/{gamma} = {R0:.2f}$\n\n"
        f"(b) Epidemic peaks when $S = \\gamma/\\beta = 1/R_0 = {peak_S:.4f} = {peak_S*100:.1f}\\%$ susceptible\n\n"
        f"(c) Infectious period: $1/\\gamma = {1/gamma:.1f}$ days"
    )
    return Problem("SIR Model & R₀", stmt, sol)


def gen_clonal_expansion(rng: random.Random) -> Problem:
    doubling_time = round(rng.uniform(6, 10), 1)
    days = rng.randint(5, 10)
    hours = days * 24
    divisions = hours / doubling_time
    final_cells = 2 ** divisions
    memory_fraction = round(rng.uniform(0.05, 0.10), 2)
    memory_cells = final_cells * memory_fraction
    stmt = (
        f"A single activated T cell divides with doubling time = {doubling_time} hours. "
        f"After {days} days of expansion, (a) how many effector cells exist? "
        f"(b) If {memory_fraction*100:.0f}% become memory cells, how many memory cells form?"
    )
    sol = (
        f"(a) Divisions: ${hours}/{doubling_time} = {divisions:.1f}$ doublings\n\n"
        f"Effector cells: $2^{{{divisions:.1f}}} = {final_cells:.2e}$\n\n"
        f"(b) Memory cells: ${final_cells:.2e} \\times {memory_fraction} = {memory_cells:.2e}$"
    )
    return Problem("Clonal Expansion", stmt, sol)


ARCHETYPES = [gen_vdj_diversity, gen_herd_immunity, gen_sir_R0, gen_clonal_expansion]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [biology, immunology, VDJ, herd-immunity, SIR-model, practice, \"review/bio/15.7\"]\n"
        "chapter: 15.7\ntype: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n---\n\n"
        "*Back to [[../15.7 - Immunology & Disease|Chapter 15.7]] | "
        "Part of [[../../09 - Learning Index]]*\n\n"
        "# Chapter 15.7 — Practice Drills: Immunology & Disease\n\n"
        "> Auto-generated by `scripts/15.7_immunology.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "15.7_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

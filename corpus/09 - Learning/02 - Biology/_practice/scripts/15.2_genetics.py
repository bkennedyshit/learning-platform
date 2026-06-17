#!/usr/bin/env python3
"""
15.2_genetics.py — Practice problem generator for Chapter 15.2
(Genetics & Inheritance).

Generates randomized drill problems:
  1. Monohybrid cross (Punnett square)
  2. Dihybrid cross (phenotype ratios)
  3. X-linked inheritance
  4. Chi-square goodness-of-fit
  5. Recombination frequency / map distance

Usage:
  python 15.2_genetics.py
  python 15.2_genetics.py --count 20 --seed 42
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


TRAITS = [
    ("tall", "dwarf", "T", "t"),
    ("round", "wrinkled", "R", "r"),
    ("purple", "white", "P", "p"),
    ("smooth", "rough", "S", "s"),
    ("yellow", "green", "Y", "y"),
]


def gen_monohybrid(rng: random.Random) -> Problem:
    dom, rec, D, d = rng.choice(TRAITS)
    crosses = [
        (f"{D}{D}", f"{D}{d}", "All offspring are heterozygous"),
        (f"{D}{d}", f"{D}{d}", "3:1 phenotype ratio"),
        (f"{D}{d}", f"{d}{d}", "1:1 phenotype ratio (testcross)"),
    ]
    p1, p2, hint = rng.choice(crosses)
    stmt = (
        f"In a plant species, {dom} ({D}) is dominant over {rec} ({d}). "
        f"Cross **{p1} × {p2}**. Predict the genotype and phenotype ratios of offspring."
    )
    # compute
    g1 = list(p1)
    g2 = list(p2)
    offspring = {}
    for a in g1:
        for b in g2:
            gt = "".join(sorted([a, b], key=lambda x: x.isupper(), reverse=True))
            offspring[gt] = offspring.get(gt, 0) + 1
    total = sum(offspring.values())
    geno_str = " : ".join(f"{v} {k}" for k, v in sorted(offspring.items()))
    dom_count = sum(v for k, v in offspring.items() if D in k)
    rec_count = sum(v for k, v in offspring.items() if D not in k)
    pheno_str = f"{dom_count} {dom} : {rec_count} {rec}" if rec_count > 0 else f"All {dom}"
    sol = f"**Genotype ratio:** {geno_str} (out of {total})\n\n**Phenotype ratio:** {pheno_str}\n\n*Hint: {hint}*"
    return Problem("Monohybrid Cross", stmt, sol)


def gen_dihybrid(rng: random.Random) -> Problem:
    t1 = rng.choice(TRAITS[:3])
    t2 = rng.choice(TRAITS[3:])
    dom1, rec1, D1, d1 = t1
    dom2, rec2, D2, d2 = t2
    stmt = (
        f"Cross two organisms heterozygous for both traits: "
        f"**{D1}{d1}{D2}{d2} × {D1}{d1}{D2}{d2}**. "
        f"{dom1} ({D1}) is dominant over {rec1} ({d1}); "
        f"{dom2} ({D2}) is dominant over {rec2} ({d2}). "
        f"What fraction of offspring show both dominant phenotypes?"
    )
    sol = (
        f"Each gene segregates independently.\n\n"
        f"$P({dom1}) = 3/4$, $P({dom2}) = 3/4$\n\n"
        f"$P(\\text{{both dominant}}) = 3/4 \\times 3/4 = 9/16$\n\n"
        f"Full ratio: 9 {dom1}+{dom2} : 3 {dom1}+{rec2} : 3 {rec1}+{dom2} : 1 {rec1}+{rec2}"
    )
    return Problem("Dihybrid Cross", stmt, sol)


def gen_chi_square(rng: random.Random) -> Problem:
    n = rng.randint(80, 200)
    expected_ratio = rng.choice([(3, 1), (1, 1), (9, 3, 3, 1)])
    total_parts = sum(expected_ratio)
    expected = [n * r / total_parts for r in expected_ratio]
    # generate observed with some noise
    observed = [int(e + rng.gauss(0, math.sqrt(e))) for e in expected]
    # ensure sum = n
    observed[-1] = n - sum(observed[:-1])
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    df = len(expected_ratio) - 1
    crit = {1: 3.841, 2: 5.991, 3: 7.815}[df]
    reject = chi2 > crit
    ratio_str = ":".join(str(r) for r in expected_ratio)
    obs_str = ", ".join(str(o) for o in observed)
    stmt = (
        f"A cross expected to produce a **{ratio_str}** ratio yields observed counts: "
        f"**{obs_str}** (total = {n}). Perform a chi-square test at α = 0.05."
    )
    exp_str = ", ".join(f"{e:.1f}" for e in expected)
    sol = (
        f"**Expected:** {exp_str}\n\n"
        f"$\\chi^2 = {chi2:.3f}$, df = {df}, critical value = {crit}\n\n"
        f"**Decision:** {'Reject' if reject else 'Fail to reject'} null hypothesis. "
        f"Data {'do NOT fit' if reject else 'are consistent with'} the {ratio_str} ratio."
    )
    return Problem("Chi-Square Test", stmt, sol)


def gen_recombination(rng: random.Random) -> Problem:
    rf = rng.randint(5, 40)
    total = rng.randint(500, 2000)
    recombinants = int(total * rf / 100)
    parentals = total - recombinants
    p1 = parentals // 2 + rng.randint(-5, 5)
    p2 = parentals - p1
    r1 = recombinants // 2 + rng.randint(-3, 3)
    r2 = recombinants - r1
    stmt = (
        f"A testcross produces: Parental class 1: {p1}, Parental class 2: {p2}, "
        f"Recombinant class 1: {r1}, Recombinant class 2: {r2}. "
        f"Calculate the recombination frequency and map distance."
    )
    actual_rf = (r1 + r2) / total * 100
    sol = (
        f"Total = {total}\n\n"
        f"Recombinants = {r1} + {r2} = {r1 + r2}\n\n"
        f"$RF = {r1 + r2}/{total} = {actual_rf:.1f}\\%$\n\n"
        f"Map distance = **{actual_rf:.1f} cM**\n\n"
        f"Genes are {'linked' if actual_rf < 50 else 'unlinked (assort independently)'}."
    )
    return Problem("Recombination Frequency", stmt, sol)


ARCHETYPES = [gen_monohybrid, gen_dihybrid, gen_chi_square, gen_recombination]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [biology, genetics, punnett-squares, chi-square, practice, \"review/bio/15.2\"]\n"
        "chapter: 15.2\ntype: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n---\n\n"
        "*Back to [[../15.2 - Genetics & Inheritance|Chapter 15.2]] | "
        "Part of [[../../09 - Learning Index]]*\n\n"
        "# Chapter 15.2 — Practice Drills: Genetics & Inheritance\n\n"
        "> Auto-generated by `scripts/15.2_genetics.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "15.2_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

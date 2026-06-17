#!/usr/bin/env python3
"""
15.4_evolution.py — Practice problem generator for Chapter 15.4
(Evolution & Natural Selection).

Generates randomized drill problems:
  1. Hardy-Weinberg equilibrium (allele/genotype frequencies)
  2. Selection against recessive allele
  3. Heterozygote advantage equilibrium
  4. Genetic drift (fixation probability)
  5. dN/dS interpretation

Usage:
  python 15.4_evolution.py
  python 15.4_evolution.py --count 15 --seed 99
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


def gen_hardy_weinberg(rng: random.Random) -> Problem:
    q2_denom = rng.choice([400, 900, 1600, 2500, 3600, 10000])
    q2 = 1 / q2_denom
    q = math.sqrt(q2)
    p = 1 - q
    carrier = 2 * p * q
    disease = rng.choice([
        "phenylketonuria", "cystic fibrosis", "sickle-cell disease",
        "albinism", "Tay-Sachs disease"
    ])
    stmt = (
        f"**{disease.title()}** (autosomal recessive) affects 1 in {q2_denom} individuals. "
        f"Assuming Hardy-Weinberg equilibrium, calculate: (a) allele frequencies, "
        f"(b) carrier frequency, (c) probability two carriers have an affected child."
    )
    sol = (
        f"(a) $q^2 = 1/{q2_denom} = {q2:.6f}$ → $q = {q:.4f}$, $p = {p:.4f}$\n\n"
        f"(b) Carrier frequency: $2pq = 2({p:.4f})({q:.4f}) = {carrier:.4f}$ ≈ 1 in {int(1/carrier)}\n\n"
        f"(c) $P(\\text{{affected}} | \\text{{both carriers}}) = 1/4 = 25\\%$"
    )
    return Problem("Hardy-Weinberg Equilibrium", stmt, sol)


def gen_selection_recessive(rng: random.Random) -> Problem:
    q0 = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5])
    s = rng.choice([0.1, 0.2, 0.5, 1.0])
    # After one generation of selection against recessive
    # w_AA=1, w_Aa=1, w_aa=1-s
    p0 = 1 - q0
    wbar = p0**2 + 2*p0*q0 + q0**2*(1-s)
    q1 = (q0**2*(1-s) + p0*q0) / wbar
    delta_q = q1 - q0
    stmt = (
        f"A recessive allele has frequency $q = {q0}$. Selection coefficient against "
        f"homozygous recessives is $s = {s}$ (fitness $w_{{aa}} = {1-s}$). "
        f"Calculate: (a) mean fitness, (b) new $q$ after one generation, (c) $\\Delta q$."
    )
    sol = (
        f"(a) $\\bar{{w}} = p^2(1) + 2pq(1) + q^2(1-s) = {p0**2:.4f} + {2*p0*q0:.4f} + {q0**2*(1-s):.4f} = {wbar:.4f}$\n\n"
        f"(b) $q' = \\frac{{q^2(1-s) + pq}}{{\\bar{{w}}}} = \\frac{{{q0**2*(1-s):.4f} + {p0*q0:.4f}}}{{{wbar:.4f}}} = {q1:.4f}$\n\n"
        f"(c) $\\Delta q = {q1:.4f} - {q0} = {delta_q:.4f}$ "
        f"({'decrease' if delta_q < 0 else 'increase'} in recessive allele frequency)"
    )
    return Problem("Selection Against Recessive", stmt, sol)


def gen_heterozygote_advantage(rng: random.Random) -> Problem:
    s1 = round(rng.uniform(0.05, 0.3), 2)
    s2 = round(rng.uniform(0.3, 0.9), 2)
    q_hat = s1 / (s1 + s2)
    p_hat = s2 / (s1 + s2)
    stmt = (
        f"In a population with heterozygote advantage: $w_{{AA}} = {1-s1}$, "
        f"$w_{{Aa}} = 1.0$, $w_{{aa}} = {1-s2}$. "
        f"Find the equilibrium allele frequencies."
    )
    sol = (
        f"At equilibrium: $\\hat{{q}} = \\frac{{s_1}}{{s_1 + s_2}} = \\frac{{{s1}}}{{{s1} + {s2}}} = {q_hat:.4f}$\n\n"
        f"$\\hat{{p}} = \\frac{{s_2}}{{s_1 + s_2}} = {p_hat:.4f}$\n\n"
        f"Disease frequency at equilibrium: $q^2 = {q_hat**2:.4f}$ = {q_hat**2*100:.2f}%"
    )
    return Problem("Heterozygote Advantage", stmt, sol)


def gen_drift_fixation(rng: random.Random) -> Problem:
    Ne = rng.choice([50, 100, 500, 1000, 5000, 10000])
    s = round(rng.uniform(0.001, 0.05), 3)
    p_fix_neutral = 1 / (2 * Ne)
    p_fix_beneficial = 2 * s
    effectively_neutral = s < 1 / (2 * Ne)
    stmt = (
        f"A new mutation arises in a population with effective size $N_e = {Ne}$. "
        f"(a) If neutral, what is its fixation probability? "
        f"(b) If beneficial with $s = {s}$, what is its fixation probability? "
        f"(c) Is this mutation effectively neutral?"
    )
    sol = (
        f"(a) Neutral fixation: $P_{{fix}} = 1/(2N_e) = 1/{2*Ne} = {p_fix_neutral:.6f}$\n\n"
        f"(b) Beneficial fixation (Haldane): $P_{{fix}} \\approx 2s = 2({s}) = {p_fix_beneficial:.4f}$\n\n"
        f"(c) Effectively neutral if $s < 1/(2N_e) = {1/(2*Ne):.6f}$. "
        f"Since $s = {s}$ {'<' if effectively_neutral else '>'} {1/(2*Ne):.6f}, "
        f"this mutation is **{'effectively neutral' if effectively_neutral else 'visible to selection'}**."
    )
    return Problem("Genetic Drift & Fixation", stmt, sol)


def gen_dnds(rng: random.Random) -> Problem:
    dN = round(rng.uniform(0.01, 1.0), 3)
    dS = round(rng.uniform(0.2, 0.8), 3)
    omega = dN / dS
    if omega < 0.3:
        interp = "Strong **purifying selection** — amino acid changes are deleterious and removed."
    elif omega < 0.8:
        interp = "Moderate purifying selection or relaxed constraint."
    elif omega < 1.2:
        interp = "Approximately **neutral evolution** — no strong selection on protein sequence."
    else:
        interp = "**Positive selection** — amino acid changes are advantageous and fixed faster than neutral."
    stmt = (
        f"Comparing orthologs between two species: $d_N = {dN}$, $d_S = {dS}$. "
        f"Calculate $\\omega$ (dN/dS) and interpret."
    )
    sol = (
        f"$\\omega = d_N/d_S = {dN}/{dS} = {omega:.3f}$\n\n"
        f"**Interpretation:** {interp}"
    )
    return Problem("dN/dS Ratio", stmt, sol)


ARCHETYPES = [gen_hardy_weinberg, gen_selection_recessive, gen_heterozygote_advantage,
              gen_drift_fixation, gen_dnds]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [biology, evolution, hardy-weinberg, population-genetics, practice, \"review/bio/15.4\"]\n"
        "chapter: 15.4\ntype: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n---\n\n"
        "*Back to [[../15.4 - Evolution & Natural Selection|Chapter 15.4]] | "
        "Part of [[../../09 - Learning Index]]*\n\n"
        "# Chapter 15.4 — Practice Drills: Evolution & Population Genetics\n\n"
        "> Auto-generated by `scripts/15.4_evolution.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=15)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "15.4_drills.md")
    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

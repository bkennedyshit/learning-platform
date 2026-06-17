#!/usr/bin/env python3
"""
16.7_organic_mechanisms.py — Practice problem generator for Chapter 16.7
(Organic Chemistry Foundations).

Generates randomized drill problems:
  1. SN1 vs SN2 prediction
  2. E1 vs E2 prediction
  3. Markovnikov addition product prediction
  4. EAS directing effects
  5. Functional group identification

Usage:
  python 16.7_organic_mechanisms.py
  python 16.7_organic_mechanisms.py --count 20 --seed 42
"""
from __future__ import annotations
import argparse, random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n<summary>Show solution</summary>\n\n"
                f"{self.solution_md}\n\n</details>\n")

def gen_sn1_vs_sn2(rng: random.Random) -> Problem:
    scenarios = [
        ("CH3Br + NaCN in DMSO", "SN2",
         "Methyl substrate (no steric hindrance), strong nucleophile (CN⁻), polar aprotic solvent (DMSO)"),
        ("(CH3)3CBr + H2O", "SN1",
         "Tertiary substrate (stable carbocation), weak nucleophile (H₂O), polar protic solvent"),
        ("CH3CH2Br + NaOH in DMSO", "SN2",
         "Primary substrate, strong nucleophile (OH⁻), polar aprotic solvent"),
        ("(CH3)3CCl + CH3OH", "SN1",
         "Tertiary substrate, weak nucleophile (methanol), polar protic solvent"),
        ("CH3CH2CH2Br + NaI in acetone", "SN2",
         "Primary substrate, strong nucleophile (I⁻), polar aprotic solvent (acetone)"),
        ("(CH3)2CHBr + NaOEt in ethanol", "E2 (competes with SN2)",
         "Secondary substrate with strong base → elimination dominates over substitution"),
    ]
    substrate, mechanism, explanation = rng.choice(scenarios)
    stmt = f"Predict the dominant mechanism for: **{substrate}**. Justify your answer."
    sol = f"**{mechanism}**\n\nReasoning: {explanation}"
    return Problem("SN1 vs SN2 vs E2 prediction", stmt, sol)

def gen_markovnikov(rng: random.Random) -> Problem:
    reactions = [
        ("CH3CH=CH2 + HBr", "CH3CHBrCH3 (2-bromopropane)",
         "H adds to less substituted C (C1), Br to more substituted C (C2) → 2° carbocation intermediate"),
        ("CH3CH=CHCH3 + HCl", "CH3CHClCHCH3 (2-chlorobutane or 3-chlorobutane)",
         "Symmetric alkene — both carbocations are 2°, so mixture of products"),
        ("(CH3)2C=CH2 + H2O/H+", "(CH3)3COH (tert-butanol)",
         "H adds to CH2 (less substituted), OH to C(CH3)2 → 3° carbocation (most stable)"),
        ("CH2=CH2 + HBr", "CH3CH2Br (bromoethane)",
         "Symmetric alkene — only one product possible (Markovnikov doesn't apply)"),
    ]
    rxn, product, explanation = rng.choice(reactions)
    stmt = f"Predict the major product of: **{rxn}** (Markovnikov addition)."
    sol = f"Major product: **{product}**\n\nExplanation: {explanation}"
    return Problem("Markovnikov addition", stmt, sol)

def gen_eas_directing(rng: random.Random) -> Problem:
    groups = [
        ("-CH3 (methyl)", "ortho/para", "activating",
         "EDG via hyperconjugation; stabilizes arenium ion at ortho/para positions"),
        ("-OH (hydroxyl)", "ortho/para", "strongly activating",
         "EDG via lone pair donation into ring; powerful activator"),
        ("-NO2 (nitro)", "meta", "deactivating",
         "EWG via resonance and induction; destabilizes ortho/para arenium ions"),
        ("-COOH (carboxyl)", "meta", "deactivating",
         "EWG; withdraws electron density from ring"),
        ("-NH2 (amino)", "ortho/para", "strongly activating",
         "EDG via lone pair donation; one of the strongest activators"),
        ("-Cl (chloro)", "ortho/para", "deactivating",
         "Lone pairs donate (ortho/para directing) but electronegativity withdraws (deactivating)"),
    ]
    group, direction, activation, explanation = rng.choice(groups)
    stmt = (f"For electrophilic aromatic substitution on a benzene ring bearing {group}:\n"
            f"(a) Is the group activating or deactivating?\n"
            f"(b) Does it direct ortho/para or meta?")
    sol = (f"(a) **{activation.capitalize()}**\n\n"
           f"(b) **{direction.capitalize()} director**\n\n"
           f"Explanation: {explanation}")
    return Problem("EAS directing effects", stmt, sol)

def gen_functional_group_id(rng: random.Random) -> Problem:
    groups = [
        ("CH3CH2OH", "alcohol (–OH)", "hydroxyl group bonded to sp³ carbon"),
        ("CH3CHO", "aldehyde (–CHO)", "carbonyl at terminal carbon"),
        ("CH3COCH3", "ketone (C=O)", "carbonyl between two carbons"),
        ("CH3COOH", "carboxylic acid (–COOH)", "carbonyl + hydroxyl on same carbon"),
        ("CH3COOCH3", "ester (–COO–)", "carbonyl bonded to –OR group"),
        ("CH3NH2", "primary amine (–NH2)", "nitrogen with two H's bonded to carbon"),
        ("CH3CONH2", "amide (–CONH2)", "carbonyl bonded to nitrogen"),
    ]
    formula, name, description = rng.choice(groups)
    stmt = f"Identify the functional group in: **{formula}**"
    sol = f"**{name}**\n\nDescription: {description}"
    return Problem("Functional group identification", stmt, sol)

ARCHETYPES = [gen_sn1_vs_sn2, gen_markovnikov, gen_eas_directing, gen_functional_group_id]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.randint(0, 2**31-1)
    rng = random.Random(seed)
    out_path = args.out or Path(__file__).resolve().parent.parent / "16.7_drills.md"
    problems = [rng.choice(ARCHETYPES)(rng) for _ in range(args.count)]
    header = (f"---\ntags: [chemistry, organic, mechanisms, practice]\nchapter: 16.7\n"
              f"type: practice\ngenerated: {datetime.now().isoformat(timespec='seconds')}\nseed: {seed}\n---\n\n"
              f"# Chapter 16.7 — Practice: Organic Chemistry Mechanisms\n\n---\n\n")
    body = "\n\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body + "\n", encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")

if __name__ == "__main__":
    main()

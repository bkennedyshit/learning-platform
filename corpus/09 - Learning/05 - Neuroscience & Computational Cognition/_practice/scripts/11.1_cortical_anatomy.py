#!/usr/bin/env python3
"""
11.1_cortical_anatomy.py — Practice problem generator & cortical layer plotter
for Chapter 11.1 (Neuroanatomy & The Cortex).

Generates randomized drill problems across 5 archetypes:
  1. Brodmann area identification (region → function)
  2. Cortical layer connectivity (which layer projects where?)
  3. Neuron density / surface area calculations
  4. Small-world coefficient computation
  5. Wilson-Cowan fixed-point stability check

Also provides --demo mode for a matplotlib cortical-layer schematic.

Usage:
  python 11.1_cortical_anatomy.py
  python 11.1_cortical_anatomy.py --count 10 --seed 42
  python 11.1_cortical_anatomy.py --demo
  python 11.1_cortical_anatomy.py --count 10 --out /tmp/_111.md

Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import random
import sys
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
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


BRODMANN_MAP = {
    4: ("Precentral gyrus", "Primary motor cortex (M1)"),
    6: ("Premotor/SMA", "Motor planning and supplementary motor"),
    17: ("Calcarine sulcus", "Primary visual cortex (V1)"),
    18: ("Peristriate", "Secondary visual cortex (V2)"),
    41: ("Superior temporal gyrus", "Primary auditory cortex (A1)"),
    3: ("Postcentral gyrus", "Primary somatosensory cortex (S1)"),
    44: ("Inferior frontal (pars opercularis)", "Broca's area — speech production"),
    22: ("Superior temporal (posterior)", "Wernicke's area — speech comprehension"),
    46: ("Dorsolateral PFC", "Working memory and executive function"),
    10: ("Frontopolar cortex", "Prospective memory and metacognition"),
    7: ("Superior parietal lobule", "Visuospatial processing and attention"),
    37: ("Fusiform gyrus", "Face and object recognition (FFA)"),
}

LAYER_OUTPUTS = {
    "I": "Molecular layer — contains apical dendrites and axon terminals; minimal cell bodies",
    "II/III": "External pyramidal — cortico-cortical projections (association + commissural fibers)",
    "IV": "Internal granular — receives thalamic afferents (spiny stellate cells)",
    "V": "Internal pyramidal — subcortical output (basal ganglia, brainstem, spinal cord)",
    "VI": "Polymorphic — corticothalamic feedback projections",
}


def gen_brodmann(rng: random.Random) -> Problem:
    ba, (region, function) = rng.choice(list(BRODMANN_MAP.items()))
    stmt = f"Identify the function and anatomical location of **Brodmann Area {ba}**."
    sol = f"**BA {ba}** is located in the **{region}**.\n\nFunction: **{function}**."
    return Problem("Brodmann area identification", stmt, sol)


def gen_layer_connectivity(rng: random.Random) -> Problem:
    layer, desc = rng.choice(list(LAYER_OUTPUTS.items()))
    stmt = f"What is the primary output target of cortical **Layer {layer}**? Describe the cell types found there."
    sol = f"**Layer {layer}**: {desc}"
    return Problem("Cortical layer connectivity", stmt, sol)


def gen_density_calc(rng: random.Random) -> Problem:
    density = rng.randint(50000, 80000)
    area_cm2 = rng.randint(2000, 3000)
    thickness_mm = round(rng.uniform(2.0, 3.5), 1)
    area_mm2 = area_cm2 * 100
    vol_mm3 = area_mm2 * thickness_mm
    n_total = density * vol_mm3
    stmt = (
        f"A cortical region has neuron density $\\rho = {density:,}$ neurons/mm³, "
        f"surface area $A = {area_cm2:,}$ cm², and mean thickness $\\bar{{t}} = {thickness_mm}$ mm. "
        f"Estimate the total neuron count."
    )
    sol = (
        f"Convert area: $A = {area_cm2:,} \\text{{ cm}}^2 \\times 100 = {area_mm2:,} \\text{{ mm}}^2$\n\n"
        f"Volume: $V = A \\times \\bar{{t}} = {area_mm2:,} \\times {thickness_mm} = {vol_mm3:,.0f} \\text{{ mm}}^3$\n\n"
        f"Total neurons: $N = \\rho \\cdot V = {density:,} \\times {vol_mm3:,.0f} = {n_total:,.0f}$ "
        f"$\\approx {n_total:.2e}$"
    )
    return Problem("Neuron density calculation", stmt, sol)


def gen_small_world(rng: random.Random) -> Problem:
    C = round(rng.uniform(0.3, 0.6), 3)
    L = round(rng.uniform(2.0, 4.0), 2)
    C_rand = round(rng.uniform(0.05, 0.15), 3)
    L_rand = round(rng.uniform(1.8, 3.0), 2)
    gamma = round(C / C_rand, 3)
    lam = round(L / L_rand, 3)
    sigma = round(gamma / lam, 3)
    stmt = (
        f"A cortical network has $C = {C}$, $L = {L}$. "
        f"Equivalent random graphs have $C_{{\\text{{rand}}}} = {C_rand}$, $L_{{\\text{{rand}}}} = {L_rand}$. "
        f"Compute the small-world coefficient $\\sigma$."
    )
    sol = (
        f"$\\gamma = C/C_{{\\text{{rand}}}} = {C}/{C_rand} = {gamma}$\n\n"
        f"$\\lambda = L/L_{{\\text{{rand}}}} = {L}/{L_rand} = {lam}$\n\n"
        f"$\\sigma = \\gamma / \\lambda = {gamma}/{lam} = {sigma}$\n\n"
        + (f"Since $\\sigma = {sigma} > 1$, this is a **small-world network**. ✓"
           if sigma > 1 else f"$\\sigma = {sigma} \\leq 1$ — not small-world.")
    )
    return Problem("Small-world coefficient", stmt, sol)


def gen_wilson_cowan_stability(rng: random.Random) -> Problem:
    wEE = rng.randint(8, 16)
    wEI = rng.randint(2, 6)
    wIE = rng.randint(8, 16)
    wII = rng.randint(1, 4)
    tau_E = rng.choice([8, 10, 12, 15])
    tau_I = rng.choice([3, 5, 7])
    # At high-activity fixed point, S'≈0, so J ≈ diag(-1/τE, -1/τI) → stable
    # At low-activity, need to check
    stmt = (
        f"For Wilson-Cowan parameters $w_{{EE}}={wEE}$, $w_{{EI}}={wEI}$, "
        f"$w_{{IE}}={wIE}$, $w_{{II}}={wII}$, $\\tau_E={tau_E}$ ms, $\\tau_I={tau_I}$ ms: "
        f"At the high-activity fixed point where $S'(x) \\approx 0$, determine stability."
    )
    j11 = -1.0 / tau_E
    j22 = -1.0 / tau_I
    tr_J = j11 + j22
    det_J = j11 * j22
    sol = (
        f"At saturation ($S' \\approx 0$), the Jacobian simplifies to:\n\n"
        f"$$\n\\mathbf{{J}} \\approx \\begin{{pmatrix}} -1/\\tau_E & 0 \\\\ 0 & -1/\\tau_I \\end{{pmatrix}} "
        f"= \\begin{{pmatrix}} {j11:.4f} & 0 \\\\ 0 & {j22:.4f} \\end{{pmatrix}}\n$$\n\n"
        f"$\\text{{tr}}(\\mathbf{{J}}) = {tr_J:.4f} < 0$ ✓\n\n"
        f"$\\det(\\mathbf{{J}}) = {det_J:.6f} > 0$ ✓\n\n"
        f"Both eigenvalues are real and negative → **stable node**."
    )
    return Problem("Wilson-Cowan stability", stmt, sol)


GENERATORS = [gen_brodmann, gen_layer_connectivity, gen_density_calc, gen_small_world, gen_wilson_cowan_stability]


def generate_problem_set(count: int, seed: int) -> list[Problem]:
    rng = random.Random(seed)
    problems = []
    for i in range(count):
        gen = GENERATORS[i % len(GENERATORS)]
        problems.append(gen(rng))
    return problems


def run_demo():
    """Produce a matplotlib cortical-layer schematic."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("matplotlib required for --demo. Install: pip install matplotlib")
        sys.exit(1)

    layers = [
        ("I — Molecular", 0.8, "#4a90d9"),
        ("II — Ext. Granular", 1.0, "#7ab648"),
        ("III — Ext. Pyramidal", 1.5, "#e6a817"),
        ("IV — Int. Granular", 1.2, "#d94a4a"),
        ("V — Int. Pyramidal", 1.8, "#9b59b6"),
        ("VI — Polymorphic", 1.2, "#1abc9c"),
    ]
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    y = 0
    for name, thickness, color in layers:
        rect = mpatches.FancyBboxPatch((0.5, y), 4, thickness, boxstyle="round,pad=0.05",
                                        facecolor=color, alpha=0.4, edgecolor="black")
        ax.add_patch(rect)
        ax.text(2.5, y + thickness / 2, name, ha="center", va="center", fontsize=11, fontweight="bold")
        y += thickness

    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, y + 0.5)
    ax.set_ylabel("Depth from pia (relative)")
    ax.set_title("Cortical Laminar Architecture (Schematic)")
    ax.set_xticks([])
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("cortical_layers_demo.png", dpi=150)
    print("Saved: cortical_layers_demo.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="11.1 Cortical Anatomy practice problems")
    parser.add_argument("--count", type=int, default=10, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output markdown file path")
    parser.add_argument("--demo", action="store_true", help="Run matplotlib cortical layer demo")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    problems = generate_problem_set(args.count, seed)

    header = (
        "---\n"
        "tags: [review/neuro, neuroanatomy, cortex, practice]\n"
        f"generated: seed={seed}\n"
        "---\n\n"
        "# 11.1 Practice — Neuroanatomy & The Cortex\n\n"
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

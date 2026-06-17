#!/usr/bin/env python3
"""
13.4_hrv_analysis.py — Practice problem generator for Chapter 13.4
(Autonomic Nervous System Telemetry - HRV).

Archetypes:
  1. RMSSD computation from R-R intervals
  2. SDNN and pNN50 computation
  3. Frequency-domain band power interpretation
  4. Poincaré SD1/SD2 calculation
  5. Overtraining detection from HRV trend

Generates synthetic R-R data deterministically from --seed.

Usage:
  python 13.4_hrv_analysis.py --count 10 --seed 42
"""
from __future__ import annotations

import argparse
import math
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


def _gen_rr_sample(rng: random.Random, n: int = 8, mean: float = 1818.0) -> list[int]:
    """Generate a short R-R sample around a mean."""
    return [int(mean + rng.randint(-120, 120)) for _ in range(n)]


def gen_rmssd(rng: random.Random) -> Problem:
    rr = _gen_rr_sample(rng, n=8)
    diffs = [rr[i+1] - rr[i] for i in range(len(rr)-1)]
    sq_diffs = [d**2 for d in diffs]
    mean_sq = sum(sq_diffs) / len(sq_diffs)
    rmssd = math.sqrt(mean_sq)

    stmt = f"R-R intervals (ms): {rr}\n\nCompute RMSSD."
    sol = (
        f"Successive differences: {diffs}\n\n"
        f"Squared: {sq_diffs}\n\n"
        f"Mean of squares: ${sum(sq_diffs)}/{len(sq_diffs)} = {mean_sq:.1f}$\n\n"
        f"$RMSSD = \\sqrt{{{mean_sq:.1f}}} = {rmssd:.2f}$ ms"
    )
    return Problem("RMSSD computation", stmt, sol)


def gen_sdnn_pnn50(rng: random.Random) -> Problem:
    rr = _gen_rr_sample(rng, n=10)
    mean_rr = sum(rr) / len(rr)
    var = sum((x - mean_rr)**2 for x in rr) / (len(rr) - 1)
    sdnn = math.sqrt(var)
    diffs = [abs(rr[i+1] - rr[i]) for i in range(len(rr)-1)]
    nn50 = sum(1 for d in diffs if d > 50)
    pnn50 = nn50 / (len(rr)-1) * 100

    stmt = f"R-R intervals (ms): {rr}\n\nCompute SDNN and pNN50."
    sol = (
        f"Mean RR = {mean_rr:.1f} ms (HR = {60000/mean_rr:.1f} BPM)\n\n"
        f"$SDNN = \\sqrt{{Var}} = {sdnn:.2f}$ ms\n\n"
        f"|ΔRR| values: {diffs}\n\n"
        f"Count > 50 ms: {nn50} out of {len(rr)-1}\n\n"
        f"$pNN50 = {nn50}/{len(rr)-1} \\times 100 = {pnn50:.1f}\\%$"
    )
    return Problem("SDNN & pNN50", stmt, sol)


def gen_frequency_domain(rng: random.Random) -> Problem:
    vlf = rng.randint(500, 2000)
    lf = rng.randint(300, 1500)
    hf = rng.randint(800, 4000)
    total = vlf + lf + hf
    lf_hf = lf / hf
    lf_nu = lf / (lf + hf) * 100
    hf_nu = hf / (lf + hf) * 100

    stmt = (
        f"HRV spectral analysis: VLF = {vlf} ms², LF = {lf} ms², HF = {hf} ms².\n\n"
        "Compute LF/HF ratio, normalized units, and interpret."
    )
    interp = "Parasympathetic dominant" if lf_hf < 1.0 else "Sympathetic dominant"
    sol = (
        f"$LF/HF = {lf}/{hf} = {lf_hf:.3f}$\n\n"
        f"$LF_{{nu}} = {lf}/({lf}+{hf}) \\times 100 = {lf_nu:.1f}\\%$\n\n"
        f"$HF_{{nu}} = {hf}/({lf}+{hf}) \\times 100 = {hf_nu:.1f}\\%$\n\n"
        f"Total power = {total} ms²\n\n"
        f"Interpretation: {interp} (LF/HF {'<' if lf_hf < 1 else '>'} 1.0)"
    )
    return Problem("Frequency-domain interpretation", stmt, sol)


def gen_poincare(rng: random.Random) -> Problem:
    rr = _gen_rr_sample(rng, n=12)
    arr = np.array(rr, dtype=float)
    diffs = np.diff(arr)
    rmssd = float(np.sqrt(np.mean(diffs**2)))
    sd1 = rmssd / math.sqrt(2)
    sdnn = float(np.std(arr, ddof=1))
    sd2 = math.sqrt(max(0, 2 * sdnn**2 - sd1**2))

    stmt = f"R-R intervals (ms): {rr}\n\nCompute Poincaré SD1 and SD2."
    sol = (
        f"$RMSSD = {rmssd:.2f}$ ms\n\n"
        f"$SD1 = RMSSD/\\sqrt{{2}} = {rmssd:.2f}/1.414 = {sd1:.2f}$ ms\n\n"
        f"$SDNN = {sdnn:.2f}$ ms\n\n"
        f"$SD2 = \\sqrt{{2 \\times SDNN^2 - SD1^2}} = \\sqrt{{2\\times{sdnn:.2f}^2 - {sd1:.2f}^2}} = {sd2:.2f}$ ms"
    )
    return Problem("Poincaré SD1/SD2", stmt, sol)


def gen_overtraining(rng: random.Random) -> Problem:
    baseline = rng.randint(90, 120)
    days = [baseline - rng.randint(0, i*8) for i in range(7)]
    days = [max(d, 30) for d in days]
    mean_d = sum(days) / 7
    threshold = baseline - 15

    stmt = (
        f"Athlete baseline RMSSD = {baseline} ms. "
        f"7-day morning readings: {days}\n\n"
        "At what day should training load be reduced (threshold: baseline - 15 ms)?"
    )
    alert_day = next((i+1 for i, d in enumerate(days) if d < threshold), None)
    sol = (
        f"Threshold = {baseline} - 15 = {threshold} ms\n\n"
        f"Day values below threshold: {[(i+1, d) for i, d in enumerate(days) if d < threshold]}\n\n"
        f"**Alert on Day {alert_day}** — reduce training load."
        if alert_day else "No day crosses threshold — training load is sustainable."
    )
    return Problem("Overtraining detection", stmt, sol)


GENERATORS = [gen_rmssd, gen_sdnn_pnn50, gen_frequency_domain, gen_poincare, gen_overtraining]


def main():
    parser = argparse.ArgumentParser(description="13.4 HRV Analysis practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [GENERATORS[i % len(GENERATORS)](rng) for i in range(args.count)]

    header = (
        "---\ntags: [review/biomech, HRV, autonomic, practice]\ndate: 2026-05-23\n---\n\n"
        "# 13.4 HRV Analysis — Practice Problems\n\n#review/biomech\n\n"
    )
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

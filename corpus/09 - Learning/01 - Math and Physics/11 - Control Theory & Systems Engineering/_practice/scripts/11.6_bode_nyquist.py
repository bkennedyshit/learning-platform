#!/usr/bin/env python3
"""
11.6_bode_nyquist.py — Practice problem generator for Chapter 11.6
(Frequency Response - Bode & Nyquist).

Archetypes:
  1. Bode magnitude at a given frequency
  2. Phase margin computation
  3. Gain margin computation
  4. Break frequency identification
  5. Nyquist encirclement counting

Usage:
  python 11.6_bode_nyquist.py --count 10 --seed 42
"""
from __future__ import annotations
import argparse, random, math
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str
    def render(self, idx: int) -> str:
        return (f"### Problem {idx} — {self.archetype}\n\n"
                f"{self.statement_md}\n\n<details>\n\n"
                f"<summary>Show solution</summary>\n\n{self.solution_md}\n\n</details>\n")

def gen_bode_magnitude(rng: random.Random) -> Problem:
    K = rng.randint(5, 50)
    p = rng.randint(2, 10)
    omega = rng.choice([1, 2, 5, 10])
    # G(jw) = K / (jw(jw + p))
    mag = K / (omega * math.sqrt(omega**2 + p**2))
    mag_db = 20 * math.log10(mag)
    stmt = (f"Compute $|G(j{omega})|$ in dB for $G(s) = {K}/(s(s+{p}))$.")
    sol = (f"$|G(j{omega})| = {K}/({omega}\\sqrt{{{omega}^2+{p}^2}}) = "
           f"{K}/({omega}\\cdot{math.sqrt(omega**2+p**2):.3f}) = {mag:.4f}$\n\n"
           f"$= 20\\log_{{10}}({mag:.4f}) = {mag_db:.2f}$ dB")
    return Problem("Bode magnitude calculation", stmt, sol)

def gen_phase_margin(rng: random.Random) -> Problem:
    K = rng.randint(5, 30)
    p1 = rng.randint(2, 6)
    p2 = rng.randint(p1+2, 12)
    # G(s) = K/(s+p1)(s+p2), find gain crossover then PM
    # At low freq this is approx K/(p1*p2) so let's use G(s) = K/s(s+p1)
    # |G(jw)| = K/(w*sqrt(w^2+p1^2)) = 1
    # K^2 = w^2(w^2+p1^2), solve for w
    # w^4 + p1^2*w^2 - K^2 = 0
    disc = p1**4 + 4*K**2
    w_gc_sq = (-p1**2 + math.sqrt(disc)) / 2
    w_gc = math.sqrt(w_gc_sq)
    phase = -90 - math.degrees(math.atan(w_gc/p1))
    PM = 180 + phase
    stmt = f"Find the phase margin for $G(s) = {K}/(s(s+{p1}))$ with unity feedback."
    sol = (f"Gain crossover: $\\omega_{{gc}} = {w_gc:.3f}$ rad/s\n\n"
           f"Phase: $-90° - \\arctan({w_gc:.3f}/{p1}) = {phase:.1f}°$\n\n"
           f"$PM = 180° + ({phase:.1f}°) = {PM:.1f}°$")
    return Problem("Phase margin", stmt, sol)

def gen_gain_margin(rng: random.Random) -> Problem:
    p1 = rng.randint(1, 4)
    p2 = rng.randint(p1+1, 8)
    K = rng.randint(5, 40)
    # G(s) = K/(s(s+p1)(s+p2))
    # Phase crossover: -90 - atan(w/p1) - atan(w/p2) = -180
    # atan(w/p1) + atan(w/p2) = 90 => (w/p1)(w/p2) = 1 => w = sqrt(p1*p2)
    w_pc = math.sqrt(p1 * p2)
    mag_at_pc = K / (w_pc * math.sqrt(w_pc**2 + p1**2) * math.sqrt(w_pc**2 + p2**2))
    GM_db = -20 * math.log10(mag_at_pc)
    stmt = f"Find the gain margin (dB) for $G(s) = {K}/(s(s+{p1})(s+{p2}))$."
    sol = (f"Phase crossover: $\\omega_{{pc}} = \\sqrt{{{p1}\\cdot{p2}}} = {w_pc:.3f}$ rad/s\n\n"
           f"$|G(j\\omega_{{pc}})| = {mag_at_pc:.4f}$\n\n"
           f"$GM = -20\\log_{{10}}({mag_at_pc:.4f}) = {GM_db:.2f}$ dB")
    return Problem("Gain margin", stmt, sol)

def gen_break_freq(rng: random.Random) -> Problem:
    poles = sorted([rng.randint(1, 5), rng.randint(6, 20)])
    K = rng.randint(2, 10) * poles[0] * poles[1]
    stmt = (f"Identify break frequencies and asymptotic slopes for "
            f"$G(s) = {K}/((s/{poles[0]}+1)(s/{poles[1]}+1))$.")
    K_dc = K / (1*1)
    sol = (f"Break frequencies: $\\omega_1 = {poles[0]}$, $\\omega_2 = {poles[1]}$ rad/s\n\n"
           f"DC gain: $20\\log({K_dc}) = {20*math.log10(K_dc):.1f}$ dB\n\n"
           f"Slopes: 0 dB/dec ($\\omega<{poles[0]}$), -20 dB/dec (${poles[0]}<\\omega<{poles[1]}$), "
           f"-40 dB/dec ($\\omega>{poles[1]}$)")
    return Problem("Break frequency identification", stmt, sol)

GENERATORS = [gen_bode_magnitude, gen_phase_margin, gen_gain_margin, gen_break_freq]

def main():
    parser = argparse.ArgumentParser(description="Ch 11.6 practice generator")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]
    header = ("---\ntags: [practice, control-theory, bode, nyquist, frequency-response]\n"
              "type: practice\n---\n# 11.6 Practice — Frequency Response (Bode & Nyquist)\n\n")
    body = "\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()

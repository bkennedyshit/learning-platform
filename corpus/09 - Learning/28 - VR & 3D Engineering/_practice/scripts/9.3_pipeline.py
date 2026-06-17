#!/usr/bin/env python3
"""
9.3_pipeline.py — Practice problem generator for Chapter 9.3
(Graphics Rendering Pipeline: rasterization, clipping, barycentric coords).

Generates randomized drill problems across 5 archetypes:
  1. Edge function point-in-triangle test
  2. Barycentric coordinate computation
  3. Clip-space line-plane intersection
  4. Perspective-correct interpolation
  5. Depth buffer precision analysis

Usage:
  python 9.3_pipeline.py
  python 9.3_pipeline.py --count 15 --seed 99
  python 9.3_pipeline.py --count 15 --seed 99 --out /tmp/_93.md
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
            f"{self.statement_md}\n\n"
            "?\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def edge_fn(a, b, p):
    return (p[0]-a[0])*(b[1]-a[1]) - (p[1]-a[1])*(b[0]-a[0])


def gen_edge_test(rng):
    v0 = np.array([rng.randint(50,150), rng.randint(50,100)])
    v1 = np.array([rng.randint(200,350), rng.randint(50,100)])
    v2 = np.array([rng.randint(100,250), rng.randint(200,300)])
    p = np.array([rng.randint(100,250), rng.randint(80,200)])
    e01 = edge_fn(v0, v1, p)
    e12 = edge_fn(v1, v2, p)
    e20 = edge_fn(v2, v0, p)
    area = edge_fn(v0, v1, v2)
    inside = (e01>=0 and e12>=0 and e20>=0) if area>0 else (e01<=0 and e12<=0 and e20<=0)
    stmt = (f"Triangle: $v_0=({v0[0]},{v0[1]})$, $v_1=({v1[0]},{v1[1]})$, "
            f"$v_2=({v2[0]},{v2[1]})$. Is $p=({p[0]},{p[1]})$ inside?")
    sol = (f"$E_{{01}}(p) = {e01}$, $E_{{12}}(p) = {e12}$, $E_{{20}}(p) = {e20}$\n\n"
           f"Triangle area sign: ${area}$ ({'CCW' if area>0 else 'CW'})\n\n"
           f"Point is **{'inside' if inside else 'outside'}**.")
    return Problem("Edge Function Test", stmt, sol)


def gen_barycentric(rng):
    v0 = np.array([rng.randint(0,100), rng.randint(0,50)], dtype=float)
    v1 = np.array([rng.randint(200,300), rng.randint(0,50)], dtype=float)
    v2 = np.array([rng.randint(100,200), rng.randint(150,250)], dtype=float)
    t1, t2 = rng.random()*0.6, rng.random()*0.3
    t0 = 1 - t1 - t2
    p = t0*v0 + t1*v1 + t2*v2
    area = edge_fn(v0, v1, v2)
    l0 = edge_fn(v1, v2, p) / area
    l1 = edge_fn(v2, v0, p) / area
    l2 = edge_fn(v0, v1, p) / area
    stmt = (f"Compute barycentric coordinates of $p=({p[0]:.1f},{p[1]:.1f})$ in triangle "
            f"$v_0=({v0[0]:.0f},{v0[1]:.0f})$, $v_1=({v1[0]:.0f},{v1[1]:.0f})$, $v_2=({v2[0]:.0f},{v2[1]:.0f})$.")
    sol = (f"$\\lambda_0 = {l0:.4f}$, $\\lambda_1 = {l1:.4f}$, $\\lambda_2 = {l2:.4f}$\n\n"
           f"Sum: ${l0+l1+l2:.6f} \\approx 1$ ✓")
    return Problem("Barycentric Coordinates", stmt, sol)


def gen_clip_intersect(rng):
    # Generate a vertex inside and one outside the right clip plane (x <= w)
    wA = rng.randint(2, 6)
    xA = wA + rng.randint(1, 4)  # outside
    yA, zA = rng.randint(-3, 3), rng.randint(-5, -1)
    wB = rng.randint(2, 8)
    xB = wB - rng.randint(1, 5)  # inside
    yB, zB = rng.randint(-3, 3), rng.randint(-5, -1)
    dA = xA - wA
    dB = xB - wB
    t = dA / (dA - dB)
    I = np.array([xA,yA,zA,wA]) + t*(np.array([xB,yB,zB,wB]) - np.array([xA,yA,zA,wA]))
    stmt = (f"Clip edge $A=({xA},{yA},{zA},{wA})$ to $B=({xB},{yB},{zB},{wB})$ "
            f"against right plane ($x \\leq w$).")
    sol = (f"$d_A = {xA}-{wA} = {dA}$ (outside), $d_B = {xB}-{wB} = {dB}$ (inside)\n\n"
           f"$t = {dA}/({dA}-({dB})) = {t:.4f}$\n\n"
           f"$I = ({I[0]:.3f}, {I[1]:.3f}, {I[2]:.3f}, {I[3]:.3f})$\n\n"
           f"Verify: $x_I = {I[0]:.3f} = w_I = {I[3]:.3f}$ ✓")
    return Problem("Clip-Space Intersection", stmt, sol)


def gen_persp_correct(rng):
    w0 = rng.choice([1, 2, 3, 4])
    w1 = rng.choice([5, 8, 10, 16])
    u0 = rng.choice([0.0, 0.2, 0.5])
    u1 = rng.choice([0.8, 1.0])
    t = rng.choice([0.25, 0.5, 0.75])
    naive = (1-t)*u0 + t*u1
    uw_interp = (1-t)*u0/w0 + t*u1/w1
    w_interp = (1-t)/w0 + t/w1
    correct = uw_interp / w_interp
    stmt = (f"Vertices: $w_0={w0}$, $w_1={w1}$, $u_0={u0}$, $u_1={u1}$. "
            f"At screen-space $t={t}$, compute perspective-correct $u$.")
    sol = (f"Naive: $u = {naive:.4f}$ (WRONG)\n\n"
           f"$u/w$ interpolated: $(1-{t})\\cdot{u0}/{w0} + {t}\\cdot{u1}/{w1} = {uw_interp:.6f}$\n\n"
           f"$1/w$ interpolated: $(1-{t})/{w0} + {t}/{w1} = {w_interp:.6f}$\n\n"
           f"Correct: $u = {uw_interp:.6f}/{w_interp:.6f} = {correct:.4f}$")
    return Problem("Perspective-Correct Interpolation", stmt, sol)


def gen_depth_precision(rng):
    near = rng.choice([0.01, 0.1, 1.0])
    far = rng.choice([100, 500, 1000])
    z_view = -rng.uniform(near, far)
    z_ndc = (far+near)/(far-near) + 2*far*near/((far-near)*z_view)
    ratio = far/near
    stmt = (f"Near={near}, far={far}. Compute $z_{{ndc}}$ for $z_{{view}} = {z_view:.2f}$. "
            f"What is the near/far precision ratio?")
    sol = (f"$z_{{ndc}} = \\frac{{{far}+{near}}}{{{far}-{near}}} + "
           f"\\frac{{2 \\cdot {far} \\cdot {near}}}{{({far}-{near}) \\cdot ({z_view:.2f})}} = {z_ndc:.6f}$\n\n"
           f"Precision ratio $\\approx f/n = {ratio:.0f}$:1 (far region gets $1/{ratio:.0f}$ of depth precision)")
    return Problem("Depth Buffer Precision", stmt, sol)


GENERATORS = [gen_edge_test, gen_barycentric, gen_clip_intersect, gen_persp_correct, gen_depth_precision]


def main():
    parser = argparse.ArgumentParser(description="9.3 Pipeline practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    header = (
        "---\ntags: [review/3d, practice, rasterization, clipping, pipeline]\n---\n\n"
        "# 9.3 — Graphics Rendering Pipeline: Practice Problems\n\n"
        f"*Generated {args.count} problems (seed={args.seed})*\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i+1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

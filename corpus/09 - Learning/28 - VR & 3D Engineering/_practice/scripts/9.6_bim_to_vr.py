#!/usr/bin/env python3
"""
9.6_bim_to_vr.py — Practice problem generator for Chapter 9.6
(AEC to VR Pipelines: IFC parsing, mesh decimation, optimization stats).

Generates randomized drill problems across 5 archetypes:
  1. IFC entity hierarchy identification
  2. Mesh decimation ratio calculation
  3. Draw call budget planning
  4. LOD switching distance computation
  5. Texture atlas memory estimation

Also includes a demo mesh decimation function using numpy
(simulating quadric error collapse without full mesh library).

Usage:
  python 9.6_bim_to_vr.py
  python 9.6_bim_to_vr.py --count 12 --seed 42
  python 9.6_bim_to_vr.py --count 12 --seed 42 --out /tmp/_96.md
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


def gen_ifc_hierarchy(rng):
    entities = [
        ("IfcWall", "IfcBuildingElement", "vertical enclosure"),
        ("IfcSlab", "IfcBuildingElement", "horizontal surface (floor/roof)"),
        ("IfcDoor", "IfcBuildingElement", "opening element with swing"),
        ("IfcBeam", "IfcBuildingElement", "structural horizontal member"),
        ("IfcColumn", "IfcBuildingElement", "structural vertical member"),
        ("IfcSpace", "IfcSpatialElement", "occupiable volume (room)"),
        ("IfcBuildingStorey", "IfcSpatialStructureElement", "floor level container"),
    ]
    e = rng.choice(entities)
    stmt = f"In the IFC schema, what is `{e[0]}`? State its parent class and architectural role."
    sol = f"`{e[0]}` inherits from `{e[1]}`. Role: {e[2]}."
    return Problem("IFC Entity Hierarchy", stmt, sol)


def gen_decimation_ratio(rng):
    original = rng.choice([10_000_000, 25_000_000, 50_000_000, 100_000_000])
    target_platform = rng.choice([
        ("Quest 2 standalone", 500_000),
        ("PCVR (RTX 3080)", 5_000_000),
        ("WebXR (mobile browser)", 200_000),
    ])
    platform, budget = target_platform
    # Account for occlusion culling (~33% visible)
    visible_budget = budget
    total_budget = int(visible_budget * 3)  # total scene can be 3x visible
    ratio = original / total_budget
    stmt = (f"A BIM model has {original:,} triangles. Target: **{platform}** "
            f"(visible budget: {visible_budget:,} tris, assume 33% visibility ratio). "
            f"What total decimation ratio is needed?")
    sol = (f"Total scene budget = {visible_budget:,} / 0.33 ≈ {total_budget:,} tris\n\n"
           f"Required ratio: {original:,} / {total_budget:,} = **{ratio:.1f}:1**\n\n"
           f"Strategy: Decimation ({min(10, ratio):.0f}:1) × LOD ({ratio/min(10,ratio):.1f}:1 at distance)")
    return Problem("Decimation Ratio", stmt, sol)


def gen_draw_call_budget(rng):
    unique_mats = rng.randint(500, 3000)
    repeated_elements = rng.randint(1000, 10000)
    budget = rng.choice([100, 200, 500])
    # Strategies
    atlas_reduction = unique_mats / rng.randint(3, 8)
    instance_reduction = repeated_elements * 0.9  # 90% are instanceable
    final_calls = int(atlas_reduction - instance_reduction * 0.5 / atlas_reduction)
    final_calls = max(final_calls, int(unique_mats / 5))
    stmt = (f"Scene: {unique_mats} unique materials, {repeated_elements} repeated elements. "
            f"Draw call budget: {budget}. Design an optimization strategy.")
    sol = (f"1. **Texture atlasing:** {unique_mats} → ~{int(unique_mats/4)} atlased materials\n\n"
           f"2. **GPU instancing:** {repeated_elements} repeated → {int(repeated_elements*0.9)} instanced "
           f"(saves ~{int(repeated_elements*0.9)} draw calls)\n\n"
           f"3. **Static batching:** combine non-moving geometry sharing materials\n\n"
           f"Estimated final: ~{min(budget, int(unique_mats/4))} draw calls "
           f"({'✓ within budget' if int(unique_mats/4) <= budget else '⚠️ needs more optimization'})")
    return Problem("Draw Call Budget", stmt, sol)


def gen_lod_distance(rng):
    radius = rng.choice([0.1, 0.3, 0.5, 1.0, 2.0])
    error_cm = rng.choice([1, 2, 5, 10])
    error_m = error_cm / 100
    res_h = rng.choice([1832, 2160, 3840])
    fov = rng.choice([90, 100, 110])
    ppd = res_h / (fov * np.pi / 180)
    distance = error_m * ppd
    stmt = (f"Object radius: {radius}m, LOD error: {error_cm}cm. "
            f"Display: {res_h}px horizontal, {fov}° FOV. "
            f"At what distance is the error sub-pixel?")
    sol = (f"Pixels per radian: {res_h} / ({fov}° × π/180) = {ppd:.0f} px/rad\n\n"
           f"Sub-pixel when: error/distance × ppd < 1\n\n"
           f"$d > {error_m} × {ppd:.0f} = {distance:.1f}$ m\n\n"
           f"Switch to this LOD at distances > **{distance:.1f} m**")
    return Problem("LOD Switch Distance", stmt, sol)


def gen_texture_memory(rng):
    num_materials = rng.randint(50, 500)
    res = rng.choice([256, 512, 1024, 2048])
    channels = 4  # RGBA
    compression = rng.choice([("ASTC 4x4", 1.0), ("BC7", 1.0), ("Uncompressed", 4.0),
                               ("ASTC 8x8", 0.5), ("BC1", 0.5)])
    comp_name, bpp_factor = compression
    # ASTC 4x4 = 8 bpp = 1 byte/pixel, BC7 = 1 byte/pixel, uncompressed = 4 bytes/pixel
    bytes_per_pixel = bpp_factor
    total_bytes = num_materials * res * res * bytes_per_pixel
    total_mb = total_bytes / (1024 * 1024)
    stmt = (f"{num_materials} materials at {res}×{res}, format: {comp_name}. "
            f"Estimate total texture memory.")
    sol = (f"Per texture: {res}×{res} × {bytes_per_pixel} bytes/px = {res*res*bytes_per_pixel/1024:.0f} KB\n\n"
           f"Total: {num_materials} × {res*res*bytes_per_pixel/1024:.0f} KB = **{total_mb:.1f} MB**\n\n"
           + (f"{'✓ Within Quest budget (256 MB)' if total_mb < 256 else '⚠️ Exceeds Quest budget — reduce resolution or material count'}"))
    return Problem("Texture Memory Estimation", stmt, sol)


GENERATORS = [gen_ifc_hierarchy, gen_decimation_ratio, gen_draw_call_budget,
              gen_lod_distance, gen_texture_memory]


def main():
    parser = argparse.ArgumentParser(description="9.6 BIM-to-VR practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    header = (
        "---\ntags: [review/3d, practice, BIM, IFC, mesh-optimization, VR-pipeline]\n---\n\n"
        "# 9.6 — AEC to VR Pipelines: Practice Problems\n\n"
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

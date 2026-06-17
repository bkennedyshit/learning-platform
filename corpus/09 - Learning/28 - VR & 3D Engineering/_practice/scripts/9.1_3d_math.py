#!/usr/bin/env python3
"""
9.1_3d_math.py — Practice problem generator for Chapter 9.1
(3D Math Fundamentals: TRS matrices, coordinate spaces, perspective projection).

Generates randomized drill problems across 6 archetypes:
  1. Build a TRS model matrix and transform a vertex
  2. Compute the inverse of a TRS matrix
  3. Perspective projection: compute NDC from view-space point
  4. Rodrigues' rotation of a vector about an arbitrary axis
  5. Normal matrix computation under non-uniform scale
  6. View matrix (LookAt) construction

Usage:
  python 9.1_3d_math.py
  python 9.1_3d_math.py --count 20 --seed 42
  python 9.1_3d_math.py --count 20 --seed 42 --out /tmp/_91.md

Exit code 0 on success.
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


def _fmt_mat4(M: np.ndarray) -> str:
    """Format a 4x4 matrix as LaTeX pmatrix."""
    rows = []
    for i in range(4):
        row = " & ".join(f"{M[i,j]:.4g}" for j in range(4))
        rows.append(row)
    return "\\begin{pmatrix} " + " \\\\ ".join(rows) + " \\end{pmatrix}"


def _fmt_vec(v: np.ndarray) -> str:
    """Format a vector as LaTeX tuple."""
    return "(" + ", ".join(f"{x:.4g}" for x in v) + ")"


def translation_matrix(tx, ty, tz):
    M = np.eye(4)
    M[0, 3], M[1, 3], M[2, 3] = tx, ty, tz
    return M


def scale_matrix(sx, sy, sz):
    return np.diag([sx, sy, sz, 1.0])


def rotation_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]], dtype=np.float64)


def rotation_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.float64)


def perspective_matrix(fov_y, aspect, near, far):
    t = np.tan(fov_y / 2.0)
    return np.array([
        [1/(aspect*t), 0, 0, 0],
        [0, 1/t, 0, 0],
        [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
        [0, 0, -1, 0]
    ], dtype=np.float64)


# ---------------------------------------------------------------------------
# Archetype 1: TRS model matrix + vertex transform
# ---------------------------------------------------------------------------
def gen_trs_transform(rng: random.Random) -> Problem:
    tx, ty, tz = rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-10, -1)
    angle_deg = rng.choice([30, 45, 60, 90, 120, 180])
    sx, sy, sz = [rng.choice([1, 2, 3]) for _ in range(3)]
    vx, vy, vz = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)

    T = translation_matrix(tx, ty, tz)
    R = rotation_y(np.radians(angle_deg))
    S = scale_matrix(sx, sy, sz)
    M = T @ R @ S

    v_local = np.array([vx, vy, vz, 1.0])
    v_world = M @ v_local

    stmt = (
        f"An object is scaled by $({sx}, {sy}, {sz})$, rotated ${angle_deg}°$ about the $y$-axis, "
        f"then translated to $({tx}, {ty}, {tz})$. "
        f"Compute the world-space position of local vertex $\\mathbf{{v}} = ({vx}, {vy}, {vz})$."
    )
    sol = (
        f"$M = T \\cdot R_y({angle_deg}°) \\cdot S$\n\n"
        f"$$\nM = {_fmt_mat4(M)}\n$$\n\n"
        f"$\\mathbf{{v}}_{{\\text{{world}}}} = M \\cdot ({vx}, {vy}, {vz}, 1)^T = {_fmt_vec(v_world[:3])}$"
    )
    return Problem("TRS Model Matrix", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Inverse TRS
# ---------------------------------------------------------------------------
def gen_inverse_trs(rng: random.Random) -> Problem:
    tx, ty, tz = rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-8, -1)
    angle_deg = rng.choice([30, 45, 60, 90])
    sx, sy, sz = [rng.choice([1, 2, 4]) for _ in range(3)]

    T = translation_matrix(tx, ty, tz)
    R = rotation_y(np.radians(angle_deg))
    S = scale_matrix(sx, sy, sz)
    M = T @ R @ S
    M_inv = np.linalg.inv(M)

    stmt = (
        f"Given $M = T({tx},{ty},{tz}) \\cdot R_y({angle_deg}°) \\cdot S({sx},{sy},{sz})$, "
        f"compute $M^{{-1}}$ using the formula $S^{{-1}} R^T T^{{-1}}$."
    )
    sol = (
        f"$S^{{-1}} = S(1/{sx}, 1/{sy}, 1/{sz})$, $R^{{-1}} = R_y(-{angle_deg}°)$, "
        f"$T^{{-1}} = T({-tx},{-ty},{-tz})$.\n\n"
        f"$$\nM^{{-1}} = {_fmt_mat4(M_inv)}\n$$\n\n"
        f"Verify: $M \\cdot M^{{-1}} = I_4$. ✓"
    )
    return Problem("Inverse TRS Matrix", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Perspective projection
# ---------------------------------------------------------------------------
def gen_perspective(rng: random.Random) -> Problem:
    x = rng.uniform(-5, 5)
    y = rng.uniform(-3, 3)
    z = rng.uniform(-20, -1)
    fov_deg = rng.choice([60, 75, 90])
    aspect = 16/9

    P = perspective_matrix(np.radians(fov_deg), aspect, 0.1, 100.0)
    v = np.array([x, y, z, 1.0])
    clip = P @ v
    ndc = clip[:3] / clip[3]

    stmt = (
        f"A point is at view-space position $({x:.2f}, {y:.2f}, {z:.2f})$. "
        f"Camera: fov_y=${fov_deg}°$, aspect=$16:9$, near=$0.1$, far=$100$. "
        f"Compute the NDC coordinates after perspective projection."
    )
    sol = (
        f"Clip space: $({clip[0]:.4f}, {clip[1]:.4f}, {clip[2]:.4f}, {clip[3]:.4f})$\n\n"
        f"Perspective divide ($\\div w = {clip[3]:.4f}$):\n\n"
        f"NDC $= ({ndc[0]:.4f}, {ndc[1]:.4f}, {ndc[2]:.4f})$\n\n"
        + ("Point is **visible** (all coords in $[-1,1]$)." if all(abs(c) <= 1 for c in ndc) else
           "Point is **clipped** (outside $[-1,1]^3$).")
    )
    return Problem("Perspective Projection", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Rodrigues' rotation
# ---------------------------------------------------------------------------
def gen_rodrigues(rng: random.Random) -> Problem:
    # Random unit axis
    k = np.array([rng.randint(-2, 2), rng.randint(-2, 2), rng.randint(1, 3)], dtype=np.float64)
    k = k / np.linalg.norm(k)
    theta_deg = rng.choice([30, 45, 60, 90, 120])
    theta = np.radians(theta_deg)
    v = np.array([rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)], dtype=np.float64)

    # Rodrigues formula
    v_rot = v * np.cos(theta) + np.cross(k, v) * np.sin(theta) + k * np.dot(k, v) * (1 - np.cos(theta))

    stmt = (
        f"Rotate $\\mathbf{{v}} = {_fmt_vec(v)}$ by ${theta_deg}°$ about axis "
        f"$\\hat{{\\mathbf{{k}}}} = {_fmt_vec(k)}$ using Rodrigues' formula."
    )
    sol = (
        f"$\\mathbf{{v}}_\\parallel = (\\hat{{k}} \\cdot v)\\hat{{k}} = {np.dot(k,v):.4f} \\cdot \\hat{{k}}$\n\n"
        f"$\\hat{{k}} \\times \\mathbf{{v}} = {_fmt_vec(np.cross(k, v))}$\n\n"
        f"$\\mathbf{{v}}' = \\mathbf{{v}}\\cos{theta_deg}° + (\\hat{{k}} \\times \\mathbf{{v}})\\sin{theta_deg}° "
        f"+ \\hat{{k}}(\\hat{{k}} \\cdot \\mathbf{{v}})(1-\\cos{theta_deg}°)$\n\n"
        f"$\\mathbf{{v}}' = {_fmt_vec(v_rot)}$"
    )
    return Problem("Rodrigues' Rotation", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Normal matrix
# ---------------------------------------------------------------------------
def gen_normal_matrix(rng: random.Random) -> Problem:
    sx, sy, sz = rng.choice([1, 2, 3]), rng.choice([1, 2, 4]), rng.choice([1, 2, 3])
    angle_deg = rng.choice([30, 45, 60, 90])
    R = rotation_z(np.radians(angle_deg))[:3, :3]
    S = np.diag([sx, sy, sz]).astype(np.float64)
    M3 = R @ S
    N = np.linalg.inv(M3).T

    n = np.array([rng.choice([-1,0,1]), rng.choice([-1,0,1]), rng.choice([-1,0,1])], dtype=np.float64)
    if np.linalg.norm(n) == 0:
        n = np.array([0, 1, 0], dtype=np.float64)
    n = n / np.linalg.norm(n)

    n_transformed = N @ n
    n_normalized = n_transformed / np.linalg.norm(n_transformed)

    stmt = (
        f"Model matrix (3×3) = $R_z({angle_deg}°) \\cdot S({sx},{sy},{sz})$. "
        f"Compute the normal matrix $N = (M^{{-1}})^T$ and transform normal $\\hat{{n}} = {_fmt_vec(n)}$."
    )
    sol = (
        f"$M^{{-1}} = S^{{-1}} R^T$, $N = (M^{{-1}})^T = R \\cdot S^{{-1}}$ (for this decomposition).\n\n"
        f"$N \\hat{{n}} = {_fmt_vec(n_transformed)}$\n\n"
        f"Normalized: $\\hat{{n}}' = {_fmt_vec(n_normalized)}$"
    )
    return Problem("Normal Matrix", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 6: LookAt view matrix
# ---------------------------------------------------------------------------
def gen_lookat(rng: random.Random) -> Problem:
    eye = np.array([rng.randint(-5, 5), rng.randint(1, 10), rng.randint(5, 15)], dtype=np.float64)
    target = np.array([rng.randint(-3, 3), 0, rng.randint(-3, 3)], dtype=np.float64)
    up = np.array([0, 1, 0], dtype=np.float64)

    f = target - eye
    f = f / np.linalg.norm(f)
    r = np.cross(f, up)
    r = r / np.linalg.norm(r)
    u = np.cross(r, f)

    V = np.eye(4)
    V[0, :3] = r
    V[1, :3] = u
    V[2, :3] = -f
    V[0, 3] = -np.dot(r, eye)
    V[1, 3] = -np.dot(u, eye)
    V[2, 3] = np.dot(f, eye)

    stmt = (
        f"Compute the view matrix for camera at $\\mathbf{{e}} = {_fmt_vec(eye)}$, "
        f"looking at $\\mathbf{{t}} = {_fmt_vec(target)}$, world up $= (0,1,0)$."
    )
    sol = (
        f"$\\hat{{f}} = {_fmt_vec(f)}$\n\n"
        f"$\\hat{{r}} = {_fmt_vec(r)}$\n\n"
        f"$\\hat{{u}} = {_fmt_vec(u)}$\n\n"
        f"$$\nV = {_fmt_mat4(V)}\n$$"
    )
    return Problem("LookAt View Matrix", stmt, sol)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
GENERATORS = [gen_trs_transform, gen_inverse_trs, gen_perspective,
              gen_rodrigues, gen_normal_matrix, gen_lookat]


def main():
    parser = argparse.ArgumentParser(description="9.1 3D Math practice problems")
    parser.add_argument("--count", type=int, default=12, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems = []
    for i in range(args.count):
        gen = rng.choice(GENERATORS)
        problems.append(gen(rng))

    header = (
        "---\n"
        "tags: [review/3d, practice, trs-matrices, projection, coordinate-spaces]\n"
        "---\n\n"
        "# 9.1 — 3D Math Fundamentals: Practice Problems\n\n"
        f"*Generated {args.count} problems (seed={args.seed})*\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(output)} bytes to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

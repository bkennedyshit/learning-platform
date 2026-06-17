#!/usr/bin/env python3
"""
10.3_cnn_vit.py — Practice problem generator for Chapter 10.3
(Computer Vision: CNNs & Vision Transformers).

Archetypes:
  1. Compute conv2d output by hand (small input + kernel)
  2. Output dimension calculation
  3. Parameter count for a CNN architecture
  4. Receptive field calculation
  5. ViT patch embedding dimensions

Usage:
  python 10.3_cnn_vit.py --count 10 --seed 42
  python 10.3_cnn_vit.py --demo
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
            f"{self.statement_md}\n\n?\n\n"
            "<details>\n\n<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n</details>\n"
        )


def gen_conv_manual(rng: random.Random) -> Problem:
    H, W, k = 4, 4, 3
    I = np.array([[rng.randint(-2, 3) for _ in range(W)] for _ in range(H)])
    K = np.array([[rng.choice([-1, 0, 1]) for _ in range(k)] for _ in range(k)])
    Ho, Wo = H - k + 1, W - k + 1
    O = np.zeros((Ho, Wo), dtype=int)
    for i in range(Ho):
        for j in range(Wo):
            O[i, j] = int(np.sum(I[i:i+k, j:j+k] * K))

    def mat_str(m):
        rows = [" & ".join(str(int(v)) for v in row) for row in m]
        return "\\begin{pmatrix}" + "\\\\".join(rows) + "\\end{pmatrix}"

    stmt = (
        f"Compute $(I * K)$ for:\n\n"
        f"$I = {mat_str(I)}$, $K = {mat_str(K)}$"
    )
    sol = f"Output: $O = {mat_str(O)}$\n\nComputed element-wise: each entry is the dot product of the kernel with the corresponding $3\\times3$ patch."
    return Problem("Manual convolution", stmt, sol)


def gen_output_dim(rng: random.Random) -> Problem:
    H = rng.choice([28, 32, 56, 112, 224])
    k = rng.choice([3, 5, 7])
    s = rng.choice([1, 2])
    p = rng.choice([0, 1, k // 2])
    Ho = (H + 2*p - k) // s + 1
    stmt = (
        f"Input size $H = {H}$, kernel $k = {k}$, stride $s = {s}$, padding $p = {p}$. "
        "Compute the output spatial dimension."
    )
    sol = f"$H_{{out}} = \\lfloor({H} + 2\\cdot{p} - {k})/{s}\\rfloor + 1 = \\lfloor{H+2*p-k}/{s}\\rfloor + 1 = {Ho}$"
    return Problem("Output dimension", stmt, sol)


def gen_param_count(rng: random.Random) -> Problem:
    cin = rng.choice([1, 3, 16, 32, 64])
    cout = rng.choice([16, 32, 64, 128])
    k = rng.choice([3, 5])
    params = cout * (cin * k * k + 1)
    stmt = f"Conv layer: $C_{{in}}={cin}$, $C_{{out}}={cout}$, kernel ${k}\\times{k}$, with bias. Count parameters."
    sol = f"$C_{{out}} \\times (C_{{in}} \\times k^2 + 1) = {cout} \\times ({cin} \\times {k*k} + 1) = {cout} \\times {cin*k*k+1} = {params}$"
    return Problem("CNN parameter count", stmt, sol)


def gen_receptive_field(rng: random.Random) -> Problem:
    n_layers = rng.randint(2, 5)
    kernels = [rng.choice([3, 5]) for _ in range(n_layers)]
    strides = [rng.choice([1, 2]) for _ in range(n_layers)]
    rf = 1
    for l in range(n_layers):
        jump = 1
        for j in range(l):
            jump *= strides[j]
        rf += (kernels[l] - 1) * jump
    layers_str = ", ".join(f"(k={kernels[i]}, s={strides[i]})" for i in range(n_layers))
    stmt = f"Compute the receptive field for {n_layers} conv layers: {layers_str}."
    sol = (
        f"$RF = 1 + \\sum_{{\\ell=1}}^{{{n_layers}}} (k_\\ell - 1)\\prod_{{j=1}}^{{\\ell-1}}s_j = {rf}$"
    )
    return Problem("Receptive field", stmt, sol)


def gen_vit_dims(rng: random.Random) -> Problem:
    img = rng.choice([224, 256, 384])
    patch = rng.choice([8, 16, 32])
    D = rng.choice([384, 512, 768, 1024])
    N = (img // patch) ** 2
    embed_params = D * (3 * patch * patch)
    stmt = (
        f"ViT with image size ${img}\\times{img}$, patch size ${patch}\\times{patch}$, "
        f"embedding dim $D={D}$. Compute: (a) number of patches, (b) sequence length, "
        "(c) patch embedding parameters."
    )
    sol = (
        f"(a) $N = ({img}/{patch})^2 = {img//patch}^2 = {N}$ patches.\n\n"
        f"(b) Sequence length = $N + 1 = {N+1}$ (with [CLS] token).\n\n"
        f"(c) Embedding: $D \\times (3 \\times P^2) = {D} \\times {3*patch*patch} = {embed_params}$ params."
    )
    return Problem("ViT dimensions", stmt, sol)


def run_demo():
    """Demo: manual conv2d + PyTorch verification."""
    print("=" * 60)
    print("DEMO: Manual Conv2D vs NumPy")
    print("=" * 60)
    I = np.array([[1,2,0,1],[3,1,2,0],[0,1,3,2],[2,0,1,1]], dtype=float)
    K = np.array([[1,0,-1],[1,0,-1],[1,0,-1]], dtype=float)
    H, W = I.shape
    k = K.shape[0]
    Ho, Wo = H-k+1, W-k+1
    O = np.zeros((Ho, Wo))
    for i in range(Ho):
        for j in range(Wo):
            O[i,j] = np.sum(I[i:i+k, j:j+k] * K)
    print(f"Input ({H}x{W}):\n{I}")
    print(f"\nKernel ({k}x{k}):\n{K}")
    print(f"\nOutput ({Ho}x{Wo}):\n{O}")
    print(f"\nThis kernel detects vertical edges (Sobel-x like).")

    try:
        import torch
        import torch.nn.functional as F
        It = torch.tensor(I).unsqueeze(0).unsqueeze(0).float()
        Kt = torch.tensor(K).unsqueeze(0).unsqueeze(0).float()
        Ot = F.conv2d(It, Kt)
        print(f"\nPyTorch verification:\n{Ot.squeeze().numpy()}")
        assert np.allclose(O, Ot.squeeze().numpy()), "Mismatch!"
        print("✓ Manual matches PyTorch.")
    except ImportError:
        print("\n(PyTorch not available for verification)")


GENERATORS = [gen_conv_manual, gen_output_dim, gen_param_count, gen_receptive_field, gen_vit_dims]


def main():
    parser = argparse.ArgumentParser(description="10.3 CNN/ViT practice problems")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    rng = random.Random(args.seed)
    problems = [rng.choice(GENERATORS)(rng) for _ in range(args.count)]

    lines = ["---", "tags: [review/ai, cnn, convolution, vision-transformer]",
             "generated: true", "---", "", "# 10.3 CNNs & ViTs — Practice Problems", ""]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(problems)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
1.15_gpu_cuda.py — Hands-on lab for Chapter 1.15 (GPU Computing & CUDA).

Detects GPU hardware, checks CUDA availability, benchmarks basic operations.

Usage:
  python 1.15_gpu_cuda.py --out ../1.15_lab_report.md
  python 1.15_gpu_cuda.py --demo
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path


def check_cuda() -> dict[str, str]:
    info = {}
    try:
        import torch
        info["pytorch_version"] = torch.__version__
        info["cuda_available"] = str(torch.cuda.is_available())
        if torch.cuda.is_available():
            info["cuda_version"] = torch.version.cuda or "N/A"
            info["device_count"] = str(torch.cuda.device_count())
            info["device_name"] = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            info["total_memory_gb"] = f"{props.total_mem / (1024**3):.1f}"
            info["compute_capability"] = f"{props.major}.{props.minor}"
            info["sm_count"] = str(props.multi_processor_count)
        else:
            info["note"] = "No CUDA GPU detected (CPU-only mode)"
    except ImportError:
        info["pytorch_version"] = "NOT INSTALLED"
        info["cuda_available"] = "False (PyTorch not installed)"

    try:
        import numba
        info["numba_version"] = numba.__version__
        from numba import cuda as numba_cuda
        info["numba_cuda"] = str(numba_cuda.is_available())
    except ImportError:
        info["numba_version"] = "NOT INSTALLED"

    return info


def benchmark_matmul() -> dict[str, str]:
    """Benchmark matrix multiply on CPU vs GPU."""
    try:
        import torch
        n = 2048
        # CPU
        a_cpu = torch.randn(n, n)
        start = time.perf_counter()
        _ = a_cpu @ a_cpu
        cpu_time = time.perf_counter() - start

        result = {"cpu_matmul_2048_ms": f"{cpu_time * 1000:.1f}"}

        if torch.cuda.is_available():
            a_gpu = torch.randn(n, n, device="cuda")
            torch.cuda.synchronize()
            start = time.perf_counter()
            _ = a_gpu @ a_gpu
            torch.cuda.synchronize()
            gpu_time = time.perf_counter() - start
            result["gpu_matmul_2048_ms"] = f"{gpu_time * 1000:.2f}"
            result["speedup"] = f"{cpu_time / gpu_time:.1f}x"
        return result
    except ImportError:
        return {"error": "PyTorch not installed"}


def render_report(cuda_info: dict, bench: dict) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, gpu, cuda, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.15", "---\n",
        "*Back to [[../1.15 - GPU Computing & CUDA Foundations|Chapter 1.15]]*\n",
        "# Chapter 1.15 — Lab Report: GPU & CUDA Validation\n",
        f"> Generated on {now}\n", "---\n",
        "## CUDA Environment\n", "| Property | Value |", "|----------|-------|",
    ]
    for k, v in cuda_info.items():
        lines.append(f"| {k} | `{v}` |")

    lines.extend(["\n## Benchmark (2048×2048 matmul)\n", "| Metric | Value |", "|--------|-------|"])
    for k, v in bench.items():
        lines.append(f"| {k} | `{v}` |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="GPU/CUDA lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    cuda_info = check_cuda()
    bench = benchmark_matmul()
    report = render_report(cuda_info, bench)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.15_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

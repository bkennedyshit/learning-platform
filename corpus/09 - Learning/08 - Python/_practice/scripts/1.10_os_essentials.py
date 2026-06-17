#!/usr/bin/env python3
"""
1.10_os_essentials.py — Hands-on lab for Chapter 1.10 (Operating Systems Essentials).

Reports system info: CPU, memory, filesystem, process limits.

Usage:
  python 1.10_os_essentials.py --out ../1.10_lab_report.md
  python 1.10_os_essentials.py --demo
"""
from __future__ import annotations

import argparse
import os
import platform
import sys
from datetime import datetime
from pathlib import Path


def get_system_info() -> dict[str, str]:
    info = {
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "cpu_count_logical": str(os.cpu_count()),
        "python_pid": str(os.getpid()),
    }
    try:
        import psutil
        mem = psutil.virtual_memory()
        info["ram_total_gb"] = f"{mem.total / (1024**3):.1f}"
        info["ram_available_gb"] = f"{mem.available / (1024**3):.1f}"
        info["cpu_freq_mhz"] = str(psutil.cpu_freq().current if psutil.cpu_freq() else "unknown")
    except ImportError:
        info["ram_total_gb"] = "(install psutil for details)"

    if hasattr(os, "getloadavg"):
        info["load_avg"] = str(os.getloadavg())

    # Filesystem info
    stat = os.statvfs(".") if hasattr(os, "statvfs") else None
    if stat:
        info["disk_free_gb"] = f"{stat.f_bavail * stat.f_frsize / (1024**3):.1f}"
    return info


def render_report(info: dict) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, os, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.10", "---\n",
        "*Back to [[../1.10 - Operating Systems Essentials|Chapter 1.10]]*\n",
        "# Chapter 1.10 — Lab Report: System Information\n",
        f"> Generated on {now}\n", "---\n",
        "## System Info\n", "| Property | Value |", "|----------|-------|",
    ]
    for k, v in info.items():
        lines.append(f"| {k} | `{v}` |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="OS essentials lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    info = get_system_info()
    report = render_report(info)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.10_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

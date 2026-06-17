#!/usr/bin/env python3
"""
1.9_docker.py — Hands-on lab for Chapter 1.9 (Docker & Containers).

Checks Docker installation, runtime, and GPU support.

Usage:
  python 1.9_docker.py --out ../1.9_lab_report.md
  python 1.9_docker.py --demo
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)


def check_docker() -> dict[str, dict]:
    checks = {}
    checks["installed"] = {"ok": shutil.which("docker") is not None, "detail": shutil.which("docker") or "not in PATH"}
    ok, out = run_cmd(["docker", "--version"])
    checks["version"] = {"ok": ok, "detail": out}
    ok, out = run_cmd(["docker", "info", "--format", "{{.ServerVersion}}"])
    checks["daemon_running"] = {"ok": ok, "detail": out if ok else "Docker daemon not running"}
    ok, out = run_cmd(["docker", "compose", "version"])
    checks["compose"] = {"ok": ok, "detail": out}
    ok, out = run_cmd(["docker", "run", "--rm", "--gpus", "all", "nvidia/cuda:12.4-base-ubuntu22.04", "nvidia-smi"])
    checks["gpu_runtime"] = {"ok": ok, "detail": "NVIDIA GPU runtime available" if ok else "No GPU runtime (expected on most dev machines)"}
    return checks


def render_report(checks: dict) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, docker, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.9", "---\n",
        "*Back to [[../1.9 - Docker & Containers|Chapter 1.9]]*\n",
        "# Chapter 1.9 — Lab Report: Docker Validation\n",
        f"> Generated on {now}\n", "---\n",
        "## Docker Checks\n", "| Check | Status | Detail |", "|-------|--------|--------|",
    ]
    for name, info in checks.items():
        status = "✅" if info["ok"] else "❌"
        lines.append(f"| {name} | {status} | {info['detail'][:80]} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Docker environment lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    checks = check_docker()
    report = render_report(checks)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.9_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

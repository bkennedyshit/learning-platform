#!/usr/bin/env python3
"""
1.8_git_vcs.py — Hands-on lab for Chapter 1.8 (Git & Version Control).

Validates Git installation, checks configuration, and reports status.

Usage:
  python 1.8_git_vcs.py --out ../1.8_lab_report.md
  python 1.8_git_vcs.py --demo
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git(args: list[str]) -> str:
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else f"ERROR: {result.stderr.strip()}"
    except FileNotFoundError:
        return "ERROR: git not found"
    except Exception as e:
        return f"ERROR: {e}"


def check_git() -> dict[str, str]:
    return {
        "version": run_git(["--version"]),
        "user.name": run_git(["config", "--global", "user.name"]),
        "user.email": run_git(["config", "--global", "user.email"]),
        "default_branch": run_git(["config", "--global", "init.defaultBranch"]),
        "editor": run_git(["config", "--global", "core.editor"]),
        "credential_helper": run_git(["config", "--global", "credential.helper"]),
    }


def render_report(info: dict) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, git, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.8", "---\n",
        "*Back to [[../1.8 - Git & Version Control|Chapter 1.8]]*\n",
        "# Chapter 1.8 — Lab Report: Git Configuration\n",
        f"> Generated on {now}\n", "---\n",
        "## Git Configuration\n", "| Setting | Value |", "|---------|-------|",
    ]
    for k, v in info.items():
        status = "⚠️ " if "ERROR" in v or not v else ""
        lines.append(f"| {k} | {status}`{v}` |")

    missing = [k for k, v in info.items() if "ERROR" in v or not v]
    lines.extend(["\n## Recommendations\n"])
    if "user.name" in missing:
        lines.append("- ⚠️ Set your name: `git config --global user.name \"Your Name\"`")
    if "user.email" in missing:
        lines.append("- ⚠️ Set your email: `git config --global user.email \"you@example.com\"`")
    if not missing:
        lines.append("- ✅ All critical settings configured.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Git configuration lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    info = check_git()
    report = render_report(info)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.8_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

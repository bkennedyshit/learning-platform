#!/usr/bin/env python3
"""
1.7_shell_cli.py — Hands-on lab script for Chapter 1.7
(Shell, Terminal & Cross-Platform CLI).

Detects platform, validates shell tools, tests subprocess execution,
and emits an Obsidian-formatted lab report.

Usage:
  python 1.7_shell_cli.py --out ../_practice/1.7_lab_report.md
  python 1.7_shell_cli.py --demo
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def detect_shell() -> dict[str, str]:
    info = {"platform": platform.system(), "shell": ""}
    if sys.platform == "win32":
        info["shell"] = os.environ.get("COMSPEC", "cmd.exe")
        ps = shutil.which("pwsh") or shutil.which("powershell")
        info["powershell"] = ps or "not found"
    else:
        info["shell"] = os.environ.get("SHELL", "/bin/sh")
    return info


def test_subprocess_basic() -> dict[str, str | bool]:
    """Test basic subprocess execution."""
    try:
        if sys.platform == "win32":
            result = subprocess.run(["cmd", "/c", "echo", "hello"], capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(["echo", "hello"], capture_output=True, text=True, timeout=5)
        return {"works": True, "output": result.stdout.strip()}
    except Exception as e:
        return {"works": False, "error": str(e)}


def test_pipe_simulation() -> dict[str, str | bool]:
    """Test piping between processes."""
    try:
        if sys.platform == "win32":
            p1 = subprocess.Popen(["cmd", "/c", "echo", "line1\nline2\nline3"], stdout=subprocess.PIPE)
        else:
            p1 = subprocess.Popen(["printf", "line1\nline2\nline3"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["python", "-c", "import sys; print(len(sys.stdin.readlines()))"],
                              stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
        output = p2.communicate(timeout=5)[0].strip()
        return {"works": True, "line_count": output}
    except Exception as e:
        return {"works": False, "error": str(e)}


def check_path_tools() -> list[dict[str, str | bool]]:
    """Check common CLI tools in PATH."""
    tools = ["git", "python", "pip", "curl", "ssh", "tar", "grep"]
    if sys.platform == "win32":
        tools.extend(["pwsh", "wsl"])
    else:
        tools.extend(["bash", "zsh", "awk", "sed"])
    return [{"name": t, "available": shutil.which(t) is not None, "path": shutil.which(t) or ""} for t in tools]


def check_env_vars() -> dict[str, str]:
    """Report key environment variables."""
    keys = ["PATH", "HOME", "USERPROFILE", "SHELL", "VIRTUAL_ENV", "PYTHONPATH", "EDITOR"]
    return {k: os.environ.get(k, "(not set)")[:100] for k in keys}


def render_report(shell: dict, sub: dict, pipe: dict, tools: list, env: dict) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, shell, cli, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.7", "---\n",
        "*Back to [[../1.7 - Shell, Terminal & Cross-Platform CLI|Chapter 1.7]]*\n",
        "# Chapter 1.7 — Lab Report: Shell & CLI Validation\n",
        f"> Generated on {now}\n", "---\n",
        "## Shell Detection\n", "| Property | Value |", "|----------|-------|",
    ]
    for k, v in shell.items():
        lines.append(f"| {k} | `{v}` |")

    lines.extend(["\n## Subprocess Tests\n",
                  f"- Basic execution: {'✅' if sub.get('works') else '❌'} — output: `{sub.get('output', sub.get('error', ''))}`",
                  f"- Pipe simulation: {'✅' if pipe.get('works') else '❌'} — lines counted: `{pipe.get('line_count', pipe.get('error', ''))}`"])

    lines.extend(["\n## PATH Tools\n", "| Tool | Available | Path |", "|------|-----------|------|"])
    for t in tools:
        lines.append(f"| {t['name']} | {'✅' if t['available'] else '❌'} | `{t['path']}` |")

    lines.extend(["\n## Environment Variables\n", "| Variable | Value |", "|----------|-------|"])
    for k, v in env.items():
        lines.append(f"| {k} | `{v}` |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Shell & CLI environment lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    shell = detect_shell()
    sub = test_subprocess_basic()
    pipe = test_pipe_simulation()
    tools = check_path_tools()
    env = check_env_vars()

    report = render_report(shell, sub, pipe, tools, env)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.7_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

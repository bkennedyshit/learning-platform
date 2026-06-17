#!/usr/bin/env python3
"""
rust_lab_runner.py — Compile & run Rust exercises, emit reports.

Creates temporary Cargo projects, compiles Rust code snippets,
captures compiler output, and generates pass/fail reports.

Usage:
  python rust_lab_runner.py --exercise ownership_basics
  python rust_lab_runner.py --file my_solution.rs --expect-compile
  python rust_lab_runner.py --file my_solution.rs --expect-fail
  python rust_lab_runner.py --dir exercises/ --report report.md

Exit code 0 if all expectations met.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class CompileResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float


@dataclass
class TestResult:
    name: str
    file: str
    expected_compile: bool
    actual_compile: bool
    passed: bool
    compiler_output: str
    runtime_output: str = ""


@dataclass
class Report:
    timestamp: str
    results: list[TestResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    def to_markdown(self) -> str:
        lines = [
            "---",
            f"date: {self.timestamp[:10]}",
            "title: \"Rust Lab Report\"",
            "tags: [rust, practice, lab-report]",
            "type: practice-report",
            "---\n",
            "# Rust Lab Report\n",
            f"**Generated:** {self.timestamp}",
            f"**Results:** {self.passed}/{self.total} passed\n",
            "| # | Exercise | Expected | Actual | Status |",
            "|---|----------|----------|--------|--------|",
        ]
        for i, r in enumerate(self.results, 1):
            exp = "compile" if r.expected_compile else "fail"
            act = "compiled" if r.actual_compile else "failed"
            status = "✅" if r.passed else "❌"
            lines.append(f"| {i} | {r.name} | {exp} | {act} | {status} |")

        lines.append("\n---\n")
        for r in self.results:
            if not r.passed:
                lines.append(f"## ❌ {r.name}\n")
                lines.append(f"**File:** `{r.file}`\n")
                lines.append("**Compiler output:**\n")
                lines.append(f"```\n{r.compiler_output[:2000]}\n```\n")

        return "\n".join(lines)


def create_cargo_project(tmp_dir: Path, code: str) -> Path:
    """Create a minimal Cargo project with the given code."""
    project_dir = tmp_dir / "rust_exercise"
    src_dir = project_dir / "src"
    src_dir.mkdir(parents=True)

    cargo_toml = (
        '[package]\nname = "exercise"\nversion = "0.1.0"\nedition = "2021"\n'
    )
    (project_dir / "Cargo.toml").write_text(cargo_toml)
    (src_dir / "main.rs").write_text(code)

    return project_dir


def compile_and_run(project_dir: Path, run: bool = False) -> CompileResult:
    """Compile (and optionally run) a Cargo project."""
    import time

    cmd = ["cargo", "build"] if not run else ["cargo", "run"]
    start = time.perf_counter()

    result = subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=60,
    )

    duration_ms = (time.perf_counter() - start) * 1000

    return CompileResult(
        success=result.returncode == 0,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.returncode,
        duration_ms=duration_ms,
    )


def check_exercise(file_path: Path, expect_compile: bool) -> TestResult:
    """Check a single Rust file against expectations."""
    code = file_path.read_text(encoding="utf-8")
    name = file_path.stem

    with tempfile.TemporaryDirectory() as tmp:
        project_dir = create_cargo_project(Path(tmp), code)
        result = compile_and_run(project_dir, run=expect_compile)

    passed = result.success == expect_compile

    return TestResult(
        name=name,
        file=str(file_path),
        expected_compile=expect_compile,
        actual_compile=result.success,
        passed=passed,
        compiler_output=result.stderr,
        runtime_output=result.stdout if result.success else "",
    )


def run_directory(dir_path: Path) -> Report:
    """Run all .rs files in a directory. Files prefixed with 'ok_' should compile,
    files prefixed with 'err_' should fail."""
    report = Report(timestamp=datetime.now().isoformat())

    for rs_file in sorted(dir_path.glob("*.rs")):
        if rs_file.name.startswith("ok_"):
            expect = True
        elif rs_file.name.startswith("err_"):
            expect = False
        else:
            expect = True  # Default: expect compilation

        result = check_exercise(rs_file, expect)
        report.results.append(result)
        status = "✅" if result.passed else "❌"
        print(f"  {status} {result.name}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Rust lab runner")
    parser.add_argument("--file", type=str, help="Single .rs file to check")
    parser.add_argument("--dir", type=str, help="Directory of .rs exercises")
    parser.add_argument("--expect-compile", action="store_true", default=True)
    parser.add_argument("--expect-fail", action="store_true")
    parser.add_argument("--report", type=str, help="Output report path (.md)")
    args = parser.parse_args()

    if args.expect_fail:
        args.expect_compile = False

    if args.file:
        result = check_exercise(Path(args.file), args.expect_compile)
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}")
        if not result.passed:
            print(f"Compiler output:\n{result.compiler_output}")
        raise SystemExit(0 if result.passed else 1)

    elif args.dir:
        print(f"Running exercises in {args.dir}...")
        report = run_directory(Path(args.dir))
        print(f"\nResults: {report.passed}/{report.total} passed")

        if args.report:
            Path(args.report).write_text(report.to_markdown(), encoding="utf-8")
            print(f"Report written to {args.report}")

        raise SystemExit(0 if report.failed == 0 else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

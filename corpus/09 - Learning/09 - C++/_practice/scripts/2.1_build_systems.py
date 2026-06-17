#!/usr/bin/env python3
"""
2.1_build_systems.py — Lab harness for Chapter 2.1 (Setup, Build Systems & Toolchain).

Generates a minimal C++ project, compiles it with CMake + Ninja, and verifies
the build pipeline works end-to-end. Reports compiler version, build time,
and binary size.

Usage:
  python 2.1_build_systems.py
  python 2.1_build_systems.py --compiler clang++ --std 23
  python 2.1_build_systems.py --out /tmp/report.md

Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def create_project(project_dir: Path, std: int) -> None:
    """Generate a minimal CMake project."""
    (project_dir / "src").mkdir()
    (project_dir / "src" / "main.cpp").write_text(f"""\
#include <iostream>
#include <array>
#include <algorithm>
#include <numeric>

int main() {{
    std::array<int, 10> data;
    std::iota(data.begin(), data.end(), 1);
    std::cout << "C++ Standard: " << __cplusplus << "\\n";
    std::cout << "Sum 1..10: "
              << std::accumulate(data.begin(), data.end(), 0) << "\\n";
    return 0;
}}
""")
    (project_dir / "CMakeLists.txt").write_text(f"""\
cmake_minimum_required(VERSION 3.20)
project(LabTest LANGUAGES CXX)
set(CMAKE_CXX_STANDARD {std})
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
add_executable(lab_test src/main.cpp)
target_compile_options(lab_test PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra>
)
""")


def run_build(project_dir: Path, compiler: str | None) -> dict:
    """Configure and build the project, return metrics."""
    build_dir = project_dir / "build"
    build_dir.mkdir()

    cmake_args = ["cmake", "-B", str(build_dir), "-S", str(project_dir)]
    if shutil.which("ninja"):
        cmake_args += ["-G", "Ninja"]
    if compiler:
        cmake_args += [f"-DCMAKE_CXX_COMPILER={compiler}"]

    t0 = time.perf_counter()
    subprocess.run(cmake_args, check=True, capture_output=True, text=True)
    subprocess.run(["cmake", "--build", str(build_dir)], check=True, capture_output=True, text=True)
    build_time = time.perf_counter() - t0

    # Find executable
    exe = None
    for candidate in [build_dir / "lab_test", build_dir / "lab_test.exe",
                      build_dir / "Debug" / "lab_test.exe"]:
        if candidate.exists():
            exe = candidate
            break

    if not exe:
        raise FileNotFoundError("Built executable not found")

    # Run it
    result = subprocess.run([str(exe)], capture_output=True, text=True, check=True)

    return {
        "build_time_s": build_time,
        "binary_size_kb": exe.stat().st_size / 1024,
        "output": result.stdout.strip(),
        "compile_commands_exists": (build_dir / "compile_commands.json").exists(),
    }


def main():
    parser = argparse.ArgumentParser(description="Ch 2.1 Build System Lab")
    parser.add_argument("--compiler", default=None, help="C++ compiler path")
    parser.add_argument("--std", type=int, default=23, choices=[17, 20, 23])
    parser.add_argument("--out", default=None, help="Output report path (.md)")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp_lab_") as tmp:
        project_dir = Path(tmp)
        create_project(project_dir, args.std)
        metrics = run_build(project_dir, args.compiler)

    report = f"""# Lab 2.1 — Build System Verification

| Metric | Value |
|--------|-------|
| C++ Standard | {args.std} |
| Build Time | {metrics['build_time_s']:.2f}s |
| Binary Size | {metrics['binary_size_kb']:.1f} KB |
| compile_commands.json | {'✅' if metrics['compile_commands_exists'] else '❌'} |

## Program Output
```
{metrics['output']}
```

## ✅ All checks passed!
"""
    print(report)
    if args.out:
        Path(args.out).write_text(report)


if __name__ == "__main__":
    main()

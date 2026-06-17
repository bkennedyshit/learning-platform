#!/usr/bin/env python3
"""
2.2_types_memory.py — Lab harness for Chapter 2.2 (Core Language: Types, Memory & Pointers).

Compiles and runs small C++ programs that demonstrate type sizes, stack vs heap
performance, and value category behavior. Emits a markdown report.

Usage:
  python 2.2_types_memory.py
  python 2.2_types_memory.py --out /tmp/report.md
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
import time
from pathlib import Path

PROGRAMS = {
    "type_sizes": """\
#include <iostream>
#include <cstdint>
#include <string>
#include <vector>
#include <optional>
int main() {
    std::cout << "sizeof(char)=" << sizeof(char) << "\\n";
    std::cout << "sizeof(int)=" << sizeof(int) << "\\n";
    std::cout << "sizeof(long)=" << sizeof(long) << "\\n";
    std::cout << "sizeof(int64_t)=" << sizeof(int64_t) << "\\n";
    std::cout << "sizeof(float)=" << sizeof(float) << "\\n";
    std::cout << "sizeof(double)=" << sizeof(double) << "\\n";
    std::cout << "sizeof(void*)=" << sizeof(void*) << "\\n";
    std::cout << "sizeof(std::string)=" << sizeof(std::string) << "\\n";
    std::cout << "sizeof(std::vector<int>)=" << sizeof(std::vector<int>) << "\\n";
    std::cout << "sizeof(std::optional<int>)=" << sizeof(std::optional<int>) << "\\n";
    return 0;
}
""",
    "stack_vs_heap": """\
#include <iostream>
#include <chrono>
#include <vector>
struct Data { float values[10]; };
int main() {
    constexpr int N = 1000000;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        Data d{}; d.values[0] = static_cast<float>(i);
        (void)d;
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        auto* d = new Data{}; d->values[0] = static_cast<float>(i);
        delete d;
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    auto stack_us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
    auto heap_us = std::chrono::duration_cast<std::chrono::microseconds>(t2-t1).count();
    std::cout << "stack_us=" << stack_us << "\\n";
    std::cout << "heap_us=" << heap_us << "\\n";
    std::cout << "ratio=" << (heap_us > 0 ? static_cast<double>(heap_us)/stack_us : 0) << "\\n";
    return 0;
}
""",
}


def compile_and_run(name: str, source: str, tmp_dir: Path) -> str:
    src_file = tmp_dir / f"{name}.cpp"
    exe_file = tmp_dir / f"{name}"
    src_file.write_text(source)

    compile_cmd = ["g++", "-std=c++20", "-O2", "-o", str(exe_file), str(src_file)]
    # Try clang++ if g++ not available
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        compile_cmd[0] = "clang++"
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)

    result = subprocess.run([str(exe_file)], capture_output=True, text=True, check=True)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description="Ch 2.2 Types & Memory Lab")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    results = {}
    with tempfile.TemporaryDirectory(prefix="cpp22_") as tmp:
        tmp_path = Path(tmp)
        for name, source in PROGRAMS.items():
            try:
                results[name] = compile_and_run(name, source, tmp_path)
            except Exception as e:
                results[name] = f"ERROR: {e}"

    report = "# Lab 2.2 — Types, Memory & Pointers\n\n"
    for name, output in results.items():
        report += f"## {name}\n```\n{output}```\n\n"

    report += "## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)


if __name__ == "__main__":
    main()

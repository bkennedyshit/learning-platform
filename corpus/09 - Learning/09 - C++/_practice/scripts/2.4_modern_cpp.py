#!/usr/bin/env python3
"""
2.4_modern_cpp.py — Lab harness for Chapter 2.4 (Smart Pointers, Move Semantics, Lambdas).

Compiles C++ programs demonstrating move vs copy performance, lambda captures,
and smart pointer behavior.

Usage:
  python 2.4_modern_cpp.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <memory>
#include <vector>
#include <chrono>
#include <string>
#include <functional>
#include <algorithm>

int main() {
    // Move vs Copy benchmark
    constexpr int N = 100000;
    std::vector<std::string> strings;
    strings.reserve(N);
    for (int i = 0; i < N; ++i)
        strings.push_back(std::string(100, 'x'));

    // Copy
    auto t0 = std::chrono::high_resolution_clock::now();
    std::vector<std::string> copied = strings;
    auto t1 = std::chrono::high_resolution_clock::now();

    // Move
    auto t2 = std::chrono::high_resolution_clock::now();
    std::vector<std::string> moved = std::move(strings);
    auto t3 = std::chrono::high_resolution_clock::now();

    auto copy_us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
    auto move_us = std::chrono::duration_cast<std::chrono::microseconds>(t3-t2).count();

    std::cout << "copy_us=" << copy_us << "\\n";
    std::cout << "move_us=" << move_us << "\\n";
    std::cout << "speedup=" << (move_us > 0 ? copy_us/move_us : 9999) << "x\\n";
    std::cout << "moved_from_size=" << strings.size() << "\\n";

    // Smart pointer demo
    auto up = std::make_unique<int>(42);
    std::cout << "unique_ptr=" << *up << "\\n";
    auto sp = std::make_shared<int>(99);
    auto sp2 = sp;
    std::cout << "shared_refcount=" << sp.use_count() << "\\n";

    // Lambda with capture
    int multiplier = 3;
    auto scale = [multiplier](int x) { return x * multiplier; };
    std::cout << "lambda_result=" << scale(7) << "\\n";

    // Lambda with STL algorithm
    std::vector<int> nums = {5, 2, 8, 1, 9, 3};
    std::sort(nums.begin(), nums.end(), [](int a, int b) { return a > b; });
    std::cout << "sorted_desc_first=" << nums[0] << "\\n";

    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp24_") as tmp:
        src = Path(tmp) / "main.cpp"
        exe = Path(tmp) / "main"
        src.write_text(SOURCE)
        try:
            subprocess.run(["g++", "-std=c++20", "-O2", "-o", str(exe), str(src)],
                          check=True, capture_output=True, text=True)
        except FileNotFoundError:
            subprocess.run(["clang++", "-std=c++20", "-O2", "-o", str(exe), str(src)],
                          check=True, capture_output=True, text=True)
        output = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout

    report = f"# Lab 2.4 — Modern C++\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

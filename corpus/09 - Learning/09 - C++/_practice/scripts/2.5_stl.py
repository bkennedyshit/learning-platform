#!/usr/bin/env python3
"""
2.5_stl.py — Lab harness for Chapter 2.5 (STL: Containers, Algorithms, Ranges).

Compiles C++ programs benchmarking container operations and demonstrating
algorithm usage.

Usage:
  python 2.5_stl.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <vector>
#include <array>
#include <unordered_map>
#include <set>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <random>

int main() {
    std::mt19937 rng(42);
    constexpr int N = 1000000;

    // Vector vs list-like access pattern
    std::vector<int> vec(N);
    std::iota(vec.begin(), vec.end(), 0);
    std::shuffle(vec.begin(), vec.end(), rng);

    // Sort benchmark
    auto t0 = std::chrono::high_resolution_clock::now();
    std::sort(vec.begin(), vec.end());
    auto t1 = std::chrono::high_resolution_clock::now();
    auto sort_us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
    std::cout << "sort_1M_us=" << sort_us << "\\n";

    // Binary search
    auto t2 = std::chrono::high_resolution_clock::now();
    bool found = std::binary_search(vec.begin(), vec.end(), N/2);
    auto t3 = std::chrono::high_resolution_clock::now();
    std::cout << "binary_search_found=" << found << "\\n";

    // Accumulate
    long long sum = std::accumulate(vec.begin(), vec.end(), 0LL);
    std::cout << "sum=" << sum << "\\n";

    // unordered_map insert benchmark
    std::unordered_map<int, int> map;
    map.reserve(N);
    auto t4 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) map[i] = i * 2;
    auto t5 = std::chrono::high_resolution_clock::now();
    auto map_insert_us = std::chrono::duration_cast<std::chrono::microseconds>(t5-t4).count();
    std::cout << "map_insert_1M_us=" << map_insert_us << "\\n";
    std::cout << "map_size=" << map.size() << "\\n";

    // Partition
    std::vector<int> data = {1,2,3,4,5,6,7,8,9,10};
    auto pivot = std::partition(data.begin(), data.end(), [](int x){ return x%2==0; });
    std::cout << "even_count=" << std::distance(data.begin(), pivot) << "\\n";

    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp25_") as tmp:
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

    report = f"# Lab 2.5 — STL\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

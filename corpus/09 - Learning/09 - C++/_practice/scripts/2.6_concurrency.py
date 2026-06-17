#!/usr/bin/env python3
"""
2.6_concurrency.py — Lab harness for Chapter 2.6 (Concurrency).

Compiles C++ programs demonstrating thread creation, atomic operations,
and data race detection.

Usage:
  python 2.6_concurrency.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <thread>
#include <atomic>
#include <vector>
#include <chrono>
#include <mutex>
#include <numeric>

int main() {
    std::cout << "hw_threads=" << std::thread::hardware_concurrency() << "\\n";

    // Atomic counter (correct)
    std::atomic<int> atomic_counter{0};
    constexpr int N = 1000000;
    {
        std::vector<std::thread> threads;
        for (int t = 0; t < 4; ++t) {
            threads.emplace_back([&]{ for(int i=0;i<N;++i) atomic_counter.fetch_add(1); });
        }
        for (auto& t : threads) t.join();
    }
    std::cout << "atomic_result=" << atomic_counter.load() << "\\n";
    std::cout << "atomic_correct=" << (atomic_counter == 4*N) << "\\n";

    // Mutex-protected counter
    int mutex_counter = 0;
    std::mutex mtx;
    {
        std::vector<std::thread> threads;
        auto t0 = std::chrono::high_resolution_clock::now();
        for (int t = 0; t < 4; ++t) {
            threads.emplace_back([&]{
                for(int i=0;i<N;++i) {
                    std::lock_guard<std::mutex> lock(mtx);
                    ++mutex_counter;
                }
            });
        }
        for (auto& t : threads) t.join();
        auto t1 = std::chrono::high_resolution_clock::now();
        auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
        std::cout << "mutex_result=" << mutex_counter << "\\n";
        std::cout << "mutex_us=" << us << "\\n";
    }

    // Parallel sum
    std::vector<int> data(N);
    std::iota(data.begin(), data.end(), 1);
    std::atomic<long long> par_sum{0};
    {
        auto t0 = std::chrono::high_resolution_clock::now();
        int chunk = N / 4;
        std::vector<std::thread> threads;
        for (int t = 0; t < 4; ++t) {
            int start = t * chunk;
            int end = (t == 3) ? N : (t+1) * chunk;
            threads.emplace_back([&, start, end]{
                long long local = 0;
                for (int i = start; i < end; ++i) local += data[i];
                par_sum.fetch_add(local);
            });
        }
        for (auto& t : threads) t.join();
        auto t1 = std::chrono::high_resolution_clock::now();
        auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
        std::cout << "parallel_sum=" << par_sum.load() << "\\n";
        std::cout << "parallel_us=" << us << "\\n";
    }

    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp26_") as tmp:
        src = Path(tmp) / "main.cpp"
        exe = Path(tmp) / "main"
        src.write_text(SOURCE)
        try:
            subprocess.run(["g++", "-std=c++20", "-O2", "-pthread", "-o", str(exe), str(src)],
                          check=True, capture_output=True, text=True)
        except FileNotFoundError:
            subprocess.run(["clang++", "-std=c++20", "-O2", "-pthread", "-o", str(exe), str(src)],
                          check=True, capture_output=True, text=True)
        output = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout

    report = f"# Lab 2.6 — Concurrency\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

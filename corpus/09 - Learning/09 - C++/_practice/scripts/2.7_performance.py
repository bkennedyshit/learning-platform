#!/usr/bin/env python3
"""
2.7_performance.py — Lab harness for Chapter 2.7 (Performance, SIMD, Cache).

Compiles C++ programs comparing AoS vs SoA layout performance and
demonstrating cache effects.

Usage:
  python 2.7_performance.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <numeric>

// AoS layout
struct ParticleAoS {
    float x, y, z;
    float vx, vy, vz;
    float r, g, b, a;  // cold data
    float lifetime;
    int flags;
};

// SoA layout
struct ParticlesSoA {
    std::vector<float> x, y, z, vx, vy, vz;
    void resize(size_t n) { x.resize(n); y.resize(n); z.resize(n);
                            vx.resize(n); vy.resize(n); vz.resize(n); }
};

int main() {
    constexpr int N = 1000000;
    constexpr float dt = 0.016f;

    // AoS benchmark
    std::vector<ParticleAoS> aos(N);
    for (int i = 0; i < N; ++i) {
        aos[i] = {float(i), float(i), 0, 1, 0.5f, 0, 0,0,0,0, 1, 0};
    }
    auto t0 = std::chrono::high_resolution_clock::now();
    for (auto& p : aos) { p.x += p.vx*dt; p.y += p.vy*dt; p.z += p.vz*dt; }
    auto t1 = std::chrono::high_resolution_clock::now();
    auto aos_us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();

    // SoA benchmark
    ParticlesSoA soa;
    soa.resize(N);
    for (int i = 0; i < N; ++i) {
        soa.x[i]=float(i); soa.y[i]=float(i); soa.z[i]=0;
        soa.vx[i]=1; soa.vy[i]=0.5f; soa.vz[i]=0;
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        soa.x[i] += soa.vx[i]*dt;
        soa.y[i] += soa.vy[i]*dt;
        soa.z[i] += soa.vz[i]*dt;
    }
    auto t3 = std::chrono::high_resolution_clock::now();
    auto soa_us = std::chrono::duration_cast<std::chrono::microseconds>(t3-t2).count();

    std::cout << "aos_us=" << aos_us << "\\n";
    std::cout << "soa_us=" << soa_us << "\\n";
    std::cout << "speedup=" << (soa_us > 0 ? double(aos_us)/soa_us : 0) << "x\\n";
    std::cout << "sizeof_AoS=" << sizeof(ParticleAoS) << "\\n";
    std::cout << "sizeof_SoA_per_particle=" << 6*sizeof(float) << "\\n";

    // Sequential vs random access
    std::vector<float> seq_data(N);
    std::iota(seq_data.begin(), seq_data.end(), 0.0f);

    auto t4 = std::chrono::high_resolution_clock::now();
    float sum1 = 0;
    for (int i = 0; i < N; ++i) sum1 += seq_data[i];
    auto t5 = std::chrono::high_resolution_clock::now();
    auto seq_us = std::chrono::duration_cast<std::chrono::microseconds>(t5-t4).count();
    std::cout << "sequential_us=" << seq_us << "\\n";
    (void)sum1;

    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp27_") as tmp:
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

    report = f"# Lab 2.7 — Performance\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
2.3_oop_templates.py — Lab harness for Chapter 2.3 (OOP, Inheritance, Templates).

Compiles C++ programs demonstrating RAII, virtual dispatch cost, and template
instantiation. Emits a markdown report.

Usage:
  python 2.3_oop_templates.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <memory>
#include <chrono>
#include <vector>

struct Base {
    virtual ~Base() = default;
    virtual int compute(int x) const { return x; }
};
struct Derived : Base {
    int compute(int x) const override { return x * 2; }
};

template<typename T>
T square(T x) { return x * x; }

int main() {
    // RAII demo
    {
        auto ptr = std::make_unique<int>(42);
        std::cout << "unique_ptr value: " << *ptr << "\\n";
    } // automatically freed

    // Virtual dispatch cost
    constexpr int N = 10000000;
    std::vector<std::unique_ptr<Base>> objects;
    objects.reserve(N);
    for (int i = 0; i < N; ++i)
        objects.push_back(std::make_unique<Derived>());

    auto t0 = std::chrono::high_resolution_clock::now();
    long sum = 0;
    for (auto& obj : objects) sum += obj->compute(1);
    auto t1 = std::chrono::high_resolution_clock::now();
    auto virtual_us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();

    // Direct call (no virtual)
    auto t2 = std::chrono::high_resolution_clock::now();
    long sum2 = 0;
    Derived d;
    for (int i = 0; i < N; ++i) sum2 += d.compute(1);
    auto t3 = std::chrono::high_resolution_clock::now();
    auto direct_us = std::chrono::duration_cast<std::chrono::microseconds>(t3-t2).count();

    std::cout << "virtual_us=" << virtual_us << "\\n";
    std::cout << "direct_us=" << direct_us << "\\n";
    std::cout << "template_int=" << square(5) << "\\n";
    std::cout << "template_double=" << square(3.14) << "\\n";
    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp23_") as tmp:
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

    report = f"# Lab 2.3 — OOP & Templates\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

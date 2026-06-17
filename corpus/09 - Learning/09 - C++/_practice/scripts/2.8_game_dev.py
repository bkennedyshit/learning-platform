#!/usr/bin/env python3
"""
2.8_game_dev.py — Lab harness for Chapter 2.8 (Game Dev with C++).

Compiles a minimal ECS implementation and game loop, benchmarks entity
iteration performance.

Usage:
  python 2.8_game_dev.py
"""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

SOURCE = """\
#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>

// Minimal ECS: SoA-style component storage
struct World {
    std::vector<float> pos_x, pos_y;
    std::vector<float> vel_x, vel_y;
    std::vector<float> health;
    size_t count = 0;

    void spawn(float px, float py, float vx, float vy, float hp) {
        pos_x.push_back(px); pos_y.push_back(py);
        vel_x.push_back(vx); vel_y.push_back(vy);
        health.push_back(hp);
        ++count;
    }
};

void movement_system(World& w, float dt) {
    for (size_t i = 0; i < w.count; ++i) {
        w.pos_x[i] += w.vel_x[i] * dt;
        w.pos_y[i] += w.vel_y[i] * dt;
    }
}

void damage_system(World& w, float dps, float dt) {
    for (size_t i = 0; i < w.count; ++i) {
        w.health[i] -= dps * dt;
    }
}

int main() {
    constexpr int NUM_ENTITIES = 100000;
    constexpr float DT = 1.0f / 60.0f;
    constexpr int FRAMES = 600;  // 10 seconds at 60fps

    World world;
    for (int i = 0; i < NUM_ENTITIES; ++i) {
        float angle = float(i) * 0.01f;
        world.spawn(0, 0, std::cos(angle), std::sin(angle), 100.0f);
    }

    std::cout << "entities=" << world.count << "\\n";
    std::cout << "frames=" << FRAMES << "\\n";

    auto t0 = std::chrono::high_resolution_clock::now();
    for (int frame = 0; frame < FRAMES; ++frame) {
        movement_system(world, DT);
        damage_system(world, 1.0f, DT);
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    auto total_ms = std::chrono::duration_cast<std::chrono::milliseconds>(t1-t0).count();
    double ms_per_frame = double(total_ms) / FRAMES;

    std::cout << "total_ms=" << total_ms << "\\n";
    std::cout << "ms_per_frame=" << ms_per_frame << "\\n";
    std::cout << "entities_per_ms=" << int(world.count / ms_per_frame) << "\\n";

    // Verify some state
    std::cout << "final_health_0=" << world.health[0] << "\\n";
    std::cout << "final_pos_x_0=" << world.pos_x[0] << "\\n";

    if (ms_per_frame < 16.67) {
        std::cout << "status=PASS (under 16.67ms budget)\\n";
    } else {
        std::cout << "status=OVER_BUDGET\\n";
    }

    return 0;
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="cpp28_") as tmp:
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

    report = f"# Lab 2.8 — Game Dev ECS\n\n```\n{output}```\n\n## ✅ Lab complete!\n"
    print(report)
    if args.out:
        Path(args.out).write_text(report)

if __name__ == "__main__":
    main()

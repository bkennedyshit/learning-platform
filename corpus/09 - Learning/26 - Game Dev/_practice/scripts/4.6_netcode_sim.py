#!/usr/bin/env python3
"""
4.6_netcode_sim.py — Network simulation for Chapter 4.6
(Multiplayer & Networking).

Simulates latency, packet loss, and rollback netcode to build intuition
about networking trade-offs.

Usage:
  python 4.6_netcode_sim.py
  python 4.6_netcode_sim.py --latency 100 --loss 0.05 --frames 300
"""

from __future__ import annotations
import argparse
import random
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Packet:
    frame: int
    player_id: int
    input_x: float
    input_y: float
    send_time: float
    arrive_time: float = 0.0
    lost: bool = False


@dataclass
class SimStats:
    total_frames: int = 0
    packets_sent: int = 0
    packets_lost: int = 0
    packets_late: int = 0
    rollbacks: int = 0
    max_rollback_frames: int = 0
    total_prediction_error: float = 0.0
    
    def report(self) -> str:
        loss_pct = self.packets_lost / max(self.packets_sent, 1) * 100
        late_pct = self.packets_late / max(self.packets_sent, 1) * 100
        avg_error = self.total_prediction_error / max(self.rollbacks, 1)
        return (
            f"## Simulation Results\n\n"
            f"| Metric | Value |\n|---|---|\n"
            f"| Frames simulated | {self.total_frames} |\n"
            f"| Packets sent | {self.packets_sent} |\n"
            f"| Packets lost | {self.packets_lost} ({loss_pct:.1f}%) |\n"
            f"| Packets late | {self.packets_late} ({late_pct:.1f}%) |\n"
            f"| Rollbacks triggered | {self.rollbacks} |\n"
            f"| Max rollback depth | {self.max_rollback_frames} frames |\n"
            f"| Avg prediction error | {avg_error:.2f} units |\n"
        )


def simulate_network(
    latency_ms: float,
    jitter_ms: float,
    packet_loss: float,
    num_frames: int,
    tick_rate: int = 60,
    rng: random.Random = None,
) -> SimStats:
    """Simulate a simple rollback netcode scenario."""
    if rng is None:
        rng = random.Random(42)
    
    stats = SimStats()
    dt = 1.0 / tick_rate
    frame_time_ms = 1000.0 / tick_rate
    
    # Simulate remote player inputs
    remote_inputs = []
    for f in range(num_frames):
        # Remote player moves in a circle
        import math
        angle = f * 0.05
        ix = math.cos(angle)
        iy = math.sin(angle)
        remote_inputs.append((ix, iy))
    
    # Simulate packet delivery
    received_at_frame: dict[int, int] = {}  # input_frame → received_at_local_frame
    
    for f in range(num_frames):
        stats.packets_sent += 1
        
        # Packet loss
        if rng.random() < packet_loss:
            stats.packets_lost += 1
            continue
        
        # Latency + jitter
        delay_ms = latency_ms + rng.gauss(0, jitter_ms)
        delay_ms = max(delay_ms, 1.0)  # minimum 1ms
        delay_frames = int(delay_ms / frame_time_ms)
        
        arrive_frame = f + delay_frames
        if arrive_frame < num_frames:
            received_at_frame[f] = arrive_frame
        else:
            stats.packets_late += 1
    
    # Simulate local prediction and rollback
    predicted_positions: dict[int, tuple[float, float]] = {}
    actual_positions: dict[int, tuple[float, float]] = {}
    
    pos_x, pos_y = 0.0, 0.0
    pred_x, pred_y = 0.0, 0.0
    last_known_input = (0.0, 0.0)
    speed = 5.0
    
    for f in range(num_frames):
        stats.total_frames += 1
        
        # Check if any remote inputs arrived this frame
        newly_confirmed = []
        for input_frame, arrive_frame in received_at_frame.items():
            if arrive_frame == f:
                newly_confirmed.append(input_frame)
        
        # Process confirmed inputs — check for mispredictions
        for input_frame in sorted(newly_confirmed):
            actual_input = remote_inputs[input_frame]
            
            # Was our prediction wrong?
            if actual_input != last_known_input:
                stats.rollbacks += 1
                rollback_depth = f - input_frame
                stats.max_rollback_frames = max(stats.max_rollback_frames, rollback_depth)
                
                # Calculate prediction error
                error = ((actual_input[0] - last_known_input[0])**2 +
                         (actual_input[1] - last_known_input[1])**2) ** 0.5
                stats.total_prediction_error += error * rollback_depth
            
            last_known_input = actual_input
        
        # Advance simulation with predicted input
        pred_x += last_known_input[0] * speed * dt
        pred_y += last_known_input[1] * speed * dt
        
        # Actual position (ground truth)
        actual_input = remote_inputs[f]
        pos_x += actual_input[0] * speed * dt
        pos_y += actual_input[1] * speed * dt
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Network simulation for game netcode")
    parser.add_argument("--latency", type=float, default=80, help="One-way latency in ms")
    parser.add_argument("--jitter", type=float, default=15, help="Jitter std dev in ms")
    parser.add_argument("--loss", type=float, default=0.03, help="Packet loss rate (0-1)")
    parser.add_argument("--frames", type=int, default=600, help="Frames to simulate")
    parser.add_argument("--tick-rate", type=int, default=60, help="Simulation tick rate")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    
    print(f"Simulating {args.frames} frames at {args.tick_rate} Hz")
    print(f"Latency: {args.latency}ms ± {args.jitter}ms, Loss: {args.loss*100:.1f}%")
    print()
    
    stats = simulate_network(
        latency_ms=args.latency,
        jitter_ms=args.jitter,
        packet_loss=args.loss,
        num_frames=args.frames,
        tick_rate=args.tick_rate,
        rng=rng,
    )
    
    report = stats.report()
    print(report)
    
    # Compare different network conditions
    print("\n## Comparison: Different Network Conditions\n")
    print("| Condition | Latency | Loss | Rollbacks | Max Depth |")
    print("|---|---|---|---|---|")
    
    conditions = [
        ("LAN", 5, 0.001),
        ("Good WiFi", 30, 0.02),
        ("Average Internet", 80, 0.03),
        ("Bad Connection", 150, 0.08),
        ("Intercontinental", 250, 0.05),
    ]
    
    for name, lat, loss in conditions:
        s = simulate_network(lat, lat * 0.2, loss, args.frames, args.tick_rate, random.Random(args.seed))
        print(f"| {name} | {lat}ms | {loss*100:.1f}% | {s.rollbacks} | {s.max_rollback_frames} |")
    
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"\nWrote report to {args.out}")


if __name__ == "__main__":
    main()

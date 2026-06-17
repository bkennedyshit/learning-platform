#!/usr/bin/env python3
"""
1.11_networks.py — Hands-on lab for Chapter 1.11 (Computer Networks).

Tests DNS resolution, measures latency, validates network stack.

Usage:
  python 1.11_networks.py --out ../1.11_lab_report.md
  python 1.11_networks.py --demo
"""
from __future__ import annotations

import argparse
import socket
import time
import sys
from datetime import datetime
from pathlib import Path


def test_dns(hostname: str) -> dict[str, str]:
    try:
        start = time.perf_counter()
        ip = socket.gethostbyname(hostname)
        elapsed = (time.perf_counter() - start) * 1000
        return {"hostname": hostname, "ip": ip, "latency_ms": f"{elapsed:.1f}", "ok": "True"}
    except Exception as e:
        return {"hostname": hostname, "ip": "", "latency_ms": "", "ok": f"False ({e})"}


def test_tcp_connect(host: str, port: int) -> dict[str, str]:
    try:
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=5):
            elapsed = (time.perf_counter() - start) * 1000
        return {"host": f"{host}:{port}", "latency_ms": f"{elapsed:.1f}", "ok": "True"}
    except Exception as e:
        return {"host": f"{host}:{port}", "latency_ms": "", "ok": f"False ({e})"}


def get_local_info() -> dict[str, str]:
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "unknown"
    return {"hostname": hostname, "local_ip": local_ip, "has_ipv6": str(socket.has_ipv6)}


def render_report(local: dict, dns_results: list, tcp_results: list) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "---", "tags: [python, networks, lab-report, practice]",
        "type: lab-report", f"generated: {now}", "chapter: 1.11", "---\n",
        "*Back to [[../1.11 - Computer Networks Essentials|Chapter 1.11]]*\n",
        "# Chapter 1.11 — Lab Report: Network Validation\n",
        f"> Generated on {now}\n", "---\n",
        "## Local Network Info\n", "| Property | Value |", "|----------|-------|",
    ]
    for k, v in local.items():
        lines.append(f"| {k} | `{v}` |")

    lines.extend(["\n## DNS Resolution\n", "| Hostname | IP | Latency (ms) | OK |", "|----------|-----|-------------|-----|"])
    for r in dns_results:
        lines.append(f"| {r['hostname']} | `{r['ip']}` | {r['latency_ms']} | {r['ok']} |")

    lines.extend(["\n## TCP Connectivity\n", "| Endpoint | Latency (ms) | OK |", "|----------|-------------|-----|"])
    for r in tcp_results:
        lines.append(f"| {r['host']} | {r['latency_ms']} | {r['ok']} |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Network validation lab")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    local = get_local_info()
    dns_results = [test_dns(h) for h in ["google.com", "github.com", "pypi.org", "docs.python.org"]]
    tcp_results = [test_tcp_connect(h, p) for h, p in [("google.com", 443), ("github.com", 443), ("pypi.org", 443)]]

    report = render_report(local, dns_results, tcp_results)

    if args.demo:
        print(report)
    else:
        out_path = args.out or (Path(__file__).resolve().parent.parent / "1.11_lab_report.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"✓ Report written to {out_path}")


if __name__ == "__main__":
    main()

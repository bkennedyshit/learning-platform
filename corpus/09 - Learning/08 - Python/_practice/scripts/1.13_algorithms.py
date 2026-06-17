#!/usr/bin/env python3
"""
1.13_algorithms.py — Practice problem generator for Chapter 1.13
(Algorithms & Data Structures in Python).

Generates randomized drill problems across 6 archetypes:
  1. Big-O complexity analysis
  2. Binary search variants
  3. Two-pointer / sliding window
  4. Graph traversal (BFS/DFS)
  5. Dynamic programming
  6. Hash map patterns

Usage:
  python 1.13_algorithms.py
  python 1.13_algorithms.py --count 20 --seed 42
  python 1.13_algorithms.py --count 20 --seed 42 --out /tmp/_113.md

Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Problem:
    archetype: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


def gen_complexity(rng: random.Random) -> Problem:
    snippets = [
        ("for i in range(n):\n    for j in range(n):\n        total += arr[i] * arr[j]", "O(n²)", "Two nested loops each iterating n times."),
        ("while n > 0:\n    n //= 2\n    count += 1", "O(log n)", "Halving n each iteration → log₂(n) iterations."),
        ("for i in range(n):\n    j = 1\n    while j < n:\n        j *= 2\n        ops += 1", "O(n log n)", "Outer loop O(n), inner loop O(log n) → O(n log n)."),
        ("for i in range(n):\n    for j in range(i, n):\n        if arr[i] + arr[j] == target:\n            return (i, j)", "O(n²)", "Nested loop where j starts at i → n(n-1)/2 = O(n²)."),
        ("seen = set()\nfor x in arr:\n    if target - x in seen:\n        return True\n    seen.add(x)", "O(n)", "Single pass with O(1) set lookup → O(n) total."),
        ("arr.sort()\nleft, right = 0, len(arr) - 1\nwhile left < right:\n    ...", "O(n log n)", "Sort is O(n log n), two-pointer scan is O(n). Dominant: O(n log n)."),
    ]
    code, answer, explanation = rng.choice(snippets)
    stmt = f"Determine the time complexity of the following code:\n\n```python\n{code}\n```\n\nState the Big-O and justify."
    sol = f"**Answer: {answer}**\n\n{explanation}"
    return Problem("Big-O Complexity Analysis", stmt, sol)


def gen_binary_search(rng: random.Random) -> Problem:
    n = rng.randint(8, 15)
    arr = sorted(rng.sample(range(1, 100), n))
    target = rng.choice(arr) if rng.random() > 0.3 else rng.randint(1, 100)
    found = target in arr

    stmt = (
        f"Given sorted array `{arr}` and target `{target}`, "
        "trace binary search step by step. State the index (or -1 if not found) "
        "and the number of comparisons made."
    )

    # Simulate binary search
    steps = []
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append(f"lo={lo}, hi={hi}, mid={mid}, arr[mid]={arr[mid]}")
        if arr[mid] == target:
            result = mid
            break
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    trace = "\n".join(f"  Step {i+1}: {s}" for i, s in enumerate(steps))
    sol = (
        f"**Result: index={result}** ({'found' if result >= 0 else 'not found'})\n\n"
        f"**Comparisons: {len(steps)}**\n\n"
        f"Trace:\n{trace}"
    )
    return Problem("Binary Search Trace", stmt, sol)


def gen_two_sum(rng: random.Random) -> Problem:
    n = rng.randint(5, 10)
    arr = [rng.randint(-20, 20) for _ in range(n)]
    # Ensure a valid pair exists
    i, j = rng.sample(range(n), 2)
    target = arr[i] + arr[j]

    stmt = (
        f"Given `nums = {arr}` and `target = {target}`, "
        "find two indices whose values sum to target. "
        "Implement using a hash map for O(n) time."
    )

    # Find solution
    seen = {}
    for idx, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            sol_indices = (seen[complement], idx)
            break
        seen[num] = idx
    else:
        sol_indices = (i, j)

    sol = (
        f"**Answer: indices {sol_indices}** → {arr[sol_indices[0]]} + {arr[sol_indices[1]]} = {target}\n\n"
        "```python\n"
        "def two_sum(nums, target):\n"
        "    seen = {}  # value → index\n"
        "    for i, num in enumerate(nums):\n"
        "        complement = target - num\n"
        "        if complement in seen:\n"
        "            return (seen[complement], i)\n"
        "        seen[num] = i\n"
        "```\n\n"
        "Time: O(n), Space: O(n)"
    )
    return Problem("Two Sum (Hash Map)", stmt, sol)


def gen_sliding_window(rng: random.Random) -> Problem:
    n = rng.randint(8, 12)
    arr = [rng.randint(1, 20) for _ in range(n)]
    k = rng.randint(3, min(5, n))

    # Compute max sum subarray of size k
    window_sum = sum(arr[:k])
    max_sum = window_sum
    max_start = 0
    for i in range(k, n):
        window_sum += arr[i] - arr[i - k]
        if window_sum > max_sum:
            max_sum = window_sum
            max_start = i - k + 1

    stmt = (
        f"Given `arr = {arr}` and window size `k = {k}`, "
        "find the maximum sum of any contiguous subarray of size k. "
        "Use the sliding window technique for O(n) time."
    )
    sol = (
        f"**Answer: max_sum = {max_sum}**, subarray = `{arr[max_start:max_start+k]}` starting at index {max_start}\n\n"
        "Sliding window: maintain running sum, add right element, subtract left element each step."
    )
    return Problem("Sliding Window Maximum Sum", stmt, sol)


def gen_graph_bfs(rng: random.Random) -> Problem:
    nodes = list("ABCDEFGH"[:rng.randint(5, 7)])
    edges = []
    for i in range(1, len(nodes)):
        parent = rng.choice(nodes[:i])
        edges.append((parent, nodes[i]))
    # Add a few extra edges
    for _ in range(rng.randint(1, 3)):
        a, b = rng.sample(nodes, 2)
        if (a, b) not in edges and (b, a) not in edges:
            edges.append((a, b))

    graph = {n: [] for n in nodes}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    start = nodes[0]
    # BFS
    from collections import deque
    visited = set()
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                queue.append(neighbor)

    edge_str = ", ".join(f"{a}-{b}" for a, b in edges)
    stmt = (
        f"Given an undirected graph with nodes `{nodes}` and edges `[{edge_str}]`, "
        f"perform BFS starting from node `{start}`. "
        "List the visit order (break ties alphabetically)."
    )
    sol = f"**BFS order: {order}**\n\nProcess: Use a queue. Visit each node once. Add unvisited neighbors in sorted order."
    return Problem("Graph BFS Traversal", stmt, sol)


def gen_dp_fibonacci(rng: random.Random) -> Problem:
    n = rng.randint(8, 20)
    # Compute fibonacci
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[-1] + fib[-2])

    stmt = (
        f"Compute the {n}th Fibonacci number using dynamic programming (bottom-up). "
        "Show the DP table and state the time/space complexity. "
        "Then optimize to O(1) space."
    )
    sol = (
        f"**F({n}) = {fib[n]}**\n\n"
        f"DP table (first 10): {fib[:min(11, n+1)]}\n\n"
        "Time: O(n), Space: O(n) with table, O(1) with two variables.\n\n"
        "```python\n"
        "def fib(n):\n"
        "    if n < 2: return n\n"
        "    a, b = 0, 1\n"
        "    for _ in range(2, n + 1):\n"
        "        a, b = b, a + b\n"
        "    return b\n"
        "```"
    )
    return Problem("Dynamic Programming (Fibonacci)", stmt, sol)


ARCHETYPES = [gen_complexity, gen_binary_search, gen_two_sum, gen_sliding_window, gen_graph_bfs, gen_dp_fibonacci]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [python, algorithms, data-structures, practice, \"review/python/1.13\"]\n"
        "chapter: 1.13\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../1.13 - Algorithms & Data Structures in Python|Chapter 1.13]] | "
        "Part of [[../../09 - Learning Index|Learning Index]]*\n\n"
        "# Chapter 1.13 — Practice Drills: Algorithms & Data Structures\n\n"
        "> Auto-generated by `scripts/1.13_algorithms.py`. Solve on paper first.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate algorithm practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "1.13_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)

    if args.demo:
        print(md)
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8")
        print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

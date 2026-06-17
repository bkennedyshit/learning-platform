#!/usr/bin/env python3
"""
3.2_generics_and_linq.py — Practice problem generator for Chapter 3.2
(Core Language: Types, Generics & LINQ).

Generates randomized drill problems across 6 archetypes:
  1. Value type vs reference type behavior prediction
  2. Generic constraint design (write the where clause)
  3. LINQ query translation (Python → C#)
  4. Pattern matching expression completion
  5. Nullable reference type analysis
  6. Record type design and usage

Usage:
  python 3.2_generics_and_linq.py
  python 3.2_generics_and_linq.py --count 12 --seed 42
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


# ---------------------------------------------------------------------------
# Archetype 1: Value vs Reference behavior
# ---------------------------------------------------------------------------
def gen_value_vs_ref(rng: random.Random) -> Problem:
    scenarios = [
        {
            "code": """```csharp
struct Point { public int X, Y; }
var a = new Point { X = 1, Y = 2 };
var b = a;
b.X = 99;
Console.WriteLine(a.X);
```""",
            "answer": "1",
            "explanation": "`Point` is a struct (value type). `b = a` copies the data. Modifying `b.X` does not affect `a`."
        },
        {
            "code": """```csharp
class Enemy { public int Health = 100; }
var e1 = new Enemy();
var e2 = e1;
e2.Health = 0;
Console.WriteLine(e1.Health);
```""",
            "answer": "0",
            "explanation": "`Enemy` is a class (reference type). `e2 = e1` copies the reference. Both point to the same object."
        },
        {
            "code": """```csharp
int[] arr1 = { 1, 2, 3 };
int[] arr2 = arr1;
arr2[0] = 99;
Console.WriteLine(arr1[0]);
```""",
            "answer": "99",
            "explanation": "Arrays are reference types. `arr2 = arr1` copies the reference, not the array contents."
        },
        {
            "code": """```csharp
record struct Tile(int X, int Y);
var t1 = new Tile(3, 4);
var t2 = t1;
// t2.X = 5;  // Would this compile?
Console.WriteLine(t1 == t2);
```""",
            "answer": "True (and the commented line would NOT compile if `readonly record struct`)",
            "explanation": "Record structs have value equality. If `readonly`, properties have no setter."
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"What does this code print? Explain why.\n\n{s['code']}"
    sol = f"**Output:** `{s['answer']}`\n\n{s['explanation']}"
    return Problem("Value vs Reference Types", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Generic constraints
# ---------------------------------------------------------------------------
def gen_generic_constraint(rng: random.Random) -> Problem:
    scenarios = [
        {
            "desc": "A method `T CreateDefault<T>()` that creates a new instance of T using a parameterless constructor.",
            "answer": "`where T : new()`",
            "full": "```csharp\npublic T CreateDefault<T>() where T : new() => new T();\n```"
        },
        {
            "desc": "A pool `ObjectPool<T>` where T must be a class with a parameterless constructor.",
            "answer": "`where T : class, new()`",
            "full": "```csharp\npublic class ObjectPool<T> where T : class, new() { }\n```"
        },
        {
            "desc": "A method that compares two items and returns the larger one.",
            "answer": "`where T : IComparable<T>`",
            "full": "```csharp\npublic T Max<T>(T a, T b) where T : IComparable<T>\n    => a.CompareTo(b) >= 0 ? a : b;\n```"
        },
        {
            "desc": "A component lookup `T? Get<T>()` where T must be a reference type implementing IComponent.",
            "answer": "`where T : class, IComponent`",
            "full": "```csharp\npublic T? Get<T>() where T : class, IComponent\n    => _components.TryGetValue(typeof(T), out var c) ? (T)c : null;\n```"
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"Write the generic constraint (`where` clause) for:\n\n> {s['desc']}"
    sol = f"**Constraint:** `{s['answer']}`\n\n{s['full']}"
    return Problem("Generic Constraints", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Python → LINQ translation
# ---------------------------------------------------------------------------
def gen_linq_translation(rng: random.Random) -> Problem:
    scenarios = [
        {
            "python": "`[x.name for x in items if x.price > 100]`",
            "csharp": "```csharp\nitems.Where(x => x.Price > 100).Select(x => x.Name).ToList()\n```"
        },
        {
            "python": "`sum(item.value * item.count for item in inventory)`",
            "csharp": "```csharp\ninventory.Sum(item => item.Value * item.Count)\n```"
        },
        {
            "python": "`sorted(enemies, key=lambda e: e.health)[:5]`",
            "csharp": "```csharp\nenemies.OrderBy(e => e.Health).Take(5).ToList()\n```"
        },
        {
            "python": "`{crop.name: crop for crop in crops if crop.season == 'spring'}`",
            "csharp": "```csharp\ncrops.Where(c => c.Season == Season.Spring)\n     .ToDictionary(c => c.Name)\n```"
        },
        {
            "python": "`any(tile.has_crop for tile in farm_tiles)`",
            "csharp": "```csharp\nfarmTiles.Any(tile => tile.HasCrop)\n```"
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"Translate this Python expression to C# LINQ:\n\n{s['python']}"
    sol = f"**C# LINQ:**\n\n{s['csharp']}"
    return Problem("Python → LINQ Translation", stmt, sol)


# ---------------------------------------------------------------------------
# Generator registry
# ---------------------------------------------------------------------------
GENERATORS = [
    gen_value_vs_ref,
    gen_generic_constraint,
    gen_linq_translation,
]


def generate_problem_set(count: int, seed: int | None) -> list[Problem]:
    rng = random.Random(seed)
    problems = []
    for i in range(count):
        gen = rng.choice(GENERATORS)
        problems.append(gen(rng))
    return problems


def render_markdown(problems: list[Problem], seed: int | None) -> str:
    lines = [
        "---",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        'title: "Practice — 3.2 Types, Generics & LINQ"',
        "type: practice",
        "chapter: 3.2",
        "---\n",
        "# Practice Problems — 3.2 Types, Generics & LINQ\n",
        f"Generated: {datetime.now().isoformat()} | Seed: {seed}\n",
        "---\n",
    ]
    for i, p in enumerate(problems, 1):
        lines.append(p.render(i))
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate C# 3.2 practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    problems = generate_problem_set(args.count, args.seed)
    md = render_markdown(problems, args.seed)

    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(md)


if __name__ == "__main__":
    main()

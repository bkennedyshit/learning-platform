#!/usr/bin/env python3
"""
6.2_type_system_drills.py — Practice problem generator for Chapter 6.2
(Type System: Primitives, Unions, Intersections, Generics).

Generates TypeScript type annotation challenges that the learner must solve.
Each problem presents a JavaScript snippet and asks for proper TypeScript typing.

Usage:
  python 6.2_type_system_drills.py
  python 6.2_type_system_drills.py --count 12 --seed 42
  python 6.2_type_system_drills.py --count 12 --seed 42 --out /tmp/_62.md

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


# ---------------------------------------------------------------------------
# Archetype 1: Annotate function parameters and return types
# ---------------------------------------------------------------------------
def gen_annotate_function(rng: random.Random) -> Problem:
    functions = [
        {
            "js": "function add(a, b) { return a + b; }",
            "ts": "function add(a: number, b: number): number { return a + b; }",
            "desc": "a function that adds two numbers",
        },
        {
            "js": "function greet(name) { return `Hello, ${name}!`; }",
            "ts": "function greet(name: string): string { return `Hello, ${name}!`; }",
            "desc": "a greeting function",
        },
        {
            "js": "function isEven(n) { return n % 2 === 0; }",
            "ts": "function isEven(n: number): boolean { return n % 2 === 0; }",
            "desc": "a function checking if a number is even",
        },
        {
            "js": "function repeat(str, times) { return str.repeat(times); }",
            "ts": "function repeat(str: string, times: number): string { return str.repeat(times); }",
            "desc": "a function that repeats a string",
        },
        {
            "js": "function first(arr) { return arr[0]; }",
            "ts": "function first<T>(arr: T[]): T | undefined { return arr[0]; }",
            "desc": "a generic function returning the first element",
        },
    ]
    fn = rng.choice(functions)
    stmt = (
        f"Add TypeScript type annotations to {fn['desc']}:\n\n"
        f"```js\n{fn['js']}\n```\n\n"
        "Provide the fully-typed version."
    )
    sol = f"```ts\n{fn['ts']}\n```"
    return Problem("Annotate Function", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 2: Union types
# ---------------------------------------------------------------------------
def gen_union_type(rng: random.Random) -> Problem:
    scenarios = [
        {
            "desc": "a variable that can be a string or number",
            "solution": "type StringOrNumber = string | number;",
        },
        {
            "desc": "an HTTP status code (200, 404, or 500)",
            "solution": "type HttpStatus = 200 | 404 | 500;",
        },
        {
            "desc": "a loading state ('idle' | 'loading' | 'success' | 'error')",
            "solution": 'type LoadingState = "idle" | "loading" | "success" | "error";',
        },
        {
            "desc": "a value that is either a User object or null",
            "solution": "type MaybeUser = User | null;",
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"Define a type alias for {s['desc']}."
    sol = f"```ts\n{s['solution']}\n```"
    return Problem("Union Type", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 3: Generics
# ---------------------------------------------------------------------------
def gen_generic(rng: random.Random) -> Problem:
    scenarios = [
        {
            "desc": "a generic `identity` function that returns its argument unchanged",
            "solution": "function identity<T>(value: T): T { return value; }",
        },
        {
            "desc": "a generic `Pair<A, B>` type representing a tuple of two different types",
            "solution": "type Pair<A, B> = [A, B];",
        },
        {
            "desc": "a generic `last` function that returns the last element of an array",
            "solution": "function last<T>(arr: T[]): T | undefined { return arr[arr.length - 1]; }",
        },
        {
            "desc": "a generic `Result<T, E>` type (discriminated union with ok/err)",
            "solution": 'type Result<T, E = Error> =\n  | { ok: true; value: T }\n  | { ok: false; error: E };',
        },
    ]
    s = rng.choice(scenarios)
    stmt = f"Write {s['desc']}."
    sol = f"```ts\n{s['solution']}\n```"
    return Problem("Generics", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 4: Type narrowing
# ---------------------------------------------------------------------------
def gen_narrowing(rng: random.Random) -> Problem:
    scenarios = [
        {
            "desc": "Write a function `stringify(value: unknown): string` that handles string, number, boolean, null, undefined, and objects.",
            "solution": (
                "function stringify(value: unknown): string {\n"
                '  if (typeof value === "string") return value;\n'
                '  if (typeof value === "number") return value.toString();\n'
                '  if (typeof value === "boolean") return value ? "true" : "false";\n'
                '  if (value === null) return "null";\n'
                '  if (value === undefined) return "undefined";\n'
                "  return JSON.stringify(value);\n"
                "}"
            ),
        },
        {
            "desc": "Write a type guard `isString(value: unknown): value is string`.",
            "solution": (
                "function isString(value: unknown): value is string {\n"
                '  return typeof value === "string";\n'
                "}"
            ),
        },
    ]
    s = rng.choice(scenarios)
    stmt = s["desc"]
    sol = f"```ts\n{s['solution']}\n```"
    return Problem("Type Narrowing", stmt, sol)


# ---------------------------------------------------------------------------
# Archetype 5: Utility types
# ---------------------------------------------------------------------------
def gen_utility_type(rng: random.Random) -> Problem:
    scenarios = [
        {
            "desc": "Given `interface User { id: string; name: string; email: string; age: number }`, create a type for updating a user where all fields are optional except `id`.",
            "solution": 'type UpdateUser = Pick<User, "id"> & Partial<Omit<User, "id">>;',
        },
        {
            "desc": "Create a `ReadonlyUser` type where all properties of User are readonly.",
            "solution": "type ReadonlyUser = Readonly<User>;",
        },
        {
            "desc": "Create a type `UserMap` that maps string keys to User values.",
            "solution": "type UserMap = Record<string, User>;",
        },
        {
            "desc": "Extract only the string-valued keys from User into a new type.",
            "solution": 'type StringFields = Pick<User, "id" | "name" | "email">;',
        },
    ]
    s = rng.choice(scenarios)
    stmt = s["desc"]
    sol = f"```ts\n{s['solution']}\n```"
    return Problem("Utility Types", stmt, sol)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
GENERATORS = [
    gen_annotate_function,
    gen_union_type,
    gen_generic,
    gen_narrowing,
    gen_utility_type,
]


def main() -> None:
    parser = argparse.ArgumentParser(description="TypeScript type system drill generator")
    parser.add_argument("--count", type=int, default=10, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problems: list[Problem] = []

    for _ in range(args.count):
        gen = rng.choice(GENERATORS)
        problems.append(gen(rng))

    # Render
    header = (
        "---\n"
        f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        "title: \"TypeScript Type System — Practice Problems\"\n"
        "type: practice\n"
        "chapter: 6.2\n"
        "---\n\n"
        "# TypeScript Type System — Practice Problems\n\n"
        f"Generated: {datetime.now().isoformat()}\n\n---\n\n"
    )

    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"✅ Wrote {args.count} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

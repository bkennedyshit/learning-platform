#!/usr/bin/env python3
"""
6.3_advanced_types_drills.py — Practice problem generator for Chapter 6.3
(Advanced Types: Conditional, Mapped, Template Literal Types).

Generates type-level programming challenges. Each problem asks the learner
to implement a utility type from scratch.

Usage:
  python 6.3_advanced_types_drills.py
  python 6.3_advanced_types_drills.py --count 10 --seed 42
  python 6.3_advanced_types_drills.py --out /tmp/_63.md

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
    difficulty: str
    statement_md: str
    solution_md: str

    def render(self, idx: int) -> str:
        return (
            f"### Problem {idx} — {self.archetype} [{self.difficulty}]\n\n"
            f"{self.statement_md}\n\n"
            "<details>\n\n"
            "<summary>Show solution</summary>\n\n"
            f"{self.solution_md}\n\n"
            "</details>\n"
        )


# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------
PROBLEMS = [
    Problem(
        "Conditional Type",
        "Easy",
        "Implement `IsString<T>` that returns `true` if T is a string, `false` otherwise.\n\n"
        "```ts\ntype IsString<T> = /* your code */;\n\n"
        "type A = IsString<'hello'>; // true\ntype B = IsString<42>; // false\n```",
        "```ts\ntype IsString<T> = T extends string ? true : false;\n```",
    ),
    Problem(
        "Conditional + infer",
        "Medium",
        "Implement `ReturnType<T>` that extracts the return type of a function type.\n\n"
        "```ts\ntype MyReturnType<T> = /* your code */;\n\n"
        "type A = MyReturnType<() => string>; // string\n"
        "type B = MyReturnType<(x: number) => boolean>; // boolean\n```",
        "```ts\ntype MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;\n```",
    ),
    Problem(
        "Mapped Type",
        "Easy",
        "Implement `MyReadonly<T>` that makes all properties of T readonly.\n\n"
        "```ts\ntype MyReadonly<T> = /* your code */;\n```",
        "```ts\ntype MyReadonly<T> = { readonly [K in keyof T]: T[K] };\n```",
    ),
    Problem(
        "Mapped Type + Filter",
        "Medium",
        "Implement `PickByType<T, V>` that picks only properties whose value extends V.\n\n"
        "```ts\ntype PickByType<T, V> = /* your code */;\n\n"
        "type A = PickByType<{ a: string; b: number; c: string }, string>;\n"
        "// { a: string; c: string }\n```",
        "```ts\ntype PickByType<T, V> = {\n  [K in keyof T as T[K] extends V ? K : never]: T[K];\n};\n```",
    ),
    Problem(
        "Template Literal",
        "Medium",
        "Implement `EventName<T>` that creates event handler names from a union of strings.\n\n"
        "```ts\ntype EventName<T extends string> = /* your code */;\n\n"
        "type A = EventName<'click' | 'focus'>;\n"
        "// 'onClick' | 'onFocus'\n```",
        "```ts\ntype EventName<T extends string> = `on${Capitalize<T>}`;\n```",
    ),
    Problem(
        "Recursive Type",
        "Hard",
        "Implement `DeepPartial<T>` that makes all nested properties optional.\n\n"
        "```ts\ntype DeepPartial<T> = /* your code */;\n```",
        "```ts\ntype DeepPartial<T> = T extends object\n  ? { [K in keyof T]?: DeepPartial<T[K]> }\n  : T;\n```",
    ),
    Problem(
        "Tuple Manipulation",
        "Hard",
        "Implement `Last<T>` that extracts the last element of a tuple.\n\n"
        "```ts\ntype Last<T extends any[]> = /* your code */;\n\n"
        "type A = Last<[1, 2, 3]>; // 3\ntype B = Last<['a', 'b']>; // 'b'\n```",
        "```ts\ntype Last<T extends any[]> = T extends [...infer _, infer L] ? L : never;\n```",
    ),
    Problem(
        "Distributive Conditional",
        "Hard",
        "Implement `NonNullable<T>` that removes null and undefined from a union.\n\n"
        "```ts\ntype MyNonNullable<T> = /* your code */;\n\n"
        "type A = MyNonNullable<string | null | undefined>; // string\n```",
        "```ts\ntype MyNonNullable<T> = T extends null | undefined ? never : T;\n```",
    ),
    Problem(
        "Key Remapping",
        "Medium",
        "Implement `Getters<T>` that creates getter method types for each property.\n\n"
        "```ts\ntype Getters<T> = /* your code */;\n\n"
        "type A = Getters<{ name: string; age: number }>;\n"
        "// { getName: () => string; getAge: () => number }\n```",
        "```ts\ntype Getters<T> = {\n  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];\n};\n```",
    ),
    Problem(
        "Branded Type",
        "Medium",
        "Create branded types `USD` and `EUR` that prevent mixing currency amounts.\n\n"
        "```ts\n// Define USD and EUR types and constructor functions\n```",
        "```ts\ntype Brand<T, B extends string> = T & { readonly __brand: B };\n\n"
        "type USD = Brand<number, 'USD'>;\ntype EUR = Brand<number, 'EUR'>;\n\n"
        "function usd(amount: number): USD { return amount as USD; }\n"
        "function eur(amount: number): EUR { return amount as EUR; }\n```",
    ),
    Problem(
        "String Parsing",
        "Hard",
        "Implement `Split<S, D>` that splits a string type by delimiter.\n\n"
        "```ts\ntype Split<S extends string, D extends string> = /* your code */;\n\n"
        "type A = Split<'a.b.c', '.'>; // ['a', 'b', 'c']\n```",
        "```ts\ntype Split<S extends string, D extends string> =\n"
        "  S extends `${infer Head}${D}${infer Tail}`\n"
        "    ? [Head, ...Split<Tail, D>]\n"
        "    : [S];\n```",
    ),
    Problem(
        "Flatten",
        "Medium",
        "Implement `Flatten<T>` that flattens a nested array type by one level.\n\n"
        "```ts\ntype Flatten<T> = /* your code */;\n\n"
        "type A = Flatten<[1, [2, 3], [4]]>; // [1, 2, 3, 4]\n```",
        "```ts\ntype Flatten<T extends any[]> = T extends [infer Head, ...infer Tail]\n"
        "  ? Head extends any[]\n"
        "    ? [...Head, ...Flatten<Tail>]\n"
        "    : [Head, ...Flatten<Tail>]\n"
        "  : [];\n```",
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced types drill generator")
    parser.add_argument("--count", type=int, default=8, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    selected = rng.sample(PROBLEMS, min(args.count, len(PROBLEMS)))

    header = (
        "---\n"
        f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        "title: \"Advanced Types — Practice Problems\"\n"
        "type: practice\n"
        "chapter: 6.3\n"
        "---\n\n"
        "# Advanced Types — Practice Problems\n\n"
        f"Generated: {datetime.now().isoformat()}\n\n---\n\n"
    )

    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(selected))
    output = header + body

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"✅ Wrote {len(selected)} problems to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()

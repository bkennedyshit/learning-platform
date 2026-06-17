#!/usr/bin/env python3
"""
14.2_ownership_drills.py — Ownership & Borrow Checker drill generator.

Generates randomized Rust code snippets that either compile or don't,
testing understanding of ownership, borrowing, and lifetimes.

Archetypes:
  1. Move semantics (use after move)
  2. Borrowing rules (&T vs &mut T conflicts)
  3. Lifetime validity (dangling references)
  4. Closure captures (move vs borrow)
  5. Partial moves in structs
  6. Iterator ownership (iter vs into_iter)
  7. Function parameter ownership
  8. Return value lifetimes

Usage:
  python 14.2_ownership_drills.py
  python 14.2_ownership_drills.py --count 20 --seed 42
  python 14.2_ownership_drills.py --count 10 --out /tmp/drills.md
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
    code: str
    compiles: bool
    explanation: str

    def render(self, idx: int) -> str:
        verdict = "✅ COMPILES" if self.compiles else "❌ DOES NOT COMPILE"
        return (
            f"### Problem {idx} — {self.archetype}\n\n"
            f"Does this code compile? If not, explain why and fix it.\n\n"
            f"```rust\n{self.code}\n```\n\n"
            "<details>\n\n"
            "<summary>Show answer</summary>\n\n"
            f"**{verdict}**\n\n"
            f"{self.explanation}\n\n"
            "</details>\n"
        )


def gen_move_after_use(rng: random.Random) -> Problem:
    types = ["String", "Vec<i32>", "HashMap<String, i32>"]
    t = rng.choice(types)
    var = rng.choice(["data", "items", "values"])
    compiles = rng.choice([True, False])

    if not compiles:
        code = (
            f"fn main() {{\n"
            f"    let {var} = {t}::new();\n"
            f"    let other = {var};\n"
            f"    println!(\"{{:?}}\", {var});\n"
            f"}}"
        )
        explanation = (
            f"`{var}` was moved to `other` on line 3. After a move, the original "
            f"binding is invalid. Fix: use `{var}.clone()` or reference `&{var}`."
        )
    else:
        code = (
            f"fn main() {{\n"
            f"    let {var} = {t}::new();\n"
            f"    let other = {var}.clone();\n"
            f"    println!(\"{{:?}}\", {var});\n"
            f"    println!(\"{{:?}}\", other);\n"
            f"}}"
        )
        explanation = (
            f"`.clone()` creates an independent copy. Both `{var}` and `other` are valid."
        )

    return Problem("Move Semantics", code, compiles, explanation)


def gen_borrow_conflict(rng: random.Random) -> Problem:
    compiles = rng.choice([True, False])

    if not compiles:
        code = (
            "fn main() {\n"
            "    let mut s = String::from(\"hello\");\n"
            "    let r1 = &s;\n"
            "    let r2 = &mut s;\n"
            "    println!(\"{r1} {r2}\");\n"
            "}"
        )
        explanation = (
            "Cannot have an immutable reference (`r1`) and a mutable reference (`r2`) "
            "active at the same time. Fix: use `r1` before creating `r2`, or remove one."
        )
    else:
        code = (
            "fn main() {\n"
            "    let mut s = String::from(\"hello\");\n"
            "    let r1 = &s;\n"
            "    println!(\"{r1}\");  // r1's last use\n"
            "    let r2 = &mut s;    // OK: r1 is dead (NLL)\n"
            "    r2.push_str(\" world\");\n"
            "    println!(\"{r2}\");\n"
            "}"
        )
        explanation = (
            "Non-Lexical Lifetimes (NLL): `r1`'s lifetime ends at its last use (line 4). "
            "The mutable borrow on line 5 is valid because `r1` is no longer active."
        )

    return Problem("Borrow Conflict", code, compiles, explanation)


def gen_dangling_reference(rng: random.Random) -> Problem:
    compiles = rng.choice([True, False])

    if not compiles:
        code = (
            "fn longest(x: &str, y: &str) -> &str {\n"
            "    if x.len() > y.len() { x } else { y }\n"
            "}"
        )
        explanation = (
            "Missing lifetime annotations. The compiler can't determine which input "
            "the return value borrows from. Fix: `fn longest<'a>(x: &'a str, y: &'a str) -> &'a str`"
        )
    else:
        code = (
            "fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {\n"
            "    if x.len() > y.len() { x } else { y }\n"
            "}\n\n"
            "fn main() {\n"
            "    let s1 = String::from(\"long string\");\n"
            "    let s2 = String::from(\"xyz\");\n"
            "    let result = longest(&s1, &s2);\n"
            "    println!(\"{result}\");\n"
            "}"
        )
        explanation = (
            "Lifetime `'a` tells the compiler the return value lives as long as the "
            "shorter of the two inputs. Both `s1` and `s2` are alive when `result` is used."
        )

    return Problem("Lifetime Annotation", code, compiles, explanation)


def gen_closure_capture(rng: random.Random) -> Problem:
    compiles = rng.choice([True, False])

    if not compiles:
        code = (
            "use std::thread;\n\n"
            "fn main() {\n"
            "    let data = vec![1, 2, 3];\n"
            "    thread::spawn(|| {\n"
            "        println!(\"{:?}\", data);\n"
            "    });\n"
            "}"
        )
        explanation = (
            "The closure borrows `data`, but the thread might outlive `main`. "
            "Fix: use `move` to transfer ownership: `thread::spawn(move || { ... })`"
        )
    else:
        code = (
            "use std::thread;\n\n"
            "fn main() {\n"
            "    let data = vec![1, 2, 3];\n"
            "    let handle = thread::spawn(move || {\n"
            "        println!(\"{:?}\", data);\n"
            "    });\n"
            "    handle.join().unwrap();\n"
            "}"
        )
        explanation = (
            "`move` transfers ownership of `data` into the closure. The thread "
            "owns the data and can safely use it regardless of the parent's lifetime."
        )

    return Problem("Closure Capture", code, compiles, explanation)


def gen_partial_move(rng: random.Random) -> Problem:
    compiles = rng.choice([True, False])

    if not compiles:
        code = (
            "struct Pair { first: String, second: String }\n\n"
            "fn main() {\n"
            "    let p = Pair {\n"
            "        first: String::from(\"hello\"),\n"
            "        second: String::from(\"world\"),\n"
            "    };\n"
            "    let f = p.first;\n"
            "    println!(\"{:?}\", p);\n"
            "}"
        )
        explanation = (
            "Partial move: `p.first` was moved to `f`. You can still use `p.second` "
            "but not `p` as a whole. Fix: use `&p.first` or derive Clone."
        )
    else:
        code = (
            "struct Pair { first: String, second: String }\n\n"
            "fn main() {\n"
            "    let p = Pair {\n"
            "        first: String::from(\"hello\"),\n"
            "        second: String::from(\"world\"),\n"
            "    };\n"
            "    let f = &p.first;\n"
            "    println!(\"{f} {}\", p.second);\n"
            "}"
        )
        explanation = (
            "Borrowing `p.first` with `&` doesn't move it. Both `f` and `p.second` "
            "are valid references/values."
        )

    return Problem("Partial Move", code, compiles, explanation)


GENERATORS = [
    gen_move_after_use,
    gen_borrow_conflict,
    gen_dangling_reference,
    gen_closure_capture,
    gen_partial_move,
]


def generate_problem_set(count: int, seed: int | None) -> list[Problem]:
    rng = random.Random(seed)
    problems = []
    for _ in range(count):
        gen = rng.choice(GENERATORS)
        problems.append(gen(rng))
    return problems


def render_markdown(problems: list[Problem], seed: int | None) -> str:
    header = (
        "---\n"
        f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        "title: \"14.2 Practice — Ownership & Borrow Checker Drills\"\n"
        "tags: [rust, ownership, borrowing, lifetimes, practice, drill]\n"
        "type: practice\n"
        "---\n\n"
        "# 14.2 Practice — Ownership & Borrow Checker Drills\n\n"
        f"Generated: {datetime.now().isoformat()} | Seed: {seed} | Count: {len(problems)}\n\n"
        "**Instructions:** For each snippet, determine if it compiles. "
        "If not, explain the error and provide a fix.\n\n---\n\n"
    )
    body = "\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body


def main():
    parser = argparse.ArgumentParser(description="Ownership drill generator")
    parser.add_argument("--count", type=int, default=12, help="Number of problems")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**32)
    problems = generate_problem_set(args.count, seed)
    md = render_markdown(problems, seed)

    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"Written {len(problems)} problems to {args.out}")
    else:
        print(md)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.1_relational_algebra.py — Practice problem generator for Chapter 7.1
(Relational Theory & Set Logic).

Generates randomized drills:
  1. Translate relational algebra to SQL
  2. Translate SQL to relational algebra
  3. Set operations (UNION, INTERSECT, EXCEPT)
  4. NULL and three-valued logic
  5. Division (universal quantification)

Usage:
  python 7.1_relational_algebra.py
  python 7.1_relational_algebra.py --count 16 --seed 42

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
import sqlite3
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


ALGEBRA_TO_SQL = [
    (
        r"$\pi_{\text{name, salary}}(\sigma_{\text{dept\_id} = 3}(\text{employees}))$",
        "```sql\nSELECT DISTINCT name, salary\nFROM employees\nWHERE dept_id = 3;\n```",
        "Projection (π) → SELECT columns; Selection (σ) → WHERE clause."
    ),
    (
        r"$\pi_{\text{title}}(\sigma_{\text{budget} > 200000}(\text{projects}))$",
        "```sql\nSELECT DISTINCT title\nFROM projects\nWHERE budget > 200000;\n```",
        "π = column selection, σ = row filter. DISTINCT enforces set semantics."
    ),
    (
        r"$\pi_{\text{name}}(\text{employees} \bowtie_{\text{e.dept\_id} = \text{d.dept\_id}} \text{departments})$",
        "```sql\nSELECT DISTINCT e.name\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.dept_id;\n```",
        "Natural join (⋈) → INNER JOIN with ON condition."
    ),
    (
        r"$\pi_{\text{name}}(\text{employees}) - \pi_{\text{name}}(\text{managers})$",
        "```sql\nSELECT name FROM employees\nEXCEPT\nSELECT name FROM managers;\n```",
        "Set difference (−) → EXCEPT in SQL."
    ),
]

NULL_PROBLEMS = [
    (
        "What does `SELECT * FROM t WHERE x = NULL` return?",
        "**Nothing** (empty result). `x = NULL` evaluates to UNKNOWN, and WHERE only passes TRUE.\n\n"
        "**Correct:** `SELECT * FROM t WHERE x IS NULL`"
    ),
    (
        "If `closed_departments` contains a NULL `dept_id`, what does\n`SELECT * FROM employees WHERE dept_id NOT IN (SELECT dept_id FROM closed_departments)` return?",
        "**Empty result!** NOT IN with any NULL in the subquery makes the entire predicate UNKNOWN for every row.\n\n"
        "**Fix:** `WHERE dept_id NOT IN (SELECT dept_id FROM closed_departments WHERE dept_id IS NOT NULL)`\n"
        "**Or:** Use `NOT EXISTS` which handles NULLs correctly."
    ),
    (
        "Evaluate: `NULL AND TRUE`, `NULL OR TRUE`, `NULL AND FALSE`, `NOT NULL`",
        "- `NULL AND TRUE` → UNKNOWN\n- `NULL OR TRUE` → TRUE (short-circuit)\n"
        "- `NULL AND FALSE` → FALSE (short-circuit)\n- `NOT NULL` → UNKNOWN"
    ),
]


def gen_algebra_to_sql(rng: random.Random) -> Problem:
    expr, sql, explanation = rng.choice(ALGEBRA_TO_SQL)
    stmt = f"**Translate to SQL:**\n\n{expr}"
    sol = f"{sql}\n\n**Explanation:** {explanation}"
    return Problem("Algebra → SQL", stmt, sol)


def gen_null_logic(rng: random.Random) -> Problem:
    question, answer = rng.choice(NULL_PROBLEMS)
    return Problem("NULL & Three-Valued Logic", question, answer)


def gen_set_operation(rng: random.Random) -> Problem:
    op = rng.choice(["UNION", "INTERSECT", "EXCEPT"])
    if op == "UNION":
        stmt = "Write a query to get all **unique names** from both the `employees` and `contractors` tables."
        sol = "```sql\nSELECT name FROM employees\nUNION\nSELECT name FROM contractors;\n```\n\n**Note:** UNION eliminates duplicates. Use UNION ALL to keep them."
    elif op == "INTERSECT":
        stmt = "Find people who appear in **both** the `employees` and `vip_customers` tables (by name)."
        sol = "```sql\nSELECT name FROM employees\nINTERSECT\nSELECT name FROM vip_customers;\n```"
    else:
        stmt = "Find employees whose names do **not** appear in the `terminated` table."
        sol = "```sql\nSELECT name FROM employees\nEXCEPT\nSELECT name FROM terminated;\n```\n\n**Equivalent:** `SELECT name FROM employees WHERE name NOT IN (SELECT name FROM terminated WHERE name IS NOT NULL)`"
    return Problem(f"Set operation ({op})", stmt, sol)


ARCHETYPES = [gen_algebra_to_sql, gen_null_logic, gen_set_operation]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [sql, relational-algebra, set-theory, practice, \"review/sql/7.1\"]\n"
        "chapter: 7.1\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../7.1 - Relational Theory & Set Logic|Chapter 7.1]] | "
        "Part of [[../Subject_Plan|SQL Subject Plan]]*\n\n"
        "# Chapter 7.1 — Practice Drills: Relational Algebra & Set Logic\n\n"
        "> Auto-generated by `scripts/7.1_relational_algebra.py`.\n\n"
        "**House rule:** solve on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate relational algebra practice problems")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "7.1_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.5_query_plans.py — Practice problem generator for Chapter 7.5
(Indexes & Query Performance).

Generates randomized drills:
  1. Index selection (which index to create)
  2. Sargability (rewrite non-sargable predicates)
  3. Composite index column ordering
  4. EXPLAIN output interpretation
  5. Covering index design

Usage:
  python 7.5_query_plans.py
  python 7.5_query_plans.py --count 12 --seed 42

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


INDEX_SELECTION = [
    (
        "Query: `SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending' ORDER BY created_at DESC LIMIT 10`\n\nDesign the optimal index.",
        "```sql\nCREATE INDEX idx_orders_cust_status_date\n    ON orders(customer_id, status, created_at DESC);\n```\n\n"
        "**Reasoning:** Equality columns first (customer_id, status), then range/sort column (created_at DESC). "
        "The index satisfies WHERE, ORDER BY, and LIMIT without a separate sort step."
    ),
    (
        "Query: `SELECT product_id, SUM(quantity) FROM order_items WHERE order_date >= '2025-01-01' GROUP BY product_id`\n\nDesign the optimal index.",
        "```sql\nCREATE INDEX idx_items_date_product\n    ON order_items(order_date, product_id) INCLUDE (quantity);\n```\n\n"
        "**Reasoning:** order_date first (range filter), product_id for grouping. INCLUDE quantity for index-only scan."
    ),
    (
        "Query: `SELECT * FROM users WHERE email = 'alice@example.com'`\n\nThis query runs millions of times per day. Best index?",
        "```sql\nCREATE UNIQUE INDEX idx_users_email ON users(email);\n```\n\n"
        "**Reasoning:** Pure equality lookup on a unique column. B-tree is perfect. UNIQUE also enforces the constraint. "
        "Hash index would also work but B-tree is more versatile."
    ),
]

SARGABILITY = [
    (
        "`WHERE YEAR(created_at) = 2025`",
        "```sql\nWHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'\n```\n\n"
        "**Why:** Function on column prevents index use. Rewrite as range comparison on the raw column."
    ),
    (
        "`WHERE LOWER(email) = 'alice@example.com'`",
        "**Option 1:** Create an expression index:\n```sql\nCREATE INDEX idx_email_lower ON users(LOWER(email));\n```\n\n"
        "**Option 2:** Store normalized email in a separate column and index that.\n\n"
        "**Why:** LOWER() wraps the column, making a regular B-tree on `email` unusable."
    ),
    (
        "`WHERE salary + bonus > 100000`",
        "```sql\nWHERE salary > 100000 - bonus\n```\n\n"
        "**Or** create a generated column:\n```sql\nALTER TABLE employees ADD COLUMN total_comp NUMERIC GENERATED ALWAYS AS (salary + bonus) STORED;\nCREATE INDEX idx_total_comp ON employees(total_comp);\n```"
    ),
    (
        "`WHERE name LIKE '%smith%'`",
        "**Cannot use B-tree index** (leading wildcard). Options:\n"
        "1. GIN trigram index: `CREATE INDEX idx_name_trgm ON users USING gin (name gin_trgm_ops);`\n"
        "2. Full-text search: `CREATE INDEX idx_name_fts ON users USING gin (to_tsvector('english', name));`\n\n"
        "**Note:** `LIKE 'smith%'` (no leading wildcard) CAN use a B-tree index."
    ),
]

COMPOSITE_ORDER = [
    (
        "Queries on table `events`:\n- `WHERE user_id = ? AND event_type = ? ORDER BY created_at DESC`\n- `WHERE user_id = ? ORDER BY created_at DESC`\n\nDesign ONE index that serves both.",
        "```sql\nCREATE INDEX idx_events_user_type_date\n    ON events(user_id, event_type, created_at DESC);\n```\n\n"
        "**Leftmost prefix rule:** This index serves:\n"
        "- (user_id, event_type, created_at) ✓ — first query\n"
        "- (user_id) ✓ — second query (but can't use event_type for sort, needs separate sort on created_at)\n\n"
        "**Better for both:** `CREATE INDEX idx_events_user_date ON events(user_id, created_at DESC);` serves query 2 perfectly. "
        "For query 1, add a separate index or accept a filter step."
    ),
]


def gen_index_selection(rng: random.Random) -> Problem:
    q, a = rng.choice(INDEX_SELECTION)
    return Problem("Index design", q, a)


def gen_sargability(rng: random.Random) -> Problem:
    pred, fix = rng.choice(SARGABILITY)
    stmt = f"The following predicate **cannot use a B-tree index**. Rewrite it to be sargable:\n\n{pred}"
    return Problem("Sargability fix", stmt, fix)


def gen_composite(rng: random.Random) -> Problem:
    q, a = rng.choice(COMPOSITE_ORDER)
    return Problem("Composite index ordering", q, a)


def gen_explain_reading(rng: random.Random) -> Problem:
    stmt = (
        "Given this EXPLAIN output, identify the performance issue and suggest a fix:\n\n"
        "```\n"
        "Seq Scan on orders  (cost=0.00..450000 rows=50 width=120) (actual time=4500..4500 rows=48 loops=1)\n"
        "  Filter: (customer_id = 42)\n"
        "  Rows Removed by Filter: 9999952\n"
        "Planning Time: 0.1 ms\n"
        "Execution Time: 4500 ms\n"
        "```"
    )
    sol = (
        "**Problem:** Sequential scan on a 10M-row table to find 48 rows. The filter removes 99.9995% of rows.\n\n"
        "**Fix:** Create an index on the filter column:\n"
        "```sql\nCREATE INDEX idx_orders_customer ON orders(customer_id);\n```\n\n"
        "**Expected improvement:** From Seq Scan (4500ms) to Index Scan (~1ms). "
        "The index will find the 48 matching rows directly without scanning 10M rows."
    )
    return Problem("EXPLAIN interpretation", stmt, sol)


ARCHETYPES = [gen_index_selection, gen_sargability, gen_composite, gen_explain_reading]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [sql, indexes, query-plans, performance, practice, \"review/sql/7.5\"]\n"
        "chapter: 7.5\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../7.5 - Indexes & Query Performance|Chapter 7.5]] | "
        "Part of [[../Subject_Plan|SQL Subject Plan]]*\n\n"
        "# Chapter 7.5 — Practice Drills: Indexes & Query Performance\n\n"
        "> Auto-generated by `scripts/7.5_query_plans.py`.\n\n"
        "**House rule:** design the index on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate index/performance practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "7.5_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

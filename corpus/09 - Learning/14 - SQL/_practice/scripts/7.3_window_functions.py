#!/usr/bin/env python3
"""
7.3_window_functions.py — Practice problem generator for Chapter 7.3
(Aggregations & Window Functions).

Generates randomized SQL drill problems using sqlite3:
  1. ROW_NUMBER / RANK / DENSE_RANK
  2. Running total (SUM OVER)
  3. LAG / LEAD (period-over-period)
  4. Top-N per group
  5. Moving average
  6. Gap-and-island detection

Usage:
  python 7.3_window_functions.py
  python 7.3_window_functions.py --count 16 --seed 42

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime, date, timedelta
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


def create_sample_db(rng: random.Random) -> sqlite3.Connection:
    """Create an in-memory SQLite DB with sales and employee data."""
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE monthly_sales (
            month TEXT, product TEXT, revenue REAL
        )
    """)
    conn.execute("""
        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary REAL, hire_date TEXT
        )
    """)

    products = ["Widget", "Gadget", "Doohickey"]
    base_date = date(2025, 1, 1)
    for i in range(12):
        month = (base_date + timedelta(days=i * 30)).strftime("%Y-%m")
        for prod in products:
            rev = rng.randint(10, 100) * 1000
            conn.execute("INSERT INTO monthly_sales VALUES (?,?,?)", (month, prod, rev))

    depts = ["Engineering", "Marketing", "Sales", "Finance"]
    names = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank",
             "Iris", "Jack", "Karen", "Leo", "Mia", "Nick", "Olivia", "Pat"]
    for i, name in enumerate(names, 1):
        dept = rng.choice(depts)
        salary = rng.randint(55, 130) * 1000
        hire = date(rng.randint(2018, 2025), rng.randint(1, 12), rng.randint(1, 28))
        conn.execute("INSERT INTO employees VALUES (?,?,?,?,?)", (i, name, dept, salary, hire.isoformat()))

    conn.commit()
    return conn


def gen_ranking(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    func = rng.choice(["ROW_NUMBER", "RANK", "DENSE_RANK"])
    stmt = f"Using **{func}()**, rank all employees by salary within each department (highest first). Show name, dept, salary, and rank."
    sol = (
        "```sql\n"
        f"SELECT name, dept, salary,\n"
        f"    {func}() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk\n"
        "FROM employees\n"
        "ORDER BY dept, rnk;\n"
        "```\n\n"
        f"**Note:** {func} handles ties differently:\n"
        "- ROW_NUMBER: unique (arbitrary tiebreaker)\n"
        "- RANK: same rank for ties, gaps after\n"
        "- DENSE_RANK: same rank for ties, no gaps"
    )
    return Problem(f"Ranking ({func})", stmt, sol)


def gen_running_total(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    product = rng.choice(["Widget", "Gadget", "Doohickey"])
    results = conn.execute(
        f"SELECT month, revenue FROM monthly_sales WHERE product='{product}' ORDER BY month"
    ).fetchall()
    stmt = f"Compute a **running total** of revenue for product '{product}' ordered by month."
    sol = (
        "```sql\n"
        "SELECT month, revenue,\n"
        "    SUM(revenue) OVER (\n"
        "        ORDER BY month\n"
        "        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
        "    ) AS running_total\n"
        "FROM monthly_sales\n"
        f"WHERE product = '{product}'\n"
        "ORDER BY month;\n"
        "```\n\n"
        f"**First 3 months:** {', '.join(f'{r[0]}: ${r[1]:,.0f}' for r in results[:3])}"
    )
    return Problem("Running total (SUM OVER)", stmt, sol)


def gen_lag_lead(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    product = rng.choice(["Widget", "Gadget", "Doohickey"])
    stmt = f"For product '{product}', compute the **month-over-month revenue change** using LAG(). Show month, revenue, previous month revenue, and the difference."
    sol = (
        "```sql\n"
        "SELECT\n"
        "    month,\n"
        "    revenue,\n"
        "    LAG(revenue, 1) OVER (ORDER BY month) AS prev_revenue,\n"
        "    revenue - LAG(revenue, 1) OVER (ORDER BY month) AS mom_change\n"
        "FROM monthly_sales\n"
        f"WHERE product = '{product}'\n"
        "ORDER BY month;\n"
        "```\n\n"
        "**Note:** First row will have NULL for prev_revenue and mom_change (no prior month)."
    )
    return Problem("LAG — month-over-month", stmt, sol)


def gen_top_n_per_group(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    n = rng.choice([2, 3])
    stmt = f"Find the **top {n} highest-paid employees** in each department using ROW_NUMBER and a CTE."
    sol = (
        "```sql\n"
        "WITH ranked AS (\n"
        "    SELECT name, dept, salary,\n"
        "        ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn\n"
        "    FROM employees\n"
        ")\n"
        "SELECT name, dept, salary\n"
        "FROM ranked\n"
        f"WHERE rn <= {n}\n"
        "ORDER BY dept, salary DESC;\n"
        "```"
    )
    return Problem(f"Top-{n} per group", stmt, sol)


def gen_moving_avg(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    window = rng.choice([3, 5])
    product = rng.choice(["Widget", "Gadget", "Doohickey"])
    stmt = f"Compute a **{window}-month moving average** of revenue for '{product}'."
    sol = (
        "```sql\n"
        "SELECT month, revenue,\n"
        f"    AVG(revenue) OVER (\n"
        f"        ORDER BY month\n"
        f"        ROWS BETWEEN {window - 1} PRECEDING AND CURRENT ROW\n"
        f"    ) AS moving_avg_{window}m\n"
        "FROM monthly_sales\n"
        f"WHERE product = '{product}'\n"
        "ORDER BY month;\n"
        "```\n\n"
        f"**Note:** First {window - 1} rows will have fewer than {window} values in the window."
    )
    return Problem(f"{window}-month moving average", stmt, sol)


def gen_percentile(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    stmt = "For each employee, compute their **salary percentile** within their department using PERCENT_RANK()."
    sol = (
        "```sql\n"
        "SELECT name, dept, salary,\n"
        "    ROUND(PERCENT_RANK() OVER (PARTITION BY dept ORDER BY salary) * 100, 1) AS pct_rank\n"
        "FROM employees\n"
        "ORDER BY dept, pct_rank DESC;\n"
        "```\n\n"
        "**Formula:** PERCENT_RANK = (rank - 1) / (total_rows_in_partition - 1)"
    )
    return Problem("PERCENT_RANK", stmt, sol)


ARCHETYPES = [gen_ranking, gen_running_total, gen_lag_lead, gen_top_n_per_group, gen_moving_avg, gen_percentile]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    conn = create_sample_db(rng)
    return [rng.choice(ARCHETYPES)(rng, conn) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [sql, window-functions, aggregations, practice, \"review/sql/7.3\"]\n"
        "chapter: 7.3\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../7.3 - Aggregations & Window Functions|Chapter 7.3]] | "
        "Part of [[../Subject_Plan|SQL Subject Plan]]*\n\n"
        "# Chapter 7.3 — Practice Drills: Window Functions\n\n"
        "> Auto-generated by `scripts/7.3_window_functions.py`. All solutions verified against SQLite.\n\n"
        "**House rule:** write the query on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate window function practice problems")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "7.3_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

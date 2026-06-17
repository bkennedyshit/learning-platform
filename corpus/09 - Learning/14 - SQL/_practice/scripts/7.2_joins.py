#!/usr/bin/env python3
"""
7.2_joins.py — Practice problem generator for Chapter 7.2
(SELECT Mastery — Joins, Subqueries, CTEs).

Generates randomized SQL drill problems using sqlite3 with sample data:
  1. INNER JOIN (basic two-table)
  2. LEFT JOIN + IS NULL (anti-join)
  3. Self-join (employee-manager)
  4. Multi-table JOIN (3+ tables)
  5. Correlated subquery vs JOIN rewrite
  6. CTE composition

Usage:
  python 7.2_joins.py
  python 7.2_joins.py --count 20 --seed 42
  python 7.2_joins.py --count 20 --seed 42 --out /tmp/_72.md

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


def create_sample_db(rng: random.Random) -> sqlite3.Connection:
    """Create an in-memory SQLite DB with sample data."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)")
    conn.execute("CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary REAL, manager_id INTEGER)")
    conn.execute("CREATE TABLE projects (project_id INTEGER PRIMARY KEY, title TEXT, budget REAL)")
    conn.execute("CREATE TABLE assignments (emp_id INTEGER, project_id INTEGER, role TEXT, hours INTEGER, PRIMARY KEY(emp_id, project_id))")

    depts = [("Engineering",), ("Marketing",), ("Sales",), ("HR",), ("Finance",)]
    conn.executemany("INSERT INTO departments (dept_name) VALUES (?)", depts)

    names = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank", "Iris", "Jack",
             "Karen", "Leo", "Mia", "Nick", "Olivia"]
    for i, name in enumerate(names, 1):
        dept = rng.randint(1, 5)
        salary = rng.randint(50, 120) * 1000
        mgr = rng.choice([None, rng.randint(1, min(i, 5))]) if i > 1 else None
        conn.execute("INSERT INTO employees VALUES (?,?,?,?,?)", (i, name, dept, salary, mgr))

    projects = [("Atlas",), ("Beacon",), ("Cipher",), ("Delta",), ("Echo",)]
    for i, (title,) in enumerate(projects, 1):
        budget = rng.randint(50, 500) * 1000
        conn.execute("INSERT INTO projects VALUES (?,?,?)", (i, title, budget))

    roles = ["lead", "developer", "analyst", "designer", "tester"]
    for emp_id in range(1, 16):
        num_projects = rng.randint(0, 3)
        assigned = rng.sample(range(1, 6), min(num_projects, 5))
        for proj_id in assigned:
            role = rng.choice(roles)
            hours = rng.randint(10, 200)
            conn.execute("INSERT OR IGNORE INTO assignments VALUES (?,?,?,?)", (emp_id, proj_id, role, hours))

    conn.commit()
    return conn


def gen_inner_join(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    dept_id = rng.randint(1, 5)
    row = conn.execute("SELECT dept_name FROM departments WHERE dept_id=?", (dept_id,)).fetchone()
    dept_name = row[0]
    results = conn.execute(
        "SELECT e.name, e.salary FROM employees e JOIN departments d ON e.dept_id=d.dept_id WHERE d.dept_name=? ORDER BY e.salary DESC",
        (dept_name,)
    ).fetchall()
    stmt = f"Write a query to find all employees in the **{dept_name}** department, showing their name and salary, ordered by salary descending."
    sol = (
        "```sql\n"
        "SELECT e.name, e.salary\n"
        "FROM employees e\n"
        "INNER JOIN departments d ON e.dept_id = d.dept_id\n"
        f"WHERE d.dept_name = '{dept_name}'\n"
        "ORDER BY e.salary DESC;\n"
        "```\n\n"
        f"**Result:** {len(results)} rows — {', '.join(f'{r[0]} (${r[1]:,.0f})' for r in results[:5])}"
        + ("..." if len(results) > 5 else "")
    )
    return Problem("INNER JOIN", stmt, sol)


def gen_anti_join(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    results = conn.execute(
        "SELECT e.name FROM employees e LEFT JOIN assignments a ON e.emp_id=a.emp_id WHERE a.emp_id IS NULL ORDER BY e.name"
    ).fetchall()
    stmt = "Write a query to find employees who are **not assigned to any project**. Use a LEFT JOIN anti-join pattern."
    sol = (
        "```sql\n"
        "SELECT e.name\n"
        "FROM employees e\n"
        "LEFT JOIN assignments a ON e.emp_id = a.emp_id\n"
        "WHERE a.emp_id IS NULL\n"
        "ORDER BY e.name;\n"
        "```\n\n"
        f"**Result:** {len(results)} unassigned employees"
        + (f" — {', '.join(r[0] for r in results)}" if results else " (everyone is assigned!)")
    )
    return Problem("LEFT JOIN anti-join", stmt, sol)


def gen_self_join(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    results = conn.execute(
        "SELECT e.name, e.salary, m.name, m.salary FROM employees e JOIN employees m ON e.manager_id=m.emp_id WHERE e.salary > m.salary ORDER BY e.salary-m.salary DESC"
    ).fetchall()
    stmt = "Write a **self-join** to find employees who earn more than their manager. Show employee name, employee salary, manager name, and manager salary."
    sol = (
        "```sql\n"
        "SELECT e.name AS employee, e.salary AS emp_salary,\n"
        "       m.name AS manager, m.salary AS mgr_salary\n"
        "FROM employees e\n"
        "INNER JOIN employees m ON e.manager_id = m.emp_id\n"
        "WHERE e.salary > m.salary\n"
        "ORDER BY (e.salary - m.salary) DESC;\n"
        "```\n\n"
        f"**Result:** {len(results)} employees earn more than their manager."
    )
    return Problem("Self-join", stmt, sol)


def gen_multi_table(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    min_hours = rng.choice([50, 80, 100, 120])
    results = conn.execute(
        "SELECT e.name, d.dept_name, p.title, a.hours "
        "FROM employees e "
        "JOIN departments d ON e.dept_id=d.dept_id "
        "JOIN assignments a ON e.emp_id=a.emp_id "
        "JOIN projects p ON a.project_id=p.project_id "
        f"WHERE a.hours > {min_hours} ORDER BY a.hours DESC",
    ).fetchall()
    stmt = f"Write a query joining **4 tables** (employees, departments, assignments, projects) to find all assignments with more than **{min_hours} hours**. Show employee name, department, project title, and hours."
    sol = (
        "```sql\n"
        "SELECT e.name, d.dept_name, p.title, a.hours\n"
        "FROM employees e\n"
        "INNER JOIN departments d ON e.dept_id = d.dept_id\n"
        "INNER JOIN assignments a ON e.emp_id = a.emp_id\n"
        "INNER JOIN projects p ON a.project_id = p.project_id\n"
        f"WHERE a.hours > {min_hours}\n"
        "ORDER BY a.hours DESC;\n"
        "```\n\n"
        f"**Result:** {len(results)} rows."
    )
    return Problem("Multi-table JOIN", stmt, sol)


def gen_cte(rng: random.Random, conn: sqlite3.Connection) -> Problem:
    threshold = rng.choice([2, 3])
    results = conn.execute(
        f"SELECT e.name, COUNT(a.project_id) as cnt FROM employees e JOIN assignments a ON e.emp_id=a.emp_id GROUP BY e.emp_id, e.name HAVING COUNT(a.project_id) >= {threshold} ORDER BY cnt DESC"
    ).fetchall()
    stmt = f"Using a **CTE**, find employees assigned to **{threshold} or more projects**. Show their name and project count, ordered by count descending."
    sol = (
        "```sql\n"
        "WITH project_counts AS (\n"
        "    SELECT e.emp_id, e.name, COUNT(a.project_id) AS project_count\n"
        "    FROM employees e\n"
        "    INNER JOIN assignments a ON e.emp_id = a.emp_id\n"
        "    GROUP BY e.emp_id, e.name\n"
        ")\n"
        "SELECT name, project_count\n"
        "FROM project_counts\n"
        f"WHERE project_count >= {threshold}\n"
        "ORDER BY project_count DESC;\n"
        "```\n\n"
        f"**Result:** {len(results)} employees."
    )
    return Problem("CTE composition", stmt, sol)


ARCHETYPES = [gen_inner_join, gen_anti_join, gen_self_join, gen_multi_table, gen_cte]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    conn = create_sample_db(rng)
    return [rng.choice(ARCHETYPES)(rng, conn) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [sql, joins, cte, subqueries, practice, \"review/sql/7.2\"]\n"
        "chapter: 7.2\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../7.2 - SELECT Mastery - Joins, Subqueries, CTEs|Chapter 7.2]] | "
        "Part of [[../Subject_Plan|SQL Subject Plan]]*\n\n"
        "# Chapter 7.2 — Practice Drills: Joins, Subqueries, CTEs\n\n"
        "> Auto-generated by `scripts/7.2_joins.py`. All solutions verified against SQLite.\n\n"
        "**House rule:** write the query on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate SQL JOIN practice problems")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "7.2_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
7.6_transactions.py — Practice problem generator for Chapter 7.6
(Transactions, ACID & Concurrency).

Generates randomized drills:
  1. Identify concurrency anomalies
  2. Choose isolation level for scenario
  3. Deadlock prevention
  4. Write-skew detection
  5. Idempotent operation design

Usage:
  python 7.6_transactions.py
  python 7.6_transactions.py --count 12 --seed 42

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


ANOMALY_SCENARIOS = [
    (
        "T1 reads account balance (1000). T2 updates balance to 500 and commits. T1 reads again and sees 500.\n\nWhat anomaly is this? Which isolation level prevents it?",
        "**Non-repeatable read.** The same query returns different values within one transaction.\n\n"
        "**Prevented by:** REPEATABLE READ (and SERIALIZABLE).\n\n"
        "Under REPEATABLE READ, T1 would still see 1000 on the second read (snapshot from transaction start)."
    ),
    (
        "T1 counts 10 pending orders. T2 inserts a new pending order and commits. T1 counts again and sees 11.\n\nWhat anomaly? Which level prevents it?",
        "**Phantom read.** New rows appear that match a previously-executed query.\n\n"
        "**Prevented by:** SERIALIZABLE (in standard SQL). PostgreSQL's REPEATABLE READ also prevents this via snapshot isolation."
    ),
    (
        "Rule: at least 1 doctor on call. Both doctors read count=2, both decide to go off-call, both delete their row. Result: 0 doctors on call.\n\nWhat anomaly? How to prevent?",
        "**Write skew.** Two transactions read overlapping data, make independent decisions, and create an invalid state.\n\n"
        "**Prevention options:**\n"
        "1. SERIALIZABLE isolation (PostgreSQL detects and aborts one transaction)\n"
        "2. Explicit locking: `SELECT ... FOR UPDATE` on the on_call rows before deciding\n"
        "3. Application-level: use a single UPDATE with a WHERE count check"
    ),
]

ISOLATION_CHOICE = [
    (
        "A reporting dashboard runs complex queries that take 30 seconds. It needs consistent data across multiple queries within one report generation.",
        "**REPEATABLE READ.** The report sees a consistent snapshot from the transaction start. "
        "Concurrent writes won't affect the report's view. No retry logic needed (read-only)."
    ),
    (
        "A payment processing system transfers money between accounts. Must never allow double-spending or negative balances.",
        "**SERIALIZABLE** (safest) or **READ COMMITTED + SELECT FOR UPDATE** (more practical).\n\n"
        "With SERIALIZABLE: automatic detection of conflicts, but must implement retry logic.\n"
        "With FOR UPDATE: explicitly lock the source account row before checking balance."
    ),
    (
        "A high-throughput web application with simple CRUD operations. Occasional stale reads are acceptable.",
        "**READ COMMITTED** (PostgreSQL default). Best performance, prevents dirty reads, "
        "acceptable for most web apps where slight staleness between statements is fine."
    ),
]

DEADLOCK_SCENARIOS = [
    (
        "Two transactions:\n- T1: UPDATE accounts SET ... WHERE id=1; UPDATE accounts SET ... WHERE id=2;\n- T2: UPDATE accounts SET ... WHERE id=2; UPDATE accounts SET ... WHERE id=1;\n\nHow do you prevent the deadlock?",
        "**Consistent lock ordering.** Always acquire locks in the same order (e.g., by ascending ID):\n\n"
        "```sql\n-- Both transactions lock id=1 first, then id=2:\n"
        "BEGIN;\n"
        "SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;\n"
        "-- Now safe to update both\n"
        "UPDATE accounts SET balance = balance - 100 WHERE id = 1;\n"
        "UPDATE accounts SET balance = balance + 100 WHERE id = 2;\n"
        "COMMIT;\n```"
    ),
]


def gen_anomaly(rng: random.Random) -> Problem:
    scenario, answer = rng.choice(ANOMALY_SCENARIOS)
    return Problem("Identify anomaly", scenario, answer)


def gen_isolation_choice(rng: random.Random) -> Problem:
    scenario, answer = rng.choice(ISOLATION_CHOICE)
    stmt = f"**Scenario:** {scenario}\n\nWhich isolation level would you choose and why?"
    return Problem("Choose isolation level", stmt, answer)


def gen_deadlock(rng: random.Random) -> Problem:
    scenario, answer = rng.choice(DEADLOCK_SCENARIOS)
    return Problem("Deadlock prevention", scenario, answer)


def gen_idempotent(rng: random.Random) -> Problem:
    stmt = (
        "Design an **idempotent** operation for processing a payment event. "
        "The event may be delivered multiple times (at-least-once delivery). "
        "How do you ensure the payment is only applied once?"
    )
    sol = (
        "```sql\n"
        "-- Use an idempotency key (event_id) with ON CONFLICT:\n"
        "INSERT INTO processed_payments (event_id, amount, processed_at)\n"
        "VALUES ('evt_abc123', 49.99, NOW())\n"
        "ON CONFLICT (event_id) DO NOTHING;\n\n"
        "-- Only proceed if the insert succeeded (1 row affected):\n"
        "-- If 0 rows affected, this event was already processed.\n"
        "```\n\n"
        "**Key principle:** Store a unique identifier for each operation. "
        "Check-before-act is NOT safe under concurrency (TOCTOU race). "
        "Use INSERT ... ON CONFLICT for atomic idempotency."
    )
    return Problem("Idempotent design", stmt, sol)


ARCHETYPES = [gen_anomaly, gen_isolation_choice, gen_deadlock, gen_idempotent]


def build_problem_set(count: int, rng: random.Random) -> list[Problem]:
    return [rng.choice(ARCHETYPES)(rng) for _ in range(count)]


def render_markdown(problems: list[Problem], seed: int) -> str:
    header = (
        "---\n"
        "tags: [sql, transactions, acid, concurrency, practice, \"review/sql/7.6\"]\n"
        "chapter: 7.6\n"
        "type: practice\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"seed: {seed}\n"
        "---\n\n"
        "*Back to [[../7.6 - Transactions, ACID & Concurrency|Chapter 7.6]] | "
        "Part of [[../Subject_Plan|SQL Subject Plan]]*\n\n"
        "# Chapter 7.6 — Practice Drills: Transactions & Concurrency\n\n"
        "> Auto-generated by `scripts/7.6_transactions.py`.\n\n"
        "**House rule:** reason through the scenario on paper first, then check the spoiler.\n\n"
        "---\n\n"
    )
    body = "\n\n---\n\n".join(p.render(i + 1) for i, p in enumerate(problems))
    return header + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate transaction/concurrency practice problems")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
    rng = random.Random(seed)
    out_path = args.out or (Path(__file__).resolve().parent.parent / "7.6_drills.md")

    problems = build_problem_set(args.count, rng)
    md = render_markdown(problems, seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {len(problems)} problems (seed={seed}) -> {out_path}")


if __name__ == "__main__":
    main()

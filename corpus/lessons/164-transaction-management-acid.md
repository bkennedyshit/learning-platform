---
title: "16.4 — Transaction Management & ACID"
subject: "Databases & Storage Engines"
catalog: advanced
audience_tier: higher-education
chapter: "16.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 16.4 — Transaction Management & ACID

> *"A transaction is a unit of work that appears to execute atomically, consistently, in isolation, and durably. ACID doesn't mean what you think it means — especially Consistency and Isolation."*

> *"The I in ACID is the most subtle. You can't understand isolation without knowing what anomaly you're trying to prevent."*

Transactions are the mechanism databases use to group operations into a single unit that either all succeeds or all fails, without interfering with other concurrent operations. ACID is the promise — but "promise" is doing a lot of work here. Different isolation levels make different sub-promises, and understanding exactly what each level prevents (and what it does NOT prevent) is essential for building correct concurrent applications.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define all four **ACID properties** with precision, without confusing Consistency with Isolation.
2. Describe the **transaction lifecycle**: BEGIN → operations → VALIDATION → COMMIT (WAL flush) or ABORT → ROLLBACK.
3. Name and describe the **read anomalies**: dirty read, non-repeatable read, phantom read, write skew.
4. Place each **ANSI isolation level** (Read Uncommitted, Read Committed, Repeatable Read, Serializable) in the anomaly matrix.
5. Explain **Snapshot Isolation** and why it prevents phantom reads but NOT write skew.
6. Explain why PostgreSQL's "Repeatable Read" is actually Snapshot Isolation.
7. Identify when to use `SELECT FOR UPDATE` vs `SELECT FOR SHARE` vs `SKIP LOCKED`.

---

## 🖼️ Visual Anchor

![db-16__fig2](db-16__fig2.svg)

*Figure 30.4.1 — ACID properties (four quadrants), transaction lifecycle, and the isolation level × anomaly matrix.*

---

## 📚 1. ACID Properties — Precise Definitions

### 1.1 Atomicity

**Atomicity** means all operations in a transaction either all commit or all roll back. There is no partial state visible to other transactions or left on disk after a crash.

**Enforced by:**
- **Undo log**: before modifying a row, the engine writes the *before image* to an undo log. If the transaction aborts, the before images are applied in reverse order.
- **WAL rollback records**: the WAL includes enough information to undo every modification if the transaction fails to commit.

**What it does NOT mean**: It does not mean "fast". A transaction that modifies 10 million rows is still atomic — it's just a very slow transaction.

### 1.2 Consistency

**Consistency** means the database moves from one valid state to another. "Valid" is defined by constraints, foreign keys, CHECK clauses, unique constraints, and trigger-enforced business rules.

**Enforced by:**
- Constraint checks at `COMMIT` time (or on each statement, depending on deferrability)
- Application logic (the C in ACID is partly the application's responsibility — the database can only check what you've expressed)

**What it does NOT mean**: Consistency in ACID is NOT the same as the C in CAP theorem (linearizability). They share a word; they are different concepts.

### 1.3 Isolation

**Isolation** means concurrent transactions execute as if they were serialized (run one at a time). In practice, databases offer multiple isolation levels — weaker guarantees with lower implementation cost.

**Enforced by:**
- Locking (2-phase locking — see [chapter 16.6](16.6---Concurrency-Control-&-MVCC))
- Multiversion concurrency control (MVCC — see [chapter 16.6](16.6---Concurrency-Control-&-MVCC))
- Serializable Snapshot Isolation (SSI — a recent optimistic approach)

### 1.4 Durability

**Durability** means committed transactions survive crashes. If the database says "commit successful", the data is on stable storage.

**Enforced by:**
- WAL flush to disk (`fsync`) before returning commit acknowledgement (see [chapter 16.5](16.5---Write-Ahead-Logging-&-Recovery))
- `synchronous_commit = on` in PostgreSQL (default) guarantees this
- `synchronous_commit = off` is faster but risks losing last ~200ms of commits on crash

---

## 📚 2. Transaction Lifecycle

### 2.1 The Five States

```
               READ/WRITE
                 ops
BEGIN ──────────────────→ VALIDATION ──→ COMMIT (WAL flush + return ACK)
  ↑                            │
  │    (if constraint fails,   │
  │     deadlock, timeout)     ↓
  └───────────────────────── ABORT ──→ ROLLBACK (apply undo log)
```

**VALIDATION** is when constraints are checked:
- `DEFERRED` constraints are checked at commit time
- `IMMEDIATE` constraints (default) are checked after each statement
- Foreign key checks, unique constraints, CHECK predicates

### 2.2 Savepoints

Transactions can have **savepoints** — internal checkpoints that allow partial rollback:

```sql
BEGIN;
  INSERT INTO orders (id, amount) VALUES (1001, 50.00);
  SAVEPOINT before_payment;
  UPDATE accounts SET balance = balance - 50.00 WHERE id = 9001;
  -- Oops, check failed
  ROLLBACK TO SAVEPOINT before_payment;
  -- order inserted, payment rolled back; can try again
COMMIT;
```

PostgreSQL implements savepoints via sub-transactions. Each `SAVEPOINT` assigns a sub-transaction ID; `ROLLBACK TO SAVEPOINT` applies undo records back to that point.

### 2.3 Two-Phase Commit (2PC) for Distributed Transactions

For transactions spanning multiple nodes/databases, PostgreSQL supports **two-phase commit**:

```sql
-- Coordinator
BEGIN;
-- ... operations on node A and node B ...
PREPARE TRANSACTION 'txn-20260526-001';  -- Phase 1: all nodes vote to commit
COMMIT PREPARED 'txn-20260526-001';       -- Phase 2: coordinator orders commit
-- (or ROLLBACK PREPARED if any node voted no)
```

2PC guarantees atomicity across nodes but blocks if the coordinator crashes between Phase 1 and Phase 2 (the "blocking problem"). Alternatives: Saga pattern (compensating transactions), or Paxos/Raft-based distributed transactions (CockroachDB, Spanner).

---

## 📚 3. Read Anomalies — The Catalogue

Before discussing isolation levels, we need to know exactly what we're protecting against.

### 3.1 Dirty Read

**Definition**: Transaction T2 reads a row that T1 has modified but not yet committed. If T1 later aborts, T2 has read a value that never officially existed.

```
T1: BEGIN; UPDATE balance SET amount=100 WHERE id=1;  -- not committed
T2: SELECT amount FROM balance WHERE id=1;  -- reads 100 (dirty!)
T1: ROLLBACK;  -- amount is actually still the old value
T2: made a decision based on a ghost value
```

### 3.2 Non-Repeatable Read

**Definition**: T2 reads a row, T1 updates and commits that row, T2 reads the same row again and gets a different value within the same transaction.

```
T2: SELECT amount FROM balance WHERE id=1;  -- returns 100
T1: UPDATE balance SET amount=200 WHERE id=1; COMMIT;
T2: SELECT amount FROM balance WHERE id=1;  -- returns 200 (different!)
```

### 3.3 Phantom Read

**Definition**: T2 runs a range query, T1 inserts a new row that falls within that range and commits, T2 runs the same range query and gets a different set of rows.

```
T2: SELECT COUNT(*) FROM orders WHERE customer_id=9001;  -- returns 5
T1: INSERT INTO orders (customer_id, ...) VALUES (9001, ...); COMMIT;
T2: SELECT COUNT(*) FROM orders WHERE customer_id=9001;  -- returns 6 (phantom!)
```

Phantom reads are harder to prevent than non-repeatable reads because you can't lock a row that doesn't exist yet. Solutions: **predicate locking** (lock the range, not just existing rows) or **MVCC snapshot** (don't see newly inserted rows within your snapshot).

### 3.4 Write Skew

**Definition**: Two transactions each read an overlapping set of rows, each decides to write based on what they read, and the combined result violates an invariant — even though each transaction individually appeared correct.

```
Invariant: at least one doctor must be on call at all times.
Currently: Doctor Alice (on_call=true), Doctor Bob (on_call=true)

T1: reads both doctors (both on call) → decides Alice can go off call
T2: reads both doctors (both on call) → decides Bob can go off call

T1 COMMITS: Alice → off call  (invariant: Bob still on call ✓)
T2 COMMITS: Bob  → off call  (invariant: VIOLATED — both off call ✗)
```

Write skew cannot happen with true Serializable isolation, but it CAN happen under Snapshot Isolation. This is the critical difference.

**Prevention**: Use `SELECT FOR UPDATE` to lock rows you depend on, or use PostgreSQL's Serializable (SSI) isolation level.

---

## 📚 4. ANSI Isolation Levels

### 4.1 The Anomaly Matrix

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Write Skew |
|---|---|---|---|---|
| **Read Uncommitted** | ✗ possible | ✗ possible | ✗ possible | ✗ possible |
| **Read Committed** | ✓ prevented | ✗ possible | ✗ possible | ✗ possible |
| **Repeatable Read** | ✓ prevented | ✓ prevented | ✗ possible (ANSI) | ✗ possible |
| **Snapshot Isolation** | ✓ prevented | ✓ prevented | ✓ prevented | ✗ possible ← **critical** |
| **Serializable** | ✓ prevented | ✓ prevented | ✓ prevented | ✓ prevented |

### 4.2 Read Uncommitted

Almost never used in practice. A transaction can read dirty (uncommitted) data from other transactions. Useful only for approximate analytics where absolute correctness is not required (e.g., "approximately how many users are logged in right now").

### 4.3 Read Committed

The **default in PostgreSQL** and many other databases. Each statement within a transaction sees a fresh snapshot of committed data as of the *statement's* start time. This prevents dirty reads but allows non-repeatable reads:

```sql
-- PostgreSQL default: READ COMMITTED
BEGIN;
SELECT balance FROM accounts WHERE id=1;  -- sees snapshot at T=10, balance=100
-- (another transaction commits, changes balance to 200)
SELECT balance FROM accounts WHERE id=1;  -- sees snapshot at T=15, balance=200 ← different!
COMMIT;
```

**Use Read Committed when**: your application logic can tolerate reading fresh data each statement, and non-repeatable reads are acceptable (most web applications).

### 4.4 Repeatable Read (Snapshot Isolation in PostgreSQL)

PostgreSQL's "Repeatable Read" is actually **Snapshot Isolation** — the database takes a snapshot of committed data at transaction start and uses it for the entire transaction.

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id=1;  -- snapshot at T=10, balance=100
-- (another transaction commits, changes balance to 200)
SELECT balance FROM accounts WHERE id=1;  -- still 100! (snapshot is frozen)
COMMIT;
```

Snapshot Isolation prevents dirty reads, non-repeatable reads, and phantom reads — but NOT write skew. This distinction matters for financial applications and any invariant spanning multiple rows.

### 4.5 Serializable (SSI in PostgreSQL)

PostgreSQL 9.1 introduced **Serializable Snapshot Isolation (SSI)**, an optimistic concurrency control algorithm that detects read-write conflicts and aborts transactions that would violate serializability:

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- ... read-write operations ...
COMMIT;  -- may fail with: ERROR: could not serialize access due to concurrent update
         -- application must retry the transaction
```

SSI adds minimal overhead (~10–15% write overhead, no read overhead) compared to traditional lock-based Serializable. It's the only PostgreSQL isolation level that prevents write skew without explicit `SELECT FOR UPDATE` locks.

---

## 📚 5. Choosing Isolation Levels in Practice

### 5.1 The Default is Not Always Safe

PostgreSQL's Read Committed default is correct for stateless single-row operations:

```sql
-- Safe under Read Committed (no read-modify-write cycle)
UPDATE accounts SET balance = balance - 50 WHERE id=9001;
```

But **not safe** for read-modify-write patterns:

```sql
-- NOT safe under Read Committed: classic TOCTOU race condition
BEGIN;
SELECT balance FROM accounts WHERE id=9001;  -- reads 200
-- (another transaction withdraws 150, commits)
UPDATE accounts SET balance = 50 WHERE id=9001;  -- based on stale read!
COMMIT;  -- balance is now 50, but should be 0 (or fail with overdraft)
```

**Fix 1**: `SELECT ... FOR UPDATE` acquires a row-level write lock:

```sql
BEGIN;
SELECT balance FROM accounts WHERE id=9001 FOR UPDATE;  -- locks row
-- no other transaction can modify this row until we commit
UPDATE accounts SET balance = balance - 50 WHERE id=9001;
COMMIT;
```

**Fix 2**: Use atomic `UPDATE` with condition:

```sql
UPDATE accounts SET balance = balance - 50
WHERE id=9001 AND balance >= 50;
-- check affected rows; if 0, the balance was insufficient
```

**Fix 3**: Use `ISOLATION LEVEL SERIALIZABLE` for complex invariants spanning multiple rows.

### 5.2 `SELECT FOR UPDATE` vs `SELECT FOR SHARE` vs `SKIP LOCKED`

| Variant | Effect |
|---|---|
| `SELECT FOR UPDATE` | Acquires exclusive lock on selected rows; blocks other `FOR UPDATE` and writes |
| `SELECT FOR SHARE` | Acquires shared lock; blocks `FOR UPDATE` and writes but not other `FOR SHARE` |
| `SELECT FOR UPDATE NOWAIT` | Fails immediately (raises error) if lock cannot be acquired |
| `SELECT FOR UPDATE SKIP LOCKED` | Skips rows that are already locked; returns unlocked rows only |

**`SKIP LOCKED` use case** — job queue processing:

```sql
-- Worker pattern: each worker picks an unprocessed job without contention
BEGIN;
SELECT id, payload FROM job_queue
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- process the job
UPDATE job_queue SET status = 'done' WHERE id = $1;
COMMIT;
```

Multiple workers can run this concurrently — each picks a different job atomically.

---

## 📚 6. Worked Example: The Doctor On-Call Write Skew Bug

This is the canonical write skew example from DDIA Chapter 7.

```sql
CREATE TABLE doctors (id INT, name TEXT, on_call BOOL);
INSERT INTO doctors VALUES (1, 'Alice', true), (2, 'Bob', true);

-- Constraint we want to enforce (not a database constraint — app logic):
-- At least 1 doctor must be on_call = true at all times

-- WRONG (Snapshot Isolation — write skew possible):
BEGIN ISOLATION LEVEL REPEATABLE READ;
  -- Check: how many doctors on call?
  SELECT COUNT(*) FROM doctors WHERE on_call = true;  -- returns 2
  -- Decide: since 2 are on call, we can take Alice off
  UPDATE doctors SET on_call = false WHERE name = 'Alice';
COMMIT;

-- Concurrently, Bob runs the same transaction and takes Bob off call
-- Result: 0 doctors on call. Invariant violated despite "repeatable read".

-- FIX 1: Use SELECT FOR UPDATE
BEGIN;
  SELECT COUNT(*) FROM doctors WHERE on_call = true FOR UPDATE;  -- locks all on-call rows
  UPDATE doctors SET on_call = false WHERE name = 'Alice';
COMMIT;

-- FIX 2: Use SERIALIZABLE isolation
BEGIN ISOLATION LEVEL SERIALIZABLE;
  SELECT COUNT(*) FROM doctors WHERE on_call = true;
  UPDATE doctors SET on_call = false WHERE name = 'Alice';
COMMIT;  -- SSI detects the conflict; one transaction aborts, application retries
```

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [16.5 - Write-Ahead Logging & Recovery](16.5---Write-Ahead-Logging-&-Recovery) — how Durability is implemented mechanically
- [16.6 - Concurrency Control & MVCC](16.6---Concurrency-Control-&-MVCC) — how Isolation is implemented (2PL and MVCC)
- [Subject_Plan](Subject_Plan) — SQL-level transaction syntax

### External
- [DDIA Chapter 7 — Transactions (Kleppmann)](https://dataintensive.net/)
- [CMU 15-445 Lecture 17 — Transactions](https://15445.courses.cs.cmu.edu/)
- [CMU 15-445 Lecture 18 — Timestamp Ordering Concurrency Control](https://15445.courses.cs.cmu.edu/)
- [PostgreSQL Documentation — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [Serializable Snapshot Isolation paper — Cahill et al. 2009](https://dl.acm.org/doi/10.1145/1559845.1559850)
- [Hermitage — test suite for isolation level anomalies (github.com/ept/hermitage)](https://github.com/ept/hermitage)

---

## ⚠️ 8. Common Misconceptions

- **"ACID means the database is always correct."** No — ACID means the database enforces its own constraints and provides isolation guarantees. If your application logic has bugs, ACID won't save you. "Consistency" is partially the application's responsibility.
- **"Snapshot Isolation is Serializable."** They are different. Snapshot Isolation allows write skew. PostgreSQL's `REPEATABLE READ` is Snapshot Isolation. To get true Serializable, use `ISOLATION LEVEL SERIALIZABLE`.
- **"Read Committed prevents all problems."** It prevents dirty reads only. Non-repeatable reads and write skew are still possible. Most web application bugs involving stale reads happen at Read Committed.
- **"SERIALIZABLE is too slow for production."** PostgreSQL's SSI (since v9.1) has ~10–15% overhead over Snapshot Isolation for typical workloads. For applications where correctness matters, the overhead is justified.
- **"BEGIN is the same as LOCK."** BEGIN starts a transaction. It does NOT acquire any locks. Locks are acquired on `SELECT FOR UPDATE`, `INSERT`, `UPDATE`, `DELETE`, or explicitly with `LOCK TABLE`.

---

*Next: [16.5 - Write-Ahead Logging & Recovery](16.5---Write-Ahead-Logging-&-Recovery) — How a power cut doesn't lose your committed data.*

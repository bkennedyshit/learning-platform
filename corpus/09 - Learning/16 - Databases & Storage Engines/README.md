---
date: 2026-05-26
type: subject-readme
tags: [databases, storage-engines, b-tree, lsm-tree, wal, mvcc, acid, raft, query-processing, replication]
title: "README — 16 - Databases & Storage Engines"
---

# 16 - Databases & Storage Engines — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/dbs__<chapter>-fig<n>.svg` and embedded inline via `![[dbs__30.x-figN.svg]]`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, GitHub, or in your local sidecar (gitignored). Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick start

```bash
# Navigate to the track folder
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/16 - Databases & Storage Engines"

# Spin up a local Postgres to run examples from chapter notes
docker run --name pg-internals -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16

# Or use DuckDB in-process (no server needed)
python3 -c "import duckdb; print(duckdb.sql('SELECT version()').fetchone())"

# CMU 15-445 lecture playlist (free)
# open: https://www.youtube.com/playlist?list=PLSE8ODhjZXjbj8BMuIrRcacnQh20hmY9g
```

---

## 📜 Chapter Index

- [[16.1 - Storage Engine Fundamentals]]
- [[16.2 - B-Trees & Page Management]]
- [[16.3 - LSM-Trees & Write-Optimized Storage]]
- [[16.4 - Transaction Management & ACID]]
- [[16.5 - Write-Ahead Logging & Recovery]]
- [[16.6 - Concurrency Control & MVCC]]
- [[16.7 - Query Processing & Execution]]
- [[16.8 - Distributed Databases & Replication]]

---

## 🎬 Video & Picture References (external — open in browser)

> Open-source / pro-grade media that supplements the chapter notes. Not stored in this repo.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **CMU 15-445 — Database Systems (Andy Pavlo)** | The entire track — storage, B-trees, transactions, recovery, concurrency, query execution | [15445.courses.cs.cmu.edu](https://15445.courses.cs.cmu.edu/) / [YouTube playlist](https://www.youtube.com/playlist?list=PLSE8ODhjZXjbj8BMuIrRcacnQh20hmY9g) |
| **CMU 15-721 — Advanced Database Systems** | Column stores, vectorized execution, HTAP | [15721.courses.cs.cmu.edu](https://15721.courses.cs.cmu.edu/) |
| **MIT 6.824 — Distributed Systems (Robert Morris)** | Raft, Paxos, Spanner, ZooKeeper | [pdos.csail.mit.edu/6.824](https://pdos.csail.mit.edu/6.824/) |
| **Hussein Nasser — Postgres Deep Dives** | MVCC internals, EXPLAIN ANALYZE walkthroughs, VACUUM | [@hnasr](https://www.youtube.com/@hnasr) |
| **ByteByteGo** | Visual explainers: B-trees, LSM-trees, ACID | [@ByteByteGo](https://www.youtube.com/@ByteByteGo) |
| **Martin Kleppmann — DDIA Lectures** | Cambridge lecture series matching DDIA chapters | [youtube.com/channel/UClnL0vDhFzZLMwEMYdKJoIQ](https://www.youtube.com/channel/UClnL0vDhFzZLMwEMYdKJoIQ) |
| **Alex Petrov — Database Internals Talks** | B-tree variants, LSM-tree tuning, distributed storage | Search "Alex Petrov database" on YouTube |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **CMU 15-445 lecture slides** | The best diagrams of B-tree splits, buffer pool, ARIES phases | [15445.courses.cs.cmu.edu](https://15445.courses.cs.cmu.edu/) → Schedule |
| **PostgreSQL storage documentation** | Official page layout diagrams, WAL format, MVCC visibility rules | [postgresql.org/docs/current/storage.html](https://www.postgresql.org/docs/current/storage.html) |
| **RocksDB wiki** | LSM-tree compaction diagrams, tuning guides | [github.com/facebook/rocksdb/wiki](https://github.com/facebook/rocksdb/wiki) |
| **Raft visualization** | Interactive Raft election + log replication animation | [raft.github.io](https://raft.github.io/) |
| **The Red Book — Readings in Database Systems** | Curated research papers with editorial commentary | [redbook.io](http://www.redbook.io/) |
| **Use The Index, Luke** | Visual B-tree index tutorial for developers | [use-the-index-luke.com](https://use-the-index-luke.com/) |

### 📚 Open-Source / Free Books

| Title | Author | Link |
|---|---|---|
| Designing Data-Intensive Applications (Ch. 3, 7–9) | Martin Kleppmann | [dataintensive.net](https://dataintensive.net/) |
| Database Internals (preview chapters) | Alex Petrov | [databass.dev](https://www.databass.dev/) |
| Architecture of a Database System (free PDF) | Hellerstein, Stonebraker, Hamilton | [dsf.berkeley.edu/papers](http://dsf.berkeley.edu/papers/fntdb07-architecture.pdf) |
| Readings in Database Systems (Red Book, 5th ed) | Hellerstein & Stonebraker | [redbook.io](http://www.redbook.io/) |
| LevelDB source code & implementation notes | Jeff Dean / Sanjay Ghemawat | [github.com/google/leveldb](https://github.com/google/leveldb) |
| SQLite file format documentation | D. Richard Hipp | [sqlite.org/fileformat.html](https://www.sqlite.org/fileformat.html) |

---

## 🔭 2026 Industry Snapshot

> Sources rephrased for compliance — never more than 30 consecutive words from any single source.

| Area | 2026 Reality | Sources |
|---|---|---|
| PostgreSQL | v17 (Oct 2024) shipped incremental backup + VACUUM improvements. v18 (late 2026) expected with better logical replication and JIT improvements. | [postgresql.org/about/news](https://www.postgresql.org/about/news/) |
| DuckDB | Reached 1.0 in 2024; now the standard embedded OLAP engine. Queries Parquet/Arrow/CSV in-process. Used widely in data engineering pipelines. | [duckdb.org](https://duckdb.org/) |
| RocksDB ecosystem | Underlies TiKV, MyRocks, CockroachDB Pebble, Yugabyte DocDB. The LSM-tree pattern is now the write-optimized storage primitive of choice. | [github.com/facebook/rocksdb](https://github.com/facebook/rocksdb) |
| Raft consensus | Now the default consensus mechanism across etcd, CockroachDB, TiKV, Kafka (KRaft). The Paxos vs Raft debate has largely settled in Raft's favour for new systems. | [raft.github.io](https://raft.github.io/) |
| HTAP convergence | TiDB (TiKV + TiFlash), SingleStore, and PostgreSQL extensions push toward hybrid TP+AP. The OLTP/OLAP boundary is blurring. | [pingcap.com](https://pingcap.com/) |
| NVMe / NVM | 100–200 µs NVMe SSDs are forcing re-evaluation of buffer pool and WAL designs. "Storage is almost RAM" challenges design assumptions from the HDD era. | [vldb.org](https://vldb.org/) |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz (B-tree splits, ACID anomalies, ARIES phases, MVCC xmin/xmax)

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: Anki deck (B-tree height invariant; ACID definitions; isolation anomalies; Bloom filter FP formula; ARIES 3 phases; Raft quorum rule)

### 🎬 Video overviews
- [ ] TODO: Personal recording walking through a EXPLAIN ANALYZE output live

### 📋 Data tables
- [ ] TODO: comparison matrices (PostgreSQL vs MySQL vs SQLite storage internals; B-tree vs LSM-tree WA/RA/SA; isolation levels × anomalies; join algorithms × conditions)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/16 - Databases & Storage Engines/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/16 - Databases & Storage Engines/LEARNING_PATH]]
- SQL querying fundamentals: [[../14 - SQL/Subject_Plan]]
- OS essentials (disk I/O, page cache): [[../01- Python/1.10 - Operating Systems Essentials]]
- Networking essentials: [[../01- Python/1.11 - Computer Networks Essentials]]
- Concurrency model (threads, locks): [[../01- Python/1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL]]
- System Design (when to choose which DB): [[../19 - System Design & Distributed Architecture/Subject_Plan]]
- System Design — Databases at Scale: [[../19 - System Design & Distributed Architecture/27.3 - Databases at Scale]]
- DevOps & SRE (autovacuum, replication monitoring): [[../20 - DevOps & SRE/Subject_Plan]]
- Cloud Platforms (RDS, Aurora, Spanner): [[../21 - Cloud Platforms/Subject_Plan]]
- Rust (build your own storage engine): [[../11 - Rust/Subject_Plan]]
- AI/ML Systems (vector indexes, pgvector): [[../23 - AI & Machine Learning Systems/Subject_Plan]]
- Scaling north star: [[BUILDING_AT_SCALE]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]

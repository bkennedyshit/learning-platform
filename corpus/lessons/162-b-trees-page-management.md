---
title: "16.2 — B-Trees & Page Management"
subject: "Databases & Storage Engines"
catalog: advanced
audience_tier: higher-education
chapter: "16.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 16.2 — B-Trees & Page Management

> *"The B-tree is the duct tape of data structures. It goes everywhere and it works."* — paraphrased, attributed to various database educators

> *"Every production database that stores data on disk uses a B-tree. Even the ones that say they don't — they have a B-tree somewhere."*

The B+ tree is the single most important data structure in storage systems. It powers the primary key and every secondary index in PostgreSQL, MySQL InnoDB, SQLite, Oracle, and SQL Server. Understanding it at the page level — not just as an abstract tree — is what separates "I know what an index is" from "I understand why an index costs what it costs."

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the **B+ tree anatomy**: internal nodes (keys + pointers), leaf nodes (keys + record pointers + sibling link), and the height invariant.
2. Prove that **search is O(log n)** given the tree order and height formula.
3. Walk through a **full insert with node split** in a 4-key-order tree, including split propagation to the root.
4. Explain **delete with merge and rotation** and know when each applies.
5. Explain why **page size = OS page size** (4 KB or 8 KB alignment + I/O amplification avoidance).
6. Describe the **PostgreSQL heap page layout** in detail (header, line pointers, ctid, xmin, xmax).
7. Explain **HOT updates** (Heap-Only Tuples) and how they reduce index churn.

---

## 🖼️ Visual Anchor

![dbs__30.2-fig1](dbs__30.2-fig1.svg)

*Figure 30.2.1 — B+ tree: internal nodes (blue) with keys and child pointers, leaf nodes (green) with data pointers and sibling links, plus a worked 4-key-order insert split.*

---

## 📚 1. The B-Tree Family — B vs B+

### 1.1 Why "B-Tree" vs "B+ Tree"?

Rudolf Bayer and Edward McCreight invented the B-tree in 1970. The common variant used in databases is the **B+ tree** (sometimes written B+-tree or B⁺-tree):

| Property | B-tree | B+ tree |
|---|---|---|
| Data stored | Internal nodes AND leaf nodes | **Leaf nodes only** |
| Internal nodes | Keys + pointers + data values | Keys + pointers only |
| Leaf nodes | Keys + data | Keys + data + **sibling pointer** |
| Range scans | Must traverse tree (no sibling links) | **O(1) after first lookup** via leaf linked list |
| Real-world use | Rarely used in databases | **Used in virtually all databases** |

The critical B+ tree difference: since data lives only in leaf nodes, internal nodes can hold more keys (they're smaller without data), keeping the tree height lower for the same number of records.

### Definition 16.2.1 — B+ Tree Order

A B+ tree of **order n** (also called **degree n** or **branching factor n**) satisfies:
- Every internal node has **at most n pointers** (and n−1 keys)
- Every internal node (except the root) has **at least ⌈n/2⌉ pointers**
- The root has **at least 2 pointers** (unless it is a leaf)
- Every leaf has **at most n−1 keys + values**
- Every leaf has **at least ⌈(n−1)/2⌉ keys** (the half-full invariant)

These rules maintain the **height invariant**: all leaf nodes are at the same depth.

---

## 📚 2. B+ Tree Anatomy

### 2.1 Internal Nodes

An internal node stores keys and child pointers. It acts purely as a routing structure — you never store actual data (row values) in an internal node.

```
Internal node (order 5 example — up to 4 keys, 5 pointers):

[ P0 | K1 | P1 | K2 | P2 | K3 | P3 | K4 | P4 ]
  ↑          ↑          ↑          ↑          ↑
 child 0   child 1   child 2   child 3   child 4

Routing rule:
  keys in child 0:          key < K1
  keys in child 1:  K1 ≤   key < K2
  keys in child 2:  K2 ≤   key < K3
  keys in child 3:  K3 ≤   key < K4
  keys in child 4:  K4 ≤   key
```

### 2.2 Leaf Nodes

A leaf node stores the actual key-value pairs and a pointer to the next leaf sibling:

```
Leaf node (order 5 — up to 4 key-value pairs):

[ K1→V1 | K2→V2 | K3→V3 | K4→V4 | NEXT_LEAF → ]
                                        ↑
                              pointer to next leaf (for range scans)

V = either:
  (a) the full row data (clustered/index-organized tables — MySQL InnoDB)
  (b) a (page, offset) "tuple ID" (ctid) pointing to the heap
      (unclustered/heap indexes — PostgreSQL B-tree indexes)
```

**PostgreSQL uses unclustered B-tree indexes by default**: the leaf value is a `ctid = (page_number, line_pointer_index)`. To get the full row, the executor does a **heap fetch** using that ctid. This extra hop is why a sequential heap scan can sometimes beat an index scan at low selectivity.

### 2.3 The Sibling Linked List

All leaf nodes are linked in a doubly-linked list from left to right (sorted key order). This enables **efficient range scans**:

```sql
SELECT * FROM orders WHERE created_at BETWEEN '2026-01-01' AND '2026-06-01';
```

1. Traverse from root to the leaf containing `2026-01-01` — O(log n) I/Os.
2. Follow sibling pointers rightward collecting all qualifying keys — O(k/n) I/Os where k is the number of qualifying rows and n is leaf page capacity.

Without sibling links, a range scan would require ascending back up the tree for every page — O(k log n).

---

## 📚 3. Search: O(log n) Proof

### 3.1 Height Formula

For a B+ tree of order n storing N records in leaf nodes:
- Each leaf holds up to n−1 keys, so minimum leaves = ⌈N / (n−1)⌉
- Each internal node has branching factor n, so height h satisfies:
  - n^h ≥ ⌈N / (n−1)⌉
  - h ≥ log_n(N / (n-1)) ≈ log_n(N) for large N

**Typical numbers** for PostgreSQL with 8 KB pages and integer keys:
- 8 KB internal node ≈ 8192 / (8+8) ≈ 512 keys (where 8 bytes = key, 8 bytes = pointer)
- 1 million rows → height = ⌈log₅₁₂(1,000,000)⌉ = 3 levels
- 1 billion rows → height = ⌈log₅₁₂(1,000,000,000)⌉ = 4 levels

**This means:** for any table up to 1 billion rows, finding a row by primary key requires at most **4 page reads** (4 I/Os).

### 3.2 The Search Algorithm

```
function search(node, key):
    if node is leaf:
        return linear_scan_for(key, node.entries)
    else:
        i = largest i such that node.keys[i] ≤ key
        return search(node.children[i], key)

Complexity: O(h × n) comparisons at most
           = O(log_n(N) × n)   [within each node, linear scan of n keys]
           ≈ O(log(N) / log(n) × n)
           = O(log N)          [n factors cancel in big-O]
```

In practice, each node fits in one page, so each level of the tree = one I/O = one buffer pool lookup. The O(log n) bound is really an I/O bound.

---

## 📚 4. Insert with Node Splits — Full Worked Example

We use a **4-key-order tree** (order n=4: max 3 keys per leaf, max 3 keys per internal node, min 2 children for non-root).

### Starting State

```
Root (internal): [ 30 | 70 ]
  ↙               ↓              ↘
Leaf A:          Leaf B:          Leaf C:
[10 | 20 | 25]  [30 | 50 | 60]  [70 | 80 | 90]
   ↕                  ↕               ↕
sibling links (→ next leaf)
```

### Insert key 35

Step 1: Traverse root. Key 35 is between 30 and 70, so descend to Leaf B.
Step 2: Leaf B has keys [30 | 50 | 60]. Key 35 goes between 30 and 50.
Step 3: Leaf B has room (only 3 keys, max is 3 for order-4). Insert directly.

```
Leaf B after insert: [30 | 35 | 50 | 60]  ← Wait! That's 4 keys — overflow!
```

Actually, order-4 means max n−1=3 keys per leaf. Leaf B is **full before** inserting 35 (it has exactly 3 keys). Let's restart with a slightly different starting state to show the split cleanly:

### Revised Starting State (Leaf B is full)

```
Root (internal): [ 50 ]
  ↙                    ↘
Leaf A: [10|20|30|40]  Leaf B: [50|60|70|80]
(4 keys = full, order-5 tree where max = 4 keys)
```

### Insert key 55

Step 1: Traverse root. Key 55 ≥ 50, so descend to Leaf B.
Step 2: Leaf B is **full** (4 keys in order-5 tree where max = 4).

**→ Split Leaf B:**

```
Before: Leaf B: [50 | 60 | 70 | 80] + insert 55

Sort: [50 | 55 | 60 | 70 | 80]  (5 keys)

Split at midpoint (⌊5/2⌋ = 2):
  Left half:  New Leaf B_left:  [50 | 55]
  Right half: New Leaf B_right: [60 | 70 | 80]

Promote first key of right half to parent: promote 60
```

Step 3: Push promoted key 60 to root. Root currently has [50]. Insert 60.

```
Root after: [ 50 | 60 ]
  ↙             ↓          ↘
Leaf A:     Leaf B_left:  Leaf B_right:
[10|20|30|40] [50|55]    [60|70|80]
```

Leaf B_left and B_right are linked as siblings.

### Insert key 25 (triggers split that propagates to root)

Starting from:
```
Root (internal): [ 30 | 60 ]
  ↙                  ↓             ↘
Leaf A: [10|20]   Leaf B: [30|40|50|55]   Leaf C: [60|70|80]
```

Leaf B is full (4 keys). Insert 25 → goes to Leaf A (25 < 30). Leaf A has room. Insert directly:

```
Leaf A after: [10|20|25]  ← fits fine
```

Now let's consider the case where the split propagates. Insert 22 when Leaf A is also full:

```
Starting: Root: [30]
  ↙                    ↘
Leaf A: [10|15|20|25]   Leaf B: [30|40|50|60]
(both full in an order-5 tree)
```

**Insert 22:**

Step 1: 22 < 30, go to Leaf A.
Step 2: Leaf A is full → Split.

```
Sort [10|15|20|22|25]:
  Left:  [10|15]
  Right: [20|22|25]  ← promote 20 to parent
```

Step 3: Promote 20 to root. Root currently has [30]. Insert 20.

```
Root after insert: [20|30]
  ↙           ↓          ↘
[10|15]  [20|22|25]  [30|40|50|60]
```

**Root split (when root overflows):**

If the root was already full, we split the root and create a **new root** — this is the ONLY case where the tree height increases:

```
Example: Root is full [10|20|30|40], inserting new key causes split:
  Split root into two nodes + create new empty root
  New tree height = old height + 1
```

---

## 📚 5. Delete: Merges and Rotations

### 5.1 Delete Algorithm

Deleting a key from a B+ tree:

1. Find the leaf containing the key. Remove it.
2. If the leaf is still at least half-full → done.
3. If the leaf is **underflowing** (below ⌈(n-1)/2⌉ keys):
   - Try **rotation from a sibling**: borrow a key from an adjacent sibling via the parent. Update the separator key in the parent.
   - If sibling is also at minimum → **merge** the two leaves into one. Remove the separator key from the parent.
4. If the parent now underflows, recursively apply the same merge/rotate logic up the tree.
5. If the root has only one child after a merge → remove the root, child becomes new root. Tree height decreases.

### 5.2 Rotation Example

```
Parent: [30]
  ↙          ↘
[10|20|25]   [30|40|50]  ← delete 40

After delete 40: [30|50] (still half-full in order-4 → 2 keys ≥ ⌈(4-1)/2⌉=2 ✓)
No rotation needed.
```

Now delete 50:

```
Parent: [30]
  ↙          ↘
[10|20|25]   [30]  ← only 1 key, underflow!

Left sibling has 3 keys [10|20|25] — can donate.
Rotate: move 25 up to parent as separator, bring old separator 30 down to right leaf:

Parent: [25]
  ↙          ↘
[10|20]   [25|30]
```

If left sibling had only 2 keys (the minimum), rotation is impossible → merge:

```
Merge: combine [10|20] and [30] into [10|20|30], remove parent separator
```

---

## 📚 6. Page Size = OS Page Size — Why Alignment Matters

### 6.1 The I/O Amplification Argument

Disk I/O (and SSD I/O) operates in units of the OS page size (typically 4 KB). If a database page is 1 KB, then fetching one database page requires reading 4 KB from the device — 4× **I/O amplification**. If the database page is exactly 4 KB or 8 KB (two OS pages), there is no sub-page amplification.

### 6.2 The Bus Width Argument

Modern CPUs, memory controllers, PCIe interfaces, and NVMe protocols all work with aligned power-of-two chunks. Misaligned structures that straddle alignment boundaries require more transactions and may trigger hardware penalties.

### 6.3 The B-tree Branching Factor Argument

Larger pages hold more keys per internal node → higher branching factor → lower tree height → fewer I/Os per lookup. The sweet spot for OLTP is typically 4–16 KB:

```
4 KB page,  8-byte key + 8-byte pointer: ~250 keys/internal node → height 4 for 3.9B rows
8 KB page,  8-byte key + 8-byte pointer: ~512 keys/internal node → height 3 for 134M rows  ← Postgres default
16 KB page, 8-byte key + 8-byte pointer: ~1024 keys/internal node → height 3 for 1B rows   ← MySQL InnoDB default
```

**PostgreSQL uses 8 KB** because it matches the Linux/macOS default huge page boundary for mmap, and 512 keys/node is a sweet spot for OLTP trees. If you need to change it, you must recompile PostgreSQL (it's `BLCKSZ`).

---

## 📚 7. PostgreSQL Heap Page Layout — Deep Dive

### 7.1 The PostgreSQL Heap Page in Bytes

```
 0                   8192
 ├──────────────────────────────────────────────────────────────────────┤
 │ PageHeader (24 bytes)                                                 │
 │   pd_lsn          (8 bytes)  — LSN when page was last modified       │
 │   pd_checksum     (2 bytes)  — page checksum (if enabled)            │
 │   pd_flags        (2 bytes)  — HAS_FREE_LINES | HAS_DEAD_TUPLES etc  │
 │   pd_lower        (2 bytes)  — offset to start of free space         │
 │   pd_upper        (2 bytes)  — offset to end of free space           │
 │   pd_special      (2 bytes)  — offset to special data (index pages)  │
 │   pd_pagesize_version (2 bytes)                                       │
 ├──────────────────────────────────────────────────────────────────────┤
 │ ItemId array (4 bytes each)                                           │
 │   ItemId[0]: lp_off=192, lp_flags=NORMAL, lp_len=54                  │
 │   ItemId[1]: lp_off=138, lp_flags=NORMAL, lp_len=52                  │
 │   ItemId[2]: lp_off=... (HOT redirect, lp_flags=REDIRECT)            │
 │   ...                                                                 │
 │   pd_lower advances → with each new ItemId                           │
 ├────────────────────── pd_lower ──────────────────────────────────────┤
 │                     FREE SPACE                                        │
 ├────────────────────── pd_upper ──────────────────────────────────────┤
 │ Tuple N (oldest insertion at highest offset → grows downward)         │
 │   HeapTupleHeader:                                                    │
 │     t_xmin:   XID that inserted this row version                      │
 │     t_xmax:   XID that deleted/updated this row (0 = still live)     │
 │     t_ctid:   (page, offset) of current version (self if current)    │
 │     t_infomask: flags (HEAP_XMIN_COMMITTED, HEAP_HAS_NULL, etc.)     │
 │     t_hoff:   offset to user data within this header                  │
 │   User data: actual column values (null bitmap + varlena fields)      │
 │ ...                                                                   │
 │ Tuple 1 (most recently inserted tuple near pd_upper)                  │
 ├──────────────────────────────────────────────────────────────────────┤
 │ Special space (for heap pages: empty; for B-tree pages: high key)     │
 └──────────────────────────────────────────────────────────────────────┘
```

### 7.2 Inspecting a Real Page

```sql
-- Enable the pageinspect extension (available in PostgreSQL)
CREATE EXTENSION pageinspect;

-- See raw page header info
SELECT * FROM page_header(get_raw_page('orders', 0));

-- See heap tuples on page 0 of the orders table
SELECT lp, lp_off, lp_flags, lp_len, t_xmin, t_xmax, t_ctid,
       t_infomask::bit(16)
FROM heap_page_items(get_raw_page('orders', 0));

-- Typical output shows:
-- lp=1, lp_off=8136, lp_len=54, t_xmin=1234567, t_xmax=0, t_ctid=(0,1)
-- → tuple 1, written at byte 8136, alive (t_xmax=0), ctid points to itself
```

### 7.3 HOT Updates (Heap-Only Tuples)

A normal `UPDATE` in PostgreSQL:
1. Marks the old tuple dead (`t_xmax = current XID`)
2. Inserts a new tuple version (possibly on a different page)
3. Updates ALL indexes that reference the old tuple to point to the new tuple

This means a single-column update touches potentially dozens of index pages for no reason — if the updated column is not indexed, the indexes still point to valid data via the old ctid.

**HOT (Heap-Only Tuple) update** solves this:
- If the updated columns are not in any index, AND the new tuple fits on the SAME PAGE as the old tuple:
- Set `lp_flags = REDIRECT` on the old ItemId, pointing to the new tuple's ItemId
- Do NOT update any index — the index still points to the old ItemId, which redirects to the new tuple

```
Before HOT update:
Index → ItemId[3] → Tuple (old, t_xmax set)
                         ↕ t_ctid
                    ItemId[4] → Tuple (new, t_xmax=0)

After HOT: index unchanged, ItemId[3] has lp_flags=REDIRECT pointing to ItemId[4]
```

HOT updates dramatically reduce index write amplification for updates that don't touch indexed columns (e.g., updating a `last_seen` timestamp that isn't indexed).

---

## 📚 8. B-Tree Index Internals in PostgreSQL

### 8.1 PostgreSQL B-Tree Implementation (nbtree)

PostgreSQL's B-tree (called **nbtree** internally) uses the **Lehman-Yao concurrent B-tree** algorithm, which allows concurrent access with minimal locking:

- Each non-rightmost page has a **high key** (the first key in the sibling to the right) stored in the special area at the end of the page.
- If a search or split finds a key equal to the high key, it follows the rightward pointer — this allows concurrent splits without holding locks on parent pages.

### 8.2 Index Page Layout

```sql
-- See B-tree index pages using pageinspect
SELECT * FROM bt_page_stats('orders_pkey', 1);
-- Returns: type (leaf/internal), live_items, dead_items, avg_item_size, etc.

SELECT itemoffset, ctid, itemlen, nulls, vars, data
FROM bt_page_items('orders_pkey', 1);
-- Shows each entry: key value + ctid (heap tuple pointer)
```

### 8.3 FILLFACTOR and Index Bloat

PostgreSQL B-tree indexes have a `FILLFACTOR` parameter (default 90 for indexes, 100 for heaps) that leaves some free space in each page to accommodate inserts without immediate splits. A `FILLFACTOR` of 70 means 30% of each page is reserved for future inserts:

```sql
CREATE INDEX CONCURRENTLY idx_orders_customer
ON orders (customer_id)
WITH (fillfactor = 70);
```

Over time, deleted and updated tuples leave dead entries in B-tree pages. `VACUUM` marks dead entries, and eventually `REINDEX` or `VACUUM FULL` reclaims space.

---

## 🔗 9. Cross-links & Further Reading

### Internal
- [16.1 - Storage Engine Fundamentals](16.1---Storage-Engine-Fundamentals) — heap files and the buffer pool that backs these pages
- [16.3 - LSM-Trees & Write-Optimized Storage](16.3---LSM-Trees-&-Write-Optimized-Storage) — the alternative to update-in-place
- [16.6 - Concurrency Control & MVCC](16.6---Concurrency-Control-&-MVCC) — xmin, xmax, and HOT tuple visibility
- [16.7 - Query Processing & Execution](16.7---Query-Processing-&-Execution) — when the planner chooses an index scan vs sequential scan
- [Subject_Plan](Subject_Plan) — the SQL indexes you create map to these B+ tree structures

### External
- [CMU 15-445 Lecture 7 — Tree Indexes I](https://15445.courses.cs.cmu.edu/)
- [CMU 15-445 Lecture 8 — Tree Indexes II](https://15445.courses.cs.cmu.edu/)
- [Database Internals — Alex Petrov, Ch. 2–4 (B-tree storage)](https://www.databass.dev/)
- [Use The Index, Luke — B-tree index visual tutorial](https://use-the-index-luke.com/)
- [PostgreSQL nbtree README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README)
- [PostgreSQL pageinspect extension](https://www.postgresql.org/docs/current/pageinspect.html)
- [Lehman-Yao concurrent B-tree paper (1981)](https://dl.acm.org/doi/10.1145/319628.319663)

---

## ⚠️ 10. Common Misconceptions

- **"B-tree means B+tree."** In database contexts, "B-tree" almost always means B+tree. True B-trees with data in internal nodes are almost never used in practice.
- **"An index always makes the query faster."** Only for high-selectivity queries. For a full-table scan, a sequential heap read is 1 I/O per 8 KB page; an index scan is 1 I/O per leaf entry + 1 I/O per heap fetch. If >20% of the table matches, sequential scan wins.
- **"B-tree splits are fast."** A split writes two new pages. If those pages aren't in the buffer pool, that's potentially 2 random I/Os. Splits cascade — a full root split creates 3 new pages. In pathological insert patterns (sorted sequential inserts into a non-clustered index), splits are very frequent.
- **"Index bloat is not a real problem."** Dead entries in B-tree pages prevent new entries from fitting, forcing premature splits. Regular `VACUUM` (or `REINDEX CONCURRENTLY`) is essential for write-heavy indexes.
- **"Clustered and unclustered indexes are the same."** PostgreSQL heaps are unclustered — the physical order of pages has no relationship to any index. MySQL InnoDB's primary key index IS the table (clustered). In PostgreSQL, `CLUSTER` rewrites the table in index order but it doesn't stay clustered after writes.

---

*Next: [16.3 - LSM-Trees & Write-Optimized Storage](16.3---LSM-Trees-&-Write-Optimized-Storage) — Why Cassandra is faster to write than Postgres, and what that costs you.*

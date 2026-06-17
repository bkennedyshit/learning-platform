---
title: "14.2 — SELECT Mastery — Joins, Subqueries, CTEs"
subject: "SQL"
catalog: advanced
audience_tier: higher-education
chapter: "14.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 14.2 — SELECT Mastery — Joins, Subqueries, CTEs

> *"The join is the most important operation in relational databases. Get it wrong and you get wrong answers. Get it right and you unlock the full power of the relational model."* — C.J. Date

Joins are where relational databases earn their name. A single table is just a spreadsheet. The moment you connect tables through joins, you're leveraging the relational model's true power — normalized data with zero redundancy, reassembled on demand into any shape your query requires.

This chapter covers every join type, subquery pattern, and CTE technique you'll encounter in production systems, data pipelines, and coding interviews.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write and reason about INNER, LEFT, RIGHT, FULL OUTER, CROSS, and LATERAL joins.
2. Understand the physical execution strategies (nested loop, hash join, merge join) and when each is chosen.
3. Use scalar subqueries, correlated subqueries, EXISTS/NOT EXISTS, and IN/NOT IN correctly.
4. Compose complex queries using Common Table Expressions (CTEs) for readability and reuse.
5. Identify and fix common join pitfalls (fan-out, NULL handling, accidental cross joins).

---

## 🖼️ Visual Anchor — Join Types Venn Diagram

![sql-14__fig1](sql-14__fig1.svg)

---

## 📚 1. The JOIN Family

### Setup: Sample Schema

All examples use this schema:

```sql
CREATE TABLE departments (
    dept_id   INTEGER PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    emp_id     INTEGER PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    dept_id    INTEGER REFERENCES departments(dept_id),
    salary     NUMERIC(10,2),
    manager_id INTEGER REFERENCES employees(emp_id),
    hire_date  DATE
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    title      VARCHAR(100) NOT NULL,
    budget     NUMERIC(12,2)
);

CREATE TABLE assignments (
    emp_id     INTEGER REFERENCES employees(emp_id),
    project_id INTEGER REFERENCES projects(project_id),
    role       VARCHAR(50),
    hours      INTEGER,
    PRIMARY KEY (emp_id, project_id)
);
```

---

### 1.1 INNER JOIN

Returns only rows where the join predicate matches in **both** tables.

$$
R \bowtie_\theta S = \sigma_\theta(R \times S)
$$

```sql
-- All employees with their department names (only those WITH a department)
SELECT e.name, e.salary, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```

**Execution plan intuition:** The optimizer chooses between:
- **Nested Loop:** For each row in the outer table, scan the inner table. Best when inner table is small or has an index on the join column. Cost: $O(m \cdot n)$ worst case, $O(m \cdot \log n)$ with index.
- **Hash Join:** Build a hash table on the smaller relation, probe with the larger. Best for large unsorted tables without indexes. Cost: $O(m + n)$.
- **Merge Join:** Both inputs sorted on join key, merge like merge-sort. Best when both are pre-sorted (e.g., index scan). Cost: $O(m + n)$ after sorting.

```sql
-- See what the optimizer chose:
EXPLAIN ANALYZE
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```

---

### 1.2 LEFT (OUTER) JOIN

Returns **all rows from the left table**, plus matching rows from the right. Non-matching right-side columns are NULL.

```sql
-- All employees, including those without a department
SELECT e.name, e.salary, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
```

**Use case — finding unmatched rows:**

```sql
-- Employees NOT assigned to any project (anti-join pattern)
SELECT e.name
FROM employees e
LEFT JOIN assignments a ON e.emp_id = a.emp_id
WHERE a.emp_id IS NULL;
```

This "LEFT JOIN + IS NULL" pattern is an **anti-join** — equivalent to `NOT EXISTS` but sometimes preferred by optimizers.

---

### 1.3 RIGHT (OUTER) JOIN

Returns **all rows from the right table**, plus matching rows from the left. Logically equivalent to swapping table order and using LEFT JOIN.

```sql
-- All departments, including those with no employees
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

-- Equivalent (and more common in practice):
SELECT e.name, d.dept_name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id;
```

**Convention:** Most teams standardize on LEFT JOIN and reorder tables rather than using RIGHT JOIN. It reads more naturally (primary table first).

---

### 1.4 FULL OUTER JOIN

Returns **all rows from both tables**. Unmatched rows on either side get NULLs.

```sql
-- Show all employees and all departments, including unmatched on both sides
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;
```

**Use case — data reconciliation:**

```sql
-- Find discrepancies between two data sources
SELECT
    COALESCE(a.id, b.id) AS record_id,
    a.value AS source_a_value,
    b.value AS source_b_value,
    CASE
        WHEN a.id IS NULL THEN 'Missing in A'
        WHEN b.id IS NULL THEN 'Missing in B'
        WHEN a.value <> b.value THEN 'Value mismatch'
        ELSE 'Match'
    END AS status
FROM source_a a
FULL OUTER JOIN source_b b ON a.id = b.id
WHERE a.id IS NULL OR b.id IS NULL OR a.value <> b.value;
```

**Note:** MySQL does not support FULL OUTER JOIN directly. Emulate with UNION of LEFT and RIGHT joins.

---

### 1.5 CROSS JOIN

The Cartesian product — every row from the left combined with every row from the right.

$$
|R \times S| = |R| \cdot |S|
$$

```sql
-- Generate all possible employee-project combinations
SELECT e.name, p.title
FROM employees e
CROSS JOIN projects p;

-- Practical use: generate a calendar grid
SELECT d.date, h.hour
FROM generate_series('2026-01-01'::date, '2026-12-31'::date, '1 day') AS d(date)
CROSS JOIN generate_series(0, 23) AS h(hour);
```

**Warning:** Cross joins on large tables are catastrophic. 10,000 × 10,000 = 100,000,000 rows.

---

### 1.6 LATERAL JOIN (PostgreSQL, MySQL 8.0+)

`LATERAL` allows the right-hand subquery to reference columns from the left-hand table — like a correlated subquery in the FROM clause.

```sql
-- For each department, get the top 3 highest-paid employees
SELECT d.dept_name, top_emp.name, top_emp.salary
FROM departments d
CROSS JOIN LATERAL (
    SELECT e.name, e.salary
    FROM employees e
    WHERE e.dept_id = d.dept_id
    ORDER BY e.salary DESC
    LIMIT 3
) AS top_emp;
```

Without LATERAL, you'd need window functions or correlated subqueries. LATERAL is the cleanest solution for "top-N per group" problems.

**Execution plan:** LATERAL is typically executed as a nested loop — for each row on the left, evaluate the lateral subquery. The optimizer may rewrite it if possible.

```sql
-- Another LATERAL use: unnesting JSON arrays (PostgreSQL)
SELECT o.order_id, item.*
FROM orders o
CROSS JOIN LATERAL jsonb_array_elements(o.items) AS item;
```

---

### 1.7 Self-Join

Joining a table to itself — essential for hierarchical data and comparisons within the same table.

```sql
-- Find each employee's manager name
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;

-- Find employees who earn more than their manager
SELECT e.name, e.salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
INNER JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```

---

### 1.8 Multi-Table Joins

Real queries often join 3+ tables. The optimizer determines join order.

```sql
-- Employee names, their department, and projects they're assigned to
SELECT
    e.name,
    d.dept_name,
    p.title AS project,
    a.role,
    a.hours
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
INNER JOIN assignments a ON e.emp_id = a.emp_id
INNER JOIN projects p ON a.project_id = p.project_id
WHERE p.budget > 100000
ORDER BY d.dept_name, e.name;
```

**Join order matters for performance** but not correctness (for inner joins). The optimizer explores different orderings. For outer joins, order **does** affect semantics — be explicit.

---

## 📚 2. Subqueries

### 2.1 Scalar Subqueries

Return exactly one value (one row, one column). Can appear in SELECT, WHERE, or HAVING.

```sql
-- Each employee's salary compared to company average
SELECT
    name,
    salary,
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

**Danger:** If a scalar subquery returns more than one row, you get a runtime error.

### 2.2 Table Subqueries (Derived Tables)

Return a result set used as a virtual table in FROM.

```sql
-- Average salary by department, then find departments above the global average
SELECT sub.dept_name, sub.avg_salary
FROM (
    SELECT d.dept_name, AVG(e.salary) AS avg_salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
    GROUP BY d.dept_name
) sub
WHERE sub.avg_salary > (SELECT AVG(salary) FROM employees);
```

### 2.3 Correlated Subqueries

Reference the outer query — re-evaluated for each outer row.

```sql
-- Employees earning above their department's average
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e.dept_id  -- correlation: references outer e
);
```

**Performance note:** Correlated subqueries can be expensive ($O(n \cdot m)$). The optimizer may decorrelate them into joins internally.

### 2.4 EXISTS and NOT EXISTS

Test for the existence of rows. More NULL-safe than IN/NOT IN.

```sql
-- Departments that have at least one employee earning > 100k
SELECT d.dept_name
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.dept_id = d.dept_id AND e.salary > 100000
);

-- Departments with NO employees (anti-semi-join)
SELECT d.dept_name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id
);
```

**EXISTS vs IN:**
- `EXISTS` stops at the first match (short-circuits) — efficient for large subqueries
- `IN` materializes the full subquery result — can be faster for small result sets
- `NOT IN` is dangerous with NULLs (returns empty if any NULL in subquery); `NOT EXISTS` handles NULLs correctly

### 2.5 IN, ANY, ALL

```sql
-- Employees in departments 1, 3, or 5
SELECT name FROM employees WHERE dept_id IN (1, 3, 5);

-- Employees earning more than ANY employee in dept 2
SELECT name, salary FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE dept_id = 2);

-- Employees earning more than ALL employees in dept 2
SELECT name, salary FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id = 2);
```

---

## 📚 3. Common Table Expressions (CTEs)

### 3.1 Basic CTEs

CTEs provide named, reusable subqueries that improve readability.

```sql
WITH dept_stats AS (
    SELECT
        dept_id,
        AVG(salary) AS avg_salary,
        COUNT(*) AS headcount
    FROM employees
    GROUP BY dept_id
)
SELECT
    e.name,
    e.salary,
    ds.avg_salary AS dept_avg,
    e.salary - ds.avg_salary AS diff
FROM employees e
JOIN dept_stats ds ON e.dept_id = ds.dept_id
WHERE e.salary > ds.avg_salary
ORDER BY diff DESC;
```

### 3.2 Multiple CTEs

Chain CTEs for step-by-step logic:

```sql
WITH
high_earners AS (
    SELECT emp_id, name, salary, dept_id
    FROM employees
    WHERE salary > 100000
),
dept_high_count AS (
    SELECT dept_id, COUNT(*) AS high_earner_count
    FROM high_earners
    GROUP BY dept_id
)
SELECT d.dept_name, dhc.high_earner_count
FROM dept_high_count dhc
JOIN departments d ON dhc.dept_id = d.dept_id
ORDER BY dhc.high_earner_count DESC;
```

### 3.3 CTE Materialization

**PostgreSQL behavior (pre-12):** CTEs were always materialized (computed once, stored in temp). This could be a performance barrier — the optimizer couldn't push predicates into the CTE.

**PostgreSQL 12+:** CTEs are inlined by default if referenced once and not recursive. Use `MATERIALIZED` / `NOT MATERIALIZED` to control:

```sql
-- Force materialization (useful if CTE is referenced multiple times):
WITH expensive_calc AS MATERIALIZED (
    SELECT dept_id, complex_function(salary) AS result
    FROM employees
)
SELECT * FROM expensive_calc WHERE dept_id = 5;

-- Force inlining (let optimizer push predicates in):
WITH simple_filter AS NOT MATERIALIZED (
    SELECT * FROM employees WHERE active = true
)
SELECT * FROM simple_filter WHERE dept_id = 5;
```

### 3.4 CTEs vs. Subqueries vs. Views vs. Temp Tables

| Feature | CTE | Subquery | View | Temp Table |
|---------|-----|----------|------|------------|
| Scope | Single query | Single query | Session/permanent | Session |
| Reusable in query | Yes (by name) | No | Yes | Yes |
| Optimizer can inline | Yes (PG 12+) | Yes | Yes | No |
| Can be recursive | Yes | No | No | No |
| Persists data | No* | No | No | Yes |
| Indexes | No | No | On base tables | Yes |

*Unless `MATERIALIZED` is specified.

---

## 📚 4. Advanced Join Patterns

### 4.1 Anti-Join (Find Non-Matches)

Three equivalent patterns — performance varies by engine:

```sql
-- Pattern 1: LEFT JOIN + IS NULL (often fastest in PostgreSQL)
SELECT e.name
FROM employees e
LEFT JOIN assignments a ON e.emp_id = a.emp_id
WHERE a.emp_id IS NULL;

-- Pattern 2: NOT EXISTS (NULL-safe, often fastest in MySQL)
SELECT e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM assignments a WHERE a.emp_id = e.emp_id
);

-- Pattern 3: NOT IN (dangerous with NULLs!)
SELECT name
FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM assignments WHERE emp_id IS NOT NULL);
```

### 4.2 Semi-Join (Existence Check Without Duplication)

```sql
-- Departments that have employees (no duplicate dept rows)
-- Semi-join via EXISTS:
SELECT d.dept_name
FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id);

-- Semi-join via IN:
SELECT dept_name
FROM departments
WHERE dept_id IN (SELECT dept_id FROM employees);

-- NOT a semi-join (may duplicate departments if multiple employees):
SELECT DISTINCT d.dept_name
FROM departments d
INNER JOIN employees e ON d.dept_id = e.dept_id;
```

### 4.3 Inequality Joins (Range Joins)

```sql
-- Find salary bands for each employee
SELECT e.name, e.salary, b.band_name
FROM employees e
INNER JOIN salary_bands b
    ON e.salary >= b.min_salary
   AND e.salary < b.max_salary;

-- Find overlapping date ranges
SELECT a.event_name, b.event_name
FROM events a
INNER JOIN events b
    ON a.event_id < b.event_id  -- avoid self-match and duplicates
   AND a.start_date < b.end_date
   AND b.start_date < a.end_date;
```

### 4.4 The "Top-N Per Group" Pattern

```sql
-- Top 3 earners per department using LATERAL:
SELECT d.dept_name, t.name, t.salary
FROM departments d
CROSS JOIN LATERAL (
    SELECT e.name, e.salary
    FROM employees e
    WHERE e.dept_id = d.dept_id
    ORDER BY e.salary DESC
    LIMIT 3
) t;

-- Alternative using window functions (covered in 14.3):
WITH ranked AS (
    SELECT
        name, salary, dept_id,
        ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT name, salary, dept_id
FROM ranked
WHERE rn <= 3;
```

---

## 📚 5. Execution Plan Reading

### Understanding EXPLAIN Output

```sql
EXPLAIN ANALYZE
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > 80000;
```

Key nodes to understand:

| Node | Meaning |
|------|---------|
| `Seq Scan` | Full table scan (reads every row) |
| `Index Scan` | Uses an index to find specific rows |
| `Index Only Scan` | Answers query entirely from index (covering index) |
| `Bitmap Index Scan` | Builds a bitmap of matching pages, then fetches |
| `Nested Loop` | For each outer row, scan inner |
| `Hash Join` | Build hash table on inner, probe with outer |
| `Merge Join` | Merge two sorted inputs |
| `Sort` | Sorts input (for ORDER BY or Merge Join) |
| `Aggregate` | Computes aggregates (SUM, COUNT, etc.) |

**Reading costs:** `(startup_cost..total_cost)` in arbitrary units. `actual time` in milliseconds. `rows` = estimated vs actual row count.

```
Hash Join  (cost=3.25..8.50 rows=100 width=64) (actual time=0.05..0.12 rows=95 loops=1)
  Hash Cond: (e.dept_id = d.dept_id)
  -> Seq Scan on employees e  (cost=0.00..4.50 rows=50 width=48) (actual time=0.01..0.03 rows=47 loops=1)
        Filter: (salary > 80000)
        Rows Removed by Filter: 53
  -> Hash  (cost=2.00..2.00 rows=10 width=20) (actual time=0.02..0.02 rows=10 loops=1)
        -> Seq Scan on departments d  (cost=0.00..2.00 rows=10 width=20)
```

**Interpretation:** The optimizer chose a Hash Join. It first scanned employees with a filter (salary > 80000), removing 53 rows. Then it built a hash table on the 10 department rows and probed it with the 47 filtered employee rows.

---

## 🧪 6. Worked Examples

### Example 14.2.1 — Multi-Level Hierarchy

```sql
-- Find the full management chain for employee 'Alice'
-- (Recursive CTE — preview of Chapter 14.7)
WITH RECURSIVE chain AS (
    -- Base case: start with Alice
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees
    WHERE name = 'Alice'

    UNION ALL

    -- Recursive case: find each manager's manager
    SELECT e.emp_id, e.name, e.manager_id, c.level + 1
    FROM employees e
    INNER JOIN chain c ON e.emp_id = c.manager_id
)
SELECT level, name FROM chain ORDER BY level;
```

### Example 14.2.2 — Data Pipeline: Joining Fact and Dimension Tables

```sql
-- Star schema query: total sales by product category and quarter
WITH quarterly_sales AS (
    SELECT
        f.product_id,
        d.quarter,
        SUM(f.amount) AS total_amount
    FROM fact_sales f
    INNER JOIN dim_date d ON f.date_id = d.date_id
    WHERE d.year = 2025
    GROUP BY f.product_id, d.quarter
)
SELECT
    p.category,
    qs.quarter,
    qs.total_amount
FROM quarterly_sales qs
INNER JOIN dim_product p ON qs.product_id = p.product_id
ORDER BY p.category, qs.quarter;
```

### Example 14.2.3 — Gap Analysis with FULL OUTER JOIN

```sql
-- Compare expected vs actual inventory
SELECT
    COALESCE(e.sku, a.sku) AS sku,
    e.expected_qty,
    a.actual_qty,
    COALESCE(a.actual_qty, 0) - COALESCE(e.expected_qty, 0) AS variance
FROM expected_inventory e
FULL OUTER JOIN actual_inventory a ON e.sku = a.sku
WHERE e.expected_qty IS DISTINCT FROM a.actual_qty
ORDER BY ABS(COALESCE(a.actual_qty, 0) - COALESCE(e.expected_qty, 0)) DESC;
```

---

## 🧪 7. Common Pitfalls & Fixes

### Pitfall 1: Fan-Out (Unintended Row Multiplication)

```sql
-- If an employee has 3 assignments, joining employees to assignments
-- triples that employee's rows. Aggregating without awareness gives wrong results.

-- WRONG: salary counted multiple times
SELECT d.dept_name, SUM(e.salary) AS total_salary
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
JOIN assignments a ON e.emp_id = a.emp_id
GROUP BY d.dept_name;

-- CORRECT: aggregate before joining, or use DISTINCT
SELECT d.dept_name, SUM(DISTINCT e.salary) AS total_salary  -- if salaries unique
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
JOIN assignments a ON e.emp_id = a.emp_id
GROUP BY d.dept_name;

-- BETTER: aggregate in a subquery to avoid fan-out entirely
SELECT d.dept_name, dept_totals.total_salary
FROM departments d
JOIN (
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
) dept_totals ON d.dept_id = dept_totals.dept_id;
```

### Pitfall 2: Outer Join + WHERE Filtering

```sql
-- WRONG: WHERE on the right table converts LEFT JOIN to INNER JOIN
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Engineering';  -- Filters out NULLs!

-- CORRECT: put the filter in the ON clause
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id AND d.dept_name = 'Engineering';
```

### Pitfall 3: Joining on Nullable Columns

```sql
-- NULL = NULL is UNKNOWN, not TRUE. Rows with NULL join keys never match.
-- If you need NULLs to match, use IS NOT DISTINCT FROM (PostgreSQL):
SELECT *
FROM table_a a
JOIN table_b b ON a.key IS NOT DISTINCT FROM b.key;
```

---

## 🏋️ 8. Exercises

1. Write a query to find all employees who are assigned to more than 2 projects.
2. Using a LATERAL join, find the most recent hire in each department.
3. Write an anti-join to find projects with no assigned employees.
4. Rewrite a correlated subquery as a JOIN (and vice versa).
5. Read an EXPLAIN ANALYZE output and identify whether the optimizer chose nested loop, hash join, or merge join. Explain why.

---

## 🔗 Cross-References

- **Previous:** [14.1 - Relational Theory & Set Logic](14.1---Relational-Theory-&-Set-Logic) — the algebra behind joins
- **Next:** [14.3 - Aggregations & Window Functions](14.3---Aggregations-&-Window-Functions) — analytics on joined data
- **Performance:** [14.5 - Indexes & Query Performance](14.5---Indexes-&-Query-Performance) — making joins fast
- **Practice:** Run `python _practice/scripts/7.2_joins.py --count 20` for drill problems

---

## 📖 Key Sources

- PostgreSQL JOIN documentation: https://www.postgresql.org/docs/current/queries-table-expressions.html
- Use The Index, Luke — Join chapter: https://use-the-index-luke.com/sql/join
- Pavlo, A. CMU 15-445 Lecture 11: Join Algorithms



---

## 📚 12. Deep Dive — LATERAL Joins, Recursive CTEs & PIVOT/UNPIVOT

### 12.1 LATERAL Joins — Correlated Subqueries in FROM

`LATERAL` allows a subquery in the `FROM` clause to reference columns from preceding tables — essentially a correlated subquery that returns a set of rows.

**Syntax:**

```sql
SELECT ...
FROM table_a a
CROSS JOIN LATERAL (
    SELECT ... FROM table_b b WHERE b.key = a.key  -- references 'a'
    LIMIT N
) sub;
```

Without `LATERAL`, subqueries in `FROM` cannot reference other `FROM` items. `LATERAL` lifts this restriction.

**Pattern 1: Top-N Per Group (Most Efficient)**

```sql
-- Top 3 highest-paid employees per department
-- This is MORE EFFICIENT than window functions for small N
-- because it can use an index on (dept_id, salary DESC)
SELECT d.dept_name, e.name, e.salary
FROM departments d
CROSS JOIN LATERAL (
    SELECT emp.name, emp.salary
    FROM employees emp
    WHERE emp.dept_id = d.dept_id
    ORDER BY emp.salary DESC
    LIMIT 3
) e;
```

**Why LATERAL beats window functions here:**
- Window function approach: scans ALL employees, computes ROW_NUMBER for ALL, then filters
- LATERAL approach: for each department, uses index to grab only top 3 — stops early

**Pattern 2: Latest Record Per Entity**

```sql
-- Most recent order for each customer
SELECT c.customer_id, c.name, latest.order_id, latest.order_date, latest.total
FROM customers c
CROSS JOIN LATERAL (
    SELECT o.order_id, o.order_date, o.total
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    LIMIT 1
) latest;
-- Note: customers with NO orders are excluded (CROSS JOIN).
-- Use LEFT JOIN LATERAL ... ON true to include them with NULLs.
```

**Pattern 3: Expanding JSON Arrays**

```sql
-- Each row has a JSONB array; expand into rows
SELECT
    p.product_id,
    p.name,
    tag.value AS tag
FROM products p
CROSS JOIN LATERAL jsonb_array_elements_text(p.tags) AS tag(value);
```

**Pattern 4: Running Calculations with Lookups**

```sql
-- For each sale, find the exchange rate valid at that date
SELECT
    s.sale_id,
    s.amount_local,
    s.sale_date,
    rate.rate,
    s.amount_local * rate.rate AS amount_usd
FROM sales s
CROSS JOIN LATERAL (
    SELECT r.rate
    FROM exchange_rates r
    WHERE r.currency = s.currency
      AND r.effective_date <= s.sale_date
    ORDER BY r.effective_date DESC
    LIMIT 1
) rate;
```

### 12.2 Recursive CTEs — Hierarchies, Graphs & Series Generation

Recursive CTEs have two parts: the **anchor** (base case) and the **recursive member**, connected by `UNION ALL`.

**Execution model:**
1. Execute anchor → working table (WT)
2. Execute recursive member using WT as input → intermediate table (IT)
3. Replace WT with IT
4. Repeat until IT is empty
5. Final result = UNION ALL of all intermediate results

**Pattern 1: Organizational Hierarchy with Depth & Path**

```sql
WITH RECURSIVE org_tree AS (
    -- Anchor: CEO (no manager)
    SELECT
        emp_id,
        name,
        manager_id,
        1 AS depth,
        ARRAY[name] AS path,
        name AS path_string
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: each employee's direct reports
    SELECT
        e.emp_id,
        e.name,
        e.manager_id,
        t.depth + 1,
        t.path || e.name,
        t.path_string || ' → ' || e.name
    FROM employees e
    INNER JOIN org_tree t ON e.manager_id = t.emp_id
)
SELECT depth, path_string, name
FROM org_tree
ORDER BY path;  -- alphabetical tree ordering
```

**Pattern 2: Bill of Materials (BOM) — Exploding Components**

```sql
WITH RECURSIVE bom AS (
    -- Anchor: top-level product
    SELECT
        component_id,
        component_name,
        quantity,
        1 AS level,
        ARRAY[component_id] AS visited  -- cycle detection
    FROM product_components
    WHERE parent_id IS NULL AND product_id = 100

    UNION ALL

    SELECT
        pc.component_id,
        pc.component_name,
        pc.quantity * bom.quantity AS total_quantity,  -- multiply through
        bom.level + 1,
        bom.visited || pc.component_id
    FROM product_components pc
    INNER JOIN bom ON pc.parent_id = bom.component_id
    WHERE pc.component_id != ALL(bom.visited)  -- prevent cycles
)
SELECT level, component_name, total_quantity
FROM bom
ORDER BY level, component_name;
```

**Pattern 3: Graph Shortest Path (BFS)**

```sql
-- Find shortest path between nodes in an unweighted graph
WITH RECURSIVE paths AS (
    SELECT
        target_node AS current,
        ARRAY[source_node, target_node] AS path,
        1 AS hops
    FROM edges
    WHERE source_node = 'A'

    UNION ALL

    SELECT
        e.target_node,
        p.path || e.target_node,
        p.hops + 1
    FROM edges e
    INNER JOIN paths p ON e.source_node = p.current
    WHERE e.target_node != ALL(p.path)  -- no revisiting
      AND p.hops < 10  -- safety limit
)
SELECT path, hops
FROM paths
WHERE current = 'Z'
ORDER BY hops
LIMIT 1;
```

**Pattern 4: Date/Number Series Generation**

```sql
-- Generate a calendar table (useful for LEFT JOINing sparse data)
WITH RECURSIVE calendar AS (
    SELECT DATE '2025-01-01' AS dt
    UNION ALL
    SELECT dt + INTERVAL '1 day'
    FROM calendar
    WHERE dt < '2025-12-31'
)
SELECT dt::date AS calendar_date
FROM calendar;

-- PostgreSQL native (faster):
SELECT generate_series('2025-01-01'::date, '2025-12-31'::date, '1 day') AS dt;
```

**Cycle detection strategies:**

| Strategy | Mechanism | Overhead |
|----------|-----------|----------|
| Path array + `!= ALL(path)` | Track visited nodes in array | O(path_length) per row |
| `CYCLE` clause (SQL:2023) | Built-in cycle detection | Engine-optimized |
| Depth limit (`WHERE depth < N`) | Hard cutoff | Minimal |
| Hash set in application | Process results in app code | Zero SQL overhead |

```sql
-- SQL:2023 CYCLE clause (PostgreSQL 14+):
WITH RECURSIVE traversal AS (
    SELECT emp_id, manager_id, name FROM employees WHERE emp_id = 1
    UNION ALL
    SELECT e.emp_id, e.manager_id, e.name
    FROM employees e JOIN traversal t ON e.manager_id = t.emp_id
)
CYCLE emp_id SET is_cycle USING path_array
SELECT * FROM traversal WHERE NOT is_cycle;
```

### 12.3 PIVOT and UNPIVOT

**PIVOT** transforms rows into columns (long → wide). **UNPIVOT** does the reverse (wide → long).

**PostgreSQL — PIVOT via CASE/FILTER (no native PIVOT keyword):**

```sql
-- Monthly revenue by product (rows → columns)
SELECT
    product_id,
    SUM(amount) FILTER (WHERE month = 1) AS jan,
    SUM(amount) FILTER (WHERE month = 2) AS feb,
    SUM(amount) FILTER (WHERE month = 3) AS mar,
    SUM(amount) FILTER (WHERE month = 4) AS apr,
    SUM(amount) FILTER (WHERE month = 5) AS may,
    SUM(amount) FILTER (WHERE month = 6) AS jun,
    SUM(amount) FILTER (WHERE month = 7) AS jul,
    SUM(amount) FILTER (WHERE month = 8) AS aug,
    SUM(amount) FILTER (WHERE month = 9) AS sep,
    SUM(amount) FILTER (WHERE month = 10) AS oct,
    SUM(amount) FILTER (WHERE month = 11) AS nov,
    SUM(amount) FILTER (WHERE month = 12) AS dec
FROM (
    SELECT product_id, EXTRACT(MONTH FROM sale_date)::int AS month, amount
    FROM sales
    WHERE sale_date >= '2025-01-01' AND sale_date < '2026-01-01'
) sub
GROUP BY product_id;
```

**PostgreSQL — Dynamic PIVOT with crosstab (tablefunc extension):**

```sql
-- Enable the extension:
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Static crosstab:
SELECT * FROM crosstab(
    'SELECT product_id, month, total_amount
     FROM monthly_sales
     ORDER BY 1, 2',
    'SELECT generate_series(1, 12)'
) AS ct(
    product_id INT,
    jan NUMERIC, feb NUMERIC, mar NUMERIC, apr NUMERIC,
    may NUMERIC, jun NUMERIC, jul NUMERIC, aug NUMERIC,
    sep NUMERIC, oct NUMERIC, nov NUMERIC, dec NUMERIC
);
```

**SQL Server — Native PIVOT:**

```sql
-- SQL Server PIVOT syntax:
SELECT product_id, [1] AS jan, [2] AS feb, [3] AS mar, [4] AS apr
FROM (
    SELECT product_id, MONTH(sale_date) AS sale_month, amount
    FROM sales
    WHERE YEAR(sale_date) = 2025
) src
PIVOT (
    SUM(amount) FOR sale_month IN ([1], [2], [3], [4], [5], [6],
                                    [7], [8], [9], [10], [11], [12])
) pvt;
```

**UNPIVOT — Wide to Long:**

```sql
-- PostgreSQL: UNPIVOT via UNION ALL or VALUES + LATERAL
SELECT product_id, month_name, revenue
FROM monthly_wide
CROSS JOIN LATERAL (
    VALUES
        ('jan', jan), ('feb', feb), ('mar', mar),
        ('apr', apr), ('may', may), ('jun', jun),
        ('jul', jul), ('aug', aug), ('sep', sep),
        ('oct', oct), ('nov', nov), ('dec', dec)
) AS unpivoted(month_name, revenue)
WHERE revenue IS NOT NULL;

-- SQL Server native UNPIVOT:
SELECT product_id, month_name, revenue
FROM monthly_wide
UNPIVOT (
    revenue FOR month_name IN (jan, feb, mar, apr, may, jun,
                                jul, aug, sep, oct, nov, dec)
) unpvt;
```

---

## 📚 13. Appendix — Query Plan Reading & Cost-Based Optimizer Fundamentals

### 13.1 The Query Processing Pipeline

Every SQL query passes through these stages:

1. **Parser** → Abstract Syntax Tree (AST)
2. **Analyzer/Binder** → Resolves names, checks types, produces query tree
3. **Rewriter** → Applies rules (view expansion, security policies)
4. **Optimizer** → Generates candidate plans, estimates costs, picks cheapest
5. **Executor** → Runs the chosen physical plan

### 13.2 EXPLAIN ANALYZE Deep Dive (PostgreSQL)

```sql
EXPLAIN (ANALYZE, BUFFERS, TIMING, FORMAT TEXT)
SELECT
    d.dept_name,
    COUNT(*) AS emp_count,
    AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
WHERE e.hire_date > '2020-01-01'
  AND e.salary > 50000
GROUP BY d.dept_name
HAVING COUNT(*) > 3
ORDER BY avg_salary DESC;
```

**Output anatomy:**

```
Sort  (cost=156.23..156.48 rows=10 width=48) (actual time=2.15..2.16 rows=5 loops=1)
  Sort Key: (avg(e.salary)) DESC
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=45 read=3
  ->  HashAggregate  (cost=155.00..155.75 rows=10 width=48) (actual time=2.10..2.12 rows=5 loops=1)
        Group Key: d.dept_name
        Filter: (count(*) > 3)
        Rows Removed by Filter: 3
        Batches: 1  Memory Usage: 40kB
        ->  Hash Join  (cost=3.25..150.00 rows=500 width=20) (actual time=0.08..1.80 rows=480 loops=1)
              Hash Cond: (e.dept_id = d.dept_id)
              ->  Bitmap Heap Scan on employees e  (cost=4.50..140.00 rows=500 width=12) (actual time=0.05..1.50 rows=480 loops=1)
                    Recheck Cond: (hire_date > '2020-01-01')
                    Filter: (salary > 50000)
                    Rows Removed by Filter: 120
                    Heap Blocks: exact=30
                    ->  Bitmap Index Scan on idx_emp_hire_date  (cost=0.00..4.37 rows=600 width=0) (actual time=0.03..0.03 rows=600 loops=1)
                          Index Cond: (hire_date > '2020-01-01')
              ->  Hash  (cost=2.00..2.00 rows=10 width=12) (actual time=0.02..0.02 rows=10 loops=1)
                    Buckets: 1024  Batches: 1  Memory Usage: 9kB
                    ->  Seq Scan on departments d  (cost=0.00..2.00 rows=10 width=12) (actual time=0.01..0.01 rows=10 loops=1)
Planning Time: 0.25 ms
Execution Time: 2.30 ms
```

**Key metrics to examine:**

| Metric | Meaning | Red Flag |
|--------|---------|----------|
| `actual time` | Wall-clock ms (startup..total) | Large gap between estimated and actual rows |
| `rows` | Estimated vs actual row count | Off by 10x+ → stale statistics |
| `Buffers: shared hit` | Pages found in cache | Low hit ratio → insufficient shared_buffers |
| `Buffers: shared read` | Pages read from disk | High reads → cold cache or table too large for RAM |
| `loops` | Times this node executed | High loops in nested loop → consider hash join |
| `Rows Removed by Filter` | Rows that passed index but failed filter | High count → index not selective enough |

### 13.3 Cost Model Fundamentals

PostgreSQL's cost model uses these configurable constants:

```sql
-- View current cost settings:
SHOW seq_page_cost;        -- 1.0 (baseline: cost of reading one page sequentially)
SHOW random_page_cost;     -- 4.0 (random I/O is ~4x more expensive)
SHOW cpu_tuple_cost;       -- 0.01 (processing one row)
SHOW cpu_index_tuple_cost; -- 0.005 (processing one index entry)
SHOW cpu_operator_cost;    -- 0.0025 (evaluating one operator/function)
SHOW effective_cache_size; -- 4GB (how much of the table is likely cached)
```

**Total cost formula (simplified):**

$$
\text{Cost} = (\text{pages\_read} \times \text{page\_cost}) + (\text{rows\_processed} \times \text{cpu\_tuple\_cost}) + (\text{operators\_evaluated} \times \text{cpu\_operator\_cost})
$$

**Sequential scan cost:**

$$
\text{Cost}_{\text{seq}} = N_{\text{pages}} \times \text{seq\_page\_cost} + N_{\text{rows}} \times \text{cpu\_tuple\_cost}
$$

**Index scan cost:**

$$
\text{Cost}_{\text{idx}} = N_{\text{index\_pages}} \times \text{random\_page\_cost} + N_{\text{matching\_rows}} \times (\text{cpu\_index\_tuple\_cost} + \text{random\_page\_cost} \times \text{correlation\_factor})
$$

**When does the optimizer choose Seq Scan over Index Scan?**

If the query returns more than ~5-15% of the table, sequential scan wins because:
- Sequential I/O is 4x cheaper than random I/O (on spinning disks)
- Index scan requires reading the index AND the heap pages (double I/O)
- For SSDs, `random_page_cost` should be lowered to ~1.1-1.5

```sql
-- Tune for SSD:
SET random_page_cost = 1.1;
-- Now the optimizer will prefer index scans more aggressively
```

### 13.4 Join Algorithm Selection

The optimizer chooses between three join algorithms:

**Nested Loop Join:**
- Best for: small outer table, indexed inner table
- Cost: $O(N \times M)$ worst case, $O(N \times \log M)$ with index
- Chosen when: inner side has < ~1000 rows or good index exists

```sql
-- Forces nested loop (for testing):
SET enable_hashjoin = off;
SET enable_mergejoin = off;
```

**Hash Join:**
- Best for: medium-to-large tables, equality joins, no useful index
- Cost: $O(N + M)$ — build hash on smaller table, probe with larger
- Memory: requires `work_mem` to hold the hash table
- Chosen when: equality condition, tables too large for nested loop

**Merge Join:**
- Best for: large pre-sorted inputs, inequality joins
- Cost: $O(N \log N + M \log M)$ if sorting needed, $O(N + M)$ if pre-sorted
- Chosen when: inputs already sorted (from index) or ORDER BY matches join

### 13.5 Statistics and Cardinality Estimation

The optimizer relies on table statistics to estimate row counts:

```sql
-- View statistics for a column:
SELECT
    attname,
    n_distinct,       -- estimated distinct values (-1 = unique)
    most_common_vals, -- most frequent values
    most_common_freqs,-- their frequencies
    histogram_bounds  -- equi-depth histogram boundaries
FROM pg_stats
WHERE tablename = 'employees' AND attname = 'dept_id';

-- Force statistics refresh:
ANALYZE employees;

-- Increase statistics target for better estimates on skewed columns:
ALTER TABLE employees ALTER COLUMN dept_id SET STATISTICS 1000;
ANALYZE employees;
```

**When estimates go wrong:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Nested loop on large table | Underestimated rows | `ANALYZE`; increase `default_statistics_target` |
| Hash join spills to disk | Underestimated hash table size | Increase `work_mem` |
| Seq scan when index exists | Overestimated selectivity | Check correlation; update statistics |
| Plan changes after data load | Stale statistics | Run `ANALYZE` after bulk loads |

### 13.6 Common EXPLAIN Patterns and Fixes

**Pattern: Sort + Limit (Top-N)**

```sql
-- Slow: sorts entire table then takes 10
EXPLAIN SELECT * FROM events ORDER BY created_at DESC LIMIT 10;
-- Fix: create index
CREATE INDEX idx_events_created ON events(created_at DESC);
-- Now: Index Scan Backward, stops after 10 rows
```

**Pattern: Bitmap Heap Scan with high "Rows Removed by Filter"**

```sql
-- The index finds 10000 rows but the filter removes 9500
-- → The index is not selective enough for this query
-- Fix: create a composite index or partial index
CREATE INDEX idx_emp_active_dept ON employees(dept_id) WHERE active = true;
```

**Pattern: HashAggregate with "Batches > 1"**

```sql
-- Hash table exceeded work_mem and spilled to disk
-- Fix: increase work_mem for this query
SET work_mem = '256MB';
-- Or redesign: pre-aggregate in a materialized view
```

### 13.7 Forcing Plan Choices (Last Resort)

```sql
-- PostgreSQL: pg_hint_plan extension
/*+ SeqScan(employees) HashJoin(employees departments) */
SELECT ...;

-- PostgreSQL: disable specific strategies
SET enable_seqscan = off;      -- force index usage (debugging only!)
SET enable_hashjoin = off;     -- force nested loop or merge
SET enable_nestloop = off;     -- force hash or merge

-- MySQL: query hints
SELECT /*+ INDEX(e idx_emp_dept) */ e.name FROM employees e WHERE e.dept_id = 5;

-- ALWAYS reset after debugging:
RESET enable_seqscan;
RESET enable_hashjoin;
RESET enable_nestloop;
```

**Warning:** Forcing plans is almost always wrong in production. If the optimizer makes a bad choice, fix the root cause (stale stats, missing index, bad `random_page_cost` setting).

---

## 📖 Additional Sources (Sections 12–13)

- PostgreSQL LATERAL: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-LATERAL
- PostgreSQL Recursive Queries: https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE
- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- Pavlo, A. CMU 15-445 Lectures 12-14: Query Optimization
- Selinger, P.G. et al. (1979). "Access Path Selection in a Relational Database Management System." *ACM SIGMOD*.

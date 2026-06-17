---
date: 2026-01-24
title: SQL Essentials for Coding Tests
mission: Master database queries, joins, aggregations, subqueries, and SQL patterns for technical interviews
status: reference
tags: [sql, database, queries, joins, aggregations, coding-tests]
type: learning-note
---

# SQL Essentials for Coding Tests

**Database Queries for Interviews**

---

## 1. Basic SELECT Queries

### Simple SELECT
```sql
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT name, email, age FROM users;

-- Select with alias (rename column)
SELECT name AS user_name, email AS contact_email
FROM users;

-- Select with calculation
SELECT name, salary, salary * 0.1 AS bonus
FROM employees;

-- DISTINCT (unique values only)
SELECT DISTINCT city FROM users;
SELECT DISTINCT age, city FROM users;  -- Unique combinations

-- LIMIT (restrict number of results)
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- Skip first 20, get next 10
```

---

## 2. WHERE Clause (Filtering)

### Comparison Operators
```sql
-- Equal
SELECT * FROM users WHERE age = 25;
SELECT * FROM users WHERE city = 'NYC';

-- Not equal
SELECT * FROM users WHERE age != 25;
SELECT * FROM users WHERE age <> 25;  -- Same as !=

-- Greater/Less than
SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE age >= 25;
SELECT * FROM users WHERE age < 25;
SELECT * FROM users WHERE age <= 25;

-- BETWEEN (inclusive)
SELECT * FROM users WHERE age BETWEEN 25 AND 35;
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- IN (match any value in list)
SELECT * FROM users WHERE city IN ('NYC', 'LA', 'Chicago');
SELECT * FROM users WHERE age IN (25, 30, 35);

-- NOT IN
SELECT * FROM users WHERE city NOT IN ('NYC', 'LA');
```

### String Matching (LIKE)
```sql
-- Wildcards: % (any characters), _ (single character)
SELECT * FROM users WHERE name LIKE 'B%';        -- Starts with B
SELECT * FROM users WHERE name LIKE '%son';      -- Ends with son
SELECT * FROM users WHERE name LIKE '%ill%';     -- Contains ill
SELECT * FROM users WHERE name LIKE 'B_lly';     -- B + single char + lly
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Case insensitive (depends on DB)
SELECT * FROM users WHERE LOWER(name) LIKE 'billy%';

-- NOT LIKE
SELECT * FROM users WHERE name NOT LIKE 'A%';
```

### NULL Handling
```sql
-- Check for NULL
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- COALESCE (return first non-null)
SELECT name, COALESCE(email, 'No email') AS email FROM users;
SELECT COALESCE(phone, mobile, 'No contact') AS contact FROM users;

-- NULLIF (return NULL if equal)
SELECT NULLIF(age, 0) FROM users;  -- Returns NULL if age is 0
```

### Logical Operators
```sql
-- AND (all conditions must be true)
SELECT * FROM users WHERE age > 25 AND city = 'NYC';

-- OR (at least one condition must be true)
SELECT * FROM users WHERE age > 25 OR city = 'NYC';

-- NOT
SELECT * FROM users WHERE NOT age > 25;
SELECT * FROM users WHERE NOT city = 'NYC';

-- Combination
SELECT * FROM users
WHERE (age > 25 AND city = 'NYC')
   OR (age < 20 AND city = 'LA');
```

---

## 3. ORDER BY (Sorting)

```sql
-- Ascending (default)
SELECT * FROM users ORDER BY age;
SELECT * FROM users ORDER BY age ASC;

-- Descending
SELECT * FROM users ORDER BY age DESC;

-- Multiple columns (priority: left to right)
SELECT * FROM users ORDER BY city ASC, age DESC;

-- By column alias
SELECT name, age, salary * 12 AS annual_salary
FROM employees
ORDER BY annual_salary DESC;

-- By column number (not recommended, but works)
SELECT name, age FROM users ORDER BY 2;  -- Order by age (2nd column)

-- NULL handling
SELECT * FROM users ORDER BY email NULLS FIRST;
SELECT * FROM users ORDER BY email NULLS LAST;
```

---

## 4. Aggregate Functions

### Common Aggregates
```sql
-- COUNT
SELECT COUNT(*) FROM users;                    -- Count all rows
SELECT COUNT(email) FROM users;                -- Count non-NULL emails
SELECT COUNT(DISTINCT city) FROM users;        -- Count unique cities

-- SUM
SELECT SUM(amount) FROM orders;
SELECT SUM(salary) FROM employees WHERE department = 'Engineering';

-- AVG
SELECT AVG(age) FROM users;
SELECT AVG(salary) FROM employees;

-- MIN / MAX
SELECT MIN(age) FROM users;
SELECT MAX(salary) FROM employees;
SELECT MIN(created_at), MAX(created_at) FROM orders;

-- Multiple aggregates
SELECT COUNT(*) AS user_count,
       AVG(age) AS avg_age,
       MIN(age) AS youngest,
       MAX(age) AS oldest
FROM users;
```

### GROUP BY (Aggregate by Groups)
```sql
-- Group by single column
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city;

-- Group by multiple columns
SELECT city, age, COUNT(*) AS count
FROM users
GROUP BY city, age;

-- With aggregate functions
SELECT department,
       COUNT(*) AS employee_count,
       AVG(salary) AS avg_salary,
       MIN(salary) AS min_salary,
       MAX(salary) AS max_salary
FROM employees
GROUP BY department;

-- HAVING (filter AFTER grouping)
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
HAVING COUNT(*) > 10;

-- WHERE vs HAVING
-- WHERE filters rows BEFORE grouping
-- HAVING filters groups AFTER grouping
SELECT city, AVG(age) AS avg_age
FROM users
WHERE age > 18              -- Filter before grouping
GROUP BY city
HAVING AVG(age) > 30;       -- Filter after grouping
```

---

## 5. JOINs (CRITICAL for Interviews!)

### INNER JOIN (Only Matching Rows)
```sql
-- Basic join
SELECT users.name, orders.amount
FROM users
INNER JOIN orders ON users.id = orders.user_id;

-- Table aliases (shorter)
SELECT u.name, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Join with WHERE
SELECT u.name, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;

-- Multiple joins
SELECT u.name, o.amount, p.title AS product
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN products p ON o.product_id = p.id;
```

### LEFT JOIN (All from Left, Matching from Right)
```sql
-- Get all users, with their orders (if any)
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Find users with NO orders (NULL check)
SELECT u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### RIGHT JOIN (All from Right, Matching from Left)
```sql
-- Get all orders, with user info (if available)
SELECT u.name, o.amount
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- Rarely used (can flip to LEFT JOIN)
```

### FULL OUTER JOIN (All from Both)
```sql
-- Get all users and all orders
SELECT u.name, o.amount
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- Find unmatched rows from either side
SELECT u.name, o.amount
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id
WHERE u.id IS NULL OR o.id IS NULL;
```

### SELF JOIN (Join Table to Itself)
```sql
-- Employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.id;

-- Find pairs of users in same city
SELECT u1.name, u2.name, u1.city
FROM users u1
JOIN users u2 ON u1.city = u2.city AND u1.id < u2.id;
```

### CROSS JOIN (Cartesian Product)
```sql
-- Every combination
SELECT u.name, p.title
FROM users u
CROSS JOIN products p;

-- Rarely used intentionally
```

---

## 6. Subqueries (Queries within Queries)

### Subquery in WHERE
```sql
-- Find users who placed orders over $100
SELECT * FROM users
WHERE id IN (
    SELECT user_id FROM orders WHERE amount > 100
);

-- Find users with above-average age
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- NOT IN
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM orders);
```

### Subquery in FROM (Derived Table)
```sql
-- Average of averages
SELECT AVG(avg_salary) AS overall_avg
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_avgs;

-- Must use alias for subquery
```

### Subquery in SELECT
```sql
-- Include aggregated value for each row
SELECT name,
       age,
       (SELECT AVG(age) FROM users) AS avg_age
FROM users;
```

### Correlated Subquery (References Outer Query)
```sql
-- Find employees earning more than their department average
SELECT e.name, e.salary, e.department
FROM employees e
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department = e.department
);

-- EXISTS (check if subquery returns any rows)
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- NOT EXISTS
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

---

## 7. INSERT, UPDATE, DELETE

### INSERT
```sql
-- Single row
INSERT INTO users (name, email, age)
VALUES ('Billy', 'billy@example.com', 33);

-- Multiple rows
INSERT INTO users (name, email, age)
VALUES
    ('Billy', 'billy@example.com', 33),
    ('Alex', 'alex@example.com', 28),
    ('Sam', 'sam@example.com', 25);

-- Insert from SELECT
INSERT INTO archive_users
SELECT * FROM users WHERE created_at < '2024-01-01';

-- Insert with specific columns
INSERT INTO users (name, email)
VALUES ('Billy', 'billy@example.com');
-- Other columns get default values or NULL
```

### UPDATE
```sql
-- Update all rows (CAREFUL!)
UPDATE users SET age = 34;

-- Update with WHERE
UPDATE users SET age = 34 WHERE name = 'Billy';

-- Update multiple columns
UPDATE users
SET age = 34, city = 'NYC'
WHERE id = 1;

-- Update with calculation
UPDATE employees
SET salary = salary * 1.1
WHERE department = 'Engineering';

-- Update from subquery
UPDATE users
SET status = 'inactive'
WHERE id IN (SELECT user_id FROM inactive_list);
```

### DELETE
```sql
-- Delete all rows (CAREFUL!)
DELETE FROM users;

-- Delete with WHERE
DELETE FROM users WHERE age < 18;

-- Delete from subquery
DELETE FROM users
WHERE id NOT IN (SELECT user_id FROM orders);

-- TRUNCATE (faster, resets auto-increment)
TRUNCATE TABLE users;
```

---

## 8. Window Functions (Advanced)

### ROW_NUMBER, RANK, DENSE_RANK
```sql
-- ROW_NUMBER (unique sequential number)
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;

-- RANK (same rank for ties, gaps after ties)
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
-- Example: 1, 2, 2, 4, 5 (gap after tie)

-- DENSE_RANK (same rank for ties, NO gaps)
SELECT name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
-- Example: 1, 2, 2, 3, 4 (no gap)

-- PARTITION BY (rank within groups)
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

### Aggregate Window Functions
```sql
-- Running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) AS running_total
FROM sales;

-- Moving average (last 3 rows)
SELECT date, amount,
       AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM sales;

-- Compare to previous row (LAG) or next row (LEAD)
SELECT date, amount,
       LAG(amount) OVER (ORDER BY date) AS prev_amount,
       LEAD(amount) OVER (ORDER BY date) AS next_amount
FROM sales;

-- First and last values
SELECT name, department, salary,
       FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_in_dept,
       LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS lowest_in_dept
FROM employees;
```

---

## 9. Common Table Expressions (CTEs)

### Basic CTE
```sql
-- WITH clause (named subquery)
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 100000
)
SELECT department, COUNT(*) AS count
FROM high_earners
GROUP BY department;

-- Multiple CTEs
WITH
    high_earners AS (
        SELECT * FROM employees WHERE salary > 100000
    ),
    young_employees AS (
        SELECT * FROM employees WHERE age < 30
    )
SELECT * FROM high_earners
UNION
SELECT * FROM young_employees;
```

### Recursive CTE
```sql
-- Employee hierarchy (manager tree)
WITH RECURSIVE employee_hierarchy AS (
    -- Base case
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;
```

---

## 10. Set Operations

### UNION (Combine Results, Remove Duplicates)
```sql
SELECT name FROM customers
UNION
SELECT name FROM suppliers;

-- UNION ALL (keep duplicates, faster)
SELECT name FROM customers
UNION ALL
SELECT name FROM suppliers;
```

### INTERSECT (Common Rows)
```sql
-- Find names in both tables
SELECT name FROM customers
INTERSECT
SELECT name FROM suppliers;
```

### EXCEPT (Rows in First, Not in Second)
```sql
-- Customers who are NOT suppliers
SELECT name FROM customers
EXCEPT
SELECT name FROM suppliers;
```

---

## 11. Common Interview Patterns

### Find Nth Highest Salary
```sql
-- Using LIMIT and OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;  -- 3rd highest (0-indexed)

-- Using subquery
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);  -- 2nd highest

-- Using window function
WITH ranked AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
    FROM employees
)
SELECT DISTINCT salary FROM ranked WHERE rank = 3;
```

### Find Duplicates
```sql
-- Find duplicate emails
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Get all rows with duplicate emails
SELECT * FROM users
WHERE email IN (
    SELECT email FROM users
    GROUP BY email
    HAVING COUNT(*) > 1
);
```

### Delete Duplicates (Keep One)
```sql
-- Using ROW_NUMBER
WITH duplicates AS (
    SELECT id, email,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS row_num
    FROM users
)
DELETE FROM users
WHERE id IN (
    SELECT id FROM duplicates WHERE row_num > 1
);
```

### Running Total
```sql
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) AS running_total
FROM sales;
```

### Top N Per Group
```sql
-- Top 3 employees by salary in each department
WITH ranked AS (
    SELECT name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
    FROM employees
)
SELECT * FROM ranked WHERE rank <= 3;
```

### Consecutive Sequences
```sql
-- Find consecutive days with sales
WITH numbered AS (
    SELECT date,
           ROW_NUMBER() OVER (ORDER BY date) AS row_num,
           DATE_SUB(date, INTERVAL ROW_NUMBER() OVER (ORDER BY date) DAY) AS grp
    FROM sales
)
SELECT MIN(date) AS start_date, MAX(date) AS end_date, COUNT(*) AS days
FROM numbered
GROUP BY grp
HAVING COUNT(*) >= 3;  -- At least 3 consecutive days
```

---

## Quick SQL Tips for Tests

1. **Always use table aliases** in joins: `FROM users u JOIN orders o`
2. **WHERE filters before GROUP BY**, HAVING filters after
3. **INNER JOIN** = only matching rows, **LEFT JOIN** = all from left
4. **COUNT(*)** counts all rows, **COUNT(column)** counts non-NULL
5. **DISTINCT** removes duplicates
6. **Use LIMIT** to test queries on large tables
7. **Window functions** don't reduce rows (unlike GROUP BY)
8. **CTEs** make complex queries readable
9. **IN/NOT IN** can be slow; consider EXISTS/NOT EXISTS
10. **NULL is not equal to anything**, use IS NULL
11. **Date functions** vary by DB (MySQL vs PostgreSQL vs SQL Server)
12. **String concatenation**: || (SQL standard) or CONCAT()
13. **Case sensitivity** depends on database settings
14. **Indexes** speed up WHERE, JOIN, ORDER BY (not tested, but good to know)
15. **Explain query plans** before optimizing

---

## Common SQL Functions

### String Functions
```sql
UPPER(name)                    -- BILLY
LOWER(name)                    -- billy
LENGTH(name)                   -- 5
SUBSTRING(name, 1, 3)          -- Bil
CONCAT(first, ' ', last)       -- Billy Kennedy
TRIM(name)                     -- Remove whitespace
REPLACE(email, '@', ' AT ')    -- Replace text
```

### Date Functions (MySQL)
```sql
NOW()                          -- Current datetime
CURDATE()                      -- Current date
DATE(created_at)               -- Extract date part
YEAR(created_at)               -- Extract year
MONTH(created_at)              -- Extract month
DAY(created_at)                -- Extract day
DATE_ADD(date, INTERVAL 1 DAY) -- Add 1 day
DATE_SUB(date, INTERVAL 1 MONTH) -- Subtract 1 month
DATEDIFF(date1, date2)         -- Days between
```

### Math Functions
```sql
ABS(-5)                        -- 5
CEIL(3.2)                      -- 4
FLOOR(3.8)                     -- 3
ROUND(3.567, 2)                -- 3.57
POWER(2, 3)                    -- 8
SQRT(16)                       -- 4
MOD(10, 3)                     -- 1 (remainder)
```

### CASE (Conditional Logic)
```sql
SELECT name,
       CASE
           WHEN age < 18 THEN 'Minor'
           WHEN age < 65 THEN 'Adult'
           ELSE 'Senior'
       END AS age_group
FROM users;

-- Simple CASE
SELECT name,
       CASE status
           WHEN 1 THEN 'Active'
           WHEN 2 THEN 'Inactive'
           ELSE 'Unknown'
       END AS status_text
FROM users;
```

---

## Related Notes

- [[Python File IO Essentials]] - Similar data operations
- [[Working with APIs in Python]] - Data processing patterns
- [[Common Algorithms for Coding Tests]] - Data structure concepts
- [[JavaScript Essentials for Coding Tests]] - Array methods (similar to SQL)
- [[TypeScript Essentials for Coding Tests]] - Type-safe data handling

---

**Use this note when:**
- Preparing for SQL coding interviews
- Need quick reference for JOINs and aggregations
- Working with databases and data analysis
- Learning window functions and CTEs
- Building reports or dashboards

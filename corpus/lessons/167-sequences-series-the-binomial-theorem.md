---
title: "16.7 - Sequences, Series & the Binomial Theorem"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.7"
type: chapter
objectives:
  - "Write explicit and recursive formulas for arithmetic and geometric sequences"
  - "Evaluate finite sums in sigma notation and with the arithmetic and geometric series formulas"
  - "Decide whether an infinite geometric series converges and find its sum when it does"
  - "Expand a binomial power and find a specific term with binomial coefficients"
open_source: true
---

# 16.7 - Sequences, Series & the Binomial Theorem

A sequence is an ordered list of numbers, and a series is the sum of a sequence's terms. Two patterns appear constantly: adding the same amount each time (arithmetic) and multiplying by the same amount each time (geometric). This lesson gives formulas for the terms and sums of both, shows when an infinite sum has a finite value, and uses counting coefficients to expand powers like $(x + 2)^4$ without multiplying them out by hand.

## Prerequisites

You should be comfortable with function notation, since a sequence is a function whose inputs are the positive integers, as in [14.4 - Functions & Relations](/144-functions-relations). Geometric sequences use the exponent rules and exponential functions from [16.3 - Exponential & Logarithmic Functions](/163-exponential-logarithmic-functions), and binomial expansion relies on multiplying polynomials from [14.7 - Exponents & Polynomials](/147-exponents-polynomials).

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether a sequence is arithmetic, geometric, or neither, and write its $n$th term explicitly or recursively.
2. Expand and evaluate a sum written in sigma notation.
3. Find the sum of the first $n$ terms of an arithmetic or geometric sequence.
4. Determine whether an infinite geometric series converges and find its sum, including converting a repeating decimal to a fraction.
5. Use Pascal's triangle or $\binom{n}{k}$ to expand $(a + b)^n$ and to find one specific term.

## Core ideas

### Sequences

A **sequence** $a_1, a_2, a_3, \ldots$ can be given by an **explicit formula**, such as $a_n = n^2$, or by a **recursive formula** that gives the first term and a rule for each term from the previous one, such as $a_1 = 4$, $a_n = a_{n-1} + 3$.

- **Arithmetic:** consecutive terms differ by a constant **common difference** $d$, and $a_n = a_1 + (n - 1)d$.
- **Geometric:** consecutive terms have a constant **common ratio** $r$, and $a_n = a_1 r^{n-1}$.

### Sigma notation

$$\sum_{k=1}^{n} a_k = a_1 + a_2 + \cdots + a_n.$$

The variable $k$ is the **index**, $1$ is the lower limit, and $n$ is the upper limit. A sum from $k = m$ to $k = n$ has $n - m + 1$ terms.

### Series formulas

- Arithmetic: $S_n = \dfrac{n(a_1 + a_n)}{2}$, the number of terms times the average of the first and last terms.
- Geometric, $r \neq 1$: $S_n = \dfrac{a_1(1 - r^n)}{1 - r}$.
- Infinite geometric: if $|r| \lt 1$, then $S = \dfrac{a_1}{1 - r}$. If $|r| \geq 1$, the series **diverges**; it has no finite sum.

### The binomial theorem

The **binomial coefficient** $\binom{n}{k} = \dfrac{n!}{k!(n - k)!}$ counts the ways to choose $k$ items from $n$. The binomial theorem states

$$(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k.$$

The coefficients for each $n$ form a row of **Pascal's triangle**, where each entry is the sum of the two above it. Row $4$ is $1, 4, 6, 4, 1$. The term containing $b^k$ is $\binom{n}{k}a^{n-k}b^k$, which is the $(k + 1)$st term.

## Worked examples

### Example 1: An arithmetic sequence and its sum

For $7, 11, 15, 19, \ldots$, find $a_n$, $a_{50}$, and the sum of the first $50$ terms.

1. Differences are all $4$, so it is arithmetic with $a_1 = 7$ and $d = 4$.
2. $a_n = 7 + (n - 1)4 = 4n + 3$.
3. $a_{50} = 4(50) + 3 = 203$.
4. $S_{50} = \dfrac{50(7 + 203)}{2} = 25 \cdot 210 = 5250$.

### Example 2: A geometric sequence and its sum

For $3, 6, 12, 24, \ldots$, find $a_{10}$ and $S_{10}$.

1. Ratios are all $2$, so it is geometric with $a_1 = 3$ and $r = 2$.
2. $a_{10} = 3 \cdot 2^{9} = 3 \cdot 512 = 1536$.
3. $S_{10} = \dfrac{3(1 - 2^{10})}{1 - 2} = \dfrac{3(1 - 1024)}{-1} = 3069$.

### Example 3: Sigma notation

(a) $\displaystyle\sum_{k=1}^{5}(2k - 1) = 1 + 3 + 5 + 7 + 9 = 25$.

(b) $\displaystyle\sum_{k=1}^{20}(3k + 2)$: the terms run from $5$ to $62$ with common difference $3$, and there are $20$ of them. So the sum is $\dfrac{20(5 + 62)}{2} = 670$.

### Example 4: Infinite geometric series

(a) Write $0.\overline{7} = 0.777\ldots$ as a fraction. As a series, $0.7 + 0.07 + 0.007 + \cdots$ has $a_1 = 0.7$ and $r = 0.1$. Since $|r| \lt 1$, $S = \dfrac{0.7}{1 - 0.1} = \dfrac{0.7}{0.9} = \dfrac{7}{9}$.

(b) $8 - 4 + 2 - 1 + \cdots$ has $r = -\tfrac{1}{2}$, so $S = \dfrac{8}{1 - (-1/2)} = \dfrac{8}{3/2} = \dfrac{16}{3}$.

### Example 5: Expanding a binomial

Expand $(x + 2)^4$.

1. Row $4$ of Pascal's triangle: $1, 4, 6, 4, 1$.
2. Powers of $x$ decrease from $4$ to $0$ while powers of $2$ increase from $0$ to $4$.
3. $(x + 2)^4 = x^4 + 4x^3(2) + 6x^2(4) + 4x(8) + 16 = x^4 + 8x^3 + 24x^2 + 32x + 16$.
4. Check at $x = 1$: $(1 + 2)^4 = 81$ and $1 + 8 + 24 + 32 + 16 = 81$.

### Example 6: One specific term

Find the coefficient of $x^3$ in $(2x - 1)^7$.

1. The general term is $\binom{7}{k}(2x)^{7-k}(-1)^k$.
2. The power of $x$ is $7 - k = 3$, so $k = 4$.
3. $\binom{7}{4} = 35$, $(2x)^3 = 8x^3$, and $(-1)^4 = 1$.
4. The coefficient is $35 \cdot 8 = 280$.

## Common misconceptions and boundary cases

- **Summing a divergent series.** The formula $\tfrac{a_1}{1 - r}$ requires $|r| \lt 1$. Applied to $1 + 2 + 4 + \cdots$ it would give $-1$, which is meaningless; that series grows without bound.
- **Using $r^n$ instead of $r^{n-1}$.** The first term is $a_1 = a_1 r^0$, so the $n$th term has exponent $n - 1$.
- **"Freshman's dream."** $(a + b)^n \neq a^n + b^n$ for $n \geq 2$. For example, $(1 + 1)^2 = 4$, but $1^2 + 1^2 = 2$.
- **Miscounting terms.** $\sum_{k=0}^{10}$ has $11$ terms, not $10$.
- **Negative signs inside the binomial.** In $(2x - 1)^7$, treat $b = -1$; the signs alternate, and $(2x)^3 = 8x^3$, not $2x^3$.
- **Calling a sequence geometric because it grows fast.** $1, 4, 9, 16, \ldots$ grows quickly but its ratios ($4$, $2.25$, $1.78$, $\ldots$) are not constant; it is neither arithmetic nor geometric.

## Practice

1. For $20, 17, 14, \ldots$, write $a_n$ and find $a_{30}$.
2. Find the sum of the first $40$ terms of $20, 17, 14, \ldots$.
3. A geometric sequence has $a_1 = 5$ and $r = 3$. Find $a_6$ and $S_6$.
4. Evaluate $\displaystyle\sum_{k=1}^{4} 2^k$.
5. Decide whether each series converges, and find its sum if it does: (a) $\displaystyle\sum_{n=1}^{\infty} 6\left(\tfrac{2}{3}\right)^{n-1}$; (b) $\displaystyle\sum_{n=1}^{\infty}\left(-\tfrac{5}{4}\right)^{n}$.
6. Write $0.\overline{36} = 0.3636\ldots$ as a fraction in lowest terms.
7. Expand $(a - b)^5$.
8. Find the coefficient of $x^2$ in $(x + 3)^6$.
9. List the first four terms of $a_1 = 2$, $a_n = 3a_{n-1} - 1$.

<details>
<summary>Answer key and self-check</summary>

1. $d = -3$, so $a_n = 20 + (n - 1)(-3) = 23 - 3n$, and $a_{30} = -67$.
2. $a_{40} = 23 - 120 = -97$, so $S_{40} = \dfrac{40(20 - 97)}{2} = -1540$.
3. $a_6 = 5 \cdot 3^5 = 1215$; $S_6 = \dfrac{5(1 - 3^6)}{1 - 3} = \dfrac{5(-728)}{-2} = 1820$.
4. $2 + 4 + 8 + 16 = 30$.
5. (a) $r = \tfrac{2}{3}$, converges to $\dfrac{6}{1 - 2/3} = 18$. (b) $|r| = \tfrac{5}{4} \geq 1$, diverges.
6. $a_1 = 0.36$, $r = 0.01$: $\dfrac{0.36}{0.99} = \dfrac{36}{99} = \dfrac{4}{11}$.
7. $a^5 - 5a^4b + 10a^3b^2 - 10a^2b^3 + 5ab^4 - b^5$.
8. $x^{6-k} = x^2$ gives $k = 4$: $\binom{6}{4}3^4 = 15 \cdot 81 = 1215$.
9. $2, 5, 14, 41$.

Self-check method: for sums, add the first few terms directly and compare with the formula for a small $n$. For binomial expansions, substitute $x = 1$ (or $a = b = 1$) and confirm that the coefficients add up to the value of the original power.

</details>

## Where this fits

This lesson follows [16.6 - Conic Sections](/166-conic-sections) in the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). Infinite geometric series are the first example of a limit of partial sums, which is the subject of [16.8 - Limits & Introduction to Calculus](/168-limits-introduction-to-calculus). Binomial coefficients reappear as counting tools in probability.

## Sources

- OpenStax, *Precalculus 2e*, [11.1 Sequences and Their Notations](https://openstax.org/books/precalculus-2e/pages/11-1-sequences-and-their-notations)
- OpenStax, *Precalculus 2e*, [11.2 Arithmetic Sequences](https://openstax.org/books/precalculus-2e/pages/11-2-arithmetic-sequences)
- OpenStax, *Precalculus 2e*, [11.3 Geometric Sequences](https://openstax.org/books/precalculus-2e/pages/11-3-geometric-sequences)
- OpenStax, *Precalculus 2e*, [11.4 Series and Their Notations](https://openstax.org/books/precalculus-2e/pages/11-4-series-and-their-notations)
- OpenStax, *Precalculus 2e*, [11.6 Binomial Theorem](https://openstax.org/books/precalculus-2e/pages/11-6-binomial-theorem)

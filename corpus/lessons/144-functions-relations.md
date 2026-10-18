---
title: "14.4 - Functions & Relations"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.4"
type: chapter
objectives:
  - "Decide whether a relation given as pairs, a table, an equation, or a graph is a function"
  - "Find the domain and range of a function, including restrictions from division and square roots"
  - "Evaluate functions written in f(x) notation, including piecewise functions"
  - "Write explicit formulas for arithmetic and geometric sequences as functions of n"
open_source: true
---

# 14.4 - Functions & Relations

A function is a rule that assigns each input exactly one output. This lesson explains how a function differs from a general relation, how to find domain and range, how to read and evaluate $f(x)$ notation, and how arithmetic and geometric sequences can be treated as functions.

## Prerequisites

You should be able to evaluate expressions with negative inputs ([14.1 - The Language of Algebra](/141-the-language-of-algebra)), plot points on a coordinate plane, and write a solution set using inequality or interval notation ([14.3 - Linear Inequalities](/143-linear-inequalities)).

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether a set of ordered pairs, a table, an equation, or a graph represents a function, and justify the decision.
2. State the domain and range of a function, including values excluded because of division by zero or square roots of negative numbers.
3. Evaluate $f(x)$ for numbers and for expressions such as $f(a + 1)$.
4. Evaluate a piecewise function by choosing the correct rule for each input.
5. Write the $n$th term of an arithmetic or geometric sequence.

## Core ideas

### Relations and functions

A **relation** is any set of ordered pairs $(x, y)$. The set of all first coordinates (inputs) is the **domain**, and the set of all second coordinates (outputs) is the **range**. A **function** is a relation in which every input is paired with **exactly one** output. Two different inputs may share an output; one input may not have two different outputs.

On a graph, this becomes the **vertical line test**: if any vertical line crosses the graph more than once, some $x$-value has two $y$-values and the graph is not a function.

### Function notation

$f(x)$ is read "$f$ of $x$" and means "the output of the function $f$ when the input is $x$." The parentheses do not mean multiplication. To evaluate $f(3)$, replace every $x$ in the rule with $3$.

### Domain restrictions

When a function is given only as a formula, its domain is every real number for which the formula produces a real output. In Algebra I the two common restrictions are:

- a denominator cannot equal zero;
- the expression under a square root cannot be negative.

### Piecewise functions

A piecewise function uses different rules on different parts of the domain. To evaluate it, first decide which condition the input satisfies, then use only that rule.

### Sequences as functions

A sequence is a function whose domain is the positive integers $n = 1, 2, 3, \ldots$, with $a_n$ meaning the $n$th term.

- **Arithmetic:** each term adds a common difference $d$, so $a_n = a_1 + (n - 1)d$.
- **Geometric:** each term multiplies by a common ratio $r$, so $a_n = a_1 \cdot r^{\,n-1}$.

## Worked examples

### Example 1: Function or not?

(a) $\{(1, 4), (2, 5), (1, 6)\}$ is **not** a function: the input $1$ is paired with both $4$ and $6$.

(b) $\{(1, 4), (2, 4), (3, 4)\}$ **is** a function: each input has one output, even though all of the outputs are the same. Its domain is $\{1, 2, 3\}$ and its range is $\{4\}$.

(c) The circle $x^2 + y^2 = 25$ is not a function of $x$. When $x = 3$, $y^2 = 16$, so $y = 4$ or $y = -4$. A vertical line at $x = 3$ meets the circle twice.

### Example 2: Evaluating with numbers and expressions

Let $f(x) = x^2 - 3x + 2$.

1. $f(-1) = (-1)^2 - 3(-1) + 2 = 1 + 3 + 2 = 6$.
2. $f(2) = 4 - 6 + 2 = 0$, so $x = 2$ is an input that produces an output of zero.
3. $f(a + 1)$: replace each $x$ with $(a + 1)$:
   $$(a + 1)^2 - 3(a + 1) + 2 = a^2 + 2a + 1 - 3a - 3 + 2 = a^2 - a.$$

Self-check for step 3: when $a = 1$, $f(a + 1) = f(2) = 0$, and $a^2 - a = 0$. They agree.

### Example 3: Finding domains

(a) $g(x) = \dfrac{1}{x - 4}$. The denominator is zero when $x = 4$, so the domain is all real numbers except $4$: $(-\infty, 4) \cup (4, \infty)$.

(b) $h(x) = \sqrt{x + 3}$. We need $x + 3 \ge 0$, so $x \ge -3$, giving domain $[-3, \infty)$. A principal square root is never negative, so the range is $[0, \infty)$.

### Example 4: A piecewise function

$$f(x) = \begin{cases} 2x + 1, & x \lt 0 \\ x^2, & x \ge 0 \end{cases}$$

- $f(-3)$: since $-3 \lt 0$, use the first rule: $2(-3) + 1 = -5$.
- $f(0)$: since $0 \ge 0$, use the second rule: $0^2 = 0$.
- $f(2)$: use the second rule: $2^2 = 4$.

### Example 5: Sequences

(a) $7, 11, 15, 19, \ldots$ has common difference $d = 4$. Then $a_n = 7 + 4(n - 1) = 4n + 3$, and $a_{20} = 4(20) + 3 = 83$.

(b) $3, 6, 12, 24, \ldots$ has common ratio $r = 2$. Then $a_n = 3 \cdot 2^{\,n-1}$, and $a_8 = 3 \cdot 2^7 = 3 \cdot 128 = 384$.

## Common misconceptions and boundary cases

- **Reading $f(x)$ as multiplication.** $f(3)$ is not "$f$ times $3$." It is the output for input $3$.
- **Assuming $f(a + b) = f(a) + f(b)$.** For $f(x) = x^2$, $f(1 + 2) = 9$ but $f(1) + f(2) = 1 + 4 = 5$. Substitute the whole expression instead.
- **Rejecting repeated outputs.** A function may send many inputs to the same output (Example 1b). Only a repeated **input** with different outputs breaks the definition.
- **Missing hidden restrictions.** $\sqrt{x - 5}$ requires $x \ge 5$, not $x \gt 5$; zero is allowed under a square root but not in a denominator.
- **Using both pieces at a boundary.** In Example 4 the input $0$ belongs only to the second piece because of the $\ge$ sign. Check which inequality includes the boundary.

## Practice

1. Is each relation a function? (a) $\{(-2, 3), (0, 3), (5, 1)\}$ (b) $\{(4, 1), (4, -1), (9, 3)\}$
2. For $f(x) = 2x^2 - 5$, find $f(-3)$, $f(0)$, and $f(t - 1)$.
3. Find the domain of $k(x) = \sqrt{2x - 6}$ and of $m(x) = \dfrac{5}{x + 2}$.
4. For $p(x) = -x$ when $x \le 1$ and $p(x) = 3x - 2$ when $x \gt 1$, find $p(1)$ and $p(4)$.
5. Write a formula for $50, 47, 44, \ldots$ and find the 15th term.
6. Find the 6th term of the geometric sequence $2, 6, 18, \ldots$.

<details>
<summary>Answer key and self-check</summary>

1. (a) Function: each input appears once. (b) Not a function: input $4$ has outputs $1$ and $-1$.
2. $f(-3) = 18 - 5 = 13$; $f(0) = -5$; $f(t - 1) = 2(t^2 - 2t + 1) - 5 = 2t^2 - 4t - 3$. Check with $t = 1$: both give $f(0) = -5$.
3. $2x - 6 \ge 0$ gives domain $[3, \infty)$. For $m$, $x \neq -2$: $(-\infty, -2) \cup (-2, \infty)$.
4. $p(1) = -1$ (first rule, because $1 \le 1$); $p(4) = 3(4) - 2 = 10$.
5. $d = -3$, so $a_n = 50 - 3(n - 1) = 53 - 3n$, and $a_{15} = 53 - 45 = 8$.
6. $r = 3$, so $a_6 = 2 \cdot 3^5 = 486$.

Self-check method: for sequence formulas, substitute $n = 1$ and $n = 2$ and confirm the first two terms. For domains, test a number you excluded and confirm it really produces division by zero or a negative square root.

</details>

## Where this fits

Functions are the organizing idea for the rest of the [Algebra I course](/subject/algebra-i). Next, [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing) studies the most important family of functions in detail, and quadratic functions appear in [14.8 - Factoring & Quadratics](/148-factoring-quadratics).

## Sources

- OpenStax, *Intermediate Algebra 2e*, [3.5 Relations and Functions](https://openstax.org/books/intermediate-algebra-2e/pages/3-5-relations-and-functions)
- OpenStax, *Intermediate Algebra 2e*, [3.6 Graphs of Functions](https://openstax.org/books/intermediate-algebra-2e/pages/3-6-graphs-of-functions)

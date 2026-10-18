---
title: "14.3 - Linear Inequalities"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.3"
type: chapter
objectives:
  - "Solve one-step and multi-step linear inequalities and reverse the symbol when required"
  - "Express solution sets with a number line, inequality notation, and interval notation"
  - "Solve compound inequalities joined by AND or OR"
  - "Solve absolute value equations and inequalities and recognize empty or all-real solution sets"
  - "Write and interpret an inequality for a budget or limit situation"
open_source: true
---

# 14.3 - Linear Inequalities

An inequality states that one expression is less than or greater than another, and its solution is usually an entire interval of numbers rather than a single value. This lesson shows how to solve linear inequalities, write the answer in interval notation, and handle compound and absolute value inequalities.

The four inequality symbols are $\lt$ (less than), $\le$ (less than or equal to), $\gt$ (greater than), and $\ge$ (greater than or equal to).

## Prerequisites

You should be able to solve multi-step linear equations, as in [14.2 - Linear Equations](/142-linear-equations), and to place positive and negative numbers in order on a number line.

## Learning objectives

By the end of this lesson you should be able to:

1. Solve a linear inequality and explain exactly when the inequality symbol must be reversed.
2. Graph a solution set on a number line using open and closed endpoints.
3. Convert between inequality notation and interval notation.
4. Solve compound inequalities and describe the result as an intersection (AND) or union (OR).
5. Rewrite an absolute value inequality as a compound inequality and solve it.

## Core ideas

### Solving rules

Adding or subtracting the same number on both sides keeps the inequality true. Multiplying or dividing both sides by a **positive** number also keeps the direction. Multiplying or dividing by a **negative** number reverses the direction. To see why, start with the true statement $2 \lt 5$ and multiply by $-1$: the results are $-2$ and $-5$, and $-2 \gt -5$. The order flipped, so the symbol must flip.

### Notation

- A closed endpoint (filled dot, square bracket) means the endpoint is included: $\le$ or $\ge$.
- An open endpoint (hollow dot, parenthesis) means the endpoint is excluded: $\lt$ or $\gt$.
- Infinity is never included, so it always takes a parenthesis.

For example, $x \le 3$ is written $(-\infty, 3]$, and $-2 \lt x \le 4$ is written $(-2, 4]$.

### Compound inequalities

An **AND** inequality is satisfied by numbers that make both parts true, so its solution is the **intersection** (overlap) of the two sets. An **OR** inequality is satisfied when at least one part is true, so its solution is the **union** of the two sets, written with $\cup$.

### Absolute value

$|x|$ is the distance from $x$ to $0$. For a positive number $a$:

- $|x| = a$ means $x = a$ or $x = -a$.
- $|x| \lt a$ means $-a \lt x \lt a$ (distance less than $a$: one interval, an AND statement).
- $|x| \gt a$ means $x \lt -a$ or $x \gt a$ (distance more than $a$: two rays, an OR statement).

Isolate the absolute value expression before applying these rules.

## Worked examples

### Example 1: Dividing by a negative

Solve $-3x + 5 \gt 17$.

1. Subtract $5$: $-3x \gt 12$.
2. Divide by $-3$ and reverse the symbol: $x \lt -4$.
3. Interval notation: $(-\infty, -4)$. On a number line, draw a hollow dot at $-4$ and shade to the left.

Check one value inside and the boundary: for $x = -5$, $-3(-5) + 5 = 20$ and $20 \gt 17$ is true. For $x = -4$, the left side equals $17$, and $17 \gt 17$ is false, which confirms the open endpoint.

### Example 2: A three-part AND inequality

Solve $-1 \le 2x + 3 \lt 9$.

1. Subtract $3$ from all three parts: $-4 \le 2x \lt 6$.
2. Divide all three parts by $2$ (positive, so no reversal): $-2 \le x \lt 3$.
3. Interval notation: $[-2, 3)$.

### Example 3: An OR inequality

Solve $x - 1 \lt -3$ or $2x \ge 8$.

1. Solve each part separately: $x \lt -2$ or $x \ge 4$.
2. Combine as a union: $(-\infty, -2) \cup [4, \infty)$.

There is no single interval that describes this set, so it cannot be squeezed into one three-part statement.

### Example 4: Absolute value inequalities

(a) Solve $|x - 2| \le 5$. This is a "less than" case, so write $-5 \le x - 2 \le 5$. Add $2$ to every part: $-3 \le x \le 7$, or $[-3, 7]$. Every solution is within $5$ units of $2$.

(b) Solve $|2x + 1| \gt 7$. This is a "greater than" case, so split it: $2x + 1 \gt 7$ or $2x + 1 \lt -7$. Then $x \gt 3$ or $x \lt -4$, which is $(-\infty, -4) \cup (3, \infty)$.

### Example 5: A budget limit

A phone plan costs \$25 per month plus \$0.10 per text message. How many texts keep the bill at or below \$40? (Illustrative pricing.)

1. Let $t$ be the number of texts: $25 + 0.10t \le 40$.
2. Subtract $25$: $0.10t \le 15$. Divide by $0.10$: $t \le 150$.
3. Interpret: texts are counted in whole numbers and cannot be negative, so the realistic answer is any whole number from $0$ to $150$.

## Common misconceptions and boundary cases

- **Reversing for the wrong reason.** The symbol reverses only when multiplying or dividing by a negative number. Subtracting a number, or having a negative answer, does not reverse it: $x + 5 \lt 2$ gives $x \lt -3$ with no flip.
- **Writing an impossible three-part inequality.** "$x \lt -2$ or $x \ge 4$" must not be written as $-2 \gt x \ge 4$, because no number is both less than $-2$ and at least $4$.
- **Negative right sides with absolute value.** $|x| \lt -2$ has **no solution** because a distance cannot be negative. $|x| \gt -2$ is true for **all real numbers**. $|x| = 0$ has the single solution $x = 0$.
- **Wrong endpoint type.** Use brackets only with $\le$ or $\ge$. Never put a bracket next to $\infty$.
- **Ignoring context.** In Example 5 the algebra gives $t \le 150$, but negative or fractional texts are meaningless. Always restrict the answer to values that make sense in the situation.

## Practice

1. Solve $4 - 5x \ge 19$ and write the answer in interval notation.
2. Solve $3(x - 2) \lt 5x + 4$.
3. Solve $-6 \lt 3x - 9 \le 6$.
4. Solve $|x + 4| \lt 3$.
5. Solve $|3x - 6| \ge 9$.
6. A gym charges a \$30 joining fee plus \$12 per class. Write and solve an inequality for the number of classes $c$ that keep the total at most \$150. (Illustrative pricing.)

<details>
<summary>Answer key and self-check</summary>

1. $-5x \ge 15$, divide by $-5$ and reverse: $x \le -3$, or $(-\infty, -3]$.
2. $3x - 6 \lt 5x + 4$, so $-10 \lt 2x$ and $x \gt -5$, or $(-5, \infty)$.
3. Add $9$: $3 \lt 3x \le 15$. Divide by $3$: $1 \lt x \le 5$, or $(1, 5]$.
4. $-3 \lt x + 4 \lt 3$, so $-7 \lt x \lt -1$, or $(-7, -1)$.
5. $3x - 6 \ge 9$ or $3x - 6 \le -9$, so $x \ge 5$ or $x \le -1$: $(-\infty, -1] \cup [5, \infty)$.
6. $30 + 12c \le 150$, so $12c \le 120$ and $c \le 10$. Any whole number of classes from $0$ to $10$.

Self-check method: pick one number inside your solution set and one outside it, substitute both into the original inequality, and confirm the first makes it true and the second makes it false. Then test the endpoint to confirm open or closed.

</details>

## Where this fits

Inequalities describe limits and ranges throughout the [Algebra I course](/subject/algebra-i). Next, [14.4 - Functions & Relations](/144-functions-relations) uses inequality and interval notation to describe the domain and range of a function.

## Sources

- OpenStax, *Elementary Algebra 2e*, [2.7 Solve Linear Inequalities](https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities)
- OpenStax, *Intermediate Algebra 2e*, [2.6 Solve Compound Inequalities](https://openstax.org/books/intermediate-algebra-2e/pages/2-6-solve-compound-inequalities)
- OpenStax, *Intermediate Algebra 2e*, [2.7 Solve Absolute Value Inequalities](https://openstax.org/books/intermediate-algebra-2e/pages/2-7-solve-absolute-value-inequalities)

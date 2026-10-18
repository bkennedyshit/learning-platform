---
title: "16.1 - Polynomial Functions"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.1"
type: chapter
objectives:
  - "Predict the end behavior of a polynomial from its degree and leading coefficient"
  - "Find zeros, state their multiplicities, and describe how the graph behaves at each zero"
  - "Divide by a linear factor with synthetic division and apply the remainder and factor theorems"
  - "Use the rational zero theorem to find all real and complex zeros of a polynomial"
open_source: true
---

# 16.1 - Polynomial Functions

A polynomial function is built only from a variable raised to whole-number powers, multiplied by constants, and added together. Polynomials model areas, volumes, and many smooth curves, and they are the first family of functions whose graphs you can sketch accurately from algebra alone. This lesson shows how to read end behavior and zeros from a formula, how to divide polynomials quickly, and how to find every zero of a polynomial.

## Prerequisites

You should be comfortable adding, multiplying, and factoring polynomials and solving quadratic equations from [14.7 - Exponents & Polynomials](/147-exponents-polynomials) and [14.8 - Factoring & Quadratics](/148-factoring-quadratics). You also need to evaluate a function at a number and find intercepts from [14.4 - Functions & Relations](/144-functions-relations).

## Learning objectives

By the end of this lesson you should be able to:

1. State the degree and leading coefficient of a polynomial and use them to describe its end behavior.
2. Find the zeros of a factored polynomial, state the multiplicity of each, and decide whether the graph crosses or touches the $x$-axis there.
3. Divide a polynomial by $x - c$ using synthetic division and use the remainder theorem to evaluate $f(c)$.
4. List candidate rational zeros, confirm one with the factor theorem, and reduce the polynomial to find all remaining zeros, including complex ones.

## Core ideas

### Definition and vocabulary

A **polynomial function** of degree $n$ has the form

$$f(x) = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0,$$

where $n$ is a nonnegative integer and $a_n \neq 0$. The number $a_n$ is the **leading coefficient** and $a_n x^n$ is the **leading term**. Expressions such as $x^{-1}$ or $\sqrt{x}$ are not allowed, so $f(x) = 3x^2 + \sqrt{x}$ is not a polynomial.

### End behavior

For large $|x|$, the leading term dominates every other term, so it alone decides what happens at the far left and far right of the graph.

- Even degree, positive leading coefficient: both ends rise.
- Even degree, negative leading coefficient: both ends fall.
- Odd degree, positive leading coefficient: falls on the left, rises on the right.
- Odd degree, negative leading coefficient: rises on the left, falls on the right.

### Zeros and multiplicity

If $(x - c)^k$ is a factor of $f$ and $(x - c)^{k+1}$ is not, then $c$ is a zero of **multiplicity** $k$. At a zero of odd multiplicity the graph crosses the $x$-axis; at a zero of even multiplicity it touches the axis and turns back. A polynomial of degree $n$ has at most $n$ real zeros and at most $n - 1$ turning points.

### Division theorems

- **Remainder theorem:** when $f(x)$ is divided by $x - c$, the remainder is $f(c)$.
- **Factor theorem:** $x - c$ is a factor of $f(x)$ exactly when $f(c) = 0$.
- **Rational zero theorem:** if a polynomial has integer coefficients, every rational zero has the form $\tfrac{p}{q}$, where $p$ divides the constant term $a_0$ and $q$ divides the leading coefficient $a_n$.
- **Fundamental theorem of algebra:** a polynomial of degree $n \geq 1$ has exactly $n$ complex zeros when each zero is counted by its multiplicity. If the coefficients are real, nonreal zeros come in conjugate pairs $a \pm bi$.

**Synthetic division** is a compact way to divide by $x - c$. Write $c$ and the coefficients of $f$, including a $0$ for every missing power. Bring down the first coefficient, multiply it by $c$, add the product to the next coefficient, and repeat. The last number is the remainder and the others are the coefficients of the quotient, one degree lower than $f$.

## Worked examples

### Example 1: End behavior, zeros, and a rough graph

Describe the graph of $f(x) = -(x + 2)(x - 1)^2$.

1. Multiplying the leading terms gives $-x \cdot x^2 = -x^3$, so the degree is $3$ and the leading coefficient is $-1$. The graph rises on the left and falls on the right.
2. Zeros: $x = -2$ has multiplicity $1$, so the graph crosses there. $x = 1$ has multiplicity $2$, so the graph touches the axis and turns back.
3. $y$-intercept: $f(0) = -(2)(1) = -2$, so the point is $(0, -2)$.
4. Test the sign in each interval: $f(-3) = -(-1)(16) = 16 \gt 0$, $f(0) = -2 \lt 0$, and $f(2) = -(4)(1) = -4 \lt 0$. The graph comes down from the upper left, crosses at $-2$, stays below the axis, touches at $1$, and continues down. This matches the end behavior from step 1.

### Example 2: Synthetic division and the factor theorem

Show that $x - 3$ is a factor of $f(x) = 2x^3 - 3x^2 - 11x + 6$, then find all zeros.

1. Use $c = 3$ with coefficients $2, -3, -11, 6$.
2. Bring down $2$. Multiply: $2 \cdot 3 = 6$; add: $-3 + 6 = 3$. Multiply: $3 \cdot 3 = 9$; add: $-11 + 9 = -2$. Multiply: $-2 \cdot 3 = -6$; add: $6 + (-6) = 0$.
3. The remainder is $0$, so $f(3) = 0$ and $x - 3$ is a factor. The quotient is $2x^2 + 3x - 2$.
4. Factor the quotient: $2x^2 + 3x - 2 = (2x - 1)(x + 2)$.
5. So $f(x) = (x - 3)(2x - 1)(x + 2)$ and the zeros are $3$, $\tfrac{1}{2}$, and $-2$.

Check: $f(3) = 54 - 27 - 33 + 6 = 0$.

### Example 3: The remainder theorem with a missing term

Find the remainder when $f(x) = x^4 - 3x^3 + 2x - 5$ is divided by $x - 2$.

1. There is no $x^2$ term, so the coefficient list is $1, -3, 0, 2, -5$.
2. Synthetic division with $c = 2$: bring down $1$; $1 \cdot 2 = 2$, $-3 + 2 = -1$; $-1 \cdot 2 = -2$, $0 + (-2) = -2$; $-2 \cdot 2 = -4$, $2 + (-4) = -2$; $-2 \cdot 2 = -4$, $-5 + (-4) = -9$.
3. The remainder is $-9$ and the quotient is $x^3 - x^2 - 2x - 2$.

Check by direct substitution: $f(2) = 16 - 24 + 4 - 5 = -9$, as the remainder theorem predicts.

### Example 4: All zeros, including complex zeros

Find all zeros of $f(x) = x^3 - x^2 + 4x - 4$.

1. The constant term is $-4$ and the leading coefficient is $1$, so the candidate rational zeros are $\pm 1, \pm 2, \pm 4$.
2. Test $x = 1$: $1 - 1 + 4 - 4 = 0$. So $x - 1$ is a factor.
3. Synthetic division with $c = 1$ on $1, -1, 4, -4$ gives $1, 0, 4$ with remainder $0$, so the quotient is $x^2 + 4$.
4. Solve $x^2 + 4 = 0$: $x^2 = -4$, so $x = \pm 2i$.
5. The zeros are $1$, $2i$, and $-2i$: three zeros for a degree-3 polynomial, with the nonreal zeros forming a conjugate pair. The graph crosses the $x$-axis only once, at $x = 1$.

## Common misconceptions and boundary cases

- **Judging end behavior from the sign alone.** $-x^4$ and $-x^3$ both have negative leading coefficients, but $-x^4$ falls on both sides while $-x^3$ rises on the left. Degree parity matters as much as the sign.
- **Skipping zero placeholders.** In Example 3, leaving out the $0$ for the missing $x^2$ term shifts every coefficient and gives the wrong quotient and remainder.
- **Using the wrong sign for $c$.** Dividing by $x + 2$ means $c = -2$, because $x + 2 = x - (-2)$.
- **Treating candidates as zeros.** The rational zero theorem only lists possibilities. Each candidate must be tested, and irrational or complex zeros never appear on the list.
- **Expecting $n$ real zeros.** A degree-$n$ polynomial has $n$ complex zeros counted with multiplicity, but some may be nonreal, as in Example 4.

## Practice

1. Describe the end behavior and give the $y$-intercept of $g(x) = 3x^4 - x^3 + 7$.
2. List each zero of $h(x) = x^2(x - 4)^3(x + 1)$ with its multiplicity, and say whether the graph crosses or touches at each one.
3. Use synthetic division to divide $x^3 + 4x^2 - 7x - 10$ by $x + 1$, then find all zeros.
4. Use the remainder theorem to find the remainder when $p(x) = 2x^3 - 5x + 1$ is divided by $x - 3$.
5. Find all zeros of $f(x) = 2x^3 + x^2 - 13x + 6$.
6. Write a degree-3 polynomial with real coefficients and leading coefficient $1$ whose zeros include $2$ and $3i$.
7. Decide whether $x - 2$ is a factor of $x^4 - 16$, and factor it completely over the real numbers.

<details>
<summary>Answer key and self-check</summary>

1. Degree $4$ (even) with positive leading coefficient, so both ends rise. $y$-intercept $(0, 7)$.
2. $0$ has multiplicity $2$ (touches); $4$ has multiplicity $3$ (crosses, flattening as it passes through); $-1$ has multiplicity $1$ (crosses). The degree is $6$ with leading coefficient $1$, so both ends rise.
3. $c = -1$ on $1, 4, -7, -10$: $1$; $4 - 1 = 3$; $-7 - 3 = -10$; $-10 + 10 = 0$. Quotient $x^2 + 3x - 10 = (x + 5)(x - 2)$. Zeros $-1$, $-5$, $2$.
4. $p(3) = 54 - 15 + 1 = 40$.
5. Candidates $\pm 1, \pm 2, \pm 3, \pm 6, \pm \tfrac{1}{2}, \pm \tfrac{3}{2}$. $f(2) = 16 + 4 - 26 + 6 = 0$. Dividing by $x - 2$ gives $2x^2 + 5x - 3 = (2x - 1)(x + 3)$. Zeros $2$, $\tfrac{1}{2}$, $-3$.
6. Real coefficients force $-3i$ to be a zero too: $(x - 2)(x - 3i)(x + 3i) = (x - 2)(x^2 + 9) = x^3 - 2x^2 + 9x - 18$.
7. $2^4 - 16 = 0$, so yes. $x^4 - 16 = (x^2 - 4)(x^2 + 4) = (x - 2)(x + 2)(x^2 + 4)$.

Self-check method: multiply your factors back together to recover the original polynomial, and substitute each claimed zero into the original function to confirm it gives $0$.

</details>

## Where this fits

This lesson opens the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). The next lesson, [16.2 - Rational Functions](/162-rational-functions), divides one polynomial by another; the same factoring and division skills locate its asymptotes and holes. To practice, graph each function from this lesson in a graphing tool and compare the picture with your predicted end behavior and multiplicities.

## Sources

- OpenStax, *Precalculus 2e*, [3.3 Power Functions and Polynomial Functions](https://openstax.org/books/precalculus-2e/pages/3-3-power-functions-and-polynomial-functions)
- OpenStax, *Precalculus 2e*, [3.4 Graphs of Polynomial Functions](https://openstax.org/books/precalculus-2e/pages/3-4-graphs-of-polynomial-functions)
- OpenStax, *Precalculus 2e*, [3.5 Dividing Polynomials](https://openstax.org/books/precalculus-2e/pages/3-5-dividing-polynomials)
- OpenStax, *Precalculus 2e*, [3.6 Zeros of Polynomial Functions](https://openstax.org/books/precalculus-2e/pages/3-6-zeros-of-polynomial-functions)

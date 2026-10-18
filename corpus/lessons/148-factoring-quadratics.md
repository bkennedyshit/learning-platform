---
title: "14.8 - Factoring & Quadratics"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.8"
type: chapter
objectives:
  - "Factor polynomials using the greatest common factor, trinomial methods, and special-product patterns"
  - "Solve quadratic equations by factoring with the zero-product property"
  - "Solve quadratic equations with the quadratic formula and use the discriminant to count real solutions"
  - "Find the vertex, axis of symmetry, and intercepts of a parabola"
open_source: true
---

# 14.8 - Factoring & Quadratics

Factoring rewrites a polynomial as a product, and that product form is what makes quadratic equations solvable. This lesson covers the main factoring patterns, solving quadratics by factoring and by the quadratic formula, and reading the key features of a parabola.

## Prerequisites

You should be able to multiply binomials and recognize the special products from [14.7 - Exponents & Polynomials](/147-exponents-polynomials), and to find intercepts of a graph from [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing). Factoring is multiplication run in reverse, so every factorization can be checked by multiplying.

## Learning objectives

By the end of this lesson you should be able to:

1. Factor out a greatest common factor (GCF) and factor trinomials of the forms $x^2 + bx + c$ and $ax^2 + bx + c$.
2. Recognize and factor a difference of squares and a perfect square trinomial.
3. Solve a quadratic equation by setting it equal to zero, factoring, and applying the zero-product property.
4. Solve any quadratic equation with the quadratic formula and use the discriminant to predict the number of real solutions.
5. Find the vertex, axis of symmetry, $x$-intercepts, and $y$-intercept of $y = ax^2 + bx + c$.

## Core ideas

### A factoring strategy

1. Factor out the GCF of all terms first.
2. Count the terms. For two terms, look for a **difference of squares**: $a^2 - b^2 = (a - b)(a + b)$.
3. For three terms, check for a **perfect square trinomial**: $a^2 \pm 2ab + b^2 = (a \pm b)^2$. Otherwise factor the trinomial:
   - For $x^2 + bx + c$, find two numbers whose product is $c$ and whose sum is $b$.
   - For $ax^2 + bx + c$ with $a \neq 1$, use the **ac method**: find two numbers whose product is $ac$ and whose sum is $b$, split the middle term, and factor by grouping.
4. Check each factor to see whether it can be factored further, then multiply back to verify.

### Zero-product property

If $AB = 0$, then $A = 0$ or $B = 0$. This works **only** when one side is zero, which is why a quadratic equation must be rearranged into the form $ax^2 + bx + c = 0$ before factoring.

### The quadratic formula

Every equation $ax^2 + bx + c = 0$ with $a \neq 0$ has solutions

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}.$$

The **discriminant** $b^2 - 4ac$ tells how many real solutions there are: two if it is positive, one if it is zero, and none if it is negative.

### Parabolas

The graph of $y = ax^2 + bx + c$ is a **parabola**. It opens upward if $a \gt 0$ and downward if $a \lt 0$. Its **axis of symmetry** is the vertical line $x = -\tfrac{b}{2a}$, and the **vertex** is the point on that line. The $x$-intercepts are the real solutions of $ax^2 + bx + c = 0$, and the $y$-intercept is $(0, c)$.

## Worked examples

### Example 1: GCF and a simple trinomial

(a) $6x^3 - 15x^2$: the GCF of $6$ and $15$ is $3$, and the lowest power of $x$ is $x^2$. Result: $3x^2(2x - 5)$.

(b) $x^2 - x - 12$: we need two numbers with product $-12$ and sum $-1$. The pair $-4$ and $3$ works. Result: $(x - 4)(x + 3)$. Check: $x^2 + 3x - 4x - 12 = x^2 - x - 12$.

### Example 2: The ac method

Factor $6x^2 + 7x - 3$.

1. $ac = 6 \cdot (-3) = -18$. Find two numbers with product $-18$ and sum $7$: $9$ and $-2$.
2. Split the middle term: $6x^2 + 9x - 2x - 3$.
3. Group: $3x(2x + 3) - 1(2x + 3)$.
4. Factor out the common binomial: $(3x - 1)(2x + 3)$.

Check: $(3x - 1)(2x + 3) = 6x^2 + 9x - 2x - 3 = 6x^2 + 7x - 3$.

### Example 3: Solving by factoring

Solve $x^2 + 2x = 15$.

1. Set the equation equal to zero: $x^2 + 2x - 15 = 0$.
2. Factor: $(x + 5)(x - 3) = 0$.
3. Zero-product property: $x + 5 = 0$ or $x - 3 = 0$, so $x = -5$ or $x = 3$.

Check: $(-5)^2 + 2(-5) = 25 - 10 = 15$ and $3^2 + 2(3) = 9 + 6 = 15$.

### Example 4: The quadratic formula

Solve $2x^2 - 4x - 3 = 0$, which does not factor over the integers.

1. Identify $a = 2$, $b = -4$, $c = -3$.
2. Discriminant: $(-4)^2 - 4(2)(-3) = 16 + 24 = 40$, which is positive, so there are two real solutions.
3. Substitute: $x = \dfrac{4 \pm \sqrt{40}}{4} = \dfrac{4 \pm 2\sqrt{10}}{4} = \dfrac{2 \pm \sqrt{10}}{2}$.
4. Approximate: $x \approx 2.58$ or $x \approx -0.58$.

### Example 5: Features of a parabola

Analyze $y = x^2 - 6x + 5$.

1. $a = 1 \gt 0$, so the parabola opens upward.
2. Axis of symmetry: $x = -\tfrac{-6}{2(1)} = 3$.
3. Vertex: $y = 3^2 - 6(3) + 5 = -4$, so the vertex is $(3, -4)$, the minimum point.
4. $x$-intercepts: $x^2 - 6x + 5 = (x - 1)(x - 5) = 0$, so $(1, 0)$ and $(5, 0)$. They are symmetric about $x = 3$, which confirms the axis.
5. $y$-intercept: $(0, 5)$.

## Common misconceptions and boundary cases

- **Using the zero-product property on a nonzero product.** From $x(x - 3) = 10$ you cannot conclude $x = 10$ or $x - 3 = 10$. Rewrite as $x^2 - 3x - 10 = 0$, factor as $(x - 5)(x + 2) = 0$, and get $x = 5$ or $x = -2$.
- **Dividing by the variable.** Dividing both sides of $x^2 = 5x$ by $x$ gives only $x = 5$ and loses $x = 0$. Instead, write $x^2 - 5x = 0$, factor $x(x - 5) = 0$, and keep both solutions.
- **Forgetting the GCF.** $2x^2 - 8$ factors completely as $2(x - 2)(x + 2)$. Stopping at $(2x - 4)(x + 2)$ leaves a common factor of $2$ inside a binomial.
- **Factoring a sum of squares.** $x^2 + 9$ does not factor over the real numbers; its discriminant is $-36$. Only a **difference** of squares factors this way.
- **Missing the negative root.** $x^2 = 16$ has two solutions, $x = 4$ and $x = -4$.
- **Sign errors in the formula.** With $b = -4$, the formula begins with $-b = 4$, and $b^2 = 16$, not $-16$. Write $a$, $b$, and $c$ with their signs before substituting.

## Practice

1. Factor $4x^2y - 10xy^2$.
2. Factor $x^2 + 9x + 20$.
3. Factor $3x^2 - 10x - 8$.
4. Factor $49m^2 - 25$ and $x^2 - 14x + 49$.
5. Solve $2x^2 - 18 = 0$ and $x^2 = 7x$.
6. Solve $x^2 + 4x - 1 = 0$ with the quadratic formula. Give exact and approximate answers.
7. Find the vertex, axis of symmetry, intercepts, and direction of opening for $y = -x^2 + 4x + 5$.
8. Use the discriminant to find the number of real solutions of $3x^2 + 2x + 4 = 0$.

<details>
<summary>Answer key and self-check</summary>

1. $2xy(2x - 5y)$.
2. $(x + 4)(x + 5)$.
3. $ac = -24$; the pair $-12$ and $2$ sums to $-10$. $3x^2 - 12x + 2x - 8 = 3x(x - 4) + 2(x - 4) = (3x + 2)(x - 4)$.
4. $(7m - 5)(7m + 5)$; $(x - 7)^2$.
5. $2(x^2 - 9) = 2(x - 3)(x + 3) = 0$, so $x = \pm 3$. $x^2 - 7x = 0$ gives $x(x - 7) = 0$, so $x = 0$ or $x = 7$.
6. Discriminant $16 + 4 = 20$. $x = \dfrac{-4 \pm \sqrt{20}}{2} = -2 \pm \sqrt{5}$, so $x \approx 0.24$ or $x \approx -4.24$.
7. $a = -1$, so it opens downward. Axis $x = -\tfrac{4}{2(-1)} = 2$; vertex $(2, 9)$. $-x^2 + 4x + 5 = -(x - 5)(x + 1)$, so $x$-intercepts $(-1, 0)$ and $(5, 0)$; $y$-intercept $(0, 5)$.
8. $2^2 - 4(3)(4) = 4 - 48 = -44 \lt 0$, so there are no real solutions.

Self-check method: multiply your factors to recover the original polynomial, and substitute each solution into the original equation. For parabolas, the two $x$-intercepts should be the same distance from the axis of symmetry.

</details>

## Where this fits

This lesson completes the [Algebra I course](/subject/algebra-i). Quadratic functions and the quadratic formula are developed further in [Algebra II & Pre-Calculus](/subject/algebra-ii-and-pre-calculus), and factoring and solving quadratics are used for area and length problems in [Geometry](/subject/geometry). To review the path that led here, start again from [14.1 - The Language of Algebra](/141-the-language-of-algebra).

## Sources

- OpenStax, *Elementary Algebra 2e*, [7.1 Greatest Common Factor and Factor by Grouping](https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping)
- OpenStax, *Elementary Algebra 2e*, [7.2 Factor Trinomials of the Form x2+bx+c](https://openstax.org/books/elementary-algebra-2e/pages/7-2-factor-trinomials-of-the-form-x2-bx-c)
- OpenStax, *Elementary Algebra 2e*, [7.4 Factor Special Products](https://openstax.org/books/elementary-algebra-2e/pages/7-4-factor-special-products)
- OpenStax, *Elementary Algebra 2e*, [7.6 Quadratic Equations](https://openstax.org/books/elementary-algebra-2e/pages/7-6-quadratic-equations)
- OpenStax, *Elementary Algebra 2e*, [10.3 Solve Quadratic Equations Using the Quadratic Formula](https://openstax.org/books/elementary-algebra-2e/pages/10-3-solve-quadratic-equations-using-the-quadratic-formula)
- OpenStax, *Elementary Algebra 2e*, [10.5 Graphing Quadratic Equations in Two Variables](https://openstax.org/books/elementary-algebra-2e/pages/10-5-graphing-quadratic-equations-in-two-variables)

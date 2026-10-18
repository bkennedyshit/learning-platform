---
title: "16.2 - Rational Functions"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.2"
type: chapter
objectives:
  - "State the domain of a rational function and distinguish vertical asymptotes from holes"
  - "Find horizontal or slant asymptotes by comparing degrees or by polynomial division"
  - "Sketch a rational function from its intercepts, asymptotes, holes, and sign changes"
  - "Decompose a simple rational expression with distinct linear factors into partial fractions"
open_source: true
---

# 16.2 - Rational Functions

A rational function is a quotient of two polynomials. Rational functions model averages, rates, and concentrations, and their graphs show behavior polynomials never do: they can break apart at a vertical asymptote, have a single missing point, and level off toward a line. This lesson shows how to find each of those features from the formula and combine them into an accurate sketch.

## Prerequisites

You need to factor polynomials and divide them by long or synthetic division, as in [16.1 - Polynomial Functions](/161-polynomial-functions), and to simplify algebraic fractions and solve linear equations from the [Algebra I course](/subject/algebra-i). Recall that division by zero is undefined; that single fact drives most of this lesson.

## Learning objectives

By the end of this lesson you should be able to:

1. Write the domain of a rational function and decide, for each excluded value, whether it produces a vertical asymptote or a hole.
2. Find a horizontal asymptote by comparing degrees, or a slant asymptote by division.
3. Locate intercepts and use sign tests to sketch the graph between asymptotes.
4. Split a fraction with two distinct linear factors in the denominator into partial fractions and check the result.

## Core ideas

### Definition and domain

A **rational function** has the form $f(x) = \dfrac{P(x)}{Q(x)}$, where $P$ and $Q$ are polynomials and $Q$ is not the zero polynomial. Its **domain** is every real number except the zeros of $Q$.

### Vertical asymptotes and holes

Factor numerator and denominator completely, then cancel common factors.

- A factor $x - c$ that **cancels** completely leaves a **hole** (a removable discontinuity) at $x = c$. The $y$-coordinate of the hole is the simplified function evaluated at $c$.
- A factor $x - c$ that **remains in the denominator** after canceling produces a **vertical asymptote** $x = c$. Near it, $|f(x)|$ grows without bound.

### Horizontal and slant asymptotes

Let $n$ be the degree of the numerator and $m$ the degree of the denominator.

- If $n \lt m$, the horizontal asymptote is $y = 0$.
- If $n = m$, the horizontal asymptote is $y = \dfrac{\text{leading coefficient of } P}{\text{leading coefficient of } Q}$.
- If $n = m + 1$, there is no horizontal asymptote. Divide $P$ by $Q$; the quotient (a linear polynomial) is the **slant asymptote**.
- If $n \gt m + 1$, there is no horizontal or slant asymptote; the end behavior follows a polynomial of degree $n - m$.

These asymptotes describe the graph only as $x \to \pm\infty$. A graph never crosses a vertical asymptote, but it **can** cross a horizontal or slant asymptote at finite $x$.

### Intercepts

The $x$-intercepts are the zeros of the simplified numerator that are in the domain. The $y$-intercept is $f(0)$, if $0$ is in the domain.

### Partial fractions

Reversing the addition of fractions is called **partial fraction decomposition**. When the denominator factors into distinct linear factors, write

$$\frac{P(x)}{(x - a)(x - b)} = \frac{A}{x - a} + \frac{B}{x - b},$$

provided the degree of $P$ is less than $2$. Multiply through by the denominator and substitute $x = a$ and $x = b$ to find $A$ and $B$.

## Worked examples

### Example 1: A basic rational function

Analyze $f(x) = \dfrac{2x + 1}{x - 3}$.

1. Domain: $x \neq 3$. Nothing cancels, so $x = 3$ is a vertical asymptote.
2. Both degrees are $1$, so the horizontal asymptote is $y = \tfrac{2}{1} = 2$.
3. $x$-intercept: $2x + 1 = 0$ gives $x = -\tfrac{1}{2}$. $y$-intercept: $f(0) = \tfrac{1}{-3} = -\tfrac{1}{3}$.
4. Sign test: $f(4) = \tfrac{9}{1} = 9 \gt 0$, so the graph shoots up just right of $x = 3$. $f(2) = \tfrac{5}{-1} = -5 \lt 0$, so it plunges down just left of $x = 3$.

### Example 2: A hole and an asymptote

Analyze $f(x) = \dfrac{x^2 - 4}{x^2 - x - 2}$.

1. Factor: $f(x) = \dfrac{(x - 2)(x + 2)}{(x - 2)(x + 1)}$. The domain excludes $x = 2$ and $x = -1$.
2. The factor $x - 2$ cancels, leaving $\dfrac{x + 2}{x + 1}$ for $x \neq 2$. So $x = 2$ is a hole, at height $\tfrac{2 + 2}{2 + 1} = \tfrac{4}{3}$. The point $\left(2, \tfrac{4}{3}\right)$ is drawn as an open circle.
3. The factor $x + 1$ remains, so $x = -1$ is a vertical asymptote.
4. The original degrees are both $2$ with leading coefficients $1$, so the horizontal asymptote is $y = 1$.
5. Intercepts: $x = -2$ makes the simplified numerator zero, giving $(-2, 0)$. $f(0) = \tfrac{-4}{-2} = 2$, giving $(0, 2)$.

### Example 3: A slant asymptote

Find the asymptotes of $f(x) = \dfrac{x^2 + 3x + 1}{x + 1}$.

1. The denominator is zero at $x = -1$; the numerator there is $1 - 3 + 1 = -1 \neq 0$, so $x = -1$ is a vertical asymptote.
2. The numerator's degree is one more than the denominator's, so divide. Synthetic division with $c = -1$ on $1, 3, 1$: bring down $1$; $3 + (-1) = 2$; $1 + (-2) = -1$.
3. So $f(x) = x + 2 - \dfrac{1}{x + 1}$. As $|x|$ grows, $\tfrac{1}{x + 1} \to 0$, so the slant asymptote is $y = x + 2$.

### Example 4: Partial fractions

Decompose $\dfrac{x + 7}{(x - 1)(x + 3)}$.

1. Write $\dfrac{x + 7}{(x - 1)(x + 3)} = \dfrac{A}{x - 1} + \dfrac{B}{x + 3}$.
2. Multiply by $(x - 1)(x + 3)$: $x + 7 = A(x + 3) + B(x - 1)$.
3. Let $x = 1$: $8 = 4A$, so $A = 2$. Let $x = -3$: $4 = -4B$, so $B = -1$.
4. Result: $\dfrac{2}{x - 1} - \dfrac{1}{x + 3}$.

Check: $2(x + 3) - (x - 1) = 2x + 6 - x + 1 = x + 7$.

## Common misconceptions and boundary cases

- **Every zero of the denominator is a vertical asymptote.** Not if the factor cancels. In Example 2, $x = 2$ is a hole, not an asymptote. Always factor and cancel before naming asymptotes.
- **Graphs never cross horizontal asymptotes.** They can. $f(x) = \dfrac{2x^2 + x}{x^2 + 1}$ has horizontal asymptote $y = 2$, yet $f(2) = \tfrac{10}{5} = 2$. Setting $2x^2 + x = 2(x^2 + 1)$ gives $x = 2$, the crossing point.
- **Canceling terms instead of factors.** $\dfrac{x + 2}{x + 5}$ cannot be simplified by "canceling the $x$"; only common **factors** of the whole numerator and denominator cancel.
- **Forgetting the hole after simplifying.** The simplified formula $\tfrac{x + 2}{x + 1}$ is defined at $x = 2$, but the original function is not. The domain comes from the original denominator.

## Practice

1. Find the domain, vertical asymptotes, horizontal asymptote, and zeros of $f(x) = \dfrac{3x}{x^2 - 9}$.
2. Find all holes, asymptotes, and intercepts of $g(x) = \dfrac{x^2 + x - 6}{x^2 - 4}$.
3. Find the slant asymptote of $h(x) = \dfrac{2x^2 - 3x + 4}{x - 2}$.
4. Write a rational function with a vertical asymptote $x = 1$, horizontal asymptote $y = 3$, and an $x$-intercept at $2$.
5. Solve $\dfrac{x + 1}{x - 2} = 3$ and check that your answer is in the domain.
6. Decompose $\dfrac{3x + 5}{(x + 1)(x + 3)}$ into partial fractions.
7. For $k(x) = \dfrac{2x^2 - 5x - 3}{x^2 - 2x - 3}$, find the hole and asymptotes, and decide whether the graph ever crosses its horizontal asymptote.

<details>
<summary>Answer key and self-check</summary>

1. Domain $x \neq \pm 3$. Vertical asymptotes $x = 3$ and $x = -3$. Degree $1 \lt 2$, so $y = 0$. Zero at $x = 0$.
2. $g(x) = \dfrac{(x + 3)(x - 2)}{(x - 2)(x + 2)}$. Hole at $x = 2$ with height $\tfrac{5}{4}$, so $\left(2, \tfrac{5}{4}\right)$. Vertical asymptote $x = -2$. Horizontal asymptote $y = 1$. $x$-intercept $(-3, 0)$; $y$-intercept $g(0) = \tfrac{-6}{-4} = \tfrac{3}{2}$.
3. $2x^2 - 3x + 4 = (x - 2)(2x + 1) + 6$, so $h(x) = 2x + 1 + \dfrac{6}{x - 2}$ and the slant asymptote is $y = 2x + 1$.
4. One answer: $f(x) = \dfrac{3(x - 2)}{x - 1}$. Other answers are possible; check that equal degrees give the ratio $3$.
5. $x + 1 = 3(x - 2)$ gives $x + 1 = 3x - 6$, so $x = \tfrac{7}{2}$. It is not $2$, so it is valid. Check: $\tfrac{4.5}{1.5} = 3$.
6. $3x + 5 = A(x + 3) + B(x + 1)$. $x = -1$: $2 = 2A$, $A = 1$. $x = -3$: $-4 = -2B$, $B = 2$. Result $\dfrac{1}{x + 1} + \dfrac{2}{x + 3}$.
7. $k(x) = \dfrac{(2x + 1)(x - 3)}{(x - 3)(x + 1)}$. Hole at $\left(3, \tfrac{7}{4}\right)$; vertical asymptote $x = -1$; horizontal asymptote $y = 2$. Setting $\tfrac{2x + 1}{x + 1} = 2$ gives $2x + 1 = 2x + 2$, which has no solution, so the graph never crosses $y = 2$.

Self-check method: substitute a large value such as $x = 1000$ to confirm your horizontal or slant asymptote, and substitute values just left and right of each vertical asymptote to confirm the signs in your sketch.

</details>

## Where this fits

Rational functions extend [16.1 - Polynomial Functions](/161-polynomial-functions) and are part of the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). Holes and asymptotes return in [16.8 - Limits & Introduction to Calculus](/168-limits-introduction-to-calculus), where they are described precisely with limits. The next lesson, [16.3 - Exponential & Logarithmic Functions](/163-exponential-logarithmic-functions), introduces functions with a horizontal asymptote but no vertical one.

## Sources

- OpenStax, *Precalculus 2e*, [3.5 Dividing Polynomials](https://openstax.org/books/precalculus-2e/pages/3-5-dividing-polynomials)
- OpenStax, *Precalculus 2e*, [3.7 Rational Functions](https://openstax.org/books/precalculus-2e/pages/3-7-rational-functions)
- OpenStax, *Precalculus 2e*, [9.4 Partial Fractions](https://openstax.org/books/precalculus-2e/pages/9-4-partial-fractions)

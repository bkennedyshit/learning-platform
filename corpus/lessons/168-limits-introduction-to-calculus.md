---
title: "16.8 - Limits & Introduction to Calculus"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.8"
type: chapter
objectives:
  - "Estimate limits from tables and graphs and evaluate them algebraically, including 0/0 forms"
  - "Use one-sided limits to decide whether a two-sided limit exists"
  - "Evaluate limits at infinity of rational functions and connect them to horizontal asymptotes"
  - "Test a function for continuity at a point and classify discontinuities"
  - "Compute an instantaneous rate of change as the limit of average rates of change"
open_source: true
---

# 16.8 - Limits & Introduction to Calculus

A limit describes the value a function approaches as its input gets close to some number, whether or not the function is actually defined there. Limits are the foundation of calculus: they make precise what a hole or an asymptote is, define what it means for a function to be continuous, and turn the slope between two points into the slope at a single point. This lesson develops limits informally and uses them to introduce the derivative.

## Prerequisites

You need to factor and simplify rational expressions and identify holes and asymptotes from [16.2 - Rational Functions](/162-rational-functions), and to evaluate and graph piecewise functions as in [14.4 - Functions & Relations](/144-functions-relations). The slope formula from [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing) is the starting point for rates of change.

## Learning objectives

By the end of this lesson you should be able to:

1. Estimate a limit from a table or graph, and evaluate it algebraically by substitution, factoring, or rationalizing.
2. Find one-sided limits and use them to decide whether a two-sided limit exists.
3. Evaluate limits of rational functions as $x \to \infty$ and relate them to horizontal asymptotes.
4. Apply the three-part definition of continuity and classify a discontinuity as removable, jump, or infinite.
5. Find an average rate of change and the instantaneous rate of change $f'(a)$ as a limit.

## Core ideas

### What a limit means

We write $\displaystyle\lim_{x \to c} f(x) = L$ if $f(x)$ can be made as close to $L$ as we like by taking $x$ close enough to $c$ (but not equal to $c$). The value $f(c)$ itself plays no role; $f$ need not even be defined at $c$.

The **one-sided limits** $\displaystyle\lim_{x \to c^-} f(x)$ and $\displaystyle\lim_{x \to c^+} f(x)$ use only inputs to the left or to the right of $c$. The two-sided limit exists exactly when both one-sided limits exist and are equal.

### Evaluating limits algebraically

- **Direct substitution:** for polynomials, and for rational functions whose denominator is not zero at $c$, the limit equals $f(c)$.
- **The form $\tfrac{0}{0}$:** substitution gives no information. Factor and cancel, or multiply by a conjugate to remove a square root, then substitute.
- **A nonzero number over $0$:** the function grows without bound near $c$; there is a vertical asymptote and the limit does not exist as a real number. One-sided limits may be $+\infty$ or $-\infty$.

### Limits at infinity

For a rational function, divide numerator and denominator by the highest power of $x$ in the denominator. As $x \to \infty$, every term of the form $\tfrac{k}{x^p}$ with $p \gt 0$ approaches $0$. The result matches the horizontal-asymptote rules: the limit is $0$ if the numerator's degree is smaller, the ratio of leading coefficients if the degrees are equal, and the function grows without bound if the numerator's degree is larger.

### Continuity

A function $f$ is **continuous at $c$** if all three conditions hold:

1. $f(c)$ is defined;
2. $\displaystyle\lim_{x \to c} f(x)$ exists;
3. $\displaystyle\lim_{x \to c} f(x) = f(c)$.

A **removable** discontinuity (a hole) occurs when the limit exists but condition 1 or 3 fails. A **jump** occurs when the one-sided limits are finite but different. An **infinite** discontinuity occurs at a vertical asymptote.

### Rates of change and the derivative

The **average rate of change** of $f$ on $[a, a + h]$ is the slope of the secant line:

$$\frac{f(a + h) - f(a)}{h}.$$

Letting $h \to 0$ gives the **instantaneous rate of change**, or **derivative**, at $a$:

$$f'(a) = \lim_{h \to 0}\frac{f(a + h) - f(a)}{h}.$$

Geometrically, $f'(a)$ is the slope of the tangent line to the graph at $(a, f(a))$.

## Worked examples

### Example 1: A table, then algebra

Find $\displaystyle\lim_{x \to 2}\frac{x^2 - 4}{x - 2}$.

1. A table suggests the answer: at $x = 1.9, 1.99, 2.01, 2.1$ the function equals $3.9, 3.99, 4.01, 4.1$. The values approach $4$ from both sides.
2. Algebraically, substitution gives $\tfrac{0}{0}$. Factor: $\dfrac{(x - 2)(x + 2)}{x - 2} = x + 2$ for $x \neq 2$.
3. The limit is $2 + 2 = 4$. The function is undefined at $x = 2$; its graph is the line $y = x + 2$ with a hole at $(2, 4)$.

### Example 2: Rationalizing

Find $\displaystyle\lim_{x \to 0}\frac{\sqrt{x + 9} - 3}{x}$.

1. Substitution gives $\tfrac{0}{0}$. Multiply by the conjugate $\sqrt{x + 9} + 3$ over itself.
2. The numerator becomes $(x + 9) - 9 = x$, so the expression is $\dfrac{x}{x(\sqrt{x + 9} + 3)} = \dfrac{1}{\sqrt{x + 9} + 3}$ for $x \neq 0$.
3. Substitute: $\dfrac{1}{3 + 3} = \dfrac{1}{6}$.

Check numerically: at $x = 0.01$, $\dfrac{\sqrt{9.01} - 3}{0.01} \approx 0.16662$, close to $\tfrac{1}{6} \approx 0.16667$.

### Example 3: One-sided limits and a jump

Let $f(x) = x + 1$ for $x \lt 1$ and $f(x) = x^2 + 3$ for $x \geq 1$.

1. Left: $\displaystyle\lim_{x \to 1^-}(x + 1) = 2$.
2. Right: $\displaystyle\lim_{x \to 1^+}(x^2 + 3) = 4$.
3. The one-sided limits differ, so $\displaystyle\lim_{x \to 1} f(x)$ does not exist. Since $f(1) = 4$ is defined but the limit is not, $f$ has a jump discontinuity at $x = 1$.

### Example 4: A limit at infinity

Find $\displaystyle\lim_{x \to \infty}\frac{3x^2 - x}{5x^2 + 2}$.

1. Divide every term by $x^2$: $\dfrac{3 - \tfrac{1}{x}}{5 + \tfrac{2}{x^2}}$.
2. As $x \to \infty$, $\tfrac{1}{x} \to 0$ and $\tfrac{2}{x^2} \to 0$.
3. The limit is $\tfrac{3}{5}$, so $y = \tfrac{3}{5}$ is the horizontal asymptote, matching the equal-degree rule from [16.2 - Rational Functions](/162-rational-functions).

### Example 5: Making a piecewise function continuous

Find $k$ so that $f(x) = kx + 1$ for $x \lt 2$ and $f(x) = x^2 - k$ for $x \geq 2$ is continuous at $x = 2$.

1. Left limit: $2k + 1$. Right limit and value: $f(2) = 4 - k$.
2. Set them equal: $2k + 1 = 4 - k$, so $3k = 3$ and $k = 1$.
3. Check: with $k = 1$ both sides give $3$, and $f(2) = 3$.

### Example 6: From average to instantaneous rate

For $f(x) = x^2$, find the average rate of change on $[3, 3.1]$ and the instantaneous rate at $x = 3$.

1. Average: $\dfrac{3.1^2 - 3^2}{0.1} = \dfrac{9.61 - 9}{0.1} = 6.1$.
2. Instantaneous: $\dfrac{(3 + h)^2 - 9}{h} = \dfrac{9 + 6h + h^2 - 9}{h} = \dfrac{h(6 + h)}{h} = 6 + h$ for $h \neq 0$.
3. Let $h \to 0$: $f'(3) = 6$.
4. The tangent line at $(3, 9)$ is $y - 9 = 6(x - 3)$, or $y = 6x - 9$. As $h$ shrinks, the secant slopes $6.1, 6.01, 6.001, \ldots$ approach $6$.

## Common misconceptions and boundary cases

- **"The limit is just $f(c)$."** Only for continuous functions. In Example 1, $f(2)$ does not exist but the limit is $4$; in the removable case of Practice 5 below, $f(c)$ exists but differs from the limit.
- **Reading $\tfrac{0}{0}$ as an answer.** $\tfrac{0}{0}$ is an **indeterminate form**, not $0$, $1$, or "undefined." It signals that more algebra is needed; the actual limit could be any number or might not exist.
- **Ignoring one side.** $\displaystyle\lim_{x \to 0}\frac{|x|}{x}$ looks like it should be $1$ when testing only positive inputs, but from the left the values are $-1$. The two-sided limit does not exist.
- **Treating $\infty$ as a number.** Writing $\displaystyle\lim_{x \to 3^+}\frac{1}{x - 3} = \infty$ describes unbounded growth. It does not mean the limit exists, and $\infty - \infty$ or $\tfrac{\infty}{\infty}$ cannot be simplified arithmetically.
- **Canceling $h$ too early.** In the derivative quotient, expand and simplify the numerator first; only a factor of $h$ that multiplies the **whole** numerator can be canceled.

## Practice

1. Find $\displaystyle\lim_{x \to 4}\frac{x^2 - 16}{x - 4}$.
2. Find $\displaystyle\lim_{x \to -1}\frac{x^2 + 3x + 2}{x + 1}$.
3. Find $\displaystyle\lim_{x \to 0}\frac{\sqrt{4 + x} - 2}{x}$.
4. Find $\displaystyle\lim_{x \to \infty}\frac{2x + 7}{x^2 - 1}$ and $\displaystyle\lim_{x \to \infty}\frac{4x^3 + 1}{2x^3 - x}$.
5. Let $g(x) = 2x - 1$ for $x \lt 3$, $g(3) = 8$, and $g(x) = x + 2$ for $x \gt 3$. Find $\displaystyle\lim_{x \to 3} g(x)$ and classify the discontinuity at $x = 3$.
6. Describe $\displaystyle\lim_{x \to 2^-}\frac{1}{x - 2}$, $\displaystyle\lim_{x \to 2^+}\frac{1}{x - 2}$, and the two-sided limit.
7. Use the limit definition to find $f'(1)$ for $f(x) = 3x^2 - 2x$, and write the tangent line at $x = 1$.
8. Find the average rate of change of $f(x) = \sqrt{x}$ on $[4, 9]$.
9. Find the value of $a$ for which $\displaystyle\lim_{x \to 3}\frac{x^2 - a}{x - 3}$ is a finite number, and find that limit.

<details>
<summary>Answer key and self-check</summary>

1. $\dfrac{(x - 4)(x + 4)}{x - 4} = x + 4 \to 8$.
2. $\dfrac{(x + 1)(x + 2)}{x + 1} = x + 2 \to 1$.
3. Multiply by the conjugate: $\dfrac{1}{\sqrt{4 + x} + 2} \to \dfrac{1}{4}$.
4. $0$ (numerator degree is smaller); $\tfrac{4}{2} = 2$ (equal degrees).
5. Left: $2(3) - 1 = 5$. Right: $3 + 2 = 5$. The limit is $5$, but $g(3) = 8 \neq 5$: a removable discontinuity.
6. $-\infty$ from the left and $+\infty$ from the right; the two-sided limit does not exist, and $x = 2$ is a vertical asymptote.
7. $f(1 + h) = 3(1 + 2h + h^2) - 2 - 2h = 1 + 4h + 3h^2$, so $\dfrac{f(1 + h) - f(1)}{h} = \dfrac{4h + 3h^2}{h} = 4 + 3h \to 4$. Since $f(1) = 1$, the tangent line is $y - 1 = 4(x - 1)$, or $y = 4x - 3$.
8. $\dfrac{\sqrt{9} - \sqrt{4}}{9 - 4} = \dfrac{1}{5}$.
9. The numerator must be $0$ at $x = 3$, so $a = 9$. Then $\dfrac{x^2 - 9}{x - 3} = x + 3 \to 6$.

Self-check method: confirm each algebraic limit with a quick table, using inputs such as $c \pm 0.01$ and $c \pm 0.001$ on both sides. If the two sides head toward different values, the two-sided limit does not exist.

</details>

## Where this fits

This lesson completes the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus) and is the bridge to calculus. The same ideas are treated with full rigor, including the epsilon–delta definition, in [Limits & Continuity](/11-limits-continuity), and the derivative introduced here is developed into a complete set of rules in [Single-Variable Differentiation](/12-single-variable-differentiation). To review the path that led here, return to [16.1 - Polynomial Functions](/161-polynomial-functions).

## Sources

- OpenStax, *Precalculus 2e*, [12.1 Finding Limits: Numerical and Graphical Approaches](https://openstax.org/books/precalculus-2e/pages/12-1-finding-limits-numerical-and-graphical-approaches)
- OpenStax, *Precalculus 2e*, [12.2 Finding Limits: Properties of Limits](https://openstax.org/books/precalculus-2e/pages/12-2-finding-limits-properties-of-limits)
- OpenStax, *Precalculus 2e*, [12.3 Continuity](https://openstax.org/books/precalculus-2e/pages/12-3-continuity)
- OpenStax, *Precalculus 2e*, [12.4 Derivatives](https://openstax.org/books/precalculus-2e/pages/12-4-derivatives)
- MIT OpenCourseWare, [18.01SC Single Variable Calculus, Fall 2010](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)

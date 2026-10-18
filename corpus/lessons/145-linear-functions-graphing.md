---
title: "14.5 - Linear Functions & Graphing"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.5"
type: chapter
objectives:
  - "Compute slope from two points and interpret it as a rate of change"
  - "Write the equation of a line in slope-intercept, point-slope, and standard form"
  - "Graph a line from its slope and intercept or from its intercepts"
  - "Identify and write equations of parallel and perpendicular lines"
  - "Recognize and solve direct variation problems"
open_source: true
---

# 14.5 - Linear Functions & Graphing

A linear function has a constant rate of change, so its graph is a straight line. This lesson covers slope, the three common forms for the equation of a line, graphing methods, parallel and perpendicular lines, and direct variation.

## Prerequisites

You should know function notation and the idea of domain and range from [14.4 - Functions & Relations](/144-functions-relations), be able to solve a linear equation for $y$ ([14.2 - Linear Equations](/142-linear-equations)), and be able to plot points on the coordinate plane.

## Learning objectives

By the end of this lesson you should be able to:

1. Calculate the slope between two points and say what it means in a context.
2. Write the equation of a line given a point and slope, two points, or a graph.
3. Convert between slope-intercept form and standard form.
4. Decide whether two lines are parallel, perpendicular, or neither, using slopes.
5. Use a constant of variation to solve a direct variation problem.

## Core ideas

### Slope

The **slope** of a line measures how much $y$ changes for each 1-unit increase in $x$. For two points $(x_1, y_1)$ and $(x_2, y_2)$ with $x_1 \neq x_2$:

$$m = \frac{\Delta y}{\Delta x} = \frac{y_2 - y_1}{x_2 - x_1}.$$

A positive slope rises from left to right, a negative slope falls, a horizontal line has slope $0$, and a vertical line has **undefined** slope because $\Delta x = 0$.

### Forms of a linear equation

- **Slope-intercept form:** $y = mx + b$, where $m$ is the slope and $(0, b)$ is the $y$-intercept. Best for graphing quickly.
- **Point-slope form:** $y - y_1 = m(x - x_1)$, using any point $(x_1, y_1)$ on the line. Best for writing an equation from a point and a slope.
- **Standard form:** $Ax + By = C$. Best for finding both intercepts and for systems of equations in [14.6](/146-systems-of-equations).

As a function, a non-vertical line is $f(x) = mx + b$. A vertical line $x = k$ is a relation but not a function.

### Parallel and perpendicular lines

Two distinct non-vertical lines are **parallel** when their slopes are equal. Two lines are **perpendicular** when their slopes multiply to $-1$, meaning each slope is the **negative reciprocal** of the other: $m_2 = -\tfrac{1}{m_1}$. A horizontal line and a vertical line are also perpendicular.

### Direct variation

$y$ **varies directly** with $x$ when $y = kx$ for a nonzero constant $k$, called the constant of variation. Its graph is a line through the origin with slope $k$.

## Worked examples

### Example 1: Equation from two points

Find the equation of the line through $(-2, 5)$ and $(4, -7)$.

1. Slope: $m = \dfrac{-7 - 5}{4 - (-2)} = \dfrac{-12}{6} = -2$.
2. Point-slope form using $(-2, 5)$: $y - 5 = -2(x + 2)$.
3. Distribute and solve for $y$: $y - 5 = -2x - 4$, so $y = -2x + 1$.

Check with the other point: $-2(4) + 1 = -7$. The line passes through $(4, -7)$.

### Example 2: Standard form and intercepts

Graph $3x - 4y = 12$ and find its slope.

1. $x$-intercept: let $y = 0$, so $3x = 12$ and $x = 4$. Point $(4, 0)$.
2. $y$-intercept: let $x = 0$, so $-4y = 12$ and $y = -3$. Point $(0, -3)$.
3. Plot both intercepts and draw the line through them.
4. Slope: solve for $y$: $-4y = -3x + 12$, so $y = \tfrac{3}{4}x - 3$. The slope is $\tfrac{3}{4}$.

Check with the intercepts: from $(0, -3)$ to $(4, 0)$, $\Delta y = 3$ and $\Delta x = 4$, matching $\tfrac{3}{4}$.

### Example 3: Parallel and perpendicular lines

Using the line $y = \tfrac{3}{4}x - 3$ from Example 2:

(a) The parallel line through $(0, 2)$ keeps the slope $\tfrac{3}{4}$: $y = \tfrac{3}{4}x + 2$.

(b) The perpendicular line through $(6, 1)$ has slope $-\tfrac{4}{3}$. Point-slope form: $y - 1 = -\tfrac{4}{3}(x - 6)$, so $y = -\tfrac{4}{3}x + 8 + 1 = -\tfrac{4}{3}x + 9$.

Check: $\tfrac{3}{4} \cdot \left(-\tfrac{4}{3}\right) = -1$, and $-\tfrac{4}{3}(6) + 9 = 1$, so the line passes through $(6, 1)$.

### Example 4: Direct variation

Suppose the cost $y$ of bulk rice varies directly with its weight $x$ in pounds, and 4 pounds cost \$12. (Illustrative prices.)

1. Find $k$: $12 = k \cdot 4$, so $k = 3$ dollars per pound.
2. Model: $y = 3x$.
3. Predict: 10 pounds cost $y = 3(10) = 30$ dollars.

The slope $3$ is the rate of change: each extra pound adds \$3.

## Common misconceptions and boundary cases

- **Run over rise.** Slope is change in $y$ divided by change in $x$, not the other way around.
- **Mixing the order of subtraction.** If you compute $y_2 - y_1$, you must also compute $x_2 - x_1$ in the same order. Mixing orders flips the sign of the slope.
- **Zero versus undefined.** The line $y = -2$ is horizontal with slope $0$. The line $x = 3$ is vertical with undefined slope, and it is not a function.
- **Perpendicular means only "change the sign."** The perpendicular slope to $2$ is $-\tfrac{1}{2}$, not $-2$. Take the reciprocal **and** change the sign.
- **Calling every line direct variation.** $y = 2x + 3$ is linear but is not direct variation, because it does not pass through the origin. Direct variation requires $b = 0$.

## Practice

1. Find the slope of the line through $(1, -3)$ and $(5, 9)$.
2. Write the equation of the line through $(-1, 4)$ with slope $\tfrac{1}{2}$ in slope-intercept form.
3. Rewrite $2x + 5y = 10$ in slope-intercept form and give both intercepts.
4. Are $y = 3x - 1$ and $6x - 2y = 8$ parallel, perpendicular, or neither?
5. Write the equation of the line through $(2, -1)$ perpendicular to $y = -2x + 7$.
6. Find the slope and the equation of the line through $(3, 2)$ and $(3, -5)$.
7. $y$ varies directly with $x$, and $y = -15$ when $x = 5$. Find $y$ when $x = 8$.

<details>
<summary>Answer key and self-check</summary>

1. $m = \dfrac{9 - (-3)}{5 - 1} = \dfrac{12}{4} = 3$.
2. $y - 4 = \tfrac{1}{2}(x + 1)$, so $y = \tfrac{1}{2}x + \tfrac{9}{2}$.
3. $5y = -2x + 10$, so $y = -\tfrac{2}{5}x + 2$. Intercepts: $(5, 0)$ and $(0, 2)$.
4. The second line becomes $y = 3x - 4$. Both slopes are $3$ and the intercepts differ, so the lines are parallel.
5. Perpendicular slope is $\tfrac{1}{2}$: $y + 1 = \tfrac{1}{2}(x - 2)$, so $y = \tfrac{1}{2}x - 2$.
6. $\Delta x = 0$, so the slope is undefined. The line is vertical: $x = 3$.
7. $k = -3$, so $y = -3x$ and $y = -24$ when $x = 8$.

Self-check method: substitute each given point into your final equation. If a point does not satisfy the equation, recheck the slope first.

</details>

## Where this fits

Linear functions connect equations, graphs, and rates of change across the [Algebra I course](/subject/algebra-i). Next, [14.6 - Systems of Equations](/146-systems-of-equations) asks where two lines meet, which can be read from their graphs or found algebraically.

## Sources

- OpenStax, *Elementary Algebra 2e*, [4.4 Understand Slope of a Line](https://openstax.org/books/elementary-algebra-2e/pages/4-4-understand-slope-of-a-line)
- OpenStax, *Elementary Algebra 2e*, [4.5 Use the Slope-Intercept Form of an Equation of a Line](https://openstax.org/books/elementary-algebra-2e/pages/4-5-use-the-slope-intercept-form-of-an-equation-of-a-line)
- OpenStax, *Elementary Algebra 2e*, [4.6 Find the Equation of a Line](https://openstax.org/books/elementary-algebra-2e/pages/4-6-find-the-equation-of-a-line)

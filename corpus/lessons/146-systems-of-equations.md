---
title: "14.6 - Systems of Equations"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.6"
type: chapter
objectives:
  - "Verify whether an ordered pair is a solution of a system of two linear equations"
  - "Solve systems by graphing, substitution, and elimination and choose an efficient method"
  - "Identify systems with no solution or infinitely many solutions algebraically and graphically"
  - "Model and solve ticket, mixture, and rate problems with a system"
open_source: true
---

# 14.6 - Systems of Equations

A system of linear equations is two or more equations that must be true at the same time. For two equations in two variables, a solution is an ordered pair $(x, y)$ that satisfies both, which is a point where the two lines meet. This lesson covers the graphing, substitution, and elimination methods, special cases, and applications.

## Prerequisites

You should be able to solve multi-step linear equations ([14.2 - Linear Equations](/142-linear-equations)) and graph a line and find its slope ([14.5 - Linear Functions & Graphing](/145-linear-functions-graphing)).

## Learning objectives

By the end of this lesson you should be able to:

1. Check whether a given ordered pair solves a system.
2. Solve a system by graphing and explain the limits of reading a graph.
3. Solve a system by substitution and by elimination.
4. Recognize a system with no solution or infinitely many solutions from its algebra and from its slopes.
5. Set up and solve a system from a word problem, and check the answer in context.

## Core ideas

### What a solution means

Each linear equation describes a line. A point is a solution of the system only if it lies on **both** lines. Two lines in a plane can meet in exactly one point, never meet (parallel), or be the same line, so a linear system has exactly one solution, no solution, or infinitely many solutions.

### Three methods

- **Graphing:** draw both lines and read the intersection. It shows the meaning clearly but is only exact when the intersection falls on easy-to-read coordinates.
- **Substitution:** solve one equation for one variable and substitute that expression into the other equation. It is efficient when a variable already has a coefficient of $1$ or $-1$.
- **Elimination:** add or subtract the equations, after multiplying if needed, so one variable cancels. It is efficient when both equations are in standard form $Ax + By = C$.

All three methods give the same answer. Choosing well saves work and avoids fractions.

### Special systems

If the variables cancel and you reach a false statement such as $0 = 2$, the lines are parallel and there is **no solution**. If you reach a true statement such as $0 = 0$, the equations describe the same line and there are **infinitely many solutions**. Comparing slopes and intercepts confirms this: equal slopes with different intercepts mean parallel lines; equal slopes and equal intercepts mean the same line.

## Worked examples

### Example 1: Substitution

Solve the system $y = 2x - 3$ and $3x + 2y = 15$.

1. The first equation already gives $y$. Substitute $2x - 3$ for $y$ in the second: $3x + 2(2x - 3) = 15$.
2. Distribute and combine: $3x + 4x - 6 = 15$, so $7x = 21$ and $x = 3$.
3. Back-substitute: $y = 2(3) - 3 = 3$.

Solution: $(3, 3)$. Check in both original equations: $2(3) - 3 = 3$ and $3(3) + 2(3) = 15$.

### Example 2: Elimination with two multipliers

Solve $2x + 3y = 7$ and $5x - 2y = 8$.

1. Choose to eliminate $y$. The least common multiple of $3$ and $2$ is $6$. Multiply the first equation by $2$ and the second by $3$:
   $$4x + 6y = 14 \qquad 15x - 6y = 24.$$
2. Add the equations: $19x = 38$, so $x = 2$.
3. Substitute into the first original equation: $2(2) + 3y = 7$, so $3y = 3$ and $y = 1$.

Solution: $(2, 1)$. Check the second equation: $5(2) - 2(1) = 8$.

### Example 3: No solution and infinitely many solutions

(a) $x + 2y = 4$ and $2x + 4y = 10$. Multiply the first by $-2$: $-2x - 4y = -8$. Adding to the second gives $0 = 2$, which is false. No solution. In slope-intercept form the lines are $y = -\tfrac{1}{2}x + 2$ and $y = -\tfrac{1}{2}x + \tfrac{5}{2}$: same slope, different intercepts, so they are parallel.

(b) $x + 2y = 4$ and $3x + 6y = 12$. The second equation is exactly $3$ times the first. Elimination gives $0 = 0$. Every point on the line $x + 2y = 4$ is a solution, such as $(0, 2)$ and $(4, 0)$.

### Example 4: A ticket problem

A school play sells adult tickets for \$8 and student tickets for \$5. One night, 200 tickets bring in \$1,315. How many of each were sold? (Illustrative numbers.)

1. Define variables: $a$ adult tickets, $s$ student tickets.
2. Count equation: $a + s = 200$. Money equation: $8a + 5s = 1315$.
3. Substitute $s = 200 - a$: $8a + 5(200 - a) = 1315$, so $3a + 1000 = 1315$ and $a = 105$.
4. Then $s = 200 - 105 = 95$.

Check in context: $105 + 95 = 200$ tickets, and $8(105) + 5(95) = 840 + 475 = 1315$ dollars.

## Common misconceptions and boundary cases

- **Stopping after one variable.** A system's solution is an ordered pair. Finding $x = 3$ is only half of the answer.
- **Multiplying only one side.** When scaling an equation for elimination, every term on both sides must be multiplied, including the constant.
- **Subtracting signs incorrectly.** When subtracting one equation from another, subtract every term. Many students prefer to multiply by $-1$ and then add, which avoids this error.
- **Trusting a graph too much.** For $y = 2x - 1$ and $y = -x + 3$, a hand-drawn graph might suggest an intersection near $(1.5, 2)$. Solving $2x - 1 = -x + 3$ gives the exact solution $\left(\tfrac{4}{3}, \tfrac{5}{3}\right)$. Confirm graphical answers algebraically.
- **Reporting $(0, 0)$ for special systems.** When the variables cancel, the result is "no solution" or "infinitely many solutions," not the origin.

## Practice

1. Solve by substitution: $x = 4y + 1$ and $2x - 5y = 8$.
2. Solve by elimination: $3x + 4y = 6$ and $3x - 2y = -12$.
3. Solve by elimination: $4x + 3y = 1$ and $3x + 2y = 0$.
4. Classify each system: (a) $y = -x + 5$ and $2x + 2y = 10$; (b) $y = 3x + 1$ and $y = 3x - 2$.
5. A chemist mixes a 30% acid solution with a 60% acid solution to make 12 liters of a 50% solution. How many liters of each are needed? (Illustrative problem.)
6. A boat travels 24 miles downstream in 2 hours and returns upstream in 3 hours. Find the boat's speed in still water and the speed of the current.

<details>
<summary>Answer key and self-check</summary>

1. $2(4y + 1) - 5y = 8$, so $3y = 6$ and $y = 2$; then $x = 9$. Solution $(9, 2)$. Check: $18 - 10 = 8$.
2. Subtract the second equation from the first: $6y = 18$, so $y = 3$; then $3x + 12 = 6$ gives $x = -2$. Solution $(-2, 3)$. Check: $-6 - 6 = -12$.
3. Multiply by $2$ and $3$: $8x + 6y = 2$ and $9x + 6y = 0$. Subtracting gives $-x = 2$, so $x = -2$; then $3(-2) + 2y = 0$ gives $y = 3$. Solution $(-2, 3)$. Check: $-8 + 9 = 1$.
4. (a) Substituting gives $10 = 10$: infinitely many solutions (same line). (b) Same slope, different intercepts: no solution.
5. $x + y = 12$ and $0.30x + 0.60y = 0.50(12) = 6$. Substitute $y = 12 - x$: $7.2 - 0.30x = 6$, so $x = 4$ and $y = 8$. Use 4 L of the 30% solution and 8 L of the 60% solution. Check: $1.2 + 4.8 = 6$ L of acid.
6. Downstream rate $24 \div 2 = 12$ mi/h, upstream rate $24 \div 3 = 8$ mi/h. With boat speed $b$ and current $c$: $b + c = 12$ and $b - c = 8$. Adding gives $b = 10$, so $c = 2$.

Self-check method: substitute the ordered pair into **both** original equations. For word problems, also check that the numbers make sense (for example, quantities are not negative).

</details>

## Where this fits

Systems tie together everything about lines in the [Algebra I course](/subject/algebra-i). Next, [14.7 - Exponents & Polynomials](/147-exponents-polynomials) moves beyond linear expressions to powers and polynomials, which lead to the curved graphs of [14.8 - Factoring & Quadratics](/148-factoring-quadratics).

## Sources

- OpenStax, *Elementary Algebra 2e*, [5.1 Solve Systems of Equations by Graphing](https://openstax.org/books/elementary-algebra-2e/pages/5-1-solve-systems-of-equations-by-graphing)
- OpenStax, *Elementary Algebra 2e*, [5.2 Solving Systems of Equations by Substitution](https://openstax.org/books/elementary-algebra-2e/pages/5-2-solving-systems-of-equations-by-substitution)
- OpenStax, *Elementary Algebra 2e*, [5.3 Solve Systems of Equations by Elimination](https://openstax.org/books/elementary-algebra-2e/pages/5-3-solve-systems-of-equations-by-elimination)
- OpenStax, *Elementary Algebra 2e*, [5.4 Solve Applications with Systems of Equations](https://openstax.org/books/elementary-algebra-2e/pages/5-4-solve-applications-with-systems-of-equations)

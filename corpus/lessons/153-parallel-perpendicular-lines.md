---
title: "15.3 - Parallel & Perpendicular Lines"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.3"
type: chapter
objectives:
  - "Identify corresponding, alternate interior, alternate exterior, and same-side interior angles formed by a transversal"
  - "Use parallel-line angle relationships to find unknown angle measures and solve for variables"
  - "Use converse theorems to decide whether two lines are parallel"
  - "Use slopes to write equations of parallel and perpendicular lines and find the distance from a point to a line"
open_source: true
---

# 15.3 - Parallel & Perpendicular Lines

When a line crosses two parallel lines, it creates eight angles that come in only two sizes. That fact lets you find every angle from one measurement, and its converse lets you prove lines are parallel from angle measures alone. This lesson develops those relationships, then translates parallelism and perpendicularity into slopes so they can be checked and constructed in the coordinate plane.

## Prerequisites

From [15.1 - Foundations of Geometry](/151-foundations-of-geometry) you need linear pairs and vertical angles; from [15.2 - Reasoning & Proof](/152-reasoning-proof) you need converses and two-column proofs. You should also know how to compute slope and write a line in slope-intercept or point-slope form, as in [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing).

## Learning objectives

By the end of this lesson you should be able to:

1. Name the angle pairs formed by a transversal and say which are congruent and which are supplementary when the lines are parallel.
2. Solve for unknown angles and variables in diagrams with parallel lines.
3. Use the converse theorems to decide whether two lines cut by a transversal are parallel.
4. Decide whether two lines are parallel, perpendicular, or neither from their slopes, and write such lines through a given point.
5. Find the distance from a point to a line by locating the foot of the perpendicular.

## Core ideas

### Lines in a plane and in space

**Parallel lines** are coplanar lines that never intersect ($\ell \parallel m$). **Perpendicular lines** intersect to form right angles ($\ell \perp m$). In three dimensions, two lines that are not coplanar, and therefore neither intersect nor are parallel, are **skew**.

The **Parallel Postulate** (Playfair's form of Euclid's fifth postulate): through a point not on a line, there is exactly one line parallel to the given line. Similarly, through a point not on a line there is exactly one line perpendicular to it.

### Angles formed by a transversal

A **transversal** is a line that intersects two other coplanar lines at different points. Picture two horizontal lines crossed by a slanted line. Four angles form at the top intersection and four at the bottom. Between the two lines is the *interior*; outside them is the *exterior*.

- **Corresponding angles** occupy the same position at each intersection (for example, both upper-left).
- **Alternate interior angles** are between the lines on opposite sides of the transversal.
- **Alternate exterior angles** are outside the lines on opposite sides of the transversal.
- **Same-side (consecutive) interior angles** are between the lines on the same side of the transversal.

### Theorems when the lines are parallel

If two parallel lines are cut by a transversal, then:

- corresponding angles are congruent (Corresponding Angles Postulate);
- alternate interior angles are congruent;
- alternate exterior angles are congruent;
- same-side interior angles are supplementary.

Euclid proves the alternate-angle and same-side results from his fifth postulate in *Elements* I.29. Because each angle is either congruent or supplementary to every other angle in the figure, all eight angles take only two values, $\theta$ and $180^\circ - \theta$.

### Converses: proving lines parallel

Each statement above has a true converse. If a transversal makes corresponding angles congruent, alternate interior angles congruent, alternate exterior angles congruent, or same-side interior angles supplementary, then the lines are parallel (*Elements* I.27–I.28). Also, two lines perpendicular to the same line in a plane are parallel.

### Slope criteria

For nonvertical lines with slopes $m_1$ and $m_2$:

- the lines are parallel exactly when $m_1 = m_2$ (and they are distinct);
- the lines are perpendicular exactly when $m_1 m_2 = -1$, so each slope is the negative reciprocal of the other.

Vertical lines (undefined slope) are parallel to each other and perpendicular to horizontal lines (slope $0$); the product rule does not apply to that pair.

### Distance from a point to a line

The distance from a point to a line is the length of the perpendicular segment from the point to the line; every other segment to the line is longer, because it is the hypotenuse of a right triangle whose leg is the perpendicular. For the line $Ax + By + C = 0$ and the point $(x_0, y_0)$, this distance equals

$$d = \frac{\lvert Ax_0 + By_0 + C \rvert}{\sqrt{A^2 + B^2}}.$$

## Worked examples

### Example 1: All eight angles from one

Parallel lines $\ell$ and $m$ are cut by transversal $t$. The upper-left angle at line $\ell$ measures $115^\circ$.

1. Its vertical angle (lower-right at $\ell$) is $115^\circ$; the two angles forming linear pairs with it are $180 - 115 = 65^\circ$.
2. The corresponding angle at $m$ (upper-left at $m$) is $115^\circ$.
3. The lower-right angle at $\ell$ ($115^\circ$, interior) and the upper-left angle at $m$ ($115^\circ$, interior) are alternate interior angles, consistent with the theorem.
4. The same-side interior partner of the $115^\circ$ interior angle is $65^\circ$, and $115 + 65 = 180$. Four angles are $115^\circ$ and four are $65^\circ$.

### Example 2: Solving with alternate interior angles

With $\ell \parallel m$, a pair of alternate interior angles measure $(3x + 15)^\circ$ and $(5x - 25)^\circ$.

1. Alternate interior angles are congruent: $3x + 15 = 5x - 25$.
2. $40 = 2x$, so $x = 20$.
3. Each angle is $3(20) + 15 = 75^\circ$; check $5(20) - 25 = 75$.

### Example 3: When are the lines parallel?

Same-side interior angles measure $(4x + 6)^\circ$ and $(6x - 16)^\circ$. For what value of $x$ are the lines parallel?

1. By the converse, the lines are parallel exactly when the angles are supplementary: $(4x + 6) + (6x - 16) = 180$.
2. $10x - 10 = 180$, so $x = 19$.
3. The angles are $82^\circ$ and $98^\circ$. For any other $x$ the sum is not $180^\circ$ and the lines meet on one side.

### Example 4: Parallel and perpendicular lines through a point

A line passes through $(1, 2)$ and $(4, 8)$. Write the lines through $(-1, 3)$ that are parallel and perpendicular to it.

1. Slope: $\tfrac{8 - 2}{4 - 1} = 2$.
2. Parallel line: slope $2$. $y - 3 = 2(x + 1)$, so $y = 2x + 5$.
3. Perpendicular line: slope $-\tfrac{1}{2}$, since $2 \cdot \left(-\tfrac{1}{2}\right) = -1$. $y - 3 = -\tfrac{1}{2}(x + 1)$, so $y = -\tfrac{1}{2}x + \tfrac{5}{2}$.
4. Check: both lines contain $(-1, 3)$: $2(-1) + 5 = 3$ and $\tfrac{1}{2} + \tfrac{5}{2} = 3$.

### Example 5: Distance from a point to a line

Find the distance from $P(4, -1)$ to the line $y = 2x + 1$.

1. The perpendicular through $P$ has slope $-\tfrac{1}{2}$: $y + 1 = -\tfrac{1}{2}(x - 4)$, so $y = -\tfrac{1}{2}x + 1$.
2. Intersect: $2x + 1 = -\tfrac{1}{2}x + 1$ gives $x = 0$, so the foot is $F(0, 1)$.
3. $PF = \sqrt{(4 - 0)^2 + (-1 - 1)^2} = \sqrt{20} = 2\sqrt{5} \approx 4.47$.
4. Formula check: the line is $2x - y + 1 = 0$, and $\dfrac{\lvert 2(4) - (-1) + 1 \rvert}{\sqrt{4 + 1}} = \dfrac{10}{\sqrt{5}} = 2\sqrt{5}$.

## Common misconceptions and boundary cases

- **Using the angle theorems without parallel lines.** If $\ell$ and $m$ are not parallel, corresponding angles are not congruent. You must know the lines are parallel, or be proving it with a converse.
- **Calling same-side interior angles congruent.** They are supplementary. They are congruent only in the special case where both are $90^\circ$.
- **"Lines that never meet are parallel."** In space, nonintersecting lines can be skew. Parallel lines must also be coplanar.
- **Opposite instead of negative reciprocal.** A line perpendicular to slope $3$ has slope $-\tfrac{1}{3}$, not $-3$.
- **Forgetting vertical and horizontal lines.** $x = 3$ and $y = -2$ are perpendicular even though $0 \cdot (\text{undefined})$ is not $-1$.
- **Measuring distance along a slanted segment.** The distance to a line uses the perpendicular segment; any other segment is longer.

## Practice

1. Parallel lines are cut by a transversal, and interior angle $\angle 1$ measures $48^\circ$. Find (a) the angle corresponding to $\angle 1$, (b) an angle forming a linear pair with $\angle 1$, and (c) the same-side interior partner of $\angle 1$.
2. Alternate exterior angles measure $(7x - 9)^\circ$ and $(4x + 27)^\circ$, and the lines are parallel. Find $x$ and the angle.
3. Same-side interior angles measure $(3x + 4)^\circ$ and $(5x - 8)^\circ$. What value of $x$ makes the lines parallel, and what are the angles?
4. Are the line through $(0, 0)$ and $(2, 3)$ and the line through $(1, -1)$ and $(4, -3)$ parallel, perpendicular, or neither?
5. Write an equation of the line through $(2, -3)$ perpendicular to $y = 4x - 1$.
6. Find the distance from $(3, 5)$ to the line $y = x$, and give the foot of the perpendicular.
7. Explain why the lines $x = 3$ and $y = -2$ are perpendicular.

<details>
<summary>Answer key and self-check</summary>

1. (a) $48^\circ$; (b) $132^\circ$; (c) $132^\circ$.
2. $7x - 9 = 4x + 27$ gives $x = 12$; each angle is $75^\circ$.
3. $(3x + 4) + (5x - 8) = 180$ gives $8x = 184$, so $x = 23$; the angles are $73^\circ$ and $107^\circ$.
4. Slopes $\tfrac{3}{2}$ and $\tfrac{-3 - (-1)}{4 - 1} = -\tfrac{2}{3}$; their product is $-1$, so the lines are perpendicular.
5. Slope $-\tfrac{1}{4}$: $y + 3 = -\tfrac{1}{4}(x - 2)$, so $y = -\tfrac{1}{4}x - \tfrac{5}{2}$.
6. The perpendicular through $(3, 5)$ is $y = -x + 8$, meeting $y = x$ at $(4, 4)$. Distance $\sqrt{1^2 + 1^2} = \sqrt{2} \approx 1.41$. Formula: $\tfrac{\lvert 3 - 5 \rvert}{\sqrt{2}} = \sqrt{2}$.
7. $x = 3$ is vertical and $y = -2$ is horizontal, so they meet at $(3, -2)$ at a right angle.

Self-check method: in an angle diagram, every angle must equal either $\theta$ or $180^\circ - \theta$; for slopes, multiply them and look for $-1$; for distances, confirm the foot of the perpendicular lies on both lines.

</details>

## Where this fits

This lesson follows [15.2 - Reasoning & Proof](/152-reasoning-proof) in the [Geometry course](/subject/geometry). The alternate interior angle theorem is the key step in proving the triangle angle sum in [15.4 - Triangles](/154-triangles), and parallel lines drive the proportionality theorems in [15.5 - Similarity & Proportions](/155-similarity-proportions). For more on slope and systems of lines, see [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing) and [14.6 - Systems of Equations](/146-systems-of-equations).

## Sources

- OpenStax, *Contemporary Mathematics*, [10.2 Angles](https://openstax.org/books/contemporary-mathematics/pages/10-2-angles)
- OpenStax, *Intermediate Algebra 2e*, [3.2 Slope of a Line](https://openstax.org/books/intermediate-algebra-2e/pages/3-2-slope-of-a-line)
- OpenStax, *Intermediate Algebra 2e*, [3.3 Find the Equation of a Line](https://openstax.org/books/intermediate-algebra-2e/pages/3-3-find-the-equation-of-a-line)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition I.27](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI27.html), [Proposition I.28](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI28.html), and [Proposition I.29](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI29.html)

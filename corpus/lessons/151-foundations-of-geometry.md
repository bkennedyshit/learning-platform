---
title: "15.1 - Foundations of Geometry"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.1"
type: chapter
objectives:
  - "Distinguish undefined terms, definitions, postulates, and theorems and name points, lines, rays, segments, and planes with correct notation"
  - "Use the Segment Addition and Angle Addition Postulates to write and solve equations"
  - "Classify angles and angle pairs, including complementary, supplementary, linear pairs, and vertical angles"
  - "Compute distances and midpoints in the coordinate plane and find a missing endpoint from a midpoint"
open_source: true
---

# 15.1 - Foundations of Geometry

Geometry is built like a program: a few primitive objects that are never defined, a short list of rules accepted without proof, and everything else derived from them. This first lesson sets up that vocabulary. You will learn the names and notation for the basic figures, the two "addition" postulates that turn diagrams into equations, the standard angle relationships, and the distance and midpoint formulas that connect geometry to the coordinate plane.

## Prerequisites

You should be able to solve one-variable linear equations such as $5x + 2 = 27$ (see [14.2 - Linear Equations](/142-linear-equations)), plot points in the coordinate plane (see [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing)), and simplify square roots such as $\sqrt{100} = 10$. Knowing the statement of the Pythagorean theorem, $a^2 + b^2 = c^2$, helps with the distance formula; it is proved in [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry).

## Learning objectives

By the end of this lesson you should be able to:

1. Explain the difference between an undefined term, a definition, a postulate, and a theorem, and give an example of each.
2. Name points, lines, rays, segments, and planes with correct notation, and identify collinear and coplanar points.
3. Set up and solve equations using the Segment Addition Postulate, the Angle Addition Postulate, midpoints, and bisectors.
4. Classify an angle as acute, right, obtuse, or straight, and find unknown measures in complementary, supplementary, linear-pair, and vertical-angle relationships.
5. Use the distance and midpoint formulas, including working backward from a midpoint to a missing endpoint.

## Core ideas

### Undefined terms

Every definition uses other words, so a deductive system has to start somewhere. Geometry starts with three **undefined terms** that are described rather than defined:

- A **point** marks a location and has no size. It is named with a capital letter, such as $A$. Euclid described it as "that which has no part."
- A **line** is straight, has no thickness, and extends without end in both directions. It is named by two of its points, $\overleftrightarrow{AB}$, or by a lowercase letter such as $\ell$.
- A **plane** is a flat surface with no thickness that extends without end. It is named by three points not on one line, or by a capital script letter.

Points on the same line are **collinear**; points in the same plane are **coplanar**.

### Defined terms

Using the undefined terms, we can define new figures precisely:

- A **segment** $\overline{AB}$ consists of endpoints $A$ and $B$ and all points of the line between them. Its length is written $AB$ (no bar).
- A **ray** $\overrightarrow{AB}$ starts at endpoint $A$ and extends through $B$ without end. The endpoint is always written first, so $\overrightarrow{AB}$ and $\overrightarrow{BA}$ are different rays.
- **Opposite rays** share an endpoint and point in opposite directions along one line.
- An **angle** is formed by two rays with a common endpoint, the **vertex**. $\angle ABC$ has vertex $B$, the middle letter.

Two segments are **congruent**, $\overline{AB} \cong \overline{CD}$, when their lengths are equal, $AB = CD$. Congruence relates figures; equality relates numbers.

### Postulates and theorems

A **postulate** (axiom) is accepted without proof. A **theorem** is proved from postulates, definitions, and earlier theorems. Some basic postulates:

- Through any two points there is exactly one line.
- If two distinct lines intersect, they intersect in exactly one point.
- Through any three noncollinear points there is exactly one plane.
- If two distinct planes intersect, they intersect in a line.
- **Segment Addition Postulate:** if $B$ is between $A$ and $C$ on a line, then $AB + BC = AC$.
- **Angle Addition Postulate:** if point $D$ is in the interior of $\angle ABC$, then $m\angle ABD + m\angle DBC = m\angle ABC$.

The **midpoint** of $\overline{AB}$ divides it into two congruent segments. A ray that divides an angle into two congruent angles is the **angle bisector**.

### Angles and angle pairs

By measure, an angle is **acute** ($0^\circ \lt m \lt 90^\circ$), **right** ($90^\circ$), **obtuse** ($90^\circ \lt m \lt 180^\circ$), or **straight** ($180^\circ$).

- **Complementary** angles have measures that add to $90^\circ$; **supplementary** angles add to $180^\circ$. Neither has to be adjacent.
- A **linear pair** is two adjacent angles whose outer sides are opposite rays. A linear pair is always supplementary.
- **Vertical angles** are the non-adjacent angles formed by two intersecting lines. Vertical angles are congruent (Euclid, *Elements* I.15), because each one forms a linear pair with the same angle between them.

### The coordinate plane

For points $(x_1, y_1)$ and $(x_2, y_2)$:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}, \qquad M = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right).$$

Visually, the distance formula is the Pythagorean theorem applied to a right triangle whose legs are the horizontal change and the vertical change. The midpoint averages the coordinates, so it sits halfway along each direction.

## Worked examples

### Example 1: Segment addition

$B$ is between $A$ and $C$. $AB = 2x + 3$, $BC = 3x - 1$, and $AC = 27$. Find $AB$ and $BC$.

1. Segment Addition: $(2x + 3) + (3x - 1) = 27$.
2. Combine like terms: $5x + 2 = 27$, so $5x = 25$ and $x = 5$.
3. Substitute: $AB = 2(5) + 3 = 13$ and $BC = 3(5) - 1 = 14$.
4. Check: $13 + 14 = 27$.

### Example 2: A linear pair and its vertical angle

Lines $\ell$ and $m$ intersect, forming $\angle 1$ and $\angle 2$ as a linear pair with $m\angle 1 = 3x + 10$ and $m\angle 2 = 5x - 6$. Find both angles and the angle vertical to $\angle 1$.

1. A linear pair is supplementary: $(3x + 10) + (5x - 6) = 180$.
2. $8x + 4 = 180$, so $x = 22$.
3. $m\angle 1 = 3(22) + 10 = 76^\circ$ and $m\angle 2 = 5(22) - 6 = 104^\circ$. Check: $76 + 104 = 180$.
4. The angle vertical to $\angle 1$ is congruent to it, so it also measures $76^\circ$.

### Example 3: Angle bisector

$\overrightarrow{BD}$ bisects $\angle ABC$, $m\angle ABD = 4x - 2$, and $m\angle DBC = 2x + 18$. Find $m\angle ABC$.

1. A bisector makes the two parts equal: $4x - 2 = 2x + 18$, so $x = 10$.
2. Each part is $4(10) - 2 = 38^\circ$.
3. Angle Addition: $m\angle ABC = 38 + 38 = 76^\circ$. The angle is acute.

### Example 4: Distance and midpoint

Find the length and midpoint of $\overline{AB}$ with $A(-2, 3)$ and $B(4, -5)$.

1. Horizontal change $4 - (-2) = 6$; vertical change $-5 - 3 = -8$.
2. $AB = \sqrt{6^2 + (-8)^2} = \sqrt{36 + 64} = \sqrt{100} = 10$.
3. $M = \left(\tfrac{-2 + 4}{2}, \tfrac{3 + (-5)}{2}\right) = (1, -1)$.
4. Check: $M$ to $B$ is $\sqrt{3^2 + 4^2} = 5$, exactly half of $10$.

### Example 5: Missing endpoint

$M(3, -1)$ is the midpoint of $\overline{PQ}$ and $P = (-1, 4)$. Find $Q$.

1. From $\tfrac{-1 + x}{2} = 3$: $x = 6 - (-1) = 7$.
2. From $\tfrac{4 + y}{2} = -1$: $y = -2 - 4 = -6$.
3. $Q = (7, -6)$. Check: $\left(\tfrac{-1 + 7}{2}, \tfrac{4 + (-6)}{2}\right) = (3, -1)$.

## Common misconceptions and boundary cases

- **Reading a diagram as proof.** A figure can suggest that two segments are equal or that an angle is right, but you may only use what is given, marked, or proved. Collinearity and betweenness are usually safe to read from a diagram; measures are not.
- **Segment Addition without betweenness.** $AB + BC = AC$ requires $B$ to lie on $\overline{AC}$. If $A$, $B$, $C$ form a triangle, then $AB + BC \gt AC$.
- **Mixing up ray names.** $\overrightarrow{AB}$ begins at $A$. Reversing the letters names a different ray, while $\overleftrightarrow{AB}$ and $\overleftrightarrow{BA}$ are the same line.
- **Writing $\overline{AB} = \overline{CD}$.** Segments are congruent ($\cong$); their lengths are equal ($=$).
- **Assuming complementary or supplementary angles must touch.** A $30^\circ$ angle in one corner of the page and a $60^\circ$ angle in another are still complementary.
- **Subtracting in the midpoint formula.** The midpoint averages ($x_1 + x_2$); the distance formula subtracts. A distance is never negative.

## Practice

1. How many lines contain two given points? How many planes contain three given noncollinear points?
2. $M$ is the midpoint of $\overline{AB}$, $AM = 5x - 8$, and $MB = 3x + 6$. Find $x$ and $AB$.
3. Two vertical angles measure $(7x - 20)^\circ$ and $(4x + 25)^\circ$. Find each angle and the measure of an angle that forms a linear pair with one of them.
4. The supplement of an angle is $30^\circ$ more than twice its complement. Find the angle.
5. Find the distance and the midpoint between $(-3, -1)$ and $(2, 11)$.
6. $M(-2, 5)$ is the midpoint of $\overline{AB}$ and $A = (4, 1)$. Find $B$.
7. True or false: if $AB + BC = AC$ for three points on a plane, then $B$ lies on $\overline{AC}$. Explain.

<details>
<summary>Answer key and self-check</summary>

1. Exactly one line; exactly one plane.
2. $5x - 8 = 3x + 6$ gives $x = 7$; $AM = MB = 27$, so $AB = 54$.
3. $7x - 20 = 4x + 25$ gives $x = 15$; each vertical angle is $85^\circ$, and a linear-pair partner is $180 - 85 = 95^\circ$.
4. Let the angle be $a$: $180 - a = 2(90 - a) + 30$, so $180 - a = 210 - 2a$ and $a = 30^\circ$. Check: supplement $150^\circ$, complement $60^\circ$, and $2(60) + 30 = 150$.
5. $d = \sqrt{5^2 + 12^2} = \sqrt{169} = 13$; midpoint $\left(-\tfrac{1}{2}, 5\right)$.
6. $B = (2(-2) - 4,\ 2(5) - 1) = (-8, 9)$.
7. True. If $B$ were not on $\overline{AC}$, then either $A$, $B$, $C$ would form a triangle, where $AB + BC \gt AC$, or $B$ would be on the line beyond $A$ or $C$, where $AB + BC$ also exceeds $AC$.

Self-check method: substitute your $x$ back into every expression, confirm the lengths or angles satisfy the stated relationship (sum, equality, or $90^\circ$/$180^\circ$), and for coordinate answers recompute the midpoint or distance from your result.

</details>

## Where this fits

This is the first lesson in the [Geometry course](/subject/geometry). Next, [15.2 - Reasoning & Proof](/152-reasoning-proof) turns the postulates and angle-pair facts here into formal two-column proofs. The distance and midpoint formulas return in [15.4 - Triangles](/154-triangles) for triangle centers, in [15.7 - Circles](/157-circles) for circle equations, and in [16.6 - Conic Sections](/166-conic-sections).

## Sources

- OpenStax, *Contemporary Mathematics*, [10.1 Points, Lines, and Planes](https://openstax.org/books/contemporary-mathematics/pages/10-1-points-lines-and-planes)
- OpenStax, *Contemporary Mathematics*, [10.2 Angles](https://openstax.org/books/contemporary-mathematics/pages/10-2-angles)
- OpenStax, *Intermediate Algebra 2e*, [11.1 Distance and Midpoint Formulas; Circles](https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Book I definitions and postulates](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/bookI.html) and [Proposition I.15](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI15.html)

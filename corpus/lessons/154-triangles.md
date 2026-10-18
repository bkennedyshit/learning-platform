---
title: "15.4 - Triangles"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.4"
type: chapter
objectives:
  - "Apply the Triangle Sum, Exterior Angle, and Triangle Inequality theorems to find or bound unknown measures"
  - "Choose the correct congruence criterion (SSS, SAS, ASA, AAS, HL) and explain why SSA and AAA fail"
  - "Write congruence proofs that use CPCTC and the Isosceles Triangle Theorem"
  - "Locate the centroid and circumcenter of a triangle and relate each triangle center to the segments that define it"
open_source: true
---

# 15.4 - Triangles

Triangles are the rigid building blocks of geometry: once three side lengths are fixed, the shape cannot flex. That rigidity is why triangle congruence is the main tool for proving that segments or angles are equal. This lesson covers the angle and side facts every triangle obeys, the five congruence shortcuts and the two look-alikes that fail, isosceles triangles, and the four classical triangle centers.

## Prerequisites

You need the alternate interior angle theorem from [15.3 - Parallel & Perpendicular Lines](/153-parallel-perpendicular-lines), two-column proofs from [15.2 - Reasoning & Proof](/152-reasoning-proof), and the midpoint and distance formulas from [15.1 - Foundations of Geometry](/151-foundations-of-geometry). Solving linear equations and solving a quadratic with the quadratic formula (see [14.8 - Factoring & Quadratics](/148-factoring-quadratics)) are used in the examples.

## Learning objectives

By the end of this lesson you should be able to:

1. Use the Triangle Sum and Exterior Angle theorems to find unknown angles.
2. Decide whether three lengths can form a triangle and give the range of possible third sides.
3. Choose SSS, SAS, ASA, AAS, or HL to prove triangles congruent, and explain with an example why SSA and AAA are not valid tests.
4. Use CPCTC and the Isosceles Triangle Theorem and its converse in proofs and calculations.
5. Compute a centroid from coordinates and identify where each triangle center lies.

## Core ideas

### Classifying triangles

By sides: **scalene** (no congruent sides), **isosceles** (at least two), **equilateral** (all three). By angles: **acute** (three acute angles), **right** (one right angle), **obtuse** (one obtuse angle). In an isosceles triangle the congruent sides are the **legs**, the third side is the **base**, and the angles opposite the legs are the **base angles**.

### Angle and side theorems

- **Triangle Sum Theorem:** the interior angles add to $180^\circ$. Proof idea: draw the line through one vertex parallel to the opposite side. The two new angles at that vertex are alternate interior angles congruent to the other two triangle angles, and the three angles along the line form a straight angle (*Elements* I.32).
- **Exterior Angle Theorem:** an exterior angle equals the sum of the two **remote** (non-adjacent) interior angles. It follows because the exterior angle and its adjacent interior angle form a linear pair.
- **Triangle Inequality Theorem:** the sum of any two side lengths is greater than the third (*Elements* I.20). So if two sides are $a$ and $b$ with $a \le b$, the third side $c$ satisfies $b - a \lt c \lt a + b$.
- In any triangle, the longer side is opposite the larger angle.

### Congruence criteria

Triangles are **congruent** when all corresponding sides and angles are congruent. The order in $\triangle ABC \cong \triangle DEF$ matters: $A$ corresponds to $D$, $B$ to $E$, $C$ to $F$. Five shortcuts are enough:

- **SSS:** three pairs of sides.
- **SAS:** two sides and the angle *between* them.
- **ASA:** two angles and the side between them.
- **AAS:** two angles and a non-included side (the third angle then matches by the Triangle Sum Theorem, reducing to ASA).
- **HL** (right triangles only): hypotenuse and one leg. The Pythagorean theorem forces the other legs to be equal, which reduces to SSS.

After triangles are proved congruent, any remaining pair of corresponding parts is congruent: **CPCTC** (corresponding parts of congruent triangles are congruent).

**Isosceles Triangle Theorem:** if two sides of a triangle are congruent, the angles opposite them are congruent (*Elements* I.5). The converse is also true. An equilateral triangle is therefore equiangular, with each angle $60^\circ$.

### Special segments and centers

| Segment | Definition | Point of concurrency | Property |
|---|---|---|---|
| Median | vertex to midpoint of the opposite side | centroid | divides each median $2:1$ from the vertex; the balance point |
| Perpendicular bisector | perpendicular to a side at its midpoint | circumcenter | equidistant from the three vertices |
| Angle bisector | bisects an interior angle | incenter | equidistant from the three sides |
| Altitude | vertex perpendicular to the line of the opposite side | orthocenter | none of the above in general |

The centroid has coordinates equal to the average of the vertices: $G = \left(\tfrac{x_1 + x_2 + x_3}{3}, \tfrac{y_1 + y_2 + y_3}{3}\right)$. The centroid and incenter are always inside the triangle. The circumcenter and orthocenter lie outside an obtuse triangle; in a right triangle the circumcenter is the midpoint of the hypotenuse and the orthocenter is the right-angle vertex.

## Worked examples

### Example 1: Angle sum and exterior angle

The angles of a triangle are in the ratio $1:2:3$. Then find an exterior angle of a different triangle whose remote interior angles are $40^\circ$ and $65^\circ$.

1. Let the angles be $x$, $2x$, $3x$: $6x = 180$, so $x = 30$. The angles are $30^\circ$, $60^\circ$, $90^\circ$; it is a right triangle.
2. Exterior angle $= 40 + 65 = 105^\circ$. The adjacent interior angle is $180 - 105 = 75^\circ$, and $40 + 65 + 75 = 180$ checks.

### Example 2: Possible third sides

Two sides of a triangle are $5$ and $9$. What lengths can the third side have? Can $3$, $4$, $8$ be a triangle?

1. $9 - 5 \lt c \lt 9 + 5$, so $4 \lt c \lt 14$.
2. For $3, 4, 8$: $3 + 4 = 7$, which is not greater than $8$. The two short sides cannot reach across; no triangle.

### Example 3: A congruence proof with CPCTC

Given $\overline{AB} \cong \overline{CB}$ and $D$ is the midpoint of $\overline{AC}$. Prove $\angle A \cong \angle C$ without quoting the Isosceles Triangle Theorem.

| Statement | Reason |
|---|---|
| 1. $\overline{AB} \cong \overline{CB}$ | Given |
| 2. $D$ is the midpoint of $\overline{AC}$ | Given |
| 3. $\overline{AD} \cong \overline{CD}$ | Definition of midpoint |
| 4. $\overline{BD} \cong \overline{BD}$ | Reflexive property |
| 5. $\triangle ABD \cong \triangle CBD$ | SSS (steps 1, 3, 4) |
| 6. $\angle A \cong \angle C$ | CPCTC |

This is essentially a proof of the Isosceles Triangle Theorem.

### Example 4: Isosceles algebra

The base angles of an isosceles triangle measure $(3x + 5)^\circ$ and $(5x - 15)^\circ$. Find all three angles.

1. Base angles are congruent: $3x + 5 = 5x - 15$, so $x = 10$.
2. Each base angle is $35^\circ$.
3. Vertex angle: $180 - 2(35) = 110^\circ$. The triangle is obtuse.

### Example 5: Centroid and circumcenter from coordinates

Triangle $A(0, 0)$, $B(6, 0)$, $C(0, 9)$.

1. Centroid: $G = \left(\tfrac{0 + 6 + 0}{3}, \tfrac{0 + 0 + 9}{3}\right) = (2, 3)$.
2. Check the $2:1$ ratio on the median from $A$: the midpoint of $\overline{BC}$ is $M(3, 4.5)$. $AG = \sqrt{4 + 9} = \sqrt{13}$ and $GM = \sqrt{1 + 2.25} = \tfrac{\sqrt{13}}{2}$.
3. The angle at $A$ is right, so the circumcenter is the midpoint of hypotenuse $\overline{BC}$, $(3, 4.5)$. Its distance to each vertex is $\sqrt{9 + 20.25} = \sqrt{29.25} \approx 5.41$.

### Example 6: Why SSA fails

Let $m\angle A = 30^\circ$, $AB = 10$, and $BC = 6$, with the $30^\circ$ angle not between the two given sides.

1. Place $A$ at the origin and $B$ at $(10, 0)$. Point $C$ lies on the ray from $A$ at $30^\circ$: $C = \left(\tfrac{\sqrt{3}}{2}t, \tfrac{1}{2}t\right)$ with $t = AC$.
2. Require $BC = 6$: $\left(\tfrac{\sqrt{3}}{2}t - 10\right)^2 + \tfrac{1}{4}t^2 = 36$, which simplifies to $t^2 - 10\sqrt{3}\,t + 64 = 0$.
3. Quadratic formula: $t = 5\sqrt{3} \pm \sqrt{11}$, so $AC \approx 11.98$ or $AC \approx 5.34$.
4. Both are positive, so two non-congruent triangles share the same side-side-angle data. Geometrically, a circle of radius $6$ around $B$ crosses the ray twice.

## Common misconceptions and boundary cases

- **SSA and AAA are not congruence tests.** Example 6 gives two different SSA triangles. AAA only fixes shape: a $3$-$4$-$5$ and a $6$-$8$-$10$ triangle have the same angles but are not congruent. (HL is the special SSA case that does work, because the given angle is right.)
- **Using CPCTC too early.** CPCTC can only be cited after a congruence statement has been proved.
- **Adding the adjacent angle.** The exterior angle equals the sum of the two *remote* interior angles, not the angle next to it.
- **Allowing equality in the Triangle Inequality.** Lengths $5$, $5$, $10$ give a flat (degenerate) figure, not a triangle; the inequality is strict.
- **Wrong correspondence order.** If $\triangle ABC \cong \triangle DEF$, then $\overline{BC} \cong \overline{EF}$, not $\overline{DF}$.
- **Assuming every center is inside.** For an obtuse triangle the circumcenter and orthocenter are outside the triangle.

## Practice

1. The angles of a triangle are $(2x + 10)^\circ$, $(3x - 5)^\circ$, and $(x + 25)^\circ$. Find each angle.
2. An exterior angle measures $120^\circ$ and one remote interior angle measures $45^\circ$. Find the other remote interior angle and the adjacent interior angle.
3. Which sets can be side lengths of a triangle? (a) $4, 7, 10$ (b) $5, 5, 10$ (c) $2.5, 6, 3.4$
4. Name the congruence test, or say "none": (a) two sides and the included angle; (b) three pairs of angles; (c) right triangles with congruent hypotenuses and one pair of congruent legs; (d) two angles and a non-included side.
5. An isosceles triangle has base angles $(2x + 12)^\circ$ and $(5x - 21)^\circ$. Find the vertex angle.
6. Find the centroid of the triangle with vertices $(-3, 1)$, $(5, 3)$, and $(1, -7)$.
7. Explain why HL works even though it looks like SSA.

<details>
<summary>Answer key and self-check</summary>

1. $6x + 30 = 180$, so $x = 25$; the angles are $60^\circ$, $70^\circ$, $50^\circ$.
2. Other remote angle: $120 - 45 = 75^\circ$; adjacent interior angle: $180 - 120 = 60^\circ$.
3. (a) Yes, $4 + 7 = 11 \gt 10$. (b) No, $5 + 5 = 10$ is not greater than $10$. (c) No, $2.5 + 3.4 = 5.9 \lt 6$.
4. (a) SAS; (b) none; (c) HL; (d) AAS.
5. $2x + 12 = 5x - 21$, so $x = 11$; base angles $34^\circ$; vertex angle $180 - 68 = 112^\circ$.
6. $\left(\tfrac{-3 + 5 + 1}{3}, \tfrac{1 + 3 - 7}{3}\right) = (1, -1)$.
7. If legs $a$ and hypotenuse $c$ match, the third sides both equal $\sqrt{c^2 - a^2}$ by the Pythagorean theorem, so the triangles are congruent by SSS. With a right angle, the "second triangle" that breaks SSA cannot occur.

Self-check method: confirm that your three angles add to $180^\circ$, that the largest angle is opposite the longest side, and that every congruence statement lists vertices in matching order.

</details>

## Where this fits

This lesson follows [15.3 - Parallel & Perpendicular Lines](/153-parallel-perpendicular-lines) in the [Geometry course](/subject/geometry). Next, [15.5 - Similarity & Proportions](/155-similarity-proportions) relaxes congruence to "same shape, any size." The Law of Sines in [16.5 - Trig Identities & Equations](/165-trig-identities-equations) revisits the SSA ambiguous case from Example 6.

## Sources

- OpenStax, *Contemporary Mathematics*, [10.3 Triangles](https://openstax.org/books/contemporary-mathematics/pages/10-3-triangles)
- OpenStax, *Prealgebra 2e*, [9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem](https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition I.5](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI5.html), [Proposition I.20](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI20.html), and [Proposition I.32](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI32.html)

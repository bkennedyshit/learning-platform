---
title: "15.7 - Circles"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.7"
type: chapter
objectives:
  - "Identify radii, chords, secants, tangents, arcs, central angles, and inscribed angles in a circle"
  - "Use the Inscribed Angle Theorem and tangent-radius perpendicularity to find angle and segment measures"
  - "Apply the intersecting-chord and secant-tangent segment relationships (power of a point)"
  - "Compute arc length and sector area, and convert a circle's general equation to center-radius form"
open_source: true
---

# 15.7 - Circles

A circle has one defining property: every point is the same distance from the center. From that single fact come a surprising number of exact relationships between angles, arcs, and segments. This lesson names the parts of a circle, proves the key angle theorems, introduces the segment products known as power of a point, and connects circles to the coordinate plane through arc length, sector area, and the equation $(x - h)^2 + (y - k)^2 = r^2$.

## Prerequisites

From [15.4 - Triangles](/154-triangles) you need the Isosceles Triangle Theorem and the Exterior Angle Theorem; from [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry) you need the Pythagorean theorem; and from [15.1 - Foundations of Geometry](/151-foundations-of-geometry) you need the distance formula. Completing the square, from [14.8 - Factoring & Quadratics](/148-factoring-quadratics), is used to rewrite circle equations.

## Learning objectives

By the end of this lesson you should be able to:

1. Name and identify the parts of a circle and the measure of minor arcs, major arcs, and semicircles.
2. Use the Inscribed Angle Theorem and its corollaries to find angles and arcs.
3. Use the tangent-radius theorem and the two-tangent theorem to find lengths.
4. Apply the intersecting-chords and secant-tangent products to find segment lengths.
5. Compute arc length and sector area, and find the center and radius from a circle's equation.

## Core ideas

### Parts of a circle

A **circle** is the set of points in a plane at distance $r$, the **radius**, from a **center**. A **chord** joins two points of the circle; a **diameter** is a chord through the center, of length $2r$. A **secant** is a line that crosses the circle at two points, and a **tangent** is a line that touches it at exactly one point, the **point of tangency**.

A **central angle** has its vertex at the center. The arc inside it is a **minor arc** (less than $180^\circ$); the rest of the circle is the **major arc**; a diameter cuts off two **semicircles** of $180^\circ$. The degree measure of a minor arc equals its central angle. A **sector** is the region between two radii and their arc.

### Inscribed angles

An **inscribed angle** has its vertex on the circle and chords as its sides. **Inscribed Angle Theorem:** an inscribed angle measures half its intercepted arc (equivalently, half the central angle on the same arc; *Elements* III.20).

Proof idea for one case: suppose side $\overline{BC}$ of inscribed angle $\angle ABC$ is a diameter through the center $O$, and let $m\angle ABC = x$. Then $\triangle OBA$ is isosceles ($OA = OB = r$), so $m\angle OAB = x$ as well. Because $B$, $O$, $C$ are collinear, the central angle $\angle AOC$ is an exterior angle of $\triangle OBA$, so it equals $x + x = 2x$. Other positions follow by adding or subtracting two such cases.

Corollaries:

- inscribed angles that intercept the same arc are congruent (*Elements* III.21);
- an angle inscribed in a semicircle is a right angle (*Elements* III.31);
- opposite angles of a quadrilateral inscribed in a circle are supplementary.

Angles formed by two chords that cross *inside* the circle measure half the **sum** of the two intercepted arcs. Angles formed by two secants or tangents meeting *outside* the circle measure half the **difference** of the intercepted arcs.

### Tangents and chords

- A tangent is perpendicular to the radius drawn to the point of tangency (*Elements* III.18).
- Two tangent segments from the same exterior point are congruent.
- A line through the center perpendicular to a chord bisects the chord (*Elements* III.3), which creates a right triangle with the radius as hypotenuse.

### Power of a point

- **Intersecting chords:** if chords $\overline{AB}$ and $\overline{CD}$ meet at $E$ inside the circle, then $AE \cdot EB = CE \cdot ED$ (*Elements* III.35).
- **Secant-tangent:** from an exterior point $P$, if a tangent touches at $T$ and a secant meets the circle at $A$ (near) and $B$ (far), then $PT^2 = PA \cdot PB$ (*Elements* III.36).
- **Two secants:** from $P$, $PA \cdot PB = PC \cdot PD$, each written as outside part times whole secant.

### Measurement and equations

For a central angle of $\theta$ degrees in a circle of radius $r$:

$$\text{arc length} = \frac{\theta}{360} \cdot 2\pi r, \qquad \text{sector area} = \frac{\theta}{360} \cdot \pi r^2.$$

By the distance formula, the circle with center $(h, k)$ and radius $r$ is

$$(x - h)^2 + (y - k)^2 = r^2.$$

## Worked examples

### Example 1: Inscribed and central angles

An inscribed angle intercepts an arc of $110^\circ$. A central angle intercepts the same arc.

1. Central angle $= 110^\circ$, since it equals its arc.
2. Inscribed angle $= \tfrac{1}{2}(110) = 55^\circ$.
3. Any other inscribed angle on the same arc is also $55^\circ$.

### Example 2: Arc length and sector area

A circle has radius $9$ and a central angle of $80^\circ$.

1. Arc length: $\tfrac{80}{360} \cdot 2\pi(9) = \tfrac{2}{9} \cdot 18\pi = 4\pi \approx 12.57$.
2. Sector area: $\tfrac{80}{360} \cdot \pi(81) = \tfrac{2}{9} \cdot 81\pi = 18\pi \approx 56.55$ square units.

### Example 3: Tangent length

A point $P$ is $13$ units from the center $O$ of a circle of radius $5$. Find the length of a tangent segment from $P$.

1. The tangent meets the radius at a right angle at $T$, so $\triangle OTP$ is right with hypotenuse $OP$.
2. $PT = \sqrt{13^2 - 5^2} = \sqrt{144} = 12$. The other tangent from $P$ is also $12$.

### Example 4: Power of a point

1. Chords cross inside a circle. One is split into $4$ and $9$; the other into $6$ and $x$. Then $4 \cdot 9 = 6x$, so $x = 6$.
2. From exterior point $P$, a secant has outside part $PA = 4$ and whole length $PB = 16$. A tangent from $P$ has length $t$. Then $t^2 = 4 \cdot 16 = 64$ and $t = 8$.

### Example 5: Chord distance from center

A chord of length $16$ lies in a circle of radius $10$. How far is the chord from the center?

1. The perpendicular from the center bisects the chord, giving half-chord $8$.
2. Right triangle with hypotenuse $10$ and leg $8$: distance $= \sqrt{100 - 64} = 6$.

### Example 6: Equation of a circle

Find the center and radius of $x^2 + y^2 - 6x + 4y - 12 = 0$.

1. Group and complete the square: $(x^2 - 6x + 9) + (y^2 + 4y + 4) = 12 + 9 + 4$.
2. $(x - 3)^2 + (y + 2)^2 = 25$, so the center is $(3, -2)$ and the radius is $5$.
3. Check a point: $(8, -2)$ gives $25 + 0 = 25$, so it is on the circle, $5$ units right of the center.

## Common misconceptions and boundary cases

- **Inscribed angle equals its arc.** That is true of a central angle. An inscribed angle is half its arc.
- **Arc measure vs. arc length.** Arc measure is in degrees and does not depend on the radius; arc length is a distance. A $60^\circ$ arc is $\pi$ long when $r = 3$ but $2\pi$ long when $r = 6$.
- **Sign errors in the equation.** $(x + 4)^2 + (y - 5)^2 = 9$ has center $(-4, 5)$ and radius $3$, not $9$.
- **Forgetting to add to both sides when completing the square.** Every constant added on the left must also be added on the right.
- **Using the whole secant incorrectly.** In $PT^2 = PA \cdot PB$, $PB$ is the full distance from $P$ to the far intersection, not the chord inside the circle.
- **Half-sum vs. half-difference.** Inside the circle, add the arcs; outside, subtract. Angles with vertex *on* the circle use half the single arc.
- **Assuming tangency from a picture.** A line that looks tangent must be given as tangent, or shown perpendicular to a radius at its endpoint on the circle.

## Practice

1. An inscribed angle measures $38^\circ$. Find its intercepted arc and the central angle on the same arc.
2. A triangle is inscribed in a circle with one side a diameter. One of its other angles is $27^\circ$. Find the third angle.
3. A circle has radius $6$. Find the arc length and sector area for a $150^\circ$ central angle, exactly and to two decimal places.
4. Two tangent segments from point $P$ measure $PA = 3x + 2$ and $PB = 5x - 6$. Find $PA$.
5. Chords $\overline{AB}$ and $\overline{CD}$ meet at $E$ with $AE = 5$, $EB = 8$, and $CE = 4$. Find $ED$.
6. Write the equation of the circle with center $(-1, 4)$ that passes through $(2, 8)$.
7. Find the center and radius of $x^2 + y^2 + 8x - 10y + 32 = 0$.
8. Two chords meet inside a circle and intercept arcs of $70^\circ$ and $110^\circ$. Find the angle. Then find the angle formed outside a circle by two secants intercepting arcs of $130^\circ$ and $40^\circ$.

<details>
<summary>Answer key and self-check</summary>

1. Arc $76^\circ$; central angle $76^\circ$.
2. The angle opposite the diameter is $90^\circ$, so the third angle is $180 - 90 - 27 = 63^\circ$.
3. Arc length $\tfrac{150}{360} \cdot 12\pi = 5\pi \approx 15.71$; sector area $\tfrac{150}{360} \cdot 36\pi = 15\pi \approx 47.12$.
4. $3x + 2 = 5x - 6$ gives $x = 4$, so $PA = 14$.
5. $5 \cdot 8 = 4 \cdot ED$, so $ED = 10$.
6. $r = \sqrt{3^2 + 4^2} = 5$: $(x + 1)^2 + (y - 4)^2 = 25$.
7. $(x + 4)^2 + (y - 5)^2 = -32 + 16 + 25 = 9$: center $(-4, 5)$, radius $3$.
8. Inside: $\tfrac{1}{2}(70 + 110) = 90^\circ$. Outside: $\tfrac{1}{2}(130 - 40) = 45^\circ$.

Self-check method: for equations, substitute a known point back in; for angles, check that inscribed angles are half their arcs and that arcs around one circle total $360^\circ$; for segment products, multiply both sides and confirm they match.

</details>

## Where this fits

This lesson follows [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry) in the [Geometry course](/subject/geometry). Next, [15.8 - Area, Volume & Coordinate Geometry](/158-area-volume-coordinate-geometry) uses $\pi r^2$ for cylinders, cones, and spheres. The circle equation is the first conic section in [16.6 - Conic Sections](/166-conic-sections), and radian measure, defined from arc length, is developed in [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle).

## Sources

- OpenStax, *Intermediate Algebra 2e*, [11.1 Distance and Midpoint Formulas; Circles](https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles)
- OpenStax, *Contemporary Mathematics*, [10.4 Polygons, Perimeter, and Circumference](https://openstax.org/books/contemporary-mathematics/pages/10-4-polygons-perimeter-and-circumference)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), Book III: [Proposition III.3](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII3.html), [III.18](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII18.html), [III.20](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII20.html), [III.21](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII21.html), [III.31](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII31.html), [III.35](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII35.html), and [III.36](https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII36.html)

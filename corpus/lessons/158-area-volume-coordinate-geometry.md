---
title: "15.8 - Area, Volume & Coordinate Geometry"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.8"
type: chapter
objectives:
  - "Compute areas of polygons and circles, including polygons given by coordinates"
  - "Compute volume and surface area of prisms, cylinders, pyramids, cones, and spheres and explain the one-third factor and Cavalieri's principle"
  - "Write coordinate proofs of properties of triangles and quadrilaterals"
  - "Apply translations, reflections, rotations, and dilations to coordinates and identify which preserve distance"
open_source: true
---

# 15.8 - Area, Volume & Coordinate Geometry

This final Geometry lesson pulls the course together. Area and volume formulas measure the figures you have been reasoning about, and the coordinate plane lets you prove geometric facts with algebra and describe transformations as rules. The emphasis is on knowing where each formula comes from, so you can rebuild it, check it, and recognize when it does not apply.

## Prerequisites

You need the Pythagorean theorem and special right triangles from [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry), circle area and $\pi$ from [15.7 - Circles](/157-circles), dilations and the $k^2$ area rule from [15.5 - Similarity & Proportions](/155-similarity-proportions), and the slope, distance, and midpoint formulas from [15.1 - Foundations of Geometry](/151-foundations-of-geometry) and [15.3 - Parallel & Perpendicular Lines](/153-parallel-perpendicular-lines).

## Learning objectives

By the end of this lesson you should be able to:

1. Find areas of triangles, parallelograms, trapezoids, regular polygons, circles, and composite figures, and find the area of a polygon from its vertex coordinates.
2. Find the volume and surface area of prisms, cylinders, pyramids, cones, and spheres, using height and slant height correctly.
3. Explain Cavalieri's principle and why pyramids and cones have a factor of $\tfrac{1}{3}$.
4. Write a coordinate proof by placing a figure with general coordinates.
5. Apply translations, reflections, rotations, and dilations to points and decide which transformations preserve length.

## Core ideas

### Area in two dimensions

Area counts unit squares. Each formula below comes from rearranging a rectangle ($A = bh$):

- **Parallelogram:** $A = bh$, where $h$ is perpendicular to the base. Cutting a right triangle off one end and moving it to the other makes a rectangle.
- **Triangle:** $A = \tfrac{1}{2}bh$; two copies form a parallelogram.
- **Trapezoid:** $A = \tfrac{1}{2}(b_1 + b_2)h$; two copies, one rotated, form a parallelogram with base $b_1 + b_2$.
- **Regular polygon:** $A = \tfrac{1}{2}aP$, where $a$ is the **apothem** (center to the midpoint of a side) and $P$ is the perimeter; the polygon splits into congruent triangles of height $a$.
- **Circle:** $A = \pi r^2$.

**Coordinates (shoelace formula).** For a polygon with vertices $(x_1, y_1), \dots, (x_n, y_n)$ listed in order around the boundary,

$$A = \frac{1}{2}\left\lvert \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i) \right\rvert, \quad \text{with } (x_{n+1}, y_{n+1}) = (x_1, y_1).$$

### Volume and surface area

Volume counts unit cubes. A **prism** or **cylinder** has two congruent parallel bases, so its volume is base area times height, $V = Bh$. A **pyramid** or **cone** rises from a base to a single point, and its volume is one third of the prism or cylinder with the same base and height, $V = \tfrac{1}{3}Bh$ (*Elements* XII.7 and XII.10).

| Solid | Volume | Surface area |
|---|---|---|
| Prism | $Bh$ | $2B + (\text{perimeter of base}) \cdot h$ |
| Cylinder | $\pi r^2 h$ | $2\pi r^2 + 2\pi r h$ |
| Pyramid | $\tfrac{1}{3}Bh$ | $B$ plus the areas of the triangular faces |
| Cone | $\tfrac{1}{3}\pi r^2 h$ | $\pi r^2 + \pi r \ell$ |
| Sphere | $\tfrac{4}{3}\pi r^3$ | $4\pi r^2$ |

Here $h$ is the perpendicular height and $\ell$ is the **slant height**, measured along the lateral surface. For a right cone, $\ell = \sqrt{r^2 + h^2}$.

**Cavalieri's principle:** if two solids have the same height and every plane parallel to the base cuts them in cross-sections of equal area, the solids have equal volume. Picture a stack of coins pushed sideways: the oblique stack has the same volume as the straight one, which is why $V = Bh$ also holds for oblique prisms and cylinders when $h$ is the perpendicular height. A **cross-section** is the 2D shape where a plane cuts a solid; a plane parallel to the base of a cylinder gives a circle, and a vertical plane through its axis gives a rectangle.

### Coordinate proofs

To prove a property for every figure of a type, place a general copy in the plane with variable coordinates, using the origin and an axis to keep the algebra simple. Then use slope (parallel or perpendicular), distance (congruent), and midpoint (bisects) to verify the claim.

### Transformations

| Transformation | Rule |
|---|---|
| Translation by $(a, b)$ | $(x, y) \mapsto (x + a, y + b)$ |
| Reflection in the $x$-axis | $(x, y) \mapsto (x, -y)$ |
| Reflection in the $y$-axis | $(x, y) \mapsto (-x, y)$ |
| Reflection in $y = x$ | $(x, y) \mapsto (y, x)$ |
| Rotation $90^\circ$ counterclockwise about the origin | $(x, y) \mapsto (-y, x)$ |
| Rotation $180^\circ$ about the origin | $(x, y) \mapsto (-x, -y)$ |
| Dilation by $k$ about the origin | $(x, y) \mapsto (kx, ky)$ |

Translations, reflections, and rotations are **rigid motions**: they preserve distance and angle measure, so images are congruent to the original. Dilations preserve angles but scale distances by $\lvert k \rvert$, so images are similar.

## Worked examples

### Example 1: Trapezoid and composite area

1. A trapezoid has bases $8$ and $14$ and height $5$: $A = \tfrac{1}{2}(8 + 14)(5) = 55$ square units.
2. An illustrative window is a $4 \times 6$ rectangle topped by a semicircle on the side of length $4$. Area $= 24 + \tfrac{1}{2}\pi(2)^2 = 24 + 2\pi \approx 30.28$ square units.

### Example 2: Area from coordinates

Find the area of the quadrilateral with vertices $(0, 0)$, $(6, 0)$, $(8, 4)$, $(2, 5)$ in that order.

1. Terms $x_i y_{i+1} - x_{i+1} y_i$: $0 \cdot 0 - 6 \cdot 0 = 0$; $6 \cdot 4 - 8 \cdot 0 = 24$; $8 \cdot 5 - 2 \cdot 4 = 32$; $2 \cdot 0 - 0 \cdot 5 = 0$.
2. Sum $= 56$, so $A = \tfrac{1}{2}(56) = 28$.
3. Check by splitting along the diagonal from $(0, 0)$ to $(8, 4)$: the two triangles have areas $12$ and $16$, totaling $28$.

### Example 3: Cylinder

A cylinder has radius $3$ cm and height $10$ cm.

1. $V = \pi(3)^2(10) = 90\pi \approx 282.74$ cm³.
2. $SA = 2\pi(9) + 2\pi(3)(10) = 18\pi + 60\pi = 78\pi \approx 245.04$ cm². The lateral surface unrolls into a rectangle of width $2\pi r$ and height $h$.

### Example 4: Cone, height vs. slant height

A right cone has radius $6$ and height $8$.

1. Slant height: $\ell = \sqrt{36 + 64} = 10$.
2. $V = \tfrac{1}{3}\pi(36)(8) = 96\pi \approx 301.59$ cubic units.
3. $SA = \pi(36) + \pi(6)(10) = 96\pi \approx 301.59$ square units. The numbers match by coincidence; the units differ, so the two quantities cannot be compared.

### Example 5: Sphere

A sphere has diameter $10$, so $r = 5$. Then $V = \tfrac{4}{3}\pi(125) = \tfrac{500\pi}{3} \approx 523.60$ and $SA = 4\pi(25) = 100\pi \approx 314.16$.

### Example 6: Coordinate proof

Prove that the diagonals of a parallelogram bisect each other.

1. Place the parallelogram as $O(0, 0)$, $A(a, 0)$, $B(a + b, c)$, $C(b, c)$. Opposite sides $\overline{OA}$ and $\overline{CB}$ are horizontal with length $a$, and $\overline{OC}$ and $\overline{AB}$ both have slope $\tfrac{c}{b}$, so it is a parallelogram.
2. Midpoint of diagonal $\overline{OB}$: $\left(\tfrac{a + b}{2}, \tfrac{c}{2}\right)$.
3. Midpoint of diagonal $\overline{AC}$: $\left(\tfrac{a + b}{2}, \tfrac{c}{2}\right)$.
4. The diagonals share a midpoint, so each bisects the other. Because $a$, $b$, $c$ are general, this covers every parallelogram.

### Example 7: A rotation preserves lengths

Rotate $A(1, 2)$, $B(4, 2)$, $C(1, 6)$ by $90^\circ$ counterclockwise about the origin.

1. Apply $(x, y) \mapsto (-y, x)$: $A'(-2, 1)$, $B'(-2, 4)$, $C'(-6, 1)$.
2. Original sides: $AB = 3$, $AC = 4$, $BC = \sqrt{9 + 16} = 5$.
3. Image sides: $A'B' = 3$, $A'C' = 4$, $B'C' = \sqrt{16 + 9} = 5$. The image is congruent, as expected for a rigid motion.

## Common misconceptions and boundary cases

- **Slant height in the volume formula.** Volume uses the perpendicular height $h$; only lateral surface area uses $\ell$. Using $\ell = 10$ in Example 4 would give $120\pi$, which is wrong.
- **Forgetting the $\tfrac{1}{3}$.** A cone holds one third of the cylinder with the same base and height.
- **Doubling lengths doubles volume.** Doubling every length multiplies surface area by $4$ and volume by $8$.
- **Square vs. cubic units.** Areas are in square units and volumes in cubic units, even when the numbers agree.
- **Shoelace vertices out of order.** The vertices must be listed consecutively around the boundary. Skipping around can produce a self-crossing path and the wrong area.
- **Rotation direction and center.** $(x, y) \mapsto (-y, x)$ is $90^\circ$ counterclockwise about the origin only. Clockwise is $(x, y) \mapsto (y, -x)$.
- **Cavalieri needs every cross-section.** Equal base areas and equal heights are not enough unless every parallel slice has equal area.

## Practice

1. Find the area of a triangle with base $12$ and height $7$.
2. Find the area of a regular hexagon with side $4$ using the apothem formula.
3. Use the shoelace formula to find the area of the triangle with vertices $(-2, 1)$, $(4, 3)$, $(1, -4)$.
4. A square pyramid has base edge $6$ and height $4$. Find its volume and surface area.
5. A cylinder and a cone have the same radius and height. What is the ratio of their volumes?
6. The radius of a sphere is doubled. By what factor do its volume and surface area change?
7. For the point $(3, -5)$, give its image after (a) reflection in $y = x$, (b) reflection in the $x$-axis, (c) rotation of $180^\circ$ about the origin, and (d) translation by $(-2, 4)$.
8. Show that $A(1, 1)$, $B(5, 2)$, $C(4, 6)$, $D(0, 5)$ form a square, and find its area.

<details>
<summary>Answer key and self-check</summary>

1. $\tfrac{1}{2}(12)(7) = 42$.
2. The hexagon is six equilateral triangles of side $4$, so the apothem is the height of one, $2\sqrt{3}$. $A = \tfrac{1}{2}(2\sqrt{3})(24) = 24\sqrt{3} \approx 41.57$.
3. Terms: $(-2)(3) - (4)(1) = -10$; $(4)(-4) - (1)(3) = -19$; $(1)(1) - (-2)(-4) = -7$. Sum $-36$, so $A = 18$.
4. $V = \tfrac{1}{3}(36)(4) = 48$. Slant height of each face: $\sqrt{4^2 + 3^2} = 5$. $SA = 36 + 4 \cdot \tfrac{1}{2}(6)(5) = 96$.
5. $3 : 1$ (cylinder to cone).
6. Volume $\times 8$; surface area $\times 4$.
7. (a) $(-5, 3)$; (b) $(3, 5)$; (c) $(-3, 5)$; (d) $(1, -1)$.
8. Side vectors $\overrightarrow{AB} = (4, 1)$, $\overrightarrow{BC} = (-1, 4)$, $\overrightarrow{CD} = (-4, -1)$, $\overrightarrow{DA} = (1, -4)$ all have length $\sqrt{17}$. Slopes of $\overline{AB}$ and $\overline{BC}$ are $\tfrac{1}{4}$ and $-4$, with product $-1$, so the angle at $B$ is right; the same holds at every vertex. It is a square with area $(\sqrt{17})^2 = 17$.

Self-check method: confirm your units (square or cubic), recompute a coordinate area by splitting into triangles, and after any rigid motion recheck one side length.

</details>

## Where this fits

This is the final lesson in the [Geometry course](/subject/geometry) and follows [15.7 - Circles](/157-circles). The coordinate methods continue in [16.6 - Conic Sections](/166-conic-sections). Transformations written as rules become matrices in [Linear Transformations & Change of Basis](/24-linear-transformations-change-of-basis), and the slicing idea behind Cavalieri's principle becomes volume by integration in [Single Variable Integration](/13-single-variable-integration).

## Sources

- OpenStax, *Contemporary Mathematics*, [10.5 Tessellations](https://openstax.org/books/contemporary-mathematics/pages/10-5-tessellations) (transformations)
- OpenStax, *Contemporary Mathematics*, [10.6 Area](https://openstax.org/books/contemporary-mathematics/pages/10-6-area)
- OpenStax, *Contemporary Mathematics*, [10.7 Volume and Surface Area](https://openstax.org/books/contemporary-mathematics/pages/10-7-volume-and-surface-area)
- OpenStax, *Prealgebra 2e*, [9.6 Solve Geometry Applications: Volume and Surface Area](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition XII.7](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII7.html) and [Proposition XII.10](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII10.html)

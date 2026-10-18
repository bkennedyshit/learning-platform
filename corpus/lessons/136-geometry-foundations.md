---
title: "13.6 - Geometry Foundations"
subject: "Pre-Algebra"
catalog: k12
audience_tier: 9-12
chapter: "13.6"
type: chapter
objectives:
  - "Compute areas of rectangles, parallelograms, triangles, trapezoids, circles, and composite figures, and explain where each formula comes from"
  - "Compute circumference and give exact answers in terms of pi as well as rounded approximations"
  - "Find the volume and surface area of prisms and pyramids using bases, heights, and nets"
  - "Plot points, find horizontal and vertical distances, and reflect points across the coordinate axes"
open_source: true
---

# 13.6 - Geometry Foundations

Measurement questions come in three kinds: how long (length, perimeter, circumference), how much surface (area), and how much space (volume). Each is measured in different units: units, square units, and cubic units. This lesson collects the area formulas for common plane figures, extends them to the surface area and volume of prisms and pyramids, and introduces the coordinate plane as a place to measure distances and perform reflections.

## Prerequisites

You need fraction and decimal arithmetic from [13.3 - Fractions, Decimals & Percent](/133-fractions-decimals-percent), evaluating formulas from [13.4 - Expressions & Variables](/134-expressions-variables), and solving simple equations from [13.5 - Equations & Inequalities](/135-equations-inequalities). Signed numbers from [13.2 - The Number System](/132-the-number-system) are used for coordinates.

## Learning objectives

By the end of this lesson you should be able to:

1. Find the area of rectangles, parallelograms, triangles, trapezoids, circles, and figures built from them, and explain each formula by cutting and rearranging.
2. Find the circumference of a circle and report answers both exactly (in terms of $\pi$) and rounded.
3. Find the volume and surface area of right prisms and pyramids.
4. Plot points in all four quadrants, find horizontal and vertical distances, and reflect points across the $x$- and $y$-axes.

## Core ideas

### Area formulas and why they work

- **Rectangle:** $A = lw$. A $5 \times 3$ rectangle holds $15$ unit squares.
- **Parallelogram:** $A = bh$, where $h$ is the **perpendicular** height, not the slanted side. Cutting a right triangle off one end and moving it to the other end turns the parallelogram into a rectangle with the same base and height.
- **Triangle:** $A = \tfrac{1}{2}bh$. Two copies of any triangle fit together into a parallelogram with base $b$ and height $h$.
- **Trapezoid:** $A = \tfrac{1}{2}h(b_1 + b_2)$. Two copies, one rotated, form a parallelogram with base $b_1 + b_2$.
- **Circle:** $A = \pi r^2$, where $r$ is the radius. Cutting a circle into many thin wedges and alternating them produces a shape close to a parallelogram with base half the circumference, $\pi r$, and height $r$.

A **composite figure** is split into these shapes; add the pieces, or subtract a piece that is cut out.

### Circumference

The **circumference** of a circle is $C = 2\pi r = \pi d$, where $d = 2r$ is the diameter. The number $\pi$ is the ratio of any circle's circumference to its diameter, about $3.14159$. An exact answer keeps $\pi$ as a symbol ($10\pi$ cm); an approximation replaces it ($\approx 31.42$ cm).

### Prisms and pyramids

A **prism** has two congruent, parallel bases joined by rectangular faces (in a right prism). A **pyramid** has one base and triangular faces meeting at a point called the apex.

- **Volume of a prism:** $V = Bh$, where $B$ is the area of the base and $h$ is the distance between the bases. For a rectangular prism, $V = lwh$.
- **Volume of a pyramid:** $V = \tfrac{1}{3}Bh$, where $h$ is the perpendicular height from the apex to the base. A pyramid holds exactly one third of the prism with the same base and height (Euclid, *Elements* XII.7).
- **Surface area:** the total area of all faces. Unfolding a solid into a flat **net** shows every face. For a rectangular prism, $SA = 2(lw + lh + wh)$. For a pyramid, add the base to the triangular faces, using the **slant height** (the height of each triangular face) for those triangles.

Area is in square units; volume is in cubic units.

### The coordinate plane

The **coordinate plane** is formed by a horizontal $x$-axis and a vertical $y$-axis meeting at the origin $(0, 0)$. An ordered pair $(x, y)$ means move $x$ units horizontally, then $y$ units vertically. The axes divide the plane into four **quadrants**, numbered I to IV counterclockwise starting at the upper right, where both coordinates are positive.

- Two points with the same $y$-coordinate lie on a horizontal line; the distance between them is $\lvert x_2 - x_1 \rvert$.
- Two points with the same $x$-coordinate lie on a vertical line; the distance is $\lvert y_2 - y_1 \rvert$.
- For other pairs, the horizontal and vertical distances are the legs of a right triangle, and the Pythagorean theorem gives the straight-line distance.

### Reflections

A **reflection** flips a figure across a line, producing a mirror image the same size and shape.

- Across the $x$-axis: $(x, y) \mapsto (x, -y)$.
- Across the $y$-axis: $(x, y) \mapsto (-x, y)$.

## Worked examples

### Example 1: Trapezoid area

A trapezoid has parallel sides $6$ and $10$ and height $4$.

1. $A = \tfrac{1}{2}h(b_1 + b_2) = \tfrac{1}{2}(4)(6 + 10) = 2 \cdot 16 = 32$ square units.
2. Check by splitting: a $6 \times 4$ rectangle ($24$) plus triangles with total base $10 - 6 = 4$ and height $4$ ($\tfrac{1}{2} \cdot 4 \cdot 4 = 8$) gives $32$.

### Example 2: Circle and a composite figure

1. A circle has diameter $10$ cm. Then $r = 5$, $C = 10\pi \approx 31.42$ cm, and $A = 25\pi \approx 78.54$ cm$^2$.
2. An illustrative window is a $4$ ft wide, $3$ ft tall rectangle topped by a semicircle of diameter $4$ ft. Area $= 4 \cdot 3 + \tfrac{1}{2}\pi(2)^2 = 12 + 2\pi \approx 18.28$ ft$^2$.

### Example 3: Prisms

1. A rectangular prism measures $5 \times 3 \times 2$. Volume: $5 \cdot 3 \cdot 2 = 30$ cubic units. Surface area: $2(15 + 10 + 6) = 62$ square units.
2. A triangular prism has a right-triangle base with legs $3$ and $4$ and hypotenuse $5$, and length $10$. Base area $B = \tfrac{1}{2}(3)(4) = 6$, so $V = 6 \cdot 10 = 60$. Surface area: two triangles ($2 \cdot 6 = 12$) plus three rectangles ($3 \cdot 10 + 4 \cdot 10 + 5 \cdot 10 = 120$), total $132$ square units.

### Example 4: Square pyramid

A pyramid has a square base with side $6$, height $4$, and slant height $5$. (The slant height is $5$ because the height $4$ and half the base, $3$, form a right triangle with hypotenuse $\sqrt{3^2 + 4^2} = 5$.)

1. Volume: $\tfrac{1}{3}(6^2)(4) = \tfrac{1}{3}(36)(4) = 48$ cubic units.
2. Surface area: base $36$ plus four triangles $4 \cdot \tfrac{1}{2}(6)(5) = 60$, total $96$ square units.

### Example 5: Distances and reflections on the grid

Plot $A(-3, 2)$, $B(4, 2)$, and $C(4, -5)$.

1. $A$ and $B$ share $y = 2$: $AB = \lvert 4 - (-3) \rvert = 7$.
2. $B$ and $C$ share $x = 4$: $BC = \lvert 2 - (-5) \rvert = 7$.
3. Triangle $ABC$ has a right angle at $B$, so its area is $\tfrac{1}{2}(7)(7) = 24.5$ and $AC = \sqrt{7^2 + 7^2} = 7\sqrt{2} \approx 9.90$.
4. Reflect $A$ across the $x$-axis: $(-3, -2)$. Across the $y$-axis: $(3, 2)$.

## Common misconceptions and boundary cases

- **Using the slanted side as the height.** In a parallelogram with base $12$, slanted side $7$, and height $5$, the area is $12 \cdot 5 = 60$, not $12 \cdot 7$.
- **Radius versus diameter.** $A = \pi r^2$ uses the radius. Using the diameter $10$ instead of the radius $5$ gives $100\pi$, four times too large.
- **Mixing up circumference and area.** $2\pi r$ is a length; $\pi r^2$ is an area. The units ($\text{cm}$ vs. $\text{cm}^2$) tell them apart.
- **Pyramid volume as one half.** A pyramid is $\tfrac{1}{3}$ of the matching prism, not $\tfrac{1}{2}$. The $\tfrac{1}{2}$ belongs to triangle area.
- **Height versus slant height.** Volume uses the perpendicular height; the lateral faces of a pyramid use the slant height.
- **Reflecting the wrong coordinate.** Reflecting across the $x$-axis changes the sign of $y$, because points move up or down across that horizontal axis.

## Practice

1. Find the area of a parallelogram with base $12$, slanted side $7$, and height $5$.
2. Find the area of a triangle with base $9$ and height $8$.
3. A circle has radius $3$ m. Find its circumference and area exactly and to the nearest hundredth.
4. Find the area of a trapezoid with bases $5$ and $11$ and height $7$.
5. Find the volume and surface area of a cube with edge $4$.
6. A rectangular pyramid has a base $8$ by $5$ and height $9$. Find its volume.
7. Find the distance between $P(-2, -1)$ and $Q(-2, 6)$. Then reflect $P$ across the $y$-axis and across the $x$-axis.
8. An illustrative garden is a $10$ m by $6$ m rectangle with a circular fountain of radius $1.5$ m in the middle. Find the planted area to the nearest hundredth.

<details>
<summary>Answer key and self-check</summary>

1. $A = bh = 12 \cdot 5 = 60$ square units.
2. $\tfrac{1}{2}(9)(8) = 36$ square units.
3. $C = 6\pi \approx 18.85$ m; $A = 9\pi \approx 28.27$ m$^2$.
4. $\tfrac{1}{2}(7)(5 + 11) = 56$ square units.
5. $V = 4^3 = 64$ cubic units; $SA = 6 \cdot 4^2 = 96$ square units.
6. $\tfrac{1}{3}(8 \cdot 5)(9) = \tfrac{1}{3}(40)(9) = 120$ cubic units.
7. Same $x$-coordinate: $\lvert 6 - (-1) \rvert = 7$. Across the $y$-axis: $(2, -1)$. Across the $x$-axis: $(-2, 1)$.
8. $60 - \pi(1.5)^2 = 60 - 2.25\pi \approx 60 - 7.07 = 52.93$ m$^2$.

Self-check method: confirm your units (length, square, or cubic) match the question, and estimate with $\pi \approx 3$ to catch large errors (for problem 3, $9\pi$ should be a bit more than $27$). For reflections, check that the image is the same distance from the axis as the original, on the opposite side.

</details>

## Where this fits

This lesson follows [13.5 - Equations & Inequalities](/135-equations-inequalities) in the [Pre-Algebra course](/subject/pre-algebra). Next, [13.7 - Statistics & Data](/137-statistics-data) moves from measuring shapes to summarizing data sets. In Geometry, [15.1 - Foundations of Geometry](/151-foundations-of-geometry) turns the grid distances here into the distance formula, [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry) proves the Pythagorean theorem used in Examples 4 and 5, and [15.8 - Area, Volume & Coordinate Geometry](/158-area-volume-coordinate-geometry) adds cylinders, cones, spheres, and more transformations.

## Sources

- OpenStax, *Prealgebra 2e*, [9.4 Use Properties of Rectangles, Triangles, and Trapezoids](https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids)
- OpenStax, *Prealgebra 2e*, [9.5 Solve Geometry Applications: Circles and Irregular Figures](https://openstax.org/books/prealgebra-2e/pages/9-5-solve-geometry-applications-circles-and-irregular-figures)
- OpenStax, *Prealgebra 2e*, [9.6 Solve Geometry Applications: Volume and Surface Area](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area)
- OpenStax, *Prealgebra 2e*, [11.1 Use the Rectangular Coordinate System](https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system)
- OpenStax, *Contemporary Mathematics*, [10.5 Tessellations](https://openstax.org/books/contemporary-mathematics/pages/10-5-tessellations) (reflections) and [10.7 Volume and Surface Area](https://openstax.org/books/contemporary-mathematics/pages/10-7-volume-and-surface-area)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition XII.7](https://mathcs.clarku.edu/~djoyce/java/elements/bookXII/propXII7.html) (a pyramid is one third of the prism with the same base and height)

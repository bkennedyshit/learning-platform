---
title: "15.5 - Similarity & Proportions"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.5"
type: chapter
objectives:
  - "Determine whether polygons are similar and find the scale factor and missing side lengths"
  - "Prove triangles similar with AA, SAS similarity, or SSS similarity"
  - "Apply the Side-Splitter and Triangle Midsegment theorems to find unknown lengths"
  - "Perform dilations in the coordinate plane and predict how perimeter and area change with the scale factor"
open_source: true
---

# 15.5 - Similarity & Proportions

Congruent figures have the same shape and size; similar figures have the same shape and possibly different sizes. Similarity is what makes maps, scale models, shadows, and photographs mathematically useful: if you know one length in each figure, you know the ratio for every length. This lesson defines similarity precisely, gives the three triangle similarity tests, and connects them to parallel lines and dilations.

## Prerequisites

You should be able to solve proportions by cross-multiplying, as in [13.1 - Ratios, Rates & Proportions](/131-ratios-rates-proportions). From [15.4 - Triangles](/154-triangles) you need the Triangle Sum Theorem, congruence notation, and correspondence order; from [15.3 - Parallel & Perpendicular Lines](/153-parallel-perpendicular-lines) you need corresponding angles formed by parallel lines.

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether two polygons are similar, state the scale factor, and find missing sides.
2. Prove two triangles similar using AA, SAS similarity, or SSS similarity, with a correct correspondence.
3. Use the Side-Splitter Theorem and the Triangle Midsegment Theorem to find lengths.
4. Dilate figures about the origin or another center and verify the image is similar to the original.
5. Use the fact that perimeters scale by $k$ and areas scale by $k^2$.

## Core ideas

### Similar polygons and scale factor

Two polygons are **similar**, written $ABCD \sim EFGH$, when corresponding angles are congruent *and* corresponding sides are proportional. The common ratio of corresponding sides (image to original) is the **scale factor** $k$. A scale factor of $1$ means the figures are congruent, so congruence is a special case of similarity.

For similar figures with scale factor $k$:

- every length (sides, perimeters, altitudes, medians) is multiplied by $k$;
- every area is multiplied by $k^2$ (*Elements* VI.19 states this for triangles);
- for solids, every volume is multiplied by $k^3$.

### Triangle similarity tests

You do not have to check all six parts of two triangles.

- **AA:** if two angles of one triangle are congruent to two angles of another, the triangles are similar. (The third angles then match by the Triangle Sum Theorem.)
- **SAS similarity:** two pairs of sides are proportional and the included angles are congruent.
- **SSS similarity:** all three pairs of sides are proportional.

Euclid shows in *Elements* VI.4 that equiangular triangles have proportional sides, which is the content of AA.

### Proportionality theorems

- **Side-Splitter Theorem:** if a line parallel to one side of a triangle meets the other two sides, it divides them proportionally. In $\triangle ABC$ with $D$ on $\overline{AB}$, $E$ on $\overline{AC}$, and $\overline{DE} \parallel \overline{BC}$:
$$\frac{AD}{DB} = \frac{AE}{EC}.$$
The converse also holds (*Elements* VI.2). Visually, the parallel line cuts off a small triangle $\triangle ADE$ similar to $\triangle ABC$ by AA, since corresponding angles at $D$ and $B$ are congruent.
- **Triangle Midsegment Theorem:** the segment joining the midpoints of two sides is parallel to the third side and half as long.

Be careful with which ratio applies. The small triangle gives $\tfrac{DE}{BC} = \tfrac{AD}{AB}$ (part to whole), while the Side-Splitter ratio is $\tfrac{AD}{DB}$ (part to part).

### Dilations

A **dilation** with center $O$ and scale factor $k \gt 0$ sends each point $P$ to $P'$ on ray $\overrightarrow{OP}$ with $OP' = k \cdot OP$. If $k$ is negative, $P'$ lies on the opposite ray at distance $\lvert k \rvert \cdot OP$. With center at the origin, $(x, y) \mapsto (kx, ky)$. With center $(a, b)$, $(x, y) \mapsto (a + k(x - a),\ b + k(y - b))$.

Dilations preserve angle measures, map lines to parallel lines (or to themselves if the line passes through the center), and multiply every distance by $\lvert k \rvert$. They enlarge when $\lvert k \rvert \gt 1$ and reduce when $\lvert k \rvert \lt 1$. Two figures are similar exactly when one can be mapped to the other by a dilation followed by rigid motions.

## Worked examples

### Example 1: Missing sides, perimeter, and area

$\triangle ABC \sim \triangle DEF$ with $AB = 6$, $BC = 8$, $AC = 10$, and $DE = 9$.

1. Scale factor: $k = \tfrac{DE}{AB} = \tfrac{9}{6} = 1.5$.
2. $EF = 1.5 \cdot 8 = 12$ and $DF = 1.5 \cdot 10 = 15$.
3. Perimeters: $24$ and $36$; ratio $1.5$.
4. Since $6^2 + 8^2 = 10^2$, $\triangle ABC$ is right with area $\tfrac{1}{2}(6)(8) = 24$. $\triangle DEF$ has area $\tfrac{1}{2}(9)(12) = 54$, and $\tfrac{54}{24} = 2.25 = 1.5^2$.

### Example 2: Indirect measurement with AA

An illustrative example: a $1.8$ m tall person casts a $2.4$ m shadow at the same moment a tree casts a $16$ m shadow. How tall is the tree?

1. The sun's rays are effectively parallel, so the angle of the rays with the ground is the same for both. Each object meets the ground at a right angle.
2. By AA, the person-shadow triangle is similar to the tree-shadow triangle.
3. $\tfrac{h}{16} = \tfrac{1.8}{2.4}$, so $h = 16 \cdot 0.75 = 12$ m.

### Example 3: Side-Splitter

In $\triangle ABC$, $\overline{DE} \parallel \overline{BC}$ with $AD = 4$, $DB = 6$, and $AE = 5$. Find $EC$, and find $DE$ if $BC = 20$.

1. Side-Splitter: $\tfrac{4}{6} = \tfrac{5}{EC}$, so $4 \cdot EC = 30$ and $EC = 7.5$.
2. For $DE$ use the small triangle: $\tfrac{DE}{BC} = \tfrac{AD}{AB} = \tfrac{4}{10}$, so $DE = 0.4 \cdot 20 = 8$.
3. Check with the other side: $\tfrac{AE}{AC} = \tfrac{5}{12.5} = 0.4$. Consistent.

### Example 4: SSS similarity test

Are triangles with sides $4, 6, 8$ and $6, 9, 12$ similar? What about $4, 6, 8$ and $6, 9, 11$?

1. Pair sides in increasing order: $\tfrac{6}{4} = 1.5$, $\tfrac{9}{6} = 1.5$, $\tfrac{12}{8} = 1.5$. All equal, so the triangles are similar with $k = 1.5$.
2. Second pair: $1.5$, $1.5$, $\tfrac{11}{8} = 1.375$. The ratios differ, so the triangles are not similar.

### Example 5: Dilations

1. Dilate $A(2, 1)$, $B(4, 1)$, $C(2, 5)$ by $k = 3$ about the origin: $A'(6, 3)$, $B'(12, 3)$, $C'(6, 15)$. Check: $AB = 2$ and $A'B' = 6$; $AC = 4$ and $A'C' = 12$.
2. Dilate $P(3, 4)$ by $k = 2$ about $(1, 1)$: $P' = (1 + 2(3 - 1),\ 1 + 2(4 - 1)) = (5, 7)$. The center, $P$, and $P'$ are collinear, and $P'$ is twice as far from the center as $P$.

## Common misconceptions and boundary cases

- **Thinking additively.** Enlarging a $4 \times 6$ rectangle by adding $2$ to each side gives $6 \times 8$, which is not similar: $\tfrac{6}{4} \ne \tfrac{8}{6}$. Similarity multiplies.
- **Scaling area by $k$.** Doubling every length multiplies area by $4$ and volume by $8$.
- **Mismatched correspondence.** In a proportion, each ratio must compare corresponding sides in the same order (small to large, or large to small, consistently).
- **Using the part-to-part ratio for the parallel side.** In Example 3, $\tfrac{DE}{BC}$ equals $\tfrac{AD}{AB}$, not $\tfrac{AD}{DB}$.
- **"All rectangles are similar."** Right angles match, but sides need not be proportional. All squares, all circles, and all equilateral triangles are similar.
- **Angles alone for polygons.** AA is a test for triangles only. A square and a non-square rectangle have the same angles but are not similar.

## Practice

1. Is a $4 \times 6$ rectangle similar to a $6 \times 9$ rectangle? To a $6 \times 8$ rectangle?
2. $\triangle PQR \sim \triangle STU$ with $PQ = 10$, $ST = 4$, and $QR = 15$. Find $TU$.
3. In $\triangle ABC$, $\overline{DE} \parallel \overline{BC}$ with $AD = x$, $DB = x + 3$, $AE = 6$, and $EC = 9$. Find $x$.
4. A map uses the scale $1 : 50{,}000$. What actual distance, in kilometers, does $3.2$ cm on the map represent?
5. Two similar triangles have a scale factor of $2 : 5$ (small to large). The small triangle has area $12$ square units. Find the area of the large triangle.
6. Dilate $(-2, 4)$ about the origin by $k = -\tfrac{1}{2}$.
7. A triangle has sides $10$, $14$, and $18$. Find the perimeter of the triangle formed by its three midsegments.
8. One triangle has angles $50^\circ$ and $60^\circ$; another has angles $60^\circ$ and $70^\circ$. Are they similar?

<details>
<summary>Answer key and self-check</summary>

1. $\tfrac{6}{4} = \tfrac{9}{6} = 1.5$, so yes. $\tfrac{6}{4} \ne \tfrac{8}{6}$, so no.
2. $k = \tfrac{4}{10} = 0.4$, so $TU = 0.4 \cdot 15 = 6$.
3. $\tfrac{x}{x + 3} = \tfrac{6}{9}$ gives $9x = 6x + 18$, so $x = 6$. Check: $\tfrac{6}{9} = \tfrac{6}{9}$.
4. $3.2 \cdot 50{,}000 = 160{,}000$ cm $= 1600$ m $= 1.6$ km.
5. Area ratio $\left(\tfrac{5}{2}\right)^2 = 6.25$, so the area is $12 \cdot 6.25 = 75$ square units.
6. $(1, -2)$. The image is on the opposite side of the origin, half as far away.
7. Each midsegment is half a side: $5 + 7 + 9 = 21$.
8. The first triangle's third angle is $70^\circ$ and the second's is $50^\circ$. Both have angles $50^\circ, 60^\circ, 70^\circ$, so they are similar by AA.

Self-check method: compute every ratio of corresponding sides; they must all equal the same $k$. For area answers, divide new by old area and confirm you get $k^2$.

</details>

## Where this fits

This lesson follows [15.4 - Triangles](/154-triangles) in the [Geometry course](/subject/geometry). Next, [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry) uses similar right triangles to prove the Pythagorean theorem and to explain why trigonometric ratios depend only on the angle. Dilations return with the other coordinate transformations in [15.8 - Area, Volume & Coordinate Geometry](/158-area-volume-coordinate-geometry).

## Sources

- OpenStax, *Contemporary Mathematics*, [10.3 Triangles](https://openstax.org/books/contemporary-mathematics/pages/10-3-triangles)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition VI.2](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI2.html), [Proposition VI.4](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI4.html), and [Proposition VI.19](https://mathcs.clarku.edu/~djoyce/java/elements/bookVI/propVI19.html)

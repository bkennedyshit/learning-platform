---
title: "15.6 - Right Triangles & Trigonometry"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.6"
type: chapter
objectives:
  - "Prove the Pythagorean theorem with similar triangles and use it and its converse to find sides and classify triangles"
  - "Find exact side lengths in 45-45-90 and 30-60-90 triangles"
  - "Use sine, cosine, and tangent to find missing sides of right triangles, and inverse trig functions to find angles"
  - "Solve angle-of-elevation and angle-of-depression problems with a labeled diagram"
open_source: true
---

# 15.6 - Right Triangles & Trigonometry

Every right triangle obeys one equation linking its three sides, and every right triangle with a given acute angle has the same side ratios. Those two facts, the Pythagorean theorem and similarity, are the foundation of trigonometry. This lesson proves the theorem, develops the two special right triangles whose ratios are known exactly, and defines sine, cosine, and tangent so you can solve any right triangle from two pieces of information.

## Prerequisites

You need the AA similarity test and scale factors from [15.5 - Similarity & Proportions](/155-similarity-proportions), and the Triangle Sum Theorem and Isosceles Triangle Theorem from [15.4 - Triangles](/154-triangles). You should be able to simplify radicals, for example $\sqrt{50} = 5\sqrt{2}$, and rationalize denominators, for example $\tfrac{9}{\sqrt{3}} = 3\sqrt{3}$. A scientific calculator set to **degree mode** is needed for the trigonometry examples.

## Learning objectives

By the end of this lesson you should be able to:

1. Explain a proof of the Pythagorean theorem using similar triangles.
2. Find a missing side of a right triangle, and use the converse to classify a triangle as acute, right, or obtuse from its side lengths.
3. Find exact lengths in $45^\circ$-$45^\circ$-$90^\circ$ and $30^\circ$-$60^\circ$-$90^\circ$ triangles from any one side.
4. Choose the correct trigonometric ratio to find a missing side, and use an inverse ratio to find a missing angle.
5. Draw and solve angle-of-elevation and angle-of-depression problems.

## Core ideas

### The Pythagorean theorem and its converse

In a right triangle with legs $a$ and $b$ and hypotenuse $c$ (the side opposite the right angle, always the longest):

$$a^2 + b^2 = c^2.$$

**Proof by similarity.** Draw the altitude from the right angle to the hypotenuse; it splits $c$ into segments $p$ (next to leg $a$) and $q$ (next to leg $b$). Each smaller triangle shares an acute angle with the original and has a right angle, so all three triangles are similar by AA. Matching ratios gives $\tfrac{a}{c} = \tfrac{p}{a}$ and $\tfrac{b}{c} = \tfrac{q}{b}$, so $a^2 = cp$ and $b^2 = cq$. Adding, $a^2 + b^2 = c(p + q) = c^2$. Euclid's proof (*Elements* I.47) uses areas of squares instead.

**Converse** (*Elements* I.48): if $a^2 + b^2 = c^2$, the triangle is right. More generally, with $c$ the longest side: if $a^2 + b^2 \gt c^2$ the triangle is acute; if $a^2 + b^2 \lt c^2$ it is obtuse.

Whole-number solutions such as $3$-$4$-$5$, $5$-$12$-$13$, $8$-$15$-$17$, and $7$-$24$-$25$ are **Pythagorean triples**. Any positive multiple of a triple is also a triple.

### Special right triangles

- **$45^\circ$-$45^\circ$-$90^\circ$:** this is an isosceles right triangle. With legs $s$, the hypotenuse is $\sqrt{s^2 + s^2} = s\sqrt{2}$. Sides: $s : s : s\sqrt{2}$.
- **$30^\circ$-$60^\circ$-$90^\circ$:** cut an equilateral triangle of side $2s$ along an altitude. The hypotenuse is $2s$, the short leg (opposite $30^\circ$) is $s$, and the long leg is $\sqrt{(2s)^2 - s^2} = s\sqrt{3}$. Sides: $s : s\sqrt{3} : 2s$.

### Trigonometric ratios

Because all right triangles with the same acute angle $\theta$ are similar, the ratio of any two sides depends only on $\theta$. Label the sides relative to $\theta$: **opposite**, **adjacent** (the leg touching $\theta$), and **hypotenuse**.

$$\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}, \qquad \cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}, \qquad \tan\theta = \frac{\text{opposite}}{\text{adjacent}}.$$

The memory aid is SOH-CAH-TOA. From the special triangles: $\sin 30^\circ = \tfrac{1}{2}$, $\cos 30^\circ = \tfrac{\sqrt{3}}{2}$, $\tan 45^\circ = 1$, and $\sin 60^\circ = \tfrac{\sqrt{3}}{2}$. Since the two acute angles are complementary, $\sin\theta = \cos(90^\circ - \theta)$.

To find an angle from a ratio, use the inverse functions: if $\tan\theta = 0.625$, then $\theta = \tan^{-1}(0.625)$.

### Elevation and depression

An **angle of elevation** is measured upward from the horizontal to a line of sight; an **angle of depression** is measured downward from the horizontal. When an observer looks down at an object, the angle of depression from the observer equals the angle of elevation from the object, because they are alternate interior angles between two horizontal lines.

## Worked examples

### Example 1: Missing sides

1. Legs $9$ and $12$: $c = \sqrt{81 + 144} = \sqrt{225} = 15$. (This is $3$-$4$-$5$ scaled by $3$.)
2. Hypotenuse $13$, leg $5$: $b = \sqrt{169 - 25} = \sqrt{144} = 12$.

### Example 2: Classifying by the converse

1. $7, 24, 25$: $49 + 576 = 625 = 25^2$, so right.
2. $6, 7, 9$: $36 + 49 = 85 \gt 81$, so acute.
3. $5, 7, 10$: $25 + 49 = 74 \lt 100$, so obtuse. (It is a triangle, since $5 + 7 \gt 10$.)

### Example 3: Special triangles

1. A $45^\circ$-$45^\circ$-$90^\circ$ triangle has hypotenuse $10$. Each leg is $\tfrac{10}{\sqrt{2}} = \tfrac{10\sqrt{2}}{2} = 5\sqrt{2} \approx 7.07$.
2. A $30^\circ$-$60^\circ$-$90^\circ$ triangle has hypotenuse $14$. The short leg is $7$ and the long leg is $7\sqrt{3} \approx 12.12$. Check: $49 + 147 = 196 = 14^2$.

### Example 4: Sides from an angle

A right triangle has a $35^\circ$ angle and hypotenuse $20$. Find both legs.

1. Opposite: $\sin 35^\circ = \tfrac{x}{20}$, so $x = 20\sin 35^\circ \approx 20(0.5736) \approx 11.47$.
2. Adjacent: $\cos 35^\circ = \tfrac{y}{20}$, so $y = 20\cos 35^\circ \approx 20(0.8192) \approx 16.38$.
3. Check with Pythagoras: $11.47^2 + 16.38^2 \approx 131.6 + 268.3 \approx 400 = 20^2$.

### Example 5: An angle from two sides

The legs of a right triangle are $5$ and $8$. Find the angle opposite the side of length $5$.

1. Relative to that angle, $5$ is opposite and $8$ is adjacent, so use tangent: $\tan\theta = \tfrac{5}{8} = 0.625$.
2. $\theta = \tan^{-1}(0.625) \approx 32.0^\circ$.
3. The other acute angle is $90 - 32.0 = 58.0^\circ$.

### Example 6: Elevation and depression

These are illustrative measurements.

1. From a point $40$ m from the base of a building, the angle of elevation to the top is $28^\circ$. The height is opposite and $40$ is adjacent: $h = 40\tan 28^\circ \approx 40(0.5317) \approx 21.3$ m.
2. From the top of a $50$ m cliff, the angle of depression to a boat is $12^\circ$. At the boat the angle of elevation is also $12^\circ$, the cliff is opposite, and the horizontal distance $d$ is adjacent: $d = \tfrac{50}{\tan 12^\circ} \approx \tfrac{50}{0.2126} \approx 235.2$ m.

## Common misconceptions and boundary cases

- **Using $a^2 + b^2 = c^2$ in a non-right triangle.** The theorem requires a right angle. For other triangles use the Law of Cosines, which adds a correction term.
- **Putting a leg in the $c$ position.** $c$ is always the hypotenuse. With hypotenuse $13$ and leg $5$, the missing leg is $\sqrt{169 - 25}$, not $\sqrt{169 + 25}$.
- **Calculator in radian mode.** In radian mode, $\sin 35$ returns about $-0.428$, a sign that the mode is wrong.
- **Opposite and adjacent are relative.** They switch when you change which acute angle you are working from. The hypotenuse never changes.
- **Reading $\sin^{-1}$ as a reciprocal.** $\sin^{-1} x$ means the angle whose sine is $x$, not $\tfrac{1}{\sin x}$.
- **Measuring depression from the vertical.** Both elevation and depression are measured from a horizontal line.
- **Rounding too early.** Keep full calculator precision until the final step; rounding intermediate values can shift the answer.

## Practice

1. Find the hypotenuse of a right triangle with legs $8$ and $15$.
2. A right triangle has hypotenuse $26$ and one leg $10$. Find the other leg.
3. Classify the triangle with sides $8$, $11$, and $14$ as acute, right, or obtuse.
4. In a $30^\circ$-$60^\circ$-$90^\circ$ triangle the long leg is $9$. Find the exact short leg and hypotenuse.
5. In a $45^\circ$-$45^\circ$-$90^\circ$ triangle each leg is $7$. Find the exact hypotenuse.
6. A right triangle has an acute angle of $52^\circ$ with adjacent leg $12$. Find the opposite leg and the hypotenuse to two decimal places.
7. An illustrative $6$ m ladder reaches $5.6$ m up a vertical wall. Find the angle the ladder makes with the ground.
8. Using only the special right triangles (no calculator), evaluate $\sin 30^\circ + \cos 60^\circ$ and $\tan 60^\circ \cdot \tan 30^\circ$.

<details>
<summary>Answer key and self-check</summary>

1. $\sqrt{64 + 225} = \sqrt{289} = 17$.
2. $\sqrt{676 - 100} = \sqrt{576} = 24$.
3. $64 + 121 = 185 \lt 196$, so obtuse.
4. Short leg $\tfrac{9}{\sqrt{3}} = 3\sqrt{3}$; hypotenuse $6\sqrt{3}$. Check: $27 + 81 = 108 = (6\sqrt{3})^2$.
5. $7\sqrt{2}$.
6. Opposite $= 12\tan 52^\circ \approx 15.36$; hypotenuse $= \tfrac{12}{\cos 52^\circ} \approx 19.49$. Check: $12^2 + 15.36^2 \approx 379.9 \approx 19.49^2$.
7. $\sin\theta = \tfrac{5.6}{6} \approx 0.9333$, so $\theta \approx 69.0^\circ$.
8. $\tfrac{1}{2} + \tfrac{1}{2} = 1$; $\tan 60^\circ \cdot \tan 30^\circ = \sqrt{3} \cdot \tfrac{1}{\sqrt{3}} = 1$ (the two angles are complementary, so the opposite and adjacent legs swap).

Self-check method: after solving a right triangle, confirm $a^2 + b^2 \approx c^2$, that the hypotenuse is the longest side, and that the larger acute angle is opposite the longer leg.

</details>

## Where this fits

This lesson follows [15.5 - Similarity & Proportions](/155-similarity-proportions) in the [Geometry course](/subject/geometry). Next, [15.7 - Circles](/157-circles) uses the Pythagorean theorem with tangents and chords. The special-triangle values here become the unit-circle coordinates in [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle), and the Law of Sines and Law of Cosines for non-right triangles are developed in [16.5 - Trig Identities & Equations](/165-trig-identities-equations).

## Sources

- OpenStax, *Contemporary Mathematics*, [10.8 Right Triangle Trigonometry](https://openstax.org/books/contemporary-mathematics/pages/10-8-right-triangle-trigonometry)
- OpenStax, *Algebra and Trigonometry 2e*, [7.2 Right Triangle Trigonometry](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry)
- Euclid, *Elements*, ed. D. E. Joyce (Clark University), [Proposition I.47](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI47.html) and [Proposition I.48](https://mathcs.clarku.edu/~djoyce/java/elements/bookI/propI48.html)

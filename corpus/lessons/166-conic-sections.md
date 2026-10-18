---
title: "16.6 - Conic Sections"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.6"
type: chapter
objectives:
  - "Write circles, parabolas, ellipses, and hyperbolas in standard form by completing the square"
  - "Find the center, vertices, foci, directrix, asymptotes, and eccentricity from a standard-form equation"
  - "Identify the type of conic from the coefficients of its general second-degree equation"
  - "Convert simple parametric equations of a circle or ellipse to rectangular form"
open_source: true
---

# 16.6 - Conic Sections

Slice a double cone with a plane and the cut traces a circle, an ellipse, a parabola, or a hyperbola. Each of these curves also has a distance definition and a second-degree equation in $x$ and $y$, and those equations are what let you locate the key points of the curve from algebra. Conics describe planetary orbits, the shape of satellite dishes and headlight reflectors, and the paths of objects under gravity.

## Prerequisites

You need the distance formula and completing the square. Completing the square appears when finding the vertex of a parabola in [14.8 - Factoring & Quadratics](/148-factoring-quadratics). The sine–cosine relationship $\cos^2 t + \sin^2 t = 1$ from [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle) is used for parametric equations.

## Learning objectives

By the end of this lesson you should be able to:

1. Complete the square to put a conic in standard form and state its center or vertex.
2. Find the focus and directrix of a parabola, the vertices and foci of an ellipse or hyperbola, the asymptotes of a hyperbola, and the eccentricity of an ellipse or hyperbola.
3. Identify a conic from the general equation $Ax^2 + Cy^2 + Dx + Ey + F = 0$.
4. Eliminate the parameter from $x = a\cos t$, $y = b\sin t$ to recognize an ellipse.

## Core ideas

### Circle

A **circle** is the set of points at distance $r$ from a center $(h, k)$:

$$(x - h)^2 + (y - k)^2 = r^2.$$

### Parabola

A **parabola** is the set of points equidistant from a fixed point (the **focus**) and a fixed line (the **directrix**). With vertex at the origin:

- $x^2 = 4py$ opens up if $p \gt 0$ and down if $p \lt 0$; the focus is $(0, p)$ and the directrix is $y = -p$.
- $y^2 = 4px$ opens right if $p \gt 0$ and left if $p \lt 0$; the focus is $(p, 0)$ and the directrix is $x = -p$.

The **latus rectum** is the chord through the focus perpendicular to the axis; its length is $|4p|$. Replacing $x$ by $x - h$ and $y$ by $y - k$ moves the vertex to $(h, k)$.

### Ellipse

An **ellipse** is the set of points whose distances to two foci have a constant sum $2a$. Centered at the origin with $a \gt b \gt 0$:

- Horizontal major axis: $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$, vertices $(\pm a, 0)$, co-vertices $(0, \pm b)$, foci $(\pm c, 0)$.
- Vertical major axis: $\dfrac{x^2}{b^2} + \dfrac{y^2}{a^2} = 1$, vertices $(0, \pm a)$, foci $(0, \pm c)$.

In both cases $c^2 = a^2 - b^2$ and the **eccentricity** is $e = \tfrac{c}{a}$, with $0 \lt e \lt 1$. An eccentricity near $0$ means the ellipse is nearly a circle.

### Hyperbola

A **hyperbola** is the set of points whose distances to two foci have a constant difference $2a$. Centered at the origin:

- Horizontal transverse axis: $\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1$, vertices $(\pm a, 0)$, foci $(\pm c, 0)$, asymptotes $y = \pm\tfrac{b}{a}x$.
- Vertical transverse axis: $\dfrac{y^2}{a^2} - \dfrac{x^2}{b^2} = 1$, vertices $(0, \pm a)$, foci $(0, \pm c)$, asymptotes $y = \pm\tfrac{a}{b}x$.

Here $c^2 = a^2 + b^2$ and $e = \tfrac{c}{a} \gt 1$.

### Identifying a conic from its general form

For $Ax^2 + Cy^2 + Dx + Ey + F = 0$ (no $xy$ term), assuming the graph is not degenerate:

- $A = C$: circle.
- $AC \gt 0$ with $A \neq C$: ellipse.
- $AC \lt 0$: hyperbola.
- $AC = 0$ (exactly one squared term): parabola.

When an $xy$ term is present, as in $Ax^2 + Bxy + Cy^2 + \cdots = 0$, the discriminant $B^2 - 4AC$ decides: negative for an ellipse or circle, zero for a parabola, positive for a hyperbola. The $xy$ term means the axes of the conic are rotated.

### Parametric equations

The equations $x = a\cos t$, $y = b\sin t$ trace a point as $t$ varies. Dividing by $a$ and $b$ and using $\cos^2 t + \sin^2 t = 1$ gives $\tfrac{x^2}{a^2} + \tfrac{y^2}{b^2} = 1$, an ellipse (a circle when $a = b$).

## Worked examples

### Example 1: A circle by completing the square

Find the center and radius of $x^2 + y^2 - 6x + 4y - 12 = 0$.

1. Group and move the constant: $(x^2 - 6x) + (y^2 + 4y) = 12$.
2. Complete each square, adding to both sides: $(x^2 - 6x + 9) + (y^2 + 4y + 4) = 12 + 9 + 4$.
3. $(x - 3)^2 + (y + 2)^2 = 25$, so the center is $(3, -2)$ and the radius is $5$.

### Example 2: A parabola's focus and directrix

Analyze $y^2 = 12x$.

1. Match $y^2 = 4px$: $4p = 12$, so $p = 3$.
2. The vertex is $(0, 0)$, the parabola opens right, the focus is $(3, 0)$, and the directrix is $x = -3$.
3. The latus rectum has length $12$; its endpoints are $(3, 6)$ and $(3, -6)$. Check: $6^2 = 36 = 12 \cdot 3$.

### Example 3: An ellipse

Analyze $9x^2 + 25y^2 = 225$.

1. Divide by $225$: $\dfrac{x^2}{25} + \dfrac{y^2}{9} = 1$.
2. The larger denominator is under $x^2$, so the major axis is horizontal with $a = 5$ and $b = 3$.
3. $c^2 = 25 - 9 = 16$, so $c = 4$.
4. Vertices $(\pm 5, 0)$, co-vertices $(0, \pm 3)$, foci $(\pm 4, 0)$, eccentricity $\tfrac{4}{5} = 0.8$.

### Example 4: A vertical hyperbola

Analyze $\dfrac{y^2}{16} - \dfrac{x^2}{9} = 1$.

1. The positive term contains $y$, so the transverse axis is vertical with $a = 4$ and $b = 3$.
2. $c^2 = 16 + 9 = 25$, so $c = 5$.
3. Vertices $(0, \pm 4)$, foci $(0, \pm 5)$, asymptotes $y = \pm\tfrac{4}{3}x$, eccentricity $\tfrac{5}{4}$.

### Example 5: Identify, then write in standard form

Identify the conic $4x^2 - 9y^2 - 16x - 18y - 29 = 0$ and write it in standard form.

1. $A = 4$ and $C = -9$, so $AC \lt 0$: a hyperbola.
2. Group and factor the leading coefficients: $4(x^2 - 4x) - 9(y^2 + 2y) = 29$.
3. Complete the squares. Inside the parentheses add $4$ and $1$; that adds $4 \cdot 4 = 16$ and $-9 \cdot 1 = -9$ to the left side, so add the same to the right: $4(x - 2)^2 - 9(y + 1)^2 = 29 + 16 - 9 = 36$.
4. Divide by $36$: $\dfrac{(x - 2)^2}{9} - \dfrac{(y + 1)^2}{4} = 1$.
5. Center $(2, -1)$, $a = 3$, $b = 2$, $c = \sqrt{13}$. Vertices $(5, -1)$ and $(-1, -1)$; asymptotes $y + 1 = \pm\tfrac{2}{3}(x - 2)$.

Check: expanding $4(x - 2)^2 - 9(y + 1)^2 - 36$ gives $4x^2 - 16x + 16 - 9y^2 - 18y - 9 - 36$, which is the original left side.

## Common misconceptions and boundary cases

- **Assuming $a$ always goes with $x$.** In an ellipse, $a$ is the square root of the **larger** denominator, wherever it appears. In a hyperbola, $a$ goes with the **positive** term.
- **Mixing up the $c$ relationships.** For an ellipse $c^2 = a^2 - b^2$, so the foci are inside the curve. For a hyperbola $c^2 = a^2 + b^2$, so the foci are beyond the vertices.
- **Completing the square unevenly.** In Example 5, adding $4$ inside $4(x^2 - 4x + \underline{\ \ })$ adds $16$ to the left side, not $4$. Multiply by the factored coefficient before balancing.
- **Sign of the center.** $(x + 3)^2$ means $h = -3$, because $x + 3 = x - (-3)$.
- **Degenerate cases.** Not every second-degree equation has a curve. $x^2 + y^2 + 2x + 5 = 0$ becomes $(x + 1)^2 + y^2 = -4$, which no real point satisfies. Likewise $x^2 - y^2 = 0$ is a pair of lines, not a hyperbola.

## Practice

1. Find the center and radius of $x^2 + y^2 + 8x - 2y + 8 = 0$.
2. Write the equation of the parabola with vertex $(0, 0)$ and focus $(0, -2)$, and give its directrix.
3. Write the equation of the ellipse with vertices $(0, \pm 13)$ and foci $(0, \pm 12)$.
4. Find the vertices, foci, and asymptotes of $\dfrac{x^2}{36} - \dfrac{y^2}{64} = 1$.
5. Identify each conic: (a) $3x^2 + 3y^2 - 6x + 12y = 0$; (b) $2x^2 + 5y^2 - 20 = 0$; (c) $y^2 - 8x + 2y + 17 = 0$; (d) $x^2 - 4y^2 + 4 = 0$.
6. Eliminate the parameter from $x = 3\cos t$, $y = 2\sin t$ and name the curve.
7. An illustrative dish antenna has a parabolic cross-section $y = \tfrac{x^2}{16}$, with $x$ and $y$ in inches. How far above the vertex should the receiver sit so that it is at the focus?

<details>
<summary>Answer key and self-check</summary>

1. $(x + 4)^2 + (y - 1)^2 = -8 + 16 + 1 = 9$. Center $(-4, 1)$, radius $3$.
2. $x^2 = 4py$ with $p = -2$: $x^2 = -8y$. Directrix $y = 2$.
3. $a = 13$, $c = 12$, $b^2 = 169 - 144 = 25$. Equation $\dfrac{x^2}{25} + \dfrac{y^2}{169} = 1$.
4. $a = 6$, $b = 8$, $c = \sqrt{36 + 64} = 10$. Vertices $(\pm 6, 0)$, foci $(\pm 10, 0)$, asymptotes $y = \pm\tfrac{4}{3}x$.
5. (a) circle, $A = C = 3$; it is $(x - 1)^2 + (y + 2)^2 = 5$. (b) ellipse, $AC = 10 \gt 0$; it is $\tfrac{x^2}{10} + \tfrac{y^2}{4} = 1$. (c) parabola, only $y$ is squared. (d) hyperbola, $AC = -4 \lt 0$; it is $y^2 - \tfrac{x^2}{4} = 1$.
6. $\left(\tfrac{x}{3}\right)^2 + \left(\tfrac{y}{2}\right)^2 = \cos^2 t + \sin^2 t = 1$, so $\dfrac{x^2}{9} + \dfrac{y^2}{4} = 1$, an ellipse.
7. $x^2 = 16y$, so $4p = 16$ and $p = 4$. The focus is $4$ inches above the vertex.

Self-check method: pick a point you found, such as a vertex or the endpoint of a latus rectum, and substitute it into the original equation. For ellipses and hyperbolas, also check that $c$ satisfies the correct relation with $a$ and $b$.

</details>

## Where this fits

This lesson follows [16.5 - Trig Identities & Equations](/165-trig-identities-equations) in the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). Ellipses, parabolas, and hyperbolas reappear as orbit shapes in [Orbital Elements & Conic Sections](/orbital-elements-conic-sections). The next lesson, [16.7 - Sequences, Series & the Binomial Theorem](/167-sequences-series-the-binomial-theorem), turns from curves to patterns in lists of numbers.

## Sources

- OpenStax, *Intermediate Algebra 2e*, [11.1 Distance and Midpoint Formulas; Circles](https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles)
- OpenStax, *Precalculus 2e*, [10.1 The Ellipse](https://openstax.org/books/precalculus-2e/pages/10-1-the-ellipse)
- OpenStax, *Precalculus 2e*, [10.2 The Hyperbola](https://openstax.org/books/precalculus-2e/pages/10-2-the-hyperbola)
- OpenStax, *Precalculus 2e*, [10.3 The Parabola](https://openstax.org/books/precalculus-2e/pages/10-3-the-parabola)
- OpenStax, *Precalculus 2e*, [10.4 Rotation of Axes](https://openstax.org/books/precalculus-2e/pages/10-4-rotation-of-axes)
- OpenStax, *Precalculus 2e*, [8.6 Parametric Equations](https://openstax.org/books/precalculus-2e/pages/8-6-parametric-equations)

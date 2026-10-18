---
title: "16.5 - Trig Identities & Equations"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.5"
type: chapter
objectives:
  - "Verify trigonometric identities using reciprocal, quotient, Pythagorean, and even/odd identities"
  - "Compute exact values with the sum, difference, and double-angle formulas"
  - "Solve trigonometric equations on one period and write their general solutions"
  - "Solve non-right triangles with the Law of Sines and the Law of Cosines"
open_source: true
---

# 16.5 - Trig Identities & Equations

An identity is an equation that is true for every input where both sides are defined; a trig equation is true only for particular angles. This lesson uses the unit-circle definitions to build the core identities, applies the sum and double-angle formulas to find exact values, solves trig equations, and extends trigonometry to triangles that do not have a right angle.

## Prerequisites

You need the unit-circle values, reference angles, and quadrant signs from [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle), and factoring of quadratics from [14.8 - Factoring & Quadratics](/148-factoring-quadratics). Many trig equations are quadratics in disguise, with $\sin x$ or $\cos x$ in place of $x$.

## Learning objectives

By the end of this lesson you should be able to:

1. Verify an identity by transforming one side into the other, using reciprocal, quotient, Pythagorean, and even/odd identities.
2. Find exact values such as $\cos 15^\circ$ with the sum and difference formulas, and find $\sin 2\theta$ and $\cos 2\theta$ from one given value.
3. Solve linear and quadratic trig equations on $[0, 2\pi)$ and state the general solution.
4. Use the Law of Sines and the Law of Cosines to find missing sides and angles of a triangle.

## Core ideas

### Fundamental identities

- Reciprocal: $\csc x = \dfrac{1}{\sin x}$, $\sec x = \dfrac{1}{\cos x}$, $\cot x = \dfrac{1}{\tan x}$.
- Quotient: $\tan x = \dfrac{\sin x}{\cos x}$, $\cot x = \dfrac{\cos x}{\sin x}$.
- Pythagorean: $\sin^2 x + \cos^2 x = 1$. Dividing by $\cos^2 x$ gives $\tan^2 x + 1 = \sec^2 x$; dividing by $\sin^2 x$ gives $1 + \cot^2 x = \csc^2 x$.
- Even/odd: $\cos(-x) = \cos x$, while $\sin(-x) = -\sin x$ and $\tan(-x) = -\tan x$.
- Cofunction: $\sin\left(\tfrac{\pi}{2} - x\right) = \cos x$ and $\cos\left(\tfrac{\pi}{2} - x\right) = \sin x$.

### Sum, difference, and double-angle formulas

$$\sin(A \pm B) = \sin A \cos B \pm \cos A \sin B$$

$$\cos(A \pm B) = \cos A \cos B \mp \sin A \sin B$$

Setting $A = B = \theta$ gives the double-angle formulas:

$$\sin 2\theta = 2\sin\theta\cos\theta, \qquad \cos 2\theta = \cos^2\theta - \sin^2\theta = 1 - 2\sin^2\theta = 2\cos^2\theta - 1.$$

Solving $\cos 2\theta = 1 - 2\sin^2\theta$ for $\sin^2\theta$ leads to the half-angle formulas, such as $\sin^2\tfrac{\theta}{2} = \tfrac{1 - \cos\theta}{2}$.

### Verifying identities

Work on **one side only**, usually the more complicated one, and transform it step by step until it matches the other side. Useful moves: rewrite everything in sines and cosines, combine fractions over a common denominator, factor, and substitute a Pythagorean identity.

### Solving trig equations

1. Isolate a single trig function, or factor so each factor contains one trig function.
2. Solve each piece on one period, such as $[0, 2\pi)$, using reference angles.
3. If the general solution is requested, add the period: $2\pi k$ for sine and cosine, $\pi k$ for tangent, where $k$ is any integer.

### Non-right triangles

For a triangle with angles $A$, $B$, $C$ opposite sides $a$, $b$, $c$:

- **Law of Sines:** $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C}$. Use it when you know an angle and its opposite side.
- **Law of Cosines:** $a^2 = b^2 + c^2 - 2bc\cos A$. Use it for two sides and the included angle (SAS) or for three sides (SSS).

## Worked examples

### Example 1: Verifying an identity

Verify $\sec x - \cos x = \sin x \tan x$.

1. Start with the left side and rewrite in cosines: $\sec x - \cos x = \dfrac{1}{\cos x} - \cos x$.
2. Use a common denominator: $\dfrac{1 - \cos^2 x}{\cos x}$.
3. Pythagorean identity: $1 - \cos^2 x = \sin^2 x$, so the expression is $\dfrac{\sin^2 x}{\cos x}$.
4. Split: $\sin x \cdot \dfrac{\sin x}{\cos x} = \sin x \tan x$, which is the right side.

### Example 2: An exact value from a difference formula

Find $\cos 15^\circ$ exactly.

1. Write $15^\circ = 45^\circ - 30^\circ$.
2. $\cos(45^\circ - 30^\circ) = \cos 45^\circ \cos 30^\circ + \sin 45^\circ \sin 30^\circ$.
3. Substitute: $\dfrac{\sqrt{2}}{2} \cdot \dfrac{\sqrt{3}}{2} + \dfrac{\sqrt{2}}{2} \cdot \dfrac{1}{2} = \dfrac{\sqrt{6} + \sqrt{2}}{4}$.
4. Check: $\dfrac{2.449 + 1.414}{4} \approx 0.9659$, and a calculator gives $\cos 15^\circ \approx 0.9659$.

### Example 3: Double-angle values

If $\sin\theta = \tfrac{3}{5}$ and $\theta$ is in Quadrant II, find $\sin 2\theta$ and $\cos 2\theta$.

1. $\cos^2\theta = 1 - \tfrac{9}{25} = \tfrac{16}{25}$, and cosine is negative in Quadrant II, so $\cos\theta = -\tfrac{4}{5}$.
2. $\sin 2\theta = 2 \cdot \tfrac{3}{5} \cdot \left(-\tfrac{4}{5}\right) = -\tfrac{24}{25}$.
3. $\cos 2\theta = \tfrac{16}{25} - \tfrac{9}{25} = \tfrac{7}{25}$.
4. Check: $\left(-\tfrac{24}{25}\right)^2 + \left(\tfrac{7}{25}\right)^2 = \tfrac{576 + 49}{625} = 1$.

### Example 4: A quadratic trig equation

Solve $2\cos^2 x - \cos x - 1 = 0$ on $[0, 2\pi)$.

1. Treat $\cos x$ as the variable and factor: $(2\cos x + 1)(\cos x - 1) = 0$.
2. $\cos x = -\tfrac{1}{2}$: reference angle $\tfrac{\pi}{3}$ in Quadrants II and III, so $x = \tfrac{2\pi}{3}$ or $x = \tfrac{4\pi}{3}$.
3. $\cos x = 1$: $x = 0$.
4. Solutions: $0, \tfrac{2\pi}{3}, \tfrac{4\pi}{3}$. The general solution is $x = 2\pi k$, $x = \tfrac{2\pi}{3} + 2\pi k$, or $x = \tfrac{4\pi}{3} + 2\pi k$.

### Example 5: Law of Cosines, then Law of Sines

In triangle $ABC$, $b = 5$, $c = 7$, and $A = 60^\circ$. Find $a$, $B$, and $C$.

1. SAS, so start with the Law of Cosines: $a^2 = 25 + 49 - 2(5)(7)\cos 60^\circ = 74 - 35 = 39$, so $a = \sqrt{39} \approx 6.245$.
2. Law of Sines for $B$: $\sin B = \dfrac{b \sin A}{a} = \dfrac{5(0.8660)}{6.245} \approx 0.6934$, so $B \approx 43.9^\circ$. Since $b$ is the shortest side, $B$ is the smallest angle and must be acute, so there is no second option.
3. $C = 180^\circ - 60^\circ - 43.9^\circ \approx 76.1^\circ$.
4. Check with the Law of Sines: $\dfrac{a}{\sin A} \approx 7.211$ and $7.211 \sin 76.1^\circ \approx 7.00 = c$.

## Common misconceptions and boundary cases

- **Distributing a trig function.** $\sin(A + B) \neq \sin A + \sin B$. With $A = B = \tfrac{\pi}{4}$, $\sin\tfrac{\pi}{2} = 1$ but $\sin\tfrac{\pi}{4} + \sin\tfrac{\pi}{4} = \sqrt{2} \approx 1.414$. Similarly, $\sin 2x \neq 2\sin x$.
- **Dividing by a trig function.** In $\sin 2x = \sin x$, dividing by $\sin x$ loses the solutions where $\sin x = 0$. Instead write $2\sin x\cos x - \sin x = \sin x(2\cos x - 1) = 0$, giving $x = 0, \pi$ from $\sin x = 0$ and $x = \tfrac{\pi}{3}, \tfrac{5\pi}{3}$ from $\cos x = \tfrac{1}{2}$.
- **Treating an identity as an equation to solve.** When verifying, do not move terms across the equals sign; that assumes what you are trying to prove. Transform one side until it matches.
- **Stopping at one solution.** $\sin x = \tfrac{1}{2}$ has two solutions per period, $\tfrac{\pi}{6}$ and $\tfrac{5\pi}{6}$. A calculator's inverse sine returns only one of them.
- **The ambiguous case.** Given two sides and a non-included angle (SSA), the Law of Sines can produce zero, one, or two triangles, because $\sin B = \sin(180^\circ - B)$. Check whether $180^\circ - B$ also fits with the known angle.

## Practice

1. Simplify $\sin x \csc x - \cos^2 x$.
2. Verify $(1 + \tan^2 x)\cos^2 x = 1$.
3. Find $\sin 75^\circ$ exactly.
4. If $\cos\theta = -\tfrac{5}{13}$ and $\theta$ is in Quadrant III, find $\sin 2\theta$ and $\cos 2\theta$.
5. Solve $2\cos x + \sqrt{3} = 0$ on $[0, 2\pi)$.
6. Solve $\tan^2 x = 3$ on $[0, 2\pi)$.
7. Solve $2\sin^2 x + \sin x - 1 = 0$ on $[0, 2\pi)$.
8. In triangle $ABC$, $A = 40^\circ$, $B = 75^\circ$, and $a = 10$. Find $C$, $b$, and $c$ to one decimal place.
9. Write the general solution of $\cos x = 0$.

<details>
<summary>Answer key and self-check</summary>

1. $\sin x \csc x = 1$, so the expression is $1 - \cos^2 x = \sin^2 x$.
2. $1 + \tan^2 x = \sec^2 x$, and $\sec^2 x \cos^2 x = \dfrac{1}{\cos^2 x} \cdot \cos^2 x = 1$.
3. $\sin(45^\circ + 30^\circ) = \tfrac{\sqrt{2}}{2} \cdot \tfrac{\sqrt{3}}{2} + \tfrac{\sqrt{2}}{2} \cdot \tfrac{1}{2} = \dfrac{\sqrt{6} + \sqrt{2}}{4} \approx 0.9659$.
4. $\sin\theta = -\tfrac{12}{13}$. $\sin 2\theta = 2\left(-\tfrac{12}{13}\right)\left(-\tfrac{5}{13}\right) = \tfrac{120}{169}$; $\cos 2\theta = \tfrac{25}{169} - \tfrac{144}{169} = -\tfrac{119}{169}$.
5. $\cos x = -\tfrac{\sqrt{3}}{2}$, so $x = \tfrac{5\pi}{6}$ or $x = \tfrac{7\pi}{6}$.
6. $\tan x = \pm\sqrt{3}$, so $x = \tfrac{\pi}{3}, \tfrac{2\pi}{3}, \tfrac{4\pi}{3}, \tfrac{5\pi}{3}$.
7. $(2\sin x - 1)(\sin x + 1) = 0$. $\sin x = \tfrac{1}{2}$ gives $\tfrac{\pi}{6}, \tfrac{5\pi}{6}$; $\sin x = -1$ gives $\tfrac{3\pi}{2}$.
8. $C = 65^\circ$. $b = \dfrac{10\sin 75^\circ}{\sin 40^\circ} \approx 15.0$ and $c = \dfrac{10\sin 65^\circ}{\sin 40^\circ} \approx 14.1$.
9. $x = \tfrac{\pi}{2} + k\pi$ for any integer $k$.

Self-check method: substitute each solution into the original equation with a calculator in radian mode, and test a claimed identity at two or three angles such as $x = 0.5$ and $x = 1$. A numerical test cannot prove an identity, but a single failure disproves it.

</details>

## Where this fits

This lesson builds on [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle) in the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). The identity $\cos^2 t + \sin^2 t = 1$ is what turns the parametric equations in [16.6 - Conic Sections](/166-conic-sections) back into the equations of circles and ellipses. Sum formulas and the limit $\tfrac{\sin x}{x} \to 1$ as $x \to 0$ are the tools used to differentiate sine and cosine in calculus.

## Sources

- OpenStax, *Precalculus 2e*, [7.1 Simplifying and Verifying Trigonometric Identities](https://openstax.org/books/precalculus-2e/pages/7-1-solving-trigonometric-equations-with-identities)
- OpenStax, *Precalculus 2e*, [7.2 Sum and Difference Identities](https://openstax.org/books/precalculus-2e/pages/7-2-sum-and-difference-identities)
- OpenStax, *Precalculus 2e*, [7.3 Double-Angle, Half-Angle, and Reduction Formulas](https://openstax.org/books/precalculus-2e/pages/7-3-double-angle-half-angle-and-reduction-formulas)
- OpenStax, *Precalculus 2e*, [7.5 Solving Trigonometric Equations](https://openstax.org/books/precalculus-2e/pages/7-5-solving-trigonometric-equations)
- OpenStax, *Precalculus 2e*, [8.1 Non-right Triangles: Law of Sines](https://openstax.org/books/precalculus-2e/pages/8-1-non-right-triangles-law-of-sines)
- OpenStax, *Precalculus 2e*, [8.2 Non-right Triangles: Law of Cosines](https://openstax.org/books/precalculus-2e/pages/8-2-non-right-triangles-law-of-cosines)

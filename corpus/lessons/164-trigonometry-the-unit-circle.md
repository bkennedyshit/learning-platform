---
title: "16.4 - Trigonometry — The Unit Circle"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.4"
type: chapter
objectives:
  - "Convert angle measures between degrees and radians and find coterminal angles"
  - "Define sine and cosine as coordinates of a point on the unit circle and derive the other four trig functions"
  - "Use reference angles and quadrant signs to evaluate trig functions of special angles exactly"
  - "Find all trig values of an angle from one given value and its quadrant"
open_source: true
---

# 16.4 - Trigonometry — The Unit Circle

Right-triangle trigonometry only works for angles between $0^\circ$ and $90^\circ$. The unit circle extends sine, cosine, and the other trig functions to every angle, positive or negative, which is what makes them useful for rotation, waves, and anything periodic. This lesson introduces radian measure, defines the six trig functions on the unit circle, and shows how to evaluate them exactly for the special angles.

## Prerequisites

You should know the Pythagorean theorem and the side ratios of the $30^\circ$-$60^\circ$-$90^\circ$ and $45^\circ$-$45^\circ$-$90^\circ$ triangles, which are covered in the Geometry lesson [15.6 - Right Triangles & Trigonometry](/156-right-triangles-trigonometry). You also need to simplify radicals and rationalize denominators, for example $\tfrac{1}{\sqrt{2}} = \tfrac{\sqrt{2}}{2}$.

## Learning objectives

By the end of this lesson you should be able to:

1. Convert between degrees and radians and find a coterminal angle in $[0, 2\pi)$.
2. State the coordinates of the unit-circle point for each special angle and read off its sine and cosine.
3. Compute tangent, cotangent, secant, and cosecant from sine and cosine, and identify when each is undefined.
4. Use a reference angle and the quadrant to evaluate trig functions of any special angle exactly.
5. Given one trig value and the quadrant, find the remaining trig values.

## Core ideas

### Angles and radians

An angle is in **standard position** when its vertex is at the origin and its initial side lies on the positive $x$-axis. Counterclockwise rotation gives a positive angle; clockwise gives a negative angle. Angles that share a terminal side are **coterminal**; they differ by a multiple of $360^\circ$, or $2\pi$.

The **radian** measure of a central angle is the arc length it cuts off divided by the radius: $\theta = \tfrac{s}{r}$. A full circle has circumference $2\pi r$, so $360^\circ = 2\pi$ radians and

$$180^\circ = \pi \text{ radians}.$$

To convert degrees to radians multiply by $\tfrac{\pi}{180}$; to convert radians to degrees multiply by $\tfrac{180}{\pi}$. Rearranging the definition gives the arc-length formula $s = r\theta$, valid only when $\theta$ is in radians.

### The unit circle definitions

The **unit circle** is $x^2 + y^2 = 1$. If the terminal side of angle $\theta$ meets the unit circle at $(x, y)$, then

$$\cos\theta = x, \qquad \sin\theta = y,$$

$$\tan\theta = \frac{y}{x}, \quad \cot\theta = \frac{x}{y}, \quad \sec\theta = \frac{1}{x}, \quad \csc\theta = \frac{1}{y},$$

whenever the denominator is not zero. Because $(x, y)$ is on the circle, $\cos^2\theta + \sin^2\theta = 1$ for every angle.

### Special angles in Quadrant I

| $\theta$ | $0$ | $\tfrac{\pi}{6}$ ($30^\circ$) | $\tfrac{\pi}{4}$ ($45^\circ$) | $\tfrac{\pi}{3}$ ($60^\circ$) | $\tfrac{\pi}{2}$ ($90^\circ$) |
|---|---|---|---|---|---|
| $\cos\theta$ | $1$ | $\tfrac{\sqrt{3}}{2}$ | $\tfrac{\sqrt{2}}{2}$ | $\tfrac{1}{2}$ | $0$ |
| $\sin\theta$ | $0$ | $\tfrac{1}{2}$ | $\tfrac{\sqrt{2}}{2}$ | $\tfrac{\sqrt{3}}{2}$ | $1$ |

These values come from the special right triangles with hypotenuse $1$.

### Reference angles and signs

The **reference angle** of $\theta$ is the acute angle between its terminal side and the $x$-axis. A trig function of $\theta$ has the same absolute value as the same function of its reference angle; only the sign can change. The sign depends on the quadrant:

- Quadrant I: all six functions are positive.
- Quadrant II: $x \lt 0$, $y \gt 0$, so sine and cosecant are positive.
- Quadrant III: $x \lt 0$, $y \lt 0$, so tangent and cotangent are positive.
- Quadrant IV: $x \gt 0$, $y \lt 0$, so cosine and secant are positive.

## Worked examples

### Example 1: Converting angle measures

1. $150^\circ \cdot \tfrac{\pi}{180} = \tfrac{150\pi}{180} = \tfrac{5\pi}{6}$.
2. $\tfrac{7\pi}{4} \cdot \tfrac{180}{\pi} = 7 \cdot 45^\circ = 315^\circ$.
3. $2$ radians $= 2 \cdot \tfrac{180^\circ}{\pi} \approx 114.6^\circ$. An angle without a degree symbol is in radians.

### Example 2: Evaluating at a Quadrant II angle

Find $\sin$, $\cos$, and $\tan$ of $\tfrac{5\pi}{6}$.

1. $\tfrac{5\pi}{6}$ is between $\tfrac{\pi}{2}$ and $\pi$, so it is in Quadrant II.
2. Reference angle: $\pi - \tfrac{5\pi}{6} = \tfrac{\pi}{6}$.
3. Use the $\tfrac{\pi}{6}$ values with Quadrant II signs: $\cos\tfrac{5\pi}{6} = -\tfrac{\sqrt{3}}{2}$ and $\sin\tfrac{5\pi}{6} = \tfrac{1}{2}$.
4. $\tan\tfrac{5\pi}{6} = \dfrac{1/2}{-\sqrt{3}/2} = -\dfrac{1}{\sqrt{3}} = -\dfrac{\sqrt{3}}{3}$.

### Example 3: All six functions of a Quadrant III angle

Find all six trig values of $\tfrac{4\pi}{3}$.

1. $\tfrac{4\pi}{3} = \pi + \tfrac{\pi}{3}$, so it is in Quadrant III with reference angle $\tfrac{\pi}{3}$.
2. The unit-circle point is $\left(-\tfrac{1}{2}, -\tfrac{\sqrt{3}}{2}\right)$, so $\cos\tfrac{4\pi}{3} = -\tfrac{1}{2}$ and $\sin\tfrac{4\pi}{3} = -\tfrac{\sqrt{3}}{2}$.
3. $\tan = \dfrac{-\sqrt{3}/2}{-1/2} = \sqrt{3}$, and $\cot = \dfrac{1}{\sqrt{3}} = \dfrac{\sqrt{3}}{3}$.
4. $\sec = \dfrac{1}{-1/2} = -2$, and $\csc = \dfrac{1}{-\sqrt{3}/2} = -\dfrac{2\sqrt{3}}{3}$.

Check the signs: in Quadrant III only tangent and cotangent are positive, which matches.

### Example 4: A negative angle

Evaluate $\sin(-405^\circ)$, $\cos(-405^\circ)$, and $\tan(-405^\circ)$.

1. Add $720^\circ$ to find a coterminal angle: $-405^\circ + 720^\circ = 315^\circ$.
2. $315^\circ$ is in Quadrant IV with reference angle $45^\circ$.
3. $\cos = \tfrac{\sqrt{2}}{2}$, $\sin = -\tfrac{\sqrt{2}}{2}$, and $\tan = -1$.

### Example 5: From one value to the rest

Suppose $\sin\theta = -\tfrac{3}{5}$ and $\theta$ is in Quadrant III. Find $\cos\theta$ and $\tan\theta$.

1. From $\cos^2\theta + \sin^2\theta = 1$: $\cos^2\theta = 1 - \tfrac{9}{25} = \tfrac{16}{25}$, so $\cos\theta = \pm\tfrac{4}{5}$.
2. Cosine is negative in Quadrant III, so $\cos\theta = -\tfrac{4}{5}$.
3. $\tan\theta = \dfrac{-3/5}{-4/5} = \dfrac{3}{4}$, which is positive, as expected in Quadrant III.

## Common misconceptions and boundary cases

- **Calculator in the wrong mode.** $\sin 30^\circ = 0.5$, but a calculator in radian mode computes $\sin(30 \text{ rad}) \approx -0.988$. Check the mode before every calculation.
- **Measuring the reference angle to the $y$-axis.** The reference angle is always measured to the $x$-axis. For $120^\circ$ it is $60^\circ$, not $30^\circ$.
- **Dropping the sign after using the identity.** $\cos^2\theta = \tfrac{16}{25}$ has two roots; the quadrant decides which one is correct.
- **Undefined values.** $\tan\tfrac{\pi}{2}$ and $\sec\tfrac{\pi}{2}$ are undefined because $x = 0$ there, and $\cot 0$ and $\csc 0$ are undefined because $y = 0$. They are not equal to $0$ or to infinity.
- **Using $s = r\theta$ with degrees.** The arc length of a $60^\circ$ arc on a circle of radius $3$ is $3 \cdot \tfrac{\pi}{3} = \pi$, not $3 \cdot 60 = 180$.

## Practice

1. Convert $225^\circ$ to radians and $\tfrac{11\pi}{6}$ to degrees.
2. Find the reference angle of $300^\circ$ and of $\tfrac{7\pi}{6}$.
3. Find $\sin$, $\cos$, and $\tan$ of $\tfrac{3\pi}{4}$ exactly.
4. Find all six trig values of $\tfrac{11\pi}{6}$.
5. Find a coterminal angle for $\tfrac{17\pi}{4}$ in $[0, 2\pi)$ and evaluate $\sin\tfrac{17\pi}{4}$.
6. If $\cos\theta = \tfrac{5}{13}$ and $\theta$ is in Quadrant IV, find $\sin\theta$ and $\tan\theta$.
7. In which quadrant is $\tan\theta \lt 0$ and $\sin\theta \gt 0$?
8. An illustrative bicycle wheel has radius $35$ cm. How far does a point on the rim travel when the wheel turns through $\tfrac{2\pi}{3}$ radians?

<details>
<summary>Answer key and self-check</summary>

1. $225 \cdot \tfrac{\pi}{180} = \tfrac{5\pi}{4}$; $\tfrac{11\pi}{6} \cdot \tfrac{180}{\pi} = 330^\circ$.
2. $360^\circ - 300^\circ = 60^\circ$; $\tfrac{7\pi}{6} - \pi = \tfrac{\pi}{6}$.
3. Quadrant II, reference $\tfrac{\pi}{4}$: $\sin = \tfrac{\sqrt{2}}{2}$, $\cos = -\tfrac{\sqrt{2}}{2}$, $\tan = -1$.
4. Quadrant IV, reference $\tfrac{\pi}{6}$: $\cos = \tfrac{\sqrt{3}}{2}$, $\sin = -\tfrac{1}{2}$, $\tan = -\tfrac{\sqrt{3}}{3}$, $\sec = \tfrac{2\sqrt{3}}{3}$, $\csc = -2$, $\cot = -\sqrt{3}$.
5. $\tfrac{17\pi}{4} - 4\pi = \tfrac{\pi}{4}$, so $\sin\tfrac{17\pi}{4} = \tfrac{\sqrt{2}}{2}$.
6. $\sin^2\theta = 1 - \tfrac{25}{169} = \tfrac{144}{169}$, and sine is negative in Quadrant IV, so $\sin\theta = -\tfrac{12}{13}$ and $\tan\theta = -\tfrac{12}{5}$.
7. Quadrant II (sine positive, cosine negative).
8. $s = r\theta = 35 \cdot \tfrac{2\pi}{3} = \tfrac{70\pi}{3} \approx 73.3$ cm.

Self-check method: for any answer pair, confirm $\cos^2\theta + \sin^2\theta = 1$, and confirm the signs match the quadrant rule above.

</details>

## Where this fits

This lesson follows [16.3 - Exponential & Logarithmic Functions](/163-exponential-logarithmic-functions) in the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). The identity $\cos^2\theta + \sin^2\theta = 1$ is the starting point of [16.5 - Trig Identities & Equations](/165-trig-identities-equations), and the unit-circle coordinates $(\cos\theta, \sin\theta)$ become parametric equations for circles and ellipses in [16.6 - Conic Sections](/166-conic-sections).

## Sources

- OpenStax, *Precalculus 2e*, [5.1 Angles](https://openstax.org/books/precalculus-2e/pages/5-1-angles)
- OpenStax, *Precalculus 2e*, [5.2 Unit Circle: Sine and Cosine Functions](https://openstax.org/books/precalculus-2e/pages/5-2-unit-circle-sine-and-cosine-functions)
- OpenStax, *Precalculus 2e*, [5.3 The Other Trigonometric Functions](https://openstax.org/books/precalculus-2e/pages/5-3-the-other-trigonometric-functions)

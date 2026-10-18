---
title: "17.2 - Exploring Data (2-Variable)"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.2"
type: chapter
objectives:
  - "Describe a scatterplot by direction, form, strength, and unusual points, in context"
  - "Compute and interpret the correlation coefficient r and the coefficient of determination r squared, and state their limitations"
  - "Find the least-squares regression line from data or from summary statistics, interpret its slope and intercept, and compute residuals"
  - "Recognize influential points, extrapolation, and lurking variables, and explain why correlation does not establish causation"
open_source: true
---

# 17.2 - Exploring Data (2-Variable)

Many statistical questions involve two quantitative variables measured on the same individuals: hours of practice and test score, height and arm span, temperature and electricity use. This lesson shows how to display such **bivariate** data, measure the strength of a linear association, fit the least-squares regression line, and judge whether the line is trustworthy.

## Prerequisites

You need the mean and sample standard deviation from [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable), and slope-intercept form of a line from [14.5 - Linear Functions & Graphing](/145-linear-functions-graphing). In regression, the line is written $\hat{y} = a + bx$, with $b$ as the slope and $a$ as the $y$-intercept.

## Learning objectives

By the end of this lesson you should be able to:

1. Identify explanatory and response variables and describe a scatterplot's direction, form, strength, and unusual points.
2. Compute $r$ for a small data set and explain what its sign, size, and $r^2$ do and do not tell you.
3. Find the least-squares line, interpret the slope and intercept in context, and compute and interpret residuals.
4. Explain how an influential point, extrapolation, or a lurking variable can make a regression conclusion misleading.

## Core ideas

### Scatterplots

Put the **explanatory** variable $x$ (the one that may help predict or explain) on the horizontal axis and the **response** variable $y$ on the vertical axis. Describe:

- **Direction:** positive (larger $x$ tends to go with larger $y$) or negative.
- **Form:** linear, curved, or clustered.
- **Strength:** how closely the points follow the form.
- **Unusual points:** outliers or points far from the rest in the $x$ direction.

### Correlation

The **correlation coefficient** measures the direction and strength of a **linear** relationship:

$$r = \frac{1}{n - 1} \sum \left(\frac{x - \bar{x}}{s_x}\right)\left(\frac{y - \bar{y}}{s_y}\right).$$

Each term is a product of z-scores. Points in the lower-left and upper-right quadrants (relative to the means) contribute positive products; points in the other two quadrants contribute negative ones. Key facts: $-1 \le r \le 1$; $r = \pm 1$ only if all points lie exactly on a line; $r$ has no units and does not change if either variable is rescaled with a positive multiplier; $r$ treats $x$ and $y$ symmetrically.

### The least-squares regression line

The **residual** of a point is $y - \hat{y}$, actual minus predicted. The least-squares line is the line that makes the sum of squared residuals as small as possible. Its slope and intercept are

$$b = r \cdot \frac{s_y}{s_x}, \qquad a = \bar{y} - b\bar{x},$$

so the line always passes through $(\bar{x}, \bar{y})$. An equivalent computing form is $b = \tfrac{\sum (x - \bar{x})(y - \bar{y})}{\sum (x - \bar{x})^2}$.

- **Slope:** for each one-unit increase in $x$, the *predicted* $y$ changes by $b$ units.
- **Intercept:** the predicted $y$ when $x = 0$; meaningful only if $x = 0$ is plausible and within the data's range.
- **Coefficient of determination** $r^2$: the fraction of the variation in $y$ that is accounted for by the linear relationship with $x$.

### Checking the model

A **residual plot** graphs residuals against $x$. If the line is appropriate, the residuals scatter randomly around $0$ with no curve or fan shape. A curved pattern means a straight line is the wrong form, even when $r$ is large.

An **influential point** is one whose removal would change the slope or correlation substantially; points with extreme $x$ values are the usual suspects. **Extrapolation** uses the line far outside the range of observed $x$ values, where the linear pattern may not hold. A **lurking variable** is a variable not in the analysis that affects both $x$ and $y$ and can create an association without either causing the other.

## Worked examples

### Example 1: Correlation, regression line, and residuals

An illustrative sample of five students records hours studied $x$ and test score $y$: $(1, 60), (2, 65), (3, 70), (4, 80), (5, 85)$.

1. Means: $\bar{x} = 3$, $\bar{y} = \tfrac{360}{5} = 72$.
2. Deviations: $x - \bar{x} = -2, -1, 0, 1, 2$; $y - \bar{y} = -12, -7, -2, 8, 13$.
3. Sums: $\sum (x - \bar{x})^2 = 10$; $\sum (y - \bar{y})^2 = 144 + 49 + 4 + 64 + 169 = 430$; $\sum (x - \bar{x})(y - \bar{y}) = 24 + 7 + 0 + 8 + 26 = 65$.
4. Slope: $b = \tfrac{65}{10} = 6.5$. Intercept: $a = 72 - 6.5(3) = 52.5$. The line is $\hat{y} = 52.5 + 6.5x$.
5. Correlation: $r = \tfrac{65}{\sqrt{10 \cdot 430}} \approx 0.991$, and $r^2 \approx 0.983$.
6. Check with the other formula: $s_x = \sqrt{10/4} \approx 1.581$, $s_y = \sqrt{430/4} \approx 10.368$, so $b = 0.991 \cdot \tfrac{10.368}{1.581} \approx 6.5$.
7. Residuals: at $x = 4$, $\hat{y} = 52.5 + 26 = 78.5$ and the residual is $80 - 78.5 = 1.5$. All five residuals are $1, -0.5, -2, 1.5, 0$, which sum to $0$, as least-squares residuals always do.

Interpretation: in this sample, each additional hour of study is associated with a predicted score $6.5$ points higher, and about $98\%$ of the variation in scores is accounted for by the linear relationship with hours. The intercept, $52.5$, is the predicted score for zero hours; $x = 0$ is just outside the data, so treat it cautiously.

### Example 2: One influential point

Add a sixth illustrative student who studied $10$ hours and scored $62$. Recomputing with all six points gives $\hat{y} \approx 69.79 + 0.13x$ and $r \approx 0.04$. One point with an extreme $x$ value flattened the slope from $6.5$ to about $0.13$ and erased the correlation. Report the analysis with and without such a point, and investigate it rather than silently deleting it.

### Example 3: Correlation from z-scores

For the points $(1, 2), (2, 3), (3, 5), (4, 6)$: $\bar{x} = 2.5$, $s_x \approx 1.291$, $\bar{y} = 4$, $s_y \approx 1.826$.

| $x$ | $y$ | $z_x$ | $z_y$ | $z_x z_y$ |
|---|---|---|---|---|
| 1 | 2 | $-1.162$ | $-1.095$ | $1.273$ |
| 2 | 3 | $-0.387$ | $-0.548$ | $0.212$ |
| 3 | 5 | $0.387$ | $0.548$ | $0.212$ |
| 4 | 6 | $1.162$ | $1.095$ | $1.273$ |

The products sum to about $2.970$, so $r \approx \tfrac{2.970}{3} \approx 0.990$. Every product is positive because each point is on the same side of both means.

## Common misconceptions and boundary cases

- **Correlation implies causation.** In an illustrative city, ice-cream sales and swimming accidents might rise together across months. Hot weather, a lurking variable, increases both. Only a randomized experiment (see [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design)) can directly support a cause-and-effect claim.
- **$r = 0$ means no relationship.** $r$ measures *linear* association only. Points on the parabola $y = x^2$ for $x = -2, -1, 0, 1, 2$ have $r = 0$ yet a perfect curved relationship.
- **A high $r$ proves a line is the right model.** Always look at the residual plot; a curved residual pattern means the form is wrong.
- **The slope is the correlation.** Slope has units of $y$ per unit of $x$ and can be any number; $r$ has no units and lies between $-1$ and $1$. They share a sign but are equal only when $s_x = s_y$.
- **Swapping $x$ and $y$ gives the same line.** $r$ stays the same, but the regression of $x$ on $y$ is a different line, because it minimizes horizontal rather than vertical squared distances.
- **Predicting far outside the data.** Extrapolating Example 1 to $20$ hours predicts a score of $182.5$, which is impossible on a $100$-point test.

## Practice

1. For each pair, name the explanatory and response variable: (a) daily temperature and cups of hot chocolate sold; (b) hours of sleep and reaction time.
2. Summary statistics (illustrative): $\bar{x} = 10$, $s_x = 2$, $\bar{y} = 50$, $s_y = 5$, $r = 0.8$. Find the least-squares line and the predicted $y$ when $x = 12$.
3. Using the line from problem 2, an individual with $x = 12$ has $y = 57$. Find and interpret the residual.
4. For the illustrative points $(2, 3), (4, 7), (6, 8), (8, 12)$, find the least-squares line and $r^2$.
5. Interpret $r^2 = 0.64$ from problem 2 in a sentence.
6. A residual plot shows a clear U-shaped pattern. What does that tell you about the linear model?
7. An illustrative study finds that students who own more books have higher reading scores. Name a possible lurking variable and explain why it weakens a causal claim.

<details>
<summary>Answer key and self-check</summary>

1. (a) Explanatory: temperature; response: cups sold. (b) Explanatory: hours of sleep; response: reaction time.
2. $b = 0.8 \cdot \tfrac{5}{2} = 2$; $a = 50 - 2(10) = 30$; $\hat{y} = 30 + 2x$. At $x = 12$, $\hat{y} = 54$.
3. Residual $= 57 - 54 = 3$. This individual's actual $y$ is $3$ units above what the line predicts.
4. $\bar{x} = 5$, $\bar{y} = 7.5$; $\sum (x - \bar{x})^2 = 20$; $\sum (x - \bar{x})(y - \bar{y}) = 28$. $b = 1.4$, $a = 7.5 - 1.4(5) = 0.5$, so $\hat{y} = 0.5 + 1.4x$. $\sum (y - \bar{y})^2 = 41$, so $r = \tfrac{28}{\sqrt{20 \cdot 41}} \approx 0.978$ and $r^2 \approx 0.956$.
5. About $64\%$ of the variation in $y$ is accounted for by the linear relationship with $x$.
6. The relationship is curved; a straight line is not an appropriate model, regardless of $r$.
7. Family income or parents' education could affect both the number of books at home and reading scores. Because the data are observational, the association may be due to the lurking variable rather than the books.

Self-check method: residuals from a least-squares line sum to $0$ (problem 4: $-0.3, 0.9, -0.9, 0.3$); the line passes through $(\bar{x}, \bar{y})$; and $r$ and $b$ must have the same sign.

</details>

## Where this fits

This lesson follows [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable) in the [Statistics & Probability course](/subject/statistics-and-probability). Next, [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design) explains how data collection determines whether an association can be read as cause and effect. The least-squares idea also underlies the model-fitting methods in [Statistical Learning Optimization](/231-statistical-learning-optimization).

## Sources

- OpenStax, *Introductory Statistics 2e*, [12.1 Linear Equations](https://openstax.org/books/introductory-statistics-2e/pages/12-1-linear-equations)
- OpenStax, *Introductory Statistics 2e*, [12.2 Scatter Plots](https://openstax.org/books/introductory-statistics-2e/pages/12-2-scatter-plots)
- OpenStax, *Introductory Statistics 2e*, [12.3 The Regression Equation](https://openstax.org/books/introductory-statistics-2e/pages/12-3-the-regression-equation)
- OpenStax, *Introductory Statistics 2e*, [12.6 Outliers](https://openstax.org/books/introductory-statistics-2e/pages/12-6-outliers)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [4.4.4 How can I tell if a model fits my data?](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm) (residual plots)

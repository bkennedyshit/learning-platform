---
title: "17.1 - Exploring Data (1-Variable)"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.1"
type: chapter
objectives:
  - "Classify variables as categorical or quantitative and describe a distribution by shape, center, spread, and unusual values"
  - "Compute the mean, median, quartiles, IQR, variance, and sample standard deviation, and choose resistant or non-resistant summaries to fit the shape"
  - "Build and read stem-and-leaf plots and box plots, and identify potential outliers with the 1.5 IQR rule"
  - "Predict how adding a constant or multiplying by a constant changes measures of center and spread"
open_source: true
---

# 17.1 - Exploring Data (1-Variable)

Exploratory data analysis starts with one variable at a time. Before any formula, ask what the variable is, what values occur, and how often. The answer is the **distribution** of the variable. This lesson extends the pre-algebra treatment of center and spread with the standard deviation, the language used to describe shape, and the rules for how summaries change when data are rescaled.

## Prerequisites

You should be able to compute a mean, median, quartiles, and IQR for a small data set and read a dot plot, histogram, and box plot, as in [13.7 - Statistics & Data](/137-statistics-data). Square roots and order of operations are used throughout; a calculator is fine for arithmetic.

## Learning objectives

By the end of this lesson you should be able to:

1. Classify a variable and describe a distribution by its shape, center, spread, and any unusual values, in context.
2. Compute the variance and sample standard deviation by hand for a small data set and interpret the result in the data's units.
3. Build a stem-and-leaf plot and a box plot, and flag potential outliers with the $1.5 \cdot \text{IQR}$ rule.
4. State the effect of $y = a + bx$ on the mean, median, standard deviation, and IQR.

## Core ideas

### Variables and shape

A **categorical** variable sorts individuals into groups (blood type, state of residence); it is summarized with counts or proportions and displayed with bar charts. A **quantitative** variable is a numerical measurement or count for which arithmetic makes sense; it is displayed with dot plots, stem-and-leaf plots, histograms, or box plots.

When you describe a quantitative distribution, cover four things, always in the context of the variable:

- **Shape:** roughly **symmetric**, **skewed right** (a long tail toward high values), **skewed left** (a long tail toward low values), **uniform** (bars about equal), or **bimodal** (two clear peaks, often a sign that two groups are mixed).
- **Center:** the mean or the median.
- **Spread:** the range, IQR, or standard deviation.
- **Unusual features:** potential outliers, gaps, or clusters.

### Standard deviation

The **deviation** of a value is $x - \bar{x}$. Deviations always sum to $0$, so to measure typical distance from the mean we square them first. The **sample variance** and **sample standard deviation** are

$$s^2 = \frac{\sum (x - \bar{x})^2}{n - 1}, \qquad s = \sqrt{s^2}.$$

The divisor $n - 1$ (the **degrees of freedom**) is used when the data are a sample and $s$ estimates the population standard deviation $\sigma$. If the data are the entire population, divide by $n$ instead. The standard deviation is in the same units as the data and is roughly the typical distance of a value from the mean. It is $0$ only when every value is identical.

### Resistant and non-resistant summaries

A summary is **resistant** if a few extreme values barely change it. The median and IQR are resistant; the mean, standard deviation, and range are not. Use the median and IQR for strongly skewed data or data with outliers, and the mean and standard deviation for roughly symmetric data without outliers.

### Five-number summary, box plots, and outliers

The five-number summary is minimum, $Q_1$, median, $Q_3$, maximum. In this lesson, $Q_1$ and $Q_3$ are the medians of the lower and upper halves of the ordered data, leaving out the overall median when $n$ is odd; calculators and software use several slightly different quartile rules, so their answers can differ a little. A value is a **potential outlier** if it is below $Q_1 - 1.5 \cdot \text{IQR}$ or above $Q_3 + 1.5 \cdot \text{IQR}$. In a modified box plot, whiskers extend to the most extreme values inside these fences and outliers are drawn as separate points.

### Stem-and-leaf plots

A stem-and-leaf plot splits each value into a **stem** (all but the last digit) and a **leaf** (the last digit). It shows the shape like a sideways histogram while keeping every data value. Always include a key such as "$7 \mid 3$ means $73$".

### Linear transformations

If every value is converted by $y = a + bx$ (for example, a unit change):

- Measures of center and location (mean, median, quartiles) become $a + b \cdot (\text{old value})$.
- Measures of spread (range, IQR, standard deviation) are multiplied by $\lvert b \rvert$ and are **not** affected by adding $a$.
- Shape does not change when $b > 0$; a negative $b$ also mirrors the distribution, so right skew becomes left skew.

## Worked examples

### Example 1: Standard deviation by hand

Find the sample standard deviation of the illustrative sample $4, 8, 6, 5, 7$.

1. Mean: $\bar{x} = \tfrac{4 + 8 + 6 + 5 + 7}{5} = \tfrac{30}{5} = 6$.
2. Deviations: $-2, 2, 0, -1, 1$. Check: they sum to $0$.
3. Squared deviations: $4, 4, 0, 1, 1$, which sum to $10$.
4. Variance: $s^2 = \tfrac{10}{5 - 1} = 2.5$.
5. Standard deviation: $s = \sqrt{2.5} \approx 1.58$.

The values typically sit about $1.6$ units from the mean of $6$. (If these five values were the whole population, $\sigma = \sqrt{10/5} \approx 1.41$.)

### Example 2: Stem-and-leaf plot, five-number summary, and an outlier

Fifteen illustrative test scores are $38, 61, 64, 67, 70, 72, 73, 75, 78, 80, 81, 84, 88, 90, 97$.

```text
3 | 8
4 |
5 |
6 | 1 4 7
7 | 0 2 3 5 8
8 | 0 1 4 8
9 | 0 7
Key: 7 | 3 means 73
```

1. Median: the 8th of $15$ ordered values, $75$.
2. Lower half (7 values): $38, 61, 64, 67, 70, 72, 73$, so $Q_1 = 67$. Upper half: $78, 80, 81, 84, 88, 90, 97$, so $Q_3 = 84$.
3. $\text{IQR} = 84 - 67 = 17$ and $1.5 \cdot 17 = 25.5$. Fences: $67 - 25.5 = 41.5$ and $84 + 25.5 = 109.5$.
4. $38 < 41.5$, so $38$ is a potential outlier. The five-number summary is $38, 67, 75, 84, 97$; in a modified box plot the lower whisker stops at $61$ and $38$ is plotted as a point.
5. Resistance check: the mean is $\tfrac{1118}{15} \approx 74.5$ and $s \approx 14.2$. Dropping $38$ gives a mean of $\tfrac{1080}{14} \approx 77.1$ and $s \approx 10.3$, while the median only moves from $75$ to $76.5$.

Description in context: the scores are skewed left by one unusually low score ($38$); the median score is $75$ and the middle half of the scores spans $17$ points, from $67$ to $84$.

### Example 3: Changing units

Five illustrative daily high temperatures are $16, 18, 20, 22, 24$ degrees Celsius, with mean $20$, median $20$, IQR $6$, and $s \approx 3.16$. Convert to Fahrenheit with $F = 32 + 1.8C$.

- Mean and median: $32 + 1.8(20) = 68$ degrees Fahrenheit.
- IQR: $1.8 \cdot 6 = 10.8$ degrees Fahrenheit; the $32$ does not affect spread.
- Standard deviation: $1.8 \cdot 3.16 \approx 5.69$ degrees Fahrenheit.

Recomputing directly from the converted values $60.8, 64.4, 68, 71.6, 75.2$ gives the same results.

## Common misconceptions and boundary cases

- **Dividing by $n$ for a sample.** Sample standard deviation uses $n - 1$. Dividing by $n$ gives a slightly smaller value that is the population formula.
- **Thinking standard deviation is resistant.** Because deviations are squared, one far-out value can inflate $s$ greatly, as Example 2 shows.
- **Calling every outlier an error.** The $1.5 \cdot \text{IQR}$ rule flags values worth investigating. An outlier may be a recording mistake or a genuine, important observation; do not delete it without a reason.
- **Adding a constant changes spread.** Shifting every value by the same amount moves the center but leaves range, IQR, and standard deviation unchanged.
- **Describing a distribution with numbers only.** "Mean 74.5" without shape, spread, and context is incomplete. A bimodal distribution, for instance, can have a mean where almost no data lie.
- **Comparing standard deviations across different units.** A spread of $10$ centimeters and a spread of $10$ kilograms are not comparable quantities.

## Practice

1. Classify each variable as categorical or quantitative: zip code, number of pets, time to run a mile, favorite music genre.
2. For the illustrative sample $2, 4, 4, 4, 5, 5, 7, 9$, find the mean, the variance $s^2$, and the sample standard deviation $s$.
3. For the same data, find the five-number summary and the IQR, and decide whether $9$ is a potential outlier.
4. Ten illustrative commute times (minutes) are $12, 15, 18, 20, 22, 25, 25, 28, 30, 55$. Find the median, IQR, and fences, and identify any potential outlier. Which pair of summaries, mean/SD or median/IQR, would you report?
5. A class's quiz scores have mean $72$, median $74$, standard deviation $8$, and IQR $10$. The teacher adds $5$ points to every score. Give the new four values.
6. The same original scores are instead converted to percentages by multiplying by $1.25$. Give the new four values.
7. A histogram of household incomes in a town has a long tail to the right. Which is likely larger, the mean or the median? Why?

<details>
<summary>Answer key and self-check</summary>

1. Categorical (zip codes are labels); quantitative; quantitative; categorical.
2. Mean $\tfrac{40}{8} = 5$. Squared deviations $9, 1, 1, 1, 0, 0, 4, 16$ sum to $32$. $s^2 = \tfrac{32}{7} \approx 4.57$ and $s \approx 2.14$. (The population SD of these values is exactly $2$.)
3. Median $\tfrac{4 + 5}{2} = 4.5$; lower half $2, 4, 4, 4$ gives $Q_1 = 4$; upper half $5, 5, 7, 9$ gives $Q_3 = 6$. Five-number summary $2, 4, 4.5, 6, 9$; $\text{IQR} = 2$. Upper fence $6 + 3 = 9$. $9$ is not above $9$, so it is not flagged.
4. Median $\tfrac{22 + 25}{2} = 23.5$; $Q_1 = 18$, $Q_3 = 28$, $\text{IQR} = 10$; fences $3$ and $43$. $55$ is a potential outlier. Report the median and IQR, because $55$ inflates the mean ($25$) and SD ($\approx 11.95$).
5. Mean $77$, median $79$, SD $8$, IQR $10$.
6. Mean $90$, median $92.5$, SD $10$, IQR $12.5$.
7. The mean, because the long right tail of high incomes pulls the mean upward while the median stays with the middle value.

Self-check method: deviations from the mean must sum to $0$; $s$ can never be negative; quartiles must satisfy $\min \le Q_1 \le \text{median} \le Q_3 \le \max$; and after a transformation, recompute one summary directly from two or three converted values to confirm.

</details>

## Where this fits

This is the first lesson in the [Statistics & Probability course](/subject/statistics-and-probability). It builds on [13.7 - Statistics & Data](/137-statistics-data) from Pre-Algebra. Next, [17.2 - Exploring Data (2-Variable)](/172-exploring-data-2-variable) uses means and standard deviations of two variables to measure association. The standard deviation returns in [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions), where it sets the scale of z-scores.

## Sources

- OpenStax, *Introductory Statistics 2e*, [2.1 Stem-and-Leaf Graphs (Stemplots), Line Graphs, and Bar Graphs](https://openstax.org/books/introductory-statistics-2e/pages/2-1-stem-and-leaf-graphs-stemplots-line-graphs-and-bar-graphs)
- OpenStax, *Introductory Statistics 2e*, [2.3 Measures of the Location of the Data](https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data)
- OpenStax, *Introductory Statistics 2e*, [2.4 Box Plots](https://openstax.org/books/introductory-statistics-2e/pages/2-4-box-plots)
- OpenStax, *Introductory Statistics 2e*, [2.6 Skewness and the Mean, Median, and Mode](https://openstax.org/books/introductory-statistics-2e/pages/2-6-skewness-and-the-mean-median-and-mode)
- OpenStax, *Introductory Statistics 2e*, [2.7 Measures of the Spread of the Data](https://openstax.org/books/introductory-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [1.3.5.6 Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm) and [1.3.3.7 Box Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm)

---
title: "13.7 - Statistics & Data"
subject: "Pre-Algebra"
catalog: k12
audience_tier: 9-12
chapter: "13.7"
type: chapter
objectives:
  - "Recognize statistical questions and classify variables as categorical or quantitative (discrete or continuous)"
  - "Compute the mean, median, and mode of a data set and choose the measure of center that fits its shape"
  - "Compute the range, quartiles, interquartile range, and mean absolute deviation, and flag potential outliers with the 1.5 IQR rule"
  - "Build and read dot plots, histograms, and box plots, and compare two distributions by center and spread"
open_source: true
---

# 13.7 - Statistics & Data

Statistics is the study of variability: answering questions whose answers are expected to differ from one person, object, or day to the next. "How old am I?" has one answer. "How old are the students in my school?" has many, and the useful response is a summary of their **distribution**, meaning what values occur and how often. This lesson covers the vocabulary of data, the three common displays, measures of center and spread, and how to compare two groups.

## Prerequisites

You need decimal and fraction arithmetic from [13.3 - Fractions, Decimals & Percent](/133-fractions-decimals-percent) and absolute value as distance from [13.2 - The Number System](/132-the-number-system). Reading a number line and ordering numbers are used throughout.

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether a question is statistical and classify each variable in a data set.
2. Compute the mean, median, and mode, and explain which better represents a skewed data set.
3. Compute the range, $Q_1$, $Q_3$, interquartile range (IQR), and mean absolute deviation (MAD), and identify potential outliers.
4. Draw or interpret a dot plot, histogram, and box plot, and compare two distributions using center and spread.

## Core ideas

### Statistical questions and variables

A **statistical question** anticipates variability in the answers. The characteristic being recorded is a **variable**.

- A **categorical** (qualitative) variable places each individual in a group: favorite sport, eye color, jersey number. Numbers that are labels are categorical, because averaging them is meaningless.
- A **quantitative** variable is a numerical measurement or count. It is **discrete** if it comes from counting (number of siblings) and **continuous** if it comes from measuring (height in centimeters).

### Displays

- A **dot plot** places one dot above a number line for each value. It shows every data point and works well for small data sets.
- A **histogram** groups quantitative data into equal-width intervals (bins) and draws a bar for each bin's frequency. The bars touch because the number line is continuous. Bin edges need a rule, such as "left endpoint included", so each value is counted once.
- A **box plot** draws the **five-number summary**: minimum, $Q_1$, median, $Q_3$, maximum. The box spans the middle half of the data, and the whiskers reach to the extremes (or to the most extreme non-outliers, with outliers plotted separately).
- A **bar chart** displays categorical data; its bars are separated because the categories are not on a number line.

### Measures of center

- **Mean:** the sum of the values divided by the number of values, $\bar{x} = \tfrac{\sum x}{n}$. It is the balance point of the data.
- **Median:** the middle value of the **ordered** data. With an even number of values, it is the mean of the two middle values.
- **Mode:** the most frequent value. A data set can have one mode, several, or none.

The mean is pulled toward extreme values; the median is not. For a **symmetric** distribution the two are close. For a distribution **skewed right** (a long tail of high values), the mean is usually greater than the median, and the median is the better summary of a typical value.

### Measures of spread

- **Range:** maximum minus minimum. It depends only on the two extremes.
- **Quartiles:** $Q_1$ is the median of the lower half of the ordered data and $Q_3$ is the median of the upper half. (In this lesson, when $n$ is odd, the overall median is left out of both halves. Calculators and software use several slightly different conventions, so their quartiles may differ a little.)
- **Interquartile range:** $\text{IQR} = Q_3 - Q_1$, the spread of the middle half.
- **Potential outliers:** values below $Q_1 - 1.5 \cdot \text{IQR}$ or above $Q_3 + 1.5 \cdot \text{IQR}$. They deserve a closer look; they are not automatically errors.
- **Mean absolute deviation:** the average distance of the values from the mean,
$$\text{MAD} = \frac{\sum \lvert x - \bar{x} \rvert}{n}.$$
A larger MAD means the values are more spread out around the mean.

Use the median with the IQR, and the mean with the MAD, so that center and spread are measured in compatible ways.

## Worked examples

### Example 1: Center of a skewed data set

An illustrative survey records the minutes nine students spent on homework one evening: $20, 25, 25, 30, 35, 40, 45, 50, 90$.

1. Mean: the sum is $360$, so $\bar{x} = \tfrac{360}{9} = 40$ minutes.
2. Median: the 5th of the $9$ ordered values, $35$ minutes.
3. Mode: $25$ minutes.
4. The mean exceeds the median because the single value $90$ pulls it upward. Without $90$, the mean would be $\tfrac{270}{8} = 33.75$ and the median $\tfrac{30 + 35}{2} = 32.5$; the mean changed much more.

### Example 2: Five-number summary, IQR, and outliers

Use the same data.

1. Lower half (excluding the median): $20, 25, 25, 30$, so $Q_1 = \tfrac{25 + 25}{2} = 25$.
2. Upper half: $40, 45, 50, 90$, so $Q_3 = \tfrac{45 + 50}{2} = 47.5$.
3. $\text{IQR} = 47.5 - 25 = 22.5$, and $1.5 \cdot 22.5 = 33.75$.
4. Fences: $25 - 33.75 = -8.75$ and $47.5 + 33.75 = 81.25$. The value $90$ is above $81.25$, so it is a potential outlier.
5. Five-number summary: $20, 25, 35, 47.5, 90$. On a box plot, the upper whisker would stop at $50$ and $90$ would be marked as a separate point.

### Example 3: Histogram

Group the homework data into bins of width $10$, left endpoint included: $[20, 30)$ has $3$ values ($20, 25, 25$); $[30, 40)$ has $2$; $[40, 50)$ has $2$; $[50, 60)$ has $1$; the bins from $60$ to $90$ are empty; and $[90, 100)$ has $1$. The tall bars on the left and the isolated bar on the right show the right skew.

### Example 4: MAD and comparing two groups

Two illustrative groups of five scores:

- Group A: $3, 5, 6, 8, 8$. The sum is $30$, so $\bar{x} = 6$. Distances from $6$: $3, 1, 0, 2, 2$, totaling $8$. $\text{MAD} = \tfrac{8}{5} = 1.6$.
- Group B: $1, 4, 6, 9, 10$. The sum is $30$, so $\bar{x} = 6$. Distances: $5, 2, 0, 3, 4$, totaling $14$. $\text{MAD} = \tfrac{14}{5} = 2.8$.

The groups have the same mean, but Group B's scores are more spread out. A comparison should report both center and spread, for example "both groups average $6$, but B is less consistent".

## Common misconceptions and boundary cases

- **Forgetting to sort.** The median of $9, 2, 7$ is $7$, the middle of $2, 7, 9$, not the middle value as listed.
- **Even-sized data sets.** With an even count there is no single middle value; average the two middle values.
- **Treating number labels as quantities.** The "mean jersey number" of a team is not meaningful; jersey numbers are categorical.
- **Mean as automatically "the" typical value.** In skewed data or data with outliers, the median usually describes a typical value better.
- **Reading box plots by width.** Each of the four sections of a box plot holds about a quarter of the data. A longer whisker or wider box section means the values are more spread out there, not that there are more of them.
- **Histograms versus bar charts.** Histograms are for quantitative data with touching bars on a number line; bar charts are for categories. Changing histogram bin widths can change how the shape looks, so state the bins you used.

## Practice

Problems 2–5 use this illustrative data set: $4, 8, 6, 5, 3, 8, 9, 7, 8, 2$.

1. Classify each variable: favorite sport; height in centimeters; number of siblings; jersey number.
2. Find the mean, median, and mode.
3. Find the range, $Q_1$, $Q_3$, and IQR.
4. Find the MAD.
5. Give the five-number summary and decide whether any value is a potential outlier.
6. For the data $10, 12, 13, 15, 100$, compute the mean and median. Which better describes a typical value?
7. Two classes both have a mean quiz score of $50$. Class X has MAD $2$ and Class Y has MAD $12$. Which class has more consistent scores?
8. Which is a statistical question: "How tall am I?" or "How tall are the students in my class?" Explain.

<details>
<summary>Answer key and self-check</summary>

1. Categorical; quantitative continuous; quantitative discrete; categorical.
2. Ordered: $2, 3, 4, 5, 6, 7, 8, 8, 8, 9$. The sum is $60$, so the mean is $6$. Median: $\tfrac{6 + 7}{2} = 6.5$. Mode: $8$.
3. Range: $9 - 2 = 7$. Lower half $2, 3, 4, 5, 6$ gives $Q_1 = 4$; upper half $7, 8, 8, 8, 9$ gives $Q_3 = 8$; $\text{IQR} = 4$.
4. Distances from $6$: $4, 3, 2, 1, 0, 1, 2, 2, 2, 3$, totaling $20$. $\text{MAD} = \tfrac{20}{10} = 2$.
5. $2, 4, 6.5, 8, 9$. Fences: $4 - 6 = -2$ and $8 + 6 = 14$. No value is outside them, so there are no potential outliers.
6. Mean $\tfrac{150}{5} = 30$; median $13$. The median, because the value $100$ pulls the mean up to $30$, which is larger than four of the five values.
7. Class X: a smaller MAD means scores cluster more tightly around the mean.
8. The second. It expects different answers from different students; the first has a single answer.

Self-check method: the mean must lie between the minimum and maximum, and the sum of the signed deviations $x - \bar{x}$ must be $0$ (in problem 4: $-4 - 3 - 2 - 1 + 0 + 1 + 2 + 2 + 2 + 3 = 0$). Quartiles must satisfy $\min \le Q_1 \le \text{median} \le Q_3 \le \max$.

</details>

## Where this fits

This lesson follows [13.6 - Geometry Foundations](/136-geometry-foundations) in the [Pre-Algebra course](/subject/pre-algebra). Next, [13.8 - Probability Intro](/138-probability-intro) uses relative frequencies from data as estimates of probability. These ideas are developed further in [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable) in the [Statistics & Probability course](/subject/statistics-and-probability), which adds the standard deviation and the effect of changing units.

## Sources

- OpenStax, *Introductory Statistics 2e*, [1.2 Data, Sampling, and Variation in Data and Sampling](https://openstax.org/books/introductory-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling)
- OpenStax, *Introductory Statistics 2e*, [2.2 Histograms, Frequency Polygons, and Time Series Graphs](https://openstax.org/books/introductory-statistics-2e/pages/2-2-histograms-frequency-polygons-and-time-series-graphs)
- OpenStax, *Introductory Statistics 2e*, [2.3 Measures of the Location of the Data](https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data) (quartiles, IQR, and the $1.5 \cdot \text{IQR}$ potential-outlier rule)
- OpenStax, *Introductory Statistics 2e*, [2.4 Box Plots](https://openstax.org/books/introductory-statistics-2e/pages/2-4-box-plots)
- OpenStax, *Introductory Statistics 2e*, [2.5 Measures of the Center of the Data](https://openstax.org/books/introductory-statistics-2e/pages/2-5-measures-of-the-center-of-the-data)
- OpenStax, *Introductory Statistics 2e*, [2.7 Measures of the Spread of the Data](https://openstax.org/books/introductory-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
- Illustrative Mathematics, Grade 6, Unit 8, [Lesson 11: Variability and MAD](https://im.kendallhunt.com/MS/students/1/8/11/index.html)

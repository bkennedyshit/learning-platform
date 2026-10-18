---
title: "17.7 - Confidence Intervals"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.7"
type: chapter
objectives:
  - "Explain an interval as statistic plus or minus margin of error and interpret both the interval and the confidence level correctly"
  - "Check conditions for and construct a one-sample z interval for a proportion and a one-sample t interval for a mean"
  - "Construct and interpret a two-sample t interval for a difference of means"
  - "Describe how confidence level and sample size affect the margin of error, and find the sample size needed for a target margin of error"
open_source: true
---

# 17.7 - Confidence Intervals

A single sample statistic, such as $\hat{p} = 0.58$, is almost never exactly equal to the parameter it estimates. A **confidence interval** reports a range of plausible values for the parameter together with a measure of how reliable the method is. This lesson builds intervals for a proportion, a mean, and a difference of means, and focuses on what the results do and do not mean.

## Prerequisites

You need sampling distributions, the standard deviation of $\hat{p}$ and $\bar{x}$, and the large counts and 10% conditions from [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions), and the idea of a random sample from [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design). A calculator or software that gives normal and $t$ critical values is needed.

## Learning objectives

By the end of this lesson you should be able to:

1. Write any interval as $\text{statistic} \pm (\text{critical value})(\text{standard error})$ and interpret it in context.
2. Construct a z interval for $p$ and a t interval for $\mu$ after checking the conditions.
3. Construct a t interval for $\mu_1 - \mu_2$ from two independent samples and judge whether $0$ is plausible.
4. Predict how the margin of error changes with confidence level and sample size, and solve for $n$.

## Core ideas

### The structure of an interval

Every interval in this lesson has the form

$$\text{point estimate} \pm \underbrace{(\text{critical value}) \times (\text{standard error})}_{\text{margin of error}}.$$

The **standard error** (SE) estimates the standard deviation of the statistic's sampling distribution using sample values. The **critical value** depends on the confidence level: for z intervals, $z^* = 1.645$ for $90\%$, $1.960$ for $95\%$, and $2.576$ for $99\%$.

### Interpreting confidence

- **The interval:** "We are $95\%$ confident that the interval from ... to ... captures the true [parameter in context]."
- **The confidence level:** if we took many random samples and built a $95\%$ interval from each, about $95\%$ of those intervals would capture the true parameter. The confidence is in the *method*, not in any single interval: once computed, a particular interval either contains the parameter or it does not.

### Conditions

1. **Random:** the data come from a random sample or a randomized experiment.
2. **Independence (10% condition):** when sampling without replacement, $n$ is at most $10\%$ of the population.
3. **Approximately normal sampling distribution:**
   - For proportions: at least $10$ successes and $10$ failures in the sample, $n\hat{p} \ge 10$ and $n(1 - \hat{p}) \ge 10$.
   - For means: the population is approximately normal, or $n \ge 30$; for small samples, a graph of the data should show no strong skew or outliers.

### Intervals for a proportion and a mean

One-sample z interval for $p$:

$$\hat{p} \pm z^* \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}.$$

One-sample t interval for $\mu$, used because $\sigma$ is almost never known:

$$\bar{x} \pm t^* \frac{s}{\sqrt{n}}, \qquad \text{df} = n - 1.$$

The **t distributions** are symmetric and bell-shaped like the standard normal but have heavier tails, which account for the extra uncertainty from estimating $\sigma$ with $s$. As the degrees of freedom increase, $t^*$ approaches $z^*$; for $95\%$ confidence, $t^* \approx 2.262$ with $9$ df, $2.131$ with $15$ df, and $2.064$ with $24$ df.

### Interval for a difference of two means

For independent random samples or two groups in a randomized experiment:

$$(\bar{x}_1 - \bar{x}_2) \pm t^* \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}.$$

Software computes the degrees of freedom with a formula (the Welch-Satterthwaite approximation) that usually gives a non-integer. By hand, a conservative choice is to use the smaller of $n_1 - 1$ and $n_2 - 1$ as the degrees of freedom, which gives a slightly wider interval.

### Margin of error and sample size

The margin of error gets **larger** with a higher confidence level and **smaller** with a larger sample size, in proportion to $\tfrac{1}{\sqrt{n}}$. To plan a study for a proportion with margin of error at most $M$, solve

$$z^* \sqrt{\frac{p^*(1 - p^*)}{n}} \le M \quad \Longrightarrow \quad n \ge \left(\frac{z^*}{M}\right)^2 p^*(1 - p^*),$$

using a prior estimate $p^*$, or $p^* = 0.5$ for the most conservative (largest) $n$. Always round **up**.

The margin of error covers only random sampling variability. It does not account for bias from undercoverage, nonresponse, or poor question wording.

## Worked examples

### Example 1: Interval for a proportion

In an illustrative random sample of $400$ students from a large university, $232$ say they support a later start time for morning classes. Construct a $95\%$ confidence interval for the proportion of all students at the university who support it.

1. Conditions: random sample; $400$ is less than $10\%$ of a large university; successes $232 \ge 10$ and failures $168 \ge 10$.
2. $\hat{p} = \tfrac{232}{400} = 0.58$. $\text{SE} = \sqrt{\tfrac{0.58(0.42)}{400}} \approx 0.0247$.
3. Margin of error: $1.96(0.0247) \approx 0.0484$.
4. Interval: $0.58 \pm 0.048$, or about $(0.532, 0.628)$.
5. Interpretation: we are $95\%$ confident that between about $53.2\%$ and $62.8\%$ of all students at this university support the later start. Because the whole interval is above $0.5$, a majority in favor is plausible.
6. At $99\%$ confidence, the margin of error is $2.576(0.0247) \approx 0.064$, giving about $(0.516, 0.644)$: higher confidence, wider interval.

### Example 2: Interval for a mean

An illustrative random sample of $16$ batteries of one model has mean lifetime $\bar{x} = 12.4$ hours and standard deviation $s = 2.0$ hours. A dot plot of the $16$ values shows no strong skew or outliers.

1. Conditions: random sample; $16$ batteries are far less than $10\%$ of production; $n < 30$, but the data show no strong skew or outliers.
2. $\text{df} = 15$ and $t^* \approx 2.131$. $\text{SE} = \tfrac{2.0}{\sqrt{16}} = 0.5$.
3. Margin of error: $2.131(0.5) \approx 1.066$. Interval: $12.4 \pm 1.07$, or about $(11.33, 13.47)$ hours.
4. Interpretation: we are $95\%$ confident that the mean lifetime of all batteries of this model is between about $11.3$ and $13.5$ hours.

### Example 3: Difference of two means

In an illustrative randomized experiment, $20$ students using method 1 have mean score $78$ ($s_1 = 8$) and $25$ students using method 2 have mean score $72$ ($s_2 = 10$). Construct a $95\%$ interval for $\mu_1 - \mu_2$.

1. Point estimate: $78 - 72 = 6$. $\text{SE} = \sqrt{\tfrac{8^2}{20} + \tfrac{10^2}{25}} = \sqrt{3.2 + 4} = \sqrt{7.2} \approx 2.683$.
2. Conservative $\text{df} = 19$, $t^* \approx 2.093$. Margin of error $\approx 5.62$, giving $(0.38, 11.62)$.
3. Software (Welch df $\approx 43.0$, $t^* \approx 2.017$) gives a slightly narrower $(0.59, 11.41)$.
4. Interpretation: we are $95\%$ confident that method 1 produces a mean score between about $0.4$ and $11.6$ points higher than method 2 for students like these. Both intervals lie entirely above $0$, so "no difference" is not a plausible value at this confidence level.

### Example 4: Choosing a sample size

How many people should a poll sample for a $95\%$ margin of error of at most $3$ percentage points, with no prior estimate?

$$n \ge \left(\frac{1.96}{0.03}\right)^2 (0.5)(0.5) \approx 1067.1,$$

so sample at least $1068$ people.

## Common misconceptions and boundary cases

- **"There is a 95% probability the parameter is in this interval."** In this course's framework, the parameter is fixed; the $95\%$ describes how often the method captures it over many samples.
- **"95% of the data fall in the interval."** A confidence interval estimates a parameter such as a population mean; it is not a range for individual values.
- **"A larger population requires a larger sample."** As long as the 10% condition holds, the margin of error depends on $n$, not on population size.
- **"Margin of error covers all errors."** It ignores bias. A huge voluntary-response poll can have a tiny margin of error and still be badly wrong.
- **Using $z^*$ for means with $s$.** With an estimated standard deviation, use $t^*$; the difference matters most for small samples.
- **Rounding sample size down.** $1067.1$ must become $1068$; $1067$ would give a margin of error slightly above the target.

## Practice

1. In an illustrative random sample of $500$ adults, $150$ report having read a print newspaper in the last week. Construct and interpret a $95\%$ confidence interval for the population proportion.
2. An illustrative random sample of $10$ plants has mean height $20$ cm and $s = 3$ cm, with no outliers or strong skew. Construct a $95\%$ t interval for the mean height. (Use $t^* \approx 2.262$.)
3. How large a sample is needed for a $95\%$ margin of error of at most $0.04$, using $p^* = 0.5$?
4. A researcher wants to cut a margin of error in half without changing the confidence level. By what factor must the sample size increase?
5. A $95\%$ interval for a mean is $(48, 56)$. What were the sample mean and margin of error? Would a $90\%$ interval from the same data be wider or narrower?
6. A student says, "Our $95\%$ interval for the mean commute is $(18, 24)$ minutes, so $95\%$ of students commute between $18$ and $24$ minutes." Correct the statement.
7. An illustrative two-sample interval for $\mu_1 - \mu_2$ is $(-2.1, 4.5)$. Is there convincing evidence of a difference in means? Explain.

<details>
<summary>Answer key and self-check</summary>

1. Successes $150$ and failures $350$ are both at least $10$; $500$ is less than $10\%$ of all adults. $\hat{p} = 0.30$; $\text{SE} = \sqrt{\tfrac{0.3(0.7)}{500}} \approx 0.0205$; margin of error $\approx 1.96(0.0205) \approx 0.040$. Interval $\approx (0.260, 0.340)$. We are $95\%$ confident that between about $26\%$ and $34\%$ of all adults read a print newspaper last week.
2. $\text{SE} = \tfrac{3}{\sqrt{10}} \approx 0.949$; margin of error $\approx 2.262(0.949) \approx 2.15$. Interval $\approx (17.85, 22.15)$ cm.
3. $\left(\tfrac{1.96}{0.04}\right)^2(0.25) = 600.25$, so $n = 601$.
4. By a factor of $4$, because margin of error is proportional to $\tfrac{1}{\sqrt{n}}$.
5. Sample mean $\tfrac{48 + 56}{2} = 52$; margin of error $4$. A $90\%$ interval would be narrower.
6. The interval estimates the *mean* commute of all students. Correct version: "We are $95\%$ confident that the interval from $18$ to $24$ minutes captures the mean commute time of all students." Individual commutes vary much more.
7. No. The interval includes $0$, so "no difference" is a plausible value for $\mu_1 - \mu_2$.

Self-check method: the point estimate must be the exact midpoint of the interval; for a proportion, both endpoints should be between $0$ and $1$; and a higher confidence level or smaller sample must always give a wider interval.

</details>

## Where this fits

This lesson follows [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions) in the [Statistics & Probability course](/subject/statistics-and-probability). Next, [17.8 - Significance Tests](/178-significance-tests) uses the same standard errors and conditions to judge a specific claim about a parameter, and connects tests back to intervals.

## Sources

- OpenStax, *Introductory Statistics 2e*, [8.1 A Single Population Mean using the Normal Distribution](https://openstax.org/books/introductory-statistics-2e/pages/8-1-a-single-population-mean-using-the-normal-distribution) (structure and interpretation of intervals)
- OpenStax, *Introductory Statistics 2e*, [8.2 A Single Population Mean using the Student t Distribution](https://openstax.org/books/introductory-statistics-2e/pages/8-2-a-single-population-mean-using-the-student-t-distribution)
- OpenStax, *Introductory Statistics 2e*, [8.3 A Population Proportion](https://openstax.org/books/introductory-statistics-2e/pages/8-3-a-population-proportion) (including sample-size calculation)
- OpenStax, *Introductory Statistics 2e*, [10.1 Two Population Means with Unknown Standard Deviations](https://openstax.org/books/introductory-statistics-2e/pages/10-1-two-population-means-with-unknown-standard-deviations) (Welch degrees of freedom)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [7.1.4 What are confidence intervals?](https://www.itl.nist.gov/div898/handbook/prc/section1/prc14.htm) and [1.3.6.7.2 Critical Values of the Student's t Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm)

---
title: "17.6 - Normal Distribution & Sampling Distributions"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.6"
type: chapter
objectives:
  - "Use the 68-95-99.7 rule and z-scores to find normal probabilities, and use the inverse normal to find percentiles"
  - "Explain what a sampling distribution is and distinguish it from the distribution of a population or of one sample"
  - "State the mean and standard deviation of the sampling distributions of the sample mean and the sample proportion"
  - "Check the conditions for the Central Limit Theorem and the normal approximation for a sample proportion, and use them to compute probabilities"
open_source: true
---

# 17.6 - Normal Distribution & Sampling Distributions

The normal distribution is the bell-shaped model used for many measurements and, more importantly, for the behavior of sample statistics. This lesson first develops normal-distribution calculations, then asks a new question: if you took many random samples, how would the sample mean or sample proportion vary from sample to sample? The answer, summarized by the Central Limit Theorem, is the foundation of the confidence intervals and significance tests in the next two lessons.

## Prerequisites

You need the mean and standard deviation from [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable), parameters and statistics from [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design), and expected value and the binomial distribution from [17.5 - Discrete Random Variables](/175-discrete-random-variables). You will need a calculator or software with normal-distribution functions (often named `normalcdf` and `invNorm`) or a standard normal table.

## Learning objectives

By the end of this lesson you should be able to:

1. Convert values to z-scores and find normal probabilities and percentiles.
2. Describe the sampling distribution of $\bar{x}$ and of $\hat{p}$ by shape, center, and spread.
3. Check the conditions needed to treat those sampling distributions as approximately normal.
4. Compute and interpret probabilities about a sample mean or sample proportion.

## Core ideas

### Normal distributions and z-scores

A normal distribution $N(\mu, \sigma)$ is symmetric and bell-shaped, centered at $\mu$, with inflection points at $\mu \pm \sigma$. Probabilities are areas under the density curve, so for a continuous variable $P(X = a) = 0$ and $P(X < a) = P(X \le a)$.

The **empirical rule** (68-95-99.7 rule): about $68\%$ of values fall within $1\sigma$ of $\mu$, about $95\%$ within $2\sigma$, and about $99.7\%$ within $3\sigma$. (More precisely: $68.27\%$, $95.45\%$, $99.73\%$.)

A **z-score** $z = \tfrac{x - \mu}{\sigma}$ tells how many standard deviations $x$ is from the mean. Converting to z-scores turns any normal distribution into the **standard normal** $N(0, 1)$, so one table or function covers every case. The reverse step, $x = \mu + z\sigma$, finds the value at a given percentile.

### Assessing normality

Not every data set is approximately normal. Check a histogram or dot plot for a single peak and rough symmetry, and use a **normal probability plot** (data values against expected z-scores): a roughly straight pattern supports normality, and a curved pattern indicates skew.

### Sampling distributions

The **sampling distribution** of a statistic is the distribution of its values across all possible random samples of the same size from the same population. It is different from the distribution of the population and from the distribution of the data in any one sample.

**Sample mean.** For random samples of size $n$ from a population with mean $\mu$ and standard deviation $\sigma$:

$$\mu_{\bar{x}} = \mu, \qquad \sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}.$$

The sample mean is unbiased (centered at $\mu$), and its variability shrinks as $n$ grows. The $\sqrt{n}$ means that quadrupling the sample size halves the standard deviation of $\bar{x}$.

**Central Limit Theorem (CLT).** When $n$ is large, the sampling distribution of $\bar{x}$ is approximately normal *whatever the shape of the population*. A common rule of thumb is $n \ge 30$; strongly skewed populations may need more. If the population itself is normal, $\bar{x}$ is exactly normal for any $n$.

**Sample proportion.** For random samples of size $n$ from a population with proportion of successes $p$:

$$\mu_{\hat{p}} = p, \qquad \sigma_{\hat{p}} = \sqrt{\frac{p(1 - p)}{n}}.$$

The sampling distribution of $\hat{p}$ is approximately normal when the **large counts condition** holds: $np \ge 10$ and $n(1 - p) \ge 10$.

**Independence.** Both standard-deviation formulas assume independent observations. When sampling without replacement, check the **10% condition**: $n$ is at most $10\%$ of the population.

## Worked examples

### Example 1: Normal probabilities

Illustrative scores on a standardized test are modeled as $N(500, 100)$.

1. $P(X < 650)$: $z = \tfrac{650 - 500}{100} = 1.5$, and $P(Z < 1.5) \approx 0.9332$. About $93.3\%$ of scores are below $650$.
2. $P(400 < X < 600)$: $z = -1$ to $z = 1$, so about $0.6827$, matching the empirical rule.
3. $P(X > 720)$: $z = 2.2$, and $P(Z > 2.2) \approx 0.0139$.

### Example 2: Percentile with the inverse normal

What score marks the 90th percentile of $N(500, 100)$?

1. The z-score with area $0.90$ to its left is $z \approx 1.2816$.
2. $x = \mu + z\sigma = 500 + 1.2816(100) \approx 628.2$.

About $90\%$ of scores are below about $628$.

### Example 3: Central Limit Theorem for a sample mean

An illustrative population of delivery times is strongly right-skewed with $\mu = 50$ minutes and $\sigma = 12$ minutes. Take a random sample of $36$ deliveries from a large population. Find $P(\bar{x} > 53)$.

1. Center and spread: $\mu_{\bar{x}} = 50$ and $\sigma_{\bar{x}} = \tfrac{12}{\sqrt{36}} = 2$ minutes.
2. Shape: the population is skewed, but $n = 36 \ge 30$, so by the CLT $\bar{x}$ is approximately normal. The sample of $36$ is far less than $10\%$ of a large population.
3. $z = \tfrac{53 - 50}{2} = 1.5$, so $P(\bar{x} > 53) \approx P(Z > 1.5) \approx 0.0668$.

You could **not** use this normal calculation to find the probability that a *single* delivery takes more than $53$ minutes, because individual times are skewed, not normal.

### Example 4: Sampling distribution of a sample proportion

Illustratively, $40\%$ of a large town's voters support a proposal. In a random sample of $150$ voters, find $P(\hat{p} < 0.33)$.

1. $\mu_{\hat{p}} = 0.40$ and $\sigma_{\hat{p}} = \sqrt{\tfrac{0.4(0.6)}{150}} = \sqrt{0.0016} = 0.04$.
2. Large counts: $150(0.4) = 60 \ge 10$ and $150(0.6) = 90 \ge 10$, so $\hat{p}$ is approximately normal.
3. $z = \tfrac{0.33 - 0.40}{0.04} = -1.75$, so $P(\hat{p} < 0.33) \approx 0.0401$.

A sample this far below $0.40$ would happen only about $4\%$ of the time if the true proportion were $0.40$. That style of reasoning is the basis of significance testing in 17.8.

## Common misconceptions and boundary cases

- **"The CLT makes the data normal."** The CLT is about the distribution of $\bar{x}$ across many samples. A large sample from a skewed population still has skewed data.
- **Using $\sigma$ instead of $\sigma / \sqrt{n}$.** Questions about a sample mean need the standard deviation of $\bar{x}$; questions about one individual need $\sigma$.
- **Applying the empirical rule to any data set.** The 68-95-99.7 percentages hold only for approximately normal distributions.
- **Skipping the large counts check.** With $p = 0.1$ and $n = 50$, $np = 5 < 10$; the distribution of $\hat{p}$ is noticeably right-skewed and a normal calculation can be misleading.
- **Thinking bigger populations need bigger samples.** As long as the 10% condition holds, $\sigma_{\bar{x}}$ and $\sigma_{\hat{p}}$ depend on $n$, not on the population size.

## Practice

1. Illustrative quiz scores are $N(70, 10)$. What is the z-score of $85$, and what proportion of scores are above $85$?
2. Illustrative adult heights in a population are $N(64, 2.5)$ inches. Find $P(X < 60)$ and $P(61.5 < X < 66.5)$.
3. For the heights in problem 2, find the height that marks the top $5\%$.
4. For the heights in problem 2, find $P(\bar{x} > 65)$ for a random sample of $25$ adults.
5. A population has $\sigma = 20$. What sample size makes $\sigma_{\bar{x}} = 5$? What happens to $\sigma_{\bar{x}}$ if $n$ is multiplied by $4$ again?
6. In a population with $p = 0.1$, can you use a normal model for $\hat{p}$ when $n = 50$? When $n = 200$?
7. Explain the difference between the distribution of a population, the distribution of one sample, and the sampling distribution of $\bar{x}$.

<details>
<summary>Answer key and self-check</summary>

1. $z = \tfrac{85 - 70}{10} = 1.5$; $P(Z > 1.5) \approx 0.0668$, so about $6.7\%$.
2. $z = \tfrac{60 - 64}{2.5} = -1.6$, so $P(X < 60) \approx 0.0548$. $61.5$ and $66.5$ are $\mu \pm \sigma$, so $P \approx 0.6827$.
3. $z \approx 1.645$; $x = 64 + 1.645(2.5) \approx 68.1$ inches.
4. $\sigma_{\bar{x}} = \tfrac{2.5}{\sqrt{25}} = 0.5$; $z = \tfrac{65 - 64}{0.5} = 2$; $P(Z > 2) \approx 0.0228$. The population is normal, so $\bar{x}$ is exactly normal even though $n < 30$.
5. $\tfrac{20}{\sqrt{n}} = 5$ gives $\sqrt{n} = 4$, so $n = 16$. With $n = 64$, $\sigma_{\bar{x}} = \tfrac{20}{8} = 2.5$, half as large.
6. $n = 50$: $np = 5 < 10$, so no. $n = 200$: $np = 20$ and $n(1 - p) = 180$, so yes (assuming a random sample under $10\%$ of the population).
7. The population distribution describes all individuals. A sample's distribution describes the $n$ individuals in one sample. The sampling distribution describes the values of $\bar{x}$ from all possible samples of size $n$; it is centered at $\mu$ with spread $\sigma / \sqrt{n}$.

Self-check method: sketch the normal curve and shade the region before computing; the answer must be less than $0.5$ when the shaded tail is on one side of the mean, and z-scores beyond $\pm 3$ should give tail areas below about $0.0015$.

</details>

## Where this fits

This lesson follows [17.5 - Discrete Random Variables](/175-discrete-random-variables) in the [Statistics & Probability course](/subject/statistics-and-probability). Next, [17.7 - Confidence Intervals](/177-confidence-intervals) reverses Example 4: instead of starting from a known $p$, it uses an observed $\hat{p}$ and its standard deviation to estimate an unknown $p$.

## Sources

- OpenStax, *Introductory Statistics 2e*, [6.1 The Standard Normal Distribution](https://openstax.org/books/introductory-statistics-2e/pages/6-1-the-standard-normal-distribution)
- OpenStax, *Introductory Statistics 2e*, [6.2 Using the Normal Distribution](https://openstax.org/books/introductory-statistics-2e/pages/6-2-using-the-normal-distribution)
- OpenStax, *Introductory Statistics 2e*, [7.1 The Central Limit Theorem for Sample Means (Averages)](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-averages)
- OpenStax, *Introductory Statistics 2e*, [7.3 Using the Central Limit Theorem](https://openstax.org/books/introductory-statistics-2e/pages/7-3-using-the-central-limit-theorem)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [1.3.6.6.1 Normal Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm)

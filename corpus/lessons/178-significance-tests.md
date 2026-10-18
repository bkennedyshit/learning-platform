---
title: "17.8 - Significance Tests"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.8"
type: chapter
objectives:
  - "State null and alternative hypotheses about a parameter and choose a one-sided or two-sided alternative from the research question"
  - "Carry out a one-proportion z test, a one-sample or paired t test, and a chi-square goodness-of-fit test, including conditions, test statistic, p-value, and conclusion in context"
  - "Interpret a p-value correctly and explain the relationship between the significance level, Type I and Type II errors, and power"
  - "Connect a two-sided test to the corresponding confidence interval and distinguish statistical significance from practical importance"
open_source: true
---

# 17.8 - Significance Tests

A significance test asks whether sample data give convincing evidence against a specific claim about a population. The logic resembles proof by contradiction with uncertainty: assume the claim is true, work out how surprising the observed data would be, and reject the claim if the data would be very surprising. This lesson covers the general procedure, the most common tests, and how to read and misread the results.

## Prerequisites

You need sampling distributions and z-scores from [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions), and the conditions, standard errors, and t distributions from [17.7 - Confidence Intervals](/177-confidence-intervals). Use a calculator or software that gives normal, $t$, and chi-square tail areas.

## Learning objectives

By the end of this lesson you should be able to:

1. Write $H_0$ and $H_a$ in symbols and words for a stated research question.
2. Carry out a complete test: hypotheses, conditions, test statistic, p-value, decision, and conclusion in context.
3. Interpret a p-value and describe Type I error, Type II error, and power in context.
4. Use a confidence interval to reach the same decision as a two-sided test, and judge practical importance separately from statistical significance.

## Core ideas

### Hypotheses

The **null hypothesis** $H_0$ is the claim of "no effect" or "no difference", stated as an equality about a parameter, such as $H_0\!: p = 0.5$. The **alternative hypothesis** $H_a$ is what the researcher suspects or wants evidence for: $p > 0.5$ or $p < 0.5$ (**one-sided**) or $p \ne 0.5$ (**two-sided**). Choose $H_a$ from the research question *before* looking at the data. Hypotheses are always about parameters ($p$, $\mu$), never about statistics ($\hat{p}$, $\bar{x}$).

### Test statistic and p-value

A **test statistic** measures how far the statistic is from the null value in standard-error units:

$$\text{test statistic} = \frac{\text{statistic} - \text{null value}}{\text{standard error of the statistic}}.$$

The **p-value** is the probability, *computed assuming $H_0$ is true*, of getting a test statistic at least as extreme as the one observed, in the direction(s) given by $H_a$. A small p-value means the data would be unusual if $H_0$ were true, which is evidence against $H_0$.

Compare the p-value with a **significance level** $\alpha$ chosen in advance (often $0.05$). If the p-value is at most $\alpha$, **reject $H_0$**: there is convincing evidence for $H_a$. Otherwise, **fail to reject $H_0$**: there is not convincing evidence for $H_a$. Never "accept" $H_0$; lack of evidence against a claim is not proof of it.

### Common tests

- **One-proportion z test:** $z = \dfrac{\hat{p} - p_0}{\sqrt{p_0(1 - p_0)/n}}$. Note that the standard error uses the null value $p_0$. Conditions: random, 10%, and $np_0 \ge 10$ and $n(1 - p_0) \ge 10$.
- **One-sample t test:** $t = \dfrac{\bar{x} - \mu_0}{s/\sqrt{n}}$ with $\text{df} = n - 1$. Conditions as for the t interval.
- **Paired t test:** for matched pairs, compute each pair's difference and run a one-sample t test on the differences, usually with $H_0\!: \mu_d = 0$.
- **Two-sample t test:** $t = \dfrac{(\bar{x}_1 - \bar{x}_2) - 0}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$ for independent groups, with degrees of freedom as in 17.7.
- **Chi-square goodness-of-fit test:** for one categorical variable with $k$ categories, $\chi^2 = \sum \dfrac{(\text{observed} - \text{expected})^2}{\text{expected}}$ with $\text{df} = k - 1$; the p-value is the upper-tail area. Condition: all expected counts at least $5$. The **chi-square test of independence** applies the same statistic to a two-way table, with $\text{df} = (\text{rows} - 1)(\text{columns} - 1)$. **ANOVA** extends the two-sample comparison of means to three or more groups.

### Errors and power

| | $H_0$ true | $H_0$ false |
|---|---|---|
| **Reject $H_0$** | Type I error (probability $\alpha$) | Correct decision (probability = power) |
| **Fail to reject $H_0$** | Correct decision | Type II error (probability $\beta$) |

The **power** of a test is the probability of rejecting $H_0$ when a particular alternative value is true; power $= 1 - \beta$. Power increases with larger sample size, larger $\alpha$, and a true value farther from the null value. For instance, for a one-sided test of $H_0\!: p = 0.5$ against $H_a\!: p > 0.5$ with $n = 100$ and $\alpha = 0.05$, the test rejects when $\hat{p} \ge 0.5 + 1.645(0.05) \approx 0.582$; if the true proportion is $0.6$, the power is about $0.64$.

### Tests and intervals

A two-sided test at level $\alpha$ and a $100(1 - \alpha)\%$ confidence interval for a mean lead to the same decision: reject $H_0\!: \mu = \mu_0$ exactly when $\mu_0$ lies outside the interval. For proportions the match is close but not always exact, because the test's standard error uses $p_0$ while the interval's uses $\hat{p}$.

## Worked examples

### Example 1: One-proportion z test

An illustrative coin is tossed $100$ times and lands heads $60$ times. Is there convincing evidence at $\alpha = 0.05$ that the coin is not fair?

1. Hypotheses: $H_0\!: p = 0.5$ and $H_a\!: p \ne 0.5$, where $p$ is the long-run proportion of heads.
2. Conditions: tosses are independent trials; $100(0.5) = 50 \ge 10$ and $100(0.5) = 50 \ge 10$.
3. Test statistic: $\hat{p} = 0.6$; $\text{SE} = \sqrt{\tfrac{0.5(0.5)}{100}} = 0.05$; $z = \tfrac{0.6 - 0.5}{0.05} = 2.00$.
4. p-value: two-sided, $2P(Z \ge 2.00) \approx 0.0455$.
5. Conclusion: $0.0455 \le 0.05$, so reject $H_0$. There is convincing evidence at the $5\%$ level that the coin's long-run proportion of heads is not $0.5$.

Boundary note: an exact binomial test on the same data gives a two-sided p-value of about $0.057$, which would *not* be significant at $\alpha = 0.05$. A result this close to the cutoff is weak evidence either way, and the specific method matters.

### Example 2: One-sample t test

A filling machine is supposed to put $500$ mL in each bottle. An illustrative random sample of $25$ bottles has $\bar{x} = 497.8$ mL and $s = 5$ mL, and the data show no strong skew or outliers. Test at $\alpha = 0.05$ whether the mean fill differs from $500$ mL.

1. Hypotheses: $H_0\!: \mu = 500$ and $H_a\!: \mu \ne 500$.
2. Conditions: random sample; $25$ bottles are well under $10\%$ of production; no strong skew or outliers.
3. $\text{SE} = \tfrac{5}{\sqrt{25}} = 1$; $t = \tfrac{497.8 - 500}{1} = -2.20$ with $\text{df} = 24$.
4. p-value: $2P(t_{24} \le -2.20) \approx 0.038$.
5. Conclusion: $0.038 \le 0.05$, so reject $H_0$. There is convincing evidence that the machine's mean fill differs from $500$ mL. At $\alpha = 0.01$ the decision would be to fail to reject.
6. Practical importance: the estimated shortfall is $2.2$ mL, under $0.5\%$ of the target. Whether that matters is a question about the product, not about the p-value.

### Example 3: Chi-square goodness-of-fit test

An illustrative die is rolled $120$ times, with counts $25, 17, 15, 23, 24, 16$ for faces $1$ through $6$. Is there convincing evidence at $\alpha = 0.05$ that the die is unfair?

1. Hypotheses: $H_0$: each face has probability $\tfrac{1}{6}$; $H_a$: at least one face has a different probability.
2. Expected count for each face: $\tfrac{120}{6} = 20 \ge 5$.
3. $\chi^2 = \tfrac{5^2 + (-3)^2 + (-5)^2 + 3^2 + 4^2 + (-4)^2}{20} = \tfrac{25 + 9 + 25 + 9 + 16 + 16}{20} = \tfrac{100}{20} = 5.0$, with $\text{df} = 6 - 1 = 5$.
4. p-value: $P(\chi^2_5 \ge 5.0) \approx 0.416$.
5. Conclusion: $0.416 > 0.05$, so fail to reject $H_0$. These rolls do not give convincing evidence that the die is unfair. This does not prove the die is fair.

## Common misconceptions and boundary cases

- **"The p-value is the probability that $H_0$ is true."** It is a probability about the data, computed by assuming $H_0$ is true. It does not give the probability of either hypothesis.
- **"Fail to reject" means "$H_0$ is true".** A small sample can fail to detect a real effect; that is a Type II error, and it is more likely when power is low.
- **Statistical significance means importance.** With a very large sample, a tiny and unimportant difference can produce a small p-value. Report an interval or effect size with the test.
- **Choosing a one-sided alternative after seeing the data.** Picking the direction to match the data halves the p-value unfairly. The alternative must come from the question, before data collection.
- **Running many tests and reporting only significant ones.** At $\alpha = 0.05$, about $1$ in $20$ tests of true null hypotheses will reject by chance alone.
- **Ignoring conditions.** A t test on a small, strongly skewed sample, or a chi-square test with expected counts below $5$, can give misleading p-values.

## Practice

1. For each, write $H_0$ and $H_a$: (a) a school claims the mean commute is $20$ minutes and a student suspects it is longer; (b) a manufacturer claims $5\%$ of parts are defective and an inspector suspects the rate is different.
2. An illustrative company claims $20\%$ of customers use a coupon. In a random sample of $200$ customers, $52$ do. Test $H_0\!: p = 0.2$ against $H_a\!: p > 0.2$ at $\alpha = 0.05$.
3. Eight illustrative students take a pretest and a posttest. The score differences (post minus pre) are $2, -1, 3, 4, 0, 2, 5, 1$. Find the mean and standard deviation of the differences and the paired t statistic, and use the two-sided p-value $\approx 0.025$ to state a conclusion at $\alpha = 0.05$.
4. An illustrative spinner with three equal sections lands $40, 25, 25$ times on red, blue, green in $90$ spins. Compute $\chi^2$ and its df, and use the p-value $\approx 0.082$ to state a conclusion at $\alpha = 0.05$.
5. In Example 2, describe a Type I error and a Type II error in context.
6. Name two ways to increase the power of a test.
7. A $95\%$ confidence interval for a mean is $(3.1, 5.4)$. Would a two-sided test of $H_0\!: \mu = 5$ at $\alpha = 0.05$ reject? Of $H_0\!: \mu = 6$?

<details>
<summary>Answer key and self-check</summary>

1. (a) $H_0\!: \mu = 20$, $H_a\!: \mu > 20$, where $\mu$ is the mean commute of all students. (b) $H_0\!: p = 0.05$, $H_a\!: p \ne 0.05$, where $p$ is the proportion of all parts that are defective.
2. Conditions: random; $200(0.2) = 40 \ge 10$ and $200(0.8) = 160 \ge 10$. $\hat{p} = 0.26$; $\text{SE} = \sqrt{\tfrac{0.2(0.8)}{200}} \approx 0.0283$; $z \approx 2.12$; p-value $\approx 0.017$. Reject $H_0$: there is convincing evidence that more than $20\%$ of customers use a coupon.
3. Mean difference $2$; $s_d = 2$; $t = \tfrac{2 - 0}{2/\sqrt{8}} \approx 2.83$ with $\text{df} = 7$. $0.025 \le 0.05$, so reject $H_0\!: \mu_d = 0$: convincing evidence that the mean score changed (increased) for students like these.
4. Expected $30$ each. $\chi^2 = \tfrac{10^2 + (-5)^2 + (-5)^2}{30} = \tfrac{150}{30} = 5.0$ with $\text{df} = 2$. $0.082 > 0.05$, so fail to reject: not convincing evidence that the spinner is unfair.
5. Type I: concluding the mean fill differs from $500$ mL when it really is $500$ mL (perhaps leading to an unnecessary machine adjustment). Type II: failing to detect that the mean fill really differs from $500$ mL (underfilled bottles keep shipping).
6. Any two of: increase the sample size; increase $\alpha$; reduce variability (for example, with better measurement or blocking); test against a true value farther from the null value, which the researcher usually cannot control.
7. $5$ is inside the interval, so do not reject. $6$ is outside, so reject.

Self-check method: a p-value must be between $0$ and $1$; a larger $\lvert z \rvert$, $\lvert t \rvert$, or $\chi^2$ must give a smaller p-value; a two-sided p-value is twice the one-tail area; and your conclusion must mention the parameter in context and the direction in $H_a$.

</details>

## Where this fits

This is the final lesson in the [Statistics & Probability course](/subject/statistics-and-probability). It follows [17.7 - Confidence Intervals](/177-confidence-intervals) and draws on the study-design ideas of [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design): a significant result from a randomized experiment supports a causal conclusion, while one from an observational study does not. To review the whole path, return to [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable).

## Sources

- OpenStax, *Introductory Statistics 2e*, [9.1 Null and Alternative Hypotheses](https://openstax.org/books/introductory-statistics-2e/pages/9-1-null-and-alternative-hypotheses)
- OpenStax, *Introductory Statistics 2e*, [9.2 Outcomes and the Type I and Type II Errors](https://openstax.org/books/introductory-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors)
- OpenStax, *Introductory Statistics 2e*, [9.4 Rare Events, the Sample, Decision and Conclusion](https://openstax.org/books/introductory-statistics-2e/pages/9-4-rare-events-the-sample-decision-and-conclusion)
- OpenStax, *Introductory Statistics 2e*, [9.5 Additional Information and Full Hypothesis Test Examples](https://openstax.org/books/introductory-statistics-2e/pages/9-5-additional-information-and-full-hypothesis-test-examples)
- OpenStax, *Introductory Statistics 2e*, [10.4 Matched or Paired Samples](https://openstax.org/books/introductory-statistics-2e/pages/10-4-matched-or-paired-samples)
- OpenStax, *Introductory Statistics 2e*, [11.2 Goodness-of-Fit Test](https://openstax.org/books/introductory-statistics-2e/pages/11-2-goodness-of-fit-test) and [11.3 Test of Independence](https://openstax.org/books/introductory-statistics-2e/pages/11-3-test-of-independence)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [7.1.3.1 Critical values and p values](https://www.itl.nist.gov/div898/handbook/prc/section1/prc131.htm) and [1.3.6.6.6 Chi-Square Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm)

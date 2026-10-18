---
title: "17.5 - Discrete Random Variables"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.5"
type: chapter
objectives:
  - "Verify a discrete probability distribution and use it to find probabilities of events"
  - "Compute and interpret the expected value, variance, and standard deviation of a discrete random variable"
  - "Check the binomial and geometric conditions and compute their probabilities, means, and standard deviations"
  - "Find the mean and standard deviation of a linear transformation and of a sum or difference of independent random variables"
open_source: true
---

# 17.5 - Discrete Random Variables

A **random variable** assigns a number to each outcome of a chance process: the number of heads in ten tosses, the payout of a game, the number of customers who arrive in an hour. Describing a random variable's possible values and their probabilities lets you predict its long-run average and variability. This lesson covers discrete distributions in general and two families that appear constantly: the binomial and the geometric.

## Prerequisites

You need the complement and multiplication rules and independence from [17.4 - Probability](/174-probability), and the idea of mean and standard deviation from [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable). Binomial coefficients $\binom{n}{k}$ are introduced in [16.7 - Sequences, Series & the Binomial Theorem](/167-sequences-series-the-binomial-theorem); the formula is restated below.

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether a table is a valid probability distribution and use it to answer probability questions.
2. Compute $E(X)$, $\text{Var}(X)$, and $\sigma_X$ and interpret the expected value as a long-run average.
3. Recognize binomial and geometric settings and compute their probabilities and summary values.
4. Apply the rules for $a + bX$ and for $X \pm Y$ when $X$ and $Y$ are independent.

## Core ideas

### Discrete distributions

A **discrete** random variable has a countable list of possible values (usually whole-number counts). A **continuous** random variable takes any value in an interval, such as a time or a height; it is handled with density curves in 17.6. A discrete **probability distribution** lists each value $x_i$ with its probability $p_i$, and it is valid only if every $p_i$ is between $0$ and $1$ and $\sum p_i = 1$.

### Expected value and variability

$$E(X) = \mu_X = \sum x_i p_i, \qquad \text{Var}(X) = \sigma_X^2 = \sum (x_i - \mu_X)^2 p_i, \qquad \sigma_X = \sqrt{\text{Var}(X)}.$$

An equivalent shortcut is $\text{Var}(X) = E(X^2) - [E(X)]^2$. The expected value is the long-run average of $X$ over many repetitions; it need not be a possible value of $X$.

### Binomial distributions

A count $X$ is **binomial** when four conditions hold (often remembered as BINS):

- **B**inary: each trial is a success or a failure.
- **I**ndependent trials.
- **N**umber of trials $n$ is fixed in advance.
- **S**ame probability of success $p$ on each trial.

Then, for $k = 0, 1, \ldots, n$,

$$P(X = k) = \binom{n}{k} p^k (1 - p)^{n - k}, \qquad \binom{n}{k} = \frac{n!}{k!\,(n - k)!},$$

with $\mu_X = np$ and $\sigma_X = \sqrt{np(1 - p)}$. The coefficient counts the arrangements of $k$ successes among $n$ trials; each arrangement has probability $p^k(1 - p)^{n - k}$ by the multiplication rule.

When sampling *without* replacement, trials are not exactly independent. The binomial model is still a good approximation if the sample is at most $10\%$ of the population (the **10% condition**).

### Geometric distributions

If independent trials each succeed with probability $p$ and $X$ counts the trial on which the *first* success occurs, then $X$ is **geometric**:

$$P(X = k) = (1 - p)^{k - 1} p, \quad k = 1, 2, 3, \ldots, \qquad \mu_X = \frac{1}{p}, \qquad \sigma_X = \frac{\sqrt{1 - p}}{p}.$$

Also, $P(X > k) = (1 - p)^k$, since the first $k$ trials must all fail. Unlike the binomial, there is no fixed number of trials.

### Transforming and combining random variables

- For $Y = a + bX$: $\mu_Y = a + b\mu_X$ and $\sigma_Y = \lvert b \rvert \sigma_X$.
- For any $X$ and $Y$: $\mu_{X + Y} = \mu_X + \mu_Y$ and $\mu_{X - Y} = \mu_X - \mu_Y$.
- If $X$ and $Y$ are **independent**: $\text{Var}(X + Y) = \text{Var}(X - Y) = \text{Var}(X) + \text{Var}(Y)$. Variances add; standard deviations do not.

## Worked examples

### Example 1: Expected value and standard deviation from a table

An illustrative model for the number of goals $X$ a team scores in a game:

| $x$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $P(X = x)$ | 0.1 | 0.3 | 0.4 | 0.2 |

1. Valid: each probability is in $[0, 1]$ and $0.1 + 0.3 + 0.4 + 0.2 = 1$.
2. $P(X \ge 2) = 0.4 + 0.2 = 0.6$.
3. $E(X) = 0(0.1) + 1(0.3) + 2(0.4) + 3(0.2) = 0 + 0.3 + 0.8 + 0.6 = 1.7$ goals.
4. $E(X^2) = 0 + 1(0.3) + 4(0.4) + 9(0.2) = 3.7$, so $\text{Var}(X) = 3.7 - 1.7^2 = 3.7 - 2.89 = 0.81$ and $\sigma_X = 0.9$ goals.
5. Transformation: if a sponsor pays $Y = 5X - 2$ points per game, $\mu_Y = 5(1.7) - 2 = 6.5$ and $\sigma_Y = 5(0.9) = 4.5$.
6. Sum: for two independent games, the total $T = X_1 + X_2$ has $\mu_T = 3.4$ and $\text{Var}(T) = 0.81 + 0.81 = 1.62$, so $\sigma_T = \sqrt{1.62} \approx 1.27$, not $0.9 + 0.9 = 1.8$.

### Example 2: Binomial probabilities

An illustrative basketball player makes $30\%$ of her three-point attempts, and attempts are treated as independent. She takes $10$ attempts. Let $X$ be the number made.

1. Conditions: make/miss (binary), independent by assumption, $n = 10$ fixed, $p = 0.3$ each time. $X$ is binomial.
2. $P(X = 3) = \binom{10}{3}(0.3)^3(0.7)^7 = 120 \cdot 0.027 \cdot 0.0823543 \approx 0.2668$.
3. $P(X \le 1) = (0.7)^{10} + 10(0.3)(0.7)^9 \approx 0.0282 + 0.1211 = 0.1493$.
4. $P(X \ge 2) = 1 - 0.1493 = 0.8507$.
5. $\mu_X = 10(0.3) = 3$ makes and $\sigma_X = \sqrt{10(0.3)(0.7)} = \sqrt{2.1} \approx 1.45$ makes.

### Example 3: Geometric probabilities

An illustrative quality inspector finds that $20\%$ of items from a line need adjustment, independently. Let $X$ be the number of the first item that needs adjustment.

1. $P(X = 3) = (0.8)^2(0.2) = 0.128$: the first two pass and the third fails.
2. $P(X > 3) = (0.8)^3 = 0.512$: the first three all pass.
3. $\mu_X = \tfrac{1}{0.2} = 5$ items and $\sigma_X = \tfrac{\sqrt{0.8}}{0.2} \approx 4.47$ items.

## Common misconceptions and boundary cases

- **Expecting $E(X)$ to be a possible value.** $E(X) = 1.7$ goals in Example 1; no game has $1.7$ goals. It is a long-run average.
- **Adding standard deviations.** For independent variables, add variances and then take the square root.
- **Subtracting variances for a difference.** $\text{Var}(X - Y) = \text{Var}(X) + \text{Var}(Y)$ for independent variables; subtracting adds variability.
- **Using the binomial without a fixed $n$.** "Roll until you get a six" has no fixed number of trials; it is geometric, not binomial.
- **Ignoring dependence.** Counting hearts in $5$ cards drawn from a $52$-card deck is not exactly binomial, because the draws are dependent; $5$ is about $9.6\%$ of $52$, so the binomial is only a rough approximation. Counting hearts in $20$ cards violates the 10% condition badly.
- **Confusing $P(X \le k)$ and $P(X < k)$.** For discrete variables these differ by $P(X = k)$, which can be large.

## Practice

1. Is this a valid distribution? $P(X = 0) = 0.25$, $P(X = 1) = 0.5$, $P(X = 2) = 0.35$. Explain.
2. An illustrative raffle sells tickets for \$2. A ticket wins \$100 with probability $0.01$, \$10 with probability $0.09$, and nothing otherwise. Find the expected winnings per ticket and the expected net gain.
3. Toss a fair coin $5$ times. Find $P(\text{exactly } 4 \text{ heads})$ and $P(\text{at least } 4 \text{ heads})$.
4. Illustratively, $10\%$ of a large population is left-handed. In a random sample of $20$ people, find the mean and standard deviation of the number of left-handers, and $P(\text{none})$.
5. Roll a fair die until a six appears. Find the probability the first six is on the 4th roll and the expected number of rolls.
6. $X$ has mean $10$ and standard deviation $3$; $Y$ has mean $4$ and standard deviation $4$; they are independent. Find the mean and standard deviation of $X + Y$ and of $X - Y$.
7. A game costs \$1 to play. With probability $0.2$ you win \$5 (a net gain of \$4); otherwise you lose your \$1. Is the game fair, meaning expected net gain $0$?

<details>
<summary>Answer key and self-check</summary>

1. No; the probabilities sum to $1.1$, not $1$.
2. $E(\text{winnings}) = 100(0.01) + 10(0.09) + 0(0.9) = 1 + 0.9 = 1.90$ dollars. Expected net gain $= 1.90 - 2 = -0.10$ dollars, a loss of 10 cents per ticket on average.
3. $P(4) = \binom{5}{4}(0.5)^5 = \tfrac{5}{32} = 0.15625$. $P(\ge 4) = \tfrac{5 + 1}{32} = \tfrac{6}{32} = 0.1875$.
4. $\mu = 20(0.1) = 2$; $\sigma = \sqrt{20(0.1)(0.9)} = \sqrt{1.8} \approx 1.34$; $P(0) = 0.9^{20} \approx 0.1216$. (A sample of $20$ is well under $10\%$ of a large population.)
5. $\left(\tfrac{5}{6}\right)^3 \cdot \tfrac{1}{6} = \tfrac{125}{1296} \approx 0.0965$. Expected rolls: $\tfrac{1}{1/6} = 6$.
6. $\mu_{X+Y} = 14$ and $\mu_{X-Y} = 6$. Both have variance $9 + 16 = 25$, so both standard deviations are $5$.
7. Expected net gain $= 4(0.2) + (-1)(0.8) = 0.8 - 0.8 = 0$. Yes, the game is fair.

Self-check method: confirm probabilities sum to $1$; confirm $E(X)$ lies between the smallest and largest possible values; for binomial problems, confirm $\sum_{k=0}^{n} P(X = k) = 1$ on a calculator; and remember $\sigma$ can never be negative.

</details>

## Where this fits

This lesson follows [17.4 - Probability](/174-probability) in the [Statistics & Probability course](/subject/statistics-and-probability). Next, [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions) moves to continuous random variables and shows that, for large $n$, the binomial distribution is approximately normal. The binomial coefficients here are the same ones in [16.7 - Sequences, Series & the Binomial Theorem](/167-sequences-series-the-binomial-theorem).

## Sources

- OpenStax, *Introductory Statistics 2e*, [4.1 Probability Distribution Function (PDF) for a Discrete Random Variable](https://openstax.org/books/introductory-statistics-2e/pages/4-1-probability-distribution-function-pdf-for-a-discrete-random-variable)
- OpenStax, *Introductory Statistics 2e*, [4.2 Mean or Expected Value and Standard Deviation](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation)
- OpenStax, *Introductory Statistics 2e*, [4.3 Binomial Distribution](https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution)
- OpenStax, *Introductory Statistics 2e*, [4.4 Geometric Distribution](https://openstax.org/books/introductory-statistics-2e/pages/4-4-geometric-distribution)
- NIST/SEMATECH *e-Handbook of Statistical Methods*, [1.3.6.6.18 Binomial Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)

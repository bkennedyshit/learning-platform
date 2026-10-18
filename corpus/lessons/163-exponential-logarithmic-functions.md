---
title: "16.3 - Exponential & Logarithmic Functions"
subject: "Algebra II & Pre-Calculus"
catalog: k12
audience_tier: 9-12
chapter: "16.3"
type: chapter
objectives:
  - "Distinguish exponential growth from decay and model each with a base or with the number e"
  - "Convert between exponential and logarithmic form and evaluate logarithms exactly"
  - "Expand and condense logarithmic expressions with the product, quotient, power, and change-of-base rules"
  - "Solve exponential and logarithmic equations and reject extraneous solutions"
open_source: true
---

# 16.3 - Exponential & Logarithmic Functions

An exponential function multiplies by the same factor over every equal step of input, and a logarithm undoes that multiplication by asking which exponent produced a given number. Together they model compound interest, population growth, radioactive decay, and any quantity that changes by a constant percentage. This lesson defines both families, shows the rules for working with logarithms, and uses them to solve equations.

## Prerequisites

You need the exponent rules from [14.7 - Exponents & Polynomials](/147-exponents-polynomials), including negative and zero exponents, and the idea of function notation and inverses from [14.4 - Functions & Relations](/144-functions-relations). A scientific calculator with $\ln$ and $\log$ keys is needed for decimal answers.

## Learning objectives

By the end of this lesson you should be able to:

1. Decide whether $f(x) = a \cdot b^x$ shows growth or decay and state its domain, range, and asymptote.
2. Rewrite $b^y = x$ as $\log_b x = y$ and the reverse, and evaluate logarithms exactly when possible.
3. Apply the product, quotient, power, and change-of-base rules to expand, condense, and evaluate logarithms.
4. Solve exponential equations with common bases or logarithms, solve logarithmic equations, and check for extraneous solutions.
5. Use compound-interest and half-life formulas to answer "how much" and "how long" questions.

## Core ideas

### Exponential functions

An **exponential function** has the form $f(x) = a \cdot b^x$ with $a \neq 0$, $b \gt 0$, and $b \neq 1$. If $a \gt 0$ and $b \gt 1$, the function shows **growth**; if $0 \lt b \lt 1$, it shows **decay**. The domain is all real numbers, the range (for $a \gt 0$) is $y \gt 0$, the $y$-intercept is $(0, a)$, and the line $y = 0$ is a horizontal asymptote.

A quantity that changes by rate $r$ per period follows $A = A_0(1 + r)^t$ for growth and $A = A_0(1 - r)^t$ for decay. Money compounded $n$ times per year at annual rate $r$ grows as

$$A = P\left(1 + \frac{r}{n}\right)^{nt},$$

and as $n$ grows without bound this approaches **continuous compounding**, $A = Pe^{rt}$. The number $e \approx 2.71828$ is the limit of $\left(1 + \tfrac{1}{n}\right)^n$ as $n \to \infty$.

### Logarithms

For $b \gt 0$, $b \neq 1$, and $x \gt 0$:

$$\log_b x = y \quad \text{means} \quad b^y = x.$$

So $\log_b x$ is the exponent you put on $b$ to get $x$. The function $y = \log_b x$ is the inverse of $y = b^x$: its domain is $x \gt 0$, its range is all real numbers, and $x = 0$ is a vertical asymptote. Two bases have special notation: $\log x$ means $\log_{10} x$ (the **common logarithm**) and $\ln x$ means $\log_e x$ (the **natural logarithm**).

### Rules of logarithms

For positive $M$ and $N$:

- Product: $\log_b(MN) = \log_b M + \log_b N$.
- Quotient: $\log_b\left(\dfrac{M}{N}\right) = \log_b M - \log_b N$.
- Power: $\log_b(M^p) = p \log_b M$.
- Inverse: $\log_b(b^x) = x$ and $b^{\log_b x} = x$.
- Change of base: $\log_b M = \dfrac{\ln M}{\ln b}$.

### Solving equations

- If both sides can be written with the **same base**, set the exponents equal.
- Otherwise **isolate the exponential**, take $\ln$ of both sides, and use the power rule to bring the variable down.
- For a logarithmic equation, **combine logs** into one, rewrite in exponential form, solve, and then **check every answer** in the original equation, since logarithms of zero or negative numbers are undefined.

## Worked examples

### Example 1: Evaluating logarithms exactly

1. $\log_2 32$: $2^5 = 32$, so the value is $5$.
2. $\log_3 \tfrac{1}{9}$: $3^{-2} = \tfrac{1}{9}$, so the value is $-2$.
3. $\log 0.001$: $10^{-3} = 0.001$, so the value is $-3$.
4. $\ln e^4 = 4$ by the inverse property.

### Example 2: Exponential equations

(a) Solve $3^{x + 1} = 27^{x - 1}$.

1. Rewrite $27$ as $3^3$: $3^{x + 1} = 3^{3(x - 1)} = 3^{3x - 3}$.
2. Equal bases mean equal exponents: $x + 1 = 3x - 3$, so $x = 2$.
3. Check: $3^3 = 27$ and $27^1 = 27$.

(b) Solve $5 \cdot 2^x = 35$.

1. Isolate the exponential: $2^x = 7$.
2. Take $\ln$ of both sides: $x \ln 2 = \ln 7$.
3. $x = \dfrac{\ln 7}{\ln 2} \approx \dfrac{1.9459}{0.6931} \approx 2.807$.
4. Check: $2^{2.807} \approx 7.00$, and $5 \cdot 7 = 35$.

### Example 3: A logarithmic equation with an extraneous solution

Solve $\log_2 x + \log_2(x - 2) = 3$.

1. Product rule: $\log_2[x(x - 2)] = 3$.
2. Exponential form: $x(x - 2) = 2^3 = 8$.
3. Rearrange and factor: $x^2 - 2x - 8 = 0$, so $(x - 4)(x + 2) = 0$ and $x = 4$ or $x = -2$.
4. Check: $x = -2$ would require $\log_2(-2)$, which is undefined, so it is rejected. For $x = 4$: $\log_2 4 + \log_2 2 = 2 + 1 = 3$.

The only solution is $x = 4$.

### Example 4: Compound interest

An illustrative deposit of \$1,000 earns 5% annual interest for 10 years.

1. Compounded monthly: $A = 1000\left(1 + \tfrac{0.05}{12}\right)^{120} \approx 1000(1.647009) \approx \$1{,}647.01$.
2. Compounded continuously: $A = 1000e^{0.05 \cdot 10} = 1000e^{0.5} \approx \$1{,}648.72$.

More frequent compounding helps, but only slightly; continuous compounding is the upper limit.

### Example 5: Half-life

An illustrative substance has a half-life of 10 hours. How long until 20% of a sample remains?

1. Model: $A = A_0\left(\tfrac{1}{2}\right)^{t/10}$. Set $A = 0.2A_0$: $0.2 = \left(\tfrac{1}{2}\right)^{t/10}$.
2. Take $\ln$: $\ln 0.2 = \tfrac{t}{10}\ln 0.5$.
3. Solve: $t = \dfrac{10 \ln 0.2}{\ln 0.5} \approx \dfrac{10(-1.6094)}{-0.6931} \approx 23.2$ hours.
4. Reasonableness: after 20 hours (two half-lives) 25% remains, so 20% should take a little longer, which matches.

## Common misconceptions and boundary cases

- **Splitting the log of a sum.** $\log(M + N)$ is **not** $\log M + \log N$. The product rule applies to $\log(MN)$ only. For example, $\log(10 + 10) = \log 20 \approx 1.301$, while $\log 10 + \log 10 = 2$.
- **Taking logs of nonpositive numbers.** $\log_b 0$ and $\log_b(-5)$ are undefined in the real numbers. That is why candidate answers must be checked, as in Example 3.
- **Confusing $x^2$ with $2^x$.** In a power function the variable is the base; in an exponential function it is the exponent. For large $x$, $2^x$ eventually exceeds any power of $x$.
- **Dividing logs incorrectly.** $\dfrac{\ln 7}{\ln 2}$ is not $\ln \tfrac{7}{2}$ and not $\ln 5$; compute each logarithm separately and then divide.
- **Using the percentage as the base.** A 4% growth rate gives base $1.04$, not $0.04$ or $4$.

## Practice

1. Evaluate exactly: $\log_4 64$, $\log_5 1$, $\log_{1/2} 8$, and $\ln \tfrac{1}{e^2}$.
2. Expand $\ln\left(\dfrac{x^3 y}{z^2}\right)$ for positive $x$, $y$, $z$.
3. Condense $2\log x - \log(x + 1) + \log 5$ into a single logarithm.
4. Solve $4^{2x - 1} = 8^x$.
5. Solve $e^{0.3t} = 12$ to three decimal places.
6. Solve $\log_3(x + 1) + \log_3(x - 1) = 1$.
7. An illustrative town of 2,500 people grows 4% per year. Write a model and find when the population doubles.
8. Use the change-of-base rule to evaluate $\log_7 50$ to four decimal places.

<details>
<summary>Answer key and self-check</summary>

1. $3$; $0$; $-3$ (since $\left(\tfrac{1}{2}\right)^{-3} = 8$); $-2$.
2. $3\ln x + \ln y - 2\ln z$.
3. $\log\left(\dfrac{5x^2}{x + 1}\right)$.
4. $2^{2(2x - 1)} = 2^{3x}$, so $4x - 2 = 3x$ and $x = 2$. Check: $4^3 = 64 = 8^2$.
5. $0.3t = \ln 12$, so $t = \dfrac{\ln 12}{0.3} \approx \dfrac{2.4849}{0.3} \approx 8.283$.
6. $\log_3[(x + 1)(x - 1)] = 1$, so $x^2 - 1 = 3$ and $x = \pm 2$. Reject $x = -2$ (it gives $\log_3(-1)$). Solution $x = 2$; check $\log_3 3 + \log_3 1 = 1 + 0 = 1$.
7. $P(t) = 2500(1.04)^t$. Doubling: $1.04^t = 2$, so $t = \dfrac{\ln 2}{\ln 1.04} \approx 17.7$ years.
8. $\dfrac{\ln 50}{\ln 7} \approx \dfrac{3.9120}{1.9459} \approx 2.0104$. Check: $7^{2.0104} \approx 50$.

Self-check method: substitute each solution back into the original equation, and confirm any logarithm you wrote has a positive argument.

</details>

## Where this fits

This lesson follows [16.2 - Rational Functions](/162-rational-functions) in the [Algebra II & Pre-Calculus course](/subject/algebra-ii-and-pre-calculus). Exponential models reappear as solutions of differential equations in the lesson on [first-order separable and exact ODEs](/31-first-order-odes-separable-exact), and geometric sequences in [16.7 - Sequences, Series & the Binomial Theorem](/167-sequences-series-the-binomial-theorem) are exponential functions restricted to whole-number inputs. The next lesson is [16.4 - Trigonometry — The Unit Circle](/164-trigonometry-the-unit-circle).

## Sources

- OpenStax, *Precalculus 2e*, [4.1 Exponential Functions](https://openstax.org/books/precalculus-2e/pages/4-1-exponential-functions)
- OpenStax, *Precalculus 2e*, [4.3 Logarithmic Functions](https://openstax.org/books/precalculus-2e/pages/4-3-logarithmic-functions)
- OpenStax, *Precalculus 2e*, [4.5 Logarithmic Properties](https://openstax.org/books/precalculus-2e/pages/4-5-logarithmic-properties)
- OpenStax, *Precalculus 2e*, [4.6 Exponential and Logarithmic Equations](https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations)
- OpenStax, *Precalculus 2e*, [4.7 Exponential and Logarithmic Models](https://openstax.org/books/precalculus-2e/pages/4-7-exponential-and-logarithmic-models)

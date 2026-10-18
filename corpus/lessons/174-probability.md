---
title: "17.4 - Probability"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.4"
type: chapter
objectives:
  - "Apply the complement, addition, and multiplication rules, and distinguish mutually exclusive events from independent events"
  - "Compute joint, marginal, and conditional probabilities from a two-way table and test two events for independence"
  - "Use a tree diagram, the law of total probability, and Bayes' theorem to reverse a conditional probability"
  - "Explain the law of large numbers and estimate a probability by simulation"
open_source: true
---

# 17.4 - Probability

Probability is the mathematics of random behavior: individual outcomes are unpredictable, but the long-run pattern of many repetitions is regular. This lesson formalizes the rules introduced in Pre-Algebra, adds conditional probability and independence, and shows how Bayes' theorem reverses a conditional probability, a step that is easy to get wrong without a systematic method.

## Prerequisites

You should be comfortable with sample spaces, equally likely outcomes, and $P(A) = \tfrac{\text{favorable outcomes}}{\text{total outcomes}}$ from [13.8 - Probability Intro](/138-probability-intro), and with fraction, decimal, and percent conversions. The two-way tables in this lesson count two categorical variables at once; categorical variables were introduced in [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable).

## Learning objectives

By the end of this lesson you should be able to:

1. Use the complement, general addition, and general multiplication rules correctly, and explain why mutually exclusive events with positive probabilities cannot be independent.
2. Read joint, marginal, and conditional probabilities from a two-way table and check independence numerically.
3. Build a tree diagram and apply the law of total probability and Bayes' theorem.
4. Describe what the law of large numbers does and does not promise.

## Core ideas

### Basic rules

For any event $A$ in a sample space $S$: $0 \le P(A) \le 1$ and $P(S) = 1$.

- **Complement rule:** $P(\text{not } A) = 1 - P(A)$. This is often the fastest route to "at least one" probabilities.
- **General addition rule:** $P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$. Subtracting the overlap avoids counting it twice. If $A$ and $B$ are **mutually exclusive** (disjoint, they cannot both happen), $P(A \text{ and } B) = 0$ and the rule reduces to $P(A) + P(B)$.

### Conditional probability and independence

The probability of $A$ given that $B$ has occurred is

$$P(A \mid B) = \frac{P(A \text{ and } B)}{P(B)}, \qquad P(B) > 0.$$

Conditioning shrinks the sample space to the outcomes in $B$. Rearranging gives the **general multiplication rule**: $P(A \text{ and } B) = P(B) \cdot P(A \mid B)$.

Events $A$ and $B$ are **independent** if knowing one occurred does not change the probability of the other: $P(A \mid B) = P(A)$, which is equivalent to $P(A \text{ and } B) = P(A) \cdot P(B)$. Independence is a numerical property to check, not something to assume because events "seem unrelated".

### Total probability and Bayes' theorem

If the events $B_1, B_2, \ldots$ split the sample space into non-overlapping pieces, the **law of total probability** says $P(A) = \sum P(B_i) \cdot P(A \mid B_i)$. **Bayes' theorem** combines this with the definition of conditional probability:

$$P(B_1 \mid A) = \frac{P(B_1) \cdot P(A \mid B_1)}{\sum P(B_i) \cdot P(A \mid B_i)}.$$

On a tree diagram, this is "the branch you care about divided by all branches that end in $A$".

### The law of large numbers and simulation

The **law of large numbers** says that as a random process is repeated many times, the proportion of times an event occurs gets closer and closer to its probability. It is a statement about long-run proportions. It does not say that short-run results "balance out", and it does not change the probability of the next trial. A **simulation** uses random numbers to imitate a chance process many times and estimates a probability by the relative frequency of the event.

## Worked examples

### Example 1: Two-way table

An illustrative survey of $200$ students records whether each plays a school sport ($S$) and whether each has a part-time job ($J$):

| | Job | No job | Total |
|---|---|---|---|
| Sport | 30 | 50 | 80 |
| No sport | 40 | 80 | 120 |
| Total | 70 | 130 | 200 |

1. Marginal probabilities: $P(S) = \tfrac{80}{200} = 0.40$ and $P(J) = \tfrac{70}{200} = 0.35$.
2. Joint probability: $P(S \text{ and } J) = \tfrac{30}{200} = 0.15$.
3. Addition rule: $P(S \text{ or } J) = 0.40 + 0.35 - 0.15 = 0.60$. Check by counting: $30 + 50 + 40 = 120$ students, and $\tfrac{120}{200} = 0.60$.
4. Conditional probabilities: $P(J \mid S) = \tfrac{30}{80} = 0.375$, while $P(S \mid J) = \tfrac{30}{70} \approx 0.429$. The order matters.
5. Independence check: $P(J \mid S) = 0.375 \ne 0.35 = P(J)$; equivalently $P(S) \cdot P(J) = 0.14 \ne 0.15$. In this sample, the events are not independent: athletes are slightly more likely to have a job.

### Example 2: "At least one" and drawing without replacement

1. Roll a fair die $4$ times. The rolls are independent, so $P(\text{no six}) = \left(\tfrac{5}{6}\right)^4 = \tfrac{625}{1296}$, and $P(\text{at least one six}) = 1 - \tfrac{625}{1296} = \tfrac{671}{1296} \approx 0.518$.
2. Draw two cards from a standard $52$-card deck without replacement. The draws are dependent, so use the general multiplication rule: $P(\text{both aces}) = \tfrac{4}{52} \cdot \tfrac{3}{51} = \tfrac{12}{2652} = \tfrac{1}{221} \approx 0.0045$.

### Example 3: Bayes' theorem for a screening test

The numbers in this example are illustrative, not data for any real test. Suppose $2\%$ of a population has a condition. A screening test is positive for $95\%$ of people who have the condition and also, falsely, for $5\%$ of people who do not. If a randomly chosen person tests positive, what is the probability they have the condition?

1. Tree branches: $P(\text{has it and } +) = 0.02 \cdot 0.95 = 0.019$; $P(\text{does not and } +) = 0.98 \cdot 0.05 = 0.049$.
2. Total probability: $P(+) = 0.019 + 0.049 = 0.068$.
3. Bayes: $P(\text{has it} \mid +) = \tfrac{0.019}{0.068} \approx 0.279$.
4. Count check with $10{,}000$ people: $200$ have the condition and $190$ of them test positive; $9800$ do not and $490$ of them test positive. Of the $680$ positives, $\tfrac{190}{680} \approx 27.9\%$ have the condition.

Even with an accurate-sounding test, most positives are false positives here because the condition is rare. $P(+ \mid \text{has it}) = 0.95$ and $P(\text{has it} \mid +) \approx 0.28$ answer different questions.

## Common misconceptions and boundary cases

- **Confusing $P(A \mid B)$ with $P(B \mid A)$.** Example 3 shows they can differ greatly. Always ask which group is the denominator.
- **Treating "mutually exclusive" as "independent".** If $P(A) > 0$ and $P(B) > 0$ and the events are disjoint, then knowing $A$ happened makes $P(B \mid A) = 0$, so they are dependent.
- **Adding probabilities that overlap.** $P(\text{heart or face card}) = \tfrac{13}{52} + \tfrac{12}{52} - \tfrac{3}{52} = \tfrac{22}{52}$, not $\tfrac{25}{52}$.
- **The gambler's fallacy.** After five tails in a row, a fair coin's next toss is still heads with probability $0.5$; the law of large numbers works by swamping early results with many later ones, not by correcting them.
- **Multiplying dependent probabilities as if independent.** Without replacement, the second draw's probabilities change; use $P(B \mid A)$ for the second factor.

## Practice

1. Events $A$ and $B$ are independent with $P(A) = 0.5$ and $P(B) = 0.3$. Find $P(A \text{ and } B)$ and $P(A \text{ or } B)$.
2. Using the table in Example 1, find $P(\text{no job} \mid \text{no sport})$ and $P(\text{job} \mid \text{no sport})$.
3. Toss a fair coin three times. Find $P(\text{three heads})$ and $P(\text{at least one tail})$.
4. Illustratively, $40\%$ of a school's students ride the bus and $60\%$ are driven. A bus rider is late $20\%$ of the time; a driven student is late $5\%$ of the time. Find $P(\text{late})$ and $P(\text{bus} \mid \text{late})$.
5. Can two events with $P(A) = 0.4$, $P(B) = 0.5$, and $P(A \text{ and } B) = 0$ be independent? Explain.
6. A friend says, "A spinner landed on red four times in a row, so blue is due." Respond using the law of large numbers.
7. Describe a simulation using a random digit generator to estimate the probability that a family of four children (assume boys and girls equally likely and independent) has at least one girl. What should the estimate be close to?

<details>
<summary>Answer key and self-check</summary>

1. $P(A \text{ and } B) = 0.5 \cdot 0.3 = 0.15$; $P(A \text{ or } B) = 0.5 + 0.3 - 0.15 = 0.65$.
2. $\tfrac{80}{120} = \tfrac{2}{3} \approx 0.667$ and $\tfrac{40}{120} = \tfrac{1}{3} \approx 0.333$. They sum to $1$, as conditional probabilities on the same condition must.
3. $\left(\tfrac{1}{2}\right)^3 = \tfrac{1}{8} = 0.125$; $1 - \tfrac{1}{8} = \tfrac{7}{8} = 0.875$.
4. $P(\text{late}) = 0.4(0.2) + 0.6(0.05) = 0.08 + 0.03 = 0.11$. $P(\text{bus} \mid \text{late}) = \tfrac{0.08}{0.11} \approx 0.727$.
5. No. Independence would require $P(A \text{ and } B) = 0.4 \cdot 0.5 = 0.2$, but it is $0$; the events are mutually exclusive and therefore dependent.
6. If the spins are independent, the probability of blue on the next spin is unchanged. The law of large numbers describes the long-run proportion over many spins; it does not create short-run corrections.
7. Let even digits represent a girl and odd digits a boy. Generate $4$ digits per trial, record whether any is even, repeat many times (say $1000$), and compute the proportion of trials with at least one girl. It should be close to $1 - \left(\tfrac{1}{2}\right)^4 = \tfrac{15}{16} = 0.9375$.

Self-check method: probabilities must stay between $0$ and $1$; the probabilities of all branches in a tree must sum to $1$; and for any table, recompute an "or" probability by direct counting to confirm the addition rule.

</details>

## Where this fits

This lesson follows [17.3 - Sampling & Experimental Design](/173-sampling-experimental-design) in the [Statistics & Probability course](/subject/statistics-and-probability) and extends [13.8 - Probability Intro](/138-probability-intro). Next, [17.5 - Discrete Random Variables](/175-discrete-random-variables) assigns numbers to random outcomes and uses the multiplication rule to build the binomial distribution.

## Sources

- OpenStax, *Introductory Statistics 2e*, [3.1 Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology)
- OpenStax, *Introductory Statistics 2e*, [3.2 Independent and Mutually Exclusive Events](https://openstax.org/books/introductory-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
- OpenStax, *Introductory Statistics 2e*, [3.3 Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics-2e/pages/3-3-two-basic-rules-of-probability)
- OpenStax, *Introductory Statistics 2e*, [3.4 Contingency Tables](https://openstax.org/books/introductory-statistics-2e/pages/3-4-contingency-tables)
- OpenStax, *Introductory Statistics 2e*, [3.5 Tree and Venn Diagrams](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams)

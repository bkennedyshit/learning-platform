---
title: "13.8 - Probability Intro"
subject: "Pre-Algebra"
catalog: k12
audience_tier: 9-12
chapter: "13.8"
type: chapter
objectives:
  - "List sample spaces and compute theoretical probabilities of equally likely outcomes, including complements"
  - "Compute experimental probability from trial data and explain how it relates to theoretical probability"
  - "Count outcomes with tree diagrams and the fundamental counting principle"
  - "Compute probabilities of compound events for independent events and for dependent events drawn without replacement"
open_source: true
---

# 13.8 - Probability Intro

**Probability** measures how likely an event is, on a scale from $0$ (impossible) to $1$ (certain). A forecast of a $30\%$ chance of rain, the fairness of a game, and the reliability of a test all rest on the same small set of ideas: listing what can happen, counting the outcomes you care about, and combining events correctly. This lesson introduces theoretical and experimental probability, counting methods, and compound events.

## Prerequisites

You need fractions, decimals, and percents from [13.3 - Fractions, Decimals & Percent](/133-fractions-decimals-percent), since probabilities are written in all three forms. Relative frequency from [13.7 - Statistics & Data](/137-statistics-data) connects directly to experimental probability, and multiplying fractions is used for compound events.

## Learning objectives

By the end of this lesson you should be able to:

1. Write the sample space of a simple experiment and compute $P(A)$ and $P(\text{not } A)$ when outcomes are equally likely.
2. Compute an experimental probability from trial results and explain why it may differ from the theoretical value.
3. Count outcomes with a tree diagram or the fundamental counting principle.
4. Find $P(A \text{ and } B)$ for independent events and for dependent events such as drawing without replacement.

## Core ideas

### Vocabulary

- An **experiment** is an action with uncertain results, such as rolling a die.
- An **outcome** is one possible result. The **sample space** $S$ is the set of all outcomes. For one die, $S = \{1, 2, 3, 4, 5, 6\}$.
- An **event** is a set of outcomes, such as "roll an even number" $= \{2, 4, 6\}$.

### Theoretical probability

When all outcomes are **equally likely**,
$$P(A) = \frac{\text{number of outcomes in } A}{\text{number of outcomes in } S}.$$
Every probability satisfies $0 \le P(A) \le 1$, and the probabilities of all outcomes in the sample space add to $1$.

The **complement** of $A$, written "not $A$", contains every outcome not in $A$. Because $A$ and not $A$ together make up the whole sample space,
$$P(\text{not } A) = 1 - P(A).$$
The complement is often the easier route for "at least one" questions.

### Experimental probability

The **experimental probability** (relative frequency) of an event is
$$\frac{\text{number of times the event occurred}}{\text{number of trials}}.$$
Results from a small number of trials can differ noticeably from the theoretical probability. As the number of trials grows, the relative frequency tends to settle close to the theoretical probability; this is the idea behind using data to estimate probabilities when no theoretical model exists, as with a thrown thumbtack.

A **simulation** uses a random device to model a situation. For example, to model an event with probability $0.3$, a random digit $0$ through $9$ could count as a "success" when it is $0$, $1$, or $2$.

### Counting outcomes

A **tree diagram** lists outcomes stage by stage: each branch is one choice, and each path from start to end is one outcome. The **fundamental counting principle** summarizes the tree: if one choice can be made in $m$ ways and a second in $n$ ways regardless of the first, then together they can be made in $m \cdot n$ ways. This extends to any number of stages.

### Compound events

- Events are **independent** if the outcome of one does not change the probability of the other, such as a coin flip and a die roll. Then
$$P(A \text{ and } B) = P(A) \cdot P(B).$$
- Events are **dependent** if one changes the probability of the other. Drawing two marbles **without replacement** is dependent: the first draw changes what is left. Then multiply $P(A)$ by the probability of $B$ **given that $A$ already happened**.

Drawing **with replacement** (putting the first item back) makes the draws independent.

## Worked examples

### Example 1: One die

1. $P(\text{even}) = \tfrac{3}{6} = \tfrac{1}{2}$.
2. $P(\text{greater than } 4) = P(\{5, 6\}) = \tfrac{2}{6} = \tfrac{1}{3}$.
3. $P(\text{not } 6) = 1 - \tfrac{1}{6} = \tfrac{5}{6}$.
4. $P(7) = \tfrac{0}{6} = 0$: an impossible event.

### Example 2: Experimental versus theoretical

In an illustrative class activity, a spinner with one quarter of its area colored red is spun $50$ times and lands on red $18$ times.

1. Experimental probability: $\tfrac{18}{50} = 0.36$.
2. Theoretical probability: $\tfrac{1}{4} = 0.25$.
3. A gap like this in only $50$ spins does not prove the spinner is unfair. More trials would give a more reliable estimate; a persistent large gap over many trials would be evidence that the spinner is not fair.

### Example 3: Counting principle

1. With $3$ shirts, $4$ pairs of pants, and $2$ pairs of shoes, there are $3 \cdot 4 \cdot 2 = 24$ outfits.
2. A code of $3$ letters followed by $2$ digits, with repetition allowed, has $26^3 \cdot 10^2 = 17{,}576 \cdot 100 = 1{,}757{,}600$ possibilities.

### Example 4: Tree diagrams and independent events

1. Flip two coins. The tree gives $S = \{HH, HT, TH, TT\}$. $P(\text{exactly one head}) = \tfrac{2}{4} = \tfrac{1}{2}$. Note that $HT$ and $TH$ are different outcomes.
2. Flip a coin and roll a die: $2 \cdot 6 = 12$ equally likely outcomes. $P(\text{heads and } 5) = \tfrac{1}{2} \cdot \tfrac{1}{6} = \tfrac{1}{12}$, matching the single outcome $(H, 5)$ out of $12$.

### Example 5: With and without replacement

A bag holds $5$ red and $3$ blue marbles. Two are drawn.

1. **Without replacement:** $P(\text{red first}) = \tfrac{5}{8}$. Now $4$ red remain among $7$, so $P(\text{red second given red first}) = \tfrac{4}{7}$. $P(\text{both red}) = \tfrac{5}{8} \cdot \tfrac{4}{7} = \tfrac{20}{56} = \tfrac{5}{14}$.
2. **With replacement:** the bag is unchanged, so $P(\text{both red}) = \tfrac{5}{8} \cdot \tfrac{5}{8} = \tfrac{25}{64}$.
3. The probabilities differ: $\tfrac{5}{14} \approx 0.357$ and $\tfrac{25}{64} \approx 0.391$.

## Common misconceptions and boundary cases

- **The gambler's fallacy.** After five heads in a row, a fair coin still has $P(\text{heads}) = \tfrac{1}{2}$ on the next flip. Independent trials have no memory.
- **Assuming outcomes are equally likely.** The sums of two dice range from $2$ to $12$, but they are not equally likely: a sum of $7$ occurs in $6$ of the $36$ outcomes, a sum of $2$ in only $1$.
- **"It either happens or it doesn't, so it's 50-50."** Two possible results do not mean two equally likely results.
- **Adding for "and".** For independent events, $P(A \text{ and } B)$ is a product. Adding $\tfrac{1}{2} + \tfrac{1}{6}$ for "heads and $5$" gives $\tfrac{2}{3}$, far too large.
- **Treating dependent draws as independent.** Without replacement, the denominator and possibly the numerator change after the first draw.
- **Impossible values.** A probability can never be negative or greater than $1$. A result such as $\tfrac{9}{8}$ signals a counting error.

## Practice

1. A bag holds $4$ green, $6$ yellow, and $2$ white tiles. Find $P(\text{yellow})$ and $P(\text{not white})$.
2. Two fair dice are rolled. Find $P(\text{sum is } 8)$.
3. A lunch menu offers $4$ sandwiches, $3$ sides, and $5$ drinks. How many meals have one of each?
4. A fair coin is flipped $3$ times. Find $P(\text{exactly } 2 \text{ heads})$ and $P(\text{at least one head})$.
5. A bag holds $3$ red and $2$ blue marbles. Two are drawn. Find $P(\text{both blue})$ without replacement and with replacement.
6. In an illustrative experiment, a thumbtack is tossed $80$ times and lands point-up $52$ times. Find the experimental probability of point-up, and predict the number of point-up landings in $400$ tosses.
7. A spinner has $4$ equal sections colored differently. It is spun twice. Find $P(\text{same color both times})$.
8. With two fair dice, which is more likely: a sum of $7$ or a sum of $11$? Give both probabilities.

<details>
<summary>Answer key and self-check</summary>

1. There are $12$ tiles. $P(\text{yellow}) = \tfrac{6}{12} = \tfrac{1}{2}$; $P(\text{not white}) = 1 - \tfrac{2}{12} = \tfrac{10}{12} = \tfrac{5}{6}$.
2. Outcomes with sum $8$: $(2,6), (3,5), (4,4), (5,3), (6,2)$. $P = \tfrac{5}{36}$.
3. $4 \cdot 3 \cdot 5 = 60$ meals.
4. There are $2^3 = 8$ outcomes. Exactly two heads: $HHT, HTH, THH$, so $\tfrac{3}{8}$. At least one head: $1 - P(TTT) = 1 - \tfrac{1}{8} = \tfrac{7}{8}$.
5. Without replacement: $\tfrac{2}{5} \cdot \tfrac{1}{4} = \tfrac{2}{20} = \tfrac{1}{10}$. With replacement: $\tfrac{2}{5} \cdot \tfrac{2}{5} = \tfrac{4}{25}$.
6. $\tfrac{52}{80} = 0.65$. Prediction: $0.65 \cdot 400 = 260$ point-up landings (an estimate, not a guarantee).
7. $16$ equally likely ordered pairs, $4$ of which match: $\tfrac{4}{16} = \tfrac{1}{4}$. Equivalently, whatever the first spin, the second matches with probability $\tfrac{1}{4}$.
8. Sum $7$: $\tfrac{6}{36} = \tfrac{1}{6}$. Sum $11$: $(5,6), (6,5)$, so $\tfrac{2}{36} = \tfrac{1}{18}$. A sum of $7$ is three times as likely.

Self-check method: every answer must be between $0$ and $1$. For a full sample space, check that the probabilities of all outcomes add to $1$; for two dice, list the $6 \times 6$ grid and count directly when in doubt.

</details>

## Where this fits

This is the final lesson in the [Pre-Algebra course](/subject/pre-algebra), following [13.7 - Statistics & Data](/137-statistics-data). The next step is [14.1 - The Language of Algebra](/141-the-language-of-algebra), the first lesson of the [Algebra I course](/subject/algebra-i). Probability is developed further in [17.4 - Probability](/174-probability) in the [Statistics & Probability course](/subject/statistics-and-probability), which adds conditional probability, independence, and Bayes' theorem.

## Sources

- OpenStax, *Prealgebra 2e*, [5.5 Averages and Probability](https://openstax.org/books/prealgebra-2e/pages/5-5-averages-and-probability)
- OpenStax, *Introductory Statistics 2e*, [3.1 Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology)
- OpenStax, *Introductory Statistics 2e*, [3.2 Independent and Mutually Exclusive Events](https://openstax.org/books/introductory-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
- OpenStax, *Introductory Statistics 2e*, [3.5 Tree and Venn Diagrams](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams)
- OpenStax, *Contemporary Mathematics*, [7.1 The Multiplication Rule for Counting](https://openstax.org/books/contemporary-mathematics/pages/7-1-the-multiplication-rule-for-counting)

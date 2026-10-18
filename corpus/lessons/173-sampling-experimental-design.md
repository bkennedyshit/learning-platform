---
title: "17.3 - Sampling & Experimental Design"
subject: "Statistics & Probability"
catalog: k12
audience_tier: 9-12
chapter: "17.3"
type: chapter
objectives:
  - "Distinguish a census from a sample and a population parameter from a sample statistic"
  - "Describe and carry out simple random, stratified, cluster, and systematic sampling, and identify undercoverage, nonresponse, voluntary-response, and wording bias"
  - "Distinguish observational studies from experiments and design a randomized experiment with control, random assignment, replication, and blinding"
  - "State the scope of inference a study supports: generalization to a population, cause and effect, both, or neither"
open_source: true
---

# 17.3 - Sampling & Experimental Design

Every statistical conclusion is only as good as the process that produced the data. A huge data set gathered badly can be worse than a small one gathered well, because bias does not shrink as the sample grows. This lesson covers how to choose a sample, how bias enters, how experiments differ from observational studies, and which conclusions each design supports.

## Prerequisites

You should know what a variable, a distribution, and a proportion are from [17.1 - Exploring Data (1-Variable)](/171-exploring-data-1-variable), and why association does not establish causation from [17.2 - Exploring Data (2-Variable)](/172-exploring-data-2-variable). Basic probability language ("equally likely", "at random") from [13.8 - Probability Intro](/138-probability-intro) is also used.

## Learning objectives

By the end of this lesson you should be able to:

1. Identify the population, sample, parameter, and statistic in a study description.
2. Carry out and compare four probability sampling methods and name the bias in a flawed survey.
3. Decide whether a study is an observational study or an experiment, and design a completely randomized or block experiment.
4. State what a study's design allows you to conclude.

## Core ideas

### Populations, samples, parameters, statistics

The **population** is the entire group you want information about; a **census** measures every member. A **sample** is the part of the population actually measured. A **parameter** is a number describing the population (such as the true proportion $p$ or mean $\mu$); a **statistic** is a number computed from a sample (such as $\hat{p}$ or $\bar{x}$) and is used to estimate the parameter. Different random samples give different statistics; this **sampling variability** is studied in 17.6.

### Probability sampling methods

- **Simple random sample (SRS):** every group of $n$ individuals is equally likely to be chosen. Label the population, then use a random number generator or table and skip repeats.
- **Stratified random sample:** split the population into groups of similar individuals (**strata**), such as grade levels, and take an SRS within each. It guarantees each stratum is represented and usually gives more precise estimates when strata differ.
- **Cluster sample:** split the population into groups that each resemble the population (**clusters**), such as homerooms, randomly choose some clusters, and measure everyone in them. It is cheaper but usually less precise.
- **Systematic sample:** choose a random starting point among the first $k$ individuals in a list, then take every $k$th individual after it.

A **convenience sample** (whoever is easy to reach) is not a probability sample and usually cannot be trusted to represent the population.

### Sources of bias

**Bias** is a systematic tendency to over- or underestimate a parameter.

- **Undercoverage:** some groups are left out of the sampling frame (for example, a phone survey that misses people without phones).
- **Nonresponse:** chosen individuals cannot be contacted or refuse, and they differ from those who respond.
- **Voluntary response:** people choose themselves, so those with strong opinions are overrepresented.
- **Response and wording bias:** leading questions, social pressure, or confusing wording push answers in one direction.

### Observational studies and experiments

In an **observational study**, researchers measure variables without influencing them. In an **experiment**, researchers deliberately impose **treatments** on **experimental units** (called subjects when they are people) and measure a **response**. A **confounding variable** is related to the explanatory variable and also affects the response, so their effects cannot be separated. Observational studies are vulnerable to confounding; well-designed experiments control it.

Principles of experimental design:

- **Control:** keep other variables the same for all groups, and include a comparison group (a **control group**, which may get a **placebo** or the current standard treatment).
- **Random assignment:** use chance to assign units to treatments, so that groups are roughly balanced on variables you did not measure.
- **Replication:** use enough units in each group that chance differences between groups are small.
- **Blinding:** in a **single-blind** experiment the subjects do not know which treatment they received; in a **double-blind** experiment, neither the subjects nor the people measuring the response know.

In a **randomized block design**, units are first grouped by a variable expected to affect the response (for example, prior experience), and treatments are randomly assigned within each block. A **matched pairs** design is the special case in which each block has two similar units, or one unit receives both treatments in random order.

### Scope of inference

| | Random assignment | No random assignment |
|---|---|---|
| **Random sample** | Cause and effect; generalize to the population | Association only; generalize to the population |
| **No random sample** | Cause and effect for the units in the study only | Association only, for the units studied |

Random *sampling* supports generalizing to a population. Random *assignment* supports cause-and-effect conclusions.

## Worked examples

### Example 1: Stratified and systematic samples

An illustrative school has $1000$ students: $400$ ninth graders, $300$ tenth graders, $200$ eleventh graders, and $100$ twelfth graders. The student council wants a sample of $50$.

1. **Stratified, proportional allocation:** the sample is $\tfrac{50}{1000} = 5\%$ of the school, so take $5\%$ of each grade: $0.05 \cdot 400 = 20$, $0.05 \cdot 300 = 15$, $0.05 \cdot 200 = 10$, $0.05 \cdot 100 = 5$. Check: $20 + 15 + 10 + 5 = 50$. Within each grade, number the students and use a random number generator to pick that many distinct labels.
2. **Systematic:** with an alphabetical list of all $1000$ students, $k = \tfrac{1000}{50} = 20$. Choose a random start from $1$ to $20$, say $7$, and take students $7, 27, 47, \ldots, 987$, which is $50$ students.
3. **Comparison:** the stratified sample is guaranteed to include each grade in proportion; a systematic sample from an alphabetical list is close to an SRS unless the list has a repeating pattern that lines up with $k$.

### Example 2: Diagnosing a biased survey

An illustrative news website posts the question "Don't you agree the city's wasteful new stadium should be stopped?" and $5000$ visitors click a response; $80\%$ say yes.

- **Voluntary response:** visitors chose to answer, so people with strong feelings are overrepresented.
- **Undercoverage:** only visitors to that website could respond.
- **Wording bias:** "Don't you agree" and "wasteful" push respondents toward yes.

The $80\%$ is a statistic for the respondents only. A large number of responses does not fix any of these biases. A better design would take a random sample of city residents and ask a neutral question, such as "Do you support or oppose the planned stadium?"

### Example 3: Designing an experiment

Question (illustrative): does a new flashcard method improve vocabulary quiz scores compared with the usual study guide? Forty volunteer students are available.

1. **Treatments:** flashcard method vs. study guide. **Response:** score on the same vocabulary quiz.
2. **Random assignment:** label students $01$–$40$; use a random number generator to select $20$ distinct labels for flashcards; the other $20$ use the study guide.
3. **Control:** same word list, same study time, same quiz, same grading key, administered on the same day.
4. **Blinding:** the grader does not know which group each quiz came from. (The students cannot be blind to their own study method, so this is not double-blind.)
5. **Block option:** if half the students are native speakers of the quiz language, form two blocks and randomize treatments within each block so that language background is balanced.
6. **Scope:** random assignment supports a cause-and-effect conclusion, but because the students are volunteers rather than a random sample, the conclusion applies to students like these.

## Common misconceptions and boundary cases

- **Random sampling and random assignment are the same.** Random sampling decides *who is in the study*; random assignment decides *who gets which treatment*. They answer different questions.
- **A bigger sample removes bias.** A larger sample reduces sampling variability, but a biased method stays biased at any size.
- **Strata and clusters are interchangeable.** Strata should be internally similar (all members alike) and different from each other; clusters should each look like a small version of the whole population.
- **A control group means "no treatment".** A control group is any comparison group, often a placebo or the current standard, because receiving any treatment can change outcomes (the placebo effect).
- **Observational studies are useless.** They are often the only ethical or practical option, such as studying the effects of smoking, and they can reveal associations worth testing. They just cannot rule out confounding on their own.

## Practice

1. A researcher measures the resting heart rate of $60$ randomly chosen adults in a town and finds a mean of $71$ beats per minute. Identify the population, sample, parameter, and statistic.
2. An illustrative town has $5000$ households in $100$ city blocks. Describe a cluster sample and a stratified sample of households.
3. Name the main bias: (a) a survey of gym members about how often town residents exercise; (b) a mailed survey where only $15\%$ of chosen households reply.
4. An illustrative study compares students who chose to take music lessons with students who did not and finds the music group has higher grades. Is this an observational study or an experiment? Can it show that music lessons cause higher grades?
5. Describe how to randomly assign $30$ tomato plants to three fertilizers with equal group sizes.
6. A company has $2400$ employees on a list and wants a systematic sample of $80$. What is $k$, and which employees would be chosen with a random start of $13$?
7. Explain why a double-blind design matters in a study of a new pain-relief pill.

<details>
<summary>Answer key and self-check</summary>

1. Population: all adults in the town. Sample: the $60$ adults measured. Parameter: the mean resting heart rate $\mu$ of all adults in the town (unknown). Statistic: $\bar{x} = 71$.
2. Cluster: randomly select some city blocks (for example $5$) and survey every household on them. Stratified: if blocks fall into neighborhoods that differ (for example by housing type), take an SRS of households within each neighborhood.
3. (a) Undercoverage: gym members are not representative of all residents and probably exercise more. (b) Nonresponse: the $85\%$ who did not reply may differ from the responders.
4. Observational: students chose their own group. No; a confounding variable such as family resources or study habits could explain the difference.
5. Label the plants $01$–$30$. Use a random number generator to choose $10$ distinct labels for fertilizer A, then $10$ of the remaining labels for fertilizer B; the last $10$ get fertilizer C. Keep water, light, and pot size the same.
6. $k = \tfrac{2400}{80} = 30$. Employees $13, 43, 73, \ldots$; the last is $13 + 79 \cdot 30 = 2383$.
7. Patients who know they got the real pill may report less pain because they expect relief, and an evaluator who knows the assignment may judge outcomes differently. Blinding both removes these effects as an explanation for a difference between groups.

Self-check method: for each design, ask two questions. Was there random selection from a population? Was there random assignment to treatments? Your scope-of-inference conclusion should match the table above.

</details>

## Where this fits

This lesson follows [17.2 - Exploring Data (2-Variable)](/172-exploring-data-2-variable) in the [Statistics & Probability course](/subject/statistics-and-probability). Next, [17.4 - Probability](/174-probability) develops the rules of chance that make random sampling and random assignment analyzable. The ideas of parameter, statistic, and sampling variability return in [17.6 - Normal Distribution & Sampling Distributions](/176-normal-distribution-sampling-distributions).

## Sources

- OpenStax, *Introductory Statistics 2e*, [1.2 Data, Sampling, and Variation in Data and Sampling](https://openstax.org/books/introductory-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling) (sampling methods and sources of bias)
- OpenStax, *Introductory Statistics 2e*, [1.4 Experimental Design and Ethics](https://openstax.org/books/introductory-statistics-2e/pages/1-4-experimental-design-and-ethics) (treatments, control, placebos, blinding, lurking variables)
- OpenStax, *Introductory Statistics 2e*, [10.4 Matched or Paired Samples](https://openstax.org/books/introductory-statistics-2e/pages/10-4-matched-or-paired-samples)

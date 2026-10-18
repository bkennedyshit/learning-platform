---
title: "14.2 - Linear Equations"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.2"
type: chapter
objectives:
  - "Solve one-step, two-step, and multi-step linear equations using inverse operations"
  - "Solve equations with variables on both sides and with fractions or decimals"
  - "Recognize equations with no solution and equations true for all real numbers"
  - "Solve a literal equation for a specified variable"
  - "Model and solve consecutive-integer and distance-rate-time problems"
open_source: true
---

# 14.2 - Linear Equations

Solving a linear equation means finding every value of the variable that makes the equation true. This lesson builds one general strategy that handles one-step, multi-step, fractional, and literal equations, and it shows how to recognize equations with no solution or infinitely many solutions.

In one variable, a linear equation can always be rewritten in the form $ax + b = c$ with $a \neq 0$; the variable appears only to the first power and is never multiplied by itself.

## Prerequisites

You need the vocabulary and properties from [14.1 - The Language of Algebra](/141-the-language-of-algebra): distributing, combining like terms, and evaluating an expression for a given value. Comfort with integer and fraction arithmetic is assumed.

## Learning objectives

By the end of this lesson you should be able to:

1. Solve linear equations of any length by applying inverse operations to both sides.
2. Clear fractions by multiplying by the least common denominator (LCD).
3. Decide whether an equation has exactly one solution, no solution, or infinitely many solutions.
4. Rearrange a formula to isolate a requested variable.
5. Translate a word problem into an equation, solve it, and check the answer in the original situation.

## Core ideas

### Equivalent equations

The **addition and subtraction properties of equality** say that adding or subtracting the same number on both sides produces an equation with the same solutions. The **multiplication and division properties of equality** say the same for multiplying or dividing both sides by the same nonzero number. Every step in solving is one of these moves, chosen to undo what has been done to the variable.

### A general strategy

1. Simplify each side: distribute and combine like terms.
2. Clear fractions or decimals if they make the work messy, by multiplying every term by the LCD (or by a power of ten).
3. Collect variable terms on one side and constants on the other with addition or subtraction.
4. Divide by the coefficient of the variable.
5. Check by substituting the solution into the **original** equation.

### Three possible outcomes

After simplifying, a linear equation reaches one of three forms:

- $x = k$ for a single number $k$: exactly one solution.
- A false statement such as $0 = 4$: a **contradiction**, with no solution.
- A true statement such as $0 = 0$: an **identity**, true for every real number.

## Worked examples

### Example 1: Variables on both sides

Solve $3(x - 4) + 2 = 5x - 18$.

1. Distribute: $3x - 12 + 2 = 5x - 18$.
2. Combine like terms on the left: $3x - 10 = 5x - 18$.
3. Subtract $3x$ from both sides so the variable term stays positive: $-10 = 2x - 18$.
4. Add $18$ to both sides: $8 = 2x$.
5. Divide by $2$: $x = 4$.

Check in the original: left side $3(4 - 4) + 2 = 2$; right side $5(4) - 18 = 2$. Both sides equal $2$, so $x = 4$ is correct.

### Example 2: Clearing fractions

Solve $\dfrac{x}{3} + \dfrac{x - 1}{2} = 4$.

1. The LCD of $3$ and $2$ is $6$. Multiply **every** term, including the $4$, by $6$: $2x + 3(x - 1) = 24$.
2. Distribute: $2x + 3x - 3 = 24$.
3. Combine: $5x - 3 = 24$, so $5x = 27$.
4. Divide: $x = \tfrac{27}{5} = 5.4$.

Check: $\tfrac{5.4}{3} = 1.8$ and $\tfrac{4.4}{2} = 2.2$, and $1.8 + 2.2 = 4$.

### Example 3: Special cases

Compare $2(x + 3) = 2x + 6$ with $2(x + 3) = 2x + 5$.

- First equation: distributing gives $2x + 6 = 2x + 6$; subtracting $2x$ leaves $6 = 6$, which is always true. Every real number is a solution.
- Second equation: $2x + 6 = 2x + 5$ becomes $6 = 5$, which is never true. There is no solution.

When the variable disappears, do not write $x = 0$. Read the remaining statement and report "all real numbers" or "no solution."

### Example 4: A literal equation

Solve $2x + 3y = 12$ for $y$.

1. Treat $x$ as if it were a known number. Subtract $2x$: $3y = 12 - 2x$.
2. Divide every term by $3$: $y = 4 - \tfrac{2}{3}x$.

The same method rearranges the triangle-area formula $A = \tfrac{1}{2}bh$ into $h = \tfrac{2A}{b}$ (for $b \neq 0$), which is useful when the area and base are known.

### Example 5: Distance, rate, and time

Two cyclists leave the same point at the same time riding in opposite directions, one at 12 mi/h and the other at 15 mi/h. After how many hours are they 54 miles apart? (Illustrative numbers.)

1. Let $t$ be the time in hours. Distance equals rate times time, so the riders cover $12t$ and $15t$ miles.
2. Because they move apart, the distances add: $12t + 15t = 54$.
3. Solve: $27t = 54$, so $t = 2$.

Check the units and the situation: in 2 hours they travel 24 and 30 miles, which total 54 miles.

## Common misconceptions and boundary cases

- **Only multiplying some terms by the LCD.** In Example 2, writing $2x + 3(x - 1) = 4$ forgets to multiply the right side. Every term on both sides must be multiplied.
- **Losing a negative when dividing.** From $-3x = 12$ the solution is $x = -4$. Dividing by $-3$ applies to both the coefficient and the sign.
- **Reporting $x = 0$ for an identity or contradiction.** If the variable cancels, the answer depends on whether the remaining statement is true or false, as in Example 3.
- **Checking in a rewritten step.** If a step contained an error, a later step can "check" perfectly while still being wrong. Always substitute into the original equation.
- **Dividing by an expression that could be zero.** In a literal equation like $ax = b$, writing $x = \tfrac{b}{a}$ is valid only when $a \neq 0$. State the restriction.

## Practice

1. Solve $7 - 2x = 15$.
2. Solve $4(2x - 1) = 3(x + 7)$ and check your answer.
3. Solve $\dfrac{2x}{5} - 1 = \dfrac{x}{2}$.
4. Solve the perimeter formula $P = 2l + 2w$ for $w$.
5. Classify each equation as one solution, no solution, or all real numbers: (a) $3(x - 2) + x = 4x - 6$; (b) $5x + 1 = 5(x + 1)$.
6. The sum of three consecutive integers is $87$. Find the integers.
7. Finish the equation from Lesson 14.1: solve $2n - 5 = 17$.

<details>
<summary>Answer key and self-check</summary>

1. $-2x = 8$, so $x = -4$. Check: $7 - 2(-4) = 15$.
2. $8x - 4 = 3x + 21$, so $5x = 25$ and $x = 5$. Check: $4(9) = 36$ and $3(12) = 36$.
3. Multiply by $10$: $4x - 10 = 5x$, so $x = -10$. Check: $\tfrac{-20}{5} - 1 = -5$ and $\tfrac{-10}{2} = -5$.
4. $2w = P - 2l$, so $w = \dfrac{P - 2l}{2}$, which can also be written $w = \tfrac{P}{2} - l$.
5. (a) $4x - 6 = 4x - 6$ is an identity: all real numbers. (b) $5x + 1 = 5x + 5$ leads to $1 = 5$: no solution.
6. Let the integers be $n$, $n + 1$, $n + 2$. Then $3n + 3 = 87$, so $n = 28$. The integers are $28, 29, 30$.
7. $2n = 22$, so $n = 11$.

Self-check method: substitute each answer into the original equation (or the original word problem) and confirm both sides are equal.

</details>

## Where this fits

Linear equations are the core tool of the [Algebra I course](/subject/algebra-i). Next, [14.3 - Linear Inequalities](/143-linear-inequalities) uses the same steps with one important change involving negative numbers, and [14.6 - Systems of Equations](/146-systems-of-equations) solves two linear equations at once.

## Sources

- OpenStax, *Elementary Algebra 2e*, [2.3 Solve Equations with Variables and Constants on Both Sides](https://openstax.org/books/elementary-algebra-2e/pages/2-3-solve-equations-with-variables-and-constants-on-both-sides)
- OpenStax, *Elementary Algebra 2e*, [2.4 Use a General Strategy to Solve Linear Equations](https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations)
- OpenStax, *Elementary Algebra 2e*, [2.6 Solve a Formula for a Specific Variable](https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable)

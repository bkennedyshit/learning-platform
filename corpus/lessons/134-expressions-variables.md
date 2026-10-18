---
title: "13.4 - Expressions & Variables"
subject: "Pre-Algebra"
catalog: k12
audience_tier: 9-12
chapter: "13.4"
type: chapter
objectives:
  - "Identify terms, coefficients, constants, and like terms in an algebraic expression"
  - "Evaluate expressions by substitution using the order of operations, including negative values"
  - "Simplify expressions with the distributive property and by combining like terms, and factor out a greatest common factor"
  - "Translate verbal descriptions into algebraic expressions and test two expressions for equivalence"
open_source: true
---

# 13.4 - Expressions & Variables

A **variable** is a letter that stands for a number. Variables let you write one rule that works for every case: instead of computing the cost of 1, 2, or 50 items separately, you write one expression for "four dollars per item" and use it for any number of items. This lesson introduces the vocabulary of algebraic expressions and the three skills used constantly in algebra: evaluating, simplifying, and translating.

## Prerequisites

You need integer arithmetic from [13.2 - The Number System](/132-the-number-system) and fraction arithmetic from [13.3 - Fractions, Decimals & Percent](/133-fractions-decimals-percent). You should know the order of operations: parentheses (grouping symbols), exponents, multiplication and division from left to right, then addition and subtraction from left to right.

## Learning objectives

By the end of this lesson you should be able to:

1. Name the terms, coefficients, and constant of an expression and pick out like terms.
2. Evaluate an expression for given values, using parentheses when substituting negatives.
3. Simplify an expression by distributing and combining like terms, and reverse the process by factoring out the greatest common factor.
4. Write an expression from a verbal description and check whether two expressions are equivalent.

## Core ideas

### Vocabulary

In the expression $5x^2 - 3x + 7$:

- the **terms** are $5x^2$, $-3x$, and $7$ (terms are separated by addition; subtraction is addition of a negative term);
- the **coefficients** are $5$ and $-3$, the numbers multiplying the variables;
- the **constant** is $7$, a term with no variable.

**Like terms** have the same variables raised to the same powers. $4x$ and $-9x$ are like terms; $4x$ and $4x^2$ are not, and neither are $3xy$ and $3x$.

An **expression** has no equals sign. You can evaluate or simplify an expression, but you cannot "solve" it; solving belongs to equations, which are the subject of [13.5 - Equations & Inequalities](/135-equations-inequalities).

### Evaluating

To **evaluate** an expression, replace each variable with its value, in parentheses, and follow the order of operations. Parentheses matter most with negatives: if $x = -3$, then $x^2 = (-3)^2 = 9$.

### Distributive property and like terms

The **distributive property** says
$$a(b + c) = ab + ac \quad \text{and} \quad a(b - c) = ab - ac.$$
A rectangle of width $a$ split into two pieces of lengths $b$ and $c$ shows why: the whole area $a(b + c)$ equals the sum of the two pieces. A negative or subtracted factor distributes to every term: $-(x - 4) = -x + 4$.

**Combining like terms** is the distributive property in reverse: $7x + 2x = (7 + 2)x = 9x$. Unlike terms cannot be combined.

### Factoring out the greatest common factor

**Factoring** rewrites a sum as a product. To factor out the greatest common factor (GCF), find the largest number and highest power of each variable that divide every term, write it in front, and divide each term by it:
$$12x + 18 = 6(2x + 3).$$
Distributing the result must return the original expression.

### Translating words

| Words | Expression |
|---|---|
| the sum of a number and $8$ | $n + 8$ |
| $5$ less than a number | $n - 5$ |
| the product of $7$ and a number | $7n$ |
| the quotient of a number and $4$ | $\tfrac{n}{4}$ |
| three times the sum of a number and $8$ | $3(n + 8)$ |

"Less than" and "subtracted from" reverse the order in which the words appear: "$5$ less than $n$" is $n - 5$.

### Equivalent expressions

Two expressions are **equivalent** if they give the same value for every value of the variable. Simplifying both to the same form proves equivalence. Testing a few values can reveal non-equivalence but cannot by itself prove equivalence.

## Worked examples

### Example 1: Evaluating with negatives

Evaluate $3x^2 - 2xy + 5$ when $x = -2$ and $y = 3$.

1. Substitute with parentheses: $3(-2)^2 - 2(-2)(3) + 5$.
2. Exponent first: $(-2)^2 = 4$, so $3(4) = 12$.
3. Product: $-2(-2)(3) = 12$.
4. Sum: $12 + 12 + 5 = 29$.

### Example 2: Distribute, then combine

Simplify $4(2x - 3) - 3(x - 5)$.

1. Distribute $4$: $8x - 12$.
2. Distribute $-3$ to both terms: $-3x + 15$.
3. Combine: $8x - 3x - 12 + 15 = 5x + 3$.
4. Check at $x = 1$: original $4(-1) - 3(-4) = -4 + 12 = 8$; simplified $5(1) + 3 = 8$.

### Example 3: Several kinds of like terms

Simplify $7a + 3b - 2a + 5 - b + a^2$.

1. Group like terms: $a^2 + (7a - 2a) + (3b - b) + 5$.
2. Combine: $a^2 + 5a + 2b + 5$. The $a^2$ term stays separate because its exponent differs.

### Example 4: Factoring out the GCF

1. $12x + 18$: the GCF of $12$ and $18$ is $6$. Result: $6(2x + 3)$.
2. $15y^2 - 10y$: the GCF is $5y$. Result: $5y(3y - 2)$.
3. Check by distributing: $5y \cdot 3y - 5y \cdot 2 = 15y^2 - 10y$.

### Example 5: Translating and modeling

1. "Five less than twice a number": $2n - 5$.
2. "The quotient of a number and $4$, increased by $7$": $\tfrac{n}{4} + 7$.
3. An illustrative taxi fare is \$3 plus \$2.50 per mile. The cost for $m$ miles is $3 + 2.5m$ dollars. For $m = 8$: $3 + 2.5(8) = 3 + 20 = 23$ dollars.

## Common misconceptions and boundary cases

- **Combining unlike terms.** $3x + 2$ is already simplified; it is not $5x$. Likewise $x + x^2 \ne 2x^2$, but $x \cdot x = x^2$.
- **Distributing to only the first term.** $3(x + 4) = 3x + 12$, not $3x + 4$.
- **Dropping the sign when distributing a negative.** $-3(x - 5) = -3x + 15$. The second term changes sign too.
- **Reversing "less than."** "$5$ less than a number" is $n - 5$, not $5 - n$.
- **Substituting without parentheses.** If $x = -4$, then $x^2 = 16$, but typing $-4^2$ gives $-16$.
- **Letters as labels.** In $6c$, the variable $c$ stands for a number (such as a count or cost), not for the word "cats". Writing what each variable measures, including units, prevents setup errors.

## Practice

1. Evaluate $5a - b^2$ when $a = 3$ and $b = -4$.
2. Simplify $6m - 2(3m - 7) + m$.
3. Simplify $-(4y - 9) + 2(y + 1)$.
4. Factor $24k - 36$ completely.
5. Factor $8x^2 + 20x$ completely.
6. Translate "the product of $7$ and a number, decreased by $3$" and "$7$ times the difference of a number and $3$". Are they the same?
7. A rectangle has length $2w + 3$ and width $w$. Write and simplify an expression for its perimeter, then evaluate it for $w = 4$.
8. Show whether $3(x + 2) + x$ and $4x + 6$ are equivalent.

<details>
<summary>Answer key and self-check</summary>

1. $5(3) - (-4)^2 = 15 - 16 = -1$.
2. $6m - 6m + 14 + m = m + 14$.
3. $-4y + 9 + 2y + 2 = -2y + 11$.
4. The GCF is $12$: $12(2k - 3)$. (Factoring out only $6$ gives $6(4k - 6)$, which is not complete.)
5. The GCF is $4x$: $4x(2x + 5)$.
6. $7n - 3$ and $7(n - 3) = 7n - 21$. They are different; at $n = 5$ they give $32$ and $14$.
7. $2(2w + 3) + 2w = 4w + 6 + 2w = 6w + 6$. For $w = 4$: $30$. Check: length $11$, width $4$, perimeter $2(11) + 2(4) = 30$.
8. $3x + 6 + x = 4x + 6$, so they are equivalent for every $x$. Spot check: at $x = 2$, both equal $14$.

Self-check method: after simplifying or factoring, substitute a convenient value (not $0$ or $1$, which can hide errors) into both the original and your answer. Different values mean there is a mistake.

</details>

## Where this fits

This lesson follows [13.3 - Fractions, Decimals & Percent](/133-fractions-decimals-percent) in the [Pre-Algebra course](/subject/pre-algebra). Next, [13.5 - Equations & Inequalities](/135-equations-inequalities) sets two expressions equal (or unequal) and asks which values make the statement true. In Algebra I, expressions are formalized in [14.1 - The Language of Algebra](/141-the-language-of-algebra), and factoring out a GCF is the first step of every method in [14.8 - Factoring & Quadratics](/148-factoring-quadratics).

## Sources

- OpenStax, *Prealgebra 2e*, [2.1 Use the Language of Algebra](https://openstax.org/books/prealgebra-2e/pages/2-1-use-the-language-of-algebra)
- OpenStax, *Prealgebra 2e*, [2.2 Evaluate, Simplify, and Translate Expressions](https://openstax.org/books/prealgebra-2e/pages/2-2-evaluate-simplify-and-translate-expressions)
- OpenStax, *Prealgebra 2e*, [7.3 Distributive Property](https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property)
- OpenStax, *Prealgebra 2e*, [10.6 Introduction to Factoring Polynomials](https://openstax.org/books/prealgebra-2e/pages/10-6-introduction-to-factoring-polynomials)

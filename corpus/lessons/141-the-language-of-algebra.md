---
title: "14.1 - The Language of Algebra"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.1"
type: chapter
objectives:
  - "Identify variables, constants, coefficients, and terms in an algebraic expression"
  - "Evaluate expressions with negative values using the order of operations"
  - "Simplify expressions with the distributive property and like terms"
  - "Translate verbal phrases into expressions and equations"
  - "Classify real numbers as natural, whole, integer, rational, or irrational"
open_source: true
---

# 14.1 - The Language of Algebra

Algebra is a language for describing quantities that can change. This lesson teaches its vocabulary, how to evaluate and simplify expressions, how to translate words into symbols, and how the real numbers are organized.

## Prerequisites

You should be comfortable with arithmetic on integers and fractions, including negative numbers, and with the order of operations on plain numbers. If adding $-7 + 3$ or multiplying $-\tfrac{2}{3} \cdot 6$ still feels uncertain, review the [Pre-Algebra subject](/subject/pre-algebra) first.

## Learning objectives

By the end of this lesson you should be able to:

1. Point to the variables, constants, coefficients, and terms in an expression such as $4x^2 - 7x + 3$.
2. Evaluate an expression for given values, including negative values, without sign errors.
3. Simplify an expression by distributing and combining like terms.
4. Translate a phrase such as "five less than twice a number" into symbols.
5. Place a given number in every set of the real number system it belongs to.

## Core ideas

### Vocabulary

A **variable** is a letter that stands for a number that can change or is not yet known. A **constant** is a number whose value is fixed, such as $3$ or $-\tfrac{1}{2}$. An **algebraic expression** combines variables and constants with operations, for example $4x^2 - 7x + 3$. The expression is built from **terms** that are added: here the terms are $4x^2$, $-7x$, and $3$. The number multiplying a variable is its **coefficient**, so the coefficient of $x$ in this expression is $-7$, not $7$, because the subtraction sign belongs to the term.

An expression has no equals sign and can only be simplified or evaluated. An **equation** states that two expressions are equal, such as $4x - 7 = 9$, and can be solved. Keeping that distinction clear prevents a very common error: "solving" an expression that was only meant to be simplified.

**Like terms** have exactly the same variable part. $5x$ and $-2x$ are like terms; $5x$ and $5x^2$ are not, because $x$ and $x^2$ are different quantities.

### Order of operations

When an expression is evaluated, operations are done in this order: grouping symbols (parentheses, brackets, fraction bars, absolute value bars); exponents; multiplication and division from left to right; addition and subtraction from left to right. The acronym PEMDAS is a reminder, but multiplication does not come before division, and addition does not come before subtraction. Each pair is handled left to right.

### Properties of real numbers

These properties are the legal moves for rewriting expressions:

- **Commutative:** $a + b = b + a$ and $ab = ba$. Order does not matter for addition or multiplication.
- **Associative:** $(a + b) + c = a + (b + c)$ and $(ab)c = a(bc)$. Grouping does not matter for addition or multiplication.
- **Distributive:** $a(b + c) = ab + ac$. Multiplication distributes over addition.
- **Identity:** $a + 0 = a$ and $a \cdot 1 = a$.
- **Inverse:** $a + (-a) = 0$, and $a \cdot \tfrac{1}{a} = 1$ when $a \neq 0$.

Subtraction and division are neither commutative nor associative: $8 - 3 \neq 3 - 8$.

### The real number system

- **Natural numbers:** $1, 2, 3, \ldots$
- **Whole numbers:** $0, 1, 2, 3, \ldots$
- **Integers:** $\ldots, -2, -1, 0, 1, 2, \ldots$
- **Rational numbers:** any number that can be written as $\tfrac{p}{q}$ with integers $p$ and $q$ and $q \neq 0$. Their decimals either terminate ($0.25$) or repeat ($0.\overline{3}$).
- **Irrational numbers:** real numbers that cannot be written as a fraction of integers. Their decimals never terminate or repeat. Examples are $\sqrt{2}$ and $\pi$.

Every rational and every irrational number is a **real number**. Each set in the first four bullets sits inside the next one, so $4$ is natural, whole, an integer, rational, and real all at once.

## Worked examples

### Example 1: Evaluate with a negative value

Evaluate $3x^2 - 2(x - 4)$ when $x = -2$.

1. Substitute using parentheses so the sign stays attached: $3(-2)^2 - 2((-2) - 4)$.
2. Grouping first: $(-2) - 4 = -6$.
3. Exponent next: $(-2)^2 = 4$, so the first term is $3 \cdot 4 = 12$.
4. Multiply: $-2 \cdot (-6) = 12$.
5. Add: $12 + 12 = 24$.

Self-check: the two pieces are each positive here because squaring removes the sign and a negative times a negative is positive. The value is $24$.

### Example 2: Distribute and combine like terms

Simplify $4(2a - 3) - (5a - 7)$.

1. Distribute the $4$: $8a - 12$.
2. The minus sign in front of the second parentheses means multiply each term by $-1$: $-5a + 7$.
3. Rewrite: $8a - 12 - 5a + 7$.
4. Combine like terms: $8a - 5a = 3a$ and $-12 + 7 = -5$.

Result: $3a - 5$. A quick check is to test a value. With $a = 1$ the original gives $4(-1) - (-2) = -2$, and $3(1) - 5 = -2$. The two forms agree.

### Example 3: Translate words into an equation

"Five less than twice a number is 17."

1. Name the unknown: let $n$ be the number.
2. "Twice a number" is $2n$.
3. "Five less than" something means start with that something and subtract five: $2n - 5$. It is **not** $5 - 2n$.
4. "Is" becomes the equals sign: $2n - 5 = 17$.

This is an equation, so it can be solved later (Lesson 14.2 does exactly that, giving $n = 11$).

## Common misconceptions and boundary cases

- **Squaring a negative input.** For $x = -3$, the expression $-x^2$ equals $-(-3)^2 = -9$, not $9$. The exponent applies to $x$ before the leading negative. Always substitute inside parentheses.
- **Combining unlike terms.** $3x + 2$ cannot be simplified to $5x$, and $x + x^2$ is not $2x^3$. Only terms with identical variable parts combine.
- **Distributing a subtraction.** $-(5a - 7)$ is $-5a + 7$. Changing only the first sign is one of the most frequent errors in all of Algebra I.
- **Reversed phrases.** "Less than" and "subtracted from" reverse the order in which the words appear: "3 less than $y$" is $y - 3$.
- **Rational approximations.** $\tfrac{22}{7}$ and $3.14$ are rational approximations of $\pi$; neither is equal to $\pi$. Also, $\sqrt{9} = 3$ is rational even though it is written with a root sign.

## Practice

1. Evaluate $2a^2 - 3ab + b$ when $a = -1$ and $b = 4$.
2. Simplify $5(x - 2) - 3(2x + 1)$.
3. Write an expression for "the quotient of a number and 4, increased by 6."
4. Evaluate $-x^2 + 4x$ when $x = -3$.
5. Name the property used in each statement: (a) $3(x + 5) = 3x + 15$; (b) $x + 0 = x$; (c) $(2 \cdot x) \cdot y = 2 \cdot (x \cdot y)$.
6. List every set each number belongs to: $-7$, $0.25$, $\sqrt{16}$, $\sqrt{5}$, $\tfrac{2}{3}$.

<details>
<summary>Answer key and self-check</summary>

1. $2(-1)^2 - 3(-1)(4) + 4 = 2 + 12 + 4 = 18$.
2. $5x - 10 - 6x - 3 = -x - 13$. Check with $x = 0$: original gives $-10 - 3 = -13$.
3. $\tfrac{n}{4} + 6$.
4. $-(-3)^2 + 4(-3) = -9 - 12 = -21$.
5. (a) distributive; (b) additive identity; (c) associative property of multiplication.
6. $-7$: integer, rational, real. $0.25$: rational, real. $\sqrt{16} = 4$: natural, whole, integer, rational, real. $\sqrt{5}$: irrational, real. $\tfrac{2}{3}$: rational, real.

Self-check method: for any simplification, substitute one or two easy values (such as $0$ and $1$) into both the original and your answer. If the values differ, there is an error.

</details>

## Where this fits

This lesson supplies the vocabulary used throughout the [Algebra I course](/subject/algebra-i). The next lesson, [14.2 - Linear Equations](/142-linear-equations), uses these properties to solve equations step by step, and [14.7 - Exponents & Polynomials](/147-exponents-polynomials) extends the idea of like terms to polynomials.

## Sources

- OpenStax, *Elementary Algebra 2e*, [1.2 Use the Language of Algebra](https://openstax.org/books/elementary-algebra-2e/pages/1-2-use-the-language-of-algebra)
- OpenStax, *Elementary Algebra 2e*, [1.8 The Real Numbers](https://openstax.org/books/elementary-algebra-2e/pages/1-8-the-real-numbers)
- OpenStax, *Elementary Algebra 2e*, [1.9 Properties of Real Numbers](https://openstax.org/books/elementary-algebra-2e/pages/1-9-properties-of-real-numbers)

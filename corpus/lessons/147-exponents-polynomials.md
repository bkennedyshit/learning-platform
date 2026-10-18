---
title: "14.7 - Exponents & Polynomials"
subject: "Algebra I"
catalog: k12
audience_tier: 9-12
chapter: "14.7"
type: chapter
objectives:
  - "Simplify expressions using the product, quotient, power, zero, and negative exponent rules"
  - "Convert between standard and scientific notation and compute with scientific notation"
  - "Classify a polynomial by degree and number of terms and identify its leading coefficient"
  - "Add, subtract, and multiply polynomials, including the special products"
open_source: true
---

# 14.7 - Exponents & Polynomials

Exponents are shorthand for repeated multiplication, and polynomials are sums of terms built from a variable raised to whole-number powers. This lesson develops the exponent rules, scientific notation, polynomial vocabulary, and the operations of adding, subtracting, and multiplying polynomials.

## Prerequisites

You should be fluent with combining like terms and the distributive property from [14.1 - The Language of Algebra](/141-the-language-of-algebra), and with multiplying and dividing signed numbers.

## Learning objectives

By the end of this lesson you should be able to:

1. Apply the exponent rules to simplify expressions so that each base appears once and no exponent is negative.
2. Write very large and very small numbers in scientific notation and multiply or divide them.
3. State the degree, leading coefficient, and type (monomial, binomial, trinomial) of a polynomial.
4. Add, subtract, and multiply polynomials and verify the result by substitution.
5. Use the special-product patterns for squares of binomials and for sums times differences.

## Core ideas

### Exponent rules

For real numbers $a, b$ and integers $m, n$ (with $a \neq 0$ wherever $a$ is in a denominator or raised to a zero or negative power):

- **Product rule:** $a^m \cdot a^n = a^{m+n}$
- **Quotient rule:** $\dfrac{a^m}{a^n} = a^{m-n}$
- **Power rule:** $(a^m)^n = a^{mn}$
- **Power of a product:** $(ab)^n = a^n b^n$
- **Zero exponent:** $a^0 = 1$
- **Negative exponent:** $a^{-n} = \dfrac{1}{a^n}$

The zero rule follows from the quotient rule: $\tfrac{a^3}{a^3}$ equals $1$ and also equals $a^{3-3} = a^0$. The expression $0^0$ is not assigned a value in this course.

### Scientific notation

A number is in scientific notation when it is written as $a \times 10^n$ with $1 \le |a| \lt 10$ and $n$ an integer. A positive exponent indicates a large number; a negative exponent indicates a number between $-1$ and $1$. For example, $52{,}000 = 5.2 \times 10^4$ and $0.000052 = 5.2 \times 10^{-5}$.

### Polynomial vocabulary

A **monomial** is a number, a variable, or a product of numbers and variables with whole-number exponents, such as $-4x^3$. A **polynomial** is a monomial or a sum of monomials. A polynomial with two terms is a **binomial** and one with three is a **trinomial**. The **degree** of a one-variable polynomial is its highest exponent, and the **leading coefficient** is the coefficient of that term when the polynomial is written in descending order. $\tfrac{3}{x}$ and $\sqrt{x}$ are not polynomial terms, because their exponents are not whole numbers.

### Special products

$$(a + b)^2 = a^2 + 2ab + b^2 \qquad (a - b)^2 = a^2 - 2ab + b^2 \qquad (a + b)(a - b) = a^2 - b^2$$

## Worked examples

### Example 1: Combining several rules

Simplify $(3x^2y)^3 \cdot (2xy^{-2})$.

1. Power of a product: $(3x^2y)^3 = 3^3 x^{6} y^{3} = 27x^6y^3$.
2. Multiply coefficients: $27 \cdot 2 = 54$.
3. Product rule for $x$: $x^6 \cdot x^1 = x^7$. For $y$: $y^3 \cdot y^{-2} = y^1$.

Result: $54x^7y$.

### Example 2: A quotient with negative exponents

Simplify $\dfrac{12a^5b^{-1}}{4a^{-2}b^3}$.

1. Divide coefficients: $12 \div 4 = 3$.
2. Quotient rule for $a$: $a^{5 - (-2)} = a^7$. For $b$: $b^{-1 - 3} = b^{-4}$.
3. Rewrite the negative exponent: $3a^7b^{-4} = \dfrac{3a^7}{b^4}$.

### Example 3: Scientific notation

Compute $(6.0 \times 10^4)(3.0 \times 10^{-7})$.

1. Multiply the decimal parts: $6.0 \times 3.0 = 18$.
2. Add the exponents: $10^{4 + (-7)} = 10^{-3}$.
3. The product $18 \times 10^{-3}$ is not yet in scientific notation because $18 \ge 10$. Rewrite $18 = 1.8 \times 10^1$, giving $1.8 \times 10^{-2}$.

Check in standard form: $60{,}000 \times 0.0000003 = 0.018$, which equals $1.8 \times 10^{-2}$.

### Example 4: Subtracting polynomials

Simplify $(5x^3 - 2x^2 + 7) - (3x^3 + x^2 - 4x + 9)$.

1. Distribute the subtraction to every term in the second polynomial: $5x^3 - 2x^2 + 7 - 3x^3 - x^2 + 4x - 9$.
2. Group like terms: $(5x^3 - 3x^3) + (-2x^2 - x^2) + 4x + (7 - 9)$.
3. Combine: $2x^3 - 3x^2 + 4x - 2$.

This result has degree $3$ and leading coefficient $2$.

### Example 5: Multiplying polynomials

Multiply $(2x - 3)(x^2 + 4x - 5)$.

1. Distribute $2x$: $2x^3 + 8x^2 - 10x$.
2. Distribute $-3$: $-3x^2 - 12x + 15$.
3. Combine like terms: $2x^3 + 5x^2 - 22x + 15$.

Check with $x = 2$: the original gives $(1)(4 + 8 - 5) = 7$, and the result gives $16 + 20 - 44 + 15 = 7$.

A special product is quicker: $(3x + 5)^2 = 9x^2 + 2(3x)(5) + 25 = 9x^2 + 30x + 25$.

## Common misconceptions and boundary cases

- **Squaring a sum term by term.** $(x + 3)^2 \neq x^2 + 9$. Test with $x = 1$: $(1 + 3)^2 = 16$, but $1 + 9 = 10$. The middle term $6x$ is missing; the correct expansion is $x^2 + 6x + 9$.
- **Multiplying exponents in a product.** $2x^3 \cdot 3x^4 = 6x^7$, not $6x^{12}$. Exponents multiply only when a power is raised to a power.
- **Negative exponent means negative number.** $x^{-2} = \tfrac{1}{x^2}$, which is positive for any nonzero $x$. It is not $-x^2$.
- **Sign of a negative base.** $-3^2 = -9$ because the exponent applies only to $3$, while $(-3)^2 = 9$.
- **Forgetting the coefficient inside parentheses.** $(2x)^3 = 8x^3$, but $2x^3$ means only $x$ is cubed.
- **Scientific notation out of range.** $18 \times 10^{-3}$ and $0.5 \times 10^2$ are correct values but not in scientific notation, since the decimal part must be at least $1$ and less than $10$.

## Practice

1. Simplify $(-2a^3b)^2(3ab^4)$.
2. Simplify $\dfrac{15x^{-2}y^5}{5x^3y^{-1}}$ with positive exponents only.
3. Write $0.000052$ in scientific notation, then compute $(5.2 \times 10^{-5})(4 \times 10^8)$.
4. Add $(4x^2 - 3x + 1) + (-6x^2 + 5x - 8)$.
5. Multiply $(x + 4)(3x - 2)$.
6. Expand $(2y - 7)^2$ and $(5m + 2)(5m - 2)$.
7. Evaluate $5^0 + 2^{-3}$.

<details>
<summary>Answer key and self-check</summary>

1. $(4a^6b^2)(3ab^4) = 12a^7b^6$.
2. $3x^{-5}y^{6} = \dfrac{3y^6}{x^5}$.
3. $5.2 \times 10^{-5}$. Product: $20.8 \times 10^{3} = 2.08 \times 10^4$.
4. $-2x^2 + 2x - 7$.
5. $3x^2 - 2x + 12x - 8 = 3x^2 + 10x - 8$. Check with $x = 1$: $5 \cdot 1 = 5$ and $3 + 10 - 8 = 5$.
6. $4y^2 - 28y + 49$; $25m^2 - 4$.
7. $1 + \tfrac{1}{8} = \tfrac{9}{8}$.

Self-check method: substitute a small value such as $x = 1$ or $x = 2$ into the original expression and into your simplified answer. For exponent problems, try $x = 2$ and $y = 1$, avoiding $0$ where it would create division by zero.

</details>

## Where this fits

Polynomials become the main object of study in the second half of the [Algebra I course](/subject/algebra-i). The next lesson, [14.8 - Factoring & Quadratics](/148-factoring-quadratics), reverses the multiplication done here to factor polynomials and solve quadratic equations.

## Sources

- OpenStax, *Elementary Algebra 2e*, [6.1 Add and Subtract Polynomials](https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials)
- OpenStax, *Elementary Algebra 2e*, [6.2 Use Multiplication Properties of Exponents](https://openstax.org/books/elementary-algebra-2e/pages/6-2-use-multiplication-properties-of-exponents)
- OpenStax, *Elementary Algebra 2e*, [6.3 Multiply Polynomials](https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials)
- OpenStax, *Elementary Algebra 2e*, [6.4 Special Products](https://openstax.org/books/elementary-algebra-2e/pages/6-4-special-products)
- OpenStax, *Elementary Algebra 2e*, [6.7 Integer Exponents and Scientific Notation](https://openstax.org/books/elementary-algebra-2e/pages/6-7-integer-exponents-and-scientific-notation)

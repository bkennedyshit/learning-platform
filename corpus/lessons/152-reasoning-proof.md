---
title: "15.2 - Reasoning & Proof"
subject: "Geometry"
catalog: k12
audience_tier: 9-12
chapter: "15.2"
type: chapter
objectives:
  - "Distinguish inductive from deductive reasoning and disprove a conjecture with a counterexample"
  - "Write the converse, inverse, and contrapositive of a conditional and determine each truth value"
  - "Apply the Law of Detachment and the Law of Syllogism and recognize invalid argument forms"
  - "Write two-column proofs using properties of equality, definitions, and postulates, and outline an indirect proof"
open_source: true
---

# 15.2 - Reasoning & Proof

A protractor can show that two angles in one diagram both measure 63 degrees; a proof shows that they must be equal in every diagram that meets the same conditions. This lesson develops the logic that makes that possible: how conjectures are formed and broken, how conditional statements work, which argument forms are valid, and how to lay out a two-column proof in which every step has a stated reason.

## Prerequisites

You need the vocabulary and postulates from [15.1 - Foundations of Geometry](/151-foundations-of-geometry): segment and angle addition, midpoints, linear pairs, and vertical angles. You should also be comfortable solving linear equations step by step, as in [14.2 - Linear Equations](/142-linear-equations), because algebraic proofs justify exactly those steps.

## Learning objectives

By the end of this lesson you should be able to:

1. Explain why examples can support a conjecture but cannot prove it, and produce a counterexample that disproves one.
2. Identify the hypothesis and conclusion of a conditional statement and decide when the conditional is true.
3. Write the converse, inverse, and contrapositive of a conditional and determine their truth values.
4. Use the Law of Detachment and the Law of Syllogism to reach valid conclusions, and spot the "converse error."
5. Write a two-column proof for an algebraic or segment/angle statement, and outline an indirect proof.

## Core ideas

### Inductive and deductive reasoning

**Inductive reasoning** looks at specific cases and generalizes to a **conjecture**. It is how patterns are discovered, but it never guarantees the conjecture. A single **counterexample**, a case where the hypothesis holds and the conclusion fails, proves a conjecture false.

**Deductive reasoning** starts from accepted statements (definitions, postulates, earlier theorems, and given facts) and uses valid logic to reach a conclusion that must be true whenever the starting statements are true.

### Conditional statements

A **conditional** has the form "if $p$, then $q$," written $p \to q$. The part $p$ is the **hypothesis** and $q$ is the **conclusion**. A conditional is false in exactly one situation: $p$ is true and $q$ is false.

| $p$ | $q$ | $p \to q$ |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

From one conditional you can form three related statements:

- **Converse:** $q \to p$.
- **Inverse:** $\lnot p \to \lnot q$.
- **Contrapositive:** $\lnot q \to \lnot p$.

A conditional and its contrapositive always have the same truth value; they are **logically equivalent**. The converse and inverse are equivalent to each other but not to the original. When a conditional and its converse are both true, they combine into a **biconditional**, "$p$ if and only if $q$," written $p \leftrightarrow q$. Good definitions are biconditionals: an angle is right if and only if it measures $90^\circ$.

### Valid argument forms

- **Law of Detachment** (modus ponens): if $p \to q$ is true and $p$ is true, then $q$ is true.
- **Law of Syllogism**: if $p \to q$ and $q \to r$ are true, then $p \to r$ is true.

Two common invalid forms look similar: concluding $p$ from $p \to q$ and $q$ (the **converse error**), and concluding $\lnot q$ from $p \to q$ and $\lnot p$ (the **inverse error**). Concluding $\lnot p$ from $p \to q$ and $\lnot q$ *is* valid; it uses the contrapositive.

### Reasons you may cite

- **Properties of equality:** addition, subtraction, multiplication, and division properties; substitution; distributive property; reflexive ($a = a$), symmetric (if $a = b$ then $b = a$), and transitive (if $a = b$ and $b = c$ then $a = c$) properties.
- **Definitions**, such as midpoint, bisector, complementary, supplementary, and congruent.
- **Postulates and proved theorems**, such as Segment Addition, Angle Addition, the Linear Pair Postulate (a linear pair is supplementary), and the Vertical Angles Theorem.

A **two-column proof** lists statements on the left and reasons on the right, starting from the given information and ending with the statement to be proved. An **indirect proof** assumes the conclusion is false and derives a contradiction with a known fact.

## Worked examples

### Example 1: A pattern that breaks

Conjecture: for every positive integer $n$, $n^2 - n + 41$ is prime.

1. Test cases: $n = 1$ gives $41$, $n = 2$ gives $43$, $n = 3$ gives $47$, $n = 10$ gives $131$. All prime; in fact every value from $n = 1$ through $n = 40$ is prime.
2. Try $n = 41$: $41^2 - 41 + 41 = 41^2 = 1681$, which equals $41 \cdot 41$ and is not prime.
3. One counterexample disproves the conjecture, even after forty supporting cases.

### Example 2: Related conditionals

Statement: "If an angle measures $30^\circ$, then it is acute." (True.)

1. Converse: "If an angle is acute, then it measures $30^\circ$." False; counterexample: a $45^\circ$ angle.
2. Inverse: "If an angle does not measure $30^\circ$, then it is not acute." False; the same $45^\circ$ angle works.
3. Contrapositive: "If an angle is not acute, then it does not measure $30^\circ$." True, matching the original.

### Example 3: Valid and invalid conclusions

Given: (1) If two angles form a linear pair, then they are supplementary. (2) If two angles are supplementary, then their measures add to $180^\circ$. (3) $\angle A$ and $\angle B$ form a linear pair.

1. Syllogism on (1) and (2): if two angles form a linear pair, their measures add to $180^\circ$.
2. Detachment with (3): $m\angle A + m\angle B = 180^\circ$. Valid.
3. Now suppose instead we know only (1) and "$\angle C$ and $\angle D$ are supplementary." Concluding that they form a linear pair is the converse error; two supplementary angles can be far apart.

### Example 4: Algebraic two-column proof

Given $3(x - 2) = 2x + 4$. Prove $x = 10$.

| Statement | Reason |
|---|---|
| 1. $3(x - 2) = 2x + 4$ | Given |
| 2. $3x - 6 = 2x + 4$ | Distributive property |
| 3. $x - 6 = 4$ | Subtraction property of equality ($2x$) |
| 4. $x = 10$ | Addition property of equality ($6$) |

### Example 5: Segment proof

Given points $A$, $B$, $C$, $D$ on a line in that order with $AB = CD$. Prove $AC = BD$.

| Statement | Reason |
|---|---|
| 1. $AB = CD$ | Given |
| 2. $BC = BC$ | Reflexive property |
| 3. $AB + BC = BC + CD$ | Addition property of equality (steps 1, 2) |
| 4. $AB + BC = AC$ and $BC + CD = BD$ | Segment Addition Postulate |
| 5. $AC = BD$ | Substitution (steps 3, 4) |

### Example 6: Indirect proof

Prove: two distinct lines intersect in at most one point.

1. Assume the opposite: distinct lines $\ell$ and $m$ share two different points $P$ and $Q$.
2. Then $\ell$ and $m$ are both lines through $P$ and $Q$.
3. This contradicts the postulate that through two points there is exactly one line.
4. So the assumption is false, and the lines share at most one point.

## Common misconceptions and boundary cases

- **"It worked for every case I tried."** Example 1 shows that many confirming cases are not a proof. Only a deductive argument covers every case.
- **Treating the converse as automatically true.** "If two angles are vertical, they are congruent" is true; its converse is false, since two congruent angles need not share a vertex.
- **Thinking a false hypothesis makes a conditional false.** When $p$ is false the conditional is true regardless of $q$; the statement made no promise about that case.
- **Using what a diagram looks like as a reason.** "It looks perpendicular" is not a reason. A right-angle mark, a given, or a theorem is.
- **Circular reasoning.** A proof cannot use the statement it is proving, or a theorem that depends on it, as one of its reasons.
- **Confusing "if" with "only if."** "$p$ only if $q$" means $p \to q$, not $q \to p$.

## Practice

1. Give a counterexample to the conjecture "The sum of two acute angles is always acute."
2. Write the converse, inverse, and contrapositive of "If two angles are vertical angles, then they are congruent." State whether each is true.
3. What can you conclude? "If a quadrilateral is a square, then it is a rectangle. If a quadrilateral is a rectangle, then it has four right angles. $WXYZ$ is a square."
4. Is this argument valid? "If an angle is right, then it is not obtuse. $\angle A$ is not obtuse. Therefore $\angle A$ is right."
5. Write a two-column proof: given $5x - 7 = 2x + 8$, prove $x = 5$.
6. Is the biconditional "A number is positive if and only if its square is positive" true? If not, which direction fails?
7. Prove the Congruent Supplements Theorem: given that $\angle 1$ and $\angle 2$ are supplementary and $\angle 3$ and $\angle 2$ are supplementary, prove $m\angle 1 = m\angle 3$.

<details>
<summary>Answer key and self-check</summary>

1. $60^\circ + 50^\circ = 110^\circ$, which is obtuse.
2. Converse: "If two angles are congruent, then they are vertical angles." False. Inverse: "If two angles are not vertical angles, then they are not congruent." False. Contrapositive: "If two angles are not congruent, then they are not vertical angles." True.
3. By syllogism, a square has four right angles; by detachment, $WXYZ$ has four right angles.
4. Invalid (converse error). Counterexample: $\angle A = 40^\circ$ is not obtuse and not right.
5. (1) $5x - 7 = 2x + 8$, given. (2) $3x - 7 = 8$, subtraction property. (3) $3x = 15$, addition property. (4) $x = 5$, division property.
6. False. "Positive implies square positive" is true, but "square positive implies positive" fails for $-2$, since $(-2)^2 = 4$.
7. (1) $\angle 1, \angle 2$ supplementary and $\angle 3, \angle 2$ supplementary, given. (2) $m\angle 1 + m\angle 2 = 180$ and $m\angle 3 + m\angle 2 = 180$, definition of supplementary. (3) $m\angle 1 + m\angle 2 = m\angle 3 + m\angle 2$, substitution (or transitive property). (4) $m\angle 1 = m\angle 3$, subtraction property.

Self-check method: for each proof, read only the reasons column and ask whether each reason really licenses the statement beside it; for each conditional, test it with the single T/F row that can make it false.

</details>

## Where this fits

This lesson follows [15.1 - Foundations of Geometry](/151-foundations-of-geometry) in the [Geometry course](/subject/geometry). Next, [15.3 - Parallel & Perpendicular Lines](/153-parallel-perpendicular-lines) uses these proof structures, including converses, to decide when lines are parallel. The same logic is developed symbolically in [APP-11.1 - Propositional Logic](/app-111-propositional-logic) and [APP-11.2 - Predicate Logic & Proof Techniques](/app-112-predicate-logic-proof-techniques).

## Sources

- OpenStax, *Contemporary Mathematics*, [2.1 Statements and Quantifiers](https://openstax.org/books/contemporary-mathematics/pages/2-1-statements-and-quantifiers)
- OpenStax, *Contemporary Mathematics*, [2.4 Truth Tables for the Conditional and Biconditional](https://openstax.org/books/contemporary-mathematics/pages/2-4-truth-tables-for-the-conditional-and-biconditional)
- OpenStax, *Contemporary Mathematics*, [2.5 Equivalent Statements](https://openstax.org/books/contemporary-mathematics/pages/2-5-equivalent-statements)
- OpenStax, *Contemporary Mathematics*, [2.7 Logical Arguments](https://openstax.org/books/contemporary-mathematics/pages/2-7-logical-arguments)

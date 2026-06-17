---
title: "Vector Spaces Subspaces"
subject: "Linear Algebra & Matrix Theory"
catalog: advanced
audience_tier: higher-education
chapter: "2.3"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 2.3 — Vector Spaces & Subspaces

> *"The whole point of the four fundamental subspaces is that they are the right tool for understanding everything that can happen when you apply a matrix to a vector."* — Gilbert Strang, MIT 18.06

Chapter 2.1 introduced vectors; Chapter 2.2 gave us the matrix machine. Now we step back and ask: **what structure does a matrix impose on space?** The answer is encoded in four canonical subspaces — the column space, the null space, the row space, and the left null space — linked by the Rank-Nullity Theorem and the Fundamental Theorem of Linear Algebra. This chapter builds those tools from the abstract definition down to concrete computation.

---

## 🎯 Learning Objectives

1. State the abstract vector space axioms and verify that a given set is (or is not) a vector space.
2. State and apply the three-condition subspace test.
3. Define and compute all four fundamental subspaces of a matrix.
4. Prove the Rank-Nullity Theorem.
5. State the orthogonality relations among the four fundamental subspaces (Fundamental Theorem of Linear Algebra).
6. Compute orthogonal complements and projections onto subspaces.

---

## 🖼️ Visual Anchor — Strang's Four Fundamental Subspaces Diagram

![math-02__2.3-fig1](math-02__2.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 2.3.1 — Abstract Vector Space

A **vector space** over a field $\mathbb{F}$ (we use $\mathbb{F} = \mathbb{R}$) is a set $V$ with operations $+: V \times V \to V$ and $\cdot: \mathbb{R} \times V \to V$ satisfying the 8 axioms VS1–VS8 stated in §2 of Chapter 2.1.

**Key examples beyond $\mathbb{R}^n$:**
- $\mathcal{P}_n$ — polynomials of degree $\leq n$; $\dim \mathcal{P}_n = n+1$.
- $\mathcal{C}([a,b])$ — continuous functions on $[a,b]$; infinite-dimensional.
- $M_{m \times n}(\mathbb{R})$ — $m \times n$ real matrices; $\dim = mn$.
- Solutions to a homogeneous ODE $y'' + py' + qy = 0$ on an interval.

### Definition 2.3.2 — Subspace

A non-empty subset $W \subseteq V$ is a **subspace** of $V$ iff:
1. $\mathbf{0} \in W$,
2. $\mathbf{u}, \mathbf{v} \in W \Rightarrow \mathbf{u} + \mathbf{v} \in W$ (closed under addition),
3. $\mathbf{u} \in W,\, c \in \mathbb{R} \Rightarrow c\mathbf{u} \in W$ (closed under scalar mult.).

**Efficient check.** Conditions 2 and 3 together are equivalent to: $c_1\mathbf{u} + c_2\mathbf{v} \in W$ for all $c_1, c_2 \in \mathbb{R}$ and all $\mathbf{u}, \mathbf{v} \in W$ (closure under linear combinations).


### Definition 2.3.3 — The Four Fundamental Subspaces of a Matrix

For $A \in \mathbb{R}^{m \times n}$ with rank $r$:

| Subspace | Definition | Ambient Space | Dimension |
|---|---|---|---|
| **Column space** $C(A)$ | $\{\,A\mathbf{x} : \mathbf{x} \in \mathbb{R}^n\,\}$ = span of columns | $\mathbb{R}^m$ | $r$ |
| **Null space** $N(A)$ | $\{\,\mathbf{x} : A\mathbf{x} = \mathbf{0}\,\}$ | $\mathbb{R}^n$ | $n - r$ |
| **Row space** $C(A^T)$ | span of rows of $A$ = $C(A^T)$ | $\mathbb{R}^n$ | $r$ |
| **Left null space** $N(A^T)$ | $\{\,\mathbf{y} : A^T\mathbf{y} = \mathbf{0}\,\}$ | $\mathbb{R}^m$ | $m - r$ |

**Why "left" null space?** $A^T \mathbf{y} = \mathbf{0}$ is equivalent to $\mathbf{y}^T A = \mathbf{0}^T$ — $\mathbf{y}^T$ multiplies $A$ from the **left**.

![math-02__2.3-fig2](math-02__2.3-fig2.svg)

### Definition 2.3.4 — Orthogonal Complement

For a subspace $W \subseteq \mathbb{R}^n$, the **orthogonal complement** is:

$$
W^\perp = \{\mathbf{v} \in \mathbb{R}^n : \mathbf{v} \cdot \mathbf{w} = 0 \text{ for all } \mathbf{w} \in W\}.
$$

$W^\perp$ is itself a subspace, $\dim W + \dim W^\perp = n$, and $(W^\perp)^\perp = W$.

![math-02__2.3-fig3](math-02__2.3-fig3.svg)


---

## 📐 2. The Subspace Test

The following three conditions are both necessary and sufficient for $W \neq \emptyset$ to be a subspace. We only need these — we do not need to re-verify all 8 vector space axioms because $W$ inherits them from the ambient space $V$.

**Theorem (Subspace Test).** $W \subseteq V$ is a subspace iff:
1. $\mathbf{0} \in W$,
2. $\mathbf{u}, \mathbf{v} \in W \Rightarrow \mathbf{u} + \mathbf{v} \in W$,
3. $c \in \mathbb{R},\, \mathbf{v} \in W \Rightarrow c\mathbf{v} \in W$.

**Why is $\mathbf{0} \in W$ necessary?** If $W = \emptyset$ or $\mathbf{0} \notin W$, then setting $c = 0$ in condition 3 would give $0\mathbf{v} = \mathbf{0} \in W$, contradiction. So the zero-vector condition is not redundant if we only check 2 and 3 on a potentially empty set.

---

## 👑 3. Theorems

### Theorem 2.3.1 — Subspace Test (from axioms)

The intersection $W_1 \cap W_2$ of any two subspaces is a subspace. The sum $W_1 + W_2 = \{\mathbf{w}_1 + \mathbf{w}_2 : \mathbf{w}_i \in W_i\}$ is also a subspace.

### Theorem 2.3.2 — Rank-Nullity Theorem

For any $A \in \mathbb{R}^{m \times n}$:

$$
\dim C(A) + \dim N(A) = n.
$$

That is, $\operatorname{rank}(A) + \operatorname{nullity}(A) = n$ (the number of **columns**).

### Theorem 2.3.3 — Fundamental Theorem of Linear Algebra

The four fundamental subspaces of $A \in \mathbb{R}^{m \times n}$ satisfy:

$$
C(A)^\perp = N(A^T), \qquad N(A)^\perp = C(A^T).
$$

That is, the column space and the left null space are orthogonal complements in $\mathbb{R}^m$; the row space and the null space are orthogonal complements in $\mathbb{R}^n$.

### Theorem 2.3.4 — Dimension Formula for Sum of Subspaces

For finite-dimensional subspaces $W_1, W_2$ of a vector space $V$:

$$
\dim(W_1 + W_2) = \dim W_1 + \dim W_2 - \dim(W_1 \cap W_2).
$$

---

## ✍️ 4. Proofs

### 4.1 Proof of Theorem 2.3.1 (Intersection is a Subspace)

Let $W_1, W_2$ be subspaces of $V$ and $W = W_1 \cap W_2$. Verify the three conditions:

**Zero:** $\mathbf{0} \in W_1$ and $\mathbf{0} \in W_2$ (both are subspaces), so $\mathbf{0} \in W_1 \cap W_2 = W$. ✓

**Closure under addition:** Let $\mathbf{u}, \mathbf{v} \in W$. Then $\mathbf{u}, \mathbf{v} \in W_1$ (since $W \subseteq W_1$), so $\mathbf{u} + \mathbf{v} \in W_1$ (since $W_1$ is a subspace). Similarly $\mathbf{u} + \mathbf{v} \in W_2$. Therefore $\mathbf{u} + \mathbf{v} \in W_1 \cap W_2 = W$. ✓

**Closure under scalar mult.:** Let $c \in \mathbb{R}$ and $\mathbf{v} \in W$. Then $\mathbf{v} \in W_1$ so $c\mathbf{v} \in W_1$. And $\mathbf{v} \in W_2$ so $c\mathbf{v} \in W_2$. Therefore $c\mathbf{v} \in W$. ✓ $\blacksquare$

### 4.2 Full Proof of the Rank-Nullity Theorem

**Setup.** Let $A \in \mathbb{R}^{m \times n}$, $r = \operatorname{rank}(A)$, and let $\{\mathbf{x}_1, \ldots, \mathbf{x}_{n-r}\}$ be a basis for $N(A)$ (the null space). We will extend this to a basis for $\mathbb{R}^n$ and show the extension maps to a basis for $C(A)$.

**Step 1: Extend to a basis of $\mathbb{R}^n$.** Since $\dim N(A) = n - r$ (to be derived — see below from RREF), by Theorem 2.1.4 we can choose additional vectors $\mathbf{z}_1, \ldots, \mathbf{z}_r \in \mathbb{R}^n$ such that:

$$
\mathcal{B} = \{\mathbf{x}_1, \ldots, \mathbf{x}_{n-r},\, \mathbf{z}_1, \ldots, \mathbf{z}_r\}
$$

is a basis for $\mathbb{R}^n$ (this extension is always possible in a finite-dimensional space).

**Step 2: Show $\{A\mathbf{z}_1, \ldots, A\mathbf{z}_r\}$ spans $C(A)$.** For any $\mathbf{b} \in C(A)$, there exists $\mathbf{v} \in \mathbb{R}^n$ with $A\mathbf{v} = \mathbf{b}$. Write $\mathbf{v}$ in the basis $\mathcal{B}$:

$$
\mathbf{v} = c_1 \mathbf{x}_1 + \cdots + c_{n-r}\mathbf{x}_{n-r} + d_1 \mathbf{z}_1 + \cdots + d_r \mathbf{z}_r.
$$

Apply $A$: since $A\mathbf{x}_i = \mathbf{0}$ for all $i$:

$$
\mathbf{b} = A\mathbf{v} = d_1 A\mathbf{z}_1 + \cdots + d_r A\mathbf{z}_r.
$$

So $\mathbf{b} \in \operatorname{span}\{A\mathbf{z}_1, \ldots, A\mathbf{z}_r\}$. ✓

**Step 3: Show $\{A\mathbf{z}_1, \ldots, A\mathbf{z}_r\}$ is linearly independent.** Suppose $\sum_{j=1}^r d_j A\mathbf{z}_j = \mathbf{0}$. Then $A(\sum_j d_j \mathbf{z}_j) = \mathbf{0}$, so $\sum_j d_j \mathbf{z}_j \in N(A)$. Write this vector in the basis $\mathcal{B}$:

$$
\sum_{j=1}^r d_j \mathbf{z}_j = \sum_{i=1}^{n-r} c_i \mathbf{x}_i.
$$

Rearranging: $\sum_j d_j \mathbf{z}_j - \sum_i c_i \mathbf{x}_i = \mathbf{0}$. Since $\mathcal{B}$ is a basis (independent), all coefficients are zero: $d_j = 0$ for all $j$, and $c_i = 0$ for all $i$. Hence $\{A\mathbf{z}_j\}$ is independent. ✓

**Conclusion.** $\{A\mathbf{z}_1, \ldots, A\mathbf{z}_r\}$ is a basis for $C(A)$, so $\dim C(A) = r$. We used $\dim N(A) = n - r$ (follows from the RREF having exactly $n - r$ free variables). Therefore:

$$
\dim C(A) + \dim N(A) = r + (n - r) = n. \quad \blacksquare
$$


### 4.3 Proof of Theorem 2.3.3 — Fundamental Theorem ($C(A) \perp N(A^T)$)

**Claim:** $C(A)$ and $N(A^T)$ are orthogonal complements in $\mathbb{R}^m$.

**Step 1: Orthogonality.** Let $\mathbf{b} \in C(A)$ and $\mathbf{y} \in N(A^T)$. Then $\mathbf{b} = A\mathbf{x}$ for some $\mathbf{x}$, and $A^T\mathbf{y} = \mathbf{0}$. Compute the inner product:

$$
\mathbf{y} \cdot \mathbf{b} = \mathbf{y}^T(A\mathbf{x}) = (A^T\mathbf{y})^T\mathbf{x} = \mathbf{0}^T \mathbf{x} = 0.
$$

So every vector in $C(A)$ is orthogonal to every vector in $N(A^T)$. ✓

**Step 2: Complementarity.** We have $\dim C(A) = r$ and (by applying rank-nullity to $A^T \in \mathbb{R}^{n \times m}$): $\dim N(A^T) = m - r$. Therefore:

$$
\dim C(A) + \dim N(A^T) = r + (m - r) = m = \dim \mathbb{R}^m.
$$

Two orthogonal subspaces whose dimensions sum to the ambient dimension are orthogonal complements. $\blacksquare$

**The analogous result** $N(A) \perp C(A^T)$ follows by applying the same argument to $A^T$ (swap $m \leftrightarrow n$). $\blacksquare$

### 4.4 Proof of Theorem 2.3.4 — Dimension Formula

**Strategy.** Build a basis for $W_1 + W_2$ by starting from a basis of $W_1 \cap W_2$ and extending.

Let $\dim(W_1 \cap W_2) = d$ with basis $\{\mathbf{b}_1, \ldots, \mathbf{b}_d\}$.

**Step 1.** Extend this to a basis of $W_1$: add vectors $\mathbf{u}_1, \ldots, \mathbf{u}_{p}$ so that $\{\mathbf{b}_1, \ldots, \mathbf{b}_d, \mathbf{u}_1, \ldots, \mathbf{u}_p\}$ is a basis for $W_1$. Then $\dim W_1 = d + p$.

**Step 2.** Extend the basis of $W_1 \cap W_2$ to a basis of $W_2$: add $\mathbf{v}_1, \ldots, \mathbf{v}_q$. Then $\dim W_2 = d + q$.

**Step 3.** Claim: $\mathcal{B} = \{\mathbf{b}_1,\ldots,\mathbf{b}_d, \mathbf{u}_1,\ldots,\mathbf{u}_p, \mathbf{v}_1,\ldots,\mathbf{v}_q\}$ is a basis for $W_1 + W_2$.

*Spanning:* Every $\mathbf{w} = \mathbf{w}_1 + \mathbf{w}_2 \in W_1 + W_2$ is a combination of the $\mathbf{b}_i, \mathbf{u}_j$ (from $W_1$) plus a combination of the $\mathbf{b}_i, \mathbf{v}_k$ (from $W_2$). ✓

*Independence:* Suppose $\sum \alpha_i \mathbf{b}_i + \sum \beta_j \mathbf{u}_j + \sum \gamma_k \mathbf{v}_k = \mathbf{0}$. Rewrite as:

$$
\sum \gamma_k \mathbf{v}_k = -\sum \alpha_i \mathbf{b}_i - \sum \beta_j \mathbf{u}_j.
$$

The right side $\in W_1$; the left side $\in W_2$. So both sides lie in $W_1 \cap W_2$ and can be written as a combination of $\{\mathbf{b}_i\}$. But $\{\mathbf{b}_i, \mathbf{v}_k\}$ is independent in $W_2$, so all $\gamma_k = 0$. Then $\sum \alpha_i \mathbf{b}_i + \sum \beta_j \mathbf{u}_j = \mathbf{0}$ with $\{\mathbf{b}_i, \mathbf{u}_j\}$ a basis for $W_1$ → all $\alpha_i = \beta_j = 0$. ✓

**Step 4.** $\dim(W_1 + W_2) = d + p + q = (d+p) + (d+q) - d = \dim W_1 + \dim W_2 - \dim(W_1 \cap W_2)$. $\blacksquare$

---

## 🎯 5. Worked Examples

### Example 2.3.E1 — Subspace Test: Pass

Is $W = \{(x, y, z)^T : x + 2y + 3z = 0\}$ a subspace of $\mathbb{R}^3$?

**Step 1.** $\mathbf{0}$: $0 + 0 + 0 = 0$. ✓

**Step 2.** Take $(x_1, y_1, z_1)$ and $(x_2, y_2, z_2)$ both satisfying the equation. Their sum: $(x_1+x_2) + 2(y_1+y_2) + 3(z_1+z_2) = (x_1+2y_1+3z_1) + (x_2+2y_2+3z_2) = 0 + 0 = 0$. ✓

**Step 3.** Scalar multiple: $cx + 2cy + 3cz = c(x+2y+3z) = c \cdot 0 = 0$. ✓

**Conclusion.** $W$ is a subspace — it's a **plane through the origin** in $\mathbb{R}^3$.

### Example 2.3.E2 — Subspace Test: Fail

Is $W = \{(x, y)^T : x + y = 1\}$ a subspace of $\mathbb{R}^2$?

**Step 1.** Check $\mathbf{0}$: $0 + 0 = 0 \neq 1$. So $\mathbf{0} \notin W$.

**Conclusion.** $W$ **fails** the zero-vector test → not a subspace. (It is an affine hyperplane, not a subspace.)


### Example 2.3.E3 — All Four Fundamental Subspaces of a $3 \times 4$ Matrix

Let

$$
A = \begin{pmatrix}1 & 2 & 0 & 1 \\ 2 & 4 & 1 & 3 \\ 0 & 0 & 1 & 1\end{pmatrix}.
$$

**Step 1 — RREF.** $R_2 \leftarrow R_2 - 2R_1$, then rows are already in good shape:

$$
\xrightarrow{R_2-2R_1} \begin{pmatrix}1&2&0&1\\0&0&1&1\\0&0&1&1\end{pmatrix} \xrightarrow{R_3-R_2} \begin{pmatrix}1&2&0&1\\0&0&1&1\\0&0&0&0\end{pmatrix}.
$$

Pivot columns: 1 and 3. Rank $r = 2$, nullity $= 4 - 2 = 2$.

**Step 2 — Column space $C(A)$, dim 2.** Take the original pivot columns (columns 1 and 3 of $A$):

$$
C(A) = \operatorname{span}\!\left\{\begin{pmatrix}1\\2\\0\end{pmatrix}, \begin{pmatrix}0\\1\\1\end{pmatrix}\right\}.
$$

**Step 3 — Null space $N(A)$, dim 2.** From RREF: pivot vars $x_1, x_3$; free vars $x_2 = s$, $x_4 = t$.

From row 2: $x_3 + x_4 = 0 \Rightarrow x_3 = -t$. From row 1: $x_1 + 2x_2 + x_4 = 0 \Rightarrow x_1 = -2s - t$.

$$
N(A) = \operatorname{span}\!\left\{\begin{pmatrix}-2\\1\\0\\0\end{pmatrix},\begin{pmatrix}-1\\0\\-1\\1\end{pmatrix}\right\}.
$$

**Step 4 — Row space $C(A^T)$, dim 2.** The non-zero rows of the RREF form a basis:

$$
C(A^T) = \operatorname{span}\!\left\{\begin{pmatrix}1\\2\\0\\1\end{pmatrix},\begin{pmatrix}0\\0\\1\\1\end{pmatrix}\right\}.
$$

**Step 5 — Left null space $N(A^T)$, dim 1.** Apply RREF to $A^T$ (equivalently, find $\mathbf{y}: A^T\mathbf{y}=\mathbf{0}$ or use augmented $[A\mid I_3]$ elimination). Result:

$$
N(A^T) = \operatorname{span}\!\left\{\begin{pmatrix}-2\\1\\-1\end{pmatrix}\right\}.
$$

**Rank-Nullity check:** $r + \text{nullity} = 2 + 2 = 4 = n$. ✓ And $r + \dim N(A^T) = 2 + 1 = 3 = m$. ✓

### Example 2.3.E4 — Projection onto a Subspace

Project $\mathbf{b} = (1,2,3)^T$ onto the subspace $W = \operatorname{span}\{(1,1,0)^T, (0,1,1)^T\}$.

**Step 1.** Form $A = \begin{pmatrix}1&0\\1&1\\0&1\end{pmatrix}$ (columns are the basis vectors).

**Step 2.** The projection is $\hat{\mathbf{b}} = A(A^T A)^{-1}A^T \mathbf{b}$.

**Step 3.** $A^T A = \begin{pmatrix}1&1&0\\0&1&1\end{pmatrix}\begin{pmatrix}1&0\\1&1\\0&1\end{pmatrix} = \begin{pmatrix}2&1\\1&2\end{pmatrix}$.

**Step 4.** $(A^T A)^{-1} = \frac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$.

**Step 5.** $A^T\mathbf{b} = \begin{pmatrix}3\\5\end{pmatrix}$.

**Step 6.** $(A^T A)^{-1}A^T\mathbf{b} = \frac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\begin{pmatrix}3\\5\end{pmatrix} = \frac{1}{3}\begin{pmatrix}1\\7\end{pmatrix}$.

**Step 7.** $\hat{\mathbf{b}} = A \cdot \frac{1}{3}\begin{pmatrix}1\\7\end{pmatrix} = \frac{1}{3}\begin{pmatrix}1\\8\\7\end{pmatrix}$.

The **error** $\mathbf{e} = \mathbf{b} - \hat{\mathbf{b}} = (1,2,3)^T - \frac{1}{3}(1,8,7)^T = \frac{1}{3}(2,-2,2)^T$, which is perpendicular to $W$.

**Verify:** $\mathbf{e} \cdot (1,1,0)^T = \frac{1}{3}(2-2+0) = 0$ ✓, $\mathbf{e} \cdot (0,1,1)^T = \frac{1}{3}(0-2+2) = 0$ ✓.

### Example 2.3.E5 — Rank-Nullity Verification

For $A = \begin{pmatrix}1&3&-2\\2&6&-4\end{pmatrix}$: the RREF is $\begin{pmatrix}1&3&-2\\0&0&0\end{pmatrix}$. Rank $= 1$, nullity $= 3 - 1 = 2$. Check: $1 + 2 = 3 = n$. ✓

Null space basis: $x_1 = -3x_2 + 2x_3$, so $N(A) = \operatorname{span}\{(-3,1,0)^T,(2,0,1)^T\}$.


### Example 2.3.E6 — Orthogonal Complement

Find $W^\perp$ for $W = \operatorname{span}\{(1,2,3)^T\} \subseteq \mathbb{R}^3$.

$W^\perp = \{(x,y,z)^T : x + 2y + 3z = 0\}$. Free variables: $y=s$, $z=t$, $x=-2s-3t$.

$W^\perp = \operatorname{span}\{(-2,1,0)^T,(-3,0,1)^T\}$, dim $= 2$. Check: $1 + 2 = 3 = \dim\mathbb{R}^3$. ✓

### Example 2.3.E7 — Polynomials as a Vector Space

Show that $\mathcal{P}_2 = \{a_0 + a_1 x + a_2 x^2 : a_i \in \mathbb{R}\}$ is a vector space.

All 8 axioms are inherited from function addition and scalar multiplication on $\mathbb{R}$. The zero polynomial $0$ is the additive identity. The standard basis $\{1, x, x^2\}$ demonstrates $\dim\mathcal{P}_2 = 3$.

### Example 2.3.E8 — Intersection Dimension

$W_1 = \operatorname{span}\{(1,0,0)^T,(0,1,0)^T\}$ (the $xy$-plane) and $W_2 = \operatorname{span}\{(1,0,0)^T,(0,0,1)^T\}$ (the $xz$-plane) in $\mathbb{R}^3$. Then $W_1 \cap W_2 = \operatorname{span}\{(1,0,0)^T\}$ (the $x$-axis).

By Theorem 2.3.4: $\dim(W_1 + W_2) = 2 + 2 - 1 = 3$. Indeed $W_1 + W_2 = \mathbb{R}^3$. ✓

---

## 📝 6. Challenge Problems

### Problem 2.3.P1

Show that the set $W = \{f \in \mathcal{C}([0,1]) : f(0) = 0\}$ is a subspace of $\mathcal{C}([0,1])$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Zero:** $f \equiv 0$ satisfies $f(0) = 0$. ✓

**Closure under addition:** If $f(0)=0$ and $g(0)=0$, then $(f+g)(0) = 0+0=0$. ✓

**Closure under scalar mult.:** $(cf)(0) = c \cdot 0 = 0$. ✓ Hence $W$ is a subspace. $\blacksquare$

</details>

### Problem 2.3.P2

Find all four fundamental subspaces and verify rank-nullity for $A = \begin{pmatrix}1&2&1\\3&6&3\end{pmatrix}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**RREF:** $R_2 - 3R_1 \to 0$. RREF $= \begin{pmatrix}1&2&1\\0&0&0\end{pmatrix}$. Rank $=1$.

**$C(A)$:** span$\{(1,3)^T\}$, dim 1.

**$N(A)$:** $x_1 = -2s-t$: span$\{(-2,1,0)^T,(-1,0,1)^T\}$, dim 2.

**$C(A^T)$:** span$\{(1,2,1)^T\}$, dim 1.

**$N(A^T)$:** solve $A^T\mathbf{y}=\mathbf{0}$: span$\{(-3,1)^T\}$, dim 1.

**Rank-nullity:** $1+2=3=n$. ✓ And $1+1=2=m$. ✓

</details>

### Problem 2.3.P3

Prove: $N(A) \subseteq N(A^T A)$ and $N(A^T A) \subseteq N(A)$, hence $N(A) = N(A^T A)$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**($\subseteq$):** If $A\mathbf{x}=\mathbf{0}$, then $A^T(A\mathbf{x}) = A^T\mathbf{0} = \mathbf{0}$. ✓

**($\supseteq$):** If $A^T A\mathbf{x}=\mathbf{0}$, compute $\|A\mathbf{x}\|^2 = (A\mathbf{x})^T(A\mathbf{x}) = \mathbf{x}^T A^T A \mathbf{x} = \mathbf{x}^T \mathbf{0} = 0$.

Since $\|A\mathbf{x}\|^2 = 0$ and norms are non-negative, $A\mathbf{x} = \mathbf{0}$. $\blacksquare$

</details>

### Problem 2.3.P4

For $W = \operatorname{span}\{(1,1,0,0)^T,(0,0,1,1)^T\}$ in $\mathbb{R}^4$, find $W^\perp$ and verify $\dim W + \dim W^\perp = 4$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

$W^\perp$: solve $\mathbf{v} \cdot (1,1,0,0)^T = 0$ and $\mathbf{v} \cdot (0,0,1,1)^T = 0$, i.e., $v_1+v_2=0$ and $v_3+v_4=0$.

Free vars: $v_2=s$, $v_4=t$. $W^\perp = \operatorname{span}\{(-1,1,0,0)^T,(0,0,-1,1)^T\}$, dim 2.

$\dim W + \dim W^\perp = 2+2=4$. ✓

</details>

### Problem 2.3.P5

Show that $M_{2\times2}(\mathbb{R})$ (all $2\times 2$ real matrices) is a vector space of dimension 4.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

All 8 axioms hold under component-wise addition and scalar multiplication. The standard basis is $\left\{\begin{pmatrix}1&0\\0&0\end{pmatrix},\begin{pmatrix}0&1\\0&0\end{pmatrix},\begin{pmatrix}0&0\\1&0\end{pmatrix},\begin{pmatrix}0&0\\0&1\end{pmatrix}\right\}$ — 4 independent matrices that span $M_{2\times2}$. Hence dim $= 4$. $\blacksquare$

</details>


### Problem 2.3.P6

Use the dimension formula to find $\dim(W_1 + W_2)$ where $W_1 = \operatorname{span}\{(1,0,1)^T,(0,1,0)^T\}$ and $W_2 = \operatorname{span}\{(1,0,-1)^T,(0,1,0)^T\}$ in $\mathbb{R}^3$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

$\dim W_1 = 2$, $\dim W_2 = 2$.

$W_1 \cap W_2$: a vector $c_1(1,0,1)+c_2(0,1,0) = d_1(1,0,-1)+d_2(0,1,0)$ gives: $c_1=d_1$, $c_2=d_2$, $c_1=-d_1$. Hence $c_1=0, c_2 = d_2$ free. $W_1\cap W_2 = \operatorname{span}\{(0,1,0)^T\}$, dim 1.

$\dim(W_1+W_2) = 2+2-1=3 = \dim\mathbb{R}^3$, so $W_1+W_2=\mathbb{R}^3$.

</details>

### Problem 2.3.P7

Prove that rank$(A)$ = rank$(A^T)$ using the four fundamental subspaces.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

rank$(A) = \dim C(A) = r$. Applying rank-nullity to $A^T$: $\dim C(A^T) + \dim N(A^T) = m$; also $\dim C(A^T) = $ rank$(A^T)$. By the Fundamental Theorem, $N(A^T) \perp C(A)$ in $\mathbb{R}^m$ and $\dim C(A) + \dim N(A^T) = m$, so $\dim N(A^T) = m - r$, hence $\dim C(A^T) = r = $ rank$(A)$. $\blacksquare$

</details>

### Problem 2.3.P8

For $A \in \mathbb{R}^{3 \times 3}$ with rank 2, state the dimensions of all four fundamental subspaces and sketch how they pair as orthogonal complements.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

With $m=n=3$, $r=2$:
- $\dim C(A) = 2$ (plane in $\mathbb{R}^3$)
- $\dim N(A^T) = 1$ (line in $\mathbb{R}^3$), perpendicular to $C(A)$
- $\dim C(A^T) = 2$ (plane in $\mathbb{R}^3$)
- $\dim N(A) = 1$ (line in $\mathbb{R}^3$), perpendicular to $C(A^T)$

$C(A) \oplus N(A^T) = \mathbb{R}^3$ (orthogonal direct sum). $C(A^T) \oplus N(A) = \mathbb{R}^3$ (orthogonal direct sum).

</details>

---

## ⚠️ 7. Common Pitfalls

1. **Forgetting the zero vector.** A subset without $\mathbf{0}$ cannot be a subspace. This is the single most common mistake — always check it first.

2. **Confusing column space with row space.** $C(A)$ lives in $\mathbb{R}^m$ (ambient space of outputs); $C(A^T)$ lives in $\mathbb{R}^n$ (ambient space of inputs). They have the same dimension $r$ but live in different spaces.

3. **Rank vs. nullity.** Rank counts the pivot columns (free information); nullity counts the free variable columns (lost information). $r + \text{nullity} = n$ — always the number of *columns*, not rows.

4. **Subspace vs. affine subspace.** $\{\mathbf{x} : A\mathbf{x} = \mathbf{b}\}$ for $\mathbf{b} \neq \mathbf{0}$ is *not* a subspace (it doesn't contain $\mathbf{0}$). It is the **solution set** of a non-homogeneous system — a coset of the null space.

5. **Orthogonal complement ≠ "everything else".** $W^\perp$ is precisely the set of vectors perpendicular to every vector in $W$. It is not just $V \setminus W$.

6. **Row operations preserve the row space (not the column space).** The RREF has the same row space as $A$ but different columns. The column space basis must come from the *original* pivot columns, not the RREF's pivot columns.

---

## 🔗 8. Cross-Links

- **Backward:** [2.2 - Matrix Multiplication & Gaussian Elimination](2.2---Matrix-Multiplication-&-Gaussian-Elimination) — Gaussian elimination *is* the algorithm for finding the null space and column space basis.
- **Backward:** [2.1 - Vectors & Linear Combinations](2.1---Vectors-&-Linear-Combinations) — the four subspaces are four specific applications of span and linear independence.
- **Forward:** [2.4 - Linear Transformations & Change of Basis](2.4---Linear-Transformations-&-Change-of-Basis) — the rank gives the dimension of the image; the nullity gives the dimension of the kernel. The rank-nullity theorem is the dimension half of the first isomorphism theorem.
- **Forward:** [2.7 - Inner Product Spaces & Orthogonality](2.7---Inner-Product-Spaces-&-Orthogonality) — projections and the Gram-Schmidt process build directly on orthogonal complements.
- **Physics:** In quantum mechanics, the Hilbert space $\mathcal{H}$ is an infinite-dimensional inner-product space. The image of an observable operator is the physically accessible states; its kernel represents "gauge freedom". The Fundamental Theorem of Linear Algebra is the finite-dimensional shadow of the spectral theorem.

---

## 📖 9. Sources & Further Reading

| Source | Notes |
|---|---|
| Gilbert Strang, MIT 18.06 — Lectures 9–14 | The four fundamental subspaces, Strang's "big picture". [OCW](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) |
| 3Blue1Brown — Essence of Linear Algebra, Ch. 7 (Inverse) | Null space and column space visualized as kernel and image. [YouTube](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) |
| Sergei Treil, *LADW* Ch. 1–3 | Abstract vector spaces, subspaces, and linear maps in full generality. [PDF](https://www.math.brown.edu/treil/papers/LADW/LADW.html) |
| Sheldon Axler, *LADR* Ch. 2 | Basis, dimension, and direct sum decomposition. |


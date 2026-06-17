---
title: "Svd Tensors"
subject: "Linear Algebra & Matrix Theory"
catalog: advanced
audience_tier: higher-education
chapter: "2.8"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 2.8 — Singular Value Decomposition & Tensors

> *"The SVD is the Swiss Army knife of linear algebra."* — Lloyd Trefethen & David Bau

Chapter 2.7 gave us orthonormal bases and projection. This chapter wields those tools to carve **any** matrix — rectangular, rank-deficient, non-symmetric — into its most revealing form: the **Singular Value Decomposition** (SVD). Then we step up one level of abstraction: we replace vectors (1-index objects) with **tensors** (multi-index objects) and discover that the inner product, the SVD, and the geometry of physics all live in the same algebraic family.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define singular values and singular vectors; construct the SVD $A = U\Sigma V^\top$.
2. Prove existence of the SVD by construction from eigenvalues of $A^\top A$.
3. Apply the Eckart-Young theorem: identify the best rank-$k$ approximation of $A$.
4. Compute the Moore-Penrose pseudoinverse $A^+ = V\Sigma^+ U^\top$.
5. Interpret PCA as SVD on a centered data matrix.
6. Define a $(p,q)$-tensor; apply the Einstein summation convention.
7. Raise and lower indices using the metric tensor $g_{ij}$.
8. Connect differential forms (Ch. 1.8) to antisymmetric covariant tensors.

---

## 🖼️ Visual Anchor — SVD as Three Transformations

![math-02__2.8-fig1](math-02__2.8-fig1.svg)


---

## 📚 1. Definitions

### Part A — Singular Value Decomposition

### Definition 2.8.1 — Singular Values and Singular Vectors

Let $A \in \mathbb{R}^{m \times n}$. The matrix $A^\top A \in \mathbb{R}^{n \times n}$ is symmetric positive semidefinite (its eigenvalues are all $\geq 0$ — see Problem 2.8.P4). Let $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n \geq 0$ be its eigenvalues.

The **singular values** of $A$ are:

$$
\sigma_i = \sqrt{\lambda_i} \geq 0, \quad i = 1, \ldots, n.
$$

The **right singular vectors** $v_1, \ldots, v_n$ are the orthonormal eigenvectors of $A^\top A$:

$$
A^\top A\, v_i = \lambda_i v_i = \sigma_i^2\, v_i.
$$

The **left singular vectors** $u_i$ (for $\sigma_i > 0$) are defined by:

$$
u_i = \frac{1}{\sigma_i} A v_i.
$$

One can verify $u_i$ are orthonormal and are eigenvectors of $AA^\top$ with the same eigenvalue $\sigma_i^2$ (proof in §5.1).

### Definition 2.8.2 — The Full SVD

Collect: $U = [u_1|\cdots|u_m] \in \mathbb{R}^{m \times m}$ (orthogonal), $V = [v_1|\cdots|v_n] \in \mathbb{R}^{n \times n}$ (orthogonal), and $\Sigma \in \mathbb{R}^{m \times n}$ (diagonal with $\Sigma_{ii} = \sigma_i$ for $i \leq \min(m,n)$, zero elsewhere). Then:

$$
A = U \Sigma V^\top.
$$

The **rank** of $A$ equals the number of non-zero singular values.

**Thin (economy) SVD.** When $m > n$, we can trim $U$ to its first $n$ columns ($U_r \in \mathbb{R}^{m \times n}$), trim $\Sigma$ to $\Sigma_r \in \mathbb{R}^{n \times n}$, and keep full $V$. Then $A = U_r \Sigma_r V^\top$ with $U_r^\top U_r = I_n$.

### Definition 2.8.3 — Moore-Penrose Pseudoinverse

The **pseudoinverse** of $A = U\Sigma V^\top$ is:

$$
A^+ = V \Sigma^+ U^\top,
$$

where $\Sigma^+$ is obtained from $\Sigma^\top$ by replacing each non-zero $\sigma_i$ with $1/\sigma_i$.

**Interpretation.** $A^+\mathbf{b}$ gives the minimum-norm least-squares solution: among all $\hat{\mathbf{x}}$ minimizing $\|A\mathbf{x}-\mathbf{b}\|$, it is the one with smallest $\|\hat{\mathbf{x}}\|$.

### Definition 2.8.4 — Eckart-Young Best Rank-$k$ Approximation

Given $A = \sum_{i=1}^r \sigma_i u_i v_i^\top$ (the **outer product form** of the SVD), the **best rank-$k$ approximation** to $A$ in both spectral and Frobenius norms is:

$$
A_k = \sum_{i=1}^k \sigma_i u_i v_i^\top, \quad k \leq r.
$$

The approximation error is:

$$
\|A - A_k\|_F = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}, \qquad \|A - A_k\|_2 = \sigma_{k+1}.
$$

---

### Part B — Tensors

### Definition 2.8.5 — Tensor as a Multilinear Map

A **$(p,q)$-tensor** $T$ on a vector space $V$ (over $\mathbb{R}$) is a multilinear map:

$$
T : \underbrace{V^* \times \cdots \times V^*}_{p \text{ copies}} \times \underbrace{V \times \cdots \times V}_{q \text{ copies}} \to \mathbb{R},
$$

where $V^*$ is the **dual space** (the space of linear functionals on $V$). Multilinear means $T$ is linear in each argument separately.

- A **(0,0)-tensor** is a scalar.
- A **(1,0)-tensor** (one covariant slot) is a co-vector / 1-form / linear functional $V \to \mathbb{R}$.
- A **(0,1)-tensor** is a vector (via the natural embedding in $V^{**} \cong V$).
- A **(0,2)-tensor** is a bilinear form (e.g., the metric, the stress tensor).
- A **(1,1)-tensor** is a linear map $V \to V$ — familiar from matrix multiplication.

In components (with respect to a basis $\{e_1, \ldots, e_n\}$ and dual basis $\{e^1, \ldots, e^n\}$), a $(p,q)$-tensor has $n^{p+q}$ components:

$$
T^{i_1 \cdots i_p}{}_{j_1 \cdots j_q}.
$$

The **$p$ upper indices** are **contravariant** (transform with the inverse of a basis change); the **$q$ lower indices** are **covariant** (transform with the basis change itself).

### Definition 2.8.6 — Einstein Summation Convention

Any index that appears **exactly twice** in a product — once up and once down — is **summed** over its full range. The explicit $\sum$ symbol is dropped.

$$
A^i{}_j B^j{}_k \;\equiv\; \sum_{j=1}^n A^i{}_j B^j{}_k.
$$

This encodes matrix multiplication: $C = AB$ becomes $C^i{}_k = A^i{}_j B^j{}_k$.

The **trace** of a matrix: $\text{tr}(A) = A^i{}_i$.

A **contraction** on a $(1,1)$-tensor produces a scalar: $T^i{}_i = \text{tr}(T)$.

### Definition 2.8.7 — Metric Tensor

In a (semi-)Riemannian manifold, the **metric tensor** $g$ is a non-degenerate symmetric $(0,2)$-tensor:

$$
g_{ij} = g_{ji}, \qquad g_{ij} x^i x^j > 0 \text{ for all nonzero vectors } x \text{ (Riemannian case)}.
$$

In Euclidean space with an orthonormal frame, $g_{ij} = \delta_{ij}$ (the Kronecker delta).

**Raising and lowering indices.** The inverse metric $g^{ij}$ (defined by $g^{ik}g_{kj} = \delta^i_j$) is used to **raise** an index:

$$
v^i = g^{ij} v_j \quad \text{(raise)}, \qquad v_i = g_{ij} v^j \quad \text{(lower)}.
$$

This is how the metric converts between vectors (contravariant) and covectors (covariant).

### Definition 2.8.8 — Tensor Operations

**Outer product (tensor product):** Given tensors $S$ of type $(p,q)$ and $T$ of type $(r,s)$, the outer product $S \otimes T$ has type $(p+r, q+s)$ with components:

$$
(S \otimes T)^{i_1\cdots i_p k_1\cdots k_r}{}_{j_1\cdots j_q \ell_1\cdots \ell_s} = S^{i_1\cdots i_p}{}_{j_1\cdots j_q}\, T^{k_1\cdots k_r}{}_{\ell_1\cdots \ell_s}.
$$

**Contraction:** Choose one upper and one lower index and sum over them, reducing the tensor type by $(1,1)$.

**Symmetrization:** $T_{(ij)} = \tfrac{1}{2}(T_{ij} + T_{ji})$.

**Antisymmetrization:** $T_{[ij]} = \tfrac{1}{2}(T_{ij} - T_{ji})$.


---

## 👑 2. Major Theorems

### Theorem 2.8.1 — Every Matrix Has an SVD

Every real matrix $A \in \mathbb{R}^{m \times n}$ admits a singular value decomposition $A = U\Sigma V^\top$.

### Theorem 2.8.2 — SVD Reveals the Four Fundamental Subspaces

The SVD $A = U\Sigma V^\top$ (with $r = \text{rank}(A)$ non-zero singular values) gives:

| Subspace | Basis |
|---|---|
| Column space $C(A)$ | $u_1, \ldots, u_r$ |
| Left nullspace $N(A^\top)$ | $u_{r+1}, \ldots, u_m$ |
| Row space $C(A^\top)$ | $v_1, \ldots, v_r$ |
| Nullspace $N(A)$ | $v_{r+1}, \ldots, v_n$ |

### Theorem 2.8.3 — Eckart-Young Theorem (Best Low-Rank Approximation)

Among all rank-$k$ matrices $B$ (with $k < r = \text{rank}(A)$):

$$
\|A - A_k\|_2 = \min_{\text{rank}(B) \leq k} \|A - B\|_2 = \sigma_{k+1}.
$$

The same statement holds in the Frobenius norm.

### Theorem 2.8.4 — Pseudoinverse Gives Minimum-Norm Least-Squares Solution

The vector $\hat{\mathbf{x}} = A^+\mathbf{b}$ satisfies:

1. $\hat{\mathbf{x}}$ minimizes $\|A\mathbf{x} - \mathbf{b}\|$ (least-squares condition).
2. Among all minimizers, $\hat{\mathbf{x}}$ has the smallest norm $\|\hat{\mathbf{x}}\|$.

---

## ✍️ 3. Proofs / Derivations

### 3.1 Proof That Every Matrix Has an SVD

**Step 1: Eigendecomposition of $A^\top A$.**
$A^\top A$ is symmetric positive semidefinite ($\mathbf{x}^\top (A^\top A)\mathbf{x} = \|A\mathbf{x}\|^2 \geq 0$). By the spectral theorem (Ch. 2.6), it has an orthonormal eigenbasis $\{v_1,\ldots,v_n\}$ with eigenvalues $\sigma_1^2 \geq \cdots \geq \sigma_r^2 > 0 = \sigma_{r+1}^2 = \cdots = \sigma_n^2$.

**Step 2: Define right singular vectors $V$.**
Collect $v_1, \ldots, v_n$ as columns of $V$. Then $A^\top A V = V D$ where $D = \text{diag}(\sigma_1^2,\ldots,\sigma_n^2)$, i.e., $V^\top A^\top A V = D$.

**Step 3: Define left singular vectors $u_i$ for $i \leq r$.**
For each $i \leq r$, set $u_i = (1/\sigma_i) Av_i$. These are unit vectors since:

$$
\|u_i\|^2 = \frac{1}{\sigma_i^2}\|Av_i\|^2 = \frac{1}{\sigma_i^2}v_i^\top A^\top Av_i = \frac{1}{\sigma_i^2} \sigma_i^2 \|v_i\|^2 = 1.
$$

They are mutually orthogonal: for $i \neq j \leq r$:

$$
\langle u_i, u_j \rangle = \frac{1}{\sigma_i \sigma_j} v_i^\top A^\top A v_j = \frac{\sigma_j^2}{\sigma_i \sigma_j} \langle v_i, v_j \rangle = 0.
$$

**Step 4: Extend to a full orthonormal basis.**
Choose $u_{r+1},\ldots,u_m$ to complete an orthonormal basis for $\mathbb{R}^m$ (Gram-Schmidt on any completion). By construction, $Av_i = \mathbf{0}$ for $i > r$ (since $v_i \in N(A)$), so any extension works.

**Step 5: Verify $A = U\Sigma V^\top$.**
For $i \leq r$: $Av_i = \sigma_i u_i$. For $i > r$: $Av_i = \mathbf{0} = \sigma_i u_i$ (since $\sigma_i = 0$). Writing $A = U\Sigma V^\top$ is equivalent to $AV = U\Sigma$, and each column $i$ reads: $Av_i = \sigma_i u_i$. ✓ $\blacksquare$

### 3.2 Relation Between SVD and Eigendecomposition

For a **symmetric** positive semidefinite matrix $A = Q\Lambda Q^\top$ (spectral theorem):

$$
A = Q\Lambda Q^\top = U\Sigma V^\top \quad \text{with } U = Q,\; V = Q,\; \Sigma = \Lambda.
$$

For a **non-symmetric** matrix, the left and right singular vectors $U \neq V$, and the SVD is fundamentally different from the eigendecomposition. Indeed, the eigenvalues of $A$ can be complex, while singular values are always real and non-negative.

### 3.3 Proof of Rank = Number of Non-Zero Singular Values

**($\leq$):** From $A = U\Sigma V^\top$, the column space of $A$ equals the column space of $U\Sigma$ (since $V^\top$ is invertible). The column space of $U\Sigma$ has dimension equal to the number of non-zero diagonal entries in $\Sigma$, i.e., $r$.

**($\geq$):** Conversely, the $r$ columns $u_1,\ldots,u_r$ are in $C(A)$ (they are $Av_i/\sigma_i$) and are linearly independent. So $\text{rank}(A) \geq r$. $\blacksquare$

### 3.4 Pseudoinverse via SVD

We want the least-squares, minimum-norm solution to $A\mathbf{x} = \mathbf{b}$. Write $A = U\Sigma V^\top$ and substitute $\mathbf{y} = V^\top \mathbf{x}$ (so $\|\mathbf{x}\| = \|\mathbf{y}\|$ since $V$ is orthogonal):

$$
\|A\mathbf{x} - \mathbf{b}\|^2 = \|U\Sigma\mathbf{y} - \mathbf{b}\|^2 = \|\Sigma\mathbf{y} - U^\top\mathbf{b}\|^2.
$$

Let $\mathbf{c} = U^\top\mathbf{b}$. The $i$th component of $\Sigma\mathbf{y} - \mathbf{c}$:
- For $i \leq r$ (non-zero $\sigma_i$): the residual is $\sigma_i y_i - c_i$, minimized by $y_i = c_i/\sigma_i$.
- For $i > r$ (zero $\sigma_i$): the residual is $-c_i$ (fixed; unaffected by $y_i$).

Minimum norm further forces $y_i = 0$ for $i > r$. So $\hat{\mathbf{y}} = \Sigma^+ \mathbf{c} = \Sigma^+ U^\top\mathbf{b}$, and:

$$
\hat{\mathbf{x}} = V\hat{\mathbf{y}} = V\Sigma^+ U^\top \mathbf{b} = A^+\mathbf{b}. \quad \blacksquare
$$


---

## 🖼️ 4. SVG Gallery

### SVG 2 — The Four Fundamental Subspaces via SVD

![math-02__2.8-fig2](math-02__2.8-fig2.svg)

### SVG 3 — Low-Rank Approximation: Truncating Small Singular Values

![math-02__2.8-fig3](math-02__2.8-fig3.svg)


### SVG 4 — Tensor as a Multilinear Machine

![math-02__2.8-fig4](math-02__2.8-fig4.svg)

### SVG 5 — Metric Tensor: Raising and Lowering Indices

![math-02__2.8-fig5](math-02__2.8-fig5.svg)


---

## 🎯 5. Worked Examples

### Example 2.8.E1 — SVD of a 2×3 Matrix by Hand

Compute the SVD of $A = \begin{pmatrix} 3 & 0 & 0 \\ 0 & 2 & 0 \end{pmatrix}$.

This matrix is already in "diagonal" form. By inspection:

$$
A = U\Sigma V^\top, \quad U = I_2, \quad \Sigma = \begin{pmatrix}3&0&0\\0&2&0\end{pmatrix}, \quad V = I_3.
$$

Singular values: $\sigma_1 = 3$, $\sigma_2 = 2$ (read off the diagonal). Rank = 2. $v_3 = e_3$ spans the nullspace $N(A)$; $u_1, u_2$ span $C(A) = \mathbb{R}^2$.

Now do a **non-trivial** example. Let $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \\ 0 & 0 \end{pmatrix}$ (a $3 \times 2$ matrix).

**Step 1.** Compute $A^\top A$:

$$
A^\top A = \begin{pmatrix}1&0&0\\1&1&0\end{pmatrix}\begin{pmatrix}1&1\\0&1\\0&0\end{pmatrix} = \begin{pmatrix}1&1\\1&2\end{pmatrix}.
$$

**Step 2.** Eigenvalues of $A^\top A$: $\det\begin{pmatrix}1-\lambda&1\\1&2-\lambda\end{pmatrix} = \lambda^2 - 3\lambda + 1 = 0$.

$$
\lambda_{1,2} = \frac{3 \pm \sqrt{5}}{2}.
$$

So $\sigma_1 = \sqrt{(3+\sqrt{5})/2}$, $\sigma_2 = \sqrt{(3-\sqrt{5})/2}$.

**Step 3.** Eigenvectors of $A^\top A$ (right singular vectors $V$): for $\lambda_1$:

$(A^\top A - \lambda_1 I)v = 0 \Rightarrow v_1 \propto (1, (\sqrt{5}-1)/2)^\top$ (normalized).

**Step 4.** $u_i = Av_i/\sigma_i$ gives left singular vectors; extend to orthonormal basis for $\mathbb{R}^3$.

(Full numerics: $\sigma_1 \approx 1.618$, $\sigma_2 \approx 0.618$ — the **golden ratio** and its reciprocal!)

### Example 2.8.E2 — Low-Rank Approximation

Let $A$ have singular values $\sigma_1 = 10$, $\sigma_2 = 3$, $\sigma_3 = 1$, $\sigma_4 = 0.1$. Find the best rank-2 approximation error.

By Eckart-Young:

$$
\|A - A_2\|_2 = \sigma_3 = 1, \qquad \|A - A_2\|_F = \sqrt{1^2 + 0.1^2} = \sqrt{1.01} \approx 1.005.
$$

Relative error: $\|A - A_2\|_F / \|A\|_F = \sqrt{1.01}/\sqrt{100+9+1+0.01} \approx 1.005/10.05 \approx 10\%$.

### Example 2.8.E3 — Pseudoinverse

For $A = \begin{pmatrix}2&0\\0&3\\0&0\end{pmatrix}$, the SVD is immediate: $U = I_3$, $\Sigma = \begin{pmatrix}2&0\\0&3\\0&0\end{pmatrix}$, $V = I_2$.

$$
A^+ = V\Sigma^+ U^\top = I_2 \begin{pmatrix}1/2&0&0\\0&1/3&0\end{pmatrix} I_3 = \begin{pmatrix}1/2&0&0\\0&1/3&0\end{pmatrix}.
$$

Check: $A^+ A = \begin{pmatrix}1/2&0&0\\0&1/3&0\end{pmatrix}\begin{pmatrix}2&0\\0&3\\0&0\end{pmatrix} = I_2$. ✓ (But $AA^+ = \begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix} \neq I_3$.)

### Example 2.8.E4 — Einstein Summation: Matrix Multiplication

Express matrix multiplication $C = AB$ (with $A \in \mathbb{R}^{m \times k}$, $B \in \mathbb{R}^{k \times n}$) in Einstein notation.

$$
C^i{}_j = A^i{}_k B^k{}_j.
$$

The index $k$ appears once up (in $A^i{}_k$) and once down (in $B^k{}_j$) — it is the **contracted** (summed) index. The free indices $i$ and $j$ label the row and column of the output.

**Trace:** $\text{tr}(AB) = C^i{}_i = A^i{}_k B^k{}_i$ (both $i$ and $k$ are contracted).

### Example 2.8.E5 — Einstein Summation: Quadratic Form

Express $\mathbf{x}^\top M \mathbf{x}$ (a scalar quadratic form) using Einstein summation.

In components, $x^\top M x = x_i M^{ij} x_j$ — but this mixes conventions. Using index position:

$$
x^i M_{ij} x^j \equiv \sum_{i,j} x^i M_{ij} x^j.
$$

The indices $i$ and $j$ each appear twice (once up, once down), so both are summed. For the Euclidean metric $g_{ij} = \delta_{ij}$, this reduces to the standard dot product: $\mathbf{x}^\top \mathbf{x} = x^i \delta_{ij} x^j = x^i x_i$.

### Example 2.8.E6 — Metric Tensor: Raising an Index

In 2D Euclidean space with metric $g_{ij} = \begin{pmatrix}1&0\\0&1\end{pmatrix}$ (trivial), raise the index of $v_i = (3, -2)$:

$$
v^i = g^{ij}v_j = \delta^{ij}v_j = v_i = (3, -2).
$$

No difference. Now use the metric $g_{ij} = \begin{pmatrix}2&1\\1&3\end{pmatrix}$ (a non-Euclidean inner product):

$$
g^{ij} = \frac{1}{\det g}\begin{pmatrix}3&-1\\-1&2\end{pmatrix} = \frac{1}{5}\begin{pmatrix}3&-1\\-1&2\end{pmatrix}.
$$

$$
v^1 = g^{11}v_1 + g^{12}v_2 = \frac{1}{5}(3 \cdot 3 + (-1)(-2)) = \frac{11}{5}, \qquad v^2 = \frac{1}{5}(-3+2(-2)) \cdot (-1) = \frac{7}{5}.
$$

**Wait — recompute carefully.** $v^2 = g^{21}v_1 + g^{22}v_2 = \frac{1}{5}(-1)(3) + \frac{1}{5}(2)(-2) = \frac{-3-4}{5} = -\frac{7}{5}$.

Verify: $g_{ij}v^j = v_i$? $g_{11}v^1 + g_{12}v^2 = 2 \cdot \frac{11}{5} + 1 \cdot (-\frac{7}{5}) = \frac{22-7}{5} = 3 = v_1$. ✓

### Example 2.8.E7 — Outer Product

Compute the outer product $T = u \otimes v$ for $u = (1,2)^\top$ and $v = (3,4)^\top$.

$$
T^{ij} = u^i v^j \implies T = \begin{pmatrix}1\cdot3 & 1\cdot4\\2\cdot3 & 2\cdot4\end{pmatrix} = \begin{pmatrix}3&4\\6&8\end{pmatrix}.
$$

$T$ is a $(2,0)$-tensor (or equivalently a rank-1 matrix — the outer product $uv^\top$). Note $\text{rank}(T) = 1$.


### Example 2.8.E8 — PCA Interpretation of SVD

Given a data matrix $X \in \mathbb{R}^{m \times n}$ (each of the $m$ rows is a data point in $\mathbb{R}^n$), center it: $\bar{X} = X - \mathbf{1}\mu^\top$ where $\mu$ is the column mean vector. Compute $\bar{X} = U\Sigma V^\top$.

- The **columns of $V$** (right singular vectors) are the **principal components** — the directions of maximum variance in $\mathbb{R}^n$.
- The **singular values** squared, $\sigma_i^2/(m-1)$, are the **variances** along each principal component.
- The **scores** $\bar{X}V$ give the data projected onto principal components.
- The rank-$k$ truncation $U_k \Sigma_k V_k^\top$ is the best rank-$k$ reconstruction of the centered data.

---

## ⚠️ 6. Common Pitfalls

**Pitfall 1 — Confusing $U$ (left) and $V$ (right).**
$U$ diagonalizes $AA^\top$ (acts in the output space $\mathbb{R}^m$); $V$ diagonalizes $A^\top A$ (acts in the input space $\mathbb{R}^n$). The columns of $V$ are the **right** singular vectors — they align the input so $A$ stretches along coordinate axes. Get them swapped and every subsequent formula is wrong.

**Pitfall 2 — Singular values are always non-negative.**
$\sigma_i = \sqrt{\lambda_i(A^\top A)} \geq 0$ by definition. If you're finding "negative singular values" you have made a sign error somewhere — probably in taking square roots of eigenvalues or in negating a component of a singular vector.

**Pitfall 3 — SVD ≠ eigendecomposition for non-symmetric matrices.**
For a symmetric positive definite matrix, the SVD and eigendecomposition coincide ($U = V = Q$, singular values = eigenvalues). For a general matrix, eigenvalues can be complex but singular values are always real and non-negative. Don't conflate the two for e.g. a rotation matrix: its eigenvalues are $e^{\pm i\theta}$ (complex) but its singular values are all 1.

**Pitfall 4 — Einstein summation: repeated indices must be one up, one down.**
Writing $A^i{}_j B^i{}_k$ is **not** a valid contraction: the $i$ index is up in both, so it's ambiguous. The correct form for matrix multiplication is $A^i{}_j B^j{}_k$ (one up, one down). Mixing conventions without care leads to nonsense.

**Pitfall 5 — The metric tensor and the Kronecker delta are only equal in Cartesian coordinates.**
In curvilinear coordinates (polar, spherical, general relativistic), $g_{ij} \neq \delta_{ij}$. Forgetting this when computing norms in curvilinear systems is the source of many errors in physics problems.

---

## 📝 7. Challenge Problems

### Problem 2.8.P1

Compute the SVD of $A = \begin{pmatrix}3&4\\0&0\end{pmatrix}$ by hand. Identify the column space, row space, and nullspace from $U$ and $V$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Step 1.** $A^\top A = \begin{pmatrix}3&0\\4&0\end{pmatrix}\begin{pmatrix}3&4\\0&0\end{pmatrix} = \begin{pmatrix}9&12\\12&16\end{pmatrix}$.

**Step 2.** Eigenvalues: $\det(A^\top A - \lambda I) = (9-\lambda)(16-\lambda) - 144 = \lambda^2 - 25\lambda = \lambda(\lambda-25) = 0$.

$\lambda_1 = 25$, $\lambda_2 = 0$. So $\sigma_1 = 5$, $\sigma_2 = 0$. Rank = 1.

**Step 3.** Right singular vectors:
- $\lambda_1 = 25$: $(A^\top A - 25I)v = 0 \Rightarrow \begin{pmatrix}-16&12\\12&-9\end{pmatrix}v = 0 \Rightarrow v_1 = \frac{1}{5}\begin{pmatrix}3\\4\end{pmatrix}$.
- $\lambda_2 = 0$: $v_2 = \frac{1}{5}\begin{pmatrix}-4\\3\end{pmatrix}$ (orthogonal complement).

**Step 4.** Left singular vector: $u_1 = Av_1/\sigma_1 = \frac{1}{5}\begin{pmatrix}3&4\\0&0\end{pmatrix}\begin{pmatrix}3/5\\4/5\end{pmatrix} = \frac{1}{5}\begin{pmatrix}5\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$.

Extend: $u_2 = (0,1)^\top$.

**Result:**

$$
U = I_2, \quad \Sigma = \begin{pmatrix}5&0\\0&0\end{pmatrix}, \quad V = \frac{1}{5}\begin{pmatrix}3&-4\\4&3\end{pmatrix}.
$$

**Subspaces:** $C(A) = \text{span}\{u_1\} = \text{span}\{e_1\}$; $N(A^\top) = \text{span}\{u_2\} = \text{span}\{e_2\}$; Row space $= \text{span}\{v_1\}$; $N(A) = \text{span}\{v_2\}$.

</details>

### Problem 2.8.P2

Show that $\|A\|_F^2 = \sigma_1^2 + \sigma_2^2 + \cdots + \sigma_r^2$ (the Frobenius norm equals the sum of squared singular values).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Use $\|A\|_F^2 = \text{tr}(A^\top A)$ (expand: $\|A\|_F^2 = \sum_{i,j} A_{ij}^2 = \sum_i (A^\top A)_{ii} = \text{tr}(A^\top A)$).

From the spectral theorem, $\text{tr}(A^\top A) = \sum_i \lambda_i(A^\top A) = \sum_i \sigma_i^2$. $\blacksquare$

</details>

### Problem 2.8.P3

For $A = U\Sigma V^\top$, prove that $A^+ A$ is the orthogonal projector onto $C(A^\top)$ (the row space of $A$).

<details>
<summary>🔍 View Step-by-Step Solution</summary>

$A^+ = V\Sigma^+ U^\top$. Compute:

$$
A^+ A = V\Sigma^+ U^\top U\Sigma V^\top = V \Sigma^+ \Sigma V^\top.
$$

$\Sigma^+\Sigma = \text{diag}(1,\ldots,1,0,\ldots,0)$ with $r$ ones (where $r$ = rank). So $A^+ A = V \begin{pmatrix}I_r & 0 \\ 0 & 0\end{pmatrix} V^\top$.

This is an orthogonal projector (idempotent + symmetric) onto the span of the first $r$ columns of $V$, which is the row space $C(A^\top)$. $\blacksquare$

</details>

### Problem 2.8.P4

Prove that $A^\top A$ is symmetric positive semidefinite for any $A \in \mathbb{R}^{m \times n}$.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

**Symmetric:** $(A^\top A)^\top = A^\top (A^\top)^\top = A^\top A$. ✓

**Positive semidefinite:** For any $\mathbf{x} \in \mathbb{R}^n$:

$$
\mathbf{x}^\top (A^\top A)\mathbf{x} = (A\mathbf{x})^\top (A\mathbf{x}) = \|A\mathbf{x}\|^2 \geq 0.
$$

So all eigenvalues are $\geq 0$. $\blacksquare$

</details>

### Problem 2.8.P5

Show that the Einstein summation $T^{ij}v_i w_j$ (with $T$ a $(0,2)$-tensor and $v,w$ vectors) defines a bilinear form.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

Fix $w$. Define $f(v) = T^{ij}v_i w_j$. For scalars $a,b$ and vectors $v, u$:

$$
f(av + bu) = T^{ij}(av_i + bu_i)w_j = a T^{ij}v_i w_j + b T^{ij}u_i w_j = af(v) + bf(u).
$$

So $f$ is linear in $v$. By symmetry of the argument, it is also linear in $w$. Hence the map $(v,w) \mapsto T^{ij}v_i w_j$ is bilinear. $\blacksquare$

Note: this is the general notion that a $(0,2)$-tensor *is* a bilinear form. The metric tensor $g_{ij}$ is the bilinear form that defines the inner product.

</details>

### Problem 2.8.P6

Express the formula for the Riemann curvature tensor components $R^\rho{}_{\sigma\mu\nu}$ in terms of Christoffel symbols $\Gamma^\rho_{\mu\nu}$, and identify its tensor type.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

The Riemann tensor is a **(1,3)-tensor** — one contravariant index, three covariant. Its components are:

$$
R^\rho{}_{\sigma\mu\nu} = \partial_\mu \Gamma^\rho_{\nu\sigma} - \partial_\nu \Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}.
$$

Here $\partial_\mu \equiv \partial/\partial x^\mu$. The Einstein summation convention applies to the repeated $\lambda$ index in the last two terms ($\lambda$ appears once up, once down).

**Why (1,3)?** The curvature "eats" three vectors (one direction to differentiate in, one to apply the covariant derivative to, one to commute) and outputs a vector — hence one upper, three lower indices.

**Connection to Ch. 1.8:** Antisymmetrizing $R^\rho{}_{\sigma\mu\nu}$ in $\mu,\nu$ (which is automatic since $R^\rho{}_{\sigma\mu\nu} = -R^\rho{}_{\sigma\nu\mu}$) makes the $[\mu\nu]$ pair behave like a 2-form, connecting to the differential forms of Ch. 1.8.

</details>

### Problem 2.8.P7

For the stress tensor $\sigma_{ij}$ (a symmetric $(0,2)$-tensor in mechanics), write the traction vector $t^i = \sigma^{ij}n_j$ using the metric to raise an index, and explain the physical meaning.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

In Cartesian coordinates ($g_{ij} = \delta_{ij}$), raising/lowering indices doesn't change components: $\sigma^{ij} = g^{ik}g^{j\ell}\sigma_{k\ell} = \sigma_{ij}$.

So $t^i = \sigma^{ij}n_j = \sum_j \sigma_{ij}n_j$, which in matrix form is $\mathbf{t} = \boldsymbol{\sigma}\mathbf{n}$.

**Physical meaning:** $n_j$ is the unit normal to a surface element. $t^i$ is the **traction vector** — the force per unit area acting on that surface. The stress tensor $\sigma_{ij}$ maps surface normals to traction forces; it encodes the full internal force state at a point in a continuum.

The symmetry $\sigma_{ij} = \sigma_{ji}$ (from angular momentum balance) means the stress tensor has only 6 independent components in 3D.

</details>

### Problem 2.8.P8

Show that the $k$-th exterior product $\omega = dx^{i_1} \wedge \cdots \wedge dx^{i_k}$ is an antisymmetric covariant tensor of type $(0,k)$, and compute its component count.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

A **$k$-form** $\omega$ is a $(0,k)$-tensor that is totally antisymmetric under permutation of its indices:

$$
\omega_{i_1 \cdots i_k} = \text{sgn}(\pi)\, \omega_{i_{\pi(1)} \cdots i_{\pi(k)}}
$$

for any permutation $\pi \in S_k$. In particular, $\omega_{ij} = -\omega_{ji}$ (swapping two indices reverses the sign).

The wedge product enforces antisymmetrization:

$$
(dx^i \wedge dx^j)(v,w) = dx^i(v)\,dx^j(w) - dx^i(w)\,dx^j(v),
$$

which is precisely the antisymmetrization of the tensor $dx^i \otimes dx^j$.

**Type:** $(0,k)$ — all $k$ indices are covariant (lower), and the tensor eats $k$ vectors and returns a scalar. ✓

**Component count:** In $n$ dimensions, a totally antisymmetric $(0,k)$-tensor has $\binom{n}{k}$ independent components (each distinct ordered subset of $k$ indices from $\{1,\ldots,n\}$, with sign, reduces to the $\binom{n}{k}$ unordered subsets). For $k=n$, there is exactly 1 independent component — the volume form. This connects directly to the determinant: $\det(A) = \varepsilon_{i_1\cdots i_n}A^{i_1}{}_1 \cdots A^{i_n}{}_n$ where $\varepsilon$ is the Levi-Civita tensor (the unique antisymmetric $(0,n)$-tensor up to scale).

</details>


---

## 🔗 8. Connections

**← Chapter 2.6 (Eigenvalues):** The spectral theorem for symmetric matrices is the engine behind the SVD — we eigendecompose $A^\top A$ to get $V$. For symmetric $A$, SVD and eigendecomposition coincide.

**← Chapter 2.7 (Inner Products & QR):** The orthogonal matrices $U$ and $V$ in the SVD are products of the Gram-Schmidt process applied to the singular vectors. The QR decomposition is a "half-SVD" (orthogonal times triangular, not orthogonal times diagonal times orthogonal).

**← Chapter 1.8 (Differential Forms):** The antisymmetric covariant tensors of Chapter 1.8 are precisely the $(0,k)$-tensors with full antisymmetry. The exterior derivative $d$ and the wedge product $\wedge$ are tensor operations. The Hodge star relates $k$-forms to $(n-k)$-forms using the metric tensor.

**→ Chapter 3 (PDEs):** The tensor formalism becomes essential: the wave equation in curvilinear coordinates requires the metric $g^{ij}\partial_i\partial_j\phi$; elasticity theory requires the strain and stress tensors.

**→ Chapter 8 (General Relativity):** The Riemann curvature tensor $R^\rho{}_{\sigma\mu\nu}$, the Ricci tensor $R_{\mu\nu} = R^\rho{}_{\mu\rho\nu}$ (a contraction), and the Einstein tensor $G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R$ are all tensors. The field equation $G_{\mu\nu} = 8\pi T_{\mu\nu}$ is a tensorial equality — the Einstein summation convention makes it compact.

**→ Chapter 9 (Quantum Mechanics):** The density matrix $\rho = |\psi\rangle\langle\psi|$ is an outer product (rank-1 $(1,1)$-tensor). Mixed states are convex combinations. The SVD of the coefficient matrix of a bipartite state gives the **Schmidt decomposition** — the quantum analogue of low-rank approximation.

---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

---
title: "Hilbert Space Bra Ket Formalism"
subject: "Quantum Mechanics & Quantum Field Theory"
catalog: advanced
audience_tier: higher-education
chapter: "9.2"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [07 - Math and Physics Index](07---Math-and-Physics-Index)*

# 9.2 — Hilbert Space & Bra-Ket Formalism

> *"The mathematics of quantum mechanics is the mathematics of infinite-dimensional vector spaces — Hilbert spaces — and the linear operators that act on them."* — Paul Dirac

Chapter 9.1 developed quantum mechanics in the "wave function" representation — states as functions $\Psi(x)$, operators as differential operators. But this is merely one **representation** of a deeper algebraic structure. Dirac's bra-ket notation abstracts away the representation entirely: a quantum state is a vector $\vert\psi\rangle$ in a Hilbert space, and observables are Hermitian operators acting on that space. This chapter builds the full abstract machinery — dual spaces, completeness relations, change of basis, tensor products — that makes quantum mechanics representation-independent and prepares the ground for spin, multi-particle systems, and quantum field theory.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define a Hilbert space and verify the axioms (completeness, inner product, separability).
2. Write quantum states in Dirac notation and manipulate bras, kets, and operators algebraically.
3. Compute inner products, outer products, and projection operators.
4. State and apply the completeness relation (resolution of the identity).
5. Transform between position, momentum, and energy representations.
6. Distinguish Hermitian, unitary, and normal operators and prove their spectral properties.
7. Construct tensor product spaces for composite systems.

---

## 🖼️ Visual Anchor — Hilbert Space & Bra-Ket Structure

![math-09__9.2-fig1](math-09__9.2-fig1.svg)

---

## 📚 1. Definitions

### Definition 9.2.1 — Hilbert Space

A **Hilbert space** $\mathcal{H}$ is a complete inner product space over $\mathbb{C}$. Specifically, it is a complex vector space equipped with an inner product $\langle\cdot|\cdot\rangle : \mathcal{H} \times \mathcal{H} \to \mathbb{C}$ satisfying:

1. **Conjugate symmetry:** $\langle\phi\vert\psi\rangle = \overline{\langle\psi\vert\phi\rangle}$
2. **Linearity in the second argument:** $\langle\phi\vert\alpha\psi_1 + \beta\psi_2\rangle = \alpha\langle\phi\vert\psi_1\rangle + \beta\langle\phi\vert\psi_2\rangle$
3. **Positive definiteness:** $\langle\psi\vert\psi\rangle \geq 0$, with equality iff $\vert\psi\rangle = 0$
4. **Completeness:** Every Cauchy sequence in $\mathcal{H}$ converges to an element of $\mathcal{H}$

In quantum mechanics, the relevant Hilbert space is $L^2(\mathbb{R})$ — the space of square-integrable functions — with inner product:

$$
\langle\phi\vert\psi\rangle = \int_{-\infty}^{\infty} \phi^*(x)\psi(x)\,dx.
$$

### Definition 9.2.2 — Ket Vector

A **ket** $\vert\psi\rangle$ is an element of the Hilbert space $\mathcal{H}$. It represents a quantum state. In the position representation:

$$
\vert\psi\rangle \longleftrightarrow \psi(x) = \langle x\vert\psi\rangle.
$$

### Definition 9.2.3 — Bra Vector (Dual Space)

A **bra** $\langle\psi\vert$ is an element of the dual space $\mathcal{H}^*$ — the space of continuous linear functionals on $\mathcal{H}$. It is defined by the Riesz representation theorem: for every $\vert\psi\rangle \in \mathcal{H}$, there exists a unique $\langle\psi\vert \in \mathcal{H}^*$ such that:

$$
\langle\psi\vert(\vert\phi\rangle) = \langle\psi\vert\phi\rangle.
$$

The bra is the Hermitian conjugate (adjoint) of the ket: $\langle\psi\vert = (\vert\psi\rangle)^\dagger$.

### Definition 9.2.4 — Inner Product (Bracket)

The **bracket** $\langle\phi\vert\psi\rangle \in \mathbb{C}$ is the inner product of two states. Properties:

$$
\langle\phi\vert\psi\rangle = \overline{\langle\psi\vert\phi\rangle}, \qquad \langle\psi\vert\psi\rangle = \|\psi\|^2 \geq 0.
$$

### Definition 9.2.5 — Outer Product (Operator)

The **outer product** $\vert\phi\rangle\langle\psi\vert$ is a linear operator that maps kets to kets:

$$
(\vert\phi\rangle\langle\psi\vert)\vert\chi\rangle = \vert\phi\rangle\langle\psi\vert\chi\rangle = (\langle\psi\vert\chi\rangle)\vert\phi\rangle.
$$

### Definition 9.2.6 — Hermitian (Self-Adjoint) Operator

An operator $\hat{A}$ is **Hermitian** if $\hat{A}^\dagger = \hat{A}$, i.e.:

$$
\langle\phi\vert\hat{A}\vert\psi\rangle = \langle\hat{A}\phi\vert\psi\rangle \quad \forall\,\vert\phi\rangle, \vert\psi\rangle \in \mathcal{H}.
$$

Equivalently, in matrix representation: $(A^\dagger)_{ij} = \overline{A_{ji}} = A_{ij}$.

Hermitian operators represent **physical observables**. Their eigenvalues are real.

### Definition 9.2.7 — Unitary Operator

An operator $\hat{U}$ is **unitary** if $\hat{U}^\dagger\hat{U} = \hat{U}\hat{U}^\dagger = \hat{I}$. Unitary operators:
- Preserve inner products: $\langle U\phi\vert U\psi\rangle = \langle\phi\vert\psi\rangle$
- Preserve norms (probabilities)
- Represent symmetry transformations and time evolution: $\hat{U}(t) = e^{-i\hat{H}t/\hbar}$

### Definition 9.2.8 — Projection Operator

The **projection operator** onto state $\vert n\rangle$ is:

$$
\hat{P}_n = \vert n\rangle\langle n\vert.
$$

Properties: $\hat{P}_n^2 = \hat{P}_n$ (idempotent), $\hat{P}_n^\dagger = \hat{P}_n$ (Hermitian), $\hat{P}_m\hat{P}_n = \delta_{mn}\hat{P}_n$.

### Definition 9.2.9 — Completeness Relation (Resolution of the Identity)

For a complete orthonormal basis $\{\vert n\rangle\}$ of $\mathcal{H}$:

$$
\sum_n \vert n\rangle\langle n\vert = \hat{I} \quad \text{(discrete spectrum)},
$$

$$
\int \vert x\rangle\langle x\vert\,dx = \hat{I} \quad \text{(continuous spectrum)}.
$$

### Definition 9.2.10 — Tensor Product Space

For two systems with Hilbert spaces $\mathcal{H}_A$ and $\mathcal{H}_B$, the composite system lives in:

$$
\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B.
$$

If $\{\vert i\rangle_A\}$ and $\{\vert j\rangle_B\}$ are bases, then $\{\vert i\rangle_A \otimes \vert j\rangle_B\}$ is a basis for $\mathcal{H}_{AB}$ with $\dim(\mathcal{H}_{AB}) = \dim(\mathcal{H}_A) \cdot \dim(\mathcal{H}_B)$.

### Definition 9.2.11 — Trace of an Operator

The **trace** of operator $\hat{A}$ is:

$$
\operatorname{Tr}(\hat{A}) = \sum_n \langle n\vert\hat{A}\vert n\rangle,
$$

where $\{\vert n\rangle\}$ is any complete orthonormal basis. The trace is basis-independent (cyclic property: $\operatorname{Tr}(\hat{A}\hat{B}) = \operatorname{Tr}(\hat{B}\hat{A})$).




---

## 📐 2. Axioms / Postulates

### Postulate 9.2.P1 — State Space

The state of a quantum system is represented by a unit vector (ray) in a complex Hilbert space $\mathcal{H}$:

$$
\vert\psi\rangle \in \mathcal{H}, \quad \langle\psi\vert\psi\rangle = 1.
$$

Two vectors differing by a global phase $e^{i\alpha}\vert\psi\rangle$ represent the same physical state.

### Postulate 9.2.P2 — Observables

Every measurable physical quantity $A$ is associated with a Hermitian operator $\hat{A}$ acting on $\mathcal{H}$. The possible measurement outcomes are the eigenvalues of $\hat{A}$.

### Postulate 9.2.P3 — Measurement Probability

If the system is in state $\vert\psi\rangle$ and we measure observable $\hat{A}$ with eigenvalue $a_n$ and eigenstate $\vert a_n\rangle$, the probability of obtaining $a_n$ is:

$$
P(a_n) = |\langle a_n\vert\psi\rangle|^2.
$$

For degenerate eigenvalues with eigenspace spanned by $\{\vert a_n^{(i)}\rangle\}$:

$$
P(a_n) = \sum_i |\langle a_n^{(i)}\vert\psi\rangle|^2.
$$

### Postulate 9.2.P4 — State Collapse

Immediately after a measurement yielding $a_n$, the state collapses to:

$$
\vert\psi\rangle \to \frac{\hat{P}_n\vert\psi\rangle}{\sqrt{\langle\psi\vert\hat{P}_n\vert\psi\rangle}}, \quad \hat{P}_n = \sum_i \vert a_n^{(i)}\rangle\langle a_n^{(i)}\vert.
$$

### Postulate 9.2.P5 — Time Evolution

The state evolves unitarily:

$$
\vert\psi(t)\rangle = \hat{U}(t,t_0)\vert\psi(t_0)\rangle, \quad \hat{U}(t,t_0) = e^{-i\hat{H}(t-t_0)/\hbar},
$$

where $\hat{H}$ is the Hamiltonian (time-independent case). This is equivalent to the Schrödinger equation $i\hbar\frac{d}{dt}\vert\psi\rangle = \hat{H}\vert\psi\rangle$.

### Postulate 9.2.P6 — Composite Systems

The state space of a composite system is the tensor product of the component state spaces:

$$
\mathcal{H}_{\text{total}} = \mathcal{H}_1 \otimes \mathcal{H}_2 \otimes \cdots \otimes \mathcal{H}_N.
$$

---

## 🛡️ 3. Lemmas

### Lemma 9.2.1 — Eigenvalues of Hermitian Operators Are Real

**Statement:** If $\hat{A} = \hat{A}^\dagger$ and $\hat{A}\vert a\rangle = a\vert a\rangle$, then $a \in \mathbb{R}$.

**Proof.**

$$
\langle a\vert\hat{A}\vert a\rangle = a\langle a\vert a\rangle = a.
$$

Taking the Hermitian conjugate of $\hat{A}\vert a\rangle = a\vert a\rangle$:

$$
\langle a\vert\hat{A}^\dagger = \langle a\vert a^* \implies \langle a\vert\hat{A} = a^*\langle a\vert.
$$

Therefore:

$$
\langle a\vert\hat{A}\vert a\rangle = a^*\langle a\vert a\rangle = a^*.
$$

Comparing: $a = a^*$, so $a \in \mathbb{R}$. $\blacksquare$

### Lemma 9.2.2 — Eigenvectors of Hermitian Operators for Distinct Eigenvalues Are Orthogonal

**Statement:** If $\hat{A}\vert a\rangle = a\vert a\rangle$ and $\hat{A}\vert b\rangle = b\vert b\rangle$ with $a \neq b$, then $\langle a\vert b\rangle = 0$.

**Proof.**

$$
\langle a\vert\hat{A}\vert b\rangle = b\langle a\vert b\rangle.
$$

Also (using Hermiticity and Lemma 9.2.1):

$$
\langle a\vert\hat{A}\vert b\rangle = (\hat{A}\vert a\rangle)^\dagger\vert b\rangle = a^*\langle a\vert b\rangle = a\langle a\vert b\rangle.
$$

Subtracting: $(a - b)\langle a\vert b\rangle = 0$. Since $a \neq b$: $\langle a\vert b\rangle = 0$. $\blacksquare$

### Lemma 9.2.3 — Unitary Operators Preserve Inner Products

**Statement:** If $\hat{U}^\dagger\hat{U} = \hat{I}$, then $\langle U\phi\vert U\psi\rangle = \langle\phi\vert\psi\rangle$.

**Proof.**

$$
\langle U\phi\vert U\psi\rangle = \langle\phi\vert\hat{U}^\dagger\hat{U}\vert\psi\rangle = \langle\phi\vert\hat{I}\vert\psi\rangle = \langle\phi\vert\psi\rangle. \quad \blacksquare
$$

### Lemma 9.2.4 — Eigenvalues of Unitary Operators Have Unit Modulus

**Statement:** If $\hat{U}\vert u\rangle = \lambda\vert u\rangle$ with $\hat{U}^\dagger\hat{U} = \hat{I}$, then $|\lambda| = 1$.

**Proof.**

$$
\langle u\vert\hat{U}^\dagger\hat{U}\vert u\rangle = \langle u\vert u\rangle = 1.
$$

But also:

$$
\langle u\vert\hat{U}^\dagger\hat{U}\vert u\rangle = (\hat{U}\vert u\rangle)^\dagger(\hat{U}\vert u\rangle) = |\lambda|^2\langle u\vert u\rangle = |\lambda|^2.
$$

Therefore $|\lambda|^2 = 1$, so $|\lambda| = 1$, meaning $\lambda = e^{i\theta}$ for some real $\theta$. $\blacksquare$

### Lemma 9.2.5 — The Trace is Basis-Independent

**Statement:** $\operatorname{Tr}(\hat{A}) = \sum_n \langle n\vert\hat{A}\vert n\rangle$ is the same for any orthonormal basis $\{\vert n\rangle\}$.

**Proof.** Let $\{\vert n\rangle\}$ and $\{\vert m'\rangle\}$ be two orthonormal bases. Insert the completeness relation:

$$
\sum_n \langle n\vert\hat{A}\vert n\rangle = \sum_n \sum_{m'} \langle n\vert m'\rangle\langle m'\vert\hat{A}\vert n\rangle = \sum_{m'} \sum_n \langle m'\vert\hat{A}\vert n\rangle\langle n\vert m'\rangle.
$$

Using completeness $\sum_n \vert n\rangle\langle n\vert = \hat{I}$:

$$
= \sum_{m'} \langle m'\vert\hat{A}\vert m'\rangle. \quad \blacksquare
$$

### Lemma 9.2.6 — Cyclic Property of the Trace

**Statement:** $\operatorname{Tr}(\hat{A}\hat{B}\hat{C}) = \operatorname{Tr}(\hat{C}\hat{A}\hat{B}) = \operatorname{Tr}(\hat{B}\hat{C}\hat{A})$.

**Proof.**

$$
\operatorname{Tr}(\hat{A}\hat{B}\hat{C}) = \sum_n \langle n\vert\hat{A}\hat{B}\hat{C}\vert n\rangle.
$$

Insert $\hat{I} = \sum_m \vert m\rangle\langle m\vert$ between $\hat{C}$ and $\vert n\rangle$... actually, more directly:

$$
\operatorname{Tr}(\hat{A}\hat{B}\hat{C}) = \sum_n \langle n\vert\hat{A}\hat{B}\hat{C}\vert n\rangle = \sum_n \langle n\vert\hat{A}\hat{B}\hat{C}\vert n\rangle.
$$

Insert $\hat{I} = \sum_m\vert m\rangle\langle m\vert$ after $\hat{C}$:

Wait — let's use the two-operator case first. $\operatorname{Tr}(\hat{A}\hat{B}) = \sum_n\langle n\vert\hat{A}\hat{B}\vert n\rangle$. Insert $\hat{I}$:

$$
= \sum_n\sum_m \langle n\vert\hat{A}\vert m\rangle\langle m\vert\hat{B}\vert n\rangle = \sum_m\sum_n \langle m\vert\hat{B}\vert n\rangle\langle n\vert\hat{A}\vert m\rangle = \sum_m \langle m\vert\hat{B}\hat{A}\vert m\rangle = \operatorname{Tr}(\hat{B}\hat{A}).
$$

For three operators: $\operatorname{Tr}(\hat{A}\hat{B}\hat{C}) = \operatorname{Tr}((\hat{A}\hat{B})\hat{C}) = \operatorname{Tr}(\hat{C}(\hat{A}\hat{B})) = \operatorname{Tr}(\hat{C}\hat{A}\hat{B})$. $\blacksquare$

### Lemma 9.2.7 — Position-Momentum Representation Connection

**Statement:** The position eigenstate in momentum representation is:

$$
\langle p\vert x\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{-ipx/\hbar}.
$$

**Proof.** The momentum operator in position space is $\hat{p} = -i\hbar\frac{d}{dx}$. The eigenvalue equation $\hat{p}\vert p\rangle = p\vert p\rangle$ in position representation:

$$
-i\hbar\frac{d}{dx}\langle x\vert p\rangle = p\langle x\vert p\rangle.
$$

This is a first-order ODE with solution:

$$
\langle x\vert p\rangle = Ce^{ipx/\hbar}.
$$

Normalization with the Dirac delta: $\langle p\vert p'\rangle = \delta(p - p')$:

$$
\int_{-\infty}^{\infty}\langle p\vert x\rangle\langle x\vert p'\rangle\,dx = |C|^2\int_{-\infty}^{\infty} e^{i(p'-p)x/\hbar}\,dx = |C|^2 \cdot 2\pi\hbar\,\delta(p-p').
$$

Therefore $|C|^2 = \frac{1}{2\pi\hbar}$, giving $C = \frac{1}{\sqrt{2\pi\hbar}}$.

Thus $\langle x\vert p\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}$ and $\langle p\vert x\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{-ipx/\hbar}$. $\blacksquare$




---

## 👑 4. Theorems

### Theorem 9.2.1 — Spectral Theorem for Hermitian Operators

Every Hermitian operator $\hat{A}$ on a finite-dimensional Hilbert space admits a spectral decomposition:

$$
\hat{A} = \sum_n a_n \vert a_n\rangle\langle a_n\vert,
$$

where $\{a_n\}$ are the real eigenvalues and $\{\vert a_n\rangle\}$ form a complete orthonormal eigenbasis. For degenerate eigenvalues, the projector onto the eigenspace replaces the rank-1 projector.

### Theorem 9.2.2 — Stone's Theorem (Unitary Groups from Hermitian Generators)

Every strongly continuous one-parameter unitary group $\hat{U}(t) = e^{-i\hat{A}t}$ has a unique self-adjoint generator $\hat{A}$. Conversely, every self-adjoint operator generates a one-parameter unitary group.

**Physical significance:** Time evolution $\hat{U}(t) = e^{-i\hat{H}t/\hbar}$ is generated by the Hamiltonian. Spatial translations are generated by momentum. Rotations are generated by angular momentum.

### Theorem 9.2.3 — The Riesz Representation Theorem

For every continuous linear functional $f : \mathcal{H} \to \mathbb{C}$ on a Hilbert space, there exists a unique $\vert\phi\rangle \in \mathcal{H}$ such that:

$$
f(\vert\psi\rangle) = \langle\phi\vert\psi\rangle \quad \forall\,\vert\psi\rangle \in \mathcal{H}.
$$

This theorem justifies the bra-ket correspondence: every bra $\langle\phi\vert$ corresponds to exactly one ket $\vert\phi\rangle$.

### Theorem 9.2.4 — Completeness and Expansion

Any state $\vert\psi\rangle \in \mathcal{H}$ can be expanded in any complete orthonormal basis $\{\vert n\rangle\}$:

$$
\vert\psi\rangle = \sum_n c_n\vert n\rangle, \quad c_n = \langle n\vert\psi\rangle, \quad \sum_n |c_n|^2 = 1.
$$

The coefficients $c_n$ are the **probability amplitudes**: $P(n) = |c_n|^2$.

### Theorem 9.2.5 — Simultaneous Diagonalizability

Two Hermitian operators $\hat{A}$ and $\hat{B}$ can be simultaneously diagonalized (share a common eigenbasis) if and only if they commute:

$$
[\hat{A}, \hat{B}] = 0 \iff \exists \text{ a basis of simultaneous eigenstates of } \hat{A} \text{ and } \hat{B}.
$$

### Theorem 9.2.6 — No-Cloning Theorem

There exists no unitary operator $\hat{U}$ acting on $\mathcal{H} \otimes \mathcal{H}$ such that for all $\vert\psi\rangle$:

$$
\hat{U}(\vert\psi\rangle \otimes \vert 0\rangle) = \vert\psi\rangle \otimes \vert\psi\rangle.
$$

---

## ✍️ 5. Proofs / Derivations

### 5.1 Proof of the Spectral Theorem (Finite-Dimensional Case)

**Setup:** Let $\hat{A}$ be Hermitian on $\mathcal{H}$ with $\dim\mathcal{H} = n$.

**Step 1:** By Lemma 9.2.1, all eigenvalues are real. By the fundamental theorem of algebra applied to the characteristic polynomial $\det(\hat{A} - \lambda\hat{I}) = 0$, there exist $n$ eigenvalues (counting multiplicity) over $\mathbb{C}$, but since they're all real, we have $n$ real eigenvalues.

**Step 2:** By Lemma 9.2.2, eigenvectors for distinct eigenvalues are orthogonal. Within each degenerate eigenspace, apply Gram-Schmidt to obtain an orthonormal set.

**Step 3:** The resulting set $\{\vert a_1\rangle, \ldots, \vert a_n\rangle\}$ is orthonormal and spans $\mathcal{H}$ (since we have $n$ vectors in an $n$-dimensional space). Therefore it is a complete orthonormal basis.

**Step 4:** Express $\hat{A}$ in this basis:

$$
\hat{A} = \hat{I}\hat{A}\hat{I} = \left(\sum_i \vert a_i\rangle\langle a_i\vert\right)\hat{A}\left(\sum_j \vert a_j\rangle\langle a_j\vert\right) = \sum_{i,j}\vert a_i\rangle\langle a_i\vert\hat{A}\vert a_j\rangle\langle a_j\vert.
$$

Since $\langle a_i\vert\hat{A}\vert a_j\rangle = a_j\langle a_i\vert a_j\rangle = a_j\delta_{ij}$:

$$
\hat{A} = \sum_i a_i\vert a_i\rangle\langle a_i\vert. \quad \blacksquare
$$

### 5.2 Derivation of the Position-Space Wave Function from Bra-Ket

**Goal:** Show that $\psi(x) = \langle x\vert\psi\rangle$ reproduces all of wave mechanics.

**Step 1:** Insert the position completeness relation into the norm:

$$
\langle\psi\vert\psi\rangle = \langle\psi\vert\hat{I}\vert\psi\rangle = \int dx\,\langle\psi\vert x\rangle\langle x\vert\psi\rangle = \int dx\,\psi^*(x)\psi(x) = \int |\psi(x)|^2\,dx.
$$

This is the normalization condition of Chapter 9.1. ✓

**Step 2:** The expectation value of $\hat{x}$:

$$
\langle\hat{x}\rangle = \langle\psi\vert\hat{x}\vert\psi\rangle = \int dx\,\langle\psi\vert x\rangle\langle x\vert\hat{x}\vert\psi\rangle.
$$

Since $\hat{x}\vert x\rangle = x\vert x\rangle$, we have $\langle x\vert\hat{x}\vert\psi\rangle = x\langle x\vert\psi\rangle = x\psi(x)$:

$$
\langle\hat{x}\rangle = \int dx\,x\,|\psi(x)|^2. \quad \checkmark
$$

**Step 3:** The momentum operator in position representation. Using $\langle x\vert\hat{p}\vert\psi\rangle$:

Insert momentum completeness: $\hat{I} = \int dp\,\vert p\rangle\langle p\vert$:

$$
\langle x\vert\hat{p}\vert\psi\rangle = \int dp\,\langle x\vert\hat{p}\vert p\rangle\langle p\vert\psi\rangle = \int dp\,p\langle x\vert p\rangle\langle p\vert\psi\rangle.
$$

Using $\langle x\vert p\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}$:

$$
= \int dp\,p\cdot\frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}\tilde{\psi}(p).
$$

But also, $-i\hbar\frac{\partial}{\partial x}\langle x\vert p\rangle = -i\hbar\cdot\frac{ip}{\hbar}\cdot\frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar} = p\langle x\vert p\rangle$.

Therefore:

$$
\langle x\vert\hat{p}\vert\psi\rangle = -i\hbar\frac{\partial}{\partial x}\int dp\,\langle x\vert p\rangle\langle p\vert\psi\rangle = -i\hbar\frac{\partial}{\partial x}\langle x\vert\psi\rangle = -i\hbar\frac{\partial\psi}{\partial x}.
$$

This recovers the position-space momentum operator. $\blacksquare$

### 5.3 Proof of the No-Cloning Theorem

**Proof by contradiction.**

**Step 1:** Assume there exists a unitary $\hat{U}$ such that for all states $\vert\psi\rangle$:

$$
\hat{U}(\vert\psi\rangle\otimes\vert 0\rangle) = \vert\psi\rangle\otimes\vert\psi\rangle.
$$

**Step 2:** Apply this to two distinct states $\vert\alpha\rangle$ and $\vert\beta\rangle$:

$$
\hat{U}(\vert\alpha\rangle\otimes\vert 0\rangle) = \vert\alpha\rangle\otimes\vert\alpha\rangle,
$$

$$
\hat{U}(\vert\beta\rangle\otimes\vert 0\rangle) = \vert\beta\rangle\otimes\vert\beta\rangle.
$$

**Step 3:** Take the inner product of these two equations. Since $\hat{U}$ is unitary (preserves inner products):

$$
(\langle\alpha\vert\otimes\langle 0\vert)(\vert\beta\rangle\otimes\vert 0\rangle) = (\langle\alpha\vert\otimes\langle\alpha\vert)(\vert\beta\rangle\otimes\vert\beta\rangle).
$$

**Step 4:** Evaluate both sides:

LHS: $\langle\alpha\vert\beta\rangle\cdot\langle 0\vert 0\rangle = \langle\alpha\vert\beta\rangle$.

RHS: $\langle\alpha\vert\beta\rangle\cdot\langle\alpha\vert\beta\rangle = \langle\alpha\vert\beta\rangle^2$.

**Step 5:** Therefore $\langle\alpha\vert\beta\rangle = \langle\alpha\vert\beta\rangle^2$, which means $\langle\alpha\vert\beta\rangle(1 - \langle\alpha\vert\beta\rangle) = 0$.

This implies either $\langle\alpha\vert\beta\rangle = 0$ (orthogonal) or $\langle\alpha\vert\beta\rangle = 1$ (identical). A universal cloner cannot exist for arbitrary states. $\blacksquare$

### 5.4 Derivation of the Fourier Transform as a Change of Basis

**Goal:** Show that the Fourier transform is simply the change-of-basis matrix between position and momentum representations.

**Step 1:** Any state can be expanded in position eigenstates:

$$
\vert\psi\rangle = \int dx\,\vert x\rangle\langle x\vert\psi\rangle = \int dx\,\psi(x)\vert x\rangle.
$$

**Step 2:** The momentum-space wave function is:

$$
\tilde{\psi}(p) = \langle p\vert\psi\rangle = \int dx\,\langle p\vert x\rangle\langle x\vert\psi\rangle = \int dx\,\frac{1}{\sqrt{2\pi\hbar}}e^{-ipx/\hbar}\psi(x).
$$

This is precisely the Fourier transform (with $\hbar$ conventions).

**Step 3:** The inverse transform:

$$
\psi(x) = \langle x\vert\psi\rangle = \int dp\,\langle x\vert p\rangle\langle p\vert\psi\rangle = \int dp\,\frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}\tilde{\psi}(p).
$$

**Physical interpretation:** The Fourier transform is not a mathematical trick — it is the unitary transformation between two equivalent representations of the same quantum state. The "matrix elements" of this transformation are $\langle x\vert p\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}$. $\blacksquare$

### 5.5 Proof That $[\hat{A}, \hat{B}] = 0$ Implies Simultaneous Eigenstates

**Step 1:** Let $\hat{A}\vert a\rangle = a\vert a\rangle$. We want to show $\hat{B}\vert a\rangle$ is also an eigenvector of $\hat{A}$ with eigenvalue $a$.

**Step 2:** Compute $\hat{A}(\hat{B}\vert a\rangle)$:

$$
\hat{A}(\hat{B}\vert a\rangle) = \hat{A}\hat{B}\vert a\rangle.
$$

Since $[\hat{A},\hat{B}] = 0$, we have $\hat{A}\hat{B} = \hat{B}\hat{A}$:

$$
= \hat{B}\hat{A}\vert a\rangle = \hat{B}(a\vert a\rangle) = a(\hat{B}\vert a\rangle).
$$

**Step 3:** Therefore $\hat{B}\vert a\rangle$ is an eigenvector of $\hat{A}$ with eigenvalue $a$. If $a$ is non-degenerate, then $\hat{B}\vert a\rangle$ must be proportional to $\vert a\rangle$:

$$
\hat{B}\vert a\rangle = b\vert a\rangle,
$$

so $\vert a\rangle$ is simultaneously an eigenstate of both $\hat{A}$ and $\hat{B}$.

**Step 4:** If $a$ is degenerate (eigenspace dimension $> 1$), then $\hat{B}$ maps the eigenspace $E_a$ into itself. We can diagonalize $\hat{B}$ restricted to $E_a$ to find simultaneous eigenstates. $\blacksquare$




---

## 🧮 6. Worked Examples

### Example 9.2.1 — Matrix Representation of Spin-1/2 Operators

**Problem:** A spin-1/2 system has basis states $\vert +\rangle = \vert\uparrow\rangle$ and $\vert -\rangle = \vert\downarrow\rangle$. The spin operators are $\hat{S}_i = \frac{\hbar}{2}\sigma_i$ where $\sigma_i$ are the Pauli matrices. Verify that $[\hat{S}_x, \hat{S}_y] = i\hbar\hat{S}_z$.

**Solution:**

**Step 1:** Write the Pauli matrices:

$$
\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}.
$$

**Step 2:** Compute $\sigma_x\sigma_y$:

$$
\sigma_x\sigma_y = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}\begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix} = \begin{pmatrix} 0\cdot0 + 1\cdot i & 0\cdot(-i) + 1\cdot 0 \\ 1\cdot0 + 0\cdot i & 1\cdot(-i) + 0\cdot 0 \end{pmatrix} = \begin{pmatrix} i & 0 \\ 0 & -i \end{pmatrix} = i\sigma_z.
$$

**Step 3:** Compute $\sigma_y\sigma_x$:

$$
\sigma_y\sigma_x = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 0\cdot0 + (-i)\cdot1 & 0\cdot1 + (-i)\cdot0 \\ i\cdot0 + 0\cdot1 & i\cdot1 + 0\cdot0 \end{pmatrix} = \begin{pmatrix} -i & 0 \\ 0 & i \end{pmatrix} = -i\sigma_z.
$$

**Step 4:** The commutator:

$$
[\sigma_x, \sigma_y] = \sigma_x\sigma_y - \sigma_y\sigma_x = i\sigma_z - (-i\sigma_z) = 2i\sigma_z.
$$

**Step 5:** For the spin operators $\hat{S}_i = \frac{\hbar}{2}\sigma_i$:

$$
[\hat{S}_x, \hat{S}_y] = \frac{\hbar^2}{4}[\sigma_x, \sigma_y] = \frac{\hbar^2}{4}\cdot 2i\sigma_z = \frac{i\hbar^2}{2}\sigma_z = i\hbar\cdot\frac{\hbar}{2}\sigma_z = i\hbar\hat{S}_z. \quad \checkmark
$$

---

### Example 9.2.2 — Expanding a State in an Energy Eigenbasis

**Problem:** A particle in a harmonic oscillator is in the state $\vert\psi\rangle = \frac{1}{\sqrt{3}}\vert 0\rangle + \frac{i}{\sqrt{3}}\vert 1\rangle + \frac{1}{\sqrt{3}}\vert 2\rangle$. Compute: (a) $\langle\hat{H}\rangle$, (b) $\Delta E$, (c) the probability of measuring $E_3 = \frac{7}{2}\hbar\omega$.

**Solution:**

**Step 1:** Verify normalization:

$$
\langle\psi\vert\psi\rangle = \frac{1}{3} + \frac{1}{3} + \frac{1}{3} = 1. \quad \checkmark
$$

**Step 2 (a):** The harmonic oscillator energies are $E_n = (n + \frac{1}{2})\hbar\omega$. The expectation value:

$$
\langle\hat{H}\rangle = \sum_n |c_n|^2 E_n = \frac{1}{3}\cdot\frac{\hbar\omega}{2} + \frac{1}{3}\cdot\frac{3\hbar\omega}{2} + \frac{1}{3}\cdot\frac{5\hbar\omega}{2}.
$$

$$
= \frac{\hbar\omega}{6}(1 + 3 + 5) = \frac{9\hbar\omega}{6} = \frac{3\hbar\omega}{2}.
$$

**Step 3 (b):** Compute $\langle\hat{H}^2\rangle$:

$$
\langle\hat{H}^2\rangle = \frac{1}{3}\left(\frac{\hbar\omega}{2}\right)^2 + \frac{1}{3}\left(\frac{3\hbar\omega}{2}\right)^2 + \frac{1}{3}\left(\frac{5\hbar\omega}{2}\right)^2.
$$

$$
= \frac{(\hbar\omega)^2}{12}(1 + 9 + 25) = \frac{35(\hbar\omega)^2}{12}.
$$

$$
(\Delta E)^2 = \langle\hat{H}^2\rangle - \langle\hat{H}\rangle^2 = \frac{35(\hbar\omega)^2}{12} - \left(\frac{3\hbar\omega}{2}\right)^2 = \frac{35(\hbar\omega)^2}{12} - \frac{9(\hbar\omega)^2}{4} = \frac{35 - 27}{12}(\hbar\omega)^2 = \frac{8(\hbar\omega)^2}{12} = \frac{2(\hbar\omega)^2}{3}.
$$

$$
\Delta E = \hbar\omega\sqrt{\frac{2}{3}}.
$$

**Step 4 (c):** The probability of measuring $E_3$:

$$
P(E_3) = |\langle 3\vert\psi\rangle|^2 = |c_3|^2 = 0.
$$

The state has no $\vert 3\rangle$ component, so the probability is exactly zero.

---

### Example 9.2.3 — Using the Completeness Relation to Compute a Trace

**Problem:** Compute $\operatorname{Tr}(\vert\alpha\rangle\langle\beta\vert)$ where $\vert\alpha\rangle$ and $\vert\beta\rangle$ are arbitrary normalized states.

**Solution:**

**Step 1:** Choose any complete orthonormal basis $\{\vert n\rangle\}$:

$$
\operatorname{Tr}(\vert\alpha\rangle\langle\beta\vert) = \sum_n \langle n\vert(\vert\alpha\rangle\langle\beta\vert)\vert n\rangle = \sum_n \langle n\vert\alpha\rangle\langle\beta\vert n\rangle.
$$

**Step 2:** Recognize this as:

$$
= \sum_n \langle\beta\vert n\rangle\langle n\vert\alpha\rangle = \langle\beta\vert\left(\sum_n\vert n\rangle\langle n\vert\right)\vert\alpha\rangle = \langle\beta\vert\alpha\rangle.
$$

Therefore: $\operatorname{Tr}(\vert\alpha\rangle\langle\beta\vert) = \langle\beta\vert\alpha\rangle$.

**Special case:** $\operatorname{Tr}(\vert\psi\rangle\langle\psi\vert) = \langle\psi\vert\psi\rangle = 1$ for any normalized state. This confirms that the density matrix of a pure state has unit trace.

---

### Example 9.2.4 — Change of Basis: Spin-1/2 in the $S_x$ Eigenbasis

**Problem:** Express the $S_z$ eigenstates $\vert +\rangle_z$ and $\vert -\rangle_z$ in terms of the $S_x$ eigenstates $\vert +\rangle_x$ and $\vert -\rangle_x$.

**Solution:**

**Step 1:** Find the $S_x$ eigenstates. Solve $\hat{S}_x\vert\pm\rangle_x = \pm\frac{\hbar}{2}\vert\pm\rangle_x$:

$$
\frac{\hbar}{2}\begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = \pm\frac{\hbar}{2}\begin{pmatrix}a\\b\end{pmatrix}.
$$

For $+\frac{\hbar}{2}$: $b = a$, so $\vert +\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\1\end{pmatrix} = \frac{1}{\sqrt{2}}(\vert +\rangle_z + \vert -\rangle_z)$.

For $-\frac{\hbar}{2}$: $b = -a$, so $\vert -\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\-1\end{pmatrix} = \frac{1}{\sqrt{2}}(\vert +\rangle_z - \vert -\rangle_z)$.

**Step 2:** Invert these relations:

$$
\vert +\rangle_z = \frac{1}{\sqrt{2}}(\vert +\rangle_x + \vert -\rangle_x),
$$

$$
\vert -\rangle_z = \frac{1}{\sqrt{2}}(\vert +\rangle_x - \vert -\rangle_x).
$$

**Step 3:** Verify: If we measure $S_x$ on a spin-up-z state $\vert +\rangle_z$:

$$
P(S_x = +\tfrac{\hbar}{2}) = |{}_x\langle +\vert +\rangle_z|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}.
$$

$$
P(S_x = -\tfrac{\hbar}{2}) = |{}_x\langle -\vert +\rangle_z|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}.
$$

Equal probability of spin-up or spin-down along $x$ — as expected from the uncertainty principle for non-commuting observables.

---

### Example 9.2.5 — Constructing the Time Evolution Operator

**Problem:** A two-level system has Hamiltonian $\hat{H} = E_0\vert 0\rangle\langle 0\vert + E_1\vert 1\rangle\langle 1\vert$. If the initial state is $\vert\psi(0)\rangle = \cos\theta\vert 0\rangle + \sin\theta\vert 1\rangle$, find $\vert\psi(t)\rangle$ and the probability of finding the system in state $\vert 1\rangle$.

**Solution:**

**Step 1:** The time evolution operator:

$$
\hat{U}(t) = e^{-i\hat{H}t/\hbar} = e^{-iE_0 t/\hbar}\vert 0\rangle\langle 0\vert + e^{-iE_1 t/\hbar}\vert 1\rangle\langle 1\vert.
$$

(This follows from the spectral decomposition: $f(\hat{A}) = \sum_n f(a_n)\vert a_n\rangle\langle a_n\vert$.)

**Step 2:** Apply to the initial state:

$$
\vert\psi(t)\rangle = \hat{U}(t)\vert\psi(0)\rangle = \cos\theta\,e^{-iE_0 t/\hbar}\vert 0\rangle + \sin\theta\,e^{-iE_1 t/\hbar}\vert 1\rangle.
$$

**Step 3:** Probability of finding state $\vert 1\rangle$:

$$
P_1(t) = |\langle 1\vert\psi(t)\rangle|^2 = |\sin\theta\,e^{-iE_1 t/\hbar}|^2 = \sin^2\theta.
$$

The probability is **time-independent** because $\vert 0\rangle$ and $\vert 1\rangle$ are energy eigenstates. The phases $e^{-iE_n t/\hbar}$ are global phases within each component and cancel in the modulus squared.

**Note:** If we instead ask for the probability of a state that is a *superposition* of energy eigenstates (e.g., $\vert +\rangle_x$), we would get oscillating probabilities — quantum beats.

---

## 🔗 7. Cross-links & Further Reading

### Internal Vault Links
- [2.6 - Eigenvalues Eigenvectors & Diagonalization](2.6---Eigenvalues-Eigenvectors-&-Diagonalization) — Spectral theorem, diagonalization = finding the eigenbasis
- [2.7 - Inner Product Spaces & Orthogonality](2.7---Inner-Product-Spaces-&-Orthogonality) — Inner product axioms, Gram-Schmidt, orthogonal projections
- [2.8 - SVD & Tensors](2.8---SVD-&-Tensors) — Tensor products, multilinear algebra
- [9.1 - Wave Functions & The Schrodinger Equation](9.1---Wave-Functions-&-The-Schrodinger-Equation) — Position-space realization of this abstract framework
- [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) — Concrete eigenbasis examples
- [9.4 - Angular Momentum, Spin & Fine Structure](9.4---Angular-Momentum,-Spin-&-Fine-Structure) — Finite-dimensional Hilbert spaces (spin)

### External References
- **Susskind, L. & Friedman, A.** *Quantum Mechanics: The Theoretical Minimum* — Lectures 1–3 develop bra-ket from scratch.
- **Griffiths, D.J.** *Introduction to Quantum Mechanics*, 3rd ed. — Chapter 3 (Formalism).
- **Sakurai, J.J. & Napolitano, J.** *Modern Quantum Mechanics* — Chapter 1 is the definitive treatment of Dirac notation.
- **Tong, D.** [Quantum Field Theory Lecture Notes](https://www.damtp.cam.ac.uk/user/tong/qft.html) — Uses bra-ket throughout.

---

*Next: [9.3 - The 1D Infinite Square Well & Harmonic Oscillator](9.3---The-1D-Infinite-Square-Well-&-Harmonic-Oscillator) — Solving the TISE for the two most important potentials.*




---

## 🧠 8. Extended Worked Examples & Deep Dives

### Example 8.1 — Proving Hermitian Operators Have Real Eigenvalues and Orthogonal Eigenstates

**Problem:** Let $\hat{A}$ be a Hermitian operator ($\hat{A} = \hat{A}^\dagger$) on a Hilbert space $\mathcal{H}$. Prove: (a) all eigenvalues of $\hat{A}$ are real; (b) eigenstates belonging to distinct eigenvalues are orthogonal.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Real Eigenvalues

Let $\hat{A}\vert a\rangle = a\vert a\rangle$ with $\vert a\rangle \neq 0$.

**Step 1:** Take the inner product with $\langle a\vert$ from the left:

$$
\langle a\vert\hat{A}\vert a\rangle = a\langle a\vert a\rangle. \tag{1}
$$

**Step 2:** Now use Hermiticity. By definition $\langle a\vert\hat{A}^\dagger = \langle a\vert\hat{A}$, so:

$$
\langle a\vert\hat{A}\vert a\rangle = (\langle a\vert\hat{A}^\dagger\vert a\rangle)^* = (\langle a\vert\hat{A}\vert a\rangle)^*.
$$

Wait — more carefully: $\langle a\vert\hat{A}\vert a\rangle^* = \langle a\vert\hat{A}^\dagger\vert a\rangle = \langle a\vert\hat{A}\vert a\rangle$ (since $\hat{A}^\dagger = \hat{A}$).

So $\langle a\vert\hat{A}\vert a\rangle$ is real.

**Step 3:** From (1): $a = \frac{\langle a\vert\hat{A}\vert a\rangle}{\langle a\vert a\rangle}$. The numerator is real (Step 2) and the denominator $\langle a\vert a\rangle \gt  0$ is real. Therefore $a \in \mathbb{R}$. $\blacksquare$

#### Part (b): Orthogonality of Distinct Eigenstates

Let $\hat{A}\vert a\rangle = a\vert a\rangle$ and $\hat{A}\vert a'\rangle = a'\vert a'\rangle$ with $a \neq a'$.

**Step 1:** Compute $\langle a'\vert\hat{A}\vert a\rangle$ two ways.

First way (act right): $\langle a'\vert\hat{A}\vert a\rangle = a\langle a'\vert a\rangle$.

**Step 2:** Second way (act left, using $\hat{A}^\dagger = \hat{A}$):

$$
\langle a'\vert\hat{A}\vert a\rangle = (\hat{A}^\dagger\vert a'\rangle)^\dagger\vert a\rangle = (\hat{A}\vert a'\rangle)^\dagger\vert a\rangle.
$$

More precisely: $\langle a'\vert\hat{A}\vert a\rangle = \langle\hat{A}a'\vert a\rangle = (a'\vert a'\rangle)^\dagger\vert a\rangle = a'^*\langle a'\vert a\rangle = a'\langle a'\vert a\rangle$.

(We used $a'^* = a'$ from Part (a).)

**Step 3:** Equate the two expressions:

$$
a\langle a'\vert a\rangle = a'\langle a'\vert a\rangle.
$$

$$
(a - a')\langle a'\vert a\rangle = 0.
$$

Since $a \neq a'$, we must have $\langle a'\vert a\rangle = 0$. $\blacksquare$

</details>

### Example 8.2 — The Cauchy-Schwarz Inequality in a General Inner Product Space

**Problem:** For any two vectors $\vert\alpha\rangle, \vert\beta\rangle$ in a Hilbert space, prove:

$$
|\langle\alpha\vert\beta\rangle|^2 \leq \langle\alpha\vert\alpha\rangle\,\langle\beta\vert\beta\rangle.
$$

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: Construct a Non-Negative Quantity

For any complex number $\lambda$, define $\vert\gamma\rangle = \vert\alpha\rangle - \lambda\vert\beta\rangle$. By the positivity axiom of inner products:

$$
\langle\gamma\vert\gamma\rangle \geq 0.
$$

#### Step 2: Expand

$$
\langle\gamma\vert\gamma\rangle = \langle\alpha\vert\alpha\rangle - \lambda\langle\alpha\vert\beta\rangle - \lambda^*\langle\beta\vert\alpha\rangle + |\lambda|^2\langle\beta\vert\beta\rangle \geq 0.
$$

#### Step 3: Choose Optimal $\lambda$

To get the tightest bound, minimize over $\lambda$. Set $\lambda = \frac{\langle\beta\vert\alpha\rangle}{\langle\beta\vert\beta\rangle}$ (assuming $\vert\beta\rangle \neq 0$).

Then $\lambda^* = \frac{\langle\alpha\vert\beta\rangle}{\langle\beta\vert\beta\rangle}$ and $|\lambda|^2 = \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle^2}$.

#### Step 4: Substitute

$$
0 \leq \langle\alpha\vert\alpha\rangle - \frac{\langle\beta\vert\alpha\rangle}{\langle\beta\vert\beta\rangle}\langle\alpha\vert\beta\rangle - \frac{\langle\alpha\vert\beta\rangle}{\langle\beta\vert\beta\rangle}\langle\beta\vert\alpha\rangle + \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle^2}\langle\beta\vert\beta\rangle.
$$

Note $\langle\beta\vert\alpha\rangle\langle\alpha\vert\beta\rangle = |\langle\alpha\vert\beta\rangle|^2$. So:

$$
0 \leq \langle\alpha\vert\alpha\rangle - \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle} - \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle} + \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle}.
$$

$$
0 \leq \langle\alpha\vert\alpha\rangle - \frac{|\langle\alpha\vert\beta\rangle|^2}{\langle\beta\vert\beta\rangle}.
$$

#### Step 5: Rearrange

$$
|\langle\alpha\vert\beta\rangle|^2 \leq \langle\alpha\vert\alpha\rangle\,\langle\beta\vert\beta\rangle. \quad \blacksquare
$$

**Equality condition:** $\langle\gamma\vert\gamma\rangle = 0 \iff \vert\gamma\rangle = 0 \iff \vert\alpha\rangle = \lambda\vert\beta\rangle$ (vectors are proportional).

**Physical application:** The generalized uncertainty principle $\Delta A\,\Delta B \geq \frac{1}{2}|\langle[\hat{A},\hat{B}]\rangle|$ is derived using Cauchy-Schwarz on the vectors $(\hat{A} - \langle A\rangle)\vert\psi\rangle$ and $(\hat{B} - \langle B\rangle)\vert\psi\rangle$.

</details>

### Example 8.3 — Resolution of the Identity and Completeness

**Problem:** Given a complete orthonormal basis $\{\vert n\rangle\}$ of a Hilbert space, prove the resolution of the identity $\sum_n \vert n\rangle\langle n\vert = \hat{I}$, and use it to derive the position-space representation of the momentum operator.

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Part (a): Proof of the Resolution of Identity

**Step 1:** By completeness, any $\vert\psi\rangle \in \mathcal{H}$ can be expanded:

$$
\vert\psi\rangle = \sum_n c_n\vert n\rangle.
$$

**Step 2:** The expansion coefficients are $c_n = \langle n\vert\psi\rangle$ (by orthonormality $\langle m\vert n\rangle = \delta_{mn}$).

**Step 3:** Substitute back:

$$
\vert\psi\rangle = \sum_n \langle n\vert\psi\rangle\,\vert n\rangle = \sum_n \vert n\rangle\langle n\vert\psi\rangle = \left(\sum_n \vert n\rangle\langle n\vert\right)\vert\psi\rangle.
$$

Since this holds for **all** $\vert\psi\rangle$:

$$
\sum_n \vert n\rangle\langle n\vert = \hat{I}. \quad \blacksquare
$$

#### Part (b): Continuous Case — Position and Momentum

For the position eigenstates $\vert x\rangle$ with $\langle x\vert x'\rangle = \delta(x - x')$:

$$
\int_{-\infty}^{\infty} \vert x\rangle\langle x\vert\,dx = \hat{I}.
$$

**Step 4:** The momentum operator in position space. Start from $\hat{p}\vert p\rangle = p\vert p\rangle$ and $\langle x\vert p\rangle = \frac{1}{\sqrt{2\pi\hbar}}e^{ipx/\hbar}$.

**Step 5:** Insert the identity $\hat{I} = \int\vert p\rangle\langle p\vert\,dp$:

$$
\langle x\vert\hat{p}\vert\psi\rangle = \int \langle x\vert\hat{p}\vert p\rangle\langle p\vert\psi\rangle\,dp = \int p\,\langle x\vert p\rangle\,\phi(p)\,dp.
$$

$$
= \int p\,\frac{e^{ipx/\hbar}}{\sqrt{2\pi\hbar}}\,\phi(p)\,dp.
$$

**Step 6:** Recognize that $p\,e^{ipx/\hbar} = -i\hbar\frac{\partial}{\partial x}e^{ipx/\hbar}$:

$$
\langle x\vert\hat{p}\vert\psi\rangle = -i\hbar\frac{\partial}{\partial x}\int\frac{e^{ipx/\hbar}}{\sqrt{2\pi\hbar}}\phi(p)\,dp = -i\hbar\frac{\partial}{\partial x}\psi(x).
$$

Therefore: $\hat{p} \to -i\hbar\frac{\partial}{\partial x}$ in position representation. $\blacksquare$

</details>

### Example 8.4 — Ehrenfest's Theorem: Quantum Expectation Values Obey Classical Equations

**Problem:** Prove that for a particle in potential $V(x)$:

$$
\frac{d\langle x\rangle}{dt} = \frac{\langle p\rangle}{m}, \qquad \frac{d\langle p\rangle}{dt} = -\left\langle\frac{\partial V}{\partial x}\right\rangle.
$$

<details>
<summary>🔍 View Step-by-Step Solution</summary>

#### Step 1: General Time Derivative of an Expectation Value

For any operator $\hat{A}$ (not explicitly time-dependent):

$$
\frac{d}{dt}\langle\hat{A}\rangle = \frac{d}{dt}\langle\psi\vert\hat{A}\vert\psi\rangle = \langle\dot{\psi}\vert\hat{A}\vert\psi\rangle + \langle\psi\vert\hat{A}\vert\dot{\psi}\rangle.
$$

From the Schrödinger equation: $i\hbar\vert\dot{\psi}\rangle = \hat{H}\vert\psi\rangle$, so $\vert\dot{\psi}\rangle = -\frac{i}{\hbar}\hat{H}\vert\psi\rangle$ and $\langle\dot{\psi}\vert = \frac{i}{\hbar}\langle\psi\vert\hat{H}$.

$$
\frac{d\langle\hat{A}\rangle}{dt} = \frac{i}{\hbar}\langle\psi\vert\hat{H}\hat{A}\vert\psi\rangle - \frac{i}{\hbar}\langle\psi\vert\hat{A}\hat{H}\vert\psi\rangle = \frac{i}{\hbar}\langle[\hat{H}, \hat{A}]\rangle.
$$

#### Step 2: First Ehrenfest Relation ($\hat{A} = \hat{x}$)

$$
\frac{d\langle x\rangle}{dt} = \frac{i}{\hbar}\langle[\hat{H}, \hat{x}]\rangle.
$$

With $\hat{H} = \frac{\hat{p}^2}{2m} + V(\hat{x})$:

$$
[\hat{H}, \hat{x}] = \frac{1}{2m}[\hat{p}^2, \hat{x}] + [V(\hat{x}), \hat{x}].
$$

The second commutator vanishes (function of $\hat{x}$ commutes with $\hat{x}$).

For the first: $[\hat{p}^2, \hat{x}] = \hat{p}[\hat{p}, \hat{x}] + [\hat{p}, \hat{x}]\hat{p} = \hat{p}(-i\hbar) + (-i\hbar)\hat{p} = -2i\hbar\hat{p}$.

(We used $[\hat{p}, \hat{x}] = -i\hbar$ and the identity $[AB, C] = A[B,C] + [A,C]B$.)

Therefore:

$$
[\hat{H}, \hat{x}] = \frac{-2i\hbar\hat{p}}{2m} = \frac{-i\hbar\hat{p}}{m}.
$$

$$
\frac{d\langle x\rangle}{dt} = \frac{i}{\hbar}\cdot\frac{-i\hbar}{m}\langle\hat{p}\rangle = \frac{\langle p\rangle}{m}. \quad \checkmark
$$

#### Step 3: Second Ehrenfest Relation ($\hat{A} = \hat{p}$)

$$
\frac{d\langle p\rangle}{dt} = \frac{i}{\hbar}\langle[\hat{H}, \hat{p}]\rangle.
$$

$$
[\hat{H}, \hat{p}] = \frac{1}{2m}[\hat{p}^2, \hat{p}] + [V(\hat{x}), \hat{p}].
$$

The first commutator vanishes ($\hat{p}$ commutes with itself).

For the second, in position representation:

$$
[V(\hat{x}), \hat{p}]\psi = V(x)\left(-i\hbar\frac{d\psi}{dx}\right) - \left(-i\hbar\right)\frac{d}{dx}(V\psi).
$$

$$
= -i\hbar V\psi' + i\hbar(V'\psi + V\psi') = i\hbar V'(x)\psi.
$$

So $[V(\hat{x}), \hat{p}] = i\hbar\frac{dV}{dx}$.

Therefore:

$$
\frac{d\langle p\rangle}{dt} = \frac{i}{\hbar}\cdot i\hbar\left\langle\frac{dV}{dx}\right\rangle = -\left\langle\frac{dV}{dx}\right\rangle. \quad \blacksquare
$$

**Physical interpretation:** These are the quantum analogues of Hamilton's equations $\dot{x} = p/m$ and $\dot{p} = -V'(x)$. They are exact for any state, but only reduce to classical mechanics when the potential is at most quadratic (so $\langle V'(x)\rangle = V'(\langle x\rangle)$) or when the wave packet is narrow.

</details>

---

## 📘 9. Appendix: Extended Derivations & Special Cases

### Appendix 9.1 — The Riesz Representation Theorem and the Spectral Theorem for Self-Adjoint Operators

**The Riesz Representation Theorem** (finite-dimensional version):

Every continuous linear functional $f: \mathcal{H} \to \mathbb{C}$ on a Hilbert space can be uniquely represented as $f(\vert\psi\rangle) = \langle\phi_f\vert\psi\rangle$ for a unique $\vert\phi_f\rangle \in \mathcal{H}$.

**Proof sketch:** Define $\mathcal{N} = \ker(f)$. If $f = 0$, take $\vert\phi_f\rangle = 0$. Otherwise, $\mathcal{N}$ is a proper closed subspace, so $\mathcal{N}^\perp \neq \{0\}$. Pick $\vert z\rangle \in \mathcal{N}^\perp$ with $f(\vert z\rangle) = 1$ (normalize appropriately). For any $\vert\psi\rangle$:

$$
\vert\psi\rangle - f(\vert\psi\rangle)\vert z\rangle \in \mathcal{N},
$$

since $f(\vert\psi\rangle - f(\vert\psi\rangle)\vert z\rangle) = f(\vert\psi\rangle) - f(\vert\psi\rangle) = 0$.

Therefore $\langle z\vert\psi\rangle - f(\vert\psi\rangle)\langle z\vert z\rangle = 0$ (since $\vert z\rangle \perp \mathcal{N}$), giving $f(\vert\psi\rangle) = \frac{\langle z\vert\psi\rangle}{\langle z\vert z\rangle}$. Set $\vert\phi_f\rangle = \vert z\rangle/\langle z\vert z\rangle$.

**Physical significance:** This theorem is why bras $\langle\phi\vert$ exist — every linear functional on the state space is an inner product with some state. It justifies the entire bra-ket formalism.

---

**The Spectral Theorem** (finite-dimensional):

Every self-adjoint (Hermitian) operator $\hat{A}$ on a finite-dimensional Hilbert space $\mathcal{H}$ admits a spectral decomposition:

$$
\hat{A} = \sum_{n} a_n \vert a_n\rangle\langle a_n\vert,
$$

where $\{a_n\}$ are the (real) eigenvalues and $\{\vert a_n\rangle\}$ form a complete orthonormal basis.

**Proof sketch (induction on dimension):**

*Base case* ($\dim\mathcal{H} = 1$): $\hat{A} = a\hat{I}$ trivially.

*Inductive step:* $\hat{A}$ has at least one eigenvalue $a_1$ (roots of the characteristic polynomial exist over $\mathbb{C}$, and they're real by Hermiticity). Let $\vert a_1\rangle$ be the corresponding normalized eigenvector. Define $\mathcal{H}_1 = \text{span}\{\vert a_1\rangle\}^\perp$.

**Claim:** $\hat{A}$ maps $\mathcal{H}_1$ to itself. Proof: if $\vert\phi\rangle \in \mathcal{H}_1$, then $\langle a_1\vert\hat{A}\vert\phi\rangle = \langle\hat{A}a_1\vert\phi\rangle = a_1\langle a_1\vert\phi\rangle = 0$. So $\hat{A}\vert\phi\rangle \in \mathcal{H}_1$.

By induction, $\hat{A}\big|_{\mathcal{H}_1}$ has a spectral decomposition on the $(n-1)$-dimensional space $\mathcal{H}_1$. Combining with the $\vert a_1\rangle$ component gives the full decomposition. $\blacksquare$

**For infinite-dimensional spaces:** The spectral theorem generalizes (von Neumann, 1932) to unbounded self-adjoint operators via projection-valued measures:

$$
\hat{A} = \int_{-\infty}^{\infty} \lambda\,dE(\lambda),
$$

where $E(\lambda)$ is the spectral family of projection operators. This handles both discrete and continuous spectra simultaneously.

**References:** Reed & Simon, *Methods of Modern Mathematical Physics* Vol. I; Sakurai Ch. 1; Tong QM notes §2.


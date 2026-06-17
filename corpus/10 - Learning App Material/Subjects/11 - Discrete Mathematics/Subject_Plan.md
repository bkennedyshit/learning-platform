---
date: 2026-05-29
title: "APP-11 — Discrete Mathematics: Subject Plan"
mission: "Build the mathematical foundations of computer science — logic, sets, graph theory, combinatorics, proof techniques, and number theory — for grades 11-12 and college CS"
status: planning
tags: [discrete-math, CS, logic, graph-theory, combinatorics, grades-11-12, college, app-curriculum]
type: subject-plan
app-track: "11"
grade-band: 11-12 / college
standards: CSTA K-12 CS Standards Level 3; ACM CS2013
---

# APP-11 — Discrete Mathematics

*Part of [[Bill's Vault/05-Knowledge_Foundation/10 - Learning App Material/README|10 - Learning App Material]]*

> **App context:** Discrete Math is the missing link between high school math and computer science. It's a prerequisite for algorithms, data structures, cryptography, compilers, and AI. Most students who struggle with CS upper-division courses are missing discrete math foundations. This is the bridge.

---

## 2. Free Learning Catalog

| Resource | Type | Grade | Link |
|---------|------|-------|------|
| **MIT OpenCourseWare 6.042J (Math for CS)** | Full free course | college | [ocw.mit.edu/courses/6-042j](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/) — **primary resource** |
| **Trefor Bazett — Discrete Math (YouTube)** | Complete course | 11/college | [youtube.com/@DrTreforBazett](https://www.youtube.com/@DrTreforBazett) |
| **TrevTutor — Discrete Math (YouTube)** | Worked examples | 11/college | [youtube.com/@TrevTutor](https://www.youtube.com/@TrevTutor) |
| **Khan Academy — Logic + Proofs** | Foundational topics | 11 | [khanacademy.org](https://www.khanacademy.org/) |
| **Discrete Mathematics and Its Applications — Rosen** | Standard textbook (library) | college | Classic text; 8th ed. |
| **Book of Proof (free PDF)** | Free proof textbook | college | [people.vcu.edu/~rhammack/BookOfProof](https://www.people.vcu.edu/~rhammack/BookOfProof/) |
| **Art of Problem Solving** | Competition math + discrete | 11/college | [artofproblemsolving.com](https://artofproblemsolving.com/) |
| **CS Theory (YouTube — Reducible)** | Visual theory explainers | college | [youtube.com/@Reducible](https://www.youtube.com/@Reducible) |

---

## 3. Chapter Outline

| # | Chapter | Core skill | CS application |
|---|---------|-----------|---------------|
| 11.1 | **Propositional Logic** | Propositions; logical connectives (¬, ∧, ∨, →, ↔); truth tables; tautologies and contradictions; logical equivalences; De Morgan's laws; logical inference rules; applications to circuit design and programming conditions | Boolean logic in code, circuit design |
| 11.2 | **Predicate Logic & Proof Techniques** | Predicates and quantifiers (∀, ∃); nested quantifiers; proof techniques: direct proof, proof by contrapositive, proof by contradiction, proof by cases, proof by exhaustion; mathematical induction (weak, strong, structural) | Formal verification, algorithm correctness |
| 11.3 | **Sets, Functions & Relations** | Set notation and operations (union, intersection, complement, difference, power set, Cartesian product); Venn diagrams; cardinality; functions (injective, surjective, bijective); function composition; inverse functions; equivalence relations; partial orders | Type theory, databases, hash functions |
| 11.4 | **Combinatorics & Counting** | Multiplication and addition principles; permutations (with/without repetition); combinations; binomial theorem (Pascal's triangle); inclusion-exclusion principle; pigeonhole principle; generating functions intro | Algorithm analysis, probability calculations |
| 11.5 | **Probability & Discrete Distributions** | Sample spaces for discrete systems; conditional probability; Bayes' theorem; random variables; expected value; variance; Bernoulli and binomial distributions; geometric distribution; applications to randomized algorithms | Machine learning, algorithm analysis |
| 11.6 | **Number Theory & Cryptography** | Divisibility; prime numbers; GCD and LCM (Euclidean algorithm); modular arithmetic; congruences; Fermat's Little Theorem; Euler's theorem; RSA encryption (the math behind public-key cryptography) | Cryptography, hashing, computer security |
| 11.7 | **Graph Theory** | Graph terminology (vertices, edges, degree, path, cycle, connected); trees (definition, properties, spanning trees); graph representations (adjacency matrix, adjacency list); graph traversal (BFS, DFS); Eulerian and Hamiltonian paths; planar graphs; graph coloring; weighted graphs and shortest paths (Dijkstra's algorithm) | Networking, social graphs, algorithms, databases |
| 11.8 | **Automata & Formal Languages** | Deterministic finite automata (DFA); nondeterministic finite automata (NFA); regular expressions and regular languages; context-free grammars; pushdown automata (intro); Turing machines (intro); computability and the halting problem; complexity classes P and NP (conceptual) | Compilers, regex, theoretical CS |

---

## 5. Standards Alignment
- **CSTA K-12 CS Standards Level 3A/B** (algorithms, abstraction, models)
- **ACM/IEEE CS2013 Curriculum:** Discrete structures knowledge area
- **Connects to:** Track 08 Python (algorithms and data structures), Track 15 Compilers (formal languages), Track 23 AI/ML (probability, graph theory)

---
date: 2026-05-06
title: Calculator Suite - Quick Reference
type: reference
tags: [calculators, quick-ref]
---

# Calculator Suite Quick Reference

## What We're Building

**4 separate desktop calculators** that mimic real professional tools for AI/ML math learning.

---

## The Apps

| # | Name | Mimics | Purpose | Status |
|---|------|--------|---------|--------|
| 1 | **Matrix Commander** | MATLAB + Wolfram | Linear algebra for neural nets | 🔲 Not Started |
| 2 | **Calculus Visualizer** | Desmos + TI-Nspire | Derivatives & backpropagation | 🔲 Not Started |
| 3 | **Loss Landscape 3D** | MATLAB + TensorBoard | Multivariable calc & optimization | 🔲 Not Started |
| 4 | **Probability Studio** | R Studio + SPSS | Stats & distributions for ML | 🔲 Not Started |

---

## Build Order

**Start with #1 - Matrix Commander** because:
- Builds on your MAT-111 knowledge (you already have matrices basics)
- Linear algebra is foundation for everything in AI/ML
- Eigenvalues/SVD are critical concepts you'll need constantly
- Easiest to verify correctness (matrix math has definite right answers)

---

## How Each Calc Helps You Build LLMs

### 1️⃣ Matrix Commander
**What it teaches:**
- Weight matrices in neural networks
- How transformers use attention (it's just matrices!)
- Why eigenvalues matter for training stability
- Dimensionality reduction (SVD for embeddings)

**When you'll use it:**
- Understanding forward pass (matrix multiplication)
- Debugging weight initialization
- Visualizing how transformations work

---

### 2️⃣ Calculus Visualizer
**What it teaches:**
- Chain rule = backpropagation (LITERALLY the same)
- Gradient descent (how training works)
- Learning rates and convergence
- Why derivatives matter for optimization

**When you'll use it:**
- Learning backprop algorithm
- Understanding why gradients vanish/explode
- Tuning learning rates
- Seeing loss decrease over time

---

### 3️⃣ Loss Landscape 3D
**What it teaches:**
- Why training gets stuck (saddle points)
- How momentum helps escape local minima
- Why Adam optimizer works better than SGD
- Visualizing high-dimensional parameter space

**When you'll use it:**
- Debugging training issues
- Understanding optimizer choices
- Seeing why batch size matters
- Visualizing loss surface topology

---

### 4️⃣ Probability Studio
**What it teaches:**
- Softmax (converts logits to probabilities)
- Cross-entropy loss (classification objective)
- Why certain distributions matter
- Attention weights are probability distributions

**When you'll use it:**
- Understanding output layers
- Debugging classification issues
- Seeing why softmax temperature matters
- Understanding sampling strategies

---

## Using Them Together

**Example Learning Flow:**

1. **Week 1-2:** Study linear algebra → Use Matrix Commander
   - Create weight matrices
   - Multiply matrices (see forward pass)
   - Calculate eigenvalues (understand stability)

2. **Week 3-4:** Study calculus → Use Calculus Visualizer  
   - Take derivatives
   - Visualize chain rule
   - Animate gradient descent

3. **Week 5-6:** Study optimization → Use Loss Landscape 3D
   - Plot loss functions
   - Watch gradient descent navigate surface
   - Compare different optimizers

4. **Week 7-8:** Study probability → Use Probability Studio
   - Visualize softmax
   - Calculate cross-entropy
   - See attention distributions

5. **Week 9+:** BUILD NEURAL NET
   - Every concept now makes sense
   - Use calculators to verify math
   - Understand what's happening, not just copying code

---

## Tech Stack (All Calculators)

```
Language:    C++20
Framework:   Qt 6.x
Math:        Eigen library (linear algebra)
             SymEngine (symbolic math)
Graphics:    QtCharts (2D)
             Qt3D (3D visualization)
Build:       CMake
Platform:    Windows 11 (primary)
Deploy:      System tray integration
```

---

## File Locations

**Projects** (outside vault):
```
C:\Obsidian Vault\Learning_Tools\
├── MatrixCommander/
├── CalculusVisualizer/
├── LossLandscape3D/
└── ProbabilityStudio/
```

**Docs** (in vault):
```
C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\
├── graphing-calculator.html (web calc)
├── CALCULATOR_SUITE_VISION.md (roadmap)
├── QUICK_REFERENCE.md (this file)
└── README.md (location guide)
```

---

## Next Action

**Choose one:**
- [ ] Build Matrix Commander first (recommended - builds on MAT-111)
- [ ] Build Calculus Visualizer first (if you want to dive into derivatives)
- [ ] Set up Qt dev environment first (get tooling ready)

**What do you want to do?**

---

## Related Notes
- [[CALCULATOR_SUITE_VISION]] - Same Dev_Tools folder
- [[HOW_TO_USE_CALCULATORS]] - Same Dev_Tools folder
- [[LOCATION_SETUP_GUIDE]] - Same Dev_Tools folder
- [[Git Essentials for Coding Tests]] - Same Dev_Tools folder
- [[PRACTICE_GUI_APP_VISION]] - Same Dev_Tools folder

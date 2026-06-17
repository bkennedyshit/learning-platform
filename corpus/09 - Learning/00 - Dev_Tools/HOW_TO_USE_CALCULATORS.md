---
date: 2026-05-06
title: Calculator Suite - Quick Start & Usage Guide
type: reference
tags: [calculators, usage, quick-reference]
---

# Calculator Suite - How to Use

**Quick reference for using each calculator after they're built.**

---

## 🚀 Quick Start (After Installing Qt & Building)

### Run the Setup Check
```powershell
cd "C:\Obsidian Vault\Learning_Tools"
.\setup-check.ps1
```

### Build All Calculators
```powershell
.\build-all-calculators.ps1
```

### Launch a Calculator
```powershell
# Manual launch
.\MatrixCommander\build\Release\MatrixCommander.exe

# OR use the launcher
.\launch-calculators.ps1
```

---

## 📊 Calculator 1: Matrix Commander

### What It Does
Linear algebra calculator for understanding neural network math.

### Basic Usage

**Create a Matrix:**
1. Set dimensions (e.g., 3×3)
2. Click cells and type numbers
3. OR click "Random 🎲" for random matrix

**Basic Operations:**
- **Add/Subtract:** Enter two matrices, click operation
- **Multiply:** Matrix A × Matrix B
- **Transpose:** Flip rows/columns

**Advanced Operations:**
- **Determinant:** Calculate det(A)
- **Inverse:** Find A⁻¹ (if exists)
- **Eigenvalues:** Find λ values (critical for AI!)
- **SVD:** Singular Value Decomposition

**Visualizations:**
1. Enter 2×2 transformation matrix
2. Click "Visualize Transform"
3. Watch vectors transform
4. See eigenvectors (special directions!)

### Why It Matters for AI/ML
- **Weight matrices** in neural networks
- **Matrix multiplication** = forward pass
- **Transpose** = backprop involves A^T
- **Eigenvalues** = training stability
- **SVD** = dimensionality reduction, embeddings

### Example Workflow
```
1. Create 2×2 matrix: [[2, 1], [1, 2]]
2. Click "Eigenvalues"
3. Result: λ₁=3, λ₂=1
4. Click "Eigen Visualizer" to see graphically
5. Observe eigenvectors stay on their lines!
```

---

## 📐 Calculator 2: Calculus Visualizer

### What It Does
Derivative calculator with chain rule breakdown for understanding backpropagation.

### Basic Usage

**Graph a Function:**
1. Type function in input: `x^2`
2. Click "Graph" tab
3. See f(x) plotted
4. Toggle f'(x) to see derivative simultaneously

**Calculate Derivative:**
1. Go to "Derivatives" tab
2. Enter function: `sin(x^2)`
3. Click "Compute Derivative"
4. See step-by-step chain rule breakdown!

**Gradient Descent:**
1. Go to "Optimization" tab
2. Select function (e.g., `x^2`)
3. Adjust learning rate slider
4. Click "Start"
5. Watch optimizer find minimum!

**Tangent Lines:**
1. Go to "Tangent Analysis" tab
2. Plot a function
3. Click on graph to place tangent line
4. See slope (derivative) at that point

### Why It Matters for AI/ML
- **Chain rule** = backpropagation (same math!)
- **Derivative** = gradient for weight updates
- **Gradient descent** = how neural nets learn
- **Learning rate** = step size in optimization

### Example Workflow - Understanding Backprop
```
1. Enter: 1/(1+exp(-x))  (sigmoid function)
2. Go to "Derivatives" tab
3. Click "Compute Derivative"
4. See chain rule steps:
   - Outer function: 1/u → -1/u²
   - Inner function: 1+exp(-x) → -exp(-x)
   - Result: exp(-x)/(1+exp(-x))²
5. This is EXACTLY how backprop works!
```

---

## 🌐 Calculator 3: Loss Landscape 3D

### What It Does
3D visualization of loss surfaces and optimization algorithms.

### Basic Usage

**Plot a Loss Surface:**
1. Select function (e.g., "Rosenbrock")
2. Click "Plot Surface"
3. Drag to rotate, scroll to zoom
4. See 3D surface shape

**2D Contour View:**
1. Click "Contour" tab
2. See top-down view with level curves
3. Critical points marked (min/max/saddle)

**Gradient Field:**
1. Click "Gradient Field" tab
2. See arrows showing gradient direction
3. Color = magnitude

**Single Optimizer:**
1. Click "Optimization Path" tab
2. Select optimizer (SGD, Momentum, Adam)
3. Set learning rate
4. Click starting point
5. Watch optimizer navigate to minimum!

**Multi-Optimizer Race:**
1. Click "Multi-Optimizer" tab
2. Click "Start Race"
3. Watch 6 optimizers compete
4. See which finds minimum fastest

### Why It Matters for AI/ML
- **Loss surface** = what neural nets navigate
- **Saddle points** = major training challenge
- **Momentum** = helps escape valleys
- **Adam** = adaptive learning rates

### Example Workflow - Why Momentum Helps
```
1. Select "Rosenbrock" (narrow valley)
2. Single Optimizer tab
3. Try SGD with lr=0.01
   → Slow, zigzags across valley
4. Try Momentum with lr=0.01
   → Much faster, smoother path
5. Try Adam with lr=0.1
   → Fastest! Adapts automatically
6. NOW YOU SEE why Adam is popular!
```

---

## 📊 Calculator 4: Probability Studio

### What It Does
Statistics and probability for ML - distributions, softmax, loss functions.

### Basic Usage (9 Tabs!)

**Tab 1: Distributions**
- Select: Normal, Binomial, Poisson, etc.
- Adjust parameters with sliders
- See PDF/CDF update in real-time

**Tab 2: Softmax & Temperature**
- Enter 5 logit values
- Adjust temperature (0.1 to 3.0)
- See how temperature affects distribution
- **Critical for LLM sampling!**

**Tab 3: Bayes' Theorem**
- Set prior, likelihood, evidence
- See visual probability tree
- Calculate posterior
- Real examples (medical test, spam filter)

**Tab 4: Cross-Entropy Loss**
- Binary and categorical versions
- See why it penalizes confident errors
- Interactive loss surface

**Tab 5: KL Divergence**
- Compare two distributions
- See D_KL(P||Q) asymmetry
- Understand when distributions differ

**Tab 6: Sampling (CLT)**
- Watch Central Limit Theorem in action
- See sample means become normal
- Law of Large Numbers animation

**Tab 7: Hypothesis Testing**
- t-tests, z-tests, p-values
- Confidence intervals
- A/B testing for ML models

**Tab 8: Confusion Matrix**
- Enter TP, FP, TN, FN
- Calculate all metrics (precision, recall, F1, MCC)
- See why accuracy misleads

**Tab 9: Attention Weights**
- Visualize attention as probability distribution
- Understand transformer attention

### Why It Matters for AI/ML
- **Softmax** = converts logits to probabilities
- **Temperature** = controls LLM creativity vs determinism
- **Cross-entropy** = classification loss function
- **KL divergence** = distribution distance
- **Confusion matrix** = evaluate classifier performance

### Example Workflow - LLM Sampling
```
1. Go to "Softmax & Temperature" tab
2. Enter logits: [2.5, 1.8, 0.9, -0.3, -1.2]
3. Set temperature = 0.1 (deterministic)
   → Softmax: [0.98, 0.02, 0.00, 0.00, 0.00]
   → Almost certain about first choice
4. Set temperature = 1.0 (balanced)
   → Softmax: [0.59, 0.29, 0.12, 0.00, 0.00]
   → More distributed
5. Set temperature = 2.0 (creative)
   → Softmax: [0.42, 0.30, 0.18, 0.07, 0.03]
   → Even more spread out
6. This is EXACTLY how GPT sampling works!
```

---

## 🎯 Learning Roadmap with All 4

### Month 1: Linear Algebra (Matrix Commander)
- **Week 1:** Matrix basics (add, multiply, transpose)
- **Week 2:** Determinants and inverses
- **Week 3:** Eigenvalues (critical for AI!)
- **Week 4:** SVD and transformations

### Month 2: Calculus (Calculus Visualizer)
- **Week 5:** Derivatives and rules
- **Week 6:** Chain rule = backprop
- **Week 7:** Gradient descent basics
- **Week 8:** Optimization algorithms

### Month 3: Multivariable (Loss Landscape 3D)
- **Week 9:** 3D surfaces and gradients
- **Week 10:** Saddle points vs local minima
- **Week 11:** Momentum and Adam
- **Week 12:** Loss landscape analysis

### Month 4: Statistics (Probability Studio)
- **Week 13:** Distributions (Normal, Binomial, etc.)
- **Week 14:** Softmax and cross-entropy
- **Week 15:** Bayes' theorem and KL divergence
- **Week 16:** Classification metrics

### Month 5+: Build Neural Networks!
- **Apply everything learned**
- **Use calculators to verify your work**
- **Understand every line of PyTorch/TensorFlow**

---

## 💡 Pro Tips

### Use Together
- Plot function in **Calculus Visualizer**
- Compute derivative step-by-step
- Export weights to **Matrix Commander**
- Verify matrix operations
- Visualize in **Loss Landscape 3D**
- Check distributions in **Probability Studio**

### Export & Document
- Take screenshots of visualizations
- Copy results to clipboard
- Paste into Obsidian notes
- Build your conceptual understanding

### Verify Notebook Work
- Solve problem on paper first
- Check answer with calculator
- If wrong, use visualization to understand why

### Build Intuition
- Don't just calculate - VISUALIZE
- See the math, don't just compute it
- Use animations to build mental models

---

## 🚨 Common Issues

### "Calculator won't start"
- Run `windeployqt [calculator].exe` to copy Qt DLLs
- Or add Qt\bin to system PATH

### "Graph not rendering"
- Update graphics drivers
- Try different function
- Zoom out (might be outside view)

### "Build failed"
- Delete build/ folder
- Run CMake again from scratch
- Check Qt installation with setup-check.ps1

---

## 📚 Additional Resources

**In Vault:**
- [QT_INSTALLATION_BUILD_GUIDE.md](QT_INSTALLATION_BUILD_GUIDE.md) - Full setup
- [CALCULATOR_SUITE_VISION.md](CALCULATOR_SUITE_VISION.md) - Why each matters
- [COMPLETE_DELIVERY.md](COMPLETE_DELIVERY.md) - Technical details

**In Learning_Tools:**
- `setup-check.ps1` - Verify installation
- `build-all-calculators.ps1` - Build everything
- `launch-calculators.ps1` - Quick launcher (after build)

**Individual Project READMEs:**
- Each calculator has its own documentation in project folder

---

**Now start learning! Begin with Matrix Commander and your MAT-111 notes.** 🚀🧠

---

## Related Notes
- [[CALCULATOR_SUITE_VISION]] - Same Dev_Tools folder
- [[LOCATION_SETUP_GUIDE]] - Same Dev_Tools folder
- [[QUICK_REFERENCE]] - Same Dev_Tools folder
- [[Git Essentials for Coding Tests]] - Same Dev_Tools folder
- [[PRACTICE_GUI_APP_VISION]] - Same Dev_Tools folder

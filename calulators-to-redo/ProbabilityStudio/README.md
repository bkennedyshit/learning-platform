---
date: 2026-05-26
title: "Probability Studio - ML Statistics Toolkit"
tags: [learning, probabilitystudio]
status: reference
type: index
---

# Probability Studio - ML Statistics Toolkit

**An interactive educational application for understanding statistical and probabilistic concepts in machine learning**

![Language](https://img.shields.io/badge/Language-C%2B%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Qt-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Purpose

Probability Studio provides **interactive visualizations** that help you understand the **WHY** behind ML statistics, not just the formulas. Each widget is designed to build intuition through exploration.

## 📦 Components

### 1. **Cross-Entropy Loss Visualizer**
- Binary and categorical cross-entropy
- Interactive loss surfaces
- **Why it's used**: See how it penalizes confident wrong predictions
- Understand gradient behavior

### 2. **KL Divergence Explorer**
- Compare probability distributions (Normal, Exponential, Uniform, Beta)
- Visualize asymmetry: D_KL(P||Q) ≠ D_KL(Q||P)
- **Applications**: VAEs, model distillation, policy optimization
- Analytical formulas for specific distributions

### 3. **Sampling Theory Visualizer**
- **Central Limit Theorem**: Watch any distribution become normal!
- **Law of Large Numbers**: See convergence to true mean
- Animated demonstrations
- Multiple source distributions

### 4. **Hypothesis Testing Calculator**
- One-sample t-test, two-sample t-test, z-test, paired t-test
- Visual p-values and confidence intervals
- Critical regions on distribution curves
- **ML Applications**: A/B testing, model comparison

### 5. **Confusion Matrix & Metrics**
- Interactive confusion matrix editor
- **All metrics**: Accuracy, Precision, Recall, F1, Specificity, MCC
- Example scenarios (medical, spam, imbalanced datasets)
- **Learn**: Why accuracy alone is insufficient!

### 6. **Attention Weight Distribution**
- Visualize attention as probability distributions
- Temperature (softmax) effects on distribution sharpness
- Entropy analysis
- **Examples**: Translation, QA, multi-modal attention
- **Key Insight**: Attention = differentiable soft selection

## 🛠️ Building

### Prerequisites
- **Qt 5.15+** or **Qt 6.x**
- **CMake 3.16+** or **qmake**
- **C++11** compiler (C++17 recommended)

### Build with CMake
```bash
mkdir build
cd build
cmake ..
cmake --build .
./ProbabilityStudio
```

### Build with qmake
```bash
qmake ProbabilityStudio.pro
make  # or nmake on Windows
./ProbabilityStudio
```

### Qt Creator
1. Open `ProbabilityStudio.pro` or `CMakeLists.txt`
2. Configure project with your Qt kit
3. Build and Run

## 🎓 Educational Philosophy

Each widget follows this structure:
- **What is it?** - Clear definition
- **Why does it matter?** - Practical ML applications
- **Interactive exploration** - Adjust parameters, see results
- **Visual intuition** - Charts and graphs
- **Export capability** - Take data for further analysis

## 💡 Usage Examples

### Understanding Cross-Entropy
1. Set true label = 1.0
2. Slide predicted probability from 0.01 to 0.99
3. **Observe**: Loss explodes as prediction approaches 0
4. **Learn**: Why neural networks avoid confident wrong predictions

### Exploring KL Divergence Asymmetry
1. Set P = Normal(0, 1) and Q = Normal(0.5, 1.5)
2. Note D_KL(P||Q)
3. Click "Swap P ↔ Q"
4. **Observe**: D_KL(Q||P) is different!
5. **Learn**: Direction matters in distribution matching

### Central Limit Theorem Magic
1. Choose "Exponential" (very non-normal!)
2. Set sample size n = 30
3. Start animation
4. **Watch**: Sample means form a perfect bell curve!
5. **Learn**: Why normal distributions appear everywhere

### Hypothesis Testing Decisions
1. Try t-test with sample mean = 10.5, null = 10.0
2. Adjust sample size
3. **Observe**: Larger n → smaller p-value
4. **Learn**: More data → stronger evidence

### Confusion Matrix Trade-offs
1. Load example: "Medical Screening"
2. Note high recall (95%), lower precision
3. Switch to "Spam Filter"
4. **Compare**: Opposite priorities!
5. **Learn**: Different problems need different metrics

### Attention Temperature Effects
1. Load example: "Question Answering"
2. Set temperature = 0.1 (sharp)
3. Switch to temperature = 2.0 (smooth)
4. View entropy plot
5. **Learn**: How temperature controls attention focus

## 📊 Features

✅ **Real-time computation** - All updates instant  
✅ **Parameter exploration** - Sliders and spinboxes everywhere  
✅ **Multiple visualizations** - Bar charts, pie charts, line plots, heatmaps  
✅ **Statistical rigor** - Correct implementations of all formulas  
✅ **Export functionality** - CSV export for all data  
✅ **Example scenarios** - Pre-loaded realistic examples  
✅ **Educational explanations** - Learn WHY, not just HOW  

## 🔬 Technical Details

### Cross-Entropy Implementation
- Numerical stability with epsilon clamping
- Both binary and categorical modes
- Visualization of loss surface

### KL Divergence
- Analytical formulas (Normal-Normal, Exponential-Exponential)
- Numerical integration for arbitrary distributions
- Multiple distribution types supported

### Sampling Visualizer
- True random sampling using Mersenne Twister
- Animated convergence demonstrations
- Histogram generation from samples

### Hypothesis Testing
- Approximations of t-distribution and normal quantiles
- Critical value calculations
- Confidence interval computation
- Multiple test types

### Confusion Matrix
- All standard classification metrics
- Matthews Correlation Coefficient
- Scenario-based learning
- Metric trade-off visualization

### Attention Weights
- Softmax with temperature scaling
- Entropy computation
- Effective token counting
- Multiple visualization modes

## 🎯 Target Audience

- **ML Students**: Build intuition for statistical concepts
- **Practitioners**: Quickly visualize metrics and distributions
- **Educators**: Teaching aid for probability/statistics courses
- **Researchers**: Prototype attention mechanisms, test hypotheses

## 🚀 Future Enhancements

Ideas for expansion:
- [ ] ROC/AUC curve visualizer
- [ ] Bayesian inference explorer
- [ ] ELBO optimization viewer
- [ ] Gradient descent on loss surfaces
- [ ] Monte Carlo methods
- [ ] Markov Chain visualizer
- [ ] Information theory concepts

## 📚 Mathematical Background

All implementations follow standard formulas:

**Cross-Entropy**: `H(p,q) = -Σ p(x) log(q(x))`  
**KL Divergence**: `D_KL(P||Q) = Σ P(x) log(P(x)/Q(x))`  
**Central Limit Theorem**: `(X̄ - μ)/(σ/√n) → N(0,1)`  
**t-statistic**: `t = (x̄ - μ₀)/(s/√n)`  
**Softmax**: `σ(z)ᵢ = exp(zᵢ/τ) / Σⱼ exp(zⱼ/τ)`  

## 🤝 Contributing

This is an educational tool. Suggestions welcome:
- Additional visualizations
- Bug fixes
- Educational improvements
- Documentation enhancements

## 📄 License

MIT License - Free for educational and commercial use

## ✨ Philosophy

> "Understanding comes from exploration, not memorization. Play with parameters. Break assumptions. Build intuition."

**Probability Studio** makes abstract statistical concepts tangible through interactivity.

---

**Built with ❤️ for ML education**

*"Not just what the formulas are - understand why they matter in machine learning!"*

---
date: 2026-05-26
title: "Loss Landscape 3D - Quick Reference Card"
tags: [learning, losslandscape3d]
status: reference
type: reference
---

# Loss Landscape 3D - Quick Reference Card

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to 3D Surface view |
| `Ctrl+2` | Switch to Contour Map |
| `Ctrl+3` | Switch to Gradient Field |
| `Ctrl+4` | Switch to Single Optimizer |
| `Ctrl+5` | Switch to Optimizer Race |
| `Ctrl+S` | Export current view |
| `Ctrl+Q` | Quit application |
| `F1` | Show help |

## 🖱️ Mouse Controls

### 3D Surface View
- **Left Drag**: Rotate surface
- **Scroll**: Zoom in/out
- **Right Click**: Reset view

### 2D Views (Contour, Gradient)
- **Right Drag**: Pan view
- **Scroll**: Zoom in/out
- **Left Click**: Set optimizer start point (contour map)

## 📊 Loss Functions Cheat Sheet

### Rosenbrock: `f(x,y) = (1-x)² + 100(y-x²)²`
- **Global minimum**: (1, 1) → f = 0
- **Challenge**: Narrow parabolic valley
- **Best for**: Testing momentum algorithms
- **Tip**: Try learning rate 0.001-0.01

### Himmelblau: `f(x,y) = (x²+y-11)² + (x+y²-7)²`
- **Global minima**: 4 equivalent minima
  - (3.0, 2.0)
  - (-2.805, 3.131)
  - (-3.779, -3.283)
  - (3.584, -1.848)
- **Challenge**: Multiple local minima
- **Best for**: Testing starting point sensitivity

### Beale: `f(x,y) = (1.5-x+xy)² + (2.25-x+xy²)² + (2.625-x+xy³)²`
- **Global minimum**: (3, 0.5) → f = 0
- **Challenge**: Steep valleys, asymmetric
- **Best for**: Learning rate tuning
- **Tip**: Needs smaller learning rate (~0.001)

### Rastrigin: `f(x,y) = 20 + x² - 10cos(2πx) + y² - 10cos(2πy)`
- **Global minimum**: (0, 0) → f = 0
- **Challenge**: Highly multimodal (many peaks/valleys)
- **Best for**: Testing local minima escape
- **Tip**: Adam often performs best

### Sphere: `f(x,y) = x² + y²`
- **Global minimum**: (0, 0) → f = 0
- **Challenge**: None - convex
- **Best for**: Baseline / sanity check
- **Tip**: All optimizers should converge easily

### Saddle Point: `f(x,y) = x² - y²`
- **Global minimum**: None (saddle at origin)
- **Challenge**: Second-order saddle point
- **Best for**: Demonstrating saddle point problem
- **Tip**: Momentum escapes WAY faster than SGD

## 🔧 Optimizer Tuning Guide

### SGD (Stochastic Gradient Descent)
```
Learning Rate: 0.01 - 0.1
Pros: Simple, predictable
Cons: Slow, stuck at saddles
Best for: Convex functions (Sphere)
```

### Momentum
```
Learning Rate: 0.01 - 0.1
Momentum β: 0.9
Pros: Escapes saddles, faster convergence
Cons: Can overshoot
Best for: Valleys (Rosenbrock)
```

### Adam
```
Learning Rate: 0.001 - 0.01
β₁: 0.9 (momentum)
β₂: 0.999 (RMSprop)
Pros: Adapts per-parameter, robust
Cons: Can converge to bad minima
Best for: Most cases (default choice)
```

### RMSprop
```
Learning Rate: 0.001 - 0.01
Decay ρ: 0.9
Pros: Adaptive learning rate
Cons: No momentum
Best for: Non-stationary objectives
```

### Adagrad
```
Learning Rate: 0.01 - 0.1
Pros: Adapts to sparse features
Cons: Learning rate decays too aggressively
Best for: Sparse data (not these surfaces)
```

### Adadelta
```
Learning Rate: 1.0 (auto-adapted)
Decay ρ: 0.95
Pros: No manual learning rate
Cons: Sometimes slow
Best for: When you don't want to tune LR
```

## 🎓 Educational Experiments

### Experiment 1: Understanding Momentum
```
Surface: Rosenbrock
Optimizers: SGD (lr=0.01) vs Momentum (lr=0.01, β=0.9)
Observation: Momentum is ~5-10x faster
Lesson: Velocity helps in narrow valleys
```

### Experiment 2: Adaptive Learning Rates
```
Surface: Beale
Optimizers: SGD (lr=0.01) vs Adam (lr=0.001)
Observation: SGD overshoots, Adam adapts
Lesson: Different dimensions need different rates
```

### Experiment 3: Saddle Point Escape
```
Surface: Saddle Point
Starting Point: (0.1, 0.1)
Optimizers: SGD vs Momentum
Observation: SGD crawls, Momentum speeds through
Lesson: Second-order saddles are hard for first-order methods
```

### Experiment 4: Multiple Minima
```
Surface: Himmelblau
Action: Run "Optimizer Race" with Random Starts
Observation: Different optimizers find different minima
Lesson: Initial conditions matter!
```

### Experiment 5: Learning Rate Sensitivity
```
Surface: Rosenbrock
Optimizer: SGD
Try: lr=0.0001 (crawls), lr=0.01 (good), lr=0.5 (explodes)
Lesson: LR is critical for convergence
```

## 🐛 Common Issues & Fixes

### Optimizer diverges (loss → infinity)
**Fix**: Reduce learning rate by 10x

### Optimizer makes no progress
**Fix**: Increase learning rate OR switch to Adam/Momentum

### All optimizers get stuck
**Fix**: You found a local minimum! Try Random Starts

### 3D surface looks weird
**Fix**: Some functions have extreme values - this is normal

### Gradient arrows are tiny
**Fix**: Increase arrow size slider in Gradient Field tab

## 💡 Pro Tips

1. **Start with Sphere** - Make sure everything works
2. **Use Rosenbrock** - Classic test for momentum
3. **Try Saddle** - Best demonstration of why momentum matters
4. **Use Random Starts** - For fair optimizer comparison
5. **Lower LR for Adam** - Usually 10x less than SGD
6. **Watch the table** - Race stats show convergence speed
7. **Click on contours** - Set custom starting points
8. **Step through** - Use "Step" button to see each iteration

## 📐 Mathematical Background

### Gradient Descent Update
```
θ_{t+1} = θ_t - α ∇f(θ_t)

θ: Parameters (x, y position)
α: Learning rate
∇f: Gradient (slope direction)
```

### Momentum Update
```
v_t = β v_{t-1} - α ∇f(θ_t)
θ_{t+1} = θ_t + v_t

v: Velocity (accumulated gradient)
β: Momentum coefficient (typically 0.9)
```

### Adam Update
```
m_t = β₁ m_{t-1} + (1-β₁) ∇f(θ_t)    [First moment]
v_t = β₂ v_{t-1} + (1-β₂) (∇f(θ_t))²  [Second moment]

m̂_t = m_t / (1 - β₁^t)                [Bias correction]
v̂_t = v_t / (1 - β₂^t)

θ_{t+1} = θ_t - α m̂_t / (√v̂_t + ε)

Combines momentum + adaptive learning rate
```

## 🎯 Learning Objectives

After using this tool, you should understand:

✅ Why gradient descent minimizes loss (follows steepest descent)  
✅ How momentum accelerates convergence in valleys  
✅ Why adaptive methods (Adam) work across diverse landscapes  
✅ The saddle point problem in high-dimensional optimization  
✅ Why there's no "best" optimizer for all problems  
✅ How learning rate affects convergence speed and stability  

## 📚 Further Reading

- **Adam Paper**: Kingma & Ba (2014) - "Adam: A Method for Stochastic Optimization"
- **Momentum**: Sutskever et al. (2013) - "On the importance of initialization and momentum"
- **RMSprop**: Hinton's Coursera Lecture 6e
- **Optimization Overview**: Ruder (2016) - "An overview of gradient descent optimization algorithms"

---

**Remember**: Visualization helps intuition, but real ML is high-dimensional!
These 2D/3D surfaces are simplified analogies for understanding.

---

## Related Notes
- [[PROJECT_OVERVIEW]] - Shared losslandscape3d/learning focus
- [[UI_REFERENCE]] - Related learning topic
- [[14_Key_Buildings_Reference_Sheet]] - Related learning topic
- [[4774-Structures-Moment-Problems-#3-&-#4-—-ΣM-Verification-(Alternate-Reference-Points]] - Related learning topic
- [[Python Reference & Cheatsheets]] - Related learning topic

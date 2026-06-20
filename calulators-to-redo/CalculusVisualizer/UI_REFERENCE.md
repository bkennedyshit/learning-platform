---
date: 2026-05-26
title: "Calculus Visualizer - UI Feature Reference"
tags: [learning, calculusvisualizer]
status: reference
type: reference
---

# Calculus Visualizer - UI Feature Reference

## 🎨 Complete UI Overview

### Main Window Layout

```
╔══════════════════════════════════════════════════════════════════╗
║  Calculus Visualizer - Educational Tool                    [□][×]║
╠══════════════════════════════════════════════════════════════════╣
║  File | View | Help                                              ║
╠══════════════════════════════════════════════════════════════════╣
║  [📸 Export] [🔄 Reset] [⊞ Grid] │ [🌙 Dark Mode] │ [❓ About]   ║
╠══════════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Function Input                                             │ ║
║  │ f(x) = [________________] [Presets ▼] [Plot]             │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ 📊 Interactive Graph | ∂ Derivative Steps |               │ ║
║  │     🎯 Optimization   | 📐 Tangent Analysis                │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │                                                            │ ║
║  │              [ACTIVE TAB CONTENT HERE]                    │ ║
║  │                                                            │ ║
║  │                                                            │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╠══════════════════════════════════════════════════════════════════╣
║  Ready - Enter a function to visualize                           ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Tab 1: 📊 Interactive Graph

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  f(x) = x³ - 2x     (Blue Line)                            │
│  f'(x) = 3x² - 2    (Green Line)                           │
│                                                             │
│      │                                                      │
│    10├──────────┬──────────┬──────────┬──────────          │
│      │         ╱│╲         │         ╱│                     │
│      │        ╱ │ ╲        │        ╱ │  ← f(x) Blue       │
│      │       ╱  │  ╲       │       ╱  │                     │
│     5├──────/───┼───╲──────┼──────/── │                     │
│      │     ╱    │    ╲     │     ╱    │                     │
│    ──┼────╱─────┼─────╲────┼────╱───  │                     │
│   0  ├───●──────┼──────●───┼───●───── ├─────→              │
│      │    ╲     │     ╱    │    ╲     │    x                │
│   -5 ├─────╲────┼────╱─────┼─────╲─── │                     │
│      │      ╲   │   ╱      │      ╲   │  ← f'(x) Green      │
│  -10 ├───────╲──┼──╱───────┼───────╲─ │                     │
│      │        ╲ │ ╱        │        ╲ │                     │
│      └─────────┴─┴──────────┴──────────┘                     │
│       -5        0         5        10                        │
│                                                              │
│  Right-click: Trace | Drag: Pan | Scroll: Zoom             │
└──────────────────────────────────────────────────────────────┘
```

### Features
- **Blue curve**: Original function f(x)
- **Green curve**: Derivative f'(x)
- **Grid**: Adjustable spacing based on zoom
- **Axes**: X and Y with arrows
- **Legend**: Top-left showing both functions
- **Crosshair**: Right-click to trace points
- **Coordinates**: Display at traced point

### Interactions
| Action | Result |
|--------|--------|
| Left-click drag | Pan the view |
| Mouse wheel up | Zoom in |
| Mouse wheel down | Zoom out |
| Right-click | Trace point, show coordinates |

---

## Tab 2: ∂ Derivative Steps

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│ f(x) = [sin(x^2)___] [Presets ▼] [Calculate d/dx]          │
├──────────────────┬────────────────────────────────────────────┤
│ Rules Reference  │  Step-by-Step Solution                    │
│                  │                                            │
│ 📌 Power Rule    │  🎓 Derivative Calculation                │
│ 📌 Chain Rule    │                                            │
│ 📌 Product Rule  │  Given: f(x) = sin(x²)                    │
│ 📌 Quotient Rule │  ─────────────────────────────────────────│
│                  │                                            │
│ 🔷 Trig:         │  ┌────────────────────────────────────┐   │
│   d/dx[sin(x)]   │  │ Step 1: Identify Composition       │   │
│      = cos(x)    │  │                                    │   │
│                  │  │ This is a composite function:      │   │
│ 🔷 Exponential:  │  │ • Outer: sin(u) where u = x²       │   │
│   d/dx[e^x]      │  │ • Inner: u = x²                    │   │
│      = e^x       │  │                                    │   │
│                  │  │ We need the CHAIN RULE!            │   │
│ 🔷 Special:      │  └────────────────────────────────────┘   │
│   d/dx[1/x]      │                                            │
│      = -1/x²     │  ┌────────────────────────────────────┐   │
│                  │  │ Step 2: Apply Chain Rule          │   │
│                  │  │                                    │   │
│                  │  │ d/dx[f(g(x))] = f'(g(x))·g'(x)    │   │
│                  │  │                                    │   │
│                  │  │ 1. Outer derivative: cos(x²)       │   │
│                  │  │ 2. Inner derivative: 2x            │   │
│                  │  └────────────────────────────────────┘   │
│                  │                                            │
│                  │  ┌────────────────────────────────────┐   │
│                  │  │ Step 3: Final Result              │   │
│                  │  │                                    │   │
│                  │  │ f'(x) = 2x·cos(x²)                │   │
│                  │  │                                    │   │
│                  │  │ 💡 This is how backprop works!    │   │
│                  │  └────────────────────────────────────┘   │
├──────────────────┴────────────────────────────────────────────┤
│ Final Result: f'(x) = 2x·cos(x²)                             │
└──────────────────────────────────────────────────────────────┘
```

### Color Coding
- **Green boxes**: Rule identification
- **Blue boxes**: Application steps
- **Orange boxes**: Final results
- **Purple boxes**: Neural network special cases

### Example Functions
1. `x^2` → Power Rule demo
2. `x^3 - 2*x` → Sum Rule demo
3. `sin(x^2)` → **Chain Rule** (key for backprop!)
4. `exp(-x^2)` → Gaussian derivative
5. `1/(1+exp(-x))` → **Sigmoid** (neural networks!)

---

## Tab 3: 🎯 Optimization

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│ Function: [x^4-4x² ▼] Algorithm: [Gradient Descent ▼]      │
│ Learning Rate: [━━●━━━━━━━] α = 0.10                        │
│ [▶ Start] [⏸ Pause] [↻ Reset]                              │
│ Iteration: 0 │ f(x) = 0.000                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│      50├──────────────────────────────────────────          │
│         │         ╱╲          ╱╲                             │
│      40 │        ╱  ╲        ╱  ╲       ← Surface           │
│         │       ╱    ╲      ╱    ╲                           │
│      30 │      ╱      ╲    ╱      ╲                          │
│         │     ╱        ╲  ╱        ╲                         │
│      20 │    ╱          ╲╱          ╲                        │
│         │   ╱            ●           ╲  ← Path               │
│      10 │  ╱            ●●●           ╲                       │
│         │ ╱           ●●●  ●●          ╲                     │
│       0 ├●●●●●●●●●●●●●      ●●●●●●●●●●●├───→                │
│         │              ╲    ╱            x                   │
│         │-10  -5   ●   0●  5●  10                            │
│                      ╲ ╱╲ ╱                                  │
│         Double Well: Two minima!                             │
│                                                              │
│ Click to set starting point │ ● = Current │ Path in amber   │
├──────────────────────────────────────────────────────────────┤
│ 💡 Try different learning rates to see convergence!         │
└──────────────────────────────────────────────────────────────┘
```

### Algorithms
1. **Gradient Descent**: x -= α·∇f(x)
2. **Momentum**: Adds velocity term
3. **Adam**: Adaptive learning (best for deep learning)

### Functions
- `x^2` - Simple bowl (one minimum)
- `x^4 - 4*x^2` - Double well (two minima!)
- `x^3/3 - x` - Saddle point
- `sin(x) + x^2/10` - Noisy landscape

### Controls
- **Learning rate slider**: 0.01 to 1.00
- **Start**: Begin optimization
- **Pause**: Stop animation
- **Reset**: Return to initial state
- **Click graph**: Set new starting point

### Visualization
- **Orange path**: Optimization trajectory
- **Red pulsing dot**: Current position
- **Blue surface**: Function landscape
- **Dashed contours**: Level sets

---

## Tab 4: 📐 Tangent Analysis

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│      │                                                       │
│    10├────────────────────────────────────────               │
│      │         ╱                                             │
│      │        ╱                                              │
│      │       ╱    ╱                                          │
│     5├──────●────/─────────────  ← Tangent Line             │
│      │     ╱│   ╱          (Orange)                          │
│      │    ╱ │  ╱                                             │
│   0  ├───╱──●─╱────────────────────────────→                │
│      │  ╱   │╱                    x                          │
│   -5 ├─╱────┼─────────────────                               │
│      │╱     │                                                │
│  -10 ├──────┴─────────────────                               │
│      │                                                       │
│      Blue = f(x)  │  Green ● = Point  │  Orange = Tangent   │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ x position: [━━━━●━━━━━] x = 2.00                           │
│ [☐ Normal] [☐ Secant] [▶ Animate]                          │
│ Slope: m = 4.00 │ y = 4.00x - 4.00                          │
├──────────────────────────────────────────────────────────────┤
│ 💡 Click on graph to place tangent or use slider            │
└──────────────────────────────────────────────────────────────┘
```

### Features
- **Tangent line**: Orange dashed line
- **Point of tangency**: Green circle
- **Normal line**: Purple (perpendicular to tangent)
- **Secant line**: Yellow (between nearby points)

### Display Info
- **x position**: Current x-coordinate
- **Slope**: m = f'(x) at that point
- **Equation**: y = mx + b form

### Interactions
| Action | Result |
|--------|--------|
| Click graph | Position tangent |
| Move slider | Fine control |
| Animate button | Auto-sweep tangent |
| Show Normal | Display perpendicular |
| Show Secant | Show nearby secant |

---

## 🎨 Color Scheme (Dark Theme)

### Background Colors
- Main background: `#1e1e1e` (dark gray)
- Widget background: `#2d2d2d` (medium gray)
- Graph background: `#212121` (very dark)

### Accent Colors
- Primary accent: `#0078d4` (Microsoft blue)
- Success: `#4CAF50` (green)
- Warning: `#FF9800` (orange)
- Error: `#f44336` (red)

### Function Colors
- f(x): `#0088FF` (bright blue)
- f'(x): `#43DF65` (bright green)
- Tangent: `#FF5722` (deep orange)
- Path: `#FFC107` (amber)
- Point: `#4CAF50` (green)
- Normal: `#9C27B0` (purple)
- Secant: `#FFEB3B` (yellow)

### Text Colors
- Primary text: `#e0e0e0` (light gray)
- Highlight: `#00ff88` (bright green)
- Links: `#0078d4` (blue)
- Code: `#ffd700` (gold)

---

## 🔤 Typography

### Fonts
- **UI Text**: System default (Segoe UI on Windows)
- **Math/Code**: `Courier New` monospace
- **Headers**: Bold, 14-16pt
- **Body**: Regular, 11-12pt
- **Labels**: 10-11pt

### Styling
- **Bold**: Headers, important values
- **Italic**: Variable names, emphasis
- **Monospace**: Equations, code, derivatives

---

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Plot function |
| **Ctrl+E** | Export graph |
| **Ctrl+R** | Reset view |
| **Ctrl+G** | Toggle grid |
| **Ctrl+D** | Toggle dark mode |
| **F1** | Help/About |
| **Esc** | Stop animation |

---

## 🎯 Preset Functions Quick Reference

### Polynomials
- `x^2` - Parabola (simple)
- `x^3 - 2*x` - Cubic with extrema
- `x^4 - 4*x^2` - Quartic with two minima

### Trigonometric
- `sin(x)` - Sine wave
- `cos(x)` - Cosine wave
- `sin(x^2)` - Chain rule example

### Exponential
- `exp(x)` - Exponential growth
- `exp(-x^2)` - Gaussian (bell curve)

### Neural Network
- `1/(1+exp(-x))` - Sigmoid activation
- `x^3/3 - x` - Common test function

### Other
- `log(x)` - Natural logarithm
- `sqrt(x)` - Square root

---

## 💡 Usage Tips

### For Best Learning:
1. **Start simple**: Begin with `x^2`
2. **See the derivative**: Watch how f'(x) relates to f(x)
3. **Try composition**: Use `sin(x^2)` to see chain rule
4. **Study sigmoid**: Understand neural network activation
5. **Optimize**: Watch gradient descent find minima

### For Chain Rule:
1. Go to Derivative tab
2. Select "sin(x^2)" preset
3. Read step-by-step breakdown
4. Note the outer × inner pattern
5. Apply to backpropagation!

### For Gradient Descent:
1. Go to Optimization tab
2. Select "x^4 - 4*x^2" (double well)
3. Try low learning rate (0.05)
4. Try high learning rate (0.50)
5. Compare Momentum vs Adam

### For Tangent Lines:
1. Go to Tangent Analysis tab
2. Enter `x^3 - 2*x`
3. Click "Animate"
4. Watch slope change
5. Find where slope = 0 (extrema!)

---

## 🚀 Performance Notes

- **Smooth 20-30 FPS** animations
- **High-resolution** plotting (2× pixels)
- **Responsive** interactive controls
- **Efficient** rendering with QPainter
- **Smart** clipping and bounds

---

## 📸 Export

**Export any visualization:**
1. Navigate to desired tab
2. Click "Export" button or File → Export
3. Choose filename
4. PNG image saved at screen resolution

**Use cases:**
- Create study notes
- Include in presentations
- Share with classmates
- Document learning progress

---

This completes the Calculus Visualizer UI reference! 🎓✨

---

## Related Notes
- [[BUILD]] - Shared calculusvisualizer/learning focus
- [[BUILDING]] - Shared calculusvisualizer/learning focus
- [[DERIVATIVE_ENGINE_README]] - Shared calculusvisualizer/learning focus
- [[IMPLEMENTATION_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[PROJECT_SUMMARY]] - Shared calculusvisualizer/learning focus

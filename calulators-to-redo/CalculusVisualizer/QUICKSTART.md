---
date: 2026-05-26
title: "🚀 Quick Start Guide - Calculus Visualizer"
tags: [learning, calculusvisualizer]
status: reference
type: note
---

# 🚀 Quick Start Guide - Calculus Visualizer

Get up and running in 5 minutes!

## ⚡ Fast Track Build

### Windows (PowerShell)
```powershell
cd "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\CalculusVisualizer"
.\build.bat
```

### Linux/macOS (Bash)
```bash
cd "/path/to/CalculusVisualizer"
chmod +x build.sh
./build.sh
```

---

## 📋 Prerequisites Checklist

Before building, ensure you have:

- [ ] **Qt 6.5+** installed
  - Windows: Download from https://www.qt.io/download
  - Linux: `sudo apt install qt6-base-dev qt6-charts-dev`
  - macOS: `brew install qt@6`

- [ ] **SymEngine** library
  - Windows: `vcpkg install symengine:x64-windows`
  - Linux: `sudo apt install libsymengine-dev`
  - macOS: `brew install symengine`

- [ ] **C++20 Compiler**
  - Windows: Visual Studio 2022
  - Linux: GCC 11+ or Clang 14+
  - macOS: Xcode 14+

- [ ] **CMake 3.21+**
  - `cmake --version` to verify

---

## 🎯 First Run Tutorial

### 1. Launch the Application

```bash
# Windows
.\build\Release\CalculusVisualizer.exe

# Linux/macOS  
./build/CalculusVisualizer
```

### 2. Plot Your First Function

1. In the **Expression Input** box, type: `x^2`
2. Click **"Add to Graph"** or press `Enter`
3. See the parabola appear on the graph!

### 3. Compute a Derivative

1. With `x^2` still selected, click **"Compute Derivative (d/dx)"**
2. See the result: `2*x`
3. View step-by-step solution in the panel
4. The derivative (red line) is automatically plotted

### 4. Explore Gradient Descent

1. Click the **"📉 Gradient Descent"** tab
2. Default function is already loaded: `x^2 - 4*x + 3`
3. Click **"▶ Start"** to watch optimization
4. See the point converge to the minimum at x=2

### 5. Understand Chain Rule

1. Click the **"🔗 Chain Rule Explorer"** tab
2. Select example: **"Nested: sin(cos(x))"**
3. Study the decomposition tree
4. Read how it connects to backpropagation

---

## 🎨 Example Expressions to Try

### Basic Functions
```
x^2
x^3 - 2*x
sin(x)
cos(x)
exp(-x^2)
```

### Composite Functions (Great for Chain Rule)
```
sin(x^2)
exp(3*x + 1)
(x^2 + 1)^3
sqrt(1 + x^2)
```

### Neural Network Activations
```
1/(1 + exp(-x))          # Sigmoid
2/(1 + exp(-2*x)) - 1    # Tanh
```

### Optimization Functions
```
x^2 - 4*x + 3           # Simple quadratic
x^4 - 4*x^2             # Double well
x^3 - 3*x               # Local min/max
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New graph |
| `Ctrl+S` | Export graph |
| `Ctrl++` | Zoom in |
| `Ctrl+-` | Zoom out |
| `Ctrl+0` | Reset view |
| `Ctrl+G` | Gradient Descent tab |
| `Ctrl+C` | Chain Rule tab |
| `Enter` | Add expression |

---

## 🐛 Troubleshooting

### Build Fails - "Qt6 not found"

**Fix:**
```bash
# Set Qt path
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/6.5.0/msvc2019_64"
```

### Build Fails - "SymEngine not found"

**Fix for Windows (vcpkg):**
```powershell
vcpkg install symengine:x64-windows
cmake .. -DCMAKE_TOOLCHAIN_FILE="C:/vcpkg/scripts/buildsystems/vcpkg.cmake"
```

**Fix for Linux:**
```bash
sudo apt install libsymengine-dev
```

### Runtime Error - "Platform plugin could not be loaded"

**Fix:** Qt libraries not in PATH
```bash
# Add Qt bin directory to PATH
# Windows: Add C:\Qt\6.5.0\msvc2019_64\bin to PATH
# Linux: export LD_LIBRARY_PATH=/path/to/qt/lib:$LD_LIBRARY_PATH
```

### Expression Parser Error

**Fix:** Use proper syntax
- Use `*` for multiplication: `3*x` not `3x`
- Use `**` or `^` for powers: `x^2` or `x**2`
- Functions need parentheses: `sin(x)` not `sinx`

---

## 📊 Feature Overview

### Calculator Tab
- Add multiple functions
- Zoom/pan with mouse
- Auto-color for each function
- Remove from list to hide
- Export as PNG

### Derivative Engine
- Symbolic differentiation
- Step-by-step solutions
- Chain rule breakdown
- Auto-plotting derivatives

### Gradient Descent
- Visual optimization
- Adjustable learning rate
- Real-time convergence
- Step or continuous mode

### Chain Rule
- Function decomposition
- Visual tree structure
- Backprop connection
- Pre-loaded examples

---

## 💡 Tips for Best Experience

1. **Start Simple**: Begin with `x^2`, then try more complex
2. **Use Presets**: Chain Rule tab has great examples
3. **Watch Animation**: Gradient descent is best at medium speed
4. **Read Steps**: Derivative steps explain the math
5. **Experiment**: Try different learning rates in gradient descent

---

## 📚 Learn More

- **Full Documentation**: See [README.md](Bill's%20Vault/05-Knowledge_Foundation/00%20-%20Learning_Tools/CalculusVisualizer/README.md)
- **Build Details**: See [BUILDING.md](BUILDING.md)
- **Project Info**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🎓 Learning Path

**Week 1:** Basic calculus
- Plot simple functions
- Compute derivatives
- Understand graphical meaning

**Week 2:** Advanced calculus
- Chain rule exploration
- Composite functions
- Multiple functions

**Week 3:** Optimization
- Gradient descent basics
- Learning rate effects
- Convergence behavior

**Week 4:** ML Connection
- Backpropagation math
- Chain rule in neural nets
- Optimization in practice

---

## ✅ Verification Checklist

After first run, verify:

- [ ] Application window opens
- [ ] Can enter and plot `x^2`
- [ ] Derivative computes to `2*x`
- [ ] Gradient descent animates
- [ ] Chain rule tab loads examples
- [ ] Zoom in/out works
- [ ] Export saves PNG file

---

## 🎉 You're Ready!

**Congratulations!** You now have a powerful calculus learning tool.

**Next Steps:**
1. Plot your favorite equation
2. Compute its derivative
3. Try gradient descent on a quadratic
4. Explore composite functions with chain rule
5. Share your insights with others learning ML!

**Happy Learning! 📊🧮📉**

---

## Related Notes
- [[BUILD]] - Shared calculusvisualizer/learning focus
- [[BUILDING]] - Shared calculusvisualizer/learning focus
- [[DERIVATIVE_ENGINE_README]] - Shared calculusvisualizer/learning focus
- [[IMPLEMENTATION_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[PROJECT_SUMMARY]] - Shared calculusvisualizer/learning focus

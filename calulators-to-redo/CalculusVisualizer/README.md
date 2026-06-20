---
date: 2026-05-26
title: "Calculus Visualizer"
tags: [learning, calculusvisualizer]
status: reference
type: index
---

# Calculus Visualizer

A powerful Qt6/C++ application for learning calculus and understanding backpropagation through interactive visualization. Combines the best features of Desmos graphing calculator and TI-Nspire CAS symbolic computation.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Qt6](https://img.shields.io/badge/Qt-6.5+-green)
![C++](https://img.shields.io/badge/C++-20-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

### 📊 Interactive Graphing (Desmos-Style)
- Real-time function plotting with smooth animations
- Multiple functions on the same graph with color coding
- Zoom, pan, and reset view controls
- Export graphs as PNG/PDF
- Dark theme for comfortable viewing

### 🧮 Symbolic Mathematics (TI-Nspire CAS)
- **Symbolic differentiation** with step-by-step solutions
- **Integration** (numerical and symbolic)
- **Equation solving** for finding roots
- **Expression simplification**
- **Chain rule visualization** for composite functions

### 📉 Gradient Descent Visualizer
- Animated optimization showing how gradient descent works
- Adjustable learning rate and iteration count
- Real-time trajectory tracking
- Perfect for understanding neural network training

### 🔗 Chain Rule Explorer
- Interactive breakdown of composite function derivatives
- Visual decomposition tree showing function composition
- Direct connection to backpropagation concepts
- Pre-loaded examples including neural network activation functions

### 💻 System Integration
- System tray icon for quick access
- Background operation support
- Keyboard shortcuts for common operations
- Professional dark theme interface

## 🚀 Quick Start

### Prerequisites

- **Qt6** (6.5.0 or later)
  - Qt Widgets
  - Qt Charts
- **SymEngine** (symbolic math library)
- **CMake** (3.21+) or **qmake**
- **C++20** compatible compiler
  - MSVC 2022 (Windows)
  - GCC 11+ (Linux)
  - Clang 14+ (macOS)

### Installation

#### Windows

```powershell
# Install Qt6
winget install Qt.Qt

# Clone or navigate to project directory
cd "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\CalculusVisualizer"

# Build using the provided script
.\build.bat
```

#### Linux/macOS

```bash
# Install dependencies
# Ubuntu/Debian:
sudo apt install qt6-base-dev qt6-charts-dev libsymengine-dev cmake

# macOS:
brew install qt@6 symengine cmake

# Build
chmod +x build.sh
./build.sh
```

### Manual Build with CMake

```bash
mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH=/path/to/Qt6
cmake --build . --config Release
```

### Manual Build with qmake

```bash
qmake CalculusVisualizer.pro
make
```

## 📖 Usage Guide

### Basic Calculator

1. **Enter an expression** in the input field:
   ```
   x^2 + 3*x - 5
   sin(x)
   exp(-x^2)
   ```

2. **Add to graph** - Click "Add to Graph" or press Enter

3. **Compute derivative** - Select expression and click "Compute Derivative"
   - See step-by-step solution
   - Derivative automatically plots in red

4. **Solve equations** - Find where f(x) = 0

### Gradient Descent

1. Navigate to **"Gradient Descent"** tab
2. Enter a function: `x^2 - 4*x + 3`
3. Set learning rate α (try 0.1)
4. Click **"▶ Start"** to watch the animation
5. Observe how the algorithm finds the minimum

### Chain Rule Explorer

1. Go to **"Chain Rule Explorer"** tab
2. Select an example or enter your own: `sin(x^2)`
3. Click **"Analyze Chain Rule"**
4. Study the decomposition tree and step-by-step breakdown
5. Understand the connection to backpropagation

## 🎓 Educational Applications

### For Calculus Students
- 📐 Visualize derivatives and integrals
- 📚 Learn differentiation rules step-by-step
- 🔍 Understand the chain rule through decomposition
- 📈 See how functions behave graphically

### For Machine Learning Students
- 🧠 Understand gradient descent optimization
- ⚡ Learn backpropagation through chain rule
- 🎯 Visualize loss function minimization
- 📊 Grasp the mathematics behind neural networks

## 🏗️ Architecture

### Project Structure
```
CalculusVisualizer/
├── CMakeLists.txt              # CMake build configuration
├── CalculusVisualizer.pro      # qmake project file
├── build.bat                   # Windows build script
├── build.sh                    # Linux/macOS build script
├── README.md                   # This file
└── src/
    ├── main.cpp                # Application entry point
    ├── MainWindow.h/cpp        # Main calculator window
    ├── DerivativeEngine.h/cpp  # Symbolic math engine
    ├── GraphWidget.h/cpp       # Interactive graphing
    ├── ExpressionParser.h/cpp  # Math expression parser
    ├── GradientDescentVisualizer.h/cpp  # Optimization animation
    └── ChainRuleExplorer.h/cpp # Chain rule breakdown
```

### Key Components

#### DerivativeEngine
Wraps SymEngine for symbolic mathematics:
- Automatic differentiation
- Step-by-step solution generation
- Chain rule breakdown
- Expression simplification

#### GraphWidget
Qt Charts-based interactive plotting:
- Multi-function support
- Zoom/pan controls
- Mouse wheel zoom
- Export capabilities

#### GradientDescentVisualizer
Demonstrates optimization:
- Numerical gradient computation
- Animated descent path
- Configurable parameters
- Convergence detection

#### ChainRuleExplorer
Educational tool for composition:
- Function decomposition tree
- Step-by-step chain rule
- Backpropagation connection
- Interactive examples

## 🎨 Color Scheme

The application uses a professional dark theme optimized for learning:
- **Background:** `#1E1E1E` (Dark gray)
- **Primary:** `#2C5AA0` (Blue)
- **Accent:** `#4A9EFF` (Light blue)
- **Success:** `#00FF00` (Green)
- **Warning:** `#FF9900` (Orange)
- **Text:** `#E6E6E6` (Light gray)

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New graph |
| `Ctrl+S` | Export graph |
| `Ctrl+Q` | Quit application |
| `Ctrl++` | Zoom in |
| `Ctrl+-` | Zoom out |
| `Ctrl+0` | Reset view |
| `Ctrl+G` | Open Gradient Descent |
| `Ctrl+C` | Open Chain Rule Explorer |
| `Enter` | Add expression to graph |

## 🔧 Configuration

### Customizing Learning Rate
Default: 0.1 (adjustable in GUI)

### Graph Resolution
Default: 1000 points per function
Edit `PLOT_POINTS` in `GraphWidget.h` to change

### Animation Speed
Adjustable via slider (10-1000ms per step)

## 🤝 Contributing

This is an educational tool for personal learning. Feel free to:
- Add more calculus functions
- Implement additional differentiation rules
- Enhance the UI/UX
- Add more optimization algorithms
- Create tutorial examples

## 📚 Learning Resources

### Understanding the Code
- **Qt Documentation:** https://doc.qt.io/qt-6/
- **SymEngine:** https://github.com/symengine/symengine
- **Calculus:** Khan Academy, 3Blue1Brown
- **Backpropagation:** Michael Nielsen's Neural Networks book

### Mathematics Covered
- Derivatives (power, product, quotient, chain rules)
- Integration (basic)
- Optimization (gradient descent)
- Composite functions
- Numerical methods

## 📝 TODO / Future Enhancements

- [ ] Implement symbolic integration (SymPy integration)
- [ ] Add 3D surface plotting for multivariable calculus
- [ ] Partial derivatives visualization
- [ ] Hessian matrix computation
- [ ] Newton's method animation
- [ ] Taylor series approximation
- [ ] Fourier series visualization
- [ ] Interactive limits explorer
- [ ] LaTeX export for solutions
- [ ] Save/load session capability

## 🐛 Known Issues

- Integration is limited (computational, not symbolic)
- Complex nested functions may need simplified input
- Very steep gradients can cause numerical instability
- Some SymEngine expressions need preprocessing

## 📄 License

MIT License - Feel free to use for educational purposes

## 👤 Author

Created as an educational tool for learning calculus and understanding the mathematics behind machine learning.

## 🙏 Acknowledgments

- **Qt Framework** - Cross-platform UI
- **SymEngine** - Fast symbolic mathematics
- **Desmos** - Inspiration for graphing interface
- **TI-Nspire** - Inspiration for CAS features
- **3Blue1Brown** - Visualization inspiration

---

**Happy Learning! 📊🧮📉**

*Understanding calculus makes you understand how neural networks really work.*

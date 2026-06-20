---
date: 2026-05-26
title: "Loss Landscape 3D"
tags: [learning, losslandscape3d]
status: reference
type: index
---

# Loss Landscape 3D

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Qt](https://img.shields.io/badge/Qt-6.x-green)
![License](https://img.shields.io/badge/license-MIT-orange)

An **educational visualization tool** for understanding machine learning optimization algorithms. Watch how different optimizers (SGD, Momentum, Adam, RMSprop, etc.) navigate complex loss landscapes in real-time.

## 🎯 Purpose

This application helps students and practitioners **see** and **understand**:
- Why momentum helps escape saddle points
- How adaptive learning rates (Adam, RMSprop) adjust to landscape curvature
- Why some optimizers converge faster on certain surfaces
- The difference between gradient descent and advanced optimizers

## ✨ Features

### 📊 3D Surface Visualization
- Interactive 3D rendering of loss functions
- Rotate, zoom, and explore with mouse
- Color gradients show loss magnitude
- Toggle between mesh and solid surface

### 🗺️ Contour Maps
- 2D level curves with automatic contour detection
- Gradient vector field overlay
- Critical point detection (minima, maxima, saddle points)
- Click to set optimizer starting positions

### ➡️ Gradient Field Viewer
- Quiver plot showing gradient direction
- Magnitude-based color coding
- Adjustable arrow density and size
- Heatmap overlay option

### 🎯 Single Optimizer Mode
- Step-by-step algorithm execution
- Real-time 3D path visualization
- Adjustable learning rate and iteration count
- Educational descriptions of each algorithm

### 🏁 Multi-Optimizer Race
- Compare 6 optimizers simultaneously
- Color-coded paths and trajectories
- Live statistics table (loss, position, iterations)
- Random starting point generation

## 📚 Included Loss Functions

| Function | Characteristics | Teaching Purpose |
|----------|----------------|------------------|
| **Rosenbrock** | Narrow valley, banana-shaped | Shows why momentum helps |
| **Himmelblau** | 4 local minima | Tests global vs local search |
| **Beale** | Steep valley, asymmetric | Challenges learning rate tuning |
| **Rastrigin** | Many local minima | Tests escape from local optima |
| **Sphere** | Simple convex bowl | Baseline - all optimizers work |
| **Saddle** | x² - y² surface | Illustrates saddle point problem |

## 🔧 Supported Optimizers

1. **SGD (Stochastic Gradient Descent)**
   - Basic: `θ = θ - α∇f(θ)`
   - Simple but can get stuck in saddle points

2. **Momentum**
   - Adds velocity: `v = βv - α∇f(θ)`
   - Helps escape saddle points and accelerates convergence

3. **Adam (Adaptive Moment Estimation)**
   - Combines momentum and adaptive learning rates
   - Usually the best choice for deep learning

4. **RMSprop**
   - Adapts learning rate per parameter
   - Good for non-stationary objectives

5. **Adagrad**
   - Accumulates squared gradients
   - Great for sparse data

6. **Adadelta**
   - Extension of Adagrad with learning rate decay
   - No manual learning rate needed

## 🚀 Quick Start

### Prerequisites

- **Qt 6.x** (Qt 6.2 or higher recommended)
- **CMake 3.16+**
- **C++17 compatible compiler**
  - MSVC 2019+ (Windows)
  - GCC 9+ (Linux)
  - Clang 10+ (macOS)

### Windows Build

```powershell
# 1. Install Qt 6 from https://www.qt.io/download

# 2. Clone/download this project
cd LossLandscape3D

# 3. Create build directory
mkdir build
cd build

# 4. Configure with CMake (adjust Qt path if needed)
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/6.7.0/msvc2019_64"

# 5. Build
cmake --build . --config Release

# 6. Run
Release\LossLandscape3D.exe
```

### Linux Build

```bash
# Install Qt 6
sudo apt install qt6-base-dev qt6-datavisualization-dev

# Build
mkdir build && cd build
cmake ..
make -j$(nproc)

# Run
./LossLandscape3D
```

### macOS Build

```bash
# Install Qt 6 via Homebrew
brew install qt@6

# Build
mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH=$(brew --prefix qt@6)
make -j$(sysctl -n hw.ncpu)

# Run
open LossLandscape3D.app
```

## 📖 Usage Guide

### Basic Workflow

1. **Select a Loss Function**
   - Use the dropdown in the 3D Surface tab
   - Try Rosenbrock first to see the famous valley

2. **Explore the Surface**
   - **3D Surface**: Rotate with left mouse drag, zoom with scroll
   - **Contour Map**: Right-click drag to pan, scroll to zoom
   - **Gradient Field**: See arrows pointing to steepest descent

3. **Run an Optimizer**
   - Go to "Single Optimizer" tab
   - Choose an optimizer (try Momentum vs SGD on Rosenbrock)
   - Click "Start" and watch the path
   - Adjust learning rate to see effects

4. **Compare Algorithms**
   - Go to "Optimizer Race" tab
   - Click "Random Starts" for fair starting positions
   - Click "Start Race" to see all algorithms compete
   - Check the statistics table to see which converged fastest

### Educational Experiments

#### Experiment 1: Momentum vs SGD on Saddle Points
```
Function: Saddle Point (x² - y²)
Optimizers: SGD vs Momentum
Observation: Momentum escapes the saddle ~10x faster
```

#### Experiment 2: Learning Rate Effects
```
Function: Rosenbrock
Optimizer: SGD
Try: lr=0.001 (slow), lr=0.01 (good), lr=0.1 (diverges)
```

#### Experiment 3: Multiple Minima
```
Function: Himmelblau (4 minima at different positions)
Action: Use Random Starts with all 6 optimizers
Observation: Different starting points → different minima
```

## 🎓 Educational Insights

### Why Momentum Works
Watch Momentum on **Rosenbrock**:
- Builds velocity in the valley direction
- Oscillates less than plain SGD
- Converges ~5-10x faster

### Why Adam is Popular
Watch Adam on **Rastrigin**:
- Adapts learning rate per dimension
- Navigates both steep and flat regions
- Usually reaches lower loss than SGD

### The Saddle Point Problem
Watch SGD vs Momentum on **Saddle**:
- SGD slows down near saddle (gradient → 0)
- Momentum carries through with accumulated velocity
- Essential for deep neural networks!

## 🏗️ Architecture

```
LossLandscape3D/
├── src/
│   ├── main.cpp                  # Application entry point
│   ├── MainWindow.h/cpp          # Main window & tab coordination
│   ├── Surface3DWidget.h/cpp     # 3D surface with QtDataVisualization
│   ├── ContourWidget.h/cpp       # 2D contour plot with marching squares
│   ├── GradientFieldWidget.h/cpp # Quiver plot (vector field)
│   ├── OptimizationPath3D.h/cpp  # Single optimizer with animation
│   └── MultiOptimizer.h/cpp      # Multi-algorithm comparison
├── CMakeLists.txt                # Build configuration
└── README.md                     # This file
```

## 🔬 Technical Details

### Loss Function Evaluation
- Numerical gradient: central difference `∇f ≈ (f(x+h) - f(x-h)) / 2h`
- Step size: `h = 0.001`
- Gradients clamped to prevent overflow

### Contour Generation
- Modified marching squares algorithm
- Exponential spacing for better level curve distribution
- Automatic min/max detection

### 3D Rendering
- Qt Data Visualization framework
- Surface mesh with color gradient
- Real-time rotation and zoom

### Optimizer Implementations
All optimizers match standard ML library implementations:
- Adam follows: Kingma & Ba (2014)
- Momentum uses Nesterov acceleration option
- RMSprop matches Hinton's lecture notes

## 🐛 Troubleshooting

### "Qt6 not found" error
```bash
# Specify Qt path explicitly
cmake .. -DCMAKE_PREFIX_PATH="/path/to/Qt/6.x.x/compiler"
```

### Windows: Missing DLL errors
```bash
# Run windeployqt (should be automatic, but manual option:)
cd build/Release
windeployqt LossLandscape3D.exe
```

### 3D view is black
- Update graphics drivers
- Check OpenGL support: `glxinfo | grep OpenGL` (Linux)

### Optimizers diverge immediately
- Reduce learning rate (try 0.001 for Adam, 0.01 for SGD)
- Some functions like Rastrigin need smaller steps

## 📝 TODO / Future Features

- [ ] Custom loss function input (via expression parser)
- [ ] Export optimization paths to CSV
- [ ] 3D path overlay on surface (custom items)
- [ ] Adaptive learning rate visualization
- [ ] Batch vs stochastic gradient modes
- [ ] Second-order methods (Newton, L-BFGS)
- [ ] Loss landscape cross-sections
- [ ] Animation export to video

## 🤝 Contributing

This is an educational tool - improvements welcome!

**Ideas for contributions:**
- Add more loss functions (Styblinski-Tang, Ackley, etc.)
- Implement Nesterov Accelerated Gradient
- Add noise to gradients (stochastic simulation)
- Improve 3D path visualization
- Add dark mode

## 📄 License

MIT License - Feel free to use for teaching, learning, or research.

## 🙏 Acknowledgments

- **Qt Framework** - Cross-platform UI and 3D visualization
- **Optimizer Papers** - Kingma & Ba (Adam), Tieleman & Hinton (RMSprop)
- **Test Functions** - Classic optimization benchmarks

## 📧 Contact

Built for educational purposes to help students understand ML optimization.

**Using this in a course?** Let me know - I'd love to hear about it!

---

**Happy Optimizing! 🚀**

*Remember: There's no "best" optimizer - it depends on the landscape!*

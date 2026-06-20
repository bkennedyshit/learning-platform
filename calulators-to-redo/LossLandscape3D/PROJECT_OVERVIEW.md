---
date: 2026-05-26
title: "Loss Landscape 3D - Project Overview"
tags: [learning, losslandscape3d]
status: reference
type: note
---

# Loss Landscape 3D - Project Overview

## 📁 Complete File Structure

```
LossLandscape3D/
├── src/
│   ├── main.cpp                     # Application entry point
│   ├── MainWindow.h                 # Main window header
│   ├── MainWindow.cpp               # Main window implementation
│   ├── Surface3DWidget.h            # 3D surface visualization header
│   ├── Surface3DWidget.cpp          # 3D surface implementation
│   ├── ContourWidget.h              # 2D contour plot header
│   ├── ContourWidget.cpp            # 2D contour plot implementation
│   ├── GradientFieldWidget.h        # Gradient field viewer header
│   ├── GradientFieldWidget.cpp      # Gradient field implementation
│   ├── OptimizationPath3D.h         # Single optimizer header
│   ├── OptimizationPath3D.cpp       # Single optimizer implementation
│   ├── MultiOptimizer.h             # Multi-optimizer race header
│   └── MultiOptimizer.cpp           # Multi-optimizer race implementation
├── CMakeLists.txt                   # Build configuration
├── build.ps1                        # Windows build script
├── build.sh                         # Linux/macOS build script
├── README.md                        # Full documentation
├── QUICK_REFERENCE.md               # Quick reference guide
└── .gitignore                       # Git ignore rules
```

## 🎯 Component Overview

### 1. Surface3DWidget (2 files: .h/.cpp)
**Purpose**: Interactive 3D visualization of loss functions

**Features**:
- ✅ 6 predefined loss functions (Rosenbrock, Himmelblau, Beale, Rastrigin, Sphere, Saddle)
- ✅ Mouse rotation and zoom
- ✅ Color gradient by height (blue=low, red=high)
- ✅ Toggle mesh/solid surface
- ✅ Adjustable resolution (20-100 points)
- ✅ Smooth/flat shading options

**Key Methods**:
- `setLossFunction(name)` - Change loss function
- `updateSurface()` - Recompute surface data
- Static functions for each loss type

**Lines of Code**: ~450

---

### 2. ContourWidget (2 files: .h/.cpp)
**Purpose**: 2D contour plot with gradient overlay

**Features**:
- ✅ Automatic contour level detection (20 levels)
- ✅ Marching squares algorithm for contours
- ✅ Gradient vector field (quiver plot)
- ✅ Critical point detection (minima, maxima, saddle points)
- ✅ Mouse pan and zoom
- ✅ Click to set optimizer start points

**Key Methods**:
- `computeContours()` - Generate level curves
- `computeGradient()` - Create vector field
- `findCriticalPoints()` - Detect min/max/saddle
- `worldToScreen()` / `screenToWorld()` - Coordinate transforms

**Lines of Code**: ~550

---

### 3. GradientFieldWidget (2 files: .h/.cpp)
**Purpose**: Dedicated gradient vector field visualization

**Features**:
- ✅ Quiver plot (arrows showing grad direction)
- ✅ Color modes: Uniform, Magnitude, Direction
- ✅ Adjustable arrow density (10-50)
- ✅ Arrow size control
- ✅ Optional magnitude heatmap overlay
- ✅ Normalize arrow lengths option
- ✅ Color legend

**Key Methods**:
- `computeGradientField()` - Generate arrow grid
- `drawQuiverPlot()` - Render arrows with colors
- `magnitudeToColor()` - Map gradient magnitude to color

**Lines of Code**: ~480

---

### 4. OptimizationPath3D (2 files: .h/.cpp)
**Purpose**: Single optimizer with animated path on 3D surface

**Features**:
- ✅ 4 optimizer types: SGD, Momentum, Adam, RMSprop
- ✅ Adjustable learning rate
- ✅ Animation with speed control
- ✅ Step-by-step execution
- ✅ Real-time statistics (iteration, loss, position)
- ✅ Educational descriptions for each algorithm
- ✅ Convergence detection

**Key Methods**:
- `performOptimizationStep()` - Execute one iteration
- `start()` / `pause()` / `reset()` / `step()` - Controls
- Algorithm-specific state (velocity, moments, cache)

**Optimizers Implemented**:
1. **SGD**: θ = θ - α∇f
2. **Momentum**: v = βv - α∇f, θ = θ + v
3. **Adam**: First + second moment with bias correction
4. **RMSprop**: Adaptive learning rate per parameter

**Lines of Code**: ~420

---

### 5. MultiOptimizer (2 files: .h/.cpp)
**Purpose**: Compare 6 optimizers simultaneously (race mode)

**Features**:
- ✅ 6 pre-configured optimizers with different colors
- ✅ Enable/disable individual optimizers
- ✅ Random starting point generation
- ✅ Live statistics table (position, loss, iterations, status)
- ✅ 2D path visualization on contour background
- ✅ Race animation with speed control
- ✅ Winner detection (lowest loss)
- ✅ 6 optimizer types: SGD, Momentum, Adam, RMSprop, Adagrad, Adadelta

**Key Methods**:
- `startRace()` - Begin multi-optimizer race
- `performOptimizationStep(opt)` - Update one optimizer
- `setRandomStartPoints()` - Fair comparison setup
- `updateTable()` - Refresh statistics display

**Additional Optimizers**:
5. **Adagrad**: Accumulates squared gradients
6. **Adadelta**: Extension of Adagrad with learning rate decay

**Lines of Code**: ~620

---

### 6. MainWindow (2 files: .h/.cpp)
**Purpose**: Coordinate all components in tabbed interface

**Features**:
- ✅ 5 tabs for different views
- ✅ Menu bar (File, View, Help)
- ✅ Function synchronization across tabs
- ✅ Keyboard shortcuts (Ctrl+1-5)
- ✅ Export view to image
- ✅ Status bar updates
- ✅ About dialog
- ✅ User guide dialog

**Tabs**:
1. 📊 3D Surface - Interactive surface plot
2. 🗺️ Contour Map - Level curves + gradients
3. ➡️ Gradient Field - Vector field quiver plot
4. 🎯 Single Optimizer - One algorithm analysis
5. 🏁 Optimizer Race - Multi-algorithm comparison

**Lines of Code**: ~380

---

### 7. main.cpp (1 file)
**Purpose**: Application entry point

**Features**:
- ✅ Qt application initialization
- ✅ OpenGL surface format configuration
- ✅ Application metadata

**Lines of Code**: ~40

---

## 📊 Statistics

| Component | Files | Lines of Code | Complexity |
|-----------|-------|---------------|------------|
| Surface3DWidget | 2 | ~450 | Medium |
| ContourWidget | 2 | ~550 | High |
| GradientFieldWidget | 2 | ~480 | Medium |
| OptimizationPath3D | 2 | ~420 | Medium |
| MultiOptimizer | 2 | ~620 | High |
| MainWindow | 2 | ~380 | Medium |
| main.cpp | 1 | ~40 | Low |
| **TOTAL** | **13** | **~2,940** | **-** |

## 🔧 Build System

### CMakeLists.txt
- Qt6 integration
- Auto MOC/RCC/UIC
- Windows deployment support
- Cross-platform configuration

### Build Scripts
- **build.ps1**: Windows PowerShell script
- **build.sh**: Linux/macOS Bash script
- Auto-detect Qt installation
- One-command build process

## 📚 Documentation

### README.md (Comprehensive)
- Feature overview
- Installation instructions (Windows/Linux/macOS)
- Usage guide
- Educational experiments
- Troubleshooting
- TODO list

### QUICK_REFERENCE.md
- Keyboard shortcuts
- Loss function formulas and properties
- Optimizer tuning guide
- Common issues and fixes
- Educational experiments
- Mathematical background
- Pro tips

## 🎓 Educational Value

### What Students Learn

1. **Visual Understanding**
   - See gradients as arrows pointing downhill
   - Understand why loss decreases following gradients
   - Observe saddle points and local minima

2. **Algorithm Comparison**
   - SGD vs Momentum on Rosenbrock valley
   - Why Adam adapts better than SGD
   - Saddle point escape demonstration

3. **Hyperparameter Effects**
   - Learning rate too high → divergence
   - Learning rate too low → slow convergence
   - Optimal learning rate visualization

4. **Landscape Properties**
   - Convex (Sphere) vs non-convex (Rastrigin)
   - Multiple minima (Himmelblau)
   - Saddle points (critical but not extrema)

### Recommended Teaching Flow

1. **Week 1**: Start with Sphere (convex)
   - All optimizers work
   - Learning rate effects

2. **Week 2**: Rosenbrock (valley)
   - Momentum beats SGD
   - Learning rate sensitivity

3. **Week 3**: Saddle Point
   - Why momentum matters
   - Second-order optimization preview

4. **Week 4**: Rastrigin (many minima)
   - Local vs global optimization
   - Why initialization matters

5. **Week 5**: Multi-optimizer race
   - Compare all algorithms
   - No "best" optimizer for all cases

## 🚀 Key Innovations

### Technical
1. **Marching Squares** for contour generation
2. **Numerical gradient** with central difference
3. **Real-time animation** with Qt timers
4. **Coordinate transformation** for pan/zoom
5. **Gradient-based coloring** in all views

### Educational
1. **6 classic test functions** from optimization literature
2. **6 modern optimizers** used in deep learning
3. **Side-by-side comparison** mode
4. **Interactive exploration** vs static textbook figures
5. **Instant feedback** on parameter changes

## 🔄 Data Flow

```
User selects function
        ↓
MainWindow updates all tabs
        ↓
Each widget receives:
  - LossFunction callback
  - Bounds (minX, maxX, minY, maxY)
        ↓
Widgets compute:
  - Surface points (3D)
  - Contour levels (2D)
  - Gradient field (vectors)
        ↓
User starts optimization
        ↓
Timer triggers steps
        ↓
Optimizers update positions
        ↓
Paths accumulate
        ↓
Visualization refreshes
```

## 🎨 Visual Design

### Color Schemes

**3D Surface**:
- Blue (low loss) → Green → Yellow → Red (high loss)

**Contours**:
- Hue-based: 0.6 (blue) → 0.0 (red)

**Gradient Field**:
- Magnitude: Blue → Cyan → Green → Yellow → Red
- Direction: Hue = angle / 2π

**Optimizer Paths**:
- SGD: Red
- Momentum: Blue
- Adam: Green
- RMSprop: Orange
- Adagrad: Purple
- Adadelta: Pink

## 🧪 Testing Recommendations

### Functional Tests
1. All 6 functions render correctly
2. Each optimizer converges on Sphere
3. Momentum faster than SGD on Rosenbrock
4. Adam adapts learning rate automatically
5. Multi-optimizer race completes

### Edge Cases
1. Extreme learning rates (0.0001, 10.0)
2. Maximum iterations reached
3. Convergence threshold detection
4. Window resize during animation
5. Function switch during optimization

## 🎯 Success Metrics

**For Students**:
- ✅ Can explain why momentum helps
- ✅ Understand adaptive learning rates
- ✅ Recognize saddle points visually
- ✅ Connect 2D/3D visualization to high-D ML

**For Instructors**:
- ✅ Engage students with interactive demo
- ✅ Replace static slides with live exploration
- ✅ Hands-on homework assignments
- ✅ Research project starting point

## 🌟 Standout Features

1. **Complete Implementation** - Not a prototype, production-ready
2. **Educational Focus** - Help text explains WHY, not just WHAT
3. **Cross-Platform** - Windows, Linux, macOS support
4. **Modern Qt** - Uses Qt6 and latest best practices
5. **Well Documented** - README + Quick Reference
6. **Extensible** - Easy to add new functions or optimizers

## 🔮 Future Enhancements

**High Priority**:
- [ ] 3D path overlay on surface (custom Qt3D items)
- [ ] Export paths to CSV for analysis
- [ ] Second-order methods (Newton, L-BFGS)

**Medium Priority**:
- [ ] Custom function parser (user-defined f(x,y))
- [ ] Batch vs mini-batch simulation
- [ ] Learning rate schedules (decay, warmup)

**Low Priority**:
- [ ] Animation export to video
- [ ] Dark theme
- [ ] More test functions (Ackley, Styblinski-Tang)

---

**Total Development Estimate**: 15-20 hours for experienced Qt developer

**Perfect for**:
- University ML courses
- Online learning platforms
- Self-study optimization
- Research visualization

**License**: MIT - Free for educational and commercial use

---

## Related Notes
- [[QUICK_REFERENCE]] - Shared losslandscape3d/learning focus
- [[PROJECT_SUMMARY]] - Related learning topic
- [[01 - Design Thinking Overview]] - Related learning topic
- [[01 - Technical Writing Overview]] - Related learning topic
- [[22 - BIM Project Delivery]] - Related learning topic

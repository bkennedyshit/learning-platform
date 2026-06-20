---
date: 2026-05-26
title: "Matrix Commander - 2D Visualization System"
tags: [learning, matrixcommander]
status: reference
type: note
---

# Matrix Commander - 2D Visualization System

## Overview

This visualization system provides educational, interactive tools for understanding linear algebra transformations, specifically designed for AI/ML learning. The system includes two main components:

1. **VectorVisualizer** - For visualizing 2D vectors and matrix transformations
2. **EigenVisualizer** - For visualizing eigenvalues and eigenvectors

## Features

### VectorVisualizer

#### Core Features
- ✅ Plot 2D vectors as arrows on a coordinate grid
- ✅ Animate matrix transformations (before → after)
- ✅ Show how basis vectors (î, ĵ) transform
- ✅ Color-coded vectors (original vs transformed)
- ✅ Interactive grid with axis labels and tick marks
- ✅ Smooth animations with adjustable speed
- ✅ Zoom and pan with mouse
- ✅ Export visualizations as PNG (high resolution)

#### Educational Value
- **See transformations in action**: Watch how rotation, scaling, and shear affect vectors
- **Understand basis vectors**: See how the standard basis transforms
- **Multiple vectors**: Add many vectors to see patterns in transformations
- **Visual comparison**: Original vectors shown as dashed lines during transformation

### EigenVisualizer  

#### Core Features
- ✅ Calculate and display 2x2 matrix eigenvalues/eigenvectors
- ✅ Visualize eigenvectors as special direction arrows
- ✅ Show eigenspaces (lines through eigenvectors)
- ✅ Color-coded by eigenvalue magnitude (expanding = red, contracting = blue)
- ✅ Display eigenvalues as scaling factors
- ✅ Comparison mode - show non-eigenvectors for contrast
- ✅ Handle complex eigenvalues (displays warning - no real eigenvectors)
- ✅ Interactive zoom/pan
- ✅ Export as PNG

#### Educational Value
- **Eigenvector insight**: Visually understand that eigenvectors only get scaled, not rotated
- **Eigenvalue meaning**: See the scaling factor in action
- **Special directions**: Understand why eigenvectors are "special"
- **Comparison mode**: See how regular vectors behave differently
- **Real vs Complex**: Understand when matrices have real eigenvectors (and when they don't!)

## User Interface

### VectorVisualizer Controls

**Animation Controls:**
- **▶ Play Animation** - Animates the transformation from original to transformed vectors
- **Speed Slider** - Adjust animation duration (100ms - 3000ms)
- **Reset View** - Return to default zoom and pan
- **Export PNG** - Save current visualization as high-res image

**Display Options:**
- **Show Grid** - Toggle coordinate grid
- **Show Basis Vectors** - Toggle î and ĵ vectors
- **Show Original** - Toggle original (pre-transformation) vectors
- **Show Transformed** - Toggle transformed vectors

**Mouse Controls:**
- **Mouse Wheel** - Zoom in/out
- **Left Click + Drag** - Pan the view
- Bottom status bar shows current zoom level and vector count

### EigenVisualizer Controls

**Main Controls:**
- **Calculate Eigenvalues** - Computes eigenvalues/eigenvectors for current matrix
- **Mode Dropdown:**
  - *Eigenvectors Only* - Show just the eigenvectors
  - *With Transformation* - Show before/after transformation
  - *Comparison View* - Add regular vectors to contrast behavior
- **Reset View** - Return to default zoom/pan
- **Export PNG** - Save visualization

**Display Options:**
- **Show Grid** - Toggle coordinate grid
- **Show Eigenspaces** - Toggle eigenspace lines
- **Show Comparison Vectors** - Toggle non-eigenvectors
- **Show Scaling Factors** - Toggle eigenvalue information overlay

**Mouse Controls:**
- Same as VectorVisualizer (wheel zoom, drag pan)

## API Reference

### VectorVisualizer Class

#### Public Methods

```cpp
// Vector Management
void addVector(double x, double y, const QColor &color = Qt::blue);
void clearVectors();
void setVectors(const QVector<QPointF> &vectors);

// Transformation
void setTransformationMatrix(const Matrix &matrix);  // Must be 2x2
void applyTransformation();
void resetTransformation();
void animateTransformation(int durationMs = 1000);

// View Control
void resetView();
void setZoom(double zoom);
void centerView();

// Export
bool exportToPNG(const QString &filePath, int width = 800, int height = 800);

// Display Options
void setShowGrid(bool show);
void setShowBasisVectors(bool show);
void setShowTransformed(bool show);
void setShowOriginal(bool show);
```

#### Signals

```cpp
void vectorClicked(int index, QPointF position);
void transformationComplete();
```

### EigenVisualizer Class

#### Public Methods

```cpp
// Matrix Management
void setMatrix(const Matrix &matrix);  // Must be 2x2
void clearMatrix();

// Manual Eigenvalue Setting (if computed externally)
void setEigenData(const QVector<std::complex<double>> &eigenvalues,
                  const QVector<QPointF> &eigenvectors);

// Comparison Vectors
void addComparisonVector(double x, double y);
void clearComparisonVectors();

// View Control
void resetView();
void setZoom(double zoom);

// Export
bool exportToPNG(const QString &filePath, int width = 800, int height = 800);

// Display Options
void setShowGrid(bool show);
void setShowEigenspaces(bool show);
void setShowComparisonVectors(bool show);
void setShowScalingFactors(bool show);
```

#### Signals

```cpp
void eigenDataCalculated(int numRealEigenvalues);
void matrixChanged();
```

## Usage Examples

### Example 1: Basic Vector Visualization

```cpp
VectorVisualizer *viz = new VectorVisualizer();
viz->addVector(2.0, 1.0, Qt::blue);
viz->addVector(-1.0, 2.0, Qt::red);
viz->show();
```

### Example 2: Rotation Transformation

```cpp
VectorVisualizer *viz = new VectorVisualizer();
viz->addVector(1.0, 0.0);
viz->addVector(0.0, 1.0);

Matrix rotation(2, 2);
double angle = M_PI / 4;  // 45 degrees
rotation.setValue(0, 0, cos(angle));
rotation.setValue(0, 1, -sin(angle));
rotation.setValue(1, 0, sin(angle));
rotation.setValue(1, 1, cos(angle));

viz->setTransformationMatrix(rotation);
viz->animateTransformation(2000);  // 2 second animation
viz->show();
```

### Example 3: Eigenvalue Visualization

```cpp
EigenVisualizer *eigenViz = new EigenVisualizer();

Matrix matrix(2, 2);
matrix.setValue(0, 0, 3.0);  // Diagonal matrix
matrix.setValue(0, 1, 0.0);
matrix.setValue(1, 0, 0.0);
matrix.setValue(1, 1, 0.5);

eigenViz->setMatrix(matrix);  // Auto-calculates eigenvalues
eigenViz->show();
```

### Example 4: Comparison Mode (See the Difference)

```cpp
EigenVisualizer *eigenViz = new EigenVisualizer();

// Set matrix
Matrix shear(2, 2);
shear.setValue(0, 0, 1.0);
shear.setValue(0, 1, 1.0);
shear.setValue(1, 0, 0.0);
shear.setValue(1, 1, 1.0);

eigenViz->setMatrix(shear);

// Add comparison vectors (not eigenvectors)
eigenViz->addComparisonVector(1.0, 1.0);
eigenViz->addComparisonVector(1.0, -1.0);
eigenViz->setShowComparisonVectors(true);

eigenViz->show();
```

## Educational Use Cases

### 1. Understanding Linear Transformations

Use VectorVisualizer to demonstrate:
- **Rotation**: Vectors change direction but preserve length
- **Scaling**: Vectors change length but preserve direction  
- **Shear**: Vectors slide parallel to an axis
- **Reflection**: Vectors flip across an axis

### 2. Learning About Eigenvectors

Use EigenVisualizer to show:
- Eigenvectors stay on the same line after transformation
- Other vectors both rotate AND scale
- Eigenvalues tell you the scaling factor
- Not all matrices have real eigenvectors (pure rotations)

### 3. Principal Component Analysis (PCA)

Eigenvectors of the covariance matrix point in directions of maximum variance:

```cpp
// Covariance matrix from data
Matrix cov(2, 2);
cov.setValue(0, 0, 1.5);
cov.setValue(0, 1, 0.8);
cov.setValue(1, 0, 0.8);
cov.setValue(1, 1, 1.2);

eigenViz->setMatrix(cov);
// Eigenvectors are the principal components!
// Larger eigenvalue → direction of most variance
```

### 4. Understanding ML Transformations

Many ML operations are linear transformations:
- **Whitening** (decorrelation)
- **Feature scaling**
- **Dimensionality reduction**
- **Data augmentation** (rotation, flip)

## Color Coding

### VectorVisualizer
- **Blue (lighter)**: Original vectors (dashed)
- **Red**: Transformed vectors (solid)
- **Green**: i-hat basis vector
- **Orange**: j-hat basis vector
- **Gray**: Grid and axes

### EigenVisualizer
- **Red**: Eigenvectors with eigenvalue > 1 (expanding)
- **Blue**: Eigenvectors with eigenvalue < 1 (contracting)
- **Dark Gray**: Eigenvectors with eigenvalue ≈ 0 (collapsing)
- **Light Gray**: Comparison vectors (non-eigenvectors)
- **Dashed Lines**: Eigenspaces

## Tips and Best Practices

### Getting Started
1. Start simple - visualize 1-2 vectors first
2. Use the animation to see transformations smoothly
3. Toggle between original and transformed views
4. Zoom in/out to see details

### For Teaching
1. Show basis vectors to explain how the coordinate system transforms
2. Use multiple vectors to show patterns
3. Export to PNG for presentations or documentation
4. Compare eigenvectors with regular vectors

### Performance
- The visualizers handle 20-30 vectors well
- For more vectors, consider reducing animation detail
- Export uses separate rendering, so you can export at any resolution

### Understanding Results

**VectorVisualizer:**
- If vectors rotate, the matrix has a rotation component
- If vectors all point to a line, the transformation is degenerate (det = 0)
- Basis vectors show how the unit square transforms

**EigenVisualizer:**
- "EXPANDING" means eigenvalue magnitude > 1
- "CONTRACTING" means eigenvalue magnitude < 1  
- "COLLAPSING" means eigenvalue ≈ 0 (singular matrix)
- No eigenvectors displayed? Matrix likely has complex eigenvalues (rotation)

## Integration with Matrix Commander

Add to your main window:

```cpp
// In MainWindow.h
private:
    VectorVisualizer *vectorViz;
    EigenVisualizer *eigenViz;

// In MainWindow.cpp constructor
vectorViz = new VectorVisualizer(this);
eigenViz = new EigenVisualizer(this);

// Add menu actions
QAction *visualizeAction = new QAction("Visualize Transformation", this);
connect(visualizeAction, &QAction::triggered, [this]() {
    Matrix matrix = getSelectedMatrix();
    vectorViz->setTransformationMatrix(matrix);
    vectorViz->animateTransformation(1500);
    vectorViz->show();
});

QAction *eigenAction = new QAction("Eigenvalue Analysis", this);
connect(eigenAction, &QAction::triggered, [this]() {
    Matrix matrix = getSelectedMatrix();
    eigenViz->setMatrix(matrix);
    eigenViz->show();
});
```

## Building

The visualization files are automatically included if you use CMake or qmake:

**CMakeLists.txt:**
```cmake
add_executable(MatrixCommander
    src/main.cpp
    src/MainWindow.cpp
    src/VectorVisualizer.cpp
    src/EigenVisualizer.cpp
    # ... other files
)
```

**MatrixCommander.pro:**
```qmake
SOURCES += \
    src/main.cpp \
    src/MainWindow.cpp \
    src/VectorVisualizer.cpp \
    src/EigenVisualizer.cpp \
    # ... other files

HEADERS += \
    src/MainWindow.h \
    src/VectorVisualizer.h \
    src/EigenVisualizer.h \
    # ... other files
```

## Dependencies

- **Qt 5.x or 6.x** - Core, Gui, Widgets modules  
- **C++11 or later**
- **MatrixEngineAdapter** - For Matrix class (already in project)

## Technical Details

### Coordinate Systems

Both visualizers use:
- **World coordinates**: Standard math coordinates (right=+x, up=+y)
- **Screen coordinates**: Qt coordinates (right=+x, down=+y)
- Automatic conversion between the two

### Eigenvalue Calculation

For 2x2 matrices [[a,b],[c,d]]:
- Characteristic equation: λ² - (a+d)λ + (ad-bc) = 0
- Discriminant: Δ = (a+d)² - 4(ad-bc)
- If Δ ≥ 0: Real eigenvalues (visualizable)
- If Δ < 0: Complex eigenvalues (display warning)

### Animation

- Uses QTimer at ~60 FPS (16ms intervals)
- Smooth ease-in-ease-out interpolation
- Linear interpolation: `v(t) = v₀ + t(v₁ - v₀)`

## Troubleshooting

**Problem**: Visualizer window is empty
- **Solution**: Make sure you've added vectors or set a matrix

**Problem**: "Matrix must be 2x2" error
- **Solution**: These visualizers only work with 2D transformations

**Problem**: No eigenvectors displayed
- **Solution**: Matrix likely has complex eigenvalues (check info label)

**Problem**: Animation is too fast/slow
- **Solution**: Adjust the speed slider or pass different duration to `animateTransformation()`

**Problem**: Exported image is blank
- **Solution**: Ensure visualizer has rendered at least once before export

## License

Part of Matrix Commander educational calculator project.

## Contributing

To extend the visualizers:
1. Add new visualization modes in the paint events
2. Implement additional matrix properties (determinant, trace)
3. Add 3D visualization support (future)
4. Integrate with numerical eigenvalue solvers for larger matrices

## See Also

- `VISUALIZATION_EXAMPLES.cpp` - Complete code examples
- `MatrixEngine.h` - Core matrix operations
- `MainWindow.h` - Main application integration

---

**Happy Learning! 🎓 See linear algebra come to life! 🚀**

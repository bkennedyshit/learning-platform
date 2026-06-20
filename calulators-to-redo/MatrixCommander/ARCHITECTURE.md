---
date: 2026-05-26
title: "Architecture Overview - Matrix Commander"
tags: [learning, matrixcommander]
status: reference
type: reference
---

# Architecture Overview - Matrix Commander

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Application                        │
│                         (main.cpp)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Main Window                             │
│                   (MainWindow.h/cpp)                         │
│  - Frameless window management                               │
│  - Signal/slot coordination                                  │
│  - Theme application                                         │
│  - Keyboard shortcuts                                        │
└─────┬────────────────┬────────────────┬──────────────────────┘
      │                │                │
      ▼                ▼                ▼
┌─────────────┐  ┌────────────┐  ┌──────────────────────┐
│   Matrix    │  │ Operation  │  │   Results Display    │
│   Widget    │  │   Panel    │  │    (QTextEdit)       │
│  (custom)   │  │  (custom)  │  │   - Formatted        │
└──────┬──────┘  └─────┬──────┘  │   - Copyable         │
       │               │          │   - Exportable       │
       │               │          └──────────────────────┘
       │               │
       ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│              Matrix Engine Adapter                           │
│           (MatrixEngineAdapter.h/cpp)                        │
│  - Matrix operations (add, multiply, inverse, etc.)          │
│  - Decompositions (LU, QR)                                   │
│  - Properties (determinant, rank, trace, norm)               │
│  - Pure C++ implementation (no external dependencies)        │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. MainWindow (Orchestrator)
**Responsibilities:**
- Window creation and styling
- Component layout and organization
- Signal/slot connections
- User interaction handling
- Export/import functionality

**Key Features:**
- Borderless, draggable window
- System tray positioning
- Dark MATLAB-style theme
- Status bar with dimension tracking

### 2. MatrixWidget (Input Component)
**Responsibilities:**
- Matrix data input/output
- Dynamic sizing (1x1 to 10x10)
- Quick fill operations
- Data validation

**Key Features:**
- Editable QTableWidget cells
- Spinbox dimension controls
- Random/Identity/Zero fill buttons
- Real-time validation

**API:**
```cpp
Matrix getMatrix() const;           // Get current matrix data
void setMatrix(const Matrix &m);    // Set matrix data
void setDimensions(int r, int c);  // Resize matrix
void setValue(int r, int c, double v); // Set single cell
```

### 3. OperationPanel (Control Component)
**Responsibilities:**
- Display operation buttons
- Categorize operations
- Visual feedback on click
- Signal operation requests

**Key Features:**
- Grouped operations (Basic, Advanced, Decomposition)
- Emoji icons for visual appeal
- Tooltips with formulas
- Click animation

**Signal:**
```cpp
void operationRequested(const QString &operation);
```

### 4. MatrixEngineAdapter (Computation Engine)
**Responsibilities:**
- Matrix arithmetic
- Matrix decompositions
- Matrix properties
- Error handling

**Implementation:**
- Pure C++ (no heavy dependencies)
- Standard library algorithms
- Numerical stability considerations
- Exception-based error handling

## Data Flow

```
User Input → MatrixWidget → MainWindow → MatrixEngineAdapter
                                  ↓
                            Results Display
                                  ↓
                          Export/Clipboard
```

### Example: Matrix Addition Flow

```
1. User enters values in MatrixWidget A and B
2. User clicks "➕ Add" in OperationPanel
3. OperationPanel emits operationRequested("Add")
4. MainWindow::onMatrixOperation() receives signal
5. MainWindow calls getCurrentMatrix() and getSecondMatrix()
6. MainWindow calls engine->add(m1, m2)
7. MatrixEngineAdapter performs computation
8. MainWindow calls displayResult(result, "A + B")
9. Results displayed in formatted QTextEdit
10. Status bar updated with new dimensions
```

## Signal/Slot Connections

```cpp
// OperationPanel → MainWindow
connect(operationPanel, &OperationPanel::operationRequested,
        this, &MainWindow::onMatrixOperation);

// MatrixWidget → MainWindow
connect(matrix1Widget, &MatrixWidget::matrixChanged,
        this, &MainWindow::onMatrixChanged);

connect(matrix2Widget, &MatrixWidget::matrixChanged,
        this, &MainWindow::onMatrix2Changed);

// Buttons → MainWindow
connect(exportBtn, &QPushButton::clicked,
        this, &MainWindow::exportResults);

connect(clearBtn, &QPushButton::clicked,
        this, &MainWindow::clearAll);

// Window controls
connect(minimizeBtn, &QPushButton::clicked,
        this, &MainWindow::minimizeWindow);

connect(closeBtn, &QPushButton::clicked,
        this, &MainWindow::closeWindow);
```

## Styling System

### Theme Components
1. **Color Palette**
   - Background: `#1e1e1e` (dark gray)
   - Accent: `#00d9ff` (cyan)
   - Success: `#238636` (green)
   - Text: `#ffffff` (white)
   - Results: `#00ff88` (bright green)

2. **Typography**
   - Headers: Bold, 14-16px
   - Buttons: Bold, 13px
   - Code/Results: Consolas, 10-12px monospace

3. **Visual Effects**
   - Gradients on buttons
   - Hover state transitions
   - Click animations (200ms flash)
   - Border radius: 4-6px

## Extension Points

### Adding New Operations
```cpp
// 1. Add button in OperationPanel::setupUI()
createOperationButton("🎯 Custom", "Custom", "Custom formula", layout);

// 2. Add handler in MainWindow::onMatrixOperation()
else if (operation == "Custom") {
    result = engine->customOperation(m1);
    displayResult(result, "Custom");
}

// 3. Implement in MatrixEngineAdapter
Matrix MatrixEngineAdapter::customOperation(const Matrix &a) {
    // Your algorithm here
    return result;
}
```

### Adding New Widgets
```cpp
// 1. Create custom widget class
class CustomWidget : public QWidget {
    Q_OBJECT
public:
    CustomWidget(QWidget *parent = nullptr);
signals:
    void dataChanged();
};

// 2. Add to MainWindow
CustomWidget *customWidget = new CustomWidget();
layout->addWidget(customWidget);

// 3. Connect signals
connect(customWidget, &CustomWidget::dataChanged,
        this, &MainWindow::onCustomDataChanged);
```

## Performance Considerations

### Current Limits
- Matrix size: 10×10 (UI constraint)
- Computation: O(n³) for most operations
- Memory: Minimal (<1MB for typical usage)

### Optimization Opportunities
1. **Parallel Processing**
   - Use QtConcurrent for large operations
   - Thread decompositions

2. **Better Algorithms**
   - Integrate Eigen library for speed
   - Use BLAS/LAPACK for production

3. **Caching**
   - Cache decompositions
   - Memoize expensive calculations

## Error Handling

### Validation Levels
1. **Input Validation** (MatrixWidget)
   - Cell value parsing
   - Dimension constraints

2. **Operation Validation** (MatrixEngineAdapter)
   - Dimension compatibility
   - Matrix properties (square, invertible)

3. **Result Handling** (MainWindow)
   - Exception catching
   - User-friendly error messages

### Error Display
```cpp
void MainWindow::displayError(const QString &error) {
    // Formatted error box in results panel
    // Status bar notification
    // No blocking dialogs (non-intrusive)
}
```

## Build System

### qmake (Primary)
- Cross-platform
- Qt-native
- Simple .pro file
- Automatic MOC handling

### CMake (Alternative)
- Modern C++ projects
- Better IDE integration
- More flexible
- Standard build tool

Both systems:
- Support Qt 5.15+ and Qt 6.x
- Auto-detect Qt installation
- Generate platform-specific builds
- Handle resource compilation

---

**This is a complete, professional-grade Qt application ready for use and extension!** 🚀

---

## Related Notes
- [[BUILD_AND_RUN]] - Shared matrixcommander/learning focus
- [[PROJECT_SUMMARY]] - Shared matrixcommander/learning focus
- [[QUICKSTART]] - Shared matrixcommander/learning focus
- [[STATUS]] - Shared matrixcommander/learning focus
- [[VISUALIZATION_README]] - Shared matrixcommander/learning focus

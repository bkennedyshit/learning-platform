---
date: 2026-05-26
title: "Matrix Commander - Quick Start Guide"
tags: [learning, matrixcommander]
status: reference
type: note
---

# Matrix Commander - Quick Start Guide

## 🚀 Getting Started (3 Steps)

### Step 1: Prerequisites
Install Qt development tools for your platform:

**Windows:**
```bash
# Download Qt installer from: https://www.qt.io/download-qt-installer
# Install Qt 6.x with MinGW compiler
# Add to PATH: C:\Qt\6.x.x\mingw_64\bin
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install qt6-base-dev qt6-tools-dev build-essential
```

**macOS:**
```bash
brew install qt
```

### Step 2: Build

**Windows:**
```batch
# Double-click build.bat or run in terminal:
build.bat
```

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

**Alternative - Using CMake:**
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

### Step 3: Run
```bash
# Windows
cd build\release
MatrixCommander.exe

# Linux/macOS
./build/MatrixCommander
```

---

## 📖 User Guide

### Basic Operations

1. **Set Matrix Size**
   - Use spinboxes to set rows/columns (1-10)
   - Changes apply immediately

2. **Enter Values**
   - Click any cell to edit
   - Press Tab to move to next cell
   - Press Enter to confirm

3. **Quick Fill**
   - 🎲 Random: Fill with random values
   - I: Create identity matrix
   - 0: Fill with zeros

4. **Perform Operations**
   - Use buttons in the middle panel
   - Results appear in the right panel
   - All operations show formatted output

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Copy results to clipboard |
| Ctrl+V | Paste matrix from clipboard |
| Ctrl+Q | Quit application |
| Esc | Clear all matrices |

### Available Operations

**Basic:**
- ➕ Add (A + B)
- ➖ Subtract (A - B)
- ✖ Multiply (A × B)
- ↻ Transpose (A^T)

**Advanced:**
- ⁻¹ Inverse (A^-1)
- 📐 Determinant (det(A))
- 🔢 Rank (rank(A))
- ➰ Trace (tr(A))

**Decomposition:**
- 🔺 LU Decomposition
- 🔷 QR Decomposition
- ⚡ Eigenvalues

**Properties:**
- 📏 Norm (||A||)
- 🔍 Condition Number (κ(A))

---

## 💡 Tips & Tricks

### Efficient Workflow
1. Set up Matrix A with your primary data
2. Use quick fill for Matrix B if needed
3. Chain operations: result becomes input
4. Export final results to CSV

### Clipboard Format
Paste matrices in these formats:
```
# CSV format
1,2,3
4,5,6

# Space-separated
1 2 3
4 5 6

# Tab-separated (Excel copy)
1	2	3
4	5	6
```

### Window Management
- Drag title bar to move window
- Window stays on top (perfect for side-by-side work)
- Minimize button hides to taskbar
- ✕ button closes application

---

## 🔧 Troubleshooting

### Build Issues

**"qmake not found"**
```bash
# Add Qt to PATH
# Windows: C:\Qt\6.x.x\mingw_64\bin
# Linux: export PATH=/path/to/Qt/6.x.x/gcc_64/bin:$PATH
```

**"Cannot find -lQt6Widgets"**
```bash
# Install Qt development packages
# Ubuntu: sudo apt-get install qt6-base-dev
```

**"LNK1104: cannot open file 'Qt6Core.lib'"**
```bash
# Use Qt Creator or ensure MSVC is properly configured
# Or use MinGW build tools instead
```

### Runtime Issues

**"Matrix dimensions incompatible"**
- Check matrix sizes before operations
- Status bar shows current dimensions
- Add/Subtract require same size
- Multiply requires A.cols == B.rows

**"Matrix is singular"**
- Matrix has no inverse (determinant = 0)
- Try a different matrix
- Check for linearly dependent rows/columns

---

## 🎨 Customization

### Change Theme Colors
Edit `MainWindow.cpp -> applyMatlabTheme()`:
```cpp
QString stylesheet = R"(
    #titleBar {
        border-bottom: 2px solid #00d9ff;  // Change accent color
    }
    #resultsDisplay {
        color: #00ff88;  // Change result text color
    }
)";
```

### Increase Matrix Size Limit
Edit `MatrixWidget.cpp -> setupUI()`:
```cpp
rowSpinBox->setRange(1, 20);  // Change from 10 to 20
colSpinBox->setRange(1, 20);
```

### Add Custom Operations
1. Add button in `OperationPanel.cpp`
2. Add handler in `MainWindow::onMatrixOperation()`
3. Implement algorithm in `MatrixEngineAdapter.cpp`

---

## 📦 Project Structure

```
MatrixCommander/
├── src/
│   ├── main.cpp                    # Entry point
│   ├── MainWindow.h/cpp            # Main window & UI coordination
│   ├── MatrixWidget.h/cpp          # Matrix input/display widget
│   ├── OperationPanel.h/cpp        # Operation buttons
│   └── MatrixEngineAdapter.h/cpp   # Matrix computation engine
├── build/                          # Build output (auto-generated)
├── CMakeLists.txt                  # CMake build configuration
├── MatrixCommander.pro             # qmake build configuration
├── build.bat                       # Windows build script
├── build.sh                        # Linux/macOS build script
├── README.md                       # Full documentation
└── QUICKSTART.md                   # This file
```

---

## 🚀 Next Steps

1. **Learn Qt**: Study the source code to understand Qt Widgets
2. **Add Features**: Implement your own matrix operations
3. **Optimize**: Profile and optimize for larger matrices
4. **Extend**: Add plotting, visualization, or scripting

---

## 📚 Resources

- [Qt Documentation](https://doc.qt.io/)
- [Linear Algebra Algorithms](http://www.netlib.org/lapack/)
- [Matrix Computations (Book)](https://www.amazon.com/Computations-Hopkins-Studies-Mathematical-Sciences/dp/1421407949)

---

**Enjoy your professional matrix calculator! 🎉**

For issues or questions, check the full README.md or the source code comments.

---

## Related Notes
- [[ARCHITECTURE]] - Shared matrixcommander/learning focus
- [[BUILD_AND_RUN]] - Shared matrixcommander/learning focus
- [[PROJECT_SUMMARY]] - Shared matrixcommander/learning focus
- [[STATUS]] - Shared matrixcommander/learning focus
- [[VISUALIZATION_README]] - Shared matrixcommander/learning focus

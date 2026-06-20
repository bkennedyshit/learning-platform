---
date: 2026-05-26
title: "Quick Build Guide"
tags: [learning, calculusvisualizer]
status: reference
type: note
---

# Quick Build Guide

## Prerequisites

1. **Install Qt**
   - Download from: https://www.qt.io/download-qt-installer
   - Install Qt 5.15 or Qt 6.x
   - Select "Qt Creator" and appropriate compiler

2. **Verify Installation**
   ```bash
   qmake --version
   ```

## Build Steps

### Windows (EASIEST - Qt Creator)

1. Open **Qt Creator**
2. File → Open File or Project
3. Navigate to `CalculusVisualizer` folder
4. Open `CalculusVisualizer.pro`
5. Click "Configure Project" (select your Qt kit)
6. Click the **Build** button (🔨) or press Ctrl+B
7. Click the **Run** button (▶) or press Ctrl+R

### Windows (Command Line - qmake)

```powershell
cd "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\CalculusVisualizer"
qmake CalculusVisualizer.pro
nmake  # Or 'mingw32-make' if using MinGW
```

### Windows (CMake + Visual Studio)

```powershell
cd "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\CalculusVisualizer"
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022"
cmake --build . --config Release
```

### Linux

```bash
cd CalculusVisualizer
mkdir build
cd build
cmake ..
make -j4
./CalculusVisualizer
```

Or with qmake:
```bash
qmake CalculusVisualizer.pro
make -j4
./CalculusVisualizer
```

### macOS

```bash
cd CalculusVisualizer
mkdir build
cd build
cmake ..
make -j4
open CalculusVisualizer.app
```

## Troubleshooting

**"qmake: command not found"**
- Add Qt bin directory to PATH
- Example: `C:\Qt\6.6.0\mingw_64\bin`

**"Qt5Script not found" warning**
- Ignore it - the app works without Qt Script
- Or install Qt Script module separately

**CMake can't find Qt**
```bash
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/6.6.0/mingw_64"
```

## First Run

1. Launch the application
2. Enter a function: `x^2`
3. Click **Plot**
4. Explore the tabs!

Enjoy visualizing calculus! 🎓

---

## Related Notes
- [[BUILDING]] - Shared calculusvisualizer/learning focus
- [[DERIVATIVE_ENGINE_README]] - Shared calculusvisualizer/learning focus
- [[IMPLEMENTATION_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[PROJECT_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[QUICKSTART]] - Shared calculusvisualizer/learning focus

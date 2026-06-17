---
date: 2026-05-06
title: Calculator Suite - Build Instructions Summary
type: quick-start
tags: [build, setup, tldr]
---

# Build the Calculators - TL;DR

**Can't build yet - Qt not installed. Here's what to do:**

---

## 📥 Step 1: Install Qt (~30 min)

**Download:** https://www.qt.io/download-qt-installer

**Install these components:**
- ✅ Qt 6.7.x MinGW 64-bit
- ✅ Qt Charts
- ✅ Qt Data Visualization  
- ✅ CMake
- ✅ Qt Creator

**Full guide:** [QT_INSTALLATION_BUILD_GUIDE.md](QT_INSTALLATION_BUILD_GUIDE.md)

---

## ✅ Step 2: Check Installation (~1 min)

```powershell
cd "C:\Obsidian Vault\Learning_Tools"
.\setup-check.ps1
```

Should show all ✅ green checkmarks.

---

## 🔨 Step 3: Build All Calculators (~20 min)

```powershell
.\build-all-calculators.ps1
```

**Or manually in Qt Creator:**
1. Open Qt Creator
2. File → Open → MatrixCommander.pro
3. Build (Ctrl+B)
4. Repeat for other .pro files

---

## 🚀 Step 4: Launch & Learn!

**Quick launch:**
```powershell
.\launch-calculators.ps1
```

**Or find executables:**
```
Learning_Tools\MatrixCommander\build\Release\MatrixCommander.exe
Learning_Tools\CalculusVisualizer\build\Release\CalculusVisualizer.exe
Learning_Tools\LossLandscape3D\build\Release\LossLandscape3D.exe
Learning_Tools\ProbabilityStudio\build\Release\ProbabilityStudio.exe
```

---

## 📚 Usage Guide

See: [HOW_TO_USE_CALCULATORS.md](HOW_TO_USE_CALCULATORS.md)

**Quick examples:**
- **Matrix Commander:** Create matrix → Click "Eigenvalues"
- **Calculus Visualizer:** Type `x^2` → See derivative steps
- **Loss Landscape 3D:** Select "Rosenbrock" → Watch optimizer
- **Probability Studio:** Adjust softmax temperature

---

## 🎯 What Each Calculator Teaches

| Calculator | Teaches | For Understanding |
|------------|---------|-------------------|
| Matrix Commander | Linear algebra | Neural network layers |
| Calculus Visualizer | Derivatives, chain rule | Backpropagation |
| Loss Landscape 3D | Optimization | Training dynamics |
| Probability Studio | Statistics, distributions | Loss functions, sampling |

---

## ⚡ Current Status

- ✅ All source code created (~14,000 lines C++)
- ✅ Build scripts ready
- ✅ Documentation complete
- ❌ Qt not installed (you need to do this)
- ❌ Calculators not built yet

**Next:** Install Qt, run build script, start learning!

---

**Time to completion: ~1 hour (mostly Qt installation)**

---

## Related Notes
- [[QT_INSTALLATION_BUILD_GUIDE]] - Shared build/setup focus
- [[LOCATION_SETUP_GUIDE]] - Same Dev_Tools folder
- [[Git Essentials for Coding Tests]] - Same Dev_Tools folder
- [[PRACTICE_GUI_APP_VISION]] - Same Dev_Tools folder
- [[Terminal Commands Essentials]] - Same Dev_Tools folder

---
title: "Installing Qt & Building Calculators - Complete Guide"
subject: "Dev_Tools"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: tutorial
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Qt Installation & Calculator Build - Complete Guide

**Goal:** Install Qt 6, build all 4 calculators, start learning!

**Time Required:** ~1 hour (mostly Qt download/install)

---

## 📋 Prerequisites Checklist

Before starting:
- [ ] Windows 10/11
- [ ] ~10 GB free disk space (Qt is large!)
- [ ] Internet connection (for downloads)
- [ ] Admin rights (for installation)

---

## 🔧 Step 1: Install Qt 6 (~30 minutes)

### Download Qt Online Installer

1. **Go to:** https://www.qt.io/download-qt-installer
2. **Click:** "Download the Qt Online Installer"
3. **Run:** `qt-online-installer-windows-x64-4.x.x.exe`

### During Installation

**Create Account** (free):
- Email + password
- Select "Open source" license
- Agree to terms

**Select Components** (CRITICAL - pick the right ones!):
```
Qt
└── Qt 6.7.x (or latest 6.x)
    ├── ✅ MinGW 11.2.0 64-bit
    ├── ✅ Qt Charts
    ├── ✅ Qt Data Visualization
    └── ✅ Sources (optional - for learning)

Developer and Designer Tools
├── ✅ CMake 3.27+
├── ✅ Ninja 1.11+
└── ✅ Qt Creator 13.x (HIGHLY RECOMMENDED)
```

**Don't install:**
- ❌ Android/iOS components (unless you want them)
- ❌ Qt 5.x (we're using Qt 6)
- ❌ WebAssembly (not needed)

**Installation path:** (default is fine)
```
C:\Qt\
```

**Time:** 20-30 minutes depending on speed

---

## 🎯 Step 2: Verify Qt Installation (~2 minutes)

### Option A: Run Check Script

```powershell
cd "C:\Obsidian Vault\Learning_Tools"
.\setup-check.ps1
```

Expected output:
```
✅ Qt Framework: INSTALLED
✅ CMake: INSTALLED
✅ C++ Compiler: INSTALLED
✅ Projects: READY
```

### Option B: Manual Check

Open PowerShell and run:
```powershell
# Check Qt Creator
& "C:\Qt\Tools\QtCreator\bin\qtcreator.exe" --version

# Check compiler (MinGW)
& "C:\Qt\Tools\mingw1120_64\bin\g++.exe" --version

# Check CMake
cmake --version
```

All should return version numbers, not errors.

---

## 🚀 Step 3: Build All Calculators (~20 minutes)

### Method 1: Automated Build (RECOMMENDED)

```powershell
cd "C:\Obsidian Vault\Learning_Tools"
.\build-all-calculators.ps1
```

**What it does:**
1. Finds your Qt installation automatically
2. Builds all 4 calculators in sequence
3. Shows progress for each (~5 min per calculator)
4. Creates executables in each project's `build/` folder
5. Generates a launcher script

**Expected output:**
```
[1/4] Building Matrix Commander
  ✅ Build completed in 245s
  📦 Executable: MatrixCommander.exe (12.3 MB)

[2/4] Building Calculus Visualizer
  ✅ Build completed in 198s
  📦 Executable: CalculusVisualizer.exe (10.8 MB)

[3/4] Building Loss Landscape 3D
  ✅ Build completed in 267s
  📦 Executable: LossLandscape3D.exe (15.1 MB)

[4/4] Building Probability Studio
  ✅ Build completed in 213s
  📦 Executable: ProbabilityStudio.exe (11.4 MB)

🎉 ALL CALCULATORS BUILT SUCCESSFULLY!
```

### Method 2: Build in Qt Creator (Alternative)

**For each calculator:**

1. **Open Qt Creator**
   - Start Menu → Qt Creator

2. **Open Project**
   - File → Open File or Project
   - Navigate to: `C:\Obsidian Vault\Learning_Tools\MatrixCommander\`
   - Select: `MatrixCommander.pro`

3. **Configure Project**
   - Select kit: Desktop Qt 6.x MinGW 64-bit
   - Click "Configure Project"

4. **Build**
   - Click hammer icon 🔨 (or Ctrl+B)
   - Wait ~5 minutes
   - Look for "Build succeeded" in output

5. **Run**
   - Click play button ▶️ (or Ctrl+R)
   - Calculator should launch!

6. **Repeat** for:
   - CalculusVisualizer.pro
   - LossLandscape3D.pro
   - ProbabilityStudio.pro

---

## 🎮 Step 4: Launch & Test Calculators (~10 minutes)

### Find Your Executables

After building, executables are in:
```
C:\Obsidian Vault\Learning_Tools\
├── MatrixCommander\build\Release\MatrixCommander.exe
├── CalculusVisualizer\build\Release\CalculusVisualizer.exe
├── LossLandscape3D\build\Release\LossLandscape3D.exe
└── ProbabilityStudio\build\Release\ProbabilityStudio.exe
```

### Quick Test Each Calculator

**Matrix Commander:**
```
1. Launch MatrixCommander.exe
2. Enter a 3×3 matrix (fill cells with numbers)
3. Click "Determinant" button
4. Result should appear below
✅ Working if you see a number!
```

**Calculus Visualizer:**
```
1. Launch CalculusVisualizer.exe
2. In function input, type: x^2
3. Click "Graph" tab
4. Should see parabola plotted
✅ Working if you see the graph!
```

**Loss Landscape 3D:**
```
1. Launch LossLandscape3D.exe
2. Select "Rosenbrock" function
3. Click "Plot Surface"
4. Should see 3D banana-shaped valley
5. Drag to rotate
✅ Working if 3D surface rotates!
```

**Probability Studio:**
```
1. Launch ProbabilityStudio.exe
2. Go to "Distributions" tab
3. Select "Normal"
4. Adjust mean/stddev sliders
5. Should see bell curve update
✅ Working if distribution changes!
```

---

## 🎨 Step 5: Optional - Create Desktop Shortcuts

### Manual Method

For each calculator:
1. Right-click desktop → New → Shortcut
2. Browse to: `C:\Obsidian Vault\Learning_Tools\MatrixCommander\build\Release\MatrixCommander.exe`
3. Name it: "Matrix Commander"
4. Click Finish
5. Right-click shortcut → Properties
6. Click "Change Icon" → Browse to Qt folder for icons (optional)

### Script Method

Run in PowerShell:
```powershell
$desktop = [Environment]::GetFolderPath("Desktop")
$exes = @(
    "C:\Obsidian Vault\Learning_Tools\MatrixCommander\build\Release\MatrixCommander.exe",
    "C:\Obsidian Vault\Learning_Tools\CalculusVisualizer\build\Release\CalculusVisualizer.exe",
    "C:\Obsidian Vault\Learning_Tools\LossLandscape3D\build\Release\LossLandscape3D.exe",
    "C:\Obsidian Vault\Learning_Tools\ProbabilityStudio\build\Release\ProbabilityStudio.exe"
)

foreach($exe in $exes) {
    if(Test-Path $exe) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($exe)
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut("$desktop\$name.lnk")
        $shortcut.TargetPath = $exe
        $shortcut.Save()
        Write-Host "Created: $name.lnk" -ForegroundColor Green
    }
}
```

---

## 📚 Step 6: Using the Calculators for Learning

### Learning Roadmap

**Weeks 1-4: Matrix Commander**
- **Goal:** Understand linear algebra for neural networks
- **Activities:**
  - Create weight matrices
  - Multiply matrices (simulate forward pass)
  - Calculate eigenvalues (understand stability)
  - Visualize transformations
- **Resources:**
  - Khan Academy: Linear Algebra
  - 3Blue1Brown: Essence of Linear Algebra
  - Your MAT-111 notes (Topic 20)

**Weeks 5-8: Calculus Visualizer**
- **Goal:** Master derivatives and backpropagation
- **Activities:**
  - Plot f(x) and f'(x) simultaneously
  - See chain rule step-by-step
  - Watch gradient descent animate
  - Understand learning rates
- **Resources:**
  - 3Blue1Brown: Essence of Calculus
  - Khan Academy: Calculus I
  - Focus on chain rule = backprop!

**Weeks 9-12: Loss Landscape 3D**
- **Goal:** Visualize multivariable calculus
- **Activities:**
  - Plot 3D loss surfaces
  - Compare optimizer algorithms
  - See saddle points vs local minima
  - Understand momentum
- **Resources:**
  - Andrew Ng: ML Course (optimization lectures)
  - Sebastian Ruder: "An overview of gradient descent optimization algorithms"

**Weeks 13-16: Probability Studio**
- **Goal:** ML statistics and distributions
- **Activities:**
  - Explore normal distribution
  - Understand softmax temperature (LLM sampling!)
  - Calculate cross-entropy loss
  - See Bayes' theorem visually
- **Resources:**
  - Khan Academy: Statistics & Probability
  - Fast.ai: Practical Deep Learning
  - Focus on ML-specific stats!

---

## 🛠️ Troubleshooting

### "Qt is not found"

**Solution:**
```powershell
# Add Qt to PATH temporarily
$env:PATH = "C:\Qt\6.7.0\mingw_64\bin;$env:PATH"
```

Or add permanently:
1. Windows Search → "Environment Variables"
2. System Properties → Environment Variables
3. Edit PATH → Add: `C:\Qt\6.7.0\mingw_64\bin`

### "CMake configuration failed"

**Solution:**
```powershell
# Specify Qt path explicitly
cd "C:\Obsidian Vault\Learning_Tools\MatrixCommander\build"
cmake .. -DCMAKE_PREFIX_PATH="C:\Qt\6.7.0\mingw_64"
```

### "Cannot find -lQt6Widgets"

**Cause:** Using wrong compiler (mixing MinGW and MSVC)

**Solution:** 
- Rebuild from clean state
- Ensure using MinGW consistently
- Delete build/ folder and start over

### "Application failed to start because Qt6Widgets.dll was not found"

**Solution:** Copy Qt DLLs next to executable:
```powershell
cd "C:\Obsidian Vault\Learning_Tools\MatrixCommander\build\Release"
windeployqt MatrixCommander.exe
```

This copies all necessary Qt DLLs.

### "Build takes forever"

**Normal!** First build is slow:
- Matrix Commander: ~5 minutes
- Calculus Visualizer: ~4 minutes
- Loss Landscape 3D: ~5 minutes (3D is heavy)
- Probability Studio: ~4 minutes

Subsequent builds are much faster (only changed files).

---

## 📊 Disk Space After Installation

**Qt Installation:** ~3-5 GB
**Calculator Source:** ~20 MB
**Built Executables:** ~50 MB total
**Build Artifacts:** ~200-400 MB total

**Total:** ~4-5 GB

---

## 🎉 Success Checklist

By the end, you should have:
- [x] Qt 6 installed
- [x] All 4 calculators built
- [x] Tested each calculator (opens and works)
- [x] Desktop shortcuts (optional)
- [x] Understanding of what each calculator teaches

---

## 🚀 Next Steps

1. **Start Learning!**
   - Begin with Matrix Commander
   - Work through your MAT-111 matrices notes
   - Verify calculations with the calculator

2. **Document Your Journey**
   - Take screenshots of visualizations
   - Export graphs to your Obsidian vault
   - Write about concepts you learn

3. **Progress Through Suite**
   - Matrix → Calculus → 3D → Probability
   - Each builds on the previous

4. **Build Neural Networks**
   - Week 17+: Apply all the math
   - Implement from scratch
   - Use calculators to verify your work

---

## 📝 Notes

- **Builds are one-time:** Once built, just run the .exe
- **Updates:** If you modify source, rebuild in Qt Creator
- **Uninstall Qt:** ~4 GB freed if you remove later
- **Keep or Remove:** Source code can be deleted after building (executables work standalone)

---

**You're ready to master AI/ML math! Start with Matrix Commander and your MAT-111 notes.** 🧠✨

---

## Related Notes
- [BUILD_INSTRUCTIONS_TLDR](BUILD_INSTRUCTIONS_TLDR) - Shared build/setup focus
- [LOCATION_SETUP_GUIDE](LOCATION_SETUP_GUIDE) - Same Dev_Tools folder
- [CALCULATOR_SUITE_VISION](CALCULATOR_SUITE_VISION) - Same Dev_Tools folder
- [06 - Windows and Doors Installation](06---Windows-and-Doors-Installation) - Related windows topic
- [Git Essentials for Coding Tests](Git-Essentials-for-Coding-Tests) - Same Dev_Tools folder

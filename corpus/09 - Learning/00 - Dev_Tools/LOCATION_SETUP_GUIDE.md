---
date: 2026-05-06
title: Calculator Projects - Location & Setup Guide
type: reference
tags: [calculators, setup, git]
---

# Calculator Projects - Location Guide

## 📂 New Structure (Clean Separation!)

### Your Vault (Git Tracked)
```
C:\Obsidian Vault\Bill's Vault\
└── 05-Knowledge_Foundation\
    └── 09 - Learning\
        └── 00 - Dev_Tools\
            ├── graphing-calculator.html ✅ (works now)
            ├── CALCULATOR_SUITE_VISION.md (roadmap)
            ├── QUICK_REFERENCE.md (quick ref)
            ├── COMPLETE_DELIVERY.md (full report)
            └── README.md (location pointer)
```

**What's here:** Documentation, vision, references, web-based tools  
**Git status:** ✅ Track these (they're just markdown/html)  
**Size:** Small, fast commits

### Learning Tools (NOT Git Tracked)
```
C:\Obsidian Vault\Learning_Tools\
├── MatrixCommander\          (~5,200 lines C++)
├── CalculusVisualizer\       (~4,750 lines C++)
├── LossLandscape3D\          (~2,940 lines C++)
├── ProbabilityStudio\        (~3,500 lines C++)
├── .gitignore               (excludes build artifacts)
└── README.md                (setup guide)
```

**What's here:** Actual Qt/C++ projects, build files, dependencies  
**Git status:** ❌ Don't track (too bloated, binaries change)  
**Size:** Large (will have build/, node_modules-like deps, .exe files)

---

## 🎯 Why This Separation?

### ✅ Benefits
1. **Vault stays clean** - Fast git operations, no bloat
2. **No accidental commits** - Build artifacts don't end up in repo
3. **Easy backups** - Vault = lightweight, Tools = can rebuild
4. **Logical separation** - Knowledge vs. executables
5. **.gitignore works** - Learning_Tools has proper ignores

### ⚠️ What Goes Where

| Item | Vault | Learning_Tools |
|------|-------|----------------|
| Markdown docs | ✅ | ❌ |
| Project vision | ✅ | ❌ |
| HTML/JS tools | ✅ | ❌ |
| C++ source code | ❌ | ✅ |
| Qt .pro files | ❌ | ✅ |
| CMakeLists.txt | ❌ | ✅ |
| Build folders | ❌ | ✅ (ignored) |
| .exe / .dll | ❌ | ✅ (ignored) |
| Dependencies | ❌ | ✅ (ignored) |

---

## 🛠️ Setup Instructions

### First Time Setup

1. **Install Qt 6** (only needed once)
   ```powershell
   # Download from https://www.qt.io/download-qt-installer
   # Install to: C:\Qt\6.x.x
   # Components: Widgets, Charts, DataVisualization, MinGW
   ```

2. **Verify Projects Moved**
   ```powershell
   Get-ChildItem "C:\Obsidian Vault\Learning_Tools" -Directory
   # Should show: MatrixCommander, CalculusVisualizer, etc.
   ```

3. **Build a Calculator**
   ```powershell
   cd "C:\Obsidian Vault\Learning_Tools\MatrixCommander"
   .\build.bat
   # OR open MatrixCommander.pro in Qt Creator
   ```

### Building Each Calculator

**Option 1: Qt Creator (Easiest)**
```
1. Open Qt Creator
2. File → Open File or Project
3. Navigate to: C:\Obsidian Vault\Learning_Tools\MatrixCommander\
4. Select: MatrixCommander.pro
5. Configure project (select Qt kit)
6. Click Build (Ctrl+B)
7. Click Run (Ctrl+R)
```

**Option 2: Command Line**
```powershell
# Navigate to any project
cd "C:\Obsidian Vault\Learning_Tools\MatrixCommander"

# Build
.\build.bat

# Run
.\build\Release\MatrixCommander.exe
```

---

## 📝 Git Workflow

### Vault Commits (Small, Frequent)
```powershell
cd "C:\Obsidian Vault\Bill's Vault"
git add 05-Knowledge_Foundation/09*
git commit -m "Update calculator documentation"
git push
```

### Learning Tools (Optional Backup)
```powershell
# If you want to version the source (not builds):
cd "C:\Obsidian Vault\Learning_Tools"
git init  # Optional - only if you want source control here
git add .
git commit -m "Calculator source code"

# .gitignore already excludes build artifacts!
```

**Recommendation:** Keep Learning_Tools as simple file backup, not git. The code is delivered and complete.

---

## 🔄 If You Need to Move Again

```powershell
# Move a project elsewhere
Move-Item "C:\Obsidian Vault\Learning_Tools\MatrixCommander" "C:\Dev\MatrixCommander"

# Update the vault README to point to new location
# That's it! Vault docs don't need to move
```

---

## 📊 Disk Space Expectations

### Vault (Git Tracked)
- Documentation: ~100 KB
- HTML calculator: ~50 KB
- Total: ~150 KB (tiny!)

### Learning Tools (Not Tracked)
- Source code: ~5 MB
- **After Qt build:** ~50-100 MB per project
- **Qt installation:** ~3-5 GB (shared by all projects)
- Total: ~200-400 MB once built

---

## ✅ Checklist

- [x] Projects moved to Learning_Tools
- [x] Vault has documentation only
- [x] .gitignore in Learning_Tools
- [x] READMEs explain locations
- [ ] Qt 6 installed (you do this)
- [ ] Build Matrix Commander
- [ ] Build Calculus Visualizer
- [ ] Build Loss Landscape 3D
- [ ] Build Probability Studio

---

## 🚀 Quick Start Summary

1. **Install Qt** (30 min, one time)
2. **Navigate to Learning_Tools**
3. **Open any .pro file in Qt Creator**
4. **Build & Run**
5. **Start learning AI/ML math!**

Your vault stays clean, your projects are organized, and you're ready to build! 🎉

---

## Related Notes
- [[QT_INSTALLATION_BUILD_GUIDE]] - Same Dev_Tools folder
- [[Git Essentials for Coding Tests]] - Same Dev_Tools folder
- [[BUILD_INSTRUCTIONS_TLDR]] - Same Dev_Tools folder
- [[CALCULATOR_SUITE_VISION]] - Same Dev_Tools folder
- [[HOW_TO_USE_CALCULATORS]] - Same Dev_Tools folder

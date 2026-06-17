---
date: 2026-05-26
title: "Dev Tools - Calculator Suite Projects"
tags: [learning, dev-tools]
status: reference
type: index
---

# Dev Tools - Calculator Suite Projects

**⚠️ ACTUAL PROJECTS ARE NOT IN THE VAULT**

The calculator projects are stored outside the vault to keep it clean (no build artifacts, dependencies, or binaries in git).

---

## 📂 Project Locations

All calculator source code and build files are in:

```
C:\Obsidian Vault\Learning_Tools\
├── MatrixCommander/
├── CalculusVisualizer/
├── LossLandscape3D/
└── ProbabilityStudio/
```

**Why separate?**
- Vault = documentation, notes, knowledge (git tracked)
- Learning_Tools = actual code projects, builds, dependencies (not in git)
- Keeps vault clean and fast
- Prevents accidental commits of build artifacts

---

## 📚 Documentation (In Vault)

Documentation and references stay in the vault:

- [CALCULATOR_SUITE_VISION.md](CALCULATOR_SUITE_VISION.md) - Overall vision and roadmap
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference guide
- [COMPLETE_DELIVERY.md](COMPLETE_DELIVERY.md) - Full delivery report

---

## 🛠️ Tools In This Folder

- [graphing-calculator.html](graphing-calculator.html) - Web-based graphing calculator (already working!)

---

## 🚀 To Build Calculators

1. Navigate to project:
   ```powershell
   cd "C:\Obsidian Vault\Learning_Tools\MatrixCommander"
   ```

2. Build:
   ```powershell
   build.bat
   # OR open .pro file in Qt Creator
   ```

3. Repeat for other calculators

---

## 📝 Notes

- **Qt dependencies** will be in Learning_Tools projects, not vault
- **Build artifacts** (build/, release/, debug/) stay outside vault
- **Documentation** about the projects stays in vault
- **Source code** is in Learning_Tools but well-documented here

This structure keeps your git repo clean while still having all the tools accessible!

---
date: 2026-05-26
title: "Learning Tools"
tags: [learning, readmemd]
status: reference
type: index
---

# Learning Tools

Qt/C++ calculator projects for AI/ML math learning.

**These projects are NOT tracked in the main vault git repo.**

---

## Projects

1. **MatrixCommander/** - Linear algebra calculator
2. **CalculusVisualizer/** - Derivatives and optimization
3. **LossLandscape3D/** - 3D loss surface visualization
4. **ProbabilityStudio/** - Statistics and distributions

---

## Documentation

See vault for full docs:
`C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\00 - Dev_Tools\`

---

## .gitignore Recommendation

If you init git here, add:
```
build/
*.pro.user
*.autosave
*.exe
*.dll
*.so
*.dylib
*.a
*.lib
*.obj
*.o
CMakeCache.txt
CMakeFiles/
```

---

## Build Each Project

```powershell
cd MatrixCommander
build.bat
# OR open .pro in Qt Creator
```

All build artifacts stay in this folder, keeping your vault clean!

---
date: 2026-05-26
title: "Building Calculus Visualizer"
tags: [learning, calculusvisualizer]
status: reference
type: note
---

# Building Calculus Visualizer

Detailed build instructions for different platforms.

## Prerequisites

### All Platforms

1. **Qt 6.5+** with the following modules:
   - Qt Base (Core, Gui, Widgets)
   - Qt Charts
   - Qt Network (for future features)

2. **SymEngine** for symbolic mathematics
   - Source: https://github.com/symengine/symengine

3. **C++20 Compiler**:
   - Windows: Visual Studio 2022
   - Linux: GCC 11+ or Clang 14+
   - macOS: Xcode 14+ (Clang 14+)

4. **Build System**:
   - CMake 3.21+ (recommended)
   - OR qmake (included with Qt)

## Windows Build

### Option 1: Using Visual Studio 2022

1. Install Qt 6.5+ from https://www.qt.io/download
2. Install Visual Studio 2022 with C++ development tools
3. Install SymEngine (or use vcpkg):
   ```powershell
   vcpkg install symengine:x64-windows
   ```

4. Open PowerShell in project directory:
   ```powershell
   .\build.bat
   ```

5. Or manually with CMake:
   ```powershell
   mkdir build
   cd build
   cmake .. -G "Visual Studio 17 2022" -A x64 ^
       -DCMAKE_PREFIX_PATH="C:/Qt/6.5.0/msvc2019_64"
   cmake --build . --config Release
   ```

### Option 2: Using MinGW

```powershell
mkdir build && cd build
cmake .. -G "MinGW Makefiles" ^
    -DCMAKE_PREFIX_PATH="C:/Qt/6.5.0/mingw_64"
mingw32-make
```

## Linux Build

### Ubuntu/Debian

1. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y \
       qt6-base-dev \
       qt6-charts-dev \
       libsymengine-dev \
       cmake \
       build-essential \
       git
   ```

2. Build:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. Run:
   ```bash
   ./build/CalculusVisualizer
   ```

### Fedora/RHEL

```bash
sudo dnf install -y \
    qt6-qtbase-devel \
    qt6-qtcharts-devel \
    symengine-devel \
    cmake \
    gcc-c++

./build.sh
```

### Arch Linux

```bash
sudo pacman -S qt6-base qt6-charts symengine cmake gcc
./build.sh
```

## macOS Build

### Using Homebrew

1. Install dependencies:
   ```bash
   brew install qt@6 symengine cmake
   ```

2. Build:
   ```bash
   chmod +x build.sh
   export CMAKE_PREFIX_PATH="$(brew --prefix qt@6)"
   ./build.sh
   ```

3. Run:
   ```bash
   open build/CalculusVisualizer.app
   ```

## Build with qmake (Alternative)

If you prefer qmake over CMake:

1. Edit `CalculusVisualizer.pro` to set SymEngine paths
2. Build:
   ```bash
   qmake
   make
   ```

## Troubleshooting

### Qt6 Not Found

CMake error: `Could not find a package configuration file provided by "Qt6"`

**Solution**: Set `CMAKE_PREFIX_PATH`:
```bash
cmake .. -DCMAKE_PREFIX_PATH="/path/to/Qt/6.5.0/gcc_64"
```

### SymEngine Not Found

**Windows (vcpkg)**:
```powershell
vcpkg install symengine:x64-windows
cmake .. -DCMAKE_TOOLCHAIN_FILE="C:/vcpkg/scripts/buildsystems/vcpkg.cmake"
```

**Linux (build from source)**:
```bash
git clone https://github.com/symengine/symengine
cd symengine
cmake -DCMAKE_BUILD_TYPE=Release .
make && sudo make install
```

**macOS**:
```bash
brew install symengine
```

### C++20 Support Issues

Ensure your compiler supports C++20:
```bash
# GCC
g++ --version  # Should be 11+

# Clang
clang++ --version  # Should be 14+
```

### Missing Qt Charts

```bash
# Ubuntu/Debian
sudo apt install qt6-charts-dev

# Fedora
sudo dnf install qt6-qtcharts-devel

# macOS
brew install qt@6  # Charts included
```

## Development Build

For development with debugging symbols:

```bash
mkdir build-debug && cd build-debug
cmake .. -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_PREFIX_PATH="/path/to/Qt6"
cmake --build .
```

## IDE Support

### Qt Creator

1. Open `CalculusVisualizer.pro` or `CMakeLists.txt`
2. Configure kit with Qt 6.5+
3. Build and run

### Visual Studio Code

1. Install C/C++ and CMake Tools extensions
2. Open folder in VS Code
3. Select kit (CMake: Select a Kit)
4. Build (CMake: Build)

### CLion

1. Open project (CMakeLists.txt)
2. CLion auto-configures CMake
3. Build and run

## Release Build

For optimized release builds:

```bash
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

### Creating Distributable Package

**Windows**:
```powershell
cd build/Release
windeployqt CalculusVisualizer.exe
```

**Linux**:
```bash
# Use linuxdeployqt or create AppImage
```

**macOS**:
```bash
cd build
macdeployqt CalculusVisualizer.app -dmg
```

## Testing

Run the application:
```bash
# Linux/macOS
./build/CalculusVisualizer

# Windows
.\build\Release\CalculusVisualizer.exe
```

Test basic functionality:
1. Enter function: `x^2`
2. Click "Add to Graph"
3. Compute derivative
4. Check gradient descent tab

## Performance Optimization

For maximum performance:

```bash
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_FLAGS="-O3 -march=native"
```

## Notes

- First build may take 5-10 minutes due to Qt compilation
- Subsequent builds are incremental and much faster
- Use `-j<N>` with make for parallel compilation:
  ```bash
  cmake --build . -j8
  ```

## Getting Help

If you encounter issues:
1. Check Qt version: `qmake --version`
2. Check CMake version: `cmake --version`
3. Verify compiler: `g++ --version` or `clang++ --version`
4. Check SymEngine installation
5. Review CMake output for specific errors

---

## Related Notes
- [[BUILD]] - Shared calculusvisualizer/learning focus
- [[DERIVATIVE_ENGINE_README]] - Shared calculusvisualizer/learning focus
- [[IMPLEMENTATION_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[PROJECT_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[QUICKSTART]] - Shared calculusvisualizer/learning focus

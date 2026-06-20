---
date: 2026-05-26
title: "Build Instructions - Platform-Specific"
tags: [learning, probabilitystudio]
status: reference
type: note
---

# Build Instructions - Platform-Specific

## Windows (MSVC)

### Prerequisites
1. Install Visual Studio 2019 or later with C++ Desktop Development
2. Install Qt 6.x from https://www.qt.io/download-qt-installer
   - Select: Qt Charts, Qt 6.x for MSVC 2019 64-bit
3. Add Qt to PATH: `C:\Qt\6.x.x\msvc2019_64\bin`

### Build Steps
```cmd
# Open "x64 Native Tools Command Prompt for VS 2022"
cd C:\path\to\ProbabilityStudio
mkdir build
cd build

# Configure with CMake
cmake .. -G "Visual Studio 17 2022" -A x64 ^
  -DCMAKE_PREFIX_PATH="C:\Qt\6.5.0\msvc2019_64"

# Build
cmake --build . --config Release

# Run
cd Release
.\ProbabilityStudio.exe
```

### Alternative: Qt Creator
1. Open Qt Creator
2. File → Open File or Project
3. Select `CMakeLists.txt` or `ProbabilityStudio.pro`
4. Configure with MSVC kit
5. Build → Run

### Troubleshooting Windows
**Problem**: Qt6Charts.dll not found  
**Solution**: Copy Qt DLLs to executable directory or use `windeployqt`
```cmd
cd build\Release
windeployqt ProbabilityStudio.exe
```

---

## Linux (Ubuntu/Debian)

### Prerequisites
```bash
# Install build tools
sudo apt-get update
sudo apt-get install build-essential cmake git

# Install Qt 6 with Charts
sudo apt-get install qt6-base-dev qt6-charts-dev libqt6charts6

# Or Qt 5 if Qt 6 unavailable
sudo apt-get install qtbase5-dev libqt5charts5-dev
```

### Build Steps
```bash
cd ~/ProbabilityStudio
mkdir build && cd build

# Configure
cmake ..

# Build (use all CPU cores)
make -j$(nproc)

# Run
./ProbabilityStudio
```

### Install System-Wide (Optional)
```bash
sudo make install
# Or
sudo cmake --install .
```

### Troubleshooting Linux
**Problem**: Qt6 not found  
**Solution**: Specify Qt path
```bash
cmake .. -DCMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu/cmake/Qt6
```

**Problem**: libQt6Charts.so not found at runtime  
**Solution**: Update library cache
```bash
sudo ldconfig
```

---

## macOS

### Prerequisites
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Qt with Homebrew
brew install qt@6
brew install cmake
```

### Build Steps
```bash
cd ~/ProbabilityStudio
mkdir build && cd build

# Configure with Homebrew Qt
cmake .. -DCMAKE_PREFIX_PATH=$(brew --prefix qt@6)

# Build
make -j$(sysctl -n hw.ncpu)

# Run
./ProbabilityStudio
```

### Create .app Bundle (Optional)
```bash
# After building
macdeployqt ProbabilityStudio.app
```

### Troubleshooting macOS
**Problem**: Qt6 not found  
**Solution**: Link Qt
```bash
brew link qt@6 --force
```

**Problem**: Code signing issues  
**Solution**: Disable Gatekeeper for dev
```bash
xattr -dr com.apple.quarantine ProbabilityStudio.app
```

---

## Cross-Platform: Qt Creator (Recommended)

### Why Qt Creator?
- ✅ Handles Qt paths automatically
- ✅ Built-in debugger
- ✅ Visual form designer (if needed)
- ✅ One-click build & run

### Steps
1. **Install Qt Creator**
   - Download from https://www.qt.io/download-qt-installer
   - Install with Qt 6.x libraries + Qt Charts module

2. **Open Project**
   - Launch Qt Creator
   - File → Open File or Project
   - Navigate to `ProbabilityStudio.pro` (qmake) or `CMakeLists.txt` (CMake)

3. **Configure Kit**
   - Select Desktop Qt 6.x.x MSVC/GCC/Clang kit
   - Click "Configure Project"

4. **Build**
   - Click hammer icon 🔨 or press Ctrl+B
   - Wait for compilation to complete

5. **Run**
   - Click green play button ▶ or press Ctrl+R
   - Application launches!

---

## Building with qmake (Alternative to CMake)

### All Platforms
```bash
# Navigate to project directory
cd ProbabilityStudio

# Generate Makefile
qmake ProbabilityStudio.pro

# Build
make  # Linux/macOS
# OR
nmake  # Windows with MSVC
# OR
mingw32-make  # Windows with MinGW

# Run
./ProbabilityStudio  # Linux/macOS
# OR
release\ProbabilityStudio.exe  # Windows
```

---

## Continuous Integration / Docker

### Dockerfile Example (Ubuntu)
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    qt6-base-dev \
    qt6-charts-dev \
    libqt6charts6 \
    && rm -rf /var/lib/apt/lists/*

# Copy source
COPY . /app
WORKDIR /app

# Build
RUN mkdir build && cd build \
    && cmake .. \
    && make -j$(nproc)

# Run (requires X11 forwarding)
CMD ["./build/ProbabilityStudio"]
```

### GitHub Actions Example
```yaml
name: Build ProbabilityStudio

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        
    steps:
    - uses: actions/checkout@v3
    
    - name: Install Qt
      uses: jurplel/install-qt-action@v3
      with:
        version: '6.5.0'
        modules: 'qtcharts'
    
    - name: Configure CMake
      run: cmake -B build
      
    - name: Build
      run: cmake --build build --config Release
      
    - name: Upload Artifact
      uses: actions/upload-artifact@v3
      with:
        name: ProbabilityStudio-${{ matrix.os }}
        path: build/Release/ProbabilityStudio*
```

---

## Development Build (Debug Mode)

### For Active Development
```bash
# Enable debug symbols and assertions
cmake .. -DCMAKE_BUILD_TYPE=Debug

# Build with verbose output
make VERBOSE=1

# Run with debugger
gdb ./ProbabilityStudio
# OR
lldb ./ProbabilityStudio
```

### Qt Creator Debug Mode
1. Switch to Debug mode (left sidebar)
2. Set breakpoints by clicking line numbers
3. Run in debug mode (F5)
4. Step through code (F10, F11)

---

## Static Linking (Standalone Executable)

### Windows (MSVC)
```cmd
# Configure for static Qt
cmake .. -G "Visual Studio 17 2022" ^
  -DCMAKE_PREFIX_PATH="C:\Qt\6.5.0\msvc2019_64_static" ^
  -DQt6_DIR="C:\Qt\6.5.0\msvc2019_64_static\lib\cmake\Qt6"
  
# Build
cmake --build . --config Release

# Result: Standalone .exe with no DLL dependencies
```

### Linux (AppImage)
```bash
# Install linuxdeploy
wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

# Install Qt plugin
wget https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-x86_64.AppImage
chmod +x linuxdeploy-plugin-qt-x86_64.AppImage

# Create AppImage
./linuxdeploy-x86_64.AppImage --appdir AppDir \
  --executable ./build/ProbabilityStudio \
  --plugin qt \
  --output appimage
  
# Result: ProbabilityStudio-x86_64.AppImage (portable)
```

---

## Minimum Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Qt Version** | 5.15 | 6.5+ |
| **C++ Standard** | C++11 | C++17 |
| **CMake** | 3.16 | 3.25+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk Space** | 100 MB | 500 MB |
| **OS** | Win10, Ubuntu 20.04, macOS 11 | Latest |

---

## Dependency Tree

```
ProbabilityStudio
├── Qt6::Core (or Qt5::Core)
├── Qt6::Gui
├── Qt6::Widgets
└── Qt6::Charts
    └── Qt6::Widgets
```

No external dependencies beyond Qt!

---

## Verification

After building, verify installation:

```bash
# Check executable exists
ls -lh build/ProbabilityStudio  # Linux/Mac
dir build\Release\ProbabilityStudio.exe  # Windows

# Check linked libraries (Linux)
ldd build/ProbabilityStudio | grep Qt

# Check linked libraries (macOS)
otool -L build/ProbabilityStudio

# Run test (should launch GUI)
./build/ProbabilityStudio --version  # If version arg added
```

---

## Performance Optimization

### Compile Flags
```bash
# Maximum optimization
cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_CXX_FLAGS="-O3 -march=native"

# With Link-Time Optimization
cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON
```

### Profile-Guided Optimization (Advanced)
```bash
# Step 1: Build with profiling
cmake .. -DCMAKE_CXX_FLAGS="-fprofile-generate"
make
./ProbabilityStudio  # Use application normally

# Step 2: Rebuild with profile data
cmake .. -DCMAKE_CXX_FLAGS="-fprofile-use"
make
```

---

## Clean Build

```bash
# Remove build directory
rm -rf build

# Or clean with CMake
cmake --build build --target clean

# Or with make
make clean
```

---

## Common Build Errors

### Error: "Qt6Charts not found"
**Solution**:
```bash
# Install Qt Charts module
# Ubuntu/Debian
sudo apt-get install qt6-charts-dev

# Or specify Qt path
cmake .. -DCMAKE_PREFIX_PATH=/path/to/Qt/6.x.x/gcc_64
```

### Error: "undefined reference to vtable"
**Cause**: MOC (Meta-Object Compiler) not run  
**Solution**:
```bash
# Clean and rebuild
rm -rf build
mkdir build && cd build
cmake .. && make
```

### Error: C++11/17 features not available
**Solution**:
```bash
# Explicitly set C++ standard
cmake .. -DCMAKE_CXX_STANDARD=17
```

---

## IDE-Specific Setup

### Visual Studio Code
1. Install C++ and CMake extensions
2. Open folder in VS Code
3. CMake: Configure (Ctrl+Shift+P)
4. CMake: Build (F7)
5. Run from terminal

### CLion
1. Open CMakeLists.txt
2. Wait for indexing
3. Build → Build Project
4. Run → Run 'ProbabilityStudio'

---

**Build successful? Time to explore! 🚀**

See [QUICKSTART.md](QUICKSTART.md) for usage guide.

---

## Related Notes
- [[DELIVERY_SUMMARY]] - Shared probabilitystudio/learning focus
- [[IMPLEMENTATION_COMPLETE]] - Shared probabilitystudio/learning focus
- [[PROJECT_OVERVIEW]] - Shared probabilitystudio/learning focus
- [[QUICKSTART]] - Shared probabilitystudio/learning focus
- [[BUILD_AND_RUN]] - Related learning topic

#!/bin/bash
# Build script for Calculus Visualizer (Linux/macOS)

set -e

echo "========================================"
echo "Building Calculus Visualizer"
echo "========================================"

# Create build directory
mkdir -p build
cd build

# Configure with CMake
echo ""
echo "Configuring project..."
cmake .. -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="/usr/local/Qt-6.5.0"

# Build
echo ""
echo "Building..."
cmake --build . -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "Executable: build/CalculusVisualizer"
echo "========================================"

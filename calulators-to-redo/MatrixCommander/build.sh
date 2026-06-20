#!/bin/bash

# Build script for Matrix Commander on Linux/macOS

echo "========================================"
echo "Matrix Commander Build Script"
echo "========================================"
echo ""

# Check if qmake is available
if ! command -v qmake &> /dev/null; then
    echo "ERROR: qmake not found in PATH"
    echo "Please install Qt development tools"
    echo ""
    echo "Ubuntu/Debian: sudo apt-get install qt6-base-dev"
    echo "macOS: brew install qt"
    exit 1
fi

echo "[1/3] Running qmake..."
qmake MatrixCommander.pro
if [ $? -ne 0 ]; then
    echo "ERROR: qmake failed"
    exit 1
fi

echo ""
echo "[2/3] Building project..."
make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "[3/3] Build complete!"
echo ""
echo "Executable location: ./build/MatrixCommander"
echo ""
echo "To run: ./build/MatrixCommander"
echo ""

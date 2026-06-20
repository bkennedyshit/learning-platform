#!/bin/bash
# Loss Landscape 3D - Build Script for Linux/macOS

set -e  # Exit on error

echo "========================================"
echo "  Loss Landscape 3D - Build Script"
echo "========================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    QT_PATH=$(brew --prefix qt@6 2>/dev/null || echo "")
else
    OS="Linux"
    QT_PATH=""
fi

echo "Platform: $OS"

# Check for Qt
if [ "$OS" = "macOS" ]; then
    if [ -z "$QT_PATH" ]; then
        echo "ERROR: Qt 6 not found via Homebrew"
        echo ""
        echo "Install with: brew install qt@6"
        exit 1
    fi
    echo "Qt Path: $QT_PATH"
elif ! dpkg -l | grep -q qt6-base-dev; then
    echo "WARNING: Qt 6 may not be installed"
    echo "Install with: sudo apt install qt6-base-dev qt6-datavisualization-dev"
fi

echo ""

# Clean build directory
BUILD_DIR="build"
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning existing build directory..."
    rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Configure
echo ""
echo "Configuring with CMake..."
if [ -n "$QT_PATH" ]; then
    cmake .. -DCMAKE_PREFIX_PATH="$QT_PATH" -DCMAKE_BUILD_TYPE=Release
else
    cmake .. -DCMAKE_BUILD_TYPE=Release
fi

# Build
echo ""
echo "Building project..."
CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
make -j$CORES

# Success
echo ""
echo "========================================"
echo "  Build completed successfully!"
echo "========================================"
echo ""
echo "To run the application:"
if [ "$OS" = "macOS" ]; then
    echo "  open LossLandscape3D.app"
else
    echo "  ./LossLandscape3D"
fi
echo ""

cd ..

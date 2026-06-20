@echo off
REM Build script for Calculus Visualizer (Windows)

echo ========================================
echo Building Calculus Visualizer
echo ========================================

REM Create build directory
if not exist "build" mkdir build
cd build

REM Configure with CMake
echo.
echo Configuring project...
cmake .. -G "Visual Studio 17 2022" -A x64 ^
    -DCMAKE_PREFIX_PATH="C:/Qt/6.5.0/msvc2019_64" ^
    -DCMAKE_BUILD_TYPE=Release

if %ERRORLEVEL% NEQ 0 (
    echo Configuration failed!
    pause
    exit /b 1
)

REM Build
echo.
echo Building...
cmake --build . --config Release

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Executable: build\Release\CalculusVisualizer.exe
echo ========================================
pause

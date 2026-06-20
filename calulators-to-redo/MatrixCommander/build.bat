@echo off
REM Build script for Matrix Commander on Windows

echo ========================================
echo Matrix Commander Build Script
echo ========================================
echo.

REM Check if qmake is in PATH
where qmake >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: qmake not found in PATH
    echo Please ensure Qt is installed and qmake is in your PATH
    echo.
    echo Example: Add to PATH: C:\Qt\6.5.0\mingw_64\bin
    pause
    exit /b 1
)

echo [1/3] Running qmake...
qmake MatrixCommander.pro
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: qmake failed
    pause
    exit /b 1
)

echo.
echo [2/3] Building project...

REM Try to detect compiler
where mingw32-make >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using MinGW...
    mingw32-make
) else (
    where nmake >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo Using MSVC nmake...
        nmake
    ) else (
        echo ERROR: No compatible build tool found (mingw32-make or nmake)
        pause
        exit /b 1
    )
)

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [3/3] Build complete!
echo.
echo Executable location:
echo   - Release build: .\build\release\MatrixCommander.exe
echo   - Debug build: .\build\debug\MatrixCommander.exe
echo.
echo To run: cd build\release ^&^& MatrixCommander.exe
echo.

pause

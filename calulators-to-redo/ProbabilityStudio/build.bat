@echo off
REM ============================================================================
REM Probability Studio - Windows Build Script
REM ============================================================================
REM This script builds Probability Studio using CMake and Qt6
REM 
REM Prerequisites:
REM   - Qt6 installed (with QtCharts module)
REM   - CMake 3.16 or higher
REM   - Visual Studio 2019/2022 with C++ tools OR MinGW
REM
REM Usage:
REM   build.bat           - Build in Release mode
REM   build.bat clean     - Clean build directory
REM   build.bat debug     - Build in Debug mode
REM   build.bat run       - Build and run application
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set BUILD_DIR=build
set BUILD_TYPE=Release
set RUN_AFTER_BUILD=0
set CLEAN_BUILD=0

REM Parse arguments
:parse_args
if "%1"=="clean" (
    set CLEAN_BUILD=1
    shift
    goto parse_args
)
if "%1"=="debug" (
    set BUILD_TYPE=Debug
    shift
    goto parse_args
)
if "%1"=="run" (
    set RUN_AFTER_BUILD=1
    shift
    goto parse_args
)
if not "%1"=="" (
    echo Unknown argument: %1
    goto usage
)

REM Clean if requested
if %CLEAN_BUILD%==1 (
    echo ============================================================================
    echo Cleaning build directory...
    echo ============================================================================
    if exist %BUILD_DIR% (
        rmdir /s /q %BUILD_DIR%
        echo Build directory cleaned.
    ) else (
        echo Build directory does not exist, nothing to clean.
    )
    goto end
)

REM Check for Qt6
echo ============================================================================
echo Checking Qt6 installation...
echo ============================================================================

REM Common Qt6 installation paths
set QT_PATHS=C:\Qt\6.8.0\msvc2022_64;C:\Qt\6.7.0\msvc2022_64;C:\Qt\6.6.0\msvc2022_64;C:\Qt\6.5.0\msvc2022_64
set QT_PATHS=!QT_PATHS!;C:\Qt\6.8.0\mingw_64;C:\Qt\6.7.0\mingw_64;C:\Qt\6.6.0\mingw_64

set QT_FOUND=0
for %%p in (!QT_PATHS!) do (
    if exist "%%p\bin\qmake.exe" (
        set Qt6_DIR=%%p
        set PATH=%%p\bin;!PATH!
        set QT_FOUND=1
        echo Found Qt6 at: %%p
        goto qt_found
    )
)

:qt_found
if %QT_FOUND%==0 (
    echo ERROR: Qt6 not found in common paths!
    echo Please install Qt6 or set Qt6_DIR environment variable.
    echo Example: set Qt6_DIR=C:\Qt\6.8.0\msvc2022_64
    goto error
)

REM Check for CMake
echo ============================================================================
echo Checking CMake installation...
echo ============================================================================
where cmake >nul 2>&1
if errorlevel 1 (
    echo ERROR: CMake not found in PATH!
    echo Please install CMake from https://cmake.org/download/
    goto error
)
cmake --version

REM Create build directory
echo ============================================================================
echo Creating build directory...
echo ============================================================================
if not exist %BUILD_DIR% mkdir %BUILD_DIR%

REM Configure with CMake
echo ============================================================================
echo Configuring CMake (Build Type: %BUILD_TYPE%)...
echo ============================================================================
cd %BUILD_DIR%
cmake .. -DCMAKE_BUILD_TYPE=%BUILD_TYPE% -DCMAKE_PREFIX_PATH=%Qt6_DIR%
if errorlevel 1 (
    echo ERROR: CMake configuration failed!
    cd ..
    goto error
)

REM Build
echo ============================================================================
echo Building Probability Studio...
echo ============================================================================
cmake --build . --config %BUILD_TYPE% -j %NUMBER_OF_PROCESSORS%
if errorlevel 1 (
    echo ERROR: Build failed!
    cd ..
    goto error
)

cd ..

echo ============================================================================
echo Build completed successfully!
echo ============================================================================
echo Executable location: %BUILD_DIR%\%BUILD_TYPE%\ProbabilityStudio.exe
echo.

REM Run if requested
if %RUN_AFTER_BUILD%==1 (
    echo ============================================================================
    echo Launching Probability Studio...
    echo ============================================================================
    if exist %BUILD_DIR%\%BUILD_TYPE%\ProbabilityStudio.exe (
        start "" %BUILD_DIR%\%BUILD_TYPE%\ProbabilityStudio.exe
    ) else if exist %BUILD_DIR%\ProbabilityStudio.exe (
        start "" %BUILD_DIR%\ProbabilityStudio.exe
    ) else (
        echo ERROR: Executable not found!
        goto error
    )
)

goto end

:usage
echo Usage: build.bat [options]
echo.
echo Options:
echo   clean    - Clean build directory
echo   debug    - Build in Debug mode (default: Release)
echo   run      - Build and run application
echo.
echo Examples:
echo   build.bat              Build in Release mode
echo   build.bat debug        Build in Debug mode
echo   build.bat run          Build and run
echo   build.bat clean        Clean build directory
goto end

:error
echo.
echo ============================================================================
echo BUILD FAILED!
echo ============================================================================
exit /b 1

:end
endlocal

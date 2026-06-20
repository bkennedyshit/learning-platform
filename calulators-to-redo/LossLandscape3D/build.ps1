# Loss Landscape 3D - Build Script for Windows
# Usage: .\build.ps1

param(
    [string]$QtPath = "C:\Qt\6.7.0\msvc2019_64",
    [string]$BuildType = "Release"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Loss Landscape 3D - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Qt path exists
if (-not (Test-Path $QtPath)) {
    Write-Host "ERROR: Qt path not found: $QtPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please specify Qt path:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 -QtPath 'C:\Qt\6.7.0\msvc2019_64'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Qt Path: $QtPath" -ForegroundColor Green
Write-Host "Build Type: $BuildType" -ForegroundColor Green
Write-Host ""

# Create build directory
$BuildDir = "build"
if (Test-Path $BuildDir) {
    Write-Host "Cleaning existing build directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $BuildDir
}

New-Item -ItemType Directory -Path $BuildDir | Out-Null
Set-Location $BuildDir

# Configure with CMake
Write-Host ""
Write-Host "Configuring with CMake..." -ForegroundColor Cyan
cmake .. -DCMAKE_PREFIX_PATH="$QtPath" -DCMAKE_BUILD_TYPE=$BuildType

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: CMake configuration failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Build
Write-Host ""
Write-Host "Building project..." -ForegroundColor Cyan
cmake --build . --config $BuildType

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Success
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Build completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location:" -ForegroundColor Cyan
Write-Host "  $BuildDir\$BuildType\LossLandscape3D.exe" -ForegroundColor White
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "  cd $BuildDir\$BuildType" -ForegroundColor White
Write-Host "  .\LossLandscape3D.exe" -ForegroundColor White
Write-Host ""

Set-Location ..

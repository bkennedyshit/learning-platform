# Qt Installation & Calculator Build Guide
# Run this script to check prerequisites and get installation instructions

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CALCULATOR SUITE - SETUP CHECKER" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$results = @()

# Check 1: Qt Installation
Write-Host "[1/4] Checking for Qt..." -ForegroundColor Yellow
$qtPaths = @("C:\Qt", "C:\Qt6", "$env:USERPROFILE\Qt", "C:\Program Files\Qt")
$qtFound = $false
$qtPath = ""

foreach($path in $qtPaths) {
    if(Test-Path $path) {
        $qtFound = $true
        $qtPath = $path
        $versions = Get-ChildItem $path -Directory | Where-Object { $_.Name -match "^\d" }
        Write-Host "  ✅ Qt found at: $path" -ForegroundColor Green
        Write-Host "  Versions: $($versions.Name -join ', ')" -ForegroundColor Gray
        break
    }
}

if(-not $qtFound) {
    Write-Host "  ❌ Qt NOT found" -ForegroundColor Red
    Write-Host "  📥 Install from: https://www.qt.io/download-qt-installer" -ForegroundColor Cyan
    Write-Host "  📋 Components needed:" -ForegroundColor Gray
    Write-Host "     - Qt 6.5+ (latest stable)" -ForegroundColor Gray
    Write-Host "     - Qt Widgets" -ForegroundColor Gray
    Write-Host "     - Qt Charts" -ForegroundColor Gray
    Write-Host "     - Qt DataVisualization" -ForegroundColor Gray
    Write-Host "     - MinGW 64-bit compiler" -ForegroundColor Gray
    Write-Host "     - CMake" -ForegroundColor Gray
    Write-Host "     - Qt Creator (recommended IDE)" -ForegroundColor Gray
    $results += @{Check="Qt Framework"; Status="NOT INSTALLED"; Required=$true}
} else {
    $results += @{Check="Qt Framework"; Status="INSTALLED"; Required=$true}
}

Write-Host ""

# Check 2: CMake
Write-Host "[2/4] Checking for CMake..." -ForegroundColor Yellow
try {
    $cmakeVersion = (cmake --version 2>$null | Select-Object -First 1)
    if($cmakeVersion) {
        Write-Host "  ✅ CMake found: $cmakeVersion" -ForegroundColor Green
        $results += @{Check="CMake"; Status="INSTALLED"; Required=$true}
    } else {
        throw "Not found"
    }
} catch {
    Write-Host "  ❌ CMake NOT found" -ForegroundColor Red
    Write-Host "  📥 Install: winget install Kitware.CMake" -ForegroundColor Cyan
    Write-Host "     OR download from: https://cmake.org/download/" -ForegroundColor Cyan
    $results += @{Check="CMake"; Status="NOT INSTALLED"; Required=$true}
}

Write-Host ""

# Check 3: C++ Compiler
Write-Host "[3/4] Checking for C++ compiler..." -ForegroundColor Yellow
$compilerFound = $false

# Check for MinGW (comes with Qt)
try {
    $gccVersion = (g++ --version 2>$null | Select-Object -First 1)
    if($gccVersion) {
        Write-Host "  ✅ MinGW/GCC found: $gccVersion" -ForegroundColor Green
        $compilerFound = $true
    }
} catch {}

# Check for MSVC
try {
    $clVersion = (cl 2>&1 | Select-String "Version" | Select-Object -First 1)
    if($clVersion) {
        Write-Host "  ✅ MSVC found: $clVersion" -ForegroundColor Green
        $compilerFound = $true
    }
} catch {}

if(-not $compilerFound) {
    Write-Host "  ❌ C++ compiler NOT found" -ForegroundColor Red
    Write-Host "  📋 Options:" -ForegroundColor Cyan
    Write-Host "     1. Install Qt with MinGW (recommended)" -ForegroundColor Gray
    Write-Host "     2. Install Visual Studio Build Tools" -ForegroundColor Gray
    $results += @{Check="C++ Compiler"; Status="NOT INSTALLED"; Required=$true}
} else {
    $results += @{Check="C++ Compiler"; Status="INSTALLED"; Required=$true}
}

Write-Host ""

# Check 4: Projects
Write-Host "[4/4] Checking calculator projects..." -ForegroundColor Yellow
$projectsPath = "C:\Obsidian Vault\Learning_Tools"
if(Test-Path $projectsPath) {
    $projects = Get-ChildItem $projectsPath -Directory | Where-Object { $_.Name -notmatch "^\." }
    Write-Host "  ✅ Projects folder found" -ForegroundColor Green
    Write-Host "  📁 Projects ($($projects.Count)):" -ForegroundColor Gray
    foreach($proj in $projects) {
        $proFile = Get-ChildItem "$($proj.FullName)\*.pro" -ErrorAction SilentlyContinue
        $cppFiles = (Get-ChildItem "$($proj.FullName)\src\*.cpp" -ErrorAction SilentlyContinue).Count
        if($proFile) {
            Write-Host "     ✓ $($proj.Name) ($cppFiles C++ files)" -ForegroundColor Gray
        }
    }
    $results += @{Check="Projects"; Status="READY"; Required=$true}
} else {
    Write-Host "  ❌ Projects folder NOT found at: $projectsPath" -ForegroundColor Red
    $results += @{Check="Projects"; Status="MISSING"; Required=$true}
}

Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allReady = $true
foreach($result in $results) {
    $status = if($result.Status -match "INSTALLED|READY") { "✅" } else { "❌" }
    $color = if($result.Status -match "INSTALLED|READY") { "Green" } else { "Red" }
    Write-Host "$status $($result.Check): $($result.Status)" -ForegroundColor $color
    if($result.Required -and $result.Status -notmatch "INSTALLED|READY") {
        $allReady = $false
    }
}

Write-Host ""

if($allReady) {
    Write-Host "🎉 ALL PREREQUISITES MET!" -ForegroundColor Green
    Write-Host "`nNext step: Run build-all-calculators.ps1 to build all 4 calculators" -ForegroundColor Cyan
    Write-Host "   OR open individual .pro files in Qt Creator" -ForegroundColor Gray
} else {
    Write-Host "⚠️  SETUP INCOMPLETE" -ForegroundColor Yellow
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Install missing components (see above)" -ForegroundColor Gray
    Write-Host "2. Run this script again to verify" -ForegroundColor Gray
    Write-Host "3. Then run build-all-calculators.ps1" -ForegroundColor Gray
    
    Write-Host "`n📚 Quick Install (if you have winget):" -ForegroundColor Cyan
    Write-Host "   # CMake" -ForegroundColor Gray
    Write-Host "   winget install Kitware.CMake" -ForegroundColor White
    Write-Host ""
    Write-Host "   # Qt (manual download required)" -ForegroundColor Gray
    Write-Host "   # Visit: https://www.qt.io/download-qt-installer" -ForegroundColor White
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

# Offer to open Qt download page
$response = Read-Host "Open Qt download page in browser? (y/n)"
if($response -eq 'y') {
    Start-Process "https://www.qt.io/download-qt-installer"
}

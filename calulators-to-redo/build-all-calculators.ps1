# Build All Calculators - Automated Build Script
# This script builds all 4 Qt calculators in sequence

param(
    [string]$QtPath = "",
    [switch]$SkipTests = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CALCULATOR SUITE - BUILD ALL" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Find Qt installation
if([string]::IsNullOrEmpty($QtPath)) {
    Write-Host "🔍 Searching for Qt installation..." -ForegroundColor Yellow
    $qtSearchPaths = @(
        "C:\Qt\6.*\mingw*",
        "C:\Qt\6.*\msvc*",
        "$env:USERPROFILE\Qt\6.*\mingw*",
        "$env:USERPROFILE\Qt\6.*\msvc*"
    )
    
    foreach($searchPath in $qtSearchPaths) {
        $found = Get-Item $searchPath -ErrorAction SilentlyContinue | Select-Object -First 1
        if($found) {
            $QtPath = $found.FullName
            Write-Host "  ✅ Found Qt at: $QtPath" -ForegroundColor Green
            break
        }
    }
    
    if([string]::IsNullOrEmpty($QtPath)) {
        Write-Host "  ❌ Qt not found!" -ForegroundColor Red
        Write-Host "  Run: .\setup-check.ps1 to install prerequisites" -ForegroundColor Yellow
        exit 1
    }
}

# Setup environment
$env:PATH = "$QtPath\bin;$env:PATH"
$env:Qt6_DIR = $QtPath

# Projects to build
$projects = @(
    @{Name="Matrix Commander"; Dir="MatrixCommander"; Time="~5 min"},
    @{Name="Calculus Visualizer"; Dir="CalculusVisualizer"; Time="~4 min"},
    @{Name="Loss Landscape 3D"; Dir="LossLandscape3D"; Time="~5 min"},
    @{Name="Probability Studio"; Dir="ProbabilityStudio"; Time="~4 min"}
)

$rootDir = "C:\Obsidian Vault\Learning_Tools"
$buildResults = @()
$totalStart = Get-Date

Write-Host "📋 Build Plan:" -ForegroundColor Cyan
foreach($proj in $projects) {
    Write-Host "  • $($proj.Name) (est. $($proj.Time))" -ForegroundColor Gray
}
Write-Host ""

# Build each project
$projectNum = 1
foreach($proj in $projects) {
    $projStart = Get-Date
    $projPath = Join-Path $rootDir $proj.Dir
    $buildPath = Join-Path $projPath "build"
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "[$projectNum/4] Building $($proj.Name)" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    if(-not (Test-Path $projPath)) {
        Write-Host "❌ Project not found: $projPath" -ForegroundColor Red
        $buildResults += @{Project=$proj.Name; Status="NOT FOUND"; Time="N/A"}
        $projectNum++
        continue
    }
    
    Write-Host "📁 Project: $projPath" -ForegroundColor Gray
    
    # Clean previous build
    if(Test-Path $buildPath) {
        Write-Host "🧹 Cleaning previous build..." -ForegroundColor Yellow
        Remove-Item $buildPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    # Create build directory
    New-Item -ItemType Directory -Path $buildPath -Force | Out-Null
    Set-Location $buildPath
    
    # Run CMake
    Write-Host "⚙️  Running CMake..." -ForegroundColor Yellow
    $cmakeCmd = "cmake .. -G `"MinGW Makefiles`" -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=`"$QtPath`""
    
    if($Verbose) {
        Write-Host "   Command: $cmakeCmd" -ForegroundColor DarkGray
    }
    
    $cmakeOutput = Invoke-Expression $cmakeCmd 2>&1
    
    if($LASTEXITCODE -ne 0) {
        Write-Host "❌ CMake configuration failed!" -ForegroundColor Red
        if($Verbose) {
            Write-Host $cmakeOutput -ForegroundColor DarkRed
        }
        $buildResults += @{Project=$proj.Name; Status="CMAKE FAILED"; Time="N/A"}
        Set-Location $rootDir
        $projectNum++
        continue
    }
    
    Write-Host "   ✅ CMake configured successfully" -ForegroundColor Green
    
    # Build
    Write-Host "🔨 Building (this may take a few minutes)..." -ForegroundColor Yellow
    $buildCmd = "cmake --build . --config Release"
    
    $buildOutput = Invoke-Expression $buildCmd 2>&1
    
    if($LASTEXITCODE -ne 0) {
        Write-Host "❌ Build failed!" -ForegroundColor Red
        if($Verbose) {
            Write-Host $buildOutput -ForegroundColor DarkRed
        }
        $buildResults += @{Project=$proj.Name; Status="BUILD FAILED"; Time="N/A"}
        Set-Location $rootDir
        $projectNum++
        continue
    }
    
    $projEnd = Get-Date
    $projDuration = ($projEnd - $projStart).TotalSeconds
    
    Write-Host "   ✅ Build completed in $([math]::Round($projDuration, 1))s" -ForegroundColor Green
    
    # Find executable
    $exePattern = "$buildPath\**\$($proj.Dir).exe"
    $exe = Get-ChildItem $exePattern -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if($exe) {
        $exeSize = [math]::Round($exe.Length / 1MB, 2)
        Write-Host "   📦 Executable: $($exe.Name) ($exeSize MB)" -ForegroundColor Cyan
        Write-Host "   📂 Location: $($exe.DirectoryName)" -ForegroundColor Gray
        $buildResults += @{Project=$proj.Name; Status="SUCCESS"; Time="$([math]::Round($projDuration, 1))s"; Exe=$exe.FullName}
    } else {
        Write-Host "   ⚠️  Executable not found (build may have succeeded but exe location unknown)" -ForegroundColor Yellow
        $buildResults += @{Project=$proj.Name; Status="EXE NOT FOUND"; Time="$([math]::Round($projDuration, 1))s"}
    }
    
    Set-Location $rootDir
    Write-Host ""
    $projectNum++
}

# Final summary
$totalEnd = Get-Date
$totalDuration = ($totalEnd - $totalStart).TotalMinutes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BUILD SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$successCount = 0
foreach($result in $buildResults) {
    if($result.Status -eq "SUCCESS") {
        Write-Host "✅ $($result.Project) - Built in $($result.Time)" -ForegroundColor Green
        if($result.Exe) {
            Write-Host "   📂 $($result.Exe)" -ForegroundColor Gray
        }
        $successCount++
    } elseif($result.Status -eq "EXE NOT FOUND") {
        Write-Host "⚠️  $($result.Project) - Build completed but exe not found" -ForegroundColor Yellow
        $successCount++
    } else {
        Write-Host "❌ $($result.Project) - $($result.Status)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Total build time: $([math]::Round($totalDuration, 1)) minutes" -ForegroundColor Cyan
Write-Host "Success rate: $successCount/$($projects.Count)" -ForegroundColor $(if($successCount -eq $projects.Count){"Green"}else{"Yellow"})

if($successCount -eq $projects.Count) {
    Write-Host "`n🎉 ALL CALCULATORS BUILT SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Find executables in each project's build/ folder" -ForegroundColor Gray
    Write-Host "  2. Create desktop shortcuts (optional)" -ForegroundColor Gray
    Write-Host "  3. Start learning AI/ML math!" -ForegroundColor Gray
    Write-Host "`nOr run individual calculators:" -ForegroundColor Cyan
    foreach($result in $buildResults) {
        if($result.Exe) {
            Write-Host "  • $($result.Project):" -ForegroundColor Gray
            Write-Host "    $($result.Exe)" -ForegroundColor White
        }
    }
} else {
    Write-Host "`n⚠️  Some builds failed. Check errors above." -ForegroundColor Yellow
    Write-Host "Run with -Verbose flag for detailed output." -ForegroundColor Gray
    Write-Host "`nOr open individual projects in Qt Creator:" -ForegroundColor Cyan
    foreach($proj in $projects) {
        $proFile = Join-Path "$rootDir\$($proj.Dir)" "$($proj.Dir).pro"
        if(Test-Path $proFile) {
            Write-Host "  • $proFile" -ForegroundColor Gray
        }
    }
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

# Create launcher script if all succeeded
if($successCount -eq $projects.Count) {
    $launcherPath = Join-Path $rootDir "launch-calculators.ps1"
    $launcherContent = @"
# Quick launcher for all calculators
Write-Host "Select calculator to launch:" -ForegroundColor Cyan
Write-Host "1. Matrix Commander" -ForegroundColor White
Write-Host "2. Calculus Visualizer" -ForegroundColor White
Write-Host "3. Loss Landscape 3D" -ForegroundColor White
Write-Host "4. Probability Studio" -ForegroundColor White
Write-Host "5. Launch all" -ForegroundColor White
Write-Host ""

`$choice = Read-Host "Enter choice (1-5)"

`$exes = @(
"@
    
    foreach($result in $buildResults) {
        if($result.Exe) {
            $launcherContent += "`n    `"$($result.Exe)`","
        }
    }
    
    $launcherContent += @"

)

switch(`$choice) {
    "1" { Start-Process `$exes[0] }
    "2" { Start-Process `$exes[1] }
    "3" { Start-Process `$exes[2] }
    "4" { Start-Process `$exes[3] }
    "5" { foreach(`$exe in `$exes) { Start-Process `$exe } }
    default { Write-Host "Invalid choice" -ForegroundColor Red }
}
"@
    
    $launcherContent | Out-File $launcherPath -Encoding UTF8
    Write-Host "📝 Created launcher script: $launcherPath" -ForegroundColor Green
}

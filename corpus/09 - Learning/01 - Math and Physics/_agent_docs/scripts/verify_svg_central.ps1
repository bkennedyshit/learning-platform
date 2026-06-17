$root = "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning"
$central = Join-Path $root '_svgs'
$svgs = Get-ChildItem -Path $central -Filter '*.svg' -File -ErrorAction SilentlyContinue
$count = $svgs.Count
$bytes = ($svgs | Measure-Object Length -Sum).Sum
$kb = if ($bytes) { [math]::Round($bytes/1024, 1) } else { 0 }
Write-Host ("Central _svgs/: {0} files, {1} KB" -f $count, $kb)
Write-Host ""

$remaining = Get-ChildItem -Path $root -Directory -Recurse -Filter '_svgs' -ErrorAction SilentlyContinue |
             Where-Object { $_.FullName -ne $central }
if ($remaining) {
    Write-Host "Remaining per-subject _svgs folders:"
    foreach ($d in $remaining) {
        $fileCount = (Get-ChildItem $d.FullName -File -ErrorAction SilentlyContinue).Count
        $rel = $d.FullName.Substring($root.Length + 1)
        Write-Host ("  {0}  ({1} files)" -f $rel, $fileCount)
    }
} else {
    Write-Host "No per-subject _svgs/ folders remain."
}

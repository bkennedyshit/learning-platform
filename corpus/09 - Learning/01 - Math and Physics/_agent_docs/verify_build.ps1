$root = "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\07 - Math and Physics"
$subjects = @(
  '01 - Mathematical Foundations & Calculus',
  '02 - Linear Algebra & Matrix Theory',
  '03 - Ordinary & Partial Differential Equations',
  '04 - Classical Mechanics & Dynamical Systems',
  '05 - Thermodynamics & Statistical Mechanics',
  '06 - Fluid Dynamics & Continuum Mechanics',
  '07 - Electrodynamics & Classical Field Theory',
  '08 - Special & General Relativity',
  '09 - Quantum Mechanics & Quantum Field Theory',
  '10 - Aerospace Engineering & Orbital Mechanics',
  '11 - Control Theory & Systems Engineering',
  '12 - Solid Mechanics & Materials Science'
)
foreach ($s in $subjects) {
  $sd = Join-Path $root $s
  $chapters = Get-ChildItem -Path $sd -Filter '*.md' -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne 'Subject_Plan.md' }
  $cnt = $chapters.Count
  $bytes = ($chapters | Measure-Object Length -Sum).Sum
  $kb = if ($bytes) { [math]::Round($bytes/1024,1) } else { 0 }
  $scripts = Get-ChildItem -Path (Join-Path $sd '_practice\scripts') -Filter '*.py' -File -ErrorAction SilentlyContinue
  $scnt = $scripts.Count
  $sbytes = ($scripts | Measure-Object Length -Sum).Sum
  $skb = if ($sbytes) { [math]::Round($sbytes/1024,1) } else { 0 }
  $line = "{0,-55} chapters {1,2}  ({2,7} KB)   scripts {3,2}  ({4,5} KB)" -f $s, $cnt, $kb, $scnt, $skb
  Write-Host $line
}

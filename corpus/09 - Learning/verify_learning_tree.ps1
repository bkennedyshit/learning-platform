$root = "C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning"
$tracks = @(
  '07 - Math and Physics',
  '01- Python',
  '02 - C++',
  '03 - C hash',
  '04 - Game_Dev',
  '05 - AI_Experiments',
  '05 - JavaScript',
  '06 - Game Design',
  '06 - TypeScript',
  '07 - SQL',
  '08 - App Architectures & Frameworks',
  '09 - VR & 3D Engineering',
  '10 - AI & Machine Learning Systems',
  '11 - Neuroscience & Computational Cognition',
  '12 - Behavioral Psychology & Reinforcement Learning',
  '13 - Biomechanics & Human-Computer Interface (HCI)',
  '14 - Rust',
  '15 - Biology',
  '16 - Chemistry'
)
foreach ($t in $tracks) {
  $td = Join-Path $root $t
  if (-not (Test-Path $td)) { continue }
  # Count chapter .md files at depth-1 of the track (excluding Subject_Plan)
  $chapters = Get-ChildItem -Path $td -Filter '*.md' -File -ErrorAction SilentlyContinue |
              Where-Object { $_.Name -notmatch '^(Subject_Plan|README|Index)\.md$' }
  # Math/physics has subject-folders one level deeper
  if ($t -eq '07 - Math and Physics') {
    $chapters = Get-ChildItem -Path $td -Recurse -Filter '*.md' -File -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -notmatch '^(Subject_Plan|README|Index|.* Index)\.md$' -and $_.FullName -notmatch '_practice|_agent_docs|_examples|_svgs' }
  }
  $cnt = $chapters.Count
  $bytes = ($chapters | Measure-Object Length -Sum).Sum
  $kb = if ($bytes) { [math]::Round($bytes/1024,1) } else { 0 }
  $under30 = ($chapters | Where-Object { $_.Length -lt 30720 }).Count

  # Practice / examples
  $scripts = @()
  foreach ($d in @('_practice\scripts', '_examples')) {
    $sp = Join-Path $td $d
    if (Test-Path $sp) {
      $scripts += Get-ChildItem -Path $sp -Recurse -File -ErrorAction SilentlyContinue
    }
  }
  $scnt = $scripts.Count
  $sbytes = ($scripts | Measure-Object Length -Sum).Sum
  $skb = if ($sbytes) { [math]::Round($sbytes/1024,1) } else { 0 }

  $line = "{0,-58} ch {1,3}  ({2,7} KB, {3,2} under 30KB)   art {4,3}  ({5,5} KB)" -f $t, $cnt, $kb, $under30, $scnt, $skb
  Write-Host $line
}

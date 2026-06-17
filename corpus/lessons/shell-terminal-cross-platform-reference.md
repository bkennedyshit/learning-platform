---
title: "Shell & Terminal — Cross-Platform Reference"
subject: "Dev_Tools"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 💻 Shell & Terminal — Cross-Platform Reference

> The same idea, three different languages. This document is the Rosetta Stone.

---

## Which Shell Are You In?

| Platform | Default Shell | Where to find it |
|---------|-------------|-----------------|
| **Linux** | `bash` (most distros) | Terminal app; any CLI |
| **macOS** (Catalina+) | `zsh` | Terminal.app, iTerm2 |
| **macOS** (older) | `bash` | Same |
| **Windows** | `PowerShell` (modern) or `cmd.exe` (legacy) | Windows Terminal, Start → PowerShell |
| **Windows** (with WSL) | `bash` | Windows Terminal → Ubuntu tab |
| **Git Bash** (Windows) | `bash` | Installed with Git for Windows |

> **Recommendation:** On Windows, use **Windows Terminal** + **PowerShell 7** (not the old Windows PowerShell) + **WSL2** (Ubuntu). On Mac/Linux, you already have what you need. Install **Git Bash** on Windows if you want bash syntax without WSL.

---

## The Core Concept: Why Three Different Syntaxes?

- **Bash/Zsh (Linux + Mac):** Born on Unix in the 1970s. The `/` separator, the `ls` command, pipes (`|`), the `$VARIABLE` syntax — all from Unix. Bash and Zsh are nearly identical for everyday use.
- **CMD (Windows):** Microsoft's original shell from DOS (1981). Ancient. `dir` instead of `ls`, `\` separators, `%VARIABLE%`. Avoid it for anything non-trivial.
- **PowerShell:** Microsoft's modern shell (2006+). Runs on Windows, Mac, and Linux. Uses *objects* instead of text streams — more powerful than bash in some ways, different philosophy. `Get-ChildItem` instead of `ls` (though `ls` works as an alias).

---

## Side-by-Side Command Reference

### Navigation

| Action | Bash/Zsh (Linux/Mac) | PowerShell (Windows) | CMD (Windows, legacy) |
|--------|---------------------|---------------------|----------------------|
| Show current directory | `pwd` | `pwd` or `Get-Location` | `cd` (no args) |
| List files | `ls` | `ls` or `Get-ChildItem` | `dir` |
| List files (long format) | `ls -la` | `ls -Force` or `Get-ChildItem -Force` | `dir /a` |
| Change directory | `cd folder` | `cd folder` or `Set-Location folder` | `cd folder` |
| Go up one level | `cd ..` | `cd ..` | `cd ..` |
| Go to home directory | `cd ~` | `cd ~` or `cd $HOME` | `cd %USERPROFILE%` |
| Go to previous directory | `cd -` | `cd -` (PS7+) | *(no equivalent)* |
| Go to root | `cd /` | `cd /` (within a drive) | `cd \` |
| Show path of a command | `which python` | `Get-Command python` | `where python` |

### Files & Directories

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| Create empty file | `touch file.txt` | `New-Item file.txt` | `type nul > file.txt` |
| Create directory | `mkdir folder` | `mkdir folder` or `New-Item -Type Directory` | `mkdir folder` |
| Create nested dirs | `mkdir -p a/b/c` | `mkdir a\b\c` (auto-creates) | `mkdir a\b\c` |
| Copy file | `cp file.txt copy.txt` | `cp file.txt copy.txt` or `Copy-Item` | `copy file.txt copy.txt` |
| Copy directory | `cp -r folder/ backup/` | `cp -Recurse folder backup` | `xcopy folder backup /e /i` |
| Move/rename | `mv old.txt new.txt` | `mv old.txt new.txt` or `Move-Item` | `move old.txt new.txt` |
| Delete file | `rm file.txt` | `rm file.txt` or `Remove-Item` | `del file.txt` |
| Delete directory | `rm -r folder` | `rm -Recurse folder` | `rmdir /s /q folder` |
| Force delete | `rm -rf folder` | `rm -Recurse -Force folder` | `rmdir /s /q folder` |
| Print file contents | `cat file.txt` | `cat file.txt` or `Get-Content` | `type file.txt` |
| First N lines | `head -n 20 file.txt` | `Get-Content file.txt -Head 20` | *(no direct equivalent)* |
| Last N lines | `tail -n 20 file.txt` | `Get-Content file.txt -Tail 20` | *(no direct equivalent)* |
| Follow a log live | `tail -f log.txt` | `Get-Content log.txt -Wait` | *(no direct equivalent)* |
| Page through file | `less file.txt` | `more file.txt` | `more file.txt` |

### Searching & Finding

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| Find file by name | `find . -name "*.py"` | `Get-ChildItem -Recurse -Filter *.py` | `dir *.py /s` |
| Search text in file | `grep "pattern" file.txt` | `Select-String "pattern" file.txt` | `findstr "pattern" file.txt` |
| Search recursively | `grep -r "pattern" .` | `Get-ChildItem -Recurse \| Select-String "pattern"` | `findstr /s "pattern" *` |
| Case-insensitive grep | `grep -i "pattern" file.txt` | `Select-String -CaseSensitive:$false "pattern" file.txt` | `findstr /i "pattern" file.txt` |
| Count lines in file | `wc -l file.txt` | `(Get-Content file.txt).Count` | `find /c /v "" file.txt` |
| Find files modified recently | `find . -mtime -1` | `Get-ChildItem -Recurse \| Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}` | *(complex)* |

### Processes

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| List running processes | `ps aux` | `Get-Process` | `tasklist` |
| Kill process by PID | `kill 1234` | `Stop-Process -Id 1234` | `taskkill /PID 1234 /F` |
| Kill by name | `pkill python` | `Stop-Process -Name python` | `taskkill /IM python.exe /F` |
| Run in background | `command &` | `Start-Job { command }` | `start /b command` |
| Show what's using a port | `lsof -i :8080` | `netstat -ano \| findstr :8080` | `netstat -ano \| findstr :8080` |

### Environment Variables

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| Print a variable | `echo $HOME` | `echo $HOME` or `$env:USERPROFILE` | `echo %USERPROFILE%` |
| List all env vars | `env` or `printenv` | `Get-ChildItem Env:` | `set` |
| Set a variable (session) | `export MY_VAR=hello` | `$env:MY_VAR = "hello"` | `set MY_VAR=hello` |
| Set a variable (permanent) | Add to `~/.bashrc` or `~/.zshrc` | `[System.Environment]::SetEnvironmentVariable(...)` | `setx MY_VAR hello` |
| Unset a variable | `unset MY_VAR` | `Remove-Item Env:MY_VAR` | `set MY_VAR=` |
| Check PATH | `echo $PATH` | `$env:PATH` | `echo %PATH%` |

### Pipes, Redirection & Output

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| Pipe output to next command | `cmd1 \| cmd2` | `cmd1 \| cmd2` | `cmd1 \| cmd2` |
| Redirect output to file | `cmd > file.txt` | `cmd > file.txt` or `\| Out-File file.txt` | `cmd > file.txt` |
| Append to file | `cmd >> file.txt` | `cmd >> file.txt` or `\| Add-Content file.txt` | `cmd >> file.txt` |
| Discard output | `cmd > /dev/null` | `cmd \| Out-Null` or `cmd > $null` | `cmd > nul` |
| Redirect stderr | `cmd 2> errors.txt` | `cmd 2> errors.txt` | `cmd 2> errors.txt` |
| Redirect both stdout+stderr | `cmd > out.txt 2>&1` | `cmd > out.txt 2>&1` | `cmd > out.txt 2>&1` |
| Count output lines | `cmd \| wc -l` | `cmd \| Measure-Object -Line` | *(complex)* |

### Networking

| Action | Bash/Zsh | PowerShell | CMD |
|--------|----------|-----------|-----|
| Test connection to host | `ping google.com` | `ping google.com` or `Test-Connection google.com` | `ping google.com` |
| Show network config | `ifconfig` or `ip addr` | `Get-NetIPAddress` or `ipconfig` | `ipconfig` |
| Download a file | `curl -O url` or `wget url` | `Invoke-WebRequest -Uri url -OutFile file` | *(needs curl.exe or browser)* |
| Make HTTP request | `curl -X GET url` | `Invoke-RestMethod -Uri url` | `curl url` (Win10+) |
| Show open connections | `netstat -tuln` | `netstat -an` | `netstat -an` |
| DNS lookup | `nslookup domain` | `Resolve-DnsName domain` | `nslookup domain` |

---

## File Paths — The Separator Divide

This trips everyone up when switching between systems:

| | Unix/Mac | Windows |
|--|---------|---------|
| **Path separator** | `/` forward slash | `\` backslash |
| **Root** | `/` | `C:\` (drive letter) |
| **Home directory** | `~/` or `/home/username/` | `C:\Users\username\` |
| **Temp directory** | `/tmp/` | `C:\Windows\Temp\` or `%TEMP%` |
| **Config files** | Hidden files starting with `.` (e.g., `.bashrc`) | Registry or `AppData\` |

**In Python** — use `pathlib.Path` and it handles all of this for you:
```python
from pathlib import Path

# Works on ALL platforms — no slash drama
home = Path.home()
config = home / ".config" / "myapp" / "settings.json"
config.parent.mkdir(parents=True, exist_ok=True)
```

---

## Shell Scripting — The Differences

### Bash Script (Linux/Mac) — `script.sh`
```bash
#!/bin/bash

# Variables
NAME="Bill"
echo "Hello, $NAME"

# If statement
if [ "$NAME" == "Bill" ]; then
    echo "Welcome back"
fi

# Loop
for file in *.py; do
    echo "Processing: $file"
done

# Function
greet() {
    echo "Hello, $1"
}
greet "world"

# Exit code check
git pull
if [ $? -ne 0 ]; then
    echo "git pull failed"
    exit 1
fi
```

### PowerShell Script (Windows) — `script.ps1`
```powershell
# Variables
$Name = "Bill"
Write-Host "Hello, $Name"

# If statement
if ($Name -eq "Bill") {
    Write-Host "Welcome back"
}

# Loop
Get-ChildItem *.py | ForEach-Object {
    Write-Host "Processing: $($_.Name)"
}

# Function
function Greet {
    param($Who)
    Write-Host "Hello, $Who"
}
Greet "world"

# Error handling
try {
    git pull
} catch {
    Write-Host "git pull failed: $_"
    exit 1
}
```

### Python — Works Everywhere (the real answer)
```python
import subprocess
import sys
from pathlib import Path

# Run a shell command cross-platform
result = subprocess.run(
    ["python", "--version"],
    capture_output=True, text=True, check=True
)
print(result.stdout)

# Walk files — works on all platforms
for py_file in Path(".").rglob("*.py"):
    print(f"Processing: {py_file}")
```

> **The real-world answer:** For anything more complex than a few lines, write it in Python with `pathlib` + `subprocess`. It runs everywhere, it's readable, and you don't have to remember two different syntaxes.

---

## Keyboard Shortcuts That Work Everywhere

| Action | Shortcut |
|--------|---------|
| **Interrupt / kill current command** | `Ctrl + C` |
| **Clear the screen** | `Ctrl + L` (Mac/Linux) / `cls` (Windows) |
| **Go to beginning of line** | `Ctrl + A` |
| **Go to end of line** | `Ctrl + E` |
| **Delete word backward** | `Ctrl + W` |
| **Search command history** | `Ctrl + R` — type to filter |
| **Previous command** | `↑` arrow |
| **Autocomplete** | `Tab` (works everywhere) |
| **Suspend current process** | `Ctrl + Z` (Mac/Linux) |
| **Exit shell** | `exit` or `Ctrl + D` |

---

## Tab Completion — Use It Constantly

`Tab` autocompletes:
- File and directory names
- Command names
- In Zsh: git branch names, npm scripts, almost anything with plugins
- In PowerShell: cmdlet names, parameter names, values

**Double-Tab** shows all options when there are multiple matches.

If your tab completion isn't working well:
- **Bash:** install `bash-completion` package
- **Zsh:** comes with `zsh-completions`; use `oh-my-zsh` or `zinit` for power-user completions
- **PowerShell:** install `PSReadLine` (usually pre-installed in PS7)

---

## Shell Configuration Files

These run every time you open a terminal:

| Shell | Config file | Location | Use it for |
|-------|------------|----------|-----------|
| **Bash** | `.bashrc` | `~/.bashrc` | Aliases, exports, functions (interactive shells) |
| **Bash** | `.bash_profile` | `~/.bash_profile` | Login shells (SSH, etc.) |
| **Zsh** | `.zshrc` | `~/.zshrc` | Everything — aliases, plugins, theme |
| **PowerShell** | `profile.ps1` | `$PROFILE` (type this to see the path) | Aliases, functions, module imports |

**Useful things to put in `.bashrc` / `.zshrc`:**
```bash
# Aliases — shortcuts for commands you type constantly
alias ll='ls -la'
alias gs='git status'
alias gc='git commit -m'
alias py='python3'

# Add a directory to PATH
export PATH="$HOME/.local/bin:$PATH"

# Set default editor
export EDITOR="code"    # VS Code
# export EDITOR="vim"

# Python virtual environment shortcut
alias venv='python3 -m venv .venv && source .venv/bin/activate'
```

After editing, apply changes with: `source ~/.zshrc` (or `source ~/.bashrc`)

---

## Python Virtual Environments — Cross-Platform

The most common shell task for Python work:

```bash
# Create a virtual environment
python3 -m venv .venv          # Mac/Linux
python -m venv .venv            # Windows

# Activate it
source .venv/bin/activate       # Mac/Linux (bash/zsh)
.venv\Scripts\Activate.ps1      # Windows PowerShell
.venv\Scripts\activate.bat      # Windows CMD

# You'll see (.venv) in your prompt when active

# Install packages
pip install requests numpy

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate
deactivate
```

---

## Common Gotchas When Switching Between Systems

| Gotcha | What happens | Fix |
|--------|-------------|-----|
| **Line endings** | Linux/Mac uses `\n`; Windows uses `\r\n`. Files edited on Windows open weird on Linux. | `git config --global core.autocrlf input` (Mac/Linux) or use `.editorconfig` |
| **Case sensitivity** | Linux filesystem IS case-sensitive (`File.py` ≠ `file.py`). Mac/Windows are NOT by default. | Be consistent with casing in filenames; treat filenames as case-sensitive everywhere |
| **Backslash in scripts** | Bash treats `\` as line continuation. PowerShell uses `` ` `` (backtick). | Use Python for cross-platform scripts |
| **`python` vs `python3`** | On Linux, `python` might be Python 2. On Mac with Homebrew, it's Python 3. On Windows it depends. | Always use `python3` explicitly on Mac/Linux; use `py` launcher on Windows |
| **PATH separator** | Unix uses `:` to separate PATH entries. Windows uses `;`. | Let Python's `pathlib` and `os.environ` handle this |
| **Spaces in paths** | Spaces in filenames/paths break shell scripts. | Quote paths: `cd "My Documents"`. Better: avoid spaces in project directory names. |
| **Permissions** | Unix has file permissions (`chmod`). Windows has ACLs. | Use `chmod +x script.sh` to make scripts executable on Mac/Linux |

---

## Quick Reference: Which Shell Should I Use?

| Situation | Best choice |
|-----------|------------|
| Mac daily development | `zsh` (default) — it's bash with better autocomplete |
| Linux server work | `bash` — it's on every Linux machine guaranteed |
| Windows daily development | **PowerShell 7** + **WSL2** for Linux tools |
| Cross-platform scripting | **Python** — runs everywhere, no syntax switching |
| Quick one-liners on Windows | PowerShell — `dir`, `cp`, `mv` all work as aliases |
| Git operations | Whatever shell you're in — Git works everywhere |
| Docker | Whatever shell — `docker` commands are identical everywhere |

---

## Related Notes

- [08.7 - Shell, Terminal & Cross-Platform CLI](08.7---Shell,-Terminal-&-Cross-Platform-CLI) — Python integration: subprocess, argparse, click, building CLI tools
- [08.8 - Git & Version Control](08.8---Git-&-Version-Control) — Git from the command line
- [09 - Docker & Containers](09---Docker-&-Containers) — Docker CLI commands
- [Terminal Commands Essentials](Terminal-Commands-Essentials) — original quick reference (bash-focused)

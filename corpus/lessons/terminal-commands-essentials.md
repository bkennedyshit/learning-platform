---
title: "Terminal Commands Essentials"
subject: "Dev_Tools"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# Terminal Commands Essentials

## Navigation
```bash
# Current directory
pwd

# List files
ls              # List files
ls -l           # Long format (permissions, size)
ls -la          # Include hidden files
ls -lh          # Human-readable sizes

# Change directory
cd folder       # Go to folder
cd ..           # Go up one level
cd ~            # Go to home directory
cd -            # Go to previous directory
cd /            # Go to root

# Windows (Command Prompt/PowerShell)
dir             # List files
cd folder       # Change directory
cd ..           # Go up
```

## File Operations
```bash
# Create
touch file.txt          # Create empty file
mkdir folder            # Create directory
mkdir -p path/to/folder # Create nested directories

# Copy
cp file.txt backup.txt  # Copy file
cp -r folder backup     # Copy directory recursively

# Move/Rename
mv file.txt newname.txt # Rename
mv file.txt folder/     # Move to folder

# Delete
rm file.txt             # Delete file
rm -r folder            # Delete directory
rm -rf folder           # Force delete (CAREFUL!)

# View files
cat file.txt            # Print entire file
head file.txt           # First 10 lines
tail file.txt           # Last 10 lines
tail -n 20 file.txt     # Last 20 lines
less file.txt           # View with scrolling (q to quit)
```

## Search & Find
```bash
# Find files
find . -name "*.py"           # Find Python files
find . -type f -name "test*"  # Find files starting with "test"
find . -type d -name "src"    # Find directories

# Search in files
grep "search term" file.txt            # Search in file
grep -r "search term" .                # Search recursively
grep -i "search term" file.txt         # Case insensitive
grep -n "search term" file.txt         # Show line numbers
grep -l "search term" *.txt            # Show filenames only
```

## File Content
```bash
# Count
wc file.txt             # Lines, words, characters
wc -l file.txt          # Line count only
wc -w file.txt          # Word count

# Compare
diff file1.txt file2.txt  # Show differences

# Sort
sort file.txt           # Sort lines
sort -r file.txt        # Reverse sort
sort -n file.txt        # Numeric sort

# Unique
uniq file.txt           # Remove duplicate lines
sort file.txt | uniq    # Sort then remove duplicates
```

## Pipes & Redirection
```bash
# Redirect output
command > file.txt      # Write to file (overwrite)
command >> file.txt     # Append to file
command 2> error.log    # Redirect errors

# Pipe (chain commands)
ls -l | grep ".py"      # List files, filter for .py
cat file.txt | grep "error" | wc -l  # Count error lines
history | grep "git"    # Search command history

# Multiple commands
command1 && command2    # Run command2 if command1 succeeds
command1 || command2    # Run command2 if command1 fails
command1 ; command2     # Run both regardless
```

## Process Management
```bash
# View processes
ps                      # Current processes
ps aux                  # All processes
top                     # Live process monitor (q to quit)
htop                    # Better process monitor (if installed)

# Kill process
kill PID                # Terminate process
kill -9 PID             # Force kill
killall process_name    # Kill by name

# Background/Foreground
command &               # Run in background
Ctrl + Z                # Suspend current process
bg                      # Resume in background
fg                      # Bring to foreground
jobs                    # List background jobs
```

## Permissions (Linux/Mac)
```bash
# View permissions
ls -l

# Change permissions
chmod +x script.sh      # Make executable
chmod 755 file.txt      # rwxr-xr-x
chmod 644 file.txt      # rw-r--r--

# Change owner
chown user file.txt
chown user:group file.txt

# Numbers meaning:
# 7 = rwx (read, write, execute)
# 6 = rw-
# 5 = r-x
# 4 = r--
```

## Compression
```bash
# Tar (tape archive)
tar -czf archive.tar.gz folder/   # Create compressed archive
tar -xzf archive.tar.gz           # Extract archive
tar -tzf archive.tar.gz           # List contents

# Zip
zip -r archive.zip folder/        # Create zip
unzip archive.zip                 # Extract zip
unzip -l archive.zip              # List contents
```

## Network
```bash
# Download
curl https://example.com          # Get content
curl -O https://example.com/file  # Download file
wget https://example.com/file     # Download file

# Test connection
ping google.com                   # Test connectivity
ping -c 4 google.com              # Ping 4 times

# Check ports
netstat -tuln                     # List listening ports
lsof -i :8000                     # What's using port 8000
```

## System Info
```bash
# Disk usage
df -h               # Disk space (human-readable)
du -h folder        # Directory size
du -sh folder       # Summary only

# Memory
free -h             # RAM usage (Linux)
top                 # CPU/memory live

# System
uname -a            # System information
whoami              # Current user
date                # Current date/time
uptime              # System uptime
```

## Environment Variables
```bash
# View
echo $HOME          # Print variable
echo $PATH          # View PATH
env                 # All environment variables
printenv            # Same as env

# Set (temporary)
export VAR=value    # Set variable
export PATH=$PATH:/new/path  # Add to PATH

# Set (permanent)
# Add to ~/.bashrc or ~/.zshrc
echo 'export VAR=value' >> ~/.bashrc
source ~/.bashrc    # Reload
```

## Python Specific
```bash
# Run Python
python script.py
python3 script.py
python -m module_name

# Pip
pip install package
pip install -r requirements.txt
pip freeze > requirements.txt
pip list
pip show package

# Virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
deactivate                  # Exit venv

# Run Python module
python -m http.server 8000  # Simple web server
python -m json.tool file.json  # Format JSON
```

## Git (Quick Reference)
```bash
git status
git add .
git commit -m "message"
git push
git pull
git clone url
git branch
git checkout branch-name
git log --oneline
```

## Shortcuts & Tricks
```bash
# Command history
history             # Show history
!123                # Run command #123 from history
!!                  # Run last command
!$                  # Last argument of previous command

# Clear screen
clear               # or Ctrl + L

# Auto-complete
Tab                 # Auto-complete file/command

# Cancel command
Ctrl + C            # Stop current command
Ctrl + D            # Exit (logout)
Ctrl + Z            # Suspend process

# Search history
Ctrl + R            # Reverse search
# Type to search, Enter to run, Ctrl+R again for next match
```

## Common Workflows

### Python Project Setup
```bash
# Create project
mkdir myproject
cd myproject

# Virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install requests flask

# Save dependencies
pip freeze > requirements.txt

# Git init
git init
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "Initial commit"
```

### Quick File Operations
```bash
# Find and count Python files
find . -name "*.py" | wc -l

# Search for TODO in all Python files
grep -rn "TODO" --include="*.py"

# Count lines of code
find . -name "*.py" -exec wc -l {} + | tail -1

# Remove all .pyc files
find . -name "*.pyc" -delete
```

## PowerShell (Windows)
```powershell
# Navigation (same as bash)
cd, pwd, ls

# File operations
New-Item file.txt       # Create file
Copy-Item file.txt backup.txt
Move-Item file.txt newname.txt
Remove-Item file.txt

# List
Get-ChildItem           # Like ls
Get-ChildItem -Recurse  # Recursive

# Search
Get-ChildItem -Recurse -Filter "*.py"
Select-String "search" -Path file.txt  # Like grep

# Process
Get-Process
Stop-Process -Name processname
```

## Quick Tips for Coding Tests
- Use Tab for auto-complete
- Use `Ctrl + R` to search command history
- `cd -` to go back to previous directory
- `ls -lah` to see everything including hidden files
- Use `grep` to search file contents quickly
- `find . -name "filename"` to locate files
- Pipe commands together with `|`
- Virtual environments for Python projects

---

## Related Notes
- [Git Essentials for Coding Tests](Git-Essentials-for-Coding-Tests)
- [VS Code Shortcuts & Productivity](VS-Code-Shortcuts-&-Productivity)
- [Python Development Setup](Python-Development-Setup)
- [Linux Commands Deep Dive](Linux-Commands-Deep-Dive)
- [PowerShell Essentials](PowerShell-Essentials)

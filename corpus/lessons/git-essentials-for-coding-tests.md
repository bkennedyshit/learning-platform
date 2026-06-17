---
title: "Git Essentials for Coding Tests"
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

# Git Essentials for Coding Tests

## Basic Commands
```bash
# Initialize repo
git init

# Clone repository
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git custom-folder-name

# Check status
git status

# View changes
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff branch1 branch2    # Between branches
```

## Staging and Committing
```bash
# Stage files
git add file.txt           # Single file
git add .                  # All changes
git add *.py               # Pattern
git add -p                 # Interactive staging

# Unstage files
git restore --staged file.txt
git reset HEAD file.txt    # Older Git

# Commit
git commit -m "Message here"
git commit -am "Message"   # Add and commit tracked files

# Amend last commit
git commit --amend -m "New message"
git commit --amend --no-edit   # Keep message, add changes
```

## Viewing History
```bash
# View commit history
git log
git log --oneline          # Compact view
git log --graph --oneline  # Visual graph
git log -n 5               # Last 5 commits
git log --author="Billy"   # By author

# View specific file history
git log file.txt
git log -p file.txt        # With changes

# Show commit details
git show commit-hash
git show HEAD              # Latest commit
```

## Branching
```bash
# List branches
git branch                 # Local branches
git branch -a              # All branches (including remote)
git branch -r              # Remote branches

# Create branch
git branch feature-name
git checkout -b feature-name   # Create and switch
git switch -c feature-name     # Newer Git

# Switch branches
git checkout branch-name
git switch branch-name     # Newer Git

# Delete branch
git branch -d branch-name  # Safe delete
git branch -D branch-name  # Force delete

# Rename branch
git branch -m old-name new-name
```

## Remote Repositories
```bash
# View remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git

# Fetch from remote
git fetch origin           # Get changes, don't merge
git fetch --all            # All remotes

# Pull (fetch + merge)
git pull origin main
git pull                   # Current branch

# Push
git push origin branch-name
git push -u origin branch-name  # Set upstream
git push --force           # CAREFUL! Overwrites remote
```

## Merging
```bash
# Merge branch into current
git merge feature-branch

# Abort merge if conflicts
git merge --abort

# Continue after resolving conflicts
# 1. Fix conflicts in files
# 2. Stage resolved files
git add .
# 3. Commit
git commit
```

## Stashing (Save work temporarily)
```bash
# Stash changes
git stash
git stash save "Work in progress"

# List stashes
git stash list

# Apply stash
git stash apply            # Keep stash
git stash pop              # Apply and remove stash
git stash apply stash@{2}  # Specific stash

# Delete stash
git stash drop
git stash clear            # Delete all
```

## Undoing Changes
```bash
# Discard changes in file
git restore file.txt
git checkout -- file.txt   # Older Git

# Undo commit (keep changes)
git reset --soft HEAD~1

# Undo commit (discard changes)
git reset --hard HEAD~1    # CAREFUL!

# Revert commit (create new commit)
git revert commit-hash     # Safer for shared branches
```

## Common Workflows

### Feature Branch Workflow
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push to remote
git push -u origin feature/new-feature

# 4. Create pull request on GitHub/GitLab
# 5. Merge PR
# 6. Delete branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Sync with Main
```bash
# Update your branch with latest main
git checkout main
git pull origin main
git checkout feature-branch
git merge main

# Or use rebase (cleaner history)
git checkout feature-branch
git rebase main
```

### Fix Conflicts
```bash
# When merge has conflicts:
# 1. Git shows conflict markers in files:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> branch-name

# 2. Edit files to resolve
# 3. Stage resolved files
git add .

# 4. Continue merge
git merge --continue
# or
git rebase --continue
```

## Useful Aliases
```bash
# Add to ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    cm = commit -m
    last = log -1 HEAD
    unstage = restore --staged
```

## .gitignore
```bash
# Create .gitignore file

# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# Node
node_modules/
.npm

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Project specific
config/secrets.json
*.log
```

## Quick Tips for Tests
- `git status` before any command
- Commit early, commit often
- Write clear commit messages
- Use feature branches, not main
- Pull before pushing
- Never `--force` push on shared branches
- Stash before switching branches
- Use `.gitignore` for secrets/temp files

## Common Interview Questions
```bash
# How to undo last commit?
git reset --soft HEAD~1

# How to see what changed?
git diff

# How to see commit history?
git log --oneline

# How to create and switch to branch?
git checkout -b branch-name

# How to resolve merge conflicts?
# Edit files, git add, git commit

# What's the difference between merge and rebase?
# Merge: keeps all history, creates merge commit
# Rebase: rewrites history, linear timeline

# How to save work without committing?
git stash
```

## Emergency Commands
```bash
# Oops, committed to wrong branch!
git reset --soft HEAD~1  # Undo commit
git stash               # Save changes
git checkout correct-branch
git stash pop           # Apply changes

# Oops, need to change commit message!
git commit --amend -m "New message"

# Oops, want to add to last commit!
git add forgotten-file.txt
git commit --amend --no-edit

# Lost changes? Check reflog
git reflog              # Shows all HEAD movements
git checkout commit-hash  # Recover lost work
```

---

## Related Notes
- [Terminal Commands Essentials](Terminal-Commands-Essentials)
- [GitHub Workflow](GitHub-Workflow)
- [Code Review Best Practices](Code-Review-Best-Practices)
- [Version Control Concepts](Version-Control-Concepts)
- [Merge vs Rebase](Merge-vs-Rebase)

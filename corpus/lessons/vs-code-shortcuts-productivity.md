---
title: "VS Code Shortcuts & Productivity"
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

# VS Code Shortcuts & Productivity

## Most Important Shortcuts (Learn These First!)

### Windows/Linux | Mac
```
Ctrl + P       | Cmd + P       # Quick file open
Ctrl + Shift + P | Cmd + Shift + P # Command palette
Ctrl + /       | Cmd + /       # Comment/uncomment line
Ctrl + D       | Cmd + D       # Select next occurrence
Ctrl + F       | Cmd + F       # Find
Ctrl + H       | Cmd + H       # Find and replace
Ctrl + Space   | Cmd + Space   # Trigger IntelliSense
Ctrl + `       | Cmd + `       # Toggle terminal
```

## Navigation
```
Ctrl + P             # Quick open file
Ctrl + Tab           # Switch between recent files
Ctrl + B             # Toggle sidebar
Ctrl + J             # Toggle panel (terminal, problems)
Ctrl + \             # Split editor

Alt + Left/Right     # Navigate back/forward
Ctrl + G             # Go to line
Ctrl + Shift + O     # Go to symbol in file
Ctrl + T             # Go to symbol in workspace

F12                  # Go to definition
Alt + F12            # Peek definition
Shift + F12          # Find all references
```

## Editing
```
Alt + Up/Down        # Move line up/down
Shift + Alt + Up/Down # Copy line up/down
Ctrl + Shift + K     # Delete line
Ctrl + Enter         # Insert line below
Ctrl + Shift + Enter # Insert line above

Ctrl + ]             # Indent line
Ctrl + [             # Outdent line

Ctrl + /             # Toggle line comment
Shift + Alt + A      # Toggle block comment

Ctrl + D             # Select next occurrence
Ctrl + K, Ctrl + D   # Move to next occurrence (skip current)
Alt + Click          # Add cursor
Ctrl + Alt + Up/Down # Add cursor above/below
```

## Multi-Cursor Editing (POWERFUL!)
```
Alt + Click          # Add cursor at position
Ctrl + Alt + Down    # Add cursor below
Ctrl + Alt + Up      # Add cursor above
Ctrl + D             # Select next occurrence (repeat for more)
Ctrl + Shift + L     # Select all occurrences
Shift + Alt + I      # Add cursors to line ends

# Example: Rename multiple variables at once
1. Ctrl + F, type variable name
2. Ctrl + Shift + L (select all)
3. Type new name
```

## Search & Replace
```
Ctrl + F             # Find
Ctrl + H             # Replace
Ctrl + Shift + F     # Find in files
Ctrl + Shift + H     # Replace in files

F3                   # Find next
Shift + F3           # Find previous

Alt + C              # Toggle case sensitive
Alt + W              # Toggle whole word
Alt + R              # Toggle regex
```

## Terminal
```
Ctrl + `             # Toggle terminal
Ctrl + Shift + `     # New terminal
Ctrl + Shift + 5     # Split terminal
Ctrl + PageUp/Down   # Switch between terminals
```

## Debugging
```
F5                   # Start debugging
F9                   # Toggle breakpoint
F10                  # Step over
F11                  # Step into
Shift + F11          # Step out
Shift + F5           # Stop debugging
```

## Code Formatting
```
Shift + Alt + F      # Format document
Ctrl + K, Ctrl + F   # Format selection

# Auto-format on save (settings.json)
"editor.formatOnSave": true
```

## IntelliSense & Snippets
```
Ctrl + Space         # Trigger IntelliSense
Ctrl + Shift + Space # Trigger parameter hints
Tab                  # Accept IntelliSense suggestion

# Python snippets (type and press Tab)
for     # for loop
if      # if statement
def     # function definition
class   # class definition
try     # try/except
```

## Panel & Layout
```
Ctrl + B             # Toggle sidebar
Ctrl + J             # Toggle panel
Ctrl + K, Z          # Zen mode (focus)
Ctrl + \             # Split editor
Ctrl + W             # Close editor
Ctrl + K, W          # Close all editors
Ctrl + K, F          # Close folder
```

## Quick Fixes & Refactoring
```
Ctrl + .             # Quick fix / show code actions
F2                   # Rename symbol
Ctrl + Shift + R     # Refactor
```

## Productivity Tips

### Extensions to Install
```
- Python (Microsoft)
- Pylance
- GitLens
- Prettier
- ESLint
- Live Server
- Better Comments
- Path Intellisense
```

### Settings to Enable
```json
// settings.json (Ctrl + ,)
{
  "editor.formatOnSave": true,
  "editor.minimap.enabled": false,
  "editor.linkedEditing": true,
  "editor.suggest.snippetsPreventQuickSuggestions": false,
  "files.autoSave": "afterDelay",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### Useful Command Palette Commands
```
> Python: Select Interpreter
> Format Document
> Organize Imports
> Rename Symbol
> Extract Method
> Sort Lines Ascending
> Transform to Uppercase/Lowercase
> Toggle Word Wrap
```

## Coding Test Workflow
```
1. Open folder: Ctrl + K, Ctrl + O
2. Create file: Ctrl + N
3. Set language: Ctrl + K, M (then type "python")
4. Write code with IntelliSense: Ctrl + Space
5. Format: Shift + Alt + F
6. Run in terminal: Ctrl + `, then python file.py
7. Debug: F5
```

## Python-Specific
```
# Run Python file
Ctrl + `            # Open terminal
python file.py      # Type manually
# Or configure task (Ctrl + Shift + P > "Tasks: Run Task")

# Debugging Python
1. Set breakpoint: F9
2. Start debugging: F5
3. Step through: F10 (over), F11 (into)
4. Inspect variables in debug panel

# Jupyter Notebooks in VS Code
Install Jupyter extension
Ctrl + Shift + P > "Create New Jupyter Notebook"
Run cell: Shift + Enter
```

## Snippets for Coding Tests
```python
# Create custom snippet
# Ctrl + Shift + P > "Preferences: Configure User Snippets"

{
  "Main function": {
    "prefix": "main",
    "body": [
      "def main():",
      "    $1",
      "",
      "if __name__ == '__main__':",
      "    main()"
    ]
  },
  "Test function": {
    "prefix": "test",
    "body": [
      "def test_$1():",
      "    assert $2 == $3"
    ]
  }
}
```

## Quick Tips for Coding Tests
- Learn `Ctrl + P` (file open) and `Ctrl + Shift + P` (command palette)
- Use `Ctrl + D` for multi-cursor editing
- Format code before submitting: `Shift + Alt + F`
- Use IntelliSense (`Ctrl + Space`) to avoid typos
- Terminal shortcut: `Ctrl + \`` saves time
- Split view (`Ctrl + \\`) for reference code
- Zen mode (`Ctrl + K, Z`) for focus

## Emergency Shortcuts
```
Ctrl + Z             # Undo
Ctrl + Shift + Z     # Redo
Ctrl + K, Ctrl + U   # Undo close editor
Ctrl + Shift + P     # Command palette (when you forget shortcuts)
```

---

## Related Notes
- [Terminal Commands Essentials](Terminal-Commands-Essentials)
- [Git Essentials for Coding Tests](Git-Essentials-for-Coding-Tests)
- [Python Development Setup](Python-Development-Setup)
- [Debugging Strategies](Debugging-Strategies)
- [Code Formatting Best Practices](Code-Formatting-Best-Practices)

from pathlib import Path

p = Path(r"C:\Obsidian Vault\Bill's Vault\05-Knowledge_Foundation\09 - Learning\07 - Math and Physics\02 - Linear Algebra & Matrix Theory\_practice\scripts\2.6_eigenvalues.py")
t = p.read_text(encoding="utf-8")
idx = t.find("def main")
out = t[idx:] if idx >= 0 else "NOT FOUND"
# Avoid charmap encoding errors
out_safe = out.encode("ascii", "replace").decode("ascii")
print(out_safe)

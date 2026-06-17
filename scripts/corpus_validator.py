import os
import re
import argparse
from pathlib import Path

# Regular expressions for markdown links and SVGs
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+\.svg)\)')

def validate_corpus(corpus_dir):
    corpus_path = Path(corpus_dir)
    if not corpus_path.exists() or not corpus_path.is_dir():
        print(f"Error: Directory '{corpus_dir}' does not exist.")
        return

    md_files = list(corpus_path.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files in {corpus_dir}")
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Validating {md_file.relative_to(corpus_path)}...")
        
        # 1. Validate cross-links
        links = LINK_RE.findall(content)
        for text, link in links:
            # Ignore external links and fragments for simplicity
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                continue
            
            target_path = (md_file.parent / link).resolve()
            if not target_path.exists():
                print(f"  [Warning] Broken cross-link: '{link}' not found.")
                
        # 2. Check SVG references
        images = IMAGE_RE.findall(content)
        for alt, src in images:
            if src.startswith('http'):
                continue
            
            svg_path = (md_file.parent / src).resolve()
            if not svg_path.exists():
                print(f"  [Warning] Missing SVG: '{src}' not found.")
                
        # 3. Flag subjects lacking practice problems
        # Look for "Practice Problems", "Exercises", etc. in content
        if not re.search(r'(?i)#+\s*(Practice Problems|Exercises)', content):
            print(f"  [Notice] No practice problems section found.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Corpus Validator')
    parser.add_argument('--dir', default='lessons', help='Directory to scan (default: lessons)')
    args = parser.parse_args()
    
    validate_corpus(args.dir)

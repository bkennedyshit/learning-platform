import os
import re
import yaml

def slugify(text):
    """
    Convert text to a slugified version for filenames.
    e.g., '14.1 The Language of Algebra' -> '141-the-language-of-algebra'
    """
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def process_file(filepath, output_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = {}
    body = content
    
    # Extract YAML frontmatter
    match = re.match(r'^\s*---\r?\n(.*?)\r?\n---\r?\n(.*)', content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2)
        except yaml.YAMLError as e:
            print(f"Warning: Could not parse frontmatter for {filepath}: {e}")
            pass

    if not isinstance(frontmatter, dict):
        frontmatter = {}

    # 1. Inject subject
    parent_folder = os.path.basename(os.path.dirname(filepath))
    subject = re.sub(r'^\d+\s*-\s*', '', parent_folder)
    frontmatter['subject'] = subject

    # 2. Inject catalog
    path_str = str(filepath)
    if "10 - Learning App Material" in path_str:
        frontmatter['catalog'] = "k12"
    elif "09 - Learning" in path_str:
        frontmatter['catalog'] = "advanced"

    # 3. Convert image embeds: ![[image.svg|size]] -> ![image](image.svg)
    def repl_image(m):
        inner = m.group(1)
        filename = inner.split('|')[0]
        basename = os.path.basename(filename)
        name_without_ext = os.path.splitext(basename)[0]
        return f"![{name_without_ext}]({basename})"
    body = re.sub(r'!\[\[(.*?)\]\]', repl_image, body)

    # 4. Convert WikiLinks: [[Folder/Page Name|Alias]] -> [Alias](Page-Name)
    def repl_wikilink(m):
        inner = m.group(1)
        if '|' in inner:
            target, alias = inner.split('|', 1)
        else:
            target = inner
            alias = None
        target_basename = os.path.basename(target)
        text = alias if alias else target_basename
        link = target_basename.replace(' ', '-')
        return f"[{text}]({link})"
    
    # Negative lookbehind to avoid matching ![[...]]
    body = re.sub(r'(?<!!)\[\[(.*?)\]\]', repl_wikilink, body)

    # 5. Output filename
    title = frontmatter.get('title')
    if not title:
        title = os.path.splitext(os.path.basename(filepath))[0]
    
    out_filename = f"{slugify(title)}.md"
    out_filepath = os.path.join(output_dir, out_filename)

    # 6. Reconstruct content
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True)
    new_content = f"---\n{yaml_str}---\n{body}"

    with open(out_filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    base_dir_09 = r"C:\Users\billk\projects\learning-platform\corpus\09 - Learning"
    base_dir_10 = r"C:\Users\billk\projects\learning-platform\corpus\10 - Learning App Material"
    output_dir = r"C:\Users\billk\projects\learning-platform\corpus\lessons"

    os.makedirs(output_dir, exist_ok=True)

    for base_dir in [base_dir_09, base_dir_10]:
        if not os.path.exists(base_dir):
            print(f"Directory not found: {base_dir}")
            continue
        
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    try:
                        process_file(filepath, output_dir)
                        print(f"Processed: {filepath}")
                    except Exception as e:
                        print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    main()

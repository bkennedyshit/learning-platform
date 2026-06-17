import argparse
import requests
import re
import yaml
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else 'Untitled'
    title = title.strip()
    
    # Finding main content area
    main_content = soup.find('article') or soup.find('main') or soup.body
    
    # Clean up scripts and styles
    for script_or_style in main_content(['script', 'style', 'nav', 'footer', 'header']):
        script_or_style.decompose()
        
    # Extract text and format as markdown (simplified)
    paragraphs = main_content.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li'])
    md_content = []
    
    for p in paragraphs:
        if p.name == 'h1':
            md_content.append(f"# {p.get_text().strip()}")
        elif p.name == 'h2':
            md_content.append(f"## {p.get_text().strip()}")
        elif p.name == 'h3':
            md_content.append(f"### {p.get_text().strip()}")
        elif p.name == 'p':
            md_content.append(f"{p.get_text().strip()}")
        elif p.name == 'li':
            # Simple list item support
            md_content.append(f"- {p.get_text().strip()}")
            
    return title, "\n\n".join(md_content)

def save_to_markdown(url, title, content, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate frontmatter
    frontmatter = {
        'title': title,
        'source_url': url,
        'type': 'educational_content',
        'has_practice_problems': False
    }
    
    # Create filename
    domain = urlparse(url).netloc
    safe_title = re.sub(r'[^a-z0-9]', '_', title.lower())
    filename = f"{domain}_{safe_title[:30]}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, default_flow_style=False)
        f.write("---\n\n")
        f.write(content)
        
    print(f"Saved educational content to {filepath}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Learning Scraper')
    parser.add_argument('url', help='URL of the educational content to scrape')
    parser.add_argument('--out', default='lessons', help='Output directory (default: lessons)')
    args = parser.parse_args()
    
    print(f"Scraping {args.url}...")
    result = scrape_article(args.url)
    if result:
        title, content = result
        save_to_markdown(args.url, title, content, args.out)

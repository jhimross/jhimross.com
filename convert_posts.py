import xml.etree.ElementTree as ET
import os
import re
import html2text
import json

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def convert():
    file_path = 'jhimross.wordpress.com.2026-05-10.000.xml'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    tree = ET.parse(file_path)
    root = tree.getroot()
    channel = root.find('channel')
    
    # Namespaces
    ns = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wp': 'http://wordpress.org/export/1.2/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
    }
    
    if not os.path.exists('posts'):
        os.makedirs('posts')
        
    h = html2text.HTML2Text()
    h.body_width = 0 # No wrapping
    h.ignore_images = False
    h.ignore_links = False
    
    # Sort posts by date descending
    all_posts = []
    
    post_count = 0
    for item in channel.findall('item'):
        post_type_el = item.find('wp:post_type', ns)
        if post_type_el is None or post_type_el.text != 'post':
            continue
            
        status_el = item.find('wp:status', ns)
        if status_el is None or status_el.text != 'publish':
            continue
            
        title = item.find('title').text or 'Untitled'
        date_el = item.find('wp:post_date', ns)
        date_full = date_el.text if date_el is not None else '2024-01-01 00:00:00'
        date_short = date_full.split(' ')[0]
        
        slug_el = item.find('wp:post_name', ns)
        slug = slug_el.text if slug_el is not None and slug_el.text else slugify(title)
        
        content_el = item.find('content:encoded', ns)
        content = content_el.text or ''
        
        # Categories and Tags
        categories = []
        tags = []
        for cat in item.findall('category'):
            domain = cat.get('domain')
            name = cat.text
            if domain == 'category':
                categories.append(name)
            elif domain == 'post_tag':
                tags.append(name)
        
        # Convert HTML to Markdown
        md_content = h.handle(content)
        
        # Clean up WP block comments
        md_content = re.sub(r'<!-- wp:.*? -->', '', md_content)
        md_content = re.sub(r'<!-- /wp:.*? -->', '', md_content)
        
        # Frontmatter
        frontmatter = [
            "---",
            f"title: \"{title}\"",
            f"date: {date_full}",
            f"slug: {slug}"
        ]
        if categories:
            frontmatter.append(f"categories: {categories}")
        if tags:
            frontmatter.append(f"tags: {tags}")
        frontmatter.append("---\n")
        
        # Ensure unique filename
        filename = f'posts/{slug}.md'
        with open(filename, 'w') as f:
            f.write("\n".join(frontmatter) + "\n" + md_content)
            
        all_posts.append({
            "title": title,
            "date": date_short,
            "slug": slug,
            "file": f"{slug}.md"
        })
        post_count += 1
    
    # Sort posts by date descending
    all_posts.sort(key=lambda x: x['date'], reverse=True)
    
    with open('posts/posts.json', 'w') as f:
        json.dump(all_posts, f, indent=2)
        
    print(f"Successfully converted {post_count} posts to 'posts/' directory and updated 'posts/posts.json'.")

if __name__ == '__main__':
    convert()

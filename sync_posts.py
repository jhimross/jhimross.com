def embed_youtube(content):
    """Replace YouTube URLs in markdown with responsive iframe embed HTML.
    Supports full YouTube URLs and short youtu.be links.
    """
    import re
    # Pattern matches full and short YouTube URLs, captures video ID
    pattern = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})")
    def repl(match):
        video_id = match.group(1)
        embed_html = f'''<div class="yt-embed"><iframe src="https://www.youtube.com/embed/{video_id}"\
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'''
        return embed_html
    return pattern.sub(repl, content)

import os
import json
import re
import ast

def extract_first_image(content):
    # Match markdown image syntax: ![alt](url)
    match = re.search(r'!\[.*?\]\((.*?)\)', content)
    if match:
        return match.group(1)
    return "https://jhimross.com/assets/about.jpg"

def extract_description(content):
    # Remove images and frontmatter
    content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    content = re.sub(r'!\[.*?\]\((.*?)\)', '', content)
    content = re.sub(r'#.*?\n', '', content)
    # Get first 160 chars of text
    text = content.strip()
    text = re.sub(r'\s+', ' ', text)
    return text[:160] + "..." if len(text) > 160 else text

def sync_posts():
    posts_dir = 'posts'
    posts_json_path = os.path.join(posts_dir, 'posts.json')
    
    # Read the template
    with open('post.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    all_posts = []
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                
                # Extract frontmatter
                fm_match = re.search(r'---\s*\n(.*?)\n---', raw_content, re.DOTALL)
                if fm_match:
                    fm_text = fm_match.group(1)
                    lines = fm_text.split('\n')
                    title, date, slug = "", "", ""
                    categories = []
                    
                    for line in lines:
                        if line.startswith('title:'):
                            title = line.replace('title:', '').strip()
                            if title.startswith('"') and title.endswith('"'):
                                title = title[1:-1].replace('\\"', '"')
                        elif line.startswith('date:'):
                            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                            if date_match: date = date_match.group(1)
                        elif line.startswith('slug:'):
                            slug = line.replace('slug:', '').strip()
                        elif line.startswith('categories:'):
                            cat_text = line.replace('categories:', '').strip()
                            try:
                                categories = ast.literal_eval(cat_text)
                            except:
                                categories = [c.strip() for c in cat_text.split(',')]
                    
                    if title and date and slug:
                        all_posts.append({
                            "title": title,
                            "date": date,
                            "slug": slug,
                            "categories": categories,
                            "file": filename
                        })
                        
                        # Generate static HTML for this post
                        image = extract_first_image(raw_content)
                        description = extract_description(raw_content)
                        
                        post_html = template
                        
                        # Inject Meta Tags
                        meta_tags = f"""
  <title>{title} — Jhimross Olinares</title>
  <meta name="description" content="{description}" />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://jhimross.com/{slug}.html" />
  <meta property="og:title" content="{title} — Jhimross Olinares" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{image}" />

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://jhimross.com/{slug}.html" />
  <meta property="twitter:title" content="{title} — Jhimross Olinares" />
  <meta property="twitter:description" content="{description}" />
  <meta property="twitter:image" content="{image}" />
"""
                        # Replace generic title and meta
                        post_html = re.sub(r'<title>.*?</title>', meta_tags, post_html, flags=re.DOTALL)
                        
                        # Modify the JS to load this specific slug automatically
                        post_html = post_html.replace('const slug = params.get(\'s\');', f'const slug = "{slug}";')
                        
                        # Ensure the CSS/JS paths are correct (they are relative now, which is fine if files are at root)
                        
                        with open(f"{slug}.html", 'w', encoding='utf-8') as f_out:
                            f_out.write(post_html)
    
    # Sort posts by date descending
    all_posts.sort(key=lambda x: (x['date'], x['slug']), reverse=True)
    
    with open(posts_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2)
        
    print(f"Successfully synced {len(all_posts)} posts and generated static HTML files.")

if __name__ == '__main__':
    sync_posts()

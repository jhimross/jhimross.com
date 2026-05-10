import os
import json
import re
import ast

def sync_posts():
    posts_dir = 'posts'
    posts_json_path = os.path.join(posts_dir, 'posts.json')
    
    all_posts = []
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract frontmatter
                fm_match = re.search(r'---\s*\n(.*?)\n---', content, re.DOTALL)
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
    
    # Sort posts by date descending
    all_posts.sort(key=lambda x: (x['date'], x['slug']), reverse=True)
    
    with open(posts_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2)
        
    print(f"Successfully synced {len(all_posts)} posts to {posts_json_path}")

if __name__ == '__main__':
    sync_posts()

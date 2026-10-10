def embed_youtube(content):
    """Replace YouTube URLs in markdown with responsive iframe embed HTML.
    Supports full YouTube URLs and short youtu.be links.
    """
    import re
    pattern = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})")
    def repl(match):
        video_id = match.group(1)
        embed_html = f'''<div class="yt-embed"><iframe src="https://www.youtube.com/embed/{video_id}"\
            title="YouTube video player" frameborder="0" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'''
        return embed_html
    return pattern.sub(repl, content)

import os
import json
import re
import ast
import html
import datetime
import markdown as md

def parse_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%B %d, %Y'):
        try:
            return datetime.datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def extract_first_image(content):
    match = re.search(r'!\[.*?\]\((.*?)\)', content)
    if match:
        return match.group(1)
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if match:
        return match.group(1)
    return "https://jhimross.com/assets/about.jpg"

def extract_description(content):
    content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    content = re.sub(r'!\[.*?\]\((.*?)\)', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'#.*?\n', '', content)
    text = content.strip()
    text = re.sub(r'\s+', ' ', text)
    preview = text[:160] + "..." if len(text) > 160 else text
    return html.escape(preview, quote=True)

def render_content(raw_content):
    fm_match = re.search(r'---\s*\n(.*?)\n---', raw_content, re.DOTALL)
    body = raw_content[fm_match.end():] if fm_match else raw_content
    body = re.sub(r'<!--\s*wp:.*?-->', '', body)
    content = md.markdown(body, extensions=['tables', 'fenced_code', 'sane_lists', 'attr_list', 'md_in_html'])
    content = embed_youtube(content)
    content = re.sub(r'(<img\b)', r'\1 loading="lazy" decoding="async"', content, flags=re.IGNORECASE)
    content = re.sub(r'(<iframe\b)', r'\1 loading="lazy"', content, flags=re.IGNORECASE)
    return content

def render_home_posts(all_posts):
    parts = []
    for p in all_posts:
        title = html.escape(p["title"], quote=True)
        cats = p.get("categories") or []
        cat_block = ""
        if cats:
            tags = "".join(f'<span class="category-tag">{html.escape(c, quote=True)}</span>' for c in cats)
            cat_block = f'\n                  <div class="post-categories">{tags}</div>'
        parts.append(
            f'<article class="post-card">\n'
            f'                  <span class="post-date">{p["date"]}</span>{cat_block}\n'
            f'                  <a href="{p["slug"]}.html"><h2>{title}</h2></a>\n'
            f'                  <a href="{p["slug"]}.html" class="read-more">Read →</a>\n'
            f'                </article>'
        )
    return "\n        ".join(parts)

def sync_posts():
    posts_dir = 'posts'
    posts_json_path = os.path.join(posts_dir, 'posts.json')

    with open('post.html', 'r', encoding='utf-8') as f:
        template = f.read()

    all_posts = []

    for filename in sorted(os.listdir(posts_dir)):
        if not filename.endswith('.md'):
            continue
        file_path = os.path.join(posts_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        fm_match = re.search(r'---\s*\n(.*?)\n---', raw_content, re.DOTALL)
        if not fm_match:
            continue
        fm_text = fm_match.group(1)
        lines = fm_text.split('\n')
        title, slug = "", ""
        date_obj = None
        categories = []

        for line in lines:
            if line.startswith('title:'):
                title = line.replace('title:', '').strip()
                if title.startswith('"') and title.endswith('"'):
                    title = title[1:-1].replace('\\"', '"')
            elif line.startswith('date:'):
                date_obj = parse_date(line.replace('date:', '').strip())
            elif line.startswith('slug:'):
                slug = line.replace('slug:', '').strip()
            elif line.startswith('categories:'):
                cat_text = line.replace('categories:', '').strip()
                try:
                    categories = ast.literal_eval(cat_text)
                except Exception:
                    categories = [c.strip() for c in cat_text.split(',')]

        if not (title and date_obj and slug):
            continue

        all_posts.append({
            "title": title,
            "date": date_obj.strftime('%B %d, %Y'),
            "slug": slug,
            "categories": categories,
            "file": filename
        })

    all_posts.sort(key=lambda x: (datetime.datetime.strptime(x['date'], '%B %d, %Y'), x['slug']), reverse=True)

    index_map = {p['slug']: i for i, p in enumerate(all_posts)}

    for p in all_posts:
        filename = p['file']
        with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
            raw_content = f.read()

        title = p['title']
        date = p['date']
        slug = p['slug']
        categories = p['categories']

        image = extract_first_image(raw_content)
        description = extract_description(raw_content)
        content_html = render_content(raw_content)
        title_esc = html.escape(title, quote=True)

        post_html = template

        meta_tags = f"""
  <title>{title_esc} — Jhimross Olinares</title>
  <meta name="description" content="{description}" />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://jhimross.com/{slug}.html" />
  <meta property="og:title" content="{title_esc} — Jhimross Olinares" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{image}" />

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://jhimross.com/{slug}.html" />
  <meta property="twitter:title" content="{title_esc} — Jhimross Olinares" />
  <meta property="twitter:description" content="{description}" />
  <meta property="twitter:image" content="{image}" />
"""
        post_html = re.sub(r'<title>.*?</title>', meta_tags, post_html, flags=re.DOTALL)

        cat_spans = ""
        if categories:
            cat_spans = "".join(f'<span class="category-tag">{html.escape(c, quote=True)}</span>' for c in categories)
        meta_line = f'Published on {date}'

        post_html = post_html.replace('%%TITLE%%', title_esc)
        post_html = post_html.replace('%%CATEGORIES%%', cat_spans)
        post_html = post_html.replace('%%META%%', meta_line)
        post_html = post_html.replace('%%CONTENT%%', content_html)

        idx = index_map[slug]
        prev_post = all_posts[idx + 1] if idx < len(all_posts) - 1 else None
        next_post = all_posts[idx - 1] if idx > 0 else None

        nav = ""
        if prev_post:
            nav += f'      <a href="{prev_post["slug"]}.html" class="nav-prev">\n        <span class="nav-label">← Previous</span>\n        <span class="nav-title">{html.escape(prev_post["title"], quote=True)}</span>\n      </a>\n'
        if next_post:
            nav += f'      <a href="{next_post["slug"]}.html" class="nav-next">\n        <span class="nav-label">Next →</span>\n        <span class="nav-title">{html.escape(next_post["title"], quote=True)}</span>\n      </a>'
        post_html = post_html.replace('%%PREV_NEXT%%', nav.rstrip())

        with open(f"{slug}.html", 'w', encoding='utf-8') as f_out:
            f_out.write(post_html)

    with open(posts_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2)
        f.write('\n')

    if os.path.exists('index.html'):
        cards = render_home_posts(all_posts)
        home = open('index.html', encoding='utf-8').read()
        start = home.index('<!-- POSTS_LIST_START -->')
        end = home.index('<!-- POSTS_LIST_END -->') + len('<!-- POSTS_LIST_END -->')
        block = (
            "<!-- POSTS_LIST_START -->\n"
            '    <div class="posts-grid">\n'
            f"        {cards}\n"
            "    <!-- POSTS_LIST_END -->"
        )
        home = home[:start] + block + home[end:]
        open('index.html', 'w', encoding='utf-8').write(home)

    print(f"Successfully synced {len(all_posts)} posts and generated static HTML files.")

if __name__ == '__main__':
    sync_posts()
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

def extract_featured_image(content):
    match = re.search(r'!\[([^\]]*)\]\((.*?)\)', content)
    if match:
        alt = re.sub(r'[*_`]', '', match.group(1)).strip()
        return match.group(2).strip(), alt
    match = re.search(r'<img\b[^>]*>', content, re.IGNORECASE)
    if match:
        tag = match.group(0)
        src_match = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        alt_match = re.search(r'\balt=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if src_match:
            return src_match.group(1), (alt_match.group(1) if alt_match else '').strip()
    return None, None

def normalize_image_url(url):
    if url.startswith('http://jhimross.com/'):
        return 'https://' + url[len('http://'):]
    return url

def thumbnail_url(url, size=600):
    if 'wordpress.com/wp-content/uploads/' not in url and 'files.wordpress.com/' not in url:
        return url
    if '?' in url:
        base, query = url.split('?', 1)
    else:
        base, query = url, ''
    params = []
    for pair in query.split('&'):
        if pair and pair.split('=', 1)[0] not in ('w', 'h', 'crop', 'resize', 'fit'):
            params.append(pair)
    params.extend([f'w={size}', f'h={size}', 'crop=1'])
    return base + '?' + '&'.join(params)

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
    for index, p in enumerate(all_posts):
        title = html.escape(p["title"], quote=True)
        initial = html.escape(next((char for char in p["title"] if char.isalnum()), "J").upper(), quote=True)
        image = p.get("image")
        if image:
            image = html.escape(thumbnail_url(normalize_image_url(image)), quote=True)
            alt = (p.get("image_alt") or p["title"]).strip()
            alt = html.escape(alt, quote=True)
            loading = "eager" if index < 4 else "lazy"
            thumb = (
                f'<div class="post-thumb">\n'
                f'                      <img src="{image}" alt="{alt}" width="600" height="600" loading="{loading}" decoding="async" onerror="this.closest(\'.post-thumb\').classList.add(\'post-thumb--broken\')" />\n'
                f'                      <span class="post-initial" aria-hidden="true">{initial}</span>\n'
                f'                    </div>'
            )
        else:
            thumb = (
                f'<div class="post-thumb post-thumb--fallback" aria-hidden="true">\n'
                f'                      <span class="post-initial">{initial}</span>\n'
                f'                    </div>'
            )
        parts.append(
            f'<article class="post-card">\n'
            f'                  <a class="post-link" href="{p["slug"]}.html">\n'
            f'                    {thumb}\n'
            f'                    <h2 class="post-title">{title}</h2>\n'
            f'                  </a>\n'
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
        image, image_alt = "", ""
        excerpt = ""

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
            elif line.startswith('excerpt:'):
                excerpt = line.replace('excerpt:', '').strip()
                if excerpt.startswith('"') and excerpt.endswith('"'):
                    excerpt = excerpt[1:-1].replace('\\"', '"')
            elif line.startswith('image_alt:'):
                image_alt = line.replace('image_alt:', '').strip()
                if image_alt.startswith('"') and image_alt.endswith('"'):
                    image_alt = image_alt[1:-1].replace('\\"', '"')
            elif line.startswith('image:'):
                image = line.replace('image:', '').strip()
                if image.startswith('"') and image.endswith('"'):
                    image = image[1:-1]

        if not (title and date_obj and slug):
            continue

        post = {
            "title": title,
            "date": date_obj.strftime('%B %d, %Y'),
            "slug": slug,
            "categories": categories,
            "file": filename,
            "image": image or None,
            "image_alt": image_alt or None
        }
        if excerpt:
            post["excerpt"] = excerpt
        all_posts.append(post)

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

        featured_image = p.get("image")
        featured_image_alt = p.get("image_alt")
        if not featured_image:
            featured_image, featured_image_alt = extract_featured_image(raw_content)
        featured_image = normalize_image_url(featured_image) if featured_image else None
        p["image"] = featured_image
        p["image_alt"] = featured_image_alt
        image = featured_image or "https://jhimross.com/assets/about.jpg"
        if p.get("excerpt"):
            description = html.escape(p["excerpt"], quote=True)
        else:
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
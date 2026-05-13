---
title: "My Zero-Cost Static Blog Migration (Just a fun experiment)"
date: 2026-05-13
slug: my-zero-cost-static-blog-migration
categories: ['Migration', 'Tech', 'GitHub']
---

I recently had to make an unexpected but interesting shift in my workflow: moving away from a traditional WordPress setup and rebuilding my entire blog as a static site powered by GitHub and Cloudflare Workers.

What started as a “my hosting expired” problem turned into a full rebuild that ended up being faster, simpler, and surprisingly closer to how I like building things.

One of the biggest wins in the process: I’m no longer paying any monthly hosting fees. The entire site now runs without recurring infrastructure costs.

Here’s how the migration happened, step by step.

---

## When my hosting expired, I had a decision to make

My hosting provider expired unexpectedly. Instead of renewing and going back to the usual WordPress setup, I took it as a signal to rethink the stack.

I’ve always liked the idea of static sites—less maintenance, faster performance, and no database to worry about. So I decided:

> Time to move everything to a static site hosted on GitHub + Cloudflare Workers.

---

## Exporting everything from WordPress

The first step was getting my content out of WordPress.

I exported my entire blog using the built-in WordPress XML export tool. This gave me a single `.xml` file containing:

- Blog posts  
- Pages  
- Categories and tags  
- Metadata (dates, titles, slugs, permalinks, etc.)

At this point, I basically had all my content “locked” in a format that needed transformation.

---

## Converting XML to Markdown with AI help

Instead of manually parsing XML (which would’ve been painful), I used **Antigravity** to help automate the process.

I asked it to:

- Recreate my existing website design structure  
- Parse the WordPress XML export  
- Convert blog posts into clean `.md` (Markdown) files  
- Preserve metadata like:
  - Title  
  - Featured image  
  - Taxonomy (tags/categories)  
  - Slugs and permalink structure  
  - Content structure  

This step was crucial. It turned WordPress content into something Git-friendly and portable.

Now each blog post lives as a simple Markdown file.

---

## Generating full HTML templates per blog post

This was a key step in keeping the structure intact.

I also asked **Antigravity** to generate HTML templates for each blog post so that every post already had:

- Correct slug-based routing  
- Permalink structure matching the original WordPress URLs  
- Metadata injection (title, description, featured image, tags)  
- A consistent post layout template  

Instead of relying on a CMS, each post follows a structured template that behaves like a rendered WordPress page—just without WordPress.

This is what allowed me to preserve URL consistency and structure while still moving to a static architecture.

---

## Rebuilding the site structure from scratch

Once the content and templates were ready, I rebuilt the frontend using plain HTML.

I created:

- `index.html` → blog listing page  
- `post.html` → individual blog post layout  
- `blog.html` → blog archive structure  
- `contact.html` → contact page  

Everything is template-driven instead of CMS-driven.

---

## Turning Markdown into a “pseudo-CMS”

Each blog post template dynamically reads from the `.md` file and extracts:

- Title  
- Featured image  
- Taxonomy (tags/categories)  
- Content  

Then it injects that data into the HTML template.

Even though it’s static, the system behaves like a dynamic CMS.

It feels like WordPress—but without WordPress.

---

## Organizing assets properly

All images from my old WordPress site were migrated into a simple structure:


/assets
/images
/posts


Every Markdown file references local assets directly—no external media system, no dependency overhead.

---

## Adding a contact form (without backend pain)

Instead of building my own backend just for forms, I used Formspree.

It gave me:

- Free form handling  
- Spam protection  
- Email delivery  
- No server required  

I embedded it into `contact.html`, and it worked instantly.

---

## Deployment with GitHub + Cloudflare Workers

The final architecture is simple but powerful:

1. Everything lives in a Git repository  
2. Every change is a commit  
3. Cloudflare Workers serves the site at the edge  

So now my workflow looks like this:

- Want to update a post? Edit a `.md` file  
- Want to add a page? Duplicate a template  
- Want to publish? Push to GitHub  

Then Cloudflare automatically deploys it.

No dashboards. No plugins. No database migrations.

Just Git.

---

## SEO stayed intact during migration

One of my biggest concerns was SEO. I didn’t want to lose years of search engine indexing.

To make sure nothing broke:

- Existing WordPress slugs were preserved exactly  
- URL structure stayed identical  
- Permalinks were replicated through the new template system  
- No redirects were needed because paths remained the same  

Search engines didn’t have to relearn the site. Everything remained under the same URLs they already indexed.

---

## Performance: perfect Lighthouse scores

After moving everything to a static architecture and serving it through Cloudflare, performance improved significantly.

The site now consistently scores:

- 100 Performance  
- 100 Accessibility  
- 100 Best Practices  
- 100 SEO  

on Google PageSpeed Insights.

No heavy optimization tricks—just a lightweight site served at the edge.

---

## No more monthly hosting bills

The biggest practical change in all of this is financial:

There are no longer any monthly hosting fees.

No shared hosting renewal.  
No database costs.  
No CMS subscriptions.  

Just a GitHub repo and Cloudflare Workers running everything.

It’s a one-time setup that now runs continuously with zero recurring infrastructure cost.

---

## Not abandoning WordPress—just experimenting

I also want to be clear: this isn’t me abandoning WordPress.

It was simply a fun experiment during a gap when I didn’t have hosting available. Instead of seeing it as a limitation, I treated it as an opportunity to explore a different architecture.

And honestly—it was worth it.

It gave me a better understanding of static site workflows, a cleaner deployment process, and a deeper appreciation of how much can be done without a traditional CMS.

---

## How it feels now

What surprised me most is how “dynamic” the site still feels, even though it’s static.

It behaves like a CMS because:

- Content is structured (Markdown + metadata)  
- Templates are reusable  
- Pages are generated consistently  
- Deployment is automated  

But it’s also:

- Faster  
- More secure  
- Easier to version control  
- Easier to recover or rebuild  
- And now, completely free to host monthly  

---

## Repository

If you want to explore the setup or use it as a reference, here’s the project:

https://github.com/jhimross/jhimross.com

---

## Final thoughts

This migration wasn’t originally planned—it started as a hosting issue. But it ended up being one of the most freeing changes I’ve made to my workflow.

Moving away from WordPress doesn’t mean losing functionality. It just means rethinking *where complexity should live*.

For me, the answer is simple now:

- Content → Markdown  
- Templates → HTML per post  
- Routing → Slug-based structure  
- Hosting → Edge (Cloudflare Workers)  
- Source of truth → GitHub  
- Cost → $0 monthly hosting fees  

And honestly, that’s enough.

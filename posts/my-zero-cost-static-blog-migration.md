---
title: "My Zero-Cost Static Blog Migration (Just a fun experiment)"
date: 2026-05-13
slug: my-zero-cost-static-blog-migration
categories: ['Migration', 'Tech', 'GitHub']
---

I recently had to make an unexpected but interesting shift in my workflow: moving away from a traditional WordPress setup and rebuilding my entire blog as a static site powered by GitHub and Cloudflare Workers.

<img width="1504" height="968" alt="image" src="https://github.com/user-attachments/assets/a635cbb2-e06c-41e0-bc31-f3c0a7b3c4d8" />


What started as a “my hosting expired” problem turned into a full rebuild that ended up being faster, simpler, and surprisingly closer to how I like building things.

One of the biggest wins in the process: I’m no longer paying any monthly hosting fees. The entire site now runs without recurring infrastructure costs.

Here’s how the migration happened, step by step.



## When my hosting expired, I had a decision to make

My hosting provider expired unexpectedly. Instead of renewing and going back to the usual WordPress setup, I took it as a signal to rethink the stack.

I’ve always liked the idea of static sites—less maintenance, faster performance, and no database to worry about. So I decided:

> Time to move everything to a static site hosted on GitHub + Cloudflare Workers.

## Exporting everything from WordPress

The first step was getting my content out of WordPress.

<img width="1084" height="762" alt="image" src="https://github.com/user-attachments/assets/91b76d0e-6636-48c5-9b7e-d6929ed95c30" />


I exported my entire blog using the built-in WordPress XML export tool. This gave me a single `.xml` file containing:

- Blog posts  
- Pages  
- Categories and tags  
- Metadata (dates, titles, slugs, permalinks, etc.)

At this point, I basically had all my content “locked” in a format that needed transformation.


## Converting XML to Markdown with AI help

Instead of manually parsing XML (which would’ve been painful), I used **Antigravity** to help automate the process.

<img width="1512" height="845" alt="image" src="https://github.com/user-attachments/assets/f55eace2-34e1-4b07-8799-c9ea19695cbf" />


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

## Generating full HTML templates per blog post

This was a key step in keeping the structure intact.

I also asked **Antigravity** to generate HTML templates for each blog post so that every post already had:

<img width="1549" height="864" alt="image" src="https://github.com/user-attachments/assets/f8ed9b67-7412-4c87-9142-3a645f01c35c" />


- Correct slug-based routing  
- Permalink structure matching the original WordPress URLs  
- Metadata injection (title, description, featured image, tags)  
- A consistent post layout template  

Instead of relying on a CMS, each post follows a structured template that behaves like a rendered WordPress page—just without WordPress.

This is what allowed me to preserve URL consistency and structure while still moving to a static architecture.


## Rebuilding the site structure from scratch

Once the content and templates were ready, I rebuilt the frontend using plain HTML.

<img width="634" height="366" alt="image" src="https://github.com/user-attachments/assets/91aa6eba-d752-4c1c-959d-1d2be064bc94" />


I created:

- `index.html` → blog listing page  
- `post.html` → individual blog post layout  
- `blog.html` → blog archive structure  
- `contact.html` → contact page  

Everything is template-driven instead of CMS-driven.



## Turning Markdown into a “pseudo-CMS”

Each blog post template dynamically reads from the `.md` file and extracts:

<img width="547" height="202" alt="image" src="https://github.com/user-attachments/assets/0f062c55-53a2-4f5b-a93d-4d4f784db034" />


- Title  
- Featured image  
- Taxonomy (tags/categories)  
- Content  

Then it injects that data into the HTML template.

Even though it’s static, the system behaves like a dynamic CMS.

It feels like WordPress—but without WordPress.



## Organizing assets properly

All images from my old WordPress site were migrated into a simple structure:

<img width="563" height="333" alt="image" src="https://github.com/user-attachments/assets/cb9de0e4-377d-47bf-8a1a-7ebe99566bee" />


/assets
/images
/posts


Every Markdown file references local assets directly—no external media system, no dependency overhead.


## Adding a contact form (without backend pain)

Instead of building my own backend just for forms, I used Web3Forms.

<img width="1863" height="956" alt="image" src="https://github.com/user-attachments/assets/30fd6b07-29a0-4c20-a4cd-25fb900674f5" />


It gave me:

- Free form handling  
- Spam protection  
- Email delivery  
- No server required  

I embedded it into `contact.html`, and it worked instantly.



## Deployment with GitHub + Cloudflare Workers

The final architecture is simple but powerful:

<img width="1906" height="964" alt="image" src="https://github.com/user-attachments/assets/6d660280-afa2-4c22-b9da-9b6980cbcf25" />


1. Everything lives in a Git repository  
2. Every change is a commit  
3. Cloudflare Workers serves the site at the edge  

So now my workflow looks like this:

- Want to update a post? Edit a `.md` file  
- Want to add a page? Duplicate a template  
- Want to publish? Push to GitHub  

Then Cloudflare automatically deploys it.

<img width="1906" height="969" alt="image" src="https://github.com/user-attachments/assets/e1f29f0e-d84c-465b-83c9-3d64ee72524d" />


No dashboards. No plugins. No database migrations.

Just Git.



## SEO stayed intact during migration

One of my biggest concerns was SEO. I didn’t want to lose years of search engine indexing.

To make sure nothing broke:

- Existing WordPress slugs were preserved exactly  
- URL structure stayed identical  
- Permalinks were replicated through the new template system  
- No redirects were needed because paths remained the same

Search engines didn’t have to relearn the site. Everything remained under the same URLs they already indexed.



## Performance: perfect Lighthouse scores

After moving everything to a static architecture and serving it through Cloudflare, performance improved significantly.

<img width="978" height="548" alt="image" src="https://github.com/user-attachments/assets/36608705-0479-48e8-8afb-b04da0dc56e2" />


The site now consistently scores:

- 100 Performance  
- 100 Accessibility  
- 100 Best Practices  
- 100 SEO  

on Google PageSpeed Insights.

No heavy optimization tricks—just a lightweight site served at the edge.



## No more monthly hosting bills

The biggest practical change in all of this is financial:

There are no longer any monthly hosting fees.

No shared hosting renewal.  
No database costs.  
No CMS subscriptions.  

Just a GitHub repo and Cloudflare Workers running everything.

It’s a one-time setup that now runs continuously with zero recurring infrastructure cost.



## Not abandoning WordPress—just experimenting

I also want to be clear: this isn’t me abandoning WordPress.

It was simply a fun experiment during a gap when I didn’t have hosting available. Instead of seeing it as a limitation, I treated it as an opportunity to explore a different architecture.

And honestly—it was worth it.

It gave me a better understanding of static site workflows, a cleaner deployment process, and a deeper appreciation of how much can be done without a traditional CMS.



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

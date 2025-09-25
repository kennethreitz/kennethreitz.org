# TufteCMS Documentation

*An experimental Flask-based content management system for markdown-driven websites*

TufteCMS is an experimental, minimal, opinionated framework for building content-rich websites from markdown files. It emphasizes readability, cross-referencing, and contemplative design patterns inspired by Edward Tufte's principles of information design.

> **Experimental Software**: TufteCMS is in active development and should be considered experimental. APIs may change, features may be incomplete, and documentation may lag behind implementation. Use in production at your own discretion.

## Core Philosophy

- **Markdown-first**: All content lives in readable markdown files
- **Human-readable URLs**: Clean, semantic paths that mirror content structure  
- **Cross-referencing**: Rich internal linking and connection tracking
- **Tufte-style annotations**: Marginal sidenotes for depth without disruption
- **Caching-aware**: Intelligent content caching with background warming
- **Minimal dependencies**: Flask + essential markdown processing

## Download & Installation

### GitHub Repository

Download TufteCMS from the official repository:

**[Download TufteCMS](https://github.com/kennethreitz/kennethreitz.org)**

```bash
# Clone the repository
git clone https://github.com/kennethreitz/kennethreitz.org.git
cd kennethreitz.org

# The TufteCMS framework is in the tuftecms/ directory
# Your content goes in the data/ directory
```

### Installation Options

**Option 1: Use as Framework Template**
```bash
# Copy the tuftecms/ directory to your new project
cp -r tuftecms/ /path/to/your/new-site/
cp engine.py /path/to/your/new-site/

# Install dependencies
cd /path/to/your/new-site/
uv sync  # or pip install flask markdown
```

**Option 2: Fork and Customize**
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/kennethreitz.org.git
cd kennethreitz.org

# Remove existing content and add your own
rm -rf data/essays/*
# Add your content to data/
```

## Quick Start

```python
# engine.py
from tuftecms import create_app

app = create_app()
app.run(debug=True)
```

Your content structure:

```
data/
├── index.md              # Homepage content
├── essays/               # Blog posts and essays
│   ├── 2025-01-01-hello-world.md
│   └── index.md          # Essays index
├── docs/                 # Documentation
│   └── index.md          # This file
└── static/              # Static assets
    ├── images/
    └── css/
```

## Key Features

### Automatic Content Discovery

TufteCMS automatically serves markdown files based on URL structure:

- `/` → `data/index.md`
- `/essays/hello-world` → `data/essays/hello-world.md` 
- `/docs` → `data/docs/index.md`
- `/docs/getting-started` → `data/docs/getting-started.md`

### Rich Metadata Extraction

Each markdown file can include frontmatter for metadata:

```yaml
---
title: "My Essay"
date: 2025-01-01
tags: [philosophy, code]
---

# My Essay

Content here...
```

### Sidenotes

Add Tufte-style sidenotes for non-disruptive annotations:

```html
This is the main text.
<label for="sn-1" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-1" class="margin-toggle"/>
<span class="sidenote">This is a sidenote that appears in the margin.</span>
```

### Cross-Reference Tracking

TufteCMS automatically tracks internal links and builds:

- **Connections index**: What links to what
- **Backlinks**: Incoming references to each page
- **Graph visualization**: Interactive network of content relationships

### Content Indexes

The system automatically generates:

- **Sidenotes index**: All marginal annotations across the site
- **Outlines index**: Heading structure from all articles  
- **Quotes index**: Blockquotes extracted from content
- **Terms index**: Key concepts with cross-references
- **Archive**: Chronological content organization

## Directory Structure

```
kennethreitz.org/
├── data/                 # All content
│   ├── index.md         # Homepage
│   ├── essays/          # Blog posts
│   ├── docs/            # Documentation
│   └── static/          # Images, assets
├── tuftecms/            # Framework code
│   ├── app.py          # Flask application factory
│   ├── blueprints/     # Route handlers
│   ├── core/           # Markdown rendering, caching
│   ├── utils/          # Content utilities
│   ├── templates/      # Jinja2 templates
│   └── static/         # CSS, JavaScript
└── engine.py           # Development server
```

## Documentation Guide

### Getting Started
- **[Getting Started](/docs/getting-started)** - Set up your first TufteCMS site from scratch
- **[Content Structure](/docs/content-structure)** - Learn how to organize your markdown files effectively

### Content Creation  
- **[Sidenotes Guide](/docs/sidenotes)** - Master Tufte-style marginal annotations
- **[Content Structure](/docs/content-structure)** - File naming, URL patterns, and organization strategies

### Customization & Deployment
- **[Customization](/docs/customization)** - Templates, styling, and brand integration  
- **[Deployment](/docs/deployment)** - Production configuration and hosting options

### Deployment Ready

TufteCMS is designed for easy deployment across platforms:

- **Traditional servers** - Nginx + Gunicorn configuration examples
- **Platform-as-a-Service** - Heroku, Railway, Fly.io ready  
- **Static generation** - Build HTML for Netlify, Vercel, GitHub Pages
- **Containerization** - Docker examples for scalable deployment

See the complete [deployment guide](/docs/deployment) for platform-specific instructions.

### Cross-References
Throughout these guides, you'll find extensive cross-linking between concepts. For example:
- [Sidenotes](/docs/sidenotes) integrate with the [content structure](/docs/content-structure) for optimal placement
- [Customization](/docs/customization) builds on concepts from [getting started](/docs/getting-started)
- [Deployment](/docs/deployment) assumes familiarity with [content organization](/docs/content-structure)

---

*TufteCMS embodies the principle that technology should serve human consciousness, not exploit it. Every design choice prioritizes readability, contemplation, and authentic expression over engagement metrics or algorithmic optimization.*
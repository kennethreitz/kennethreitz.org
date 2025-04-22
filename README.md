# kennethreitz.org

This is the repository for the website kennethreitz.org. It is built using FastAPI, Tailwind CSS, and Markdown.

## Features

- Fast and lightweight static site generation from Markdown files
- TailwindCSS for beautiful, responsive layouts
- Support for frontmatter metadata in YAML format
- Automatic image gallery generation
- Dark mode support
- API endpoints for headless content access
- Content search functionality
- Tag-based content organization
- Image EXIF data display
- Smart template selection based on content type

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for Tailwind CSS)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kennethreitz/kennethreitz.org.git
   cd kennethreitz.org
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```

4. Build the CSS:
   ```bash
   npm run build:css
   ```

5. Run the development server:
   ```bash
   python tuftedoc.py
   ```

## Directory Structure

```
kennethreitz.org/
├── data/            # Content directory with markdown files
├── static/          # Static assets (CSS, images, etc.)
│   ├── custom.css   # Generated CSS file
│   └── tailwind-input.css  # Tailwind source CSS
├── templates/       # HTML templates
├── tuftedoc.py      # The main application
├── package.json     # Node.js dependencies
└── tailwind.config.js  # Tailwind configuration
```

## Content Organization

All content should be placed in the `data/` directory. The structure of this directory determines the URL structure of your site.

### Frontmatter Metadata

You can add YAML frontmatter to your markdown files to provide metadata:

```markdown
---
title: My Article Title
date: 2023-01-01
author: Your Name
tags: [python, web, development]
description: A brief description of the article
featured_image: /path/to/image.jpg
draft: false
layout: special-template
---

# My Article Title

Content goes here...
```

## Templates

The following templates are available:

- `base.html`: The base template with common elements
- `index.html`: Default template for most pages
- `directory.html`: Template for directory listings
- `post.html`: Template for individual posts
- `photo_browser.html`: Template for image galleries

## API Endpoints

The site includes several API endpoints for headless access:

- `/api/content/{path}`: Get content and metadata for a specific path
- `/api/search?q={query}`: Search content
- `/api/tags`: Get all tags with counts

## Development

### CSS Development

To watch for CSS changes during development:

```bash
npm run watch:css
```

### Debug Mode

To enable draft content and additional debugging:

```bash
DEBUG=1 python tuftedoc.py
```

## Deployment

### Docker

A Dockerfile is included for easy deployment:

```bash
docker build -t kennethreitz-org .
docker run -p 8000:8000 kennethreitz-org
```

### Fly.io

The project includes configuration for Fly.io:

```bash
fly deploy
```

## License

This project is personal work by Kenneth Reitz.

## Acknowledgments

- Built with FastAPI and Tailwind CSS
- Inspired by Tufte CSS design principles

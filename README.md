# kennethreitz.org

Kenneth Reitz's personal website and digital garden. A living exploration of how technology can serve human consciousness rather than exploit it.

Built with [Responder](https://github.com/kennethreitz/responder), powered by markdown content, deployed on [Fly.io](https://fly.io).

## Quick Start

```bash
# Install dependencies
uv sync

# Run development server
uv run python engine.py
```

The site will be available at `http://localhost:8000`.

### Docker

```bash
docker compose up
```

## Architecture

This is a single-file Responder application (`engine.py`) serving markdown content from `data/`.

```
kennethreitz.org/
├── engine.py              # The whole application
├── data/                  # All content (markdown)
│   ├── essays/            # 250+ essays (2008-2026)
│   ├── software/          # Project pages
│   ├── themes/            # Thematic collections
│   ├── artificial-intelligence/
│   ├── poetry/
│   ├── photography/
│   ├── music/
│   └── *.md               # Standalone pages
├── tuftecms/
│   ├── templates/         # Jinja2 templates
│   ├── static/            # CSS, fonts, images
│   ├── core/              # Cache, markdown rendering
│   └── utils/             # Content helpers, SVG icons
├── Dockerfile
├── fly.toml               # Fly.io deployment config
└── pyproject.toml
```

URL paths mirror the filesystem: `data/essays/2025-08-26-example.md` → `/essays/2025-08-26-example`

## Features

- **Tufte-style sidenotes** — margin commentary without disrupting flow.
- **Full-site search** — cached index built at startup, server-side autocomplete.
- **Content indexes** — automatic extraction of sidenotes, quotes, outlines, connections, terms, themes.
- **Legacy URL redirects** — intelligent matching for old URL patterns (301 permanent).
- **Bot detection** — logs scraper activity with User-Agent identification.
- **Structured logging** — request-scoped context (ID, method, path, client IP) on every log line.
- **PDF generation** — server-side via WeasyPrint.
- **Generated SVG icons** — unique algorithmic icons for every piece of content.
- **RSS feed** — at `/feed.xml`.
- **Knowledge graph** — interactive D3 visualization of content connections.
- **Dark mode** — system-preference and manual toggle.

## API Endpoints

```
GET /api/search?q=query           # Full-site search with scoring
GET /api/search/autocomplete?q=q  # Title-based autocomplete (8 results)
GET /api/blog                     # Essay listing
GET /api/themes                   # Theme listing with icons
GET /api/directory-tree            # Site directory structure
GET /api/icon/<path>              # Generated SVG icon
GET /api/cache-stats              # Cache performance metrics
```

## Deployment

Deployed on Fly.io with 2 shared CPUs, 2GB RAM, 2 uvicorn workers.

```bash
fly deploy
```

## Content

The `data/` directory contains 15+ years of writing — essays, software documentation, poetry, photography, AI explorations, and personal pages. Content is plain markdown with optional YAML frontmatter and Tufte-style HTML sidenotes.

## License

MIT

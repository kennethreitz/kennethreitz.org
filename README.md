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
│   ├── knowledge/         # Published from the Obsidian vault (generated)
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

## Knowledge

`/knowledge` publishes the `Knowledge/` folder of Kenneth's Obsidian vault:
mythology, tarot, psychology, music theory, and the rest of the reference
shelf. The same sync publishes `Library/Books/` to `/library/books` and
refreshes a History block on the matching `/software` pages. Those software
pages stay hand-written. Only the block between `<!-- vault:history start -->`
and `<!-- vault:history end -->` is replaced.

It's generated, so edit the vault and re-sync rather than editing
`data/knowledge/` or `data/library/books/` by hand:

```bash
$ uv run python scripts/sync_vault.py --vault ~/Notes
$ make sync-vault VAULT=~/Notes
```

`scripts/import_knowledge.py` is the same command. `--dry-run` reports what
would change and writes nothing. `--check` exits 1 when the tree does not
already match. A vault with only a handful of Knowledge notes is refused,
so a partial folder cannot wipe the shelf. Pass `--allow-partial` only when
that is what you mean.

Personal notes in `HARD_EXCLUDE` are never published. Other withheld notes
are listed in `EXCLUDED`. A scrubbed note lives in
`scripts/knowledge_overrides/` or `scripts/library_overrides/` at the same
relative path as the vault file. `manifest.json` beside those files records
the sha256 of the vault source the override was written from. If the vault
note changes, sync prints a warning and still publishes the override. The
privacy guard (built-in patterns, plus `KNOWLEDGE_PRIVATE_TERMS` outside
this repo) runs on the override, not on the raw note.

At render time, `tuftecms/core/knowledge.py` turns published note titles
into a concept index: the first mention of a concept on an ordinary page
links to its Knowledge note (capped per page, never inside headings, code,
links, or sidenotes), and every Knowledge note lists the pages that mention it.

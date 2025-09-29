# TufteCMS

A Flask-based content management system designed for thoughtful writing, inspired by Edward Tufte's design principles. Built for digital gardens, essay collections, and content-rich websites that prioritize readability and deep engagement.

## Philosophy

TufteCMS embraces **human-first design** - content presentation that serves readers' mental models rather than forcing adaptation to machine logic. It provides powerful features like sidenotes, content indexing, and cross-referencing while maintaining simplicity and elegance.

## Features

### Content & Typography
- **Tufte-style sidenotes** - Margin commentary without disrupting reading flow
- **Responsive typography** - Optimized for reading across all devices
- **Markdown rendering** - Custom Mistune renderer with philosophical code blocks
- **File-based content** - Simple directory structure mirrors URL routing

### Discovery & Navigation
- **Full-text search** - Relevance-scored search with contextual snippets
- **Content indexes** - Automatic extraction of sidenotes, quotes, outlines, connections, terms
- **Cross-referencing** - Track incoming/outgoing links between content
- **Theme detection** - Automatic categorization by content patterns
- **HTML & XML sitemaps** - Both human and machine-readable navigation

### Visual Identity
- **Generated SVG icons** - Unique algorithmic icons for every piece of content
- **Deterministic design** - Same title always produces the same icon
- **Dynamic folder icons** - Color variations based on content titles
- **Reading progress** - Visual indicator for longer essays

### Performance
- **Intelligent caching** - LRU caches for blog posts, indexes, and metadata
- **Background cache warming** - Async startup loading for instant response
- **Lazy loading** - Images load via IntersectionObserver
- **HTTP caching headers** - Aggressive caching for static assets
- **Cache debugging** - API endpoint to monitor cache performance

### Developer Experience
- **Flask blueprints** - Modular architecture with clear separation
- **API endpoints** - JSON APIs for search, icons, and debugging
- **RSS/Atom feeds** - Standard feed formats for syndication
- **Template system** - Jinja2 templates with extensible blocks

## Installation

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/kennethreitz/tuftecms.git
cd tuftecms

# Install dependencies
uv sync

# Run development server
uv run python engine.py
```

The site will be available at `http://localhost:8000`

## Project Structure

```
tuftecms/
├── tuftecms/
│   ├── app.py              # Application factory
│   ├── config.py           # Configuration management
│   ├── blueprints/         # Route handlers
│   │   ├── main.py         # Homepage and core routes
│   │   ├── content.py      # Content rendering
│   │   ├── api.py          # JSON API endpoints
│   │   └── feeds.py        # RSS/sitemap generation
│   ├── core/               # Core functionality
│   │   ├── cache.py        # Caching system
│   │   ├── content.py      # Content processing
│   │   └── markdown.py     # Markdown rendering
│   ├── utils/              # Utilities
│   │   ├── content.py      # Content helpers
│   │   └── svg_icons.py    # Icon generation
│   ├── templates/          # Jinja2 templates
│   └── static/             # CSS, images, fonts
├── data/                   # Content directory
│   └── essays/             # Your content here
├── engine.py               # Development server
└── pyproject.toml          # Dependencies
```

## Content Organization

### Directory Structure

Content is organized in a simple directory structure under `data/`:

```
data/
├── essays/
│   ├── 2025-01-15-example-essay.md
│   └── 2025-02-20-another-essay.md
├── notes/
└── index.md
```

URL paths mirror the file system: `/essays/2025-01-15-example-essay`

### Writing with Sidenotes

Sidenotes provide commentary without disrupting reading flow:

```markdown
This is the main text.<label for="sn-example" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-example" class="margin-toggle"/><span class="sidenote">This is a sidenote that adds depth without breaking the narrative.</span> The text continues naturally.
```

**Critical formatting rules:**
- Sidenotes must be inline (attached to sentence end with NO line breaks)
- Use descriptive IDs like `sn-consciousness`, `sn-recursion`
- Keep away from code blocks to prevent layout issues

### Markdown Features

```markdown
# Essay Title

*Published: January 2025*

Standard markdown with [links](/other-essay) and **emphasis**.

Code blocks with philosophy:

\`\`\`python
def consciousness():
    # TODO: Model the unmappable
    pass
\`\`\`

> Blockquotes for memorable passages
```

## Configuration

Edit `tuftecms/config.py`:

```python
class Config:
    DISABLE_ANALYTICS = True  # Privacy-first by default
    SEARCH_CACHE_TIMEOUT = 60
    DATA_DIR = "data"
    MIN_SEARCH_QUERY_LENGTH = 2
    MAX_SEARCH_RESULTS = 50
```

## API Endpoints

### Search
```
GET /api/search?q=query
```

Returns JSON with relevance-scored results, snippets, and match locations.

### Cache Debugging
```
GET /api/debug-cache
```

Returns cache statistics and LRU cache performance metrics.

### Icon Generation
```
GET /api/icon/<path:article_path>
```

Returns generated SVG icon data for any content path.

## Content Indexes

TufteCMS automatically builds indexes:

- **Sidenotes** - All margin notes with context
- **Outlines** - Heading structure across content
- **Quotes** - Blockquoted passages
- **Connections** - Internal link graph
- **Terms** - Key terms appearing across multiple articles
- **Themes** - Pattern-based content categorization

Access via routes: `/sidenotes`, `/outlines`, `/quotes`, `/connections`, `/terms`

## Deployment

### Docker

```bash
docker build -t tuftecms .
docker run -p 8000:8000 tuftecms
```

### Production with Gunicorn

```bash
uv run gunicorn -w 4 -b 0.0.0.0:8000 'tuftecms.app:create_app()'
```

### Environment Variables

```bash
DISABLE_ANALYTICS=true  # Disable analytics
DEBUG=1                 # Enable debug mode
```

## Development

### Debug Mode

```bash
DEBUG=1 uv run python engine.py
```

Enables verbose logging and development features.

### Cache Management

Clear all caches:

```python
from tuftecms.core.cache import clear_all_caches
clear_all_caches()
```

### Adding New Features

1. Create new blueprint in `tuftecms/blueprints/`
2. Register in `app.py`
3. Add templates to `tuftecms/templates/`
4. Update cache logic if needed in `core/cache.py`

## Philosophy & Design

TufteCMS is built on principles of **contemplative pragmatism**:

- **Human-first design** - Optimize for people having difficult days
- **Simple over clever** - Tools should feel natural to use
- **Content-focused** - Design serves the writing, not the ego
- **Respectful reading** - No dark patterns, no engagement manipulation
- **Open and inspectable** - Clean code, clear architecture

The name honors Edward Tufte's work on information design - presenting complex information with clarity and respect for the reader's intelligence.

## Use Cases

- **Digital gardens** - Personal knowledge bases that grow organically
- **Essay collections** - Long-form writing with depth and cross-references
- **Academic writing** - Papers with extensive sidenotes and citations
- **Documentation sites** - Technical docs with commentary
- **Philosophy blogs** - Contemplative writing with layered meaning

## License

MIT License - see LICENSE file for details.

## Credits

Created by Kenneth Reitz as part of kennethreitz.org. Built with Flask, Mistune, and care for human consciousness.

---

*"Technology should serve human mental models, not force humans to adapt to machine logic."*
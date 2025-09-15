# kennethreitz.org

Kenneth Reitz's personal website and digital garden—a living exploration of consciousness, technology, and the recursive loops between code and mind.

Built with Flask, Mistune, and philosophical inquiry.

## Architecture

- **Flask** for routing and templating
- **Mistune** for Markdown processing with custom renderers
- **Tufte CSS** inspiration for typography and layout
- **Custom CSS** for sidenotes, responsive design, and visual hierarchy
- **File-based content** stored in `/data/` directory structure

## Features

- Tufte-style sidenotes with margin toggles
- Responsive typography optimized for reading
- Custom Markdown extensions for philosophy and code
- Automatic directory-based routing
- Image galleries with metadata extraction
- Full-text search across content
- Custom post templates based on content type
- API endpoints for headless access

## Getting Started

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kennethreitz/kennethreitz.org.git
cd kennethreitz.org

# Install dependencies
uv sync

# Run development server
uv run python engine.py
```

The site will be available at `http://localhost:8000`

## Directory Structure

```
kennethreitz.org/
├── data/               # All content (essays, AI work, talks, etc.)
│   ├── essays/         # Philosophy, consciousness, technology
│   ├── artificial-intelligence/  # AI collaboration and research
│   ├── talks/          # Speaking engagements and presentations
│   ├── themes/         # Curated collections by topic
│   └── ...
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, images, fonts
├── engine.py           # Main Flask application
└── CLAUDE.md           # Instructions for AI collaboration
```

## Content Organization

Content uses a directory-based structure where URL paths mirror the file system.

### Sidenotes

The site uses Tufte-style sidenotes for commentary without disrupting flow:

```html
Main text<label for="sn-id" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-id" class="margin-toggle"/><span class="sidenote">Sidenote content</span> continues.
```

## Templates

- `base.html` - Common layout and navigation
- `homepage.html` - Landing page with pathways into the work
- `post.html` - Individual essays and articles
- `directory.html` - Directory listings with descriptions
- `photo_browser.html` - Image galleries

## Development

### Debug Mode

```bash
DEBUG=1 uv run python engine.py
```

Enables draft content visibility and additional logging.

### Content Guidelines

- Write like thinking out loud—conversational but precise
- Use sidenotes for depth without disrupting flow
- Code examples should breathe with proper whitespace
- Cross-link extensively to build conceptual webs
- Maintain Kenneth's voice: vulnerable authenticity meets technical precision

## The Mission

This site documents the journey of building technology that serves human consciousness rather than exploiting it. Every essay, code example, and design decision reflects the core insight: **code shapes minds, programmers shape code, therefore programmers shape collective consciousness.**

The recursive loop between technical work and philosophical inquiry drives everything here—from API design principles to consciousness research, from mental health advocacy to algorithmic critique.

## Deployment

The site is containerized and can be deployed anywhere that supports Python web applications:

```bash
# Docker
docker build -t kennethreitz-org .
docker run -p 8000:8000 kennethreitz-org

# Or with uv in production
uv run gunicorn -w 4 -b 0.0.0.0:8000 engine:app
```

## License

The code is [MIT licensed](LICENSE). The content is personal work by Kenneth Reitz and reflects ongoing exploration of consciousness, technology, and the spaces between minds.

---

*"We sit at the center of the feedback loop between code and consciousness. What we optimize for personally, we tend to optimize for professionally. The values we embody, we embed."*
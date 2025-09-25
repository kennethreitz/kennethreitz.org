# Getting Started with TufteCMS

*Build your first content-driven website*

TufteCMS transforms markdown files into a rich, interconnected digital garden. This guide walks through setting up your first site.

> **Note**: TufteCMS is experimental software. Features and APIs may change as the framework evolves.

## Installation

TufteCMS requires Python 3.8+ and uses Flask as its web framework.

```bash
# Clone or download TufteCMS
git clone https://github.com/user/tuftecms.git
cd tuftecms

# Install dependencies (using uv recommended)
uv sync

# Or with pip
pip install flask markdown
```

## Project Structure

Create your content directory structure:

```
your-site/
├── data/                 # All your content
│   ├── index.md         # Homepage
│   ├── essays/          # Blog posts
│   │   ├── index.md     # Essays landing page
│   │   └── 2025-01-01-first-post.md
│   └── docs/            # Documentation
├── tuftecms/            # Framework (if not installed as package)
└── engine.py           # Development server
```

## Homepage Template

TufteCMS uses a template-based homepage. Copy the starter template:

```bash
# Copy the starter homepage template
cp tuftecms/templates/homepage-starter.html tuftecms/templates/homepage.html
```

Then customize `tuftecms/templates/homepage.html` to reflect your unique voice and vision. The starter template provides:
- Basic layout structure
- Sample content sections  
- Integration with TufteCMS index counts
- Responsive design elements
- Example of pathway boxes for content organization

## Your First Content

Create content pages in the `data/` directory:

```markdown
# data/essays/welcome.md

# Welcome to My Digital Garden

This is my first essay. TufteCMS will automatically serve this at `/essays/welcome`.

I can link to [other pages](/docs) and they'll be tracked in the connections system.

## About This Site

Built with [TufteCMS](/docs) - a framework for contemplative digital publishing.
```

## Development Server

Start the development server:

```bash
# Using uv (recommended)
uv run python engine.py

# Or directly with Python
python engine.py
```

Visit `http://localhost:5000` to see your site.

## Writing Content

### Basic Markdown

TufteCMS supports standard markdown with enhancements:

```markdown
# Main Heading

## Section Heading

Regular paragraph with *emphasis* and **strong** text.

- Bullet points
- Are supported
- Naturally

1. As are
2. Numbered lists

> Blockquotes are tracked in the quotes index

Code blocks work as expected:
```python
def hello_world():
    return "Hello from TufteCMS!"
```

### Content Structure

TufteCMS automatically extracts titles from your markdown headings:

```markdown
# Your Content Title

This becomes the page title automatically. TufteCMS will serve this content and extract metadata from the structure and filename.
```

### Internal Linking

Link between pages using clean URLs:

```markdown
Check out my [latest essay](/essays/programming-philosophy).

See the [complete documentation](/docs) for more details.
```

TufteCMS automatically:
- Tracks these connections
- Builds backlink indexes  
- Creates network visualizations
- Generates related content suggestions

## Adding Sidenotes

Sidenotes provide non-disruptive way to add depth:

```markdown
This is the main narrative flow.<label for="sn-example" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-example" class="margin-toggle"/><span class="sidenote">This appears in the margin without disrupting the reading flow.</span> The text continues naturally.
```

**Critical formatting notes:**
- Sidenotes must be inline with no line breaks
- Place them at the end of sentences (after the period)
- Keep them away from code blocks  
- Use descriptive IDs like `sn-technique-name`

## Directory Organization

Organize content logically:

```
data/
├── index.md              # Homepage
├── essays/               # Long-form writing
│   ├── index.md         # Essays index page
│   ├── 2025-01-01-introduction.md
│   └── 2025-01-15-philosophy.md
├── notes/               # Shorter observations
│   ├── index.md
│   └── daily-thoughts.md
├── projects/            # Work portfolio
│   ├── index.md
│   └── tuftecms.md
└── docs/               # Documentation
    ├── index.md
    └── getting-started.md
```

URLs automatically follow this structure:
- `/essays/introduction` → `data/essays/introduction.md`
- `/projects/tuftecms` → `data/projects/tuftecms.md`
- `/notes` → `data/notes/index.md`

## Content Discovery Features

TufteCMS automatically provides:

### Indexes
- **Archive**: Chronological listing of all content
- **Connections**: Cross-reference mapping between pages
- **Sidenotes**: All marginal annotations across the site
- **Quotes**: Blockquotes extracted from content
- **Terms**: Key concepts with occurrence tracking

### Navigation
- **Search**: Full-text search across all content
- **Graph**: Interactive visualization of content connections
- **Random**: Serendipitous content discovery
- **Related**: Algorithm-suggested related content

## Next Steps

Now that you have a basic site running:

1. **Organize your content** - Learn about [content structure](/docs/content-structure) for optimal file organization
2. **Add depth with sidenotes** - Master [Tufte-style annotations](/docs/sidenotes) for contemplative writing
3. **Customize your site** - Explore [customization options](/docs/customization) for templates and styling
4. **Deploy to production** - Follow the [deployment guide](/docs/deployment) for hosting options

### Related Documentation

- **[Content Structure](/docs/content-structure)** - Essential reading for organizing larger sites
- **[Sidenotes Guide](/docs/sidenotes)** - Learn TufteCMS's signature feature for adding depth
- **[Customization Guide](/docs/customization)** - Make the framework reflect your unique vision
- **[Documentation Index](/docs)** - Complete overview of all guides and features

---

*Remember: TufteCMS optimizes for human reading time over writing time. Every feature serves the goal of making your content more discoverable, connected, and contemplative.*
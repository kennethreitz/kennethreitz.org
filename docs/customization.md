# Customization Guide

*Making TufteCMS reflect your unique voice and vision*

TufteCMS provides a foundation for contemplative digital publishing while remaining flexible enough to adapt to your specific needs and aesthetic preferences.

> This guide assumes familiarity with [getting started](/docs/getting-started) and [content structure](/docs/content-structure). For specialized sidenote styling, see the [sidenotes guide](/docs/sidenotes).

## Template System

TufteCMS uses Flask's Jinja2 templating with a clean, semantic structure.

### Template Directory

```
tuftecms/templates/
├── base.html           # Master layout template
├── post.html          # Individual content pages
├── archive.html       # Chronological content listings
├── directory.html     # File browser interface
├── sidenotes.html     # Sidenotes index
├── outlines.html      # Headings index  
├── quotes.html        # Blockquotes index
├── connections.html   # Cross-references index
├── terms.html         # Terms index
├── graph.html         # Interactive content graph
└── search.html        # Full-text search interface
```

### Base Template Structure

The `base.html` template provides the foundational layout:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title }}{% endblock %}</title>
    <!-- Meta tags, CSS, etc. -->
</head>
<body>
    <nav>
        <!-- Site navigation -->
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <!-- Site footer -->
    </footer>
</body>
</html>
```

### Content Template Variables

When customizing templates, you have access to these variables:

#### All Templates
- `title`: Page title
- `current_year`: Current year for copyright
- `index_counts`: Statistics for all content indexes

#### Content Pages (`post.html`)
- `content`: Rendered HTML content
- `metadata`: Frontmatter data
- `reading_time`: Estimated reading time in minutes
- `word_count`: Content word count  
- `tags`: List of content tags
- `unique_icon`: Custom icon for the content
- `related_posts`: Algorithm-suggested related content
- `adjacent_posts`: Previous and next in chronological order

#### Index Pages
- `articles`: Content items for the index
- `total_count`: Total items in the index
- Specific data based on index type (sidenotes, quotes, etc.)

## Styling System

TufteCMS includes Tufte-inspired CSS that you can customize or replace entirely.

### CSS Architecture

```
tuftecms/static/css/
├── tufte.css          # Core Tufte-style typography
├── layout.css         # Site layout and structure  
├── components.css     # UI components (navigation, forms)
├── syntax.css         # Code syntax highlighting
└── custom.css         # Your customizations
```

### Key Design Classes

```css
/* Content layout */
.post-content          /* Main content container */
.sidenote             /* Marginal annotations */  
.margin-toggle        /* Sidenote toggle mechanism */

/* Typography */
.subtitle             /* Subtitle styling */
.legend-dot           /* Colored dots for categorization */
.project-link         /* Internal link styling */

/* Navigation */
.pathway-box          /* Homepage pathway sections */
.footer-indexes       /* Footer navigation links */

/* Content organization */
.color-philosophy     /* Philosophy content theme */  
.color-software       /* Software content theme */
.color-ai            /* AI content theme */
.color-essay         /* Essay content theme */
```

### Color Theming

TufteCMS uses a semantic color system for content categorization:

```css
:root {
  --color-philosophy: #95a5a6;
  --color-software: #e74c3c;  
  --color-ai: #9b59b6;
  --color-essay: #3498db;
  --color-music: #f39c12;
  --color-poetry: #27ae60;
}

.project-link.color-philosophy { color: var(--color-philosophy); }
.project-link.color-software { color: var(--color-software); }
/* etc. */
```

## Custom CSS

Add your customizations to `tuftecms/static/css/custom.css`:

```css
/* Override typography */
body {
    font-family: your-preferred-font, serif;
    font-size: 1.1em;
    line-height: 1.7;
}

/* Customize sidenote appearance */
.sidenote {
    background-color: #f9f9f9;
    border-left: 3px solid #ddd;
    padding-left: 0.5em;
}

/* Add custom content themes */
.project-link.color-custom {
    color: #your-brand-color;
}

/* Modify layout constraints */
.post-content {
    max-width: 50rem; /* Adjust reading column width */
}
```

## Navigation Customization

### Header Navigation

Modify the site navigation in `base.html`:

```html
<nav class="site-navigation">
    <a href="/" class="home-link">Your Site Name</a>
    <div class="nav-links">
        <a href="/essays">Essays</a>
        <a href="/projects">Projects</a>  
        <a href="/docs">Documentation</a>
        <a href="/search">Search</a>
    </div>
</nav>
```

### Footer Indexes

Customize the footer content guides in your index template:

```html
<section class="footer-indexes">
    <h3>Navigate This Garden</h3>
    <div class="index-links">
        <a href="/sidenotes">Marginalia ({{ index_counts.sidenotes }})</a>
        <a href="/connections">Cross-References ({{ index_counts.connections_outgoing }})</a>
        <a href="/archive">Archive</a>
        <a href="/random">Random Discovery</a>
    </div>
</section>
```

### Custom Index Pages

Create new index types by adding routes and templates:

```python
# In blueprints/main.py
@main_bp.route("/custom-index")
def custom_index():
    # Your custom logic here
    return render_template("custom-index.html", data=your_data)
```

## Content Processing Customization

### Markdown Extensions

Extend markdown processing in `core/markdown.py`:

```python
import markdown
from markdown.extensions import codehilite, toc, tables

# Add custom extensions
md = markdown.Markdown(
    extensions=[
        'codehilite',
        'toc',
        'tables',
        'your_custom_extension'
    ],
    extension_configs={
        'codehilite': {'css_class': 'highlight'},
        'toc': {'anchorlink': True}
    }
)
```

### Custom Content Filters

Add Jinja2 template filters in `app.py`:

```python
@app.template_filter('your_filter')
def your_custom_filter(text):
    """Custom text processing."""
    return process_text(text)
```

### Content Metadata

Extend frontmatter processing to support custom fields:

```python
# In your content processing
def extract_metadata(frontmatter_data):
    metadata = {
        'title': frontmatter_data.get('title', ''),
        'date': frontmatter_data.get('date'),
        'your_custom_field': frontmatter_data.get('custom_field'),
        # Process custom metadata here
    }
    return metadata
```

## Brand Integration

### Logo and Identity

Replace the site title with your logo in `base.html`:

```html
<div class="site-header">
    <img src="/static/images/logo.svg" alt="Your Site" class="site-logo">
    <h1 class="site-title">Your Digital Garden</h1>
</div>
```

### Custom Fonts

Add web fonts in your base template:

```html
<head>
    <!-- Google Fonts example -->
    <link href="https://fonts.googleapis.com/css2?family=Your+Font:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Or self-hosted fonts -->
    <link href="/static/fonts/your-font.css" rel="stylesheet">
</head>
```

```css
/* Apply in your CSS */
body {
    font-family: 'Your Font', Georgia, serif;
}

.sidenote {
    font-family: 'Your Sans Font', 'Helvetica Neue', sans-serif;
}
```

### Color Scheme

Define your brand colors:

```css
:root {
    --primary-color: #your-primary;
    --secondary-color: #your-secondary;
    --accent-color: #your-accent;
    --text-color: #your-text;
    --background-color: #your-background;
    --border-color: #your-border;
}

/* Apply throughout your styles */
.project-link { color: var(--accent-color); }
.sidenote { border-color: var(--border-color); }
```

## Content Organization

### Custom Content Types

Create new content categories by adding directories and customizing templates:

```
data/
├── essays/           # Existing
├── projects/         # Existing  
├── reviews/          # New: Book/film reviews
├── tutorials/        # New: Technical guides
└── experiments/      # New: Work-in-progress ideas
```

Add routing logic in `blueprints/content.py` for custom handling:

```python
# Special handling for new content types
if path.startswith("reviews/"):
    # Custom processing for reviews
    return render_review_template(content_data)
elif path.startswith("experiments/"):  
    # Different template for experimental content
    return render_experiment_template(content_data)
```

### Custom Metadata Fields

Extend frontmatter for specific content types:

```yaml
---
title: "Book Review: Consciousness Explained"
type: "review"
reviewed_item: "Consciousness Explained by Daniel Dennett"
rating: 4
review_date: 2025-01-15
tags: [consciousness, philosophy, books]
---
```

Process in templates:

```html
{% if metadata.type == 'review' %}
    <div class="review-metadata">
        <h2>{{ metadata.reviewed_item }}</h2>
        <div class="rating">Rating: {{ metadata.rating }}/5</div>
    </div>
{% endif %}
```

## Advanced Customization

### Custom Caching

Extend the caching system for your content types:

```python
# In core/cache.py
@lru_cache(maxsize=1)
def get_custom_cache():
    """Cache your custom content analysis."""
    # Your caching logic
    return processed_data
```

### Search Integration

Customize search behavior in your templates and JavaScript:

```javascript
// Custom search filtering
function filterResults(results, contentType) {
    if (contentType === 'essays') {
        return results.filter(r => r.path.includes('/essays/'));
    }
    return results;
}
```

### Analytics and Insights

Add custom analytics while respecting privacy:

```html
<!-- Privacy-respecting analytics -->
<script>
    // Your analytics code here
    // Consider: Plausible, Simple Analytics, or self-hosted solutions
</script>
```

## Performance Optimization

### Static Asset Optimization

```python
# In app.py - add asset versioning
@app.template_filter('asset_version')
def asset_version(filename):
    """Add version hash to asset URLs."""
    # Your versioning logic
    return f"{filename}?v={get_file_hash(filename)}"
```

### Caching Headers

Customize caching behavior in `blueprints/content.py`:

```python
# Custom cache headers for different content types
if file_path.suffix == '.md':
    # Shorter cache for dynamic content
    response.headers['Cache-Control'] = 'public, max-age=3600'
elif file_path.suffix in ['.jpg', '.png', '.svg']:
    # Longer cache for images  
    response.headers['Cache-Control'] = 'public, max-age=604800'
```

## Next Steps

With your customized TufteCMS site:

- **Structure your content** - Apply customizations to well-organized content using the [content structure guide](/docs/content-structure) 
- **Master sidenotes** - Style the [sidenotes system](/docs/sidenotes) to match your visual identity
- **Deploy to production** - Launch your customized site with the [deployment guide](/docs/deployment)
- **Continue exploring** - Return to the [documentation index](/docs) for advanced topics

---

*Remember: Customization should serve your content, not overshadow it. The best modifications enhance readability and discovery while maintaining the contemplative focus that makes your digital garden a place worth visiting.*
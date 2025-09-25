# Content Structure

*Organizing your markdown files for maximum discoverability*

TufteCMS transforms your directory structure into URL routes while providing intelligent content organization and cross-referencing capabilities.

> This guide assumes you've completed the [getting started](/docs/getting-started) setup. For template customization, see the [customization guide](/docs/customization).

## URL Mapping

TufteCMS follows a simple pattern: filesystem paths become URL paths.

```
data/index.md                → /
data/essays/index.md          → /essays
data/essays/hello-world.md    → /essays/hello-world
data/docs/getting-started.md → /docs/getting-started
data/projects/tuftecms.md    → /projects/tuftecms
```

## Recommended Structure

```
data/
├── index.md              # Homepage - your digital garden entrance
├── essays/               # Long-form contemplative writing
│   ├── index.md         # Essays collection page
│   ├── 2025-01-01-programming-as-practice.md
│   ├── 2025-01-15-consciousness-and-code.md
│   └── 2025-02-01-recursive-thinking.md
├── notes/               # Shorter observations and thoughts  
│   ├── index.md         # Notes collection page
│   ├── daily-reflections.md
│   └── reading-responses.md
├── projects/            # Work portfolio and case studies
│   ├── index.md         # Projects overview
│   ├── tuftecms.md     # Individual project pages
│   └── requests-library.md
├── docs/               # Framework documentation
│   ├── index.md
│   ├── getting-started.md
│   └── customization.md
└── static/            # Images, assets, downloads
    ├── images/
    ├── css/
    └── downloads/
```

## File Naming Conventions

### Date-based Posts

For chronological content like essays or blog posts:

```
YYYY-MM-DD-slug.md

Examples:
2025-01-15-python-as-english.md
2025-02-01-consciousness-research.md
2025-03-10-recursive-loops.md
```

The date in the filename is used for:
- Automatic chronological sorting
- Archive organization  
- Publishing date extraction
- URL generation (optional)

### Topic-based Pages

For reference material or evergreen content:

```
descriptive-slug.md

Examples:
getting-started.md
sidenotes-guide.md
customization.md
api-reference.md
```

### Index Pages

Each directory should have an `index.md` that serves as:
- Collection overview
- Navigation hub
- Context setting for the section

```markdown
# Essays

*Explorations of consciousness, technology, and human flourishing*

This collection documents my journey exploring how technology can serve human consciousness rather than exploit it.

## Recent Essays

[The content system automatically shows recent posts here]

## Themes

- **Programming as Practice** - Code as contemplative discipline
- **AI Consciousness** - Collaborative thinking with digital minds  
- **Algorithmic Critique** - How optimization consumes human values
```

## Automatic Metadata Extraction

TufteCMS intelligently extracts metadata from your content structure:

### Title Extraction

```markdown
# Programming as Spiritual Practice

Content starts here...
```

**Title Sources (in priority order):**
1. First H1 heading (`# Title`)
2. Filename converted to title case (`programming-as-practice.md` → "Programming as Practice")

### Date Extraction

**Filename patterns:**
```
2025-01-15-programming-as-practice.md  → January 15, 2025
2025-02-consciousness-research.md      → February 2025  
programming-basics.md                  → No date (evergreen)
```

**Italic date patterns in content:**
```markdown
# My Essay

*January 2025*

Content here...
```

### Automatic Content Analysis

TufteCMS automatically calculates:

- **Word count** - From rendered content
- **Reading time** - Estimated at ~200 words per minute  
- **Cross-references** - Internal links between pages
- **Sidenotes extraction** - Marginal annotations for indexing
- **Quotes extraction** - Blockquotes for the quotes index
- **Terms extraction** - Key concepts for the terms index
- **Outline extraction** - Heading structure for navigation

## Content Types

### Essays

Long-form contemplative writing exploring ideas in depth:

```
data/essays/
├── index.md
├── 2025-01-01-introduction.md
├── 2025-01-15-deep-exploration.md
└── 2025-02-01-synthesis.md
```

Characteristics:
- 2000-5000 words typically
- Rich with sidenotes for depth
- Extensive cross-referencing
- Philosophical or technical insights

### Notes

Shorter observations, responses, daily thoughts:

```
data/notes/
├── index.md  
├── daily-observations.md
├── book-responses.md
└── quick-insights.md
```

Characteristics:
- 200-1000 words typically
- More immediate, less polished
- Quick capture of insights
- Links to related essays

### Projects

Portfolio items, case studies, software documentation:

```
data/projects/
├── index.md
├── tuftecms.md
├── requests-library.md
└── consciousness-research.md
```

Characteristics:
- Technical documentation
- Process narratives  
- Impact analysis
- Links to code/demos

### Documentation

Framework guides, tutorials, reference material:

```
data/docs/
├── index.md
├── getting-started.md
├── content-structure.md
└── deployment.md
```

Characteristics:
- Step-by-step instructions
- Code examples
- Reference information
- Troubleshooting guides

## Cross-Reference Strategy

### Internal Linking

Link between content using clean URLs:

```markdown
This builds on ideas from [Programming as Practice](/essays/programming-as-practice).

See the [complete documentation](/docs) for technical details.

Related thoughts in my [daily notes](/notes/recursive-thinking).
```

### Contextual References

Add context to links for better understanding:

```markdown
The concept of [recursive loops in consciousness](/essays/recursive-loops) appears throughout this work.

As I explored in [the algorithm eats series](/essays/algorithm-eats-virtue), optimization creates destructive feedback cycles.
```

### Backlink Integration

TufteCMS automatically tracks incoming references and can surface them in templates. Consider how each piece fits into the larger web of ideas.

## Content Flow Patterns

### Idea Development

1. **Capture** in notes (quick, unpolished)  
2. **Develop** in essays (deep exploration)
3. **Apply** in projects (practical implementation)
4. **Document** in docs (systematic explanation)

### Cross-Pollination

- Essays reference practical projects
- Projects link back to philosophical foundations  
- Notes capture responses to both
- Documentation ties everything together

### Temporal Organization

- **Archive view**: Chronological browsing
- **Topic view**: Thematic clustering
- **Connection view**: Relationship mapping
- **Random view**: Serendipitous discovery

## Growth Strategies

### Start Small

Begin with a few well-crafted pieces:
- Homepage introduction
- 2-3 essays exploring core themes
- Basic project documentation
- Simple about/contact pages

### Expand Systematically

Add content in coherent clusters:
- Complete a series before starting another
- Build out documentation as you develop ideas
- Let cross-references emerge organically
- Maintain consistent voice and quality

### Optimize for Discovery

- Rich internal linking between related ideas
- Meaningful file names and URLs
- Strategic use of sidenotes for depth
- Clear title structure with H1 headings

## Next Steps

With your content well-organized:

- **Add depth with [sidenotes](/docs/sidenotes)** - Learn TufteCMS's signature marginal annotations
- **Customize your templates** - Follow the [customization guide](/docs/customization) to reflect your unique style  
- **Deploy your site** - Use the [deployment guide](/docs/deployment) for production hosting
- **Explore advanced features** - Return to the [documentation index](/docs) for specialized topics

---

*Remember: The goal isn't volume but coherence. Every piece should contribute to a larger understanding, with connections that help readers navigate between ideas naturally.*
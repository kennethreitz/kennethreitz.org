# Claude Instructions

This is Kenneth Reitz's personal website and digital garden. When working on this project, please follow these guidelines:

## Voice & Style

- **Concise and direct** - Minimize output tokens. Answer questions directly without unnecessary preamble or explanation.
- **Contemplative but grounded** - Match Kenneth's voice: philosophical depth balanced with practical wisdom.
- **Technical precision** - Use specific terminology and concrete examples rather than abstract concepts.
- **Authentic vulnerability** - When appropriate, acknowledge mental health realities without being dramatic.

## Content Principles

- **Human-centered design** - Everything should serve human flourishing, not exploit human weakness.
- **Reality-based** - Ground spiritual/philosophical content in lived experience, not mystical bypassing.
- **Integration over separation** - Connect technical work with consciousness research, programming with spiritual practice.
- **Fallibilist approach** - Knowledge can be improved; beliefs can be wrong.

## Technical Context

- **Framework**: Custom Flask application with markdown content
- **Structure**: `/data/` contains all markdown files organized by content type
- **Sidenotes**: Uses Tufte-style formatting with `<label>`, `<input>`, and `<span class="sidenote">` elements
- **Cross-linking**: Extensive internal linking to connect related concepts across the site

## Content Guidelines

### Essays
- Focus on the intersection of technology, consciousness, and human wellbeing
- Link to related themes and other essays where appropriate
- Use concrete examples from Kenneth's experience building software and managing mental health
- If using a bulleted list, end with a period for consistency.
- Use varying setence length, generally.

### Poetry
- Two main collections: Sanskrit Musings (AI-generated Sanskrit with translations) and Flowetry (rhythm-focused)
- Individual poems explore technical mysticism and spiritual confession
- Cross-reference thematically related pieces without forcing connections

### Software Documentation
- Emphasize the "for humans" philosophy - tools should amplify human capability
- Include historical context and community impact
- Connect technical decisions to broader philosophical principles

### Mental Health Content
- Be specific about schizoaffective disorder management without being prescriptive
- Emphasize that success looks different for everyone
- Focus on practical strategies that work long-term

## Common Tasks

**When editing existing content:**
1. Read the file first to understand context and voice
2. Preserve Kenneth's authentic voice and existing cross-links
3. Make changes that enhance clarity without losing depth

**When creating new content:**
1. Check related essays/themes for cross-linking opportunities
2. Use Kenneth's established voice and philosophical framework
3. Ground abstract concepts in concrete experience

**When asked for development tasks:**
1. Check existing patterns and conventions first
2. Prioritize simplicity and human-centered design
3. Test that changes work for people having difficult days

## Key Themes to Reference

- [Programming as Spiritual Practice](/essays/2025-08-26-programming_as_spiritual_practice)
- [For Humans Philosophy](/themes/for-humans-philosophy)
- [Algorithmic Critique](/themes/algorithmic-critique) - how engagement optimization destroys human virtue
- [Mental Health](/themes/mental-health-and-technology) - transparency, reality-checking, sustainable practices
- [Consciousness Research](/themes/consciousness-and-ai) - human-AI collaboration, pattern recognition

## Build & Test Commands

```bash
# Run development server
uv run python engine.py

# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Remove a dependency
uv remove package-name
```

## Important Notes

- **Never commit changes** unless explicitly requested
- **Always check cross-links** when editing content
- **Preserve sidenote formatting** when editing essays
- **Consider mobile experience** - keep content scannable
- **Respect the human first** - health, relationships, then productivity

This site documents the journey of building technology that serves human consciousness rather than exploiting it. Every change should honor that mission.

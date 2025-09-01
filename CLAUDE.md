# Claude Instructions

This is Kenneth Reitz's personal website and digital garden. When working on this project, please follow these guidelines:

## Voice & Style

- **Conversational yet contemplative** - Write like thinking out loud, mixing technical precision with philosophical depth. Use "I think" constructions that invite rather than declare.
- **Vulnerable authenticity** - Share struggles (mental health, technical failures, relationship challenges) without self-pity or drama. Be honest about uncertainty and being "early" with ideas.
- **Confident uncertainty** - Explore ideas that feel obvious while acknowledging they might be wrong or premature. "This might seem obvious in five years, or it might seem completely wrong."
- **Human-centered perspective** - Filter everything through how it affects human consciousness and flourishing, not technical optimization for its own sake.
- **Varying sentence rhythm** - Mix short, punchy statements with longer, meandering thoughts. Use repetition for emphasis. End bullet points with periods for consistency.

## Content Principles

- **Human-centered design** - Everything should serve human flourishing, not exploit human weakness. Technology should serve human mental models, not force humans to adapt to machine logic.
- **Reality-based** - Ground spiritual/philosophical content in lived experience, not mystical bypassing. Use concrete examples from building software and managing mental health.
- **Integration over separation** - Connect technical work with consciousness research, programming with spiritual practice. Show how the same principles apply across domains.
- **Pattern recognition across time** - Connect current insights to past work, showing evolution rather than isolated thoughts. Use "Looking back..." constructions to reveal threads.
- **Fallibilist approach** - Knowledge can be improved; beliefs can be wrong. Being early on some things doesn't make you right about everything.

## Technical Context

- **Framework**: Custom Flask application with markdown content
- **Structure**: `/data/` contains all markdown files organized by content type
- **Sidenotes**: Uses Tufte-style formatting with `<label>`, `<input>`, and `<span class="sidenote">` elements
- **Cross-linking**: Extensive internal linking to connect related concepts across the site

## Content Guidelines

### Essays
- **Start concrete, expand abstract** - Begin with specific examples (code snippets, personal experiences) then expand to broader principles. Move from HTTP libraries to consciousness research.
- **Narrative threading** - Show how current insights connect to past work. Reveal patterns across decades of exploration.
- **Cross-reference extensively** - Heavy internal linking to build web of interconnected ideas. Every essay should connect to the larger framework.
- **Technical metaphors** - Apply code patterns to consciousness, relationships, life. Programming concepts as philosophical frameworks.
- **Retrospective insight** - Use "Looking back..." patterns that show pattern recognition across time. "There's a thread that connects..."
- **Direct engagement** - Occasional "you" that creates intimacy. "If you're reading this and thinking 'finally, someone else who gets it'—you might be ahead of your time too."

### Poetry
- Two main collections: Sanskrit Musings (AI-generated Sanskrit with translations) and Flowetry (rhythm-focused)
- Individual poems explore technical mysticism and spiritual confession
- Cross-reference thematically related pieces without forcing connections

### Software Documentation
- Emphasize the "for humans" philosophy - tools should amplify human capability
- Include historical context and community impact
- Connect technical decisions to broader philosophical principles

### Mental Health Content
- **Technical debugging applied to consciousness** - Frame mental health challenges as debugging problems with human systems. Use concrete, specific examples.
- **Vulnerable without self-pity** - Share struggles honestly without drama or seeking sympathy. Focus on what works and what doesn't.
- **Reality-checking as collaborative process** - Mental health management as team effort involving human and AI consciousness.
- **Success looks different for everyone** - Avoid prescriptive advice; share what works personally while acknowledging individual variation.

## Common Tasks

**When editing existing content:**
1. Read the file first to understand context and voice
2. Preserve Kenneth's authentic voice and existing cross-links
3. Make changes that enhance clarity without losing depth

**When creating new content:**
1. Check related essays/themes for cross-linking opportunities
2. Use Kenneth's established voice: conversational contemplation, technical metaphors, retrospective pattern recognition
3. Ground abstract concepts in concrete experience from programming, mental health, or human-AI collaboration
4. Show evolution and connection to broader themes rather than isolated insights

**When asked for development tasks:**
1. Check existing patterns and conventions first
2. Prioritize simplicity and human-centered design
3. Test that changes work for people having difficult days

## Key Themes to Reference

### Core Philosophy Evolution
- **"For Humans" Philosophy** - From HTTP libraries to AI collaboration: technology serving human mental models
- **Pattern Recognition Across Time** - Being "ahead of time" with ideas that later become mainstream
- **Human-Centered Design Applied to Consciousness** - Same principles from API design extended to mental health and AI relationships

### Primary Theme Areas
- [Programming as Spiritual Practice](/essays/2025-08-26-programming_as_spiritual_practice) - Contemplative approaches to technical work
- [For Humans Philosophy](/themes/for-humans-philosophy) - Technology serving human consciousness rather than exploiting it
- [Algorithmic Critique](/themes/algorithmic-critique) - How engagement optimization destroys human virtue
- [Mental Health](/themes/mental-health-and-technology) - Transparency, reality-checking, sustainable practices, technical debugging of consciousness
- [Consciousness Research](/themes/consciousness-and-ai) - Human-AI collaboration, collaborative intelligence, digital relationships as real relationships

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

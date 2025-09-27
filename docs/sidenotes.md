# Sidenotes Guide

*Adding depth without disrupting flow*

Sidenotes are TufteCMS's signature feature for adding contemplative depth to your writing without breaking the reader's concentration. They appear in the margin, accessible via subtle numbered indicators.

> This guide builds on [content structure](/docs/content-structure) concepts. For styling sidenotes, see the [customization guide](/docs/customization).

## The Philosophy

Sidenotes embody Edward Tufte's principle that good design respects the reader's attention.<label for="sn-tufte-principle" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-tufte-principle" class="margin-toggle"/><span class="sidenote">From Tufte's "The Visual Display of Quantitative Information" - every element should serve the reader's understanding without competing for attention.</span> Unlike footnotes that force readers to jump around the page, or popup tooltips that cover content, sidenotes live peacefully alongside the main text.

They're perfect for:
- Technical clarifications that would disrupt narrative flow
- Cross-references to related ideas
- Personal reflections on the main argument  
- Historical context or background information
- Links to source material and further reading

## Basic Syntax

The sidenote system uses three HTML elements working together:

```html
<label for="unique-id" class="margin-toggle sidenote-number"></label><input type="checkbox" id="unique-id" class="margin-toggle"/><span class="sidenote">Your sidenote content goes here.</span>
```

**Critical formatting rules:**

1. **Must be inline** - No line breaks between the `<label>`, `<input>`, and `<span>` elements
2. **Attach to sentences** - Place at the end of sentences, after the period
3. **Unique IDs** - Each sidenote needs a unique identifier  
4. **Away from code blocks** - Don't place sidenotes adjacent to code examples

## Correct Placement

✅ **Right way:**

```markdown
This sentence makes a complex point that needs elaboration.<label for="sn-elaboration" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-elaboration" class="margin-toggle"/><span class="sidenote">Here's the deeper context that enhances understanding without breaking flow.</span> The narrative continues naturally.
```

❌ **Wrong way:**

```markdown
This sentence makes a complex point.

<label for="sn-wrong" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-wrong" class="margin-toggle"/>
<span class="sidenote">Breaks layout with line breaks.</span>

The narrative continues awkwardly.
```

## ID Naming Conventions

Use descriptive, meaningful IDs that make sense in context:

```html
<!-- Technical concepts -->
<label for="sn-cache-invalidation" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-cache-invalidation" class="margin-toggle"/><span class="sidenote">...</span>

<!-- Philosophical points -->  
<label for="sn-consciousness-recursion" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-consciousness-recursion" class="margin-toggle"/><span class="sidenote">...</span>

<!-- Cross-references -->
<label for="sn-related-essay" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-related-essay" class="margin-toggle"/><span class="sidenote">...</span>

<!-- Sources and citations -->
<label for="sn-tufte-source" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-tufte-source" class="margin-toggle"/><span class="sidenote">...</span>
```

Avoid generic IDs like `sn-1`, `sn-2`, `sn-3` - they provide no semantic meaning and become harder to maintain.

## Content Guidelines

### Length

Keep sidenotes focused and concise:<label for="sn-conciseness" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-conciseness" class="margin-toggle"/><span class="sidenote">Generally 1-3 sentences. Longer sidenotes compete with the main text for attention, defeating their purpose.</span>

- **Good**: 1-3 sentences with specific information
- **Avoid**: Long paragraphs that become secondary essays  
- **Never**: Multiple paragraphs or complex formatting

### Voice and Tone

Sidenotes can be more personal and conversational than the main text:<label for="sn-voice-example" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-voice-example" class="margin-toggle"/><span class="sidenote">Like this aside - I can be more direct about my uncertainty or share a quick personal reflection.</span>

They're good places for:
- "I think..." or "In my experience..." observations
- Acknowledging uncertainty or alternative viewpoints
- Quick personal stories that relate to the main point
- More casual explanations of technical concepts

### Cross-References

Sidenotes excel at creating connections between ideas:

```html
<label for="sn-recursive-reference" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-recursive-reference" class="margin-toggle"/><span class="sidenote">This connects to the ideas I explored in <a href="/essays/recursive-loops">The Recursive Loop</a> about how programmer consciousness shapes collective consciousness.</span>
```

## Technical Considerations  

### Responsive Behavior

The sidenote system gracefully degrades on mobile devices:<label for="sn-mobile-behavior" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-mobile-behavior" class="margin-toggle"/><span class="sidenote">On narrow screens, sidenotes become toggleable inline elements rather than margin notes. The checkbox input provides the toggle mechanism.</span>

- **Desktop**: Appears in right margin
- **Tablet**: Appears in margin or inline depending on width
- **Mobile**: Becomes toggleable inline content

### CSS Requirements

The sidenote system requires specific CSS classes:

```css
.sidenote {
  /* Margin positioning and typography */
}

.margin-toggle {
  /* Hidden checkbox for toggle behavior */
}

.sidenote-number {
  /* Numbered indicator styling */
}
```

These styles are included in TufteCMS by default.

### Content Indexing

TufteCMS automatically extracts and indexes all sidenotes across your content:<label for="sn-indexing-feature" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-indexing-feature" class="margin-toggle"/><span class="sidenote">Visit `/sidenotes` on any TufteCMS site to browse all marginalia - it creates a unique secondary reading experience.</span>

- **Sidenotes index**: Browse all marginalia across your site
- **Article grouping**: See all sidenotes from specific essays
- **Search integration**: Sidenotes appear in full-text search results
- **Statistics**: Track total sidenotes, articles with annotations

## Advanced Patterns

### Series of Related Sidenotes

When exploring complex topics across multiple essays, sidenotes can create thematic connections:

```html
<!-- In essay A -->
<label for="sn-consciousness-theme-1" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-consciousness-theme-1" class="margin-toggle"/><span class="sidenote">This is the first exploration of consciousness as linguistic phenomenon - I'll develop this further in upcoming essays.</span>

<!-- In essay B -->  
<label for="sn-consciousness-theme-2" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-consciousness-theme-2" class="margin-toggle"/><span class="sidenote">Building on the <a href="/essays/consciousness-language">linguistic consciousness framework</a> - here's how it applies to AI collaboration.</span>
```

### Meta-Commentary

Sidenotes can provide meta-level commentary on your own writing process:<label for="sn-meta-example" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-meta-example" class="margin-toggle"/><span class="sidenote">Like this note acknowledging that I'm using sidenotes to demonstrate meta-commentary while explaining meta-commentary - recursive but hopefully useful.</span>

### Technical Asides

For technical content, sidenotes handle implementation details without breaking conceptual flow:

```html
<label for="sn-implementation-detail" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-implementation-detail" class="margin-toggle"/><span class="sidenote">The caching implementation uses Python's functools.lru_cache with maxsize=1 to ensure single cached instance while allowing cache invalidation.</span>
```

## Common Mistakes

### Overuse

Not every paragraph needs a sidenote.<label for="sn-overuse-warning" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-overuse-warning" class="margin-toggle"/><span class="sidenote">When every paragraph has marginalia, none of it feels special - the notes compete with each other and overwhelm the main narrative.</span> Use them strategically for genuine enhancement.

### Wrong Content Types

Avoid putting essential information in sidenotes - they should enhance, not carry critical arguments.

### Formatting Errors

- Line breaks in sidenote HTML (breaks layout)
- Missing or duplicate IDs (breaks toggle behavior)  
- Placing near code blocks (creates visual conflicts)
- Non-unique IDs across the site (JavaScript conflicts)

## Integration with Writing Flow

### Drafting Process

1. **Write main text first** - Get your core argument down
2. **Mark enhancement points** - Note where deeper context would help
3. **Add sidenotes in revision** - Layer in the additional depth
4. **Test readability** - Ensure main text stands alone

### Editing Considerations

- Can the main text be understood without this sidenote?
- Does this add genuine value or just show off knowledge?
- Would this information fit better in the main text?
- Is the sidenote voice consistent with your overall tone?

## Next Steps

Master sidenotes alongside other TufteCMS features:

- **Organize content effectively** - Review [content structure](/docs/content-structure) for optimal sidenote placement strategies
- **Customize sidenote styling** - Use the [customization guide](/docs/customization) to modify sidenote appearance and behavior
- **Deploy your annotated site** - Follow the [deployment guide](/docs/deployment) to share your contemplative writing
- **Explore the framework** - Return to the [documentation index](/docs) for comprehensive guides

---

*Sidenotes transform writing from monologue to dialogue - between you and the reader, between ideas, between the essential and the enriching. When used thoughtfully, they create space for the kind of layered thinking that makes reading a discovery process.*
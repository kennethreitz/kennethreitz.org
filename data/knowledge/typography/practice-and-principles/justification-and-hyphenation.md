---
description: A justified column is a promise of evenness that only good line breaking
  can keep.
source: obsidian-knowledge
---

# Justification and Hyphenation

> *A justified column is a promise of evenness that only good line breaking can keep.*

---

## Alignment

Text can be set *justified* (flush to both margins), *flush left* (ragged right), *flush right*, or *centered*. Justified text has been the norm in books since [Johannes Gutenberg](/knowledge/typography/type-designers/johannes-gutenberg),[^sn-johannes-gutenberg] whose perfectly even columns relied on [ligatures](/knowledge/typography/anatomy/ligature), abbreviations, and [Hanging Punctuation](/knowledge/typography/practice-and-principles/hanging-punctuation). Flush left, ragged right became a modernist preference (see [Swiss International Style](/knowledge/typography/history/swiss-international-style)) because it keeps word spacing perfectly even.

## The Cost of Justification

To make every line the same length, justification varies word spacing. With a short [Measure](/knowledge/typography/anatomy/measure) or poor line breaking, this creates loose lines with big gaps, and gaps that line up vertically create *rivers* of white running down the paragraph. The cure is hyphenation, to break long words, and smarter line breaking.

## The Knuth-Plass Algorithm

Most software historically broke lines greedily, one at a time. [Donald Knuth](/knowledge/typography/type-designers/donald-knuth) and Michael Plass, in work published in 1981 and built into TeX, instead consider the whole paragraph, choosing the set of breaks that minimizes total badness, with penalties for hyphens, consecutive hyphenated lines, and very loose or tight lines. Adobe InDesign's paragraph composer applies a similar idea (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex) and [Microtypography](/knowledge/typography/practice-and-principles/microtypography)).

## On the Web

Browsers break lines greedily, which is why justified web text often looks gappy. Use justification on the web only with `hyphens: auto`, a correct `lang` attribute, and a comfortable measure. The Reitz LaTeX theme justifies and hyphenates its reading view while keeping the writing view ragged, so text never shifts under the cursor (see [Draft to Document Why I Made My Notes Look Like LaTeX Papers](/essays/2026-11-04-draft_to_document)).

## Related

- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Widows and Orphans](/knowledge/typography/practice-and-principles/widows-and-orphans)
- [Measure](/knowledge/typography/anatomy/measure)
- [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)
- [Hanging Punctuation](/knowledge/typography/practice-and-principles/hanging-punctuation)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-johannes-gutenberg]: Johannes Gutenberg was a goldsmith of Mainz who, around the 1440s and early 1450s, developed a complete system for printing with movable metal type (see Movable Type).

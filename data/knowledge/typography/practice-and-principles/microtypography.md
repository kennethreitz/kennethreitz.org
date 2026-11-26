---
description: The best typography happens at a scale the reader never consciously sees.
source: obsidian-knowledge
---

# Microtypography

> *The best typography happens at a scale the reader never consciously sees.*

---

## The Small Scale

Macrotypography is the layout of the page: grid, hierarchy, columns. Microtypography is the fine texture inside it: letter spacing, word spacing, [Kerning](/knowledge/typography/anatomy/kerning), line breaking, punctuation spacing, [Hanging Punctuation](/knowledge/typography/practice-and-principles/hanging-punctuation), [ligatures](/knowledge/typography/anatomy/ligature),[^sn-ligature] and the subtle adjustments that make a column of text look even.

## Protrusion and Expansion

Two techniques define modern microtypography. *Character protrusion* (margin kerning) lets punctuation and certain letters hang slightly into the margin, so that the text edge looks straight to the eye rather than to the ruler. *Font expansion* stretches or squeezes letters imperceptibly, by a percent or two, to help justified lines fit without big gaps between words.

[Hermann Zapf](/knowledge/typography/type-designers/hermann-zapf)'s hz-program, developed with URW in the early 1990s, explored these ideas commercially, and they influenced Adobe InDesign. Hàn Thế Thành implemented protrusion and expansion in pdfTeX for his doctoral thesis around 2000, and the LaTeX `microtype` package made them available to everyone who uses TeX (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)).

## On the Web

Browsers offer only partial tools: kerning, ligatures and other [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features), `hyphens: auto`, and newer line breaking controls like `text-wrap: pretty`, which avoids stranding a single short word on the last line. The Reitz LaTeX theme approximates microtypography as far as Chromium allows (see [Draft to Document Why I Made My Notes Look Like LaTeX Papers](/essays/2026-11-04-draft_to_document)).

## Related

- [Kerning](/knowledge/typography/anatomy/kerning)
- [Hanging Punctuation](/knowledge/typography/practice-and-principles/hanging-punctuation)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Widows and Orphans](/knowledge/typography/practice-and-principles/widows-and-orphans)
- [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-ligature]: A ligature is a single Glyph that combines two or more letters.

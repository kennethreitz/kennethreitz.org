---
description: A straight margin is an optical fact, not a measured one.
source: obsidian-knowledge
---

# Hanging Punctuation

> *A straight margin is an optical fact, not a measured one.*

---

## The Idea

When a line begins with a quotation mark or ends with a period, comma, or hyphen, the small mark creates a visible dent in the text edge, because it has less visual weight than a full letter. Hanging punctuation moves those marks partly or fully into the margin, so that the letters themselves align and the edge looks straight to the eye.

## History

The practice is old. [Johannes Gutenberg](/knowledge/typography/type-designers/johannes-gutenberg)'s 42-line Bible hangs hyphens and some punctuation into the margin, contributing to its famously even columns. It faded with mechanical typesetting and has returned with digital tools as part of [Microtypography](/knowledge/typography/practice-and-principles/microtypography).[^sn-microtypography]

## Tools

InDesign calls it optical margin alignment; LaTeX's `microtype` package calls it protrusion. CSS defines a `hanging-punctuation` property, but browser support has been limited, so web designers often fake it for opening quotation marks with a negative indent. Bringhurst recommends hanging quotation marks in display type especially (see [The Elements of Typographic Style](/knowledge/typography/key-texts/the-elements-of-typographic-style)).

## In Practice

Hang opening quotes on pull quotes and block quotes, hang bullets in lists so the text aligns, and let hyphens and periods protrude slightly in justified text.

## Related

- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Quotes and Dashes](/knowledge/typography/practice-and-principles/quotes-and-dashes)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Johannes Gutenberg](/knowledge/typography/type-designers/johannes-gutenberg)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-microtypography]: Microtypography is the fine texture inside it: letter spacing, word spacing, Kerning, line breaking, punctuation spacing, Hanging Punctuation, ligatures, and the subtle adjustments that make a column of text look even.

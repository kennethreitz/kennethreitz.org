---
description: A single line, stranded at the top of a page, looks like it missed the
  bus.
source: obsidian-knowledge
---

# Widows and Orphans

> *A single line, stranded at the top of a page, looks like it missed the bus.*

---

## The Terms

The words are used inconsistently, but the most common convention, the one Bringhurst uses, is:

| Term | Meaning |
|---|---|
| Orphan | The first line of a paragraph left alone at the bottom of a page or column |
| Widow | The last line of a paragraph carried alone to the top of the next page or column |
| Runt | A single short word left alone on the last line of a paragraph |

A mnemonic: an orphan has no past, a widow has no future. Some style guides reverse the terms, and many people use "widow" for the short last line.

## Why They Matter

Stray lines break the visual unity of the text block and of the page spread. They make the reader's eye stumble at the page break, and they leave awkward white gaps. Fixing them is part of the quiet care that [Microtypography](/knowledge/typography/practice-and-principles/microtypography)[^sn-microtypography] and [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation) describe.

## Fixing Them

In print, fix them by rewriting a little, adjusting spacing within a few lines, or letting a spread run a line long or short. TeX has penalties that discourage them automatically (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)). On the web, CSS offers `widows` and `orphans` for paged media and `text-wrap: pretty` or `balance` to avoid runts in paragraphs and headings.

## Related

- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Vertical Rhythm](/knowledge/typography/practice-and-principles/vertical-rhythm)
- [The Elements of Typographic Style](/knowledge/typography/key-texts/the-elements-of-typographic-style)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-microtypography]: Microtypography is the fine texture inside it: letter spacing, word spacing, Kerning, line breaking, punctuation spacing, Hanging Punctuation, ligatures, and the subtle adjustments that make a column of text look even.

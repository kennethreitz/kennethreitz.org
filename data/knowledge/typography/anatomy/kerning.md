---
description: Even spacing is an illusion that has to be built letter by letter.
source: obsidian-knowledge
---

# Kerning

> *Even spacing is an illusion that has to be built letter by letter.*

---

## Pairs

Kerning is the adjustment of space between particular pairs of letters so that the overall spacing looks even. Letters have fixed side spaces, called sidebearings, but some combinations leave awkward holes: **AV**, **To**, **Wa**, **LT**, **r.**. A kerning pair tells the renderer to pull those two closer (or occasionally push them apart).

## From Metal to Data

In metal type, a *kern* was literally a part of a letter that overhung the body of its sort, like the tail of an italic **f**, so it could tuck over its neighbor. Fine printers also filed down sorts by hand to close bad gaps. In digital fonts, kerning is stored as data, as a table of pairs and classes, and modern fonts can contain thousands of pairs (see [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)).

*Metric* kerning uses the pairs the type designer built. *Optical* kerning, offered by layout programs, ignores those pairs and computes spacing from the letter shapes; it can rescue a poorly spaced font and can also damage a well spaced one.

## Kerning and Tracking

Kerning adjusts single pairs; [Tracking](/knowledge/typography/anatomy/tracking) adjusts the spacing of a whole run of text. The two work together: large display type usually needs tighter tracking and hand kerning, while body text should be left alone to the designer's spacing. Bringhurst's rule (see [The Elements of Typographic Style](/knowledge/typography/key-texts/the-elements-of-typographic-style))[^sn-the-elements-of-typographic-style] is to kern consistently and modestly, or not at all.

## In Practice

Always enable kerning in body text (on the web, `font-kerning: normal` is the default in most browsers). Hand-kern headlines, logos, and large capitals, and watch the spaces around punctuation, quotation marks, and [Figures](/knowledge/typography/practice-and-principles/figures),[^sn-figures] which most fonts handle worst.

## Related

- [Tracking](/knowledge/typography/anatomy/tracking)
- [Counter](/knowledge/typography/anatomy/counter)
- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)
- [Glyph](/knowledge/typography/anatomy/glyph)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-the-elements-of-typographic-style]: Robert Bringhurst's *The Elements of Typographic Style* is the most widely admired modern guide to typography.

[^sn-figures]: Old-style figures were the norm in book typography for centuries and suit Old-Style text faces like Garamond, Caslon, and ET Book.

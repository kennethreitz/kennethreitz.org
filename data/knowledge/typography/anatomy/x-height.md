---
description: The size of a typeface is a number; the size it looks is its x-height.
source: obsidian-knowledge
---

# X-Height

> *The size of a typeface is a number; the size it looks is its x-height.*

---

## The Measure of the Lowercase

The x-height is the distance from the [Baseline](/knowledge/typography/anatomy/baseline)[^sn-baseline] to the top of the lowercase letters that have neither [ascenders](/knowledge/typography/anatomy/ascender) nor [descenders](/knowledge/typography/anatomy/descender), most simply the height of the letter **x**. Because most of what we read is lowercase, the x-height governs how large a typeface *appears*, far more than its nominal point size (see [Points and Picas](/knowledge/typography/anatomy/points-and-picas) and [Em and En](/knowledge/typography/anatomy/em-and-en)). Two faces set at 12 points can look a full size apart.

## Large and Small

Renaissance [Old-Style](/knowledge/typography/classification/old-style) faces such as [Garamond](/knowledge/typography/typefaces/garamond) and [Bembo](/knowledge/typography/typefaces/bembo) have modest x-heights and long ascenders, which gives them an elegant, airy texture and lets them be set with less [Leading](/knowledge/typography/anatomy/leading). Twentieth-century faces moved the other way. [Times New Roman](/knowledge/typography/typefaces/times-new-roman)[^sn-times-new-roman] raised the x-height to save space in narrow newspaper columns, and screen faces like [Verdana](/knowledge/typography/typefaces/verdana), [Georgia](/knowledge/typography/typefaces/georgia), [Inter](/knowledge/typography/typefaces/inter), and [SF Pro](/knowledge/typography/typefaces/sf-pro) push it higher still so the lowercase survives being drawn with only a handful of pixels (see [Screen Typography and Hinting](/knowledge/typography/practice-and-principles/screen-typography-and-hinting)).

A large x-height improves legibility at small sizes but has costs: the ascenders and descenders shrink, word shapes become less distinctive, and the face needs more space between lines to avoid looking crowded. A small x-height reads beautifully in a book and poorly on a low-resolution screen.

## In Practice

When [pairing faces](/knowledge/typography/practice-and-principles/pairing-typefaces), matching x-heights matters more than matching point sizes; the CSS property `font-size-adjust` exists precisely to normalize fallback fonts to a common x-height. Readers of [Readability and Legibility](/knowledge/typography/practice-and-principles/readability-and-legibility) research will meet the x-height constantly, because it is the single metric that most predicts how big text feels.

## Related

- [Cap Height](/knowledge/typography/anatomy/cap-height)
- [Baseline](/knowledge/typography/anatomy/baseline)
- [Ascender](/knowledge/typography/anatomy/ascender)
- [Leading](/knowledge/typography/anatomy/leading)
- [Readability and Legibility](/knowledge/typography/practice-and-principles/readability-and-legibility)
- [Screen Typography and Hinting](/knowledge/typography/practice-and-principles/screen-typography-and-hinting)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-times-new-roman]: Times New Roman was commissioned by The Times of London after Stanley Morison, typographic adviser to Monotype, criticized the paper's printing.

[^sn-baseline]: Because the baseline is shared, it is what makes a line of mixed sizes, weights, or even typefaces read as one line.

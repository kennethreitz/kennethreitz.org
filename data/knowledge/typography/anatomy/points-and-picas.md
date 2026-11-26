---
description: Every typographic system is, at bottom, a quarrel about inches.
source: obsidian-knowledge
---

# Points and Picas

> *Every typographic system is, at bottom, a quarrel about inches.*

---

## The Point

The point is the basic absolute unit of type size. Its history is a long series of national and commercial standards. Pierre-Simon Fournier proposed a systematic point in 1737; François-Ambroise Didot revised it later in the eighteenth century, and the larger *Didot point* became the European standard. American type founders adopted their own *pica point*, about 1/72.27 of an inch, in 1886.

When Adobe's PostScript defined the page for [Desktop Publishing](/knowledge/typography/history/desktop-publishing), it rounded the point to exactly 1/72 of an inch. That *PostScript point* (sometimes called the DTP point) is now the point almost everyone uses. [Donald Knuth](/knowledge/typography/type-designers/donald-knuth)'s TeX kept the traditional printer's point as `pt` (1/72.27 inch) and calls the PostScript point the "big point," `bp`, a small fossil of this history visible in every LaTeX document (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)).

## The Pica

A pica is twelve points, about a sixth of an inch. Typographers traditionally measured the [Measure](/knowledge/typography/anatomy/measure)[^sn-measure] and column widths in picas, and many page layout programs still offer picas as a unit.

## Type Size

A font's point size is the height of the *body*, the metal block on which a letter was cast, not the height of any letter. That is why two faces at the same nominal size can look so different: their [X-Height](/knowledge/typography/anatomy/x-height) and [Cap Height](/knowledge/typography/anatomy/cap-height)[^sn-cap-height] take up different fractions of the body. The relative unit built from the point size is the [em](/knowledge/typography/anatomy/em-and-en).

## Related

- [Em and En](/knowledge/typography/anatomy/em-and-en)
- [Measure](/knowledge/typography/anatomy/measure)
- [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)
- [Desktop Publishing](/knowledge/typography/history/desktop-publishing)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-cap-height]: Cap height is the distance from the Baseline to the top of a flat capital letter such as H or E.

[^sn-measure]: The measure is the width of a line of text, traditionally expressed in picas or ems and today often in characters.

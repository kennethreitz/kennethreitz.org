---
description: The em is a square of space that grows and shrinks with the type.
source: obsidian-knowledge
---

# Em and En

> *The em is a square of space that grows and shrinks with the type.*

---

## Relative Units

The **em** is a unit equal to the current point size: in 12 point type, an em is 12 points; in 30 point type, 30 points. Historically it derived from the width of the capital **M** in metal type, whose body was roughly square. The **en** is half an em. Because they scale with the type, ems and ens are the natural units for anything that should stay proportional to the text: indents, spaces, [Tracking](/knowledge/typography/anatomy/tracking),[^sn-tracking] and the size of punctuation.

## The Dashes

The two units name the two long dashes. The *em dash* is an em wide and marks a break in a sentence; the *en dash* is an en wide and marks ranges, as in "pages 10 to 20" written with a dash, or connections such as "the London to Paris train." Both are distinct from the hyphen. Their correct use, and the spacing around them, is covered in [Quotes and Dashes](/knowledge/typography/practice-and-principles/quotes-and-dashes).

## Spaces

Metal type had a whole family of fixed spaces defined as fractions of the em: the em quad, the en quad, the thick space (a third of an em), the thin space (a fifth), and the hair space. Unicode keeps them all, and they are still useful for [Microtypography](/knowledge/typography/practice-and-principles/microtypography),[^sn-microtypography] such as a thin space around an em dash or between initials.

## On the Web

CSS borrowed the unit directly. `1em` equals the element's font size, and `rem` equals the root font size, which is why responsive typography is usually written in ems and rems. Digital fonts are drawn on an *em square*, a grid usually of 1000 or 2048 units, which is the coordinate space every [Glyph](/knowledge/typography/anatomy/glyph) lives in.

## Related

- [Points and Picas](/knowledge/typography/anatomy/points-and-picas)
- [Quotes and Dashes](/knowledge/typography/practice-and-principles/quotes-and-dashes)
- [Tracking](/knowledge/typography/anatomy/tracking)
- [Glyph](/knowledge/typography/anatomy/glyph)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-tracking]: Tracking (also called letterspacing) is a uniform adjustment of the space between all the letters in a run of text, as opposed to Kerning, which adjusts individual pairs.

[^sn-microtypography]: Microtypography is the fine texture inside it: letter spacing, word spacing, Kerning, line breaking, punctuation spacing, Hanging Punctuation, ligatures, and the subtle adjustments that make a column of text look even.

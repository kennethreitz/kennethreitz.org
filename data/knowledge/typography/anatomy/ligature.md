---
description: Some letters were always going to meet; the ligature lets them shake
  hands.
source: obsidian-knowledge
---

# Ligature

> *Some letters were always going to meet; the ligature lets them shake hands.*

---

## Joined Letters

A ligature is a single [Glyph](/knowledge/typography/anatomy/glyph)[^sn-glyph] that combines two or more letters. The most common in Latin typography are **fi**, **fl**, **ff**, **ffi**, and **ffl**, where the hooked top of **f** would otherwise collide with the dot of **i** or the ascender of **l**. Some ligatures became letters in their own right: the ampersand **&** began as a ligature of Latin *et*, and **æ** and **œ** are ligatures that some languages treat as letters.

## A Long History

Scribes joined letters constantly, and early printers imitated them. [Johannes Gutenberg](/knowledge/typography/type-designers/johannes-gutenberg)'s type for the 42-line Bible included hundreds of [sorts](/knowledge/typography/anatomy/glyph), many of them ligatures and abbreviations, to match the density and evenness of a manuscript in [Blackletter](/knowledge/typography/classification/blackletter).[^sn-blackletter] [The Aldine Press](/knowledge/typography/history/the-aldine-press)'s italic was full of ligatures too. The arrival of [Hot Metal Typesetting](/knowledge/typography/history/hot-metal-typesetting) and then typewriters thinned them out, and [Desktop Publishing](/knowledge/typography/history/desktop-publishing) brought them back only once OpenType fonts made them automatic.

## Kinds

Standard ligatures (OpenType feature `liga`) fix collisions and should normally be on. Discretionary ligatures (`dlig`), like **ct** and **st** joined with a swash, are ornaments to be used sparingly. *Programming ligatures*, which draw sequences like `->` or `!=` as a single symbol, appear in some [Monospace](/knowledge/typography/classification/monospace) coding fonts, including [Iosevka](/knowledge/typography/typefaces/iosevka); they divide programmers, since they change how code looks without changing what it is (see [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)).

## In Practice

Turn off ligatures when you letterspace text, since joined letters cannot follow the extra [Tracking](/knowledge/typography/anatomy/tracking). And remember that ligatures are a matter of rendering, not spelling: the text underneath still reads "f" and "i," as it should for searching and screen readers.

## Related

- [Glyph](/knowledge/typography/anatomy/glyph)
- [Kerning](/knowledge/typography/anatomy/kerning)
- [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)
- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-blackletter]: Blackletter (also called Gothic) is the family of scripts that dominated European writing from the twelfth century onward: narrow, angular letters with heavy vertical strokes, packed densely to save expensive parchment.

[^sn-glyph]: In metal type, each glyph was a physical piece called a *sort*, and a complete set of sorts in one size and style was a *fount* (the origin of the word font).

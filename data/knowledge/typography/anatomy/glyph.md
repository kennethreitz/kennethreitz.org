---
description: A character is an idea; a glyph is one way of drawing it.
source: obsidian-knowledge
---

# Glyph

> *A character is an idea; a glyph is one way of drawing it.*

---

## Character and Glyph

A *character* is an abstract unit of text: the letter "a," the digit "7," the question mark. A *glyph* is a specific drawn shape in a specific font. One character can have many glyphs (a roman **a**, an italic *a*, a small cap, a swash), and one glyph can stand for several characters, as a [Ligature](/knowledge/typography/anatomy/ligature)[^sn-ligature] does. Unicode encodes characters; fonts supply glyphs; the shaping engine maps one to the other.

## Sorts

In metal type, each glyph was a physical piece called a *sort*, and a complete set of sorts in one size and style was a *fount* (the origin of the word font). Running out of a letter mid-job left the compositor "out of sorts." [Johannes Gutenberg](/knowledge/typography/type-designers/johannes-gutenberg)'s Bible type needed hundreds of sorts, including many abbreviations and [ligatures](/knowledge/typography/anatomy/ligature), to imitate the even texture of a scribe's [Blackletter](/knowledge/typography/classification/blackletter).[^sn-blackletter]

## Modern Fonts

An OpenType font can hold up to 65,535 glyphs, and serious text families include alternate [Figures](/knowledge/typography/practice-and-principles/figures), [Small Caps](/knowledge/typography/practice-and-principles/small-caps), ligatures, and extended alphabets for many languages, all reached through [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features). Every glyph is drawn on the em square (see [Em and En](/knowledge/typography/anatomy/em-and-en)) as outlines, either quadratic curves (TrueType) or cubic curves (PostScript and CFF), and on screens those outlines are rasterized and sometimes hinted (see [Screen Typography and Hinting](/knowledge/typography/practice-and-principles/screen-typography-and-hinting)).

## In Practice

The distinction matters any time text is processed rather than looked at. Search, copy and paste, and screen readers all see characters, which is why ligatures and alternates should come from font features, not from typing look-alike symbols.

## Related

- [Ligature](/knowledge/typography/anatomy/ligature)
- [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)
- [Em and En](/knowledge/typography/anatomy/em-and-en)
- [Figures](/knowledge/typography/practice-and-principles/figures)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-blackletter]: Blackletter (also called Gothic) is the family of scripts that dominated European writing from the twelfth century onward: narrow, angular letters with heavy vertical strokes, packed densely to save expensive parchment.

[^sn-ligature]: A ligature is a single Glyph that combines two or more letters.

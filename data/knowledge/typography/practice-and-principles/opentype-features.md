---
description: A good font is a toolbox; OpenType features are the drawers.
source: obsidian-knowledge
---

# OpenType Features

> *A good font is a toolbox; OpenType features are the drawers.*

---

## The Format

OpenType, announced by Microsoft and Adobe in 1996, unified the TrueType and PostScript font formats and added *layout features*: tables of rules that substitute or position [glyphs](/knowledge/typography/anatomy/glyph)[^sn-glyph] depending on context. A single font can contain alternate letterforms, [ligatures](/knowledge/typography/anatomy/ligature), [Small Caps](/knowledge/typography/practice-and-principles/small-caps), several styles of [Figures](/knowledge/typography/practice-and-principles/figures), and the shaping logic that complex scripts like Arabic and Devanagari require.

## Common Features

| Tag | Feature |
|---|---|
| `kern` | [Kerning](/knowledge/typography/anatomy/kerning) |
| `liga` / `dlig` | Standard and discretionary ligatures |
| `smcp` / `c2sc` | Small caps |
| `onum` / `lnum` | Old-style and lining figures |
| `tnum` / `pnum` | Tabular and proportional figures |
| `frac` | Fractions |
| `ss01` and up | Stylistic sets of alternate forms |
| `case` | Case-sensitive punctuation for all caps |
| `calt` | Contextual alternates (used by scripts and coding ligatures) |

## On the Web

CSS exposes most features through high-level properties such as `font-variant-numeric`, `font-variant-caps`, and `font-variant-ligatures`, with `font-feature-settings` as a low-level fallback. The playful [note-from-ai](/artificial-intelligence/personal/note-from-ai) in this vault records a rebuild of Kenneth's site typography that leaned on exactly these features: kerning, contextual ligatures, and old-style numerals.

## In Practice

Use features where they serve the reader: kerning and standard ligatures on, old-style figures in text, tabular figures in tables, small caps for acronyms. Check that the font actually contains the feature; browsers will not fake most of them.

## Related

- [Glyph](/knowledge/typography/anatomy/glyph)
- [Ligature](/knowledge/typography/anatomy/ligature)
- [Figures](/knowledge/typography/practice-and-principles/figures)
- [Small Caps](/knowledge/typography/practice-and-principles/small-caps)
- [Variable Fonts](/knowledge/typography/history/variable-fonts)
- [Desktop Publishing](/knowledge/typography/history/desktop-publishing)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-glyph]: In metal type, each glyph was a physical piece called a *sort*, and a complete set of sorts in one size and style was a *fount* (the origin of the word font).

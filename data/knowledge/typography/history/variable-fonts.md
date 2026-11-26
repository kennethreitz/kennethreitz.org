---
description: One file, a continuous space of styles.
source: obsidian-knowledge
---

# Variable Fonts

> *One file, a continuous space of styles.*

---

## The Format

A variable font contains a whole range of styles in a single file. Instead of separate files for light, regular, and bold, the designer draws masters at the extremes of one or more *axes*, and the renderer interpolates any point between them. Variable fonts were introduced with OpenType 1.8, announced jointly by Adobe, Apple, Google, and Microsoft in September 2016.

## Axes

| Axis | Tag | Controls |
|---|---|---|
| Weight | `wght` | Light to black |
| Width | `wdth` | Condensed to extended |
| Optical size | `opsz` | Design adjusted for small or large sizes |
| Italic | `ital` | Roman to italic |
| Slant | `slnt` | Oblique angle |

Designers can also define custom axes, such as the height of [serifs](/knowledge/typography/anatomy/serif) or the length of [ascenders](/knowledge/typography/anatomy/ascender).

## Ancestors

The idea had precedents: Adobe's Multiple Master fonts (1991) and Apple's TrueType GX (1994) both offered interpolation but never caught on. Earlier still, [Donald Knuth](/knowledge/typography/type-designers/donald-knuth)'s parametric [Computer Modern](/knowledge/typography/typefaces/computer-modern) generated a family from a single program. The optical size axis restores something metal type had and [Phototypesetting](/knowledge/typography/history/phototypesetting)[^sn-phototypesetting] lost: true designs for each size.

## In Practice

Variable fonts reduce download size for [Web Fonts](/knowledge/typography/history/web-fonts) and allow fine typographic control, such as continuous optical sizing in [SF Pro](/knowledge/typography/typefaces/sf-pro) and [Inter](/knowledge/typography/typefaces/inter) or responsive weight adjustments for dark mode.

## Related

- [Web Fonts](/knowledge/typography/history/web-fonts)
- [Computer Modern](/knowledge/typography/typefaces/computer-modern)
- [SF Pro](/knowledge/typography/typefaces/sf-pro)
- [Inter](/knowledge/typography/typefaces/inter)
- [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features)
- [History](/knowledge/typography/history)

[^sn-phototypesetting]: Phototypesetting replaced metal with light. Letter images were stored as film negatives on discs, grids, or strips, and the machine flashed light through them onto photographic paper or film, which was then used to make offset printing plates.

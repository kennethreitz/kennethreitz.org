---
description: On a screen, every letter is a negotiation between the outline and the
  grid.
source: obsidian-knowledge
---

# Screen Typography and Hinting

> *On a screen, every letter is a negotiation between the outline and the grid.*

---

## The Pixel Problem

Digital fonts are outlines (see [Glyph](/knowledge/typography/anatomy/glyph)); screens are grids of pixels. At small sizes on low-resolution screens, a stem might fall between two pixel columns and render as a gray smear, or an [X-Height](/knowledge/typography/anatomy/x-height) might round to an inconsistent pixel height. Rendering type well on screens has been a central problem of typography since the 1980s.

## Hinting

*Hinting* adds instructions to a font that tell the rasterizer how to fit outlines to the pixel grid at each size: snap stems to whole pixels, keep x-heights consistent, keep counters open. TrueType hinting is a full programming language, and hand-hinting a family could take longer than designing it. [Matthew Carter](/knowledge/typography/type-designers/matthew-carter)'s [Verdana](/knowledge/typography/typefaces/verdana) and [Georgia](/knowledge/typography/typefaces/georgia), hinted by Tom Rickner, are classics of the craft; Carter drew their bitmaps first.

## Anti-aliasing

Anti-aliasing uses gray pixels to approximate partial coverage, and *subpixel rendering* (such as Microsoft's ClearType, shipped with Windows XP) uses the separate red, green, and blue elements of LCD pixels to triple horizontal resolution. Apple historically favored preserving the shapes of letters over snapping to pixels, while Microsoft favored crispness, an old philosophical split.

## High Resolution

High-density displays, beginning with Apple's Retina iPhone 4 in 2010, made much of this less necessary. Apple removed subpixel anti-aliasing from macOS by default in 2018. With enough pixels, the fine details of [Old-Style](/knowledge/typography/classification/old-style)[^sn-old-style] and high-contrast faces finally survive on screen, which is part of why [Web Fonts](/knowledge/typography/history/web-fonts) and screen reading of serif text became practical.

## Related

- [Verdana](/knowledge/typography/typefaces/verdana)
- [Georgia](/knowledge/typography/typefaces/georgia)
- [Matthew Carter](/knowledge/typography/type-designers/matthew-carter)
- [Web Fonts](/knowledge/typography/history/web-fonts)
- [Readability and Legibility](/knowledge/typography/practice-and-principles/readability-and-legibility)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-old-style]: Old-style faces, called *Garaldes* in the Vox-ATypI system (a blend of Garamond and Aldus), descend from the roman cut by Francesco Griffo for Aldus Manutius in 1495, the type known today through its revival as Bembo.

---
description: For fifteen years the web had ten typefaces. Then it had all of them.
source: obsidian-knowledge
---

# Web Fonts

> *For fifteen years the web had ten typefaces. Then it had all of them.*

---

## The Core Fonts Era

The early web could only display fonts installed on the reader's computer. Microsoft's *Core fonts for the Web* project (1996), which distributed fonts including [Georgia](/knowledge/typography/typefaces/georgia)[^sn-georgia] and [Verdana](/knowledge/typography/typefaces/verdana) by [Matthew Carter](/knowledge/typography/type-designers/matthew-carter), gave the web a small common set. For about a decade, web typography meant choosing from a handful of "web-safe" fonts and writing font stacks of fallbacks (see font-family recommendations. Chris Morgan).

## @font-face

CSS described a way to download fonts with the `@font-face` rule in the late 1990s, but incompatible formats, licensing worries, and poor rendering held it back. The breakthrough came around 2009 and 2010: browsers converged on support, the WOFF format (a compressed wrapper for fonts, later a W3C standard, with WOFF2 following) addressed foundries' concerns, and services like Typekit (2009) and Google Fonts (2010) made licensed and open-source fonts easy to use.

## Craft Returns

With real fonts available, the web began to take typography seriously: [Measure](/knowledge/typography/anatomy/measure), [Leading](/knowledge/typography/anatomy/leading), [Vertical Rhythm](/knowledge/typography/practice-and-principles/vertical-rhythm),[^sn-vertical-rhythm] [OpenType Features](/knowledge/typography/practice-and-principles/opentype-features), and responsive type scales. Kenneth's own projects live in this world, from kennethreitz.org's custom type system to the Tufte-inspired KJVstudy.org, and his essay [The Interface Is the Subconscious](/essays/2026-03-20-the_interface_is_the_subconscious) argues why it matters. The next step was the [variable font](/knowledge/typography/history/variable-fonts), which delivers a whole family in one file.

## Related

- [Variable Fonts](/knowledge/typography/history/variable-fonts)
- [Screen Typography and Hinting](/knowledge/typography/practice-and-principles/screen-typography-and-hinting)
- [Georgia](/knowledge/typography/typefaces/georgia)
- [Verdana](/knowledge/typography/typefaces/verdana)
- [Desktop Publishing](/knowledge/typography/history/desktop-publishing)
- [History](/knowledge/typography/history)

[^sn-vertical-rhythm]: Vertical rhythm is the practice of building every vertical measurement on a page from a single unit, usually the line height of the body text (see Leading).

[^sn-georgia]: Georgia was designed by Matthew Carter for Microsoft, with hinting by Tom Rickner, and was released in 1996 as part of Microsoft's free core fonts for the web, alongside its sans serif sibling Verdana.

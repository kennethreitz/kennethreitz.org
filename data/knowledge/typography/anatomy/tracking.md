---
description: Space between letters is a volume knob; most text wants it left where
  the designer set it.
source: obsidian-knowledge
---

# Tracking

> *Space between letters is a volume knob; most text wants it left where the designer set it.*

---

## Letterspacing

Tracking (also called letterspacing) is a uniform adjustment of the space between all the letters in a run of text, as opposed to [Kerning](/knowledge/typography/anatomy/kerning),[^sn-kerning] which adjusts individual pairs. In CSS it is `letter-spacing`.

## When to Track

Typefaces are spaced by their designers for a particular range of sizes. As a rule, text set much larger than that range looks too loose and benefits from slightly negative tracking, and text set much smaller benefits from slightly positive tracking. Some modern families build this in: Apple's [SF Pro](/knowledge/typography/typefaces/sf-pro) applies size-specific tracking automatically, and fonts with an optical size axis do the same (see [Variable Fonts](/knowledge/typography/history/variable-fonts)).

Capitals and [Small Caps](/knowledge/typography/practice-and-principles/small-caps) almost always want added tracking. They were designed to be seen next to lowercase letters, and in a solid run their spacing is too tight. Lowercase letters almost never want it, since their spacing is built around word shapes. A line usually credited to the American type designer Frederic Goudy says that anyone who would letterspace lowercase would steal sheep, which is where Erik Spiekermann's book title *Stop Stealing Sheep* comes from (see [Stop Stealing Sheep](/knowledge/typography/key-texts/stop-stealing-sheep)).

## In Practice

Track capitals by a few percent of the em (see [Em and En](/knowledge/typography/anatomy/em-and-en)). Do not use tracking to force a justified line to fit; that job belongs to hyphenation and word spacing (see [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)). Turn off [ligatures](/knowledge/typography/anatomy/ligature)[^sn-ligature] wherever you letterspace.

## Related

- [Kerning](/knowledge/typography/anatomy/kerning)
- [Small Caps](/knowledge/typography/practice-and-principles/small-caps)
- [Cap Height](/knowledge/typography/anatomy/cap-height)
- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-ligature]: A ligature is a single Glyph that combines two or more letters.

[^sn-kerning]: Kerning is the adjustment of space between particular pairs of letters so that the overall spacing looks even.

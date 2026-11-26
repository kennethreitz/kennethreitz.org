---
description: A line needs room to breathe before the eye can find the next one.
source: obsidian-knowledge
---

# Leading

> *A line needs room to breathe before the eye can find the next one.*

---

## Strips of Lead

Leading (pronounced *ledding*) is the vertical distance between lines of text, measured from one [Baseline](/knowledge/typography/anatomy/baseline)[^sn-baseline] to the next. The word comes from metal typesetting, where compositors placed thin strips of lead between lines of type to open them up. Type set without them was *set solid*. In digital typography, leading is usually expressed as the total line height, so 11 point type on a 14 point line is written "11/14."

## How Much

The right leading depends on the [X-Height](/knowledge/typography/anatomy/x-height) of the face, the length of the line (see [Measure](/knowledge/typography/anatomy/measure)), and the size of the type. Faces with large x-heights look crowded at tight leading; long lines need more leading so the eye can find the start of the next line; short lines, like captions and narrow columns, can take less. Matthew Butterick's guidance in [Practical Typography](/knowledge/typography/key-texts/practical-typography) is a line spacing of roughly 120 to 145 percent of the point size for body text, a sensible starting point on screen and in print.

## Leading as Rhythm

Consistent leading is the beat of a page. Headings, block quotations, and images that sit on multiples of the base line height keep the text block in step across columns and spreads; this is the principle of [Vertical Rhythm](/knowledge/typography/practice-and-principles/vertical-rhythm)[^sn-vertical-rhythm] and of the baseline grid in [Grid Systems](/knowledge/typography/practice-and-principles/grid-systems). It is the visual cousin of [Cadence](/knowledge/key-concepts/cadence).

## In Practice

On the web, set `line-height` as a unitless number (for example 1.4) so it scales with the font size. Increase leading for long measures and for faces with tall x-heights. Reduce it for large display headings, which look disconnected at body-text spacing.

## Related

- [Measure](/knowledge/typography/anatomy/measure)
- [Vertical Rhythm](/knowledge/typography/practice-and-principles/vertical-rhythm)
- [Baseline](/knowledge/typography/anatomy/baseline)
- [X-Height](/knowledge/typography/anatomy/x-height)
- [Practical Typography](/knowledge/typography/key-texts/practical-typography)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-vertical-rhythm]: Vertical rhythm is the practice of building every vertical measurement on a page from a single unit, usually the line height of the body text (see Leading).

[^sn-baseline]: In metal type the baseline was fixed by the foundry's casting, and type from different foundries often refused to line up until the American and British foundries standardized "point line" alignment around the turn of the twentieth century.

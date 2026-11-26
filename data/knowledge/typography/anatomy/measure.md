---
description: The eye can only swim so far before it needs to breathe.
source: obsidian-knowledge
---

# Measure

> *The eye can only swim so far before it needs to breathe.*

---

## Line Length

The measure is the width of a line of text, traditionally expressed in [picas](/knowledge/typography/anatomy/points-and-picas) or ems and today often in characters. It is one of the three decisions, with type size and [Leading](/knowledge/typography/anatomy/leading),[^sn-leading] that settle how comfortable a text block is to read.

## The Classic Range

In [The Elements of Typographic Style](/knowledge/typography/key-texts/the-elements-of-typographic-style),[^sn-the-elements-of-typographic-style] Robert Bringhurst gives the range most typographers quote: anything from about 45 to 75 characters is widely regarded as a satisfactory line for a single column of serif text, and 66 characters is widely regarded as ideal. Multi-column text can run shorter, around 40 to 50 characters. Lines much longer than that make it hard for the eye to find the beginning of the next line; lines much shorter break the text into too many hyphens and ragged ends.

## In This Vault

This is more than theory here. The Reitz LaTeX theme for Obsidian uses a centered 760px measure for writing and a measure of about 41rem for reading, tuned to the text width of a LaTeX article (see [Draft to Document Why I Made My Notes Look Like LaTeX Papers](/essays/2026-11-04-draft_to_document)). Generous margins and a disciplined measure are also part of the Tufte-inspired design of KJVstudy.org.

## In Practice

On the web, constrain text containers with a `max-width` in `ch` or `em` units rather than letting paragraphs run the full width of a monitor. Pair longer measures with more leading. When a layout needs both wide images and readable text, let the images break out of the column rather than widening the column (see [Grid Systems](/knowledge/typography/practice-and-principles/grid-systems) and [Page Canons](/knowledge/typography/practice-and-principles/page-canons)).

## Related

- [Leading](/knowledge/typography/anatomy/leading)
- [Readability and Legibility](/knowledge/typography/practice-and-principles/readability-and-legibility)
- [Grid Systems](/knowledge/typography/practice-and-principles/grid-systems)
- [Page Canons](/knowledge/typography/practice-and-principles/page-canons)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Anatomy](/knowledge/typography/anatomy)

[^sn-the-elements-of-typographic-style]: Robert Bringhurst's *The Elements of Typographic Style* is the most widely admired modern guide to typography.

[^sn-leading]: In digital typography, leading is usually expressed as the total line height, so 11 point type on a 14 point line is written "11/14."

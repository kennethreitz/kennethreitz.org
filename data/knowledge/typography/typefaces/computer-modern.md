---
description: A typeface written as a program, by a computer scientist who wanted his
  books to look right.
source: obsidian-knowledge
---

# Computer Modern

> *A typeface written as a program, by a computer scientist who wanted his books to look right.*

---

## The Face

Computer Modern is the family [Donald Knuth](/knowledge/typography/type-designers/donald-knuth)[^sn-donald-knuth] designed for TeX (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)). It is modeled on Monotype Modern 8A, a late nineteenth-century style descended from the [Didone](/knowledge/typography/classification/didone) and Scotch romans, which Knuth admired in older printings of his own books. He developed it alongside TeX from the late 1970s, and published the final version in 1986 as *Computer Modern Typefaces*, the last volume of *Computers and Typesetting*.

## A Parametric Font

Computer Modern is not drawn as outlines. It is written in METAFONT, Knuth's language for describing letters as the paths of a pen, and every style (roman, italic, bold, sans, typewriter, and the mathematical symbols) is generated from shared programs by changing a set of parameters. Sizes are true optical sizes: the 5 point type is wider and sturdier than the 10 point scaled down, as metal type was. This parametric idea anticipates [Variable Fonts](/knowledge/typography/history/variable-fonts)[^sn-variable-fonts] by decades.

## The Look of Science

Because LaTeX uses it by default, Computer Modern is the face of the academic paper, instantly recognizable to anyone in mathematics, physics, or computer science. Its fairly light, high-contrast text has critics on screen, and its modern successor is [Latin Modern](/knowledge/typography/typefaces/latin-modern).

## In This Vault

The Reitz LaTeX theme began by bundling Computer Modern Unicode before switching to the genuine [Latin Modern](/knowledge/typography/typefaces/latin-modern) faces measured from a real LaTeX PDF (see [Draft to Document Why I Made My Notes Look Like LaTeX Papers](/essays/2026-11-04-draft_to_document)).

## Related

- [Donald Knuth](/knowledge/typography/type-designers/donald-knuth)
- [Latin Modern](/knowledge/typography/typefaces/latin-modern)
- [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)
- [The TeXbook](/knowledge/typography/key-texts/the-texbook)
- [Didone](/knowledge/typography/classification/didone)
- [Variable Fonts](/knowledge/typography/history/variable-fonts)
- [Typefaces](/knowledge/typography/typefaces)

[^sn-donald-knuth]: Donald Knuth, the Stanford computer scientist and author of *The Art of Computer Programming*, received the galley proofs of a new edition of one of its volumes in the mid 1970s and found the phototypeset mathematics ugly compared with the hot metal original.

[^sn-variable-fonts]: Variable fonts reduce download size for Web Fonts and allow fine typographic control, such as continuous optical sizing in SF Pro and Inter or responsive weight adjustments for dark mode.

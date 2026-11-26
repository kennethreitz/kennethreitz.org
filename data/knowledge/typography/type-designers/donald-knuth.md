---
description: He wanted his books to look as good as they used to, so he wrote a typesetting
  system.
source: obsidian-knowledge
---

# Donald Knuth

> *He wanted his books to look as good as they used to, so he wrote a typesetting system.*

---

## The Problem

Donald Knuth, the Stanford computer scientist and author of *The Art of Computer Programming*, received the galley proofs of a new edition of one of its volumes in the mid 1970s and found the [phototypeset](/knowledge/typography/history/phototypesetting)[^sn-phototypesetting] mathematics ugly compared with the hot metal original. He decided to solve the problem himself, expecting it to take a year or so.

## TeX and METAFONT

It took about a decade. The result was TeX, a typesetting system that treats a paragraph as an optimization problem (the Knuth-Plass line-breaking algorithm, see [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)), and METAFONT, a language for describing letterforms as the paths of pens, with which he designed the parametric [Computer Modern](/knowledge/typography/typefaces/computer-modern)[^sn-computer-modern] family. TeX's ability to set mathematics beautifully made it, through LaTeX, the standard for scientific publishing (see [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex) and [The TeXbook](/knowledge/typography/key-texts/the-texbook)).

## Character

Knuth froze TeX's design deliberately: its version numbers converge on pi (and METAFONT's on e), with each bug fix adding a digit, and the final version will be pi itself. He worked with [Hermann Zapf](/knowledge/typography/type-designers/hermann-zapf) on the AMS Euler typeface and pioneered literate programming, the idea that programs should be written to be read by humans. It is a natural ancestor of the "for humans" sensibility (see [For Humans](/knowledge/philosophy/for-humans)).

## Related

- [Typesetting Math with TeX](/knowledge/typography/practice-and-principles/typesetting-math-with-tex)
- [The TeXbook](/knowledge/typography/key-texts/the-texbook)
- [Computer Modern](/knowledge/typography/typefaces/computer-modern)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Hermann Zapf](/knowledge/typography/type-designers/hermann-zapf)
- [Type Designers](/knowledge/typography/type-designers)

[^sn-phototypesetting]: Phototypesetting replaced metal with light. Letter images were stored as film negatives on discs, grids, or strips, and the machine flashed light through them onto photographic paper or film, which was then used to make offset printing plates.

[^sn-computer-modern]: Computer Modern is the family Donald Knuth designed for TeX (see Typesetting Math with TeX).

---
description: Mathematics is a language that needs a typographer fluent in two dimensions.
source: obsidian-knowledge
---

# Typesetting Math with TeX

> *Mathematics is a language that needs a typographer fluent in two dimensions.*

---

## The Hard Case

Mathematical notation is the hardest common problem in typesetting: symbols stacked in two dimensions, fractions, subscripts of subscripts, special alphabets, and spacing rules that change with context. In [Hot Metal Typesetting](/knowledge/typography/history/hot-metal-typesetting) it was slow and expensive; early [Phototypesetting](/knowledge/typography/history/phototypesetting)[^sn-phototypesetting] did it badly. That failure led [Donald Knuth](/knowledge/typography/type-designers/donald-knuth) to build TeX.

## TeX and LaTeX

TeX, first released in 1978 and rewritten as TeX82, treats typesetting as computation. It sets a paragraph by considering all possible line breaks at once and choosing the best combination (the Knuth-Plass algorithm, see [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)), and encodes the spacing conventions of mathematics in detail. Leslie Lamport's LaTeX, a set of macros released in the 1980s, made TeX practical for ordinary authors, separating structure (`\section`, `\begin{theorem}`) from presentation. The default face is Knuth's [Computer Modern](/knowledge/typography/typefaces/computer-modern),[^sn-computer-modern] now commonly [Latin Modern](/knowledge/typography/typefaces/latin-modern).

## Legacy

LaTeX became the standard for mathematics, physics, and computer science, and its look is the look of the scientific paper. On the web, MathJax and KaTeX render TeX notation in browsers, which is how Obsidian displays math in this vault. Kenneth's Reitz LaTeX theme borrows LaTeX's page, not its math: the measure, the heading ratios, and the reading face (see [Draft to Document Why I Made My Notes Look Like LaTeX Papers](/essays/2026-11-04-draft_to_document)).

## Further Reading

[The TeXbook](/knowledge/typography/key-texts/the-texbook) is Knuth's own manual. The [TeX point](/knowledge/typography/anatomy/points-and-picas) (1/72.27 inch) is a small fossil of the hot metal world inside every LaTeX document.

## Related

- [Donald Knuth](/knowledge/typography/type-designers/donald-knuth)
- [The TeXbook](/knowledge/typography/key-texts/the-texbook)
- [Computer Modern](/knowledge/typography/typefaces/computer-modern)
- [Latin Modern](/knowledge/typography/typefaces/latin-modern)
- [Microtypography](/knowledge/typography/practice-and-principles/microtypography)
- [Justification and Hyphenation](/knowledge/typography/practice-and-principles/justification-and-hyphenation)
- [Practice & Principles](/knowledge/typography/practice-and-principles)

[^sn-phototypesetting]: Phototypesetting replaced metal with light. Letter images were stored as film negatives on discs, grids, or strips, and the machine flashed light through them onto photographic paper or film, which was then used to make offset printing plates.

[^sn-computer-modern]: Computer Modern is the family Donald Knuth designed for TeX (see Typesetting Math with TeX).

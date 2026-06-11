# RhymePad: A Scratchpad for Poets & Rappers

[rhymepad.org](https://rhymepad.org) is a writing pad that listens to the way words sound. Type a verse and the rhymes light up as you go, end rhymes, internal rhymes, and slant rhymes, each sound family sharing a color. It was built with Claude Code.

## The Idea

Rhyme is a feature of sound, not spelling. `tonight` and `light` rhyme; `tonight` and `delight` rhyme harder. But most writing tools treat text as a flat stream of characters and leave the ear to do all the work alone. RhymePad moves some of that listening into the page itself.

Every word is mapped to its phonemes using the CMU Pronouncing Dictionary, with lyric-friendly fallbacks for the way people actually write. `runnin'` becomes `running`, possessives resolve, and made-up words run through a grapheme-to-phoneme model so the page doesn't go silent when you invent a word. Perfect rhymes share everything from the last stressed vowel on. Slant rhymes share just the vowels. Same sound, same color.

## What It Does

- **Phonetic rhyme detection as you type**, with end, internal, slant, and multisyllabic cross-word rhymes color-coded by sound.
- **Brightness as rhyme strength**, so perfect rhymes blaze and slant rhymes sit back, a continuous gradient rather than on/off.
- **Near-miss radar**, a dotted gold outline on dead line endings that are one phoneme away from locking into a rhyme.
- **Rhyme and synonym lookup**, with frequency-ranked rhymes, near rhymes by syllable count, and WordNet synonyms by part of speech.
- **Alliteration and rhythm lenses** as separate toggles, plus draggable stanza reordering and WYSIWYG PNG export.

## Why It Matters

RhymePad is a tool that amplifies a craft rather than automating it away. It doesn't write your verse or finish your line. It surfaces structure that was always there in the sound, so you can see what your ear already half-knew: which words are pulling together, which line endings are landing, where the internal rhymes are hiding. The writing stays yours; the tool just makes the music visible.

It also runs almost entirely locally. The phonetics, the rhyme groups, the meter analysis, all served from the machine. Only dictionary definitions reach out to the free [dictionaryapi.dev](https://dictionaryapi.dev/). No accounts, no engagement metrics, no feed. Just the pad and the page.

## Visit

- [rhymepad.org](https://rhymepad.org)

## Related

- [**RhymePad: Seeing the Sound**](/essays/2026-06-11-rhymepad_seeing_the_sound) — The full story of building it and why the visual language works.
- [**Poems by Sarah**](/software/websites/poemsbysarah) — A poetry publishing platform built with Claude Code.
- [**The Hitchhiker's Guide to Python**](/software/websites/python-guide) — Another tool built for humans first.

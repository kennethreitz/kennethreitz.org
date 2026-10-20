# RhymePad: A Scratchpad for Poets & Rappers

[rhymepad.org](https://rhymepad.org) is a writing pad that listens to the way words sound. Type a verse and the rhymes light up as you go, end rhymes, internal rhymes, and slant rhymes, each sound family sharing a color. It was built with Claude Code.

## The Idea

Rhyme is a feature of sound, not spelling. `tonight` and `light` rhyme; `tonight` and `delight` rhyme harder. But most writing tools treat text as a flat stream of characters and leave the ear to do all the work alone. RhymePad moves some of that listening into the page itself.<label for="sn-rhyme-cadence" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-rhyme-cadence" class="margin-toggle"/><span class="sidenote">What it's really surfacing is [cadence](/knowledge/key-concepts/cadence), the rhythm that carries meaning before meaning is understood.</span>

Every word is mapped to its phonemes using the CMU Pronouncing Dictionary, with lyric-friendly fallbacks for the way people actually write. `runnin'` becomes `running`, possessives resolve, and made-up words run through a grapheme-to-phoneme model so the page doesn't go silent when you invent a word.<label for="sn-rhyme-abstraction" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-rhyme-abstraction" class="margin-toggle"/><span class="sidenote">Phonemes are the right [abstraction](/knowledge/key-concepts/abstraction) here. Spelling is the wrong one.</span> Perfect rhymes share everything from the last stressed vowel on. Slant rhymes share just the vowels. Same sound, same color.

## What It Does

- **Phonetic rhyme detection as you type**, with end, internal, slant, and multisyllabic cross-word rhymes color-coded by sound.
- **Brightness as rhyme strength**, so perfect rhymes blaze and slant rhymes sit back, a continuous gradient rather than on/off.
- **Near-miss radar**, a dotted gold outline on dead line endings that are one phoneme away from locking into a rhyme.
- **Rhyme and synonym lookup**, with frequency-ranked rhymes, near rhymes by syllable count, and WordNet synonyms by part of speech.
- **Alliteration and rhythm lenses** as separate toggles, plus draggable stanza reordering and WYSIWYG PNG export.

## Why It Matters

RhymePad is a tool that amplifies a craft rather than automating it away. It doesn't write your verse or finish your line. It surfaces structure that was always there in the sound, so you can see what your ear already half-knew: which words are pulling together, which line endings are landing, where the internal rhymes are hiding. The writing stays yours; the tool just makes the music visible.<label for="sn-rhyme-for-humans" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-rhyme-for-humans" class="margin-toggle"/><span class="sidenote">Amplify, don't automate: [For Humans](/knowledge/philosophy/for-humans).</span>

It also runs entirely locally. The phonetics, the rhyme groups, the meter analysis, even the dictionary definitions, all served from the machine. No external dictionary calls. No accounts, no engagement metrics, no feed. Just the pad and the page.

## Examples

Type `tonight` and `light` and they glow the same color, sharing `AY T` from the last stressed vowel on. Type `hold` and `coal` and they share a dimmer color: a slant rhyme. Yes, it knows `orange` rhymes with `door hinge`.

The same engine is available over HTTP. Ask for rhymes:

```bash
$ curl 'https://rhymepad.org/api/lookup?word=light&mode=rhyme'
{
  "word": "light",
  "mode": "rhyme",
  "known": true,
  "words": [
    {"word": "right", "z": 6.0, "syl": 1},
    {"word": "might", "z": 5.7, "syl": 1},
    {"word": "night", "z": 5.6, "syl": 1},
    ...
  ]
}
```

`mode` can also be `near` (near rhymes by syllable count) or `syn` (WordNet synonyms). `POST /api/analyze` with `{"text": "..."}` returns the full analysis: rhyme groups, per-stanza schemes, per-line meter, alliteration, and near-misses.

## Today

RhymePad is live at [rhymepad.org](https://rhymepad.org) and actively maintained by me. The [source is on GitHub](https://github.com/kennethreitz/rhymepad.org) under the ISC license, and it runs on [my own little server](/essays/2026-06-05-a_server_called_mercury). To run it locally, clone the repo and `make run`.

## Visit

- [rhymepad.org](https://rhymepad.org)
- [Source Code on GitHub](https://github.com/kennethreitz/rhymepad.org)

## Related

- [**RhymePad: Seeing the Sound**](/essays/2026-06-11-rhymepad_seeing_the_sound): The full story of building it and why the visual language works.
- [**Poems by Sarah**](/software/websites/poemsbysarah): A poetry publishing platform built with Claude Code.
- [**The Hitchhiker's Guide to Python**](/software/websites/python-guide): Another tool built for humans first.

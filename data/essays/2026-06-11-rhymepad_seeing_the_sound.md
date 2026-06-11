# RhymePad: Seeing the Sound

Rhyme is a fact about sound, not spelling. *Blue* rhymes with *shoe* and *through* and *you*, and not one of them is spelled like the others. *Comb*, *bomb*, and *tomb* all end in the same three letters and not one of them rhymes with another. The ear knows the difference instantly. The eye, staring at the same words, has no idea.

That gap has always bothered me. We write verse with our eyes open and our ears doing all the real work, alone, with no help from the page. So I built a page that listens.

[RhymePad](https://rhymepad.org) is a scratchpad for poets and rappers. You type or paste lyrics into it, and as you write, the rhyme structure lights up underneath you in real time. End rhymes, internal rhymes, slant rhymes, multisyllabic interlocks that thread across word boundaries. It reads the actual sounds, not the letters, and it paints what it hears. I vibe coded the whole thing with Claude Code, talking it into existence one conversation at a time.

Here is the easiest way to show you what that looks like. I asked it to analyze a verse about itself:

![A verse titled "RhymePad, on itself" with its rhyme families color-coded by RhymePad](/static/images/rhymepad-on-itself.png)

Every color is a sound family. Every brightness is how hard the rhyme lands. The whole essay below is really just an explanation of that one picture.

## The pad, not the dictionary

There are already good rhyming dictionaries. RhymeZone will tell you everything that rhymes with *orange* if you ask it about *orange*. But that's a lookup. You bring it a word, it brings you a list, and you go back to staring at your verse trying to hold the whole sonic structure in your head.

RhymePad inverts that.<label for="sn-inversion" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-inversion" class="margin-toggle"/><span class="sidenote">This is the same move as so much of the work I care about: stop making the human translate themselves into the machine's terms. A dictionary makes you query word by word. The pad meets you where you already are, which is in the middle of writing something.</span> It doesn't tell you what rhymes with a word. It shows you the rhyme architecture of what you're already writing, while you write it. The dictionary is still in there, a lookup panel a keystroke away, but it's the side dish. The moat is the pad. The whole point is that you never have to leave your own verse to see how it's holding together.

## Color is which sound, brightness is how hard

The visual language is the soul of the thing, so let me be precise about it.

Every rhyme family gets its own color. All the *AY-T* words, the *tonight / light / flight* cluster, share one hue. The next family gets a different one. There's a sixteen-color palette, and colors get assigned least-used-first, so they spread evenly across a verse and two adjacent families never collide into the same shade. You glance at a page and the sound groups separate themselves out by color, the way they already separate themselves out by ear.

Then there's the part I think is the best feature in the whole app: brightness is rhyme strength.<label for="sn-gradient" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-gradient" class="margin-toggle"/><span class="sidenote">It's a continuous gradient, not an on/off switch. Two words don't just rhyme or not rhyme. They rhyme to a degree, and the page renders the degree. This is closer to how hearing actually works than any binary classification.</span> Perfect rhymes blaze. Slant rhymes sit back. Consonance, the faintest kind of echo, barely glows at all. And the gradient runs *inside* a family too: the perfect anchors of a cluster burn brighter than the loose slant words that have attached themselves to the edges of it.

The effect is that a verse becomes legible at a glance. Bright is where you locked it. Faint is where you're still reaching. You can see the shape of your own craft without reading a single word, the way a producer reads a waveform.

A few quieter signals layer on top. The rhyming word takes a soft tint of its family color, sitting on a translucent block of the same color, so the signal comes through two channels at once. A faint underline marks the exact rhyming tail of a word, the *ight* under *tonight*, so you can see not just that two words rhyme but where the rhyme actually lives. Hover over any word and its entire family brightens across the whole page at once, every relative lighting up together, then settles back when you move away.

There are toggles for three lenses: rhyme, alliteration, rhythm. Alliteration underlines shared head-sounds. Rhythm drops a row of dots under the words, sheet music for rapping, where a shared dot color means a shared cadence. You turn on what you need and leave the rest off.

## How it listens

Under the visual language is an engine that has to actually hear the words. That's the hard part, and it's most of the code in `app.py`.

Every word gets mapped to its phonemes through the CMU Pronouncing Dictionary, reached with the [`pronouncing`](https://pypi.org/project/pronouncing/) library, plus a stack of lyric-friendly fallbacks for the way people actually write. `runnin'` resolves to *running*. Possessives get unwound. Made-up words, which lyrics are full of, fall through to [`g2p-en`](https://pypi.org/project/g2p-en/), a neural grapheme-to-phoneme model that sounds out a word the dictionary has never seen, so the page doesn't go silent the moment you invent one.

Then a multi-pass pipeline walks the phonemes looking for structure, strongest kind first:

```
night   →  N AY1 T     ┐
light   →  L AY1 T     ├─  perfect:  AY-T
flight  →  F L AY1 T   ┘

hold    →  HH OW1 L D  ┐
coal    →  K OW1 L     ┴─  slant:    OW (vowel only)
```

Perfect rhymes share everything from the last stressed vowel onward, and they're matched anywhere in a line, not just at the end, which is how the internal-rhyme detection falls out of the same logic for free. Then end slant rhymes, sharing just the vowel of the tail. Then the multisyllabic and mosaic and cross-word phrases, the buried interlocks: *orange* against *door hinge*, or *swimmers / finisher / commissioner* pulled together into one family across word boundaries. Then consonance, then the weakest endings last.

Around all of that sits a layer of judgment. Rhymes don't cross stanza breaks, because a blank line is a wall the ear respects. Vowel families have to stay local, within about eight lines, because two matching vowels a hundred lines apart aren't a rhyme anyone hears, they're a coincidence. Refrains that repeat four or more times get muted so the chorus doesn't drown out the verse. Dialect mergers get folded in, so the engine treats the small inflections of real speech as transparent.

The thing I'm proudest of is the taste.<label for="sn-taste" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-taste" class="margin-toggle"/><span class="sidenote">Naive vowel-matching produces a page that lights up everywhere and means nothing. The whole game is suppression: knowing what to *not* call a rhyme. Most of the regression tests exist to defend a single word that was lighting up when it shouldn't.</span> It knows *garbage* and *javascript* don't rhyme, because the codas don't match. It knows *middle* and *unavoidable* don't, because a bare schwa tail isn't enough. It knows *smell like a* doesn't rhyme off that dangling article. The engine errs, deliberately, toward the rhymes a listener actually hears, not the ones a vowel chart says are technically present.

## The tests are the spec

Most of the engine is pass ordering. The pipeline walks the phonemes looking for perfect rhymes first, then slant, then the multisyllabic and cross-word phrases, then consonance, and each pass can claim a word the next one wanted. Move consonance ahead of slant and half the page lights up wrong. Nearly every real bug lives in that ordering, not in the phoneme matching underneath it. The matching is arithmetic. The ordering is judgment, and judgment is where things break.

There is no formula for "a rhyme a listener actually hears." You can't derive it from first principles, because it isn't a principle, it's a thousand small human verdicts. So I built it the only way that holds: against real verses, one correction at a time. I'd paste in a verse, find the single word lit the wrong color, fix the engine until it was right, and then, before touching anything else, freeze that exact verse into a regression test.<label for="sn-spec" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-spec" class="margin-toggle"/><span class="sidenote">This is the inversion of normal spec-driven work. There was no spec to implement first. The corpus of real verses *became* the spec, accreting one judgment at a time. Every test is a frozen sentence that says: these words rhyme, those don't, and here is the proof.</span> There are around eighty-two of those now, each one a real bar from a real song, validated against people who do this for a living: Lil Wayne, Eminem, MF DOOM, Drake, Big Sean, Kanye, with T.S. Eliot and Tool folded in so the ear behind the engine wasn't tuned for only one tradition. The hardest single test is DOOM's "Doomsday," about the densest interlocking rhyme in recorded rap. It doesn't break the engine. The families separate cleanly and you can watch the architecture DOOM built by ear hold together exactly the way it sounds like it should.

That suite is the only reason the thing works at all. The whole app was [vibe coded](/essays/2026-04-10-the-hacker-ethic-and-the-vibe-coder), every line written by describing what I wanted to Claude Code and steering, never typed by hand. I love working that way, but a rhyme engine is exactly where it should fall apart, because the tuning is the worst kind of fiddly: a fix that catches one rhyme quietly breaks three others ten verses away, and you would never catch it by eye.<label for="sn-net" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-net" class="margin-toggle"/><span class="sidenote">This is the part of vibe coding nobody oversells enough. The model is happy to make a confident change that breaks something subtle three files over, and it will tell you it's fine. The test suite is what converts that confidence into something you can actually trust, because it answers, in a second, the only question that matters: did this quietly wreck something that used to work.</span> Vibe coding without tests on a problem this subtle would be building on sand. With the suite under it, every change to pass ordering got an instant green-or-red answer. I could let the AI rewrite an entire pass and know within a second whether I'd just regressed Eminem. The tests are what kept the vibe coding honest. They turned a domain that punishes confidence into one where I could move fast without lying to myself.

## The keepers earn their place

Here's the part of building it that taught me the most, and it's not a feature. It's everything that isn't one.

I kept building elaborate things and then cutting them back to the simplest version that felt right.<label for="sn-subtraction" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-subtraction" class="margin-toggle"/><span class="sidenote">This is the design rhythm I trust most by now: build the full ornate version, live with it long enough to feel what it costs, then strip it to the one move that earned its keep. You can't always see the keeper until you've built the thing around it that doesn't work.</span> There was a constellation weave, glowing threads drawn through every member of a rhyme family across the page. I built the whole thing. It was beautiful and it was noise. I stripped it down to the hover-illuminate, which does the same job, find the family, with none of the clutter. Grammar and part-of-speech highlighting got tried three different ways and removed all three times. Beat-arcs, right-margin connectors, dual-family coloring on words that belong to two clusters at once: built, then cut.

Every cut made the app better. The features that survived survived because they earned it, and the ones that didn't were taking attention away from the verse, which is the only thing on the page that matters. With AI you can build the elaborate version fast enough that subtraction becomes the real design work. The keystroke is cheap now. Knowing what to delete is the whole skill.

## What it's for

RhymePad doesn't write your verse. I want to be clear about that, because it's the whole philosophy. It won't finish your line or suggest your next bar or generate a hook. The closest it comes is a dotted-gold mark on a dead line ending that sits one phoneme short of a rhyme, and even that only points at a gap you made and trusts you to fill it.

What it does is show you your own work. The rhymes you locked, the ones you're reaching for, the buried interlock you put there by instinct without quite knowing you'd done it. It takes the thing your ear already knew and renders it where your eye can finally see it, so you can edit with both at once. It's of a piece with the [poetry platform I built for Sarah](/software/websites/poemsbysarah), and with [everything I keep coming back to](/essays/2026-01-30-the-becoming-building-a-poetry-publishing-pipeline-with-claude-code): the machine handles the *how*, the human keeps the *what* and the *why*, and the craft stays yours.

The ear always knew the architecture was there. The page just learned how to listen.

---

*RhymePad is live at [rhymepad.org](https://rhymepad.org). More on the project [here](/software/websites/rhymepad).*

*June 2026*

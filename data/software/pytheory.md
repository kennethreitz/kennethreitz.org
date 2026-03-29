# PyTheory: Music Theory for Humans

PyTheory is a Python library for exploring music theory and making music computationally. Notes, scales, chords, fretboards, drum patterns, synthesis, effects, sequencing, and export — all from the Python REPL.

    $ pip install pytheory

## Theory

```python
from pytheory import TonedScale, Chord, Fretboard, Key

# Scales across six musical systems.
c_major = TonedScale(tonic="C4")["major"]
hijaz = TonedScale(tonic="Do4", system="arabic")["hijaz"]
bhairav = TonedScale(tonic="Sa4", system="indian")["bhairav"]

# Chord detection from guitar fingerings.
fb = Fretboard.guitar()
chord = fb.fingering(0, 1, 0, 2, 3, 0).to_chord(fb)
print(chord.identify())  # 'C major'

# 25 instrument presets — guitar, bass, oud, sitar, shamisen, erhu...
oud = Fretboard.oud()
banjo = Fretboard.banjo()

# Key detection.
key = Key.detect("C", "E", "G", "A", "D")  # <Key C major>
```

## Composition

```python
from pytheory import Score, Duration, Pattern, play_score

score = Score("4/4", bpm=140)

# 58 drum presets, all synthesized from scratch.
score.drums("bossa nova", repeats=4)

# Parts with per-voice synth, envelope, and effects.
bass = score.part("bass", synth="sine", envelope="pluck",
                  volume=0.6, lowpass=800)
bass.add("A2", Duration.HALF).add("D2", Duration.HALF)

pad = score.part("pad", synth="supersaw", envelope="pad",
                 volume=0.3, reverb=0.6, chorus=0.4)
pad.add("Am", Duration.WHOLE).add("Dm", Duration.WHOLE)

lead = score.part("lead", synth="saw", envelope="pluck",
                  reverb=0.3, delay=0.25, lowpass=2000)
lead.add("E4", Duration.QUARTER).add("G4", Duration.QUARTER)
lead.set(lowpass=3000)  # mid-song automation
lead.add("A4", Duration.HALF)

# LFO automation.
lead.lfo("lowpass", rate=0.125, min=400, max=3000, bars=8)

# Arpeggiator with legato and portamento.
arp = score.part("arp", synth="square", envelope="pluck",
                 legato=True, glide=0.05)
arp.arpeggio("Cm", bars=2, pattern="updown",
             division=Duration.SIXTEENTH, octaves=2)

play_score(score)

# Export.
score.save_midi("track.mid")
```

10 synth waveforms. 8 ADSR envelopes. 27 synthesized drum sounds. Effects chain per part: distortion, chorus, lowpass, delay, reverb. WAV and MIDI export.

## The Story

I built this for myself. Nobody asked for it. There's no market for a Python music theory library. But it sits at the intersection of my two longest-running interests — programming and music — and working on it feels like the reason I learned to code in the first place.

It started as scales and chords. Then I wanted to hear what I was modeling, so I added synthesis. Then drums, effects, automation, sequencing. Each step was the obvious next thing, and the architecture absorbed it without complaining.

The "for humans" philosophy applied to a domain where the theory has always been more intimidating than the practice.

## Install

```bash
$ pip install pytheory
```

## Resources

- [Documentation](https://pytheory.kennethreitz.org/)
- [Source Code on GitHub](https://github.com/kennethreitz/pytheory)
- [Python Package Index](https://pypi.org/project/pytheory/)

## Related

- [**PyTheory Is Awesome**](/essays/2026-03-25-pytheory_is_awesome) — On chord detection, world music systems, and why the quietest library means the most.
- [**A Mini DAW in the Python REPL**](/essays/2026-03-25-a_mini_daw_in_the_python_repl) — Building a track from scratch with drums, synthesis, effects, and automation.
- [**PyTheory: Breaking Through Five Years of Creative Block with AI**](/essays/2026-03-22-pytheory_breaking_through_five_years_of_creative_block_with_ai) — The full story of how this library came together.

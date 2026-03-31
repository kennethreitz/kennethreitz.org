# Free Teenage Engineering OP-XY Sample Packs, from Math
*March 2026*

I made a free sample pack for the **Teenage Engineering OP-XY** and **OP-1**. 69 multisampled instruments and 12 drum kits, all generated from [PyTheory](https://pytheory.kennethreitz.org)'s [synthesis engine](/essays/2026-03-29-numpy_as_synth_engine). No recordings. Just math.

The whole thing is on GitHub: [pytheory-opxy](https://github.com/kennethreitz/pytheory-opxy).

## What You Get

69 instruments, each sampled at 6 points across the keyboard — piano, electric piano, wurlitzer, organ, harpsichord, celesta, music box, violin, viola, cello, contrabass, string ensemble, flute, clarinet, oboe, bassoon, sax (soprano through bari), trumpet, trombone, french horn, tuba, brass ensemble, acoustic guitar, electric guitar (five flavors from clean to metal), bass, upright bass, harp, sitar, pedal steel, banjo, mandolin, mandola, ukulele, koto, marimba, vibraphone, xylophone, glockenspiel, tubular bells, timpani, crotales, tingsha, singing bowl, kalimba, steel drum, synth lead, synth pad, synth bass, acid bass, 808, granular pad, vocal, choir, theremin, harmonium, accordion, didgeridoo, bagpipe.

12 drum kits — standard GM, latin, world, tabla, dhol, mridangam, djembe, doumbek, cajón, metal, marching, and effects. The tabla kit alone has seven distinct strokes. The world kit has djembe, doumbek, cajón, and rainstick all in one place.

Each instrument is set up properly — legato for theremin, mono for winds, looping for bowed strings, longer samples for slow decays. They're ready to play, not just raw waveforms.

## How to Install

You don't need Python or a terminal. Just:

1. Go to [github.com/kennethreitz/pytheory-opxy](https://github.com/kennethreitz/pytheory-opxy).
2. Click the green **Code** button → **Download ZIP** (~130 MB).
3. Unzip it and copy the folders to your device:

| Device | Copy this | To here |
|--------|-----------|---------|
| **OP-XY** | `opxy-samples/pytheory/` | `/presets/pytheory/` |
| **OP-XY** | `opxy-samples/pytheory-drums/` | `/presets/pytheory-drums/` |
| **OP-1 / OP-1 Field** | `op1-samples/pytheory/*.wav` | `/synth/user/` |

[Field Kit](https://teenage.engineering/apps/field-kit) makes the OP-XY transfer easy — drag and drop.

## Why Free

Sample packs typically run $20-50 each. That's fine for a few, but if you want a broad palette — orchestral, world percussion, synths, plucked strings — it adds up. And you're locked into whatever the producer recorded. Want a different tuning? A longer sustain? A sitar with more resonance? Buy another pack.

This one is generated from code. Don't like something? Change a parameter and re-run:

```bash
uv add pytheory numpy scipy
python generate.py           # instruments
python generate_drums.py     # drum kits
```

The sounds won't fool anyone into thinking they're hearing a real Steinway. That's not the point. The point is having 69 playable instruments and 12 drum kits on your OP-XY for free, right now, with the ability to regenerate or customize any of them.

~180 MB of audio. ~600 lines of Python. $0.

[Source code on GitHub](https://github.com/kennethreitz/pytheory-opxy).

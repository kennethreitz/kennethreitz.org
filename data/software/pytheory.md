# PyTheory: Music Theory for Humans

PyTheory is a Python library for exploring music theory computationally. Notes, scales, chords, intervals, and temperaments, all represented as Python objects you can inspect and manipulate.

    $ uv pip install pytheory

## What It Looks Like

```python
from pytheory import TonedScale

# Create a C minor scale.
c_minor = TonedScale(tonic="C4")["minor"]
print(c_minor)
# <Scale I=C4 II=D4 III=Eb4 IV=F4 V=G4 VI=Ab4 VII=Bb5 VIII=C5>

# Get the frequency of a note.
c_minor[0].pitch()
# 523.251130601197

# Get the symbolic pitch representation.
c_minor["I"].pitch(symbolic=True)
# 440*2**(1/4)

# Try Pythagorean temperament.
c_minor["tonic"].pitch(temperament="pythagorean", symbolic=True)
# 14080/27
```

Play notes directly from the command line:

```bash
$ pytheory play C4 E4 G4
```

The `symbolic` parameter is the part I find most fascinating. Instead of just calculating a frequency, it shows you the mathematical relationship. Music is math made audible, and PyTheory lets you see both sides.

## The Story

This project is highly experimental. It's more of a thought exercise than a production library. I built it to explore how music theory concepts translate into code, and it ended up teaching me more about music theory than any textbook.

Scales become lists you can index. Intervals become arithmetic. Temperaments become parameters. When you can query a chord the same way you'd query a database, the underlying structure of music becomes tangible in a way that sheet notation doesn't capture.

It sits at the intersection of my two longest-running interests: programming and music. The "for humans" philosophy applied to a domain where the theory has always been more intimidating than the practice.

## Install

```bash
$ uv pip install pytheory
```

## Resources

- [Documentation](https://pytheory.kennethreitz.org/)
- [Source Code on GitHub](https://github.com/kennethreitz/pytheory)
- [Python Package Index](https://pypi.org/project/pytheory/)

## Related

- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — Code as a lens for understanding the world.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The "for humans" philosophy applied beyond software.

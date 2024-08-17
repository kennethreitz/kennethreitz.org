# PyTheory: Music Theory for Humans

[`pytheory`](https://github.com/kennethreitz/pytheory) is a Python library that simplifies working with music theory concepts. It provides a simple and intuitive interface for representing musical elements such as notes, scales, chords, and intervals, making it easier to work with music theory in Python.

## Features

- **Note Representation**: PyTheory allows you to represent musical notes using the standard Western notation (`A`, `Bb`, `C#`, etc.), enabling you to work with notes in different formats.
- **Scale Generation**: The library provides functions for generating scales based on different modes, such as major, minor, pentatonic, and blues scales, allowing you to explore different musical scales.
- **Chord Construction**: PyTheory supports constructing chords from notes, intervals, or scale degrees, making it easy to create and analyze chords in different keys.
- **Interval Calculation**: The library allows you to calculate intervals between notes, enabling you to determine the distance between two pitches in a musical context.

This project is highly experimental, and is more of a thought exercise than a practical library. It aims to explore how music theory concepts can be represented and manipulated using Python, and to provide a foundation for further research and development in this area.

## Installation

You can install `pytheory` using pip:

```bash
$ pip install pytheory
```

## Usage

Create a `Note` object:

```pycon
>>> import pytheory

>>> c_minor = TonedScale(tonic='C4')['minor']
>>> c_minor
<Scale I=C4 II=D4 III=Eb4 IV=F4 V=G4 VI=Ab4 VII=Bb5 VIII=C5>

>>> c_minor[0].pitch()
523.251130601197

>>> c_minor["I"].pitch(symbolic=True)
440*2**(1/4)

>>> c_minor["tonic"].pitch(temperament='pythagorean', symbolic=True)
14080/27
```

I'm not sure if this is useful, but it's fun to play with, and it has enhanced my understanding of music theory— especially the `symbolic` parameter.

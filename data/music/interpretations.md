# Interpretations
*2025* — [interpretations.kennethreitz.org](https://interpretations.kennethreitz.org/)

A full-length album of 24 original compositions, written in Python through human-AI collaboration. Every track composed in code using [pytheory](https://github.com/kennethreitz/pytheory), a music theory and synthesis library I built for this purpose — with Claude as creative partner throughout the process.

The album is the answer to a question I've been asking for years: what happens when you treat Python not as a tool for making music, but as the instrument itself? And what happens when you bring AI into the composing room?

![Interpretations album cover](/static/images/interpretations-cover.png)

Twenty-four tracks. Ninety minutes. A singing bowl with a quarter-inch cable plugged into it — that's the whole idea. Ancient instruments rendered through modern synthesis, sacred geometry floating above the waveform. Everything on this record was born in a Python script.

![Interpretations player](/static/images/interpretations-player.png)

## The Sound

Interpretations spans Indian classical raga, acid house, lo-fi hip hop, ambient drone, trap, drum and bass, and a few things that don't have names yet. The tracklist is a journey — opening with a sitar raga over 808s, climbing through electronic energy, descending into raw emotional territory, then dissolving into sacred space before finally settling into silence.

Three tuning systems live side by side: standard Western equal temperament for the electronic tracks, 22-tone shruti intonation for the Indian classical pieces, and just intonation for the meditative closers. Some tracks run at A=432Hz. The tuning is part of the composition, not an afterthought.

Reverb is treated as an instrument. The Taj Mahal impulse response appears on nearly every melodic part — it's the signature acoustic space of the record. Cathedral reverb for the organ pieces. Algorithmic reverb for tight electronic production.

## The Process

Every track is a Python file. A `Score` object defines the time signature and tempo. `Part` objects define instruments with their effects chains. Notes are added one at a time — pitch, duration, velocity. Drum patterns are step sequences. Filter sweeps are LFO automations. There is no DAW, no MIDI, no audio samples. The Python script *is* the score, and pytheory renders it to audio.

The compositions were written collaboratively with Claude — I'd describe what I wanted to hear, the mood, the genre, the arc, and we'd build the score together in conversation. Musical direction and creative vision are mine. The note-by-note Python code that realizes that vision was written through dialogue. It's a new kind of composition process — closer to directing than performing, but deeply involved at every level.

```bash
uv run play              # Interactive player
uv run play tracks/raga_midnight.py   # Play a specific track
```

The interactive player is a curses TUI that shows the full tracklist with keys, tempos, and tuning systems. It renders tracks to WAV on first play, then caches them for instant playback.

## Why Python

Twenty years of drums. A studio full of analog synthesizers, all sold. An OP-XY for portable sketches. And now this — an album where the composition language is the programming language I've spent my career thinking in.

Python is how I think. And Claude understands Python the way I do — as a language for expressing ideas clearly. Together, we can move from "I want a sitar raga that drops into 808s" to a fully realized composition faster than I could alone, without losing the specificity that makes each track what it is.

The same philosophy that made [Requests](/software/requests) feel obvious — that tools should match human mental models — applies here. pytheory's API is designed so that writing music reads like describing music. A sitar plays a note in D Phrygian with shruti tuning and Taj Mahal reverb. That's what the code says, and that's what you hear. The AI collaboration layer sits on top of that — another tool that matches how I think about music.

## Listen

Available now on [Spotify](https://open.spotify.com/album/1jYjggrr6HEKfV4FchcJWD), [Apple Music](https://music.apple.com/us/album/interpretations/1890986989), and all major streaming platforms.

The source code is the album. Clone the repo, run the player, read the scores. The music and the code that creates it are the same artifact.

- [Official Site](https://interpretations.kennethreitz.org/)
- [GitHub](https://github.com/kennethreitz/interpretations)
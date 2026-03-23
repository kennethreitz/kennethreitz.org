import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", app_title="pytheory playground")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    mo.md(
        """
        # pytheory playground

        Explore music theory with Python. **pytheory** is a music theory library
        that makes theory approachable and fun — treating Python as a musical instrument.

        *Built by [Kenneth Reitz](https://kennethreitz.org) — the same mind behind Requests.*
        """
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Tones & Notes")
    return


@app.cell(hide_code=True)
def _(mo):
    note_input = mo.ui.dropdown(
        options=[
            "C", "C#", "D", "D#", "E", "F",
            "F#", "G", "G#", "A", "A#", "B",
        ],
        value="C",
        label="Note",
    )
    octave_input = mo.ui.slider(
        start=1, stop=7, value=4, label="Octave",
    )
    mo.hstack([note_input, octave_input], justify="start", gap=1)
    return note_input, octave_input


@app.cell
def _(mo, note_input, octave_input):
    from pytheory import Tone as _Tone

    _note_name = f"{note_input.value}{octave_input.value}"
    _tone = _Tone.from_string(_note_name)

    mo.md(
        f"""
        ### {_tone.full_name}

        | Property | Value |
        |----------|-------|
        | Frequency | **{_tone.frequency:.2f} Hz** |
        | MIDI Number | **{_tone.midi}** |
        | Enharmonic | **{_tone.enharmonic or 'N/A'}** |
        | Sharp? | {_tone.is_sharp} |
        | Flat? | {_tone.is_flat} |
        | Natural? | {_tone.is_natural} |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Scales")
    return


@app.cell(hide_code=True)
def _(mo):
    tonic_dropdown = mo.ui.dropdown(
        options=[
            "C", "C#", "D", "D#", "E", "F",
            "F#", "G", "G#", "A", "A#", "B",
        ],
        value="C",
        label="Tonic",
    )
    scale_dropdown = mo.ui.dropdown(
        options=[
            "major", "minor", "dorian", "phrygian",
            "lydian", "mixolydian", "locrian",
            "harmonic_minor", "melodic_minor",
            "pentatonic_major", "pentatonic_minor",
            "blues",
        ],
        value="major",
        label="Scale",
    )
    mo.hstack([tonic_dropdown, scale_dropdown], justify="start", gap=1)
    return tonic_dropdown, scale_dropdown


@app.cell
def _(mo, tonic_dropdown, scale_dropdown):
    from pytheory import TonedScale as _TonedScale

    _toned = _TonedScale(tonic=f"{tonic_dropdown.value}4")
    try:
        _scale = _toned[scale_dropdown.value]
        _notes = _scale.note_names
        mo.md(
            f"""
            ### {tonic_dropdown.value} {scale_dropdown.value}

            **Notes:** {' — '.join(_notes)}

            **Degrees:** {len(_notes)} notes
            """
        )
    except (KeyError, Exception) as e:
        mo.md(f"Scale not available: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Chords")
    return


@app.cell(hide_code=True)
def _(mo):
    chord_input = mo.ui.text(
        value="C E G",
        label="Enter notes (space-separated)",
        placeholder="e.g. C E G B",
    )
    chord_input
    return (chord_input,)


@app.cell
def _(mo, chord_input):
    from pytheory import Chord as _Chord

    _chord_notes = chord_input.value.strip().split()
    if len(_chord_notes) >= 2:
        try:
            _chord = _Chord.from_tones(*_chord_notes)
            _identity = _chord.identify() or "Unknown"
            _harmony = _chord.harmony
            _dissonance = _chord.dissonance
            _intervals_str = ", ".join(str(i) for i in _chord.intervals)

            mo.md(
                f"""
                ### {_identity}

                | Property | Value |
                |----------|-------|
                | Notes | **{', '.join(_chord_notes)}** |
                | Intervals (semitones) | **{_intervals_str}** |
                | Harmony (consonance) | **{_harmony:.3f}** |
                | Dissonance (roughness) | **{_dissonance:.3f}** |

                *Higher harmony = more consonant. Higher dissonance = more rough/tense.*
                """
            )
        except Exception as e:
            mo.md(f"Error: {e}")
    else:
        mo.md("Enter at least 2 notes to analyze a chord.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Key Explorer")
    return


@app.cell(hide_code=True)
def _(mo):
    key_tonic = mo.ui.dropdown(
        options=[
            "C", "C#", "D", "D#", "E", "F",
            "F#", "G", "G#", "A", "A#", "B",
        ],
        value="C",
        label="Key",
    )
    key_mode = mo.ui.dropdown(
        options=["major", "minor"],
        value="major",
        label="Mode",
    )
    mo.hstack([key_tonic, key_mode], justify="start", gap=1)
    return key_tonic, key_mode


@app.cell
def _(mo, key_tonic, key_mode):
    from pytheory import Key as _Key

    current_key = _Key(key_tonic.value, key_mode.value)

    _notes_str = ", ".join(current_key.note_names)
    _chords_str = ", ".join(current_key.chords) if current_key.chords else "N/A"
    _sig = current_key.signature
    _relative = current_key.relative
    _parallel = current_key.parallel

    mo.md(
        f"""
        ### Key of {key_tonic.value} {key_mode.value}

        **Notes:** {_notes_str}

        **Signature:** {_sig}

        **Diatonic Chords:** {_chords_str}

        **Relative key:** {_relative}

        **Parallel key:** {_parallel}
        """
    )
    return (current_key,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Chord Progressions")
    return


@app.cell(hide_code=True)
def _(mo):
    prog_input = mo.ui.text(
        value="I V vi IV",
        label="Progression (Roman numerals)",
        placeholder="e.g. I V vi IV",
    )
    prog_input
    return (prog_input,)


@app.cell
def _(mo, current_key, prog_input):
    _numerals = prog_input.value.strip().split()
    if _numerals:
        try:
            _progression = current_key.progression(*_numerals)
            _rows = []
            for _numeral, _ch in zip(_numerals, _progression):
                _ch_name = _ch.identify() or "?"
                _ch_notes = ", ".join(t.full_name for t in _ch.tones)
                _rows.append(f"| {_numeral} | {_ch_name} | {_ch_notes} |")

            _table = "\n".join(_rows)
            mo.md(
                f"""
                ### Progression: {' → '.join(_numerals)}

                | Numeral | Chord | Notes |
                |---------|-------|-------|
                {_table}
                """
            )
        except Exception as e:
            mo.md(f"Error building progression: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Guitar Fretboard")
    return


@app.cell(hide_code=True)
def _(mo):
    tuning_dropdown = mo.ui.dropdown(
        options=["standard", "drop d", "open g", "open d", "dadgad"],
        value="standard",
        label="Tuning",
    )
    fret_inputs = mo.ui.array(
        [mo.ui.number(start=0, stop=24, value=0, label=f"String {i+1}") for i in range(6)]
    )
    mo.vstack([tuning_dropdown, mo.md("**Fret positions** (high E to low E):"), fret_inputs])
    return tuning_dropdown, fret_inputs


@app.cell
def _(mo, tuning_dropdown, fret_inputs):
    from pytheory import Fretboard as _Fretboard

    _fb = _Fretboard.guitar(tuning_dropdown.value)
    _frets = tuple(int(f.value) for f in fret_inputs)

    try:
        _fingering = _fb.fingering(*_frets)
        _fret_chord = _fingering.chord()
        _fret_name = _fret_chord.identify() or "Unknown"
        _tones_str = ", ".join(t.full_name for t in _fingering.tones)

        mo.md(
            f"""
            ### {_fret_name}

            **Tuning:** {tuning_dropdown.value}

            **Frets:** {_frets}

            **Notes sounding:** {_tones_str}
            """
        )
    except Exception as e:
        mo.md(f"Error: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---

        *Powered by [pytheory](https://github.com/kennethreitz/pytheory)
        and [marimo](https://marimo.io).
        Explore the source at [kennethreitz.org/software/pytheory](https://kennethreitz.org/software/pytheory).*
        """
    )
    return


if __name__ == "__main__":
    app.run()

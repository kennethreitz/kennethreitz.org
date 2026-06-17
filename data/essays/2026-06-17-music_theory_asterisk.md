# Music Theory, Asterisk

*June 2026*

There is a silent asterisk after the words *music theory*. You never see it printed, but it is always there, the way it hangs after *the canon* or *the great novels*. When someone says music theory they mean one specific thing, and we have quietly agreed not to say the specific part out loud. Western. Tonal. Roughly 1700 to 1900. Twelve equal-tempered keys. Two staves. Mostly European, mostly men, mostly gone. All of it is real and most of it is beautiful and I have spent my life inside it. It is also one theory, of one music, from one place, paused at one moment, wearing the name of the whole.

The asterisk is where the rest of the world's music went.

I have been writing a [music theory library](/software/pytheory) since 2018, and refusing that asterisk was the point from the start. The tagline on day one was *Music Theory for Humans*. The very first code example in the very first README did not strike a key on a piano. It computed a single pitch two ways: in equal temperament as 440 times the fourth root of two, and in Pythagorean tuning as the exact fraction 14080 over 27. No keyboard. No default. Just the arithmetic of a vibrating string, with the temperament left as a parameter, because that is what a temperament actually is: a choice somebody made about how to divide an octave, not a law of nature. The piano was never the ground. It was only ever one of the options.

What I could not do, for a long time, was fill the frame in. The architecture had room for any tuning system on earth and I had implemented almost none of them. I was [stuck on this library for five years](/essays/2026-03-22-pytheory_breaking_through_five_years_of_creative_block_with_ai), holding a structure built for the whole world with a handful of Western scales hanging in it. The break, when it finally came, came in collaboration, the same way most of the hard things this year have. I could see the whole building. I needed help laying the floors. So when a friend who plays Hindustani classical music asked for ragas in the tuning they are actually sung in, it was not a revelation about my own blind spots. It was a promise coming due. [I have written about that one note already.](/essays/2026-06-17-conducting_between_roller_coasters) The frame had been waiting for it since 2018.

Here is the thing the design knew before I could deliver on it. The asterisk has a second meaning.

In prose the asterisk is a footnote. It means *with exceptions, see below, not really, terms apply*. In code it means the opposite. `from music import *` means everything, no exceptions, the whole namespace with nothing held back. The same little star, two readings, pointing in exactly opposite directions. One says *almost*. The other says *all*.

The whole ambition of the library, from that first symbolic pitch, was to turn the first asterisk into the second.

## How far down it goes

It starts where everyone starts. Notes, intervals, scales, the major and minor keys, the chords you build by stacking thirds. That is the lobby. Everyone expects the lobby.

Then it goes down. Functional harmony, the grammar of tension and release, Roman numerals that know a V7 wants to go home. Reharmonization, the substitutions a jazz player reaches for half-asleep, including negative harmony, the Ernst Levy mirror that hands you back a chord's shadow. Keep going. Neo-Riemannian theory, the P, L, and R moves that let a film score slide between far-apart chords with no key in sight, the Tonnetz paths drawn between them like a subway map. Twelve-tone rows and their full forty-eight-form matrices, music engineered to have no home at all. Pitch-class set theory, prime forms and Forte numbers and interval vectors, the math that lets you say something precise about a fistful of notes nobody would ever call a chord. And that is still only the Western floor. Most curricula stop here and call it the building.

Then the library turns sideways, into the direction the asterisk was always hiding. Thirty-six Hindustani ragas, voiced off the twenty-two shrutis so the notes land where they are sung and not where the keyboard insists. The seventy-two melakarta of Carnatic music. The quarter-tone maqam of Arabic music, where the pitches between the piano's pitches are not errors to be rounded away but the entire reason the music sounds like itself. Gamelan, in slendro and pelog, tunings that do not even pretend to carve the octave the way a Western keyboard does. None of these are filed under *world music*, because *world music* is not a genre. It is just most of the world, asterisked.

Then it goes down again. Rhythm as a first-class citizen and not the thing you wave at on the way to harmony, with time signatures, drum kits, swing, and a deliberate, dialed-in human imprecision, because a grid that never breathes is its own small lie. I started on drums, and rhythm is the asterisk's own asterisk, the part even the theory class skips on its way to the harmony, which is to say the piano. There is a real satisfaction in putting a drum pattern and a Neapolitan chord in the same box and not saying which one is the serious one.

And it keeps opening. The library grows a body: a synthesizer written in NumPy, sample by sample, with convolution reverb, a stereo master bus, a soft-knee limiter, so all of this theory can actually make a sound in the air. Then it learns to read and write: MIDI in and out, ABC notation, real engraved sheet music through LilyPond, and the reverse trick, listening to audio and writing down what it heard. Then it learns to perform: a metronome that trains your tempo, a guitar tuner that tracks your string in real time, a live terminal interface, a REPL that is quietly a small DAW, a clock that locks to Ableton so it can sit inside a real session. Then it grows doors so you do not have to be a programmer to walk in: a [browser playground](https://playground.pytheory.org), an Ableton extension, a command line that speaks JSON and plays sound.

Every time I am sure I have found the bottom, it turns out to be another floor.

## The asterisk never fully closes

I want to be honest about the part that is not finished, because the honesty is the whole point of the exercise.

There is no counterpoint in the library yet. No species rules, no Bach to argue with. The maqamat have their scales but not their full grammar, the way a raga carries a personality and not just a set of notes. The instruments are synthesized, which means they are honest oscillators doing an impression, and a single bar of a real sampled cello would expose every one of them. And for every tradition I have managed to bring inside, I carry the quiet weight of the ones I have not, the musics I do not yet know well enough to model without flattening, which is its own kind of harm, however carefully meant.

That is what completeness actually is when the subject is music. A horizon. You walk toward it and it keeps its distance. You do not finish. You just shrink the asterisk, one footnote at a time, knowing the work has no last line.

## Why bother

Because of what defaults quietly do to people. A tool that assumes the piano makes everyone who does not think in the piano translate themselves before it will listen. The sitar player rounds her flat third to the nearest white key and loses the exact thing that made it hers. Do it long enough and she stops hearing it as a loss. She starts hearing her own third as the mistake. That is the same quiet tax I have been trying to refund since [a library about HTTP](/software/requests), the one I keep calling *for humans*: the tool should meet you on your own terms, not demand you show up on its.

What we make default, we make true. What we leave in the asterisk, we slowly train people to hear as optional. I sit at a small keyboard deciding which musics are first-class objects and which are footnotes. Every tool has already made that call. Most of them just never admit they made it. [The values you embed are the values you spread.](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) A thing that models music is just code with the volume turned up.

So no, it will never be conclusive. That was never the offer. The offer is an asterisk being slowly argued into a wildcard, one tuning, one tradition, one honest note at a time. Everything. No exceptions. See below, forever.

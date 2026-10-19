---
description: The craft of making things usable. Values propagated through the shape
  of an API, a sentence, a snare roll.
source: obsidian-knowledge
---

# Design

> *"I'm a designer disguised as a programmer."*

---

Design, for me, is the craft of making things usable. Not decoration, not polish, not taste — the actual work of putting a thing into a shape that matches how a person is going to encounter it, and optimizing that shape for the encounter.

`requests` was a design exercise. So was `pipenv`, so was `simplemind`. The code matters less than the interface the code presents, and the interface matters less than the sentence a user silently completes when they reach for the library: *this will work the way I expect.* If that sentence completes, the design is doing its job. If it doesn't, no amount of feature-work recovers.

## What Design Actually Is

Three decisions, stacked. What is the thing for? Who is the thing for? What is the shortest path between them? Everything downstream — architecture, function signatures, error messages, the name of the library — is consequence of those first three decisions made clearly. When the decisions are unclear, the design leaks complexity. When they're clear, the design disappears into the task.

## The 90% Case

The clearest lever I know in interface design is the ninety-percent case. Most people reaching for a tool want the same handful of things, and they want them without ceremony. So the design question is: what is the one thing nearly everyone needs, and can they get it in a single obvious line? With `requests`, the answer was a GET request that returns a response object you can actually read — `requests.get(url).json()` — no opener, no handler, no boilerplate ritual to summon before the real work begins. The advanced cases still exist, but they're where the complexity is *paid for*, not where it's charged up front.

This is not laziness on the user's behalf; it's respect for their attention. Every required step before the useful step is a tax, and taxes compound. Sensible defaults are the mechanism: the library makes the common choice for you and gets out of the way, and only asks you to decide the things that genuinely vary. A default is a value judgment about what most people, most of the time, actually want — which is why choosing defaults well is most of the design.

## Design as Values

Designs carry values whether or not the designer intended them. An API that requires a configuration step for every trivial use communicates that the library doesn't trust the user. A homepage that asks three questions before showing content communicates that the reader's time is cheaper than the publisher's. Even the error messages carry values: a stack trace that blames the user for holding it wrong is a different moral posture than one that says, in plain language, what went wrong and what to try. These are value decisions being made at the interface layer, dressed up as defaults.

The [For Humans](/knowledge/philosophy/for-humans) philosophy is an attempt to name this honestly: if you're building a tool, you're implicitly choosing what the tool values. Optimize for the user's attention and the design comes out humane. Optimize the other way and you build something that extracts. This is the same fault line the Algorithm Eats series traces at civilizational scale — the difference between a design that serves the person in front of it and one that mines them.

## Design in the Small

The macro decisions — what, who, shortest path — express themselves in a thousand tiny ones. The name of a function is design. The order of its arguments is design. Whether the common parameter is positional or hidden three keywords deep is design. A well-named thing is half-documented before anyone writes the docs, because the name already tells you what to expect and the behavior confirms it. When name and behavior agree, the tool feels honest; when they diverge, every user pays a small confusion tax forever.

Documentation is part of the surface too, not an afterthought bolted on once the code works. If the quickstart can't show the ninety-percent case in the first screen, the design underneath is probably too complicated. Good docs are often a design review in disguise — the moment you try to explain the simple case and can't do it simply, the interface is telling you something.

## Design vs. Engineering

Engineering is making the thing work. Design is making the thing worth making. Both are necessary. Engineering without design produces tools that are correct and hostile. Design without engineering produces mockups and pitch decks.

My trade, practically, has been engineering used as the medium for design work. [Python](/knowledge/technology/python) turned out to be a good medium for that — readable enough that interface-level choices survive into the implementation, flexible enough that you can iterate quickly. Other people write Python to solve problems; I write Python to design tools that solve problems.

## Related

- [For Humans](/knowledge/philosophy/for-humans) — The values this craft carries
- [Python](/knowledge/technology/python) — The medium I've mostly used
- Open Source — The distribution model
- [Hacker Ethic](/knowledge/technology/hacker-ethic) — The cultural inheritance
- [Conference Speaking](/knowledge/technology/conference-speaking) — Where the design philosophy gets evangelized
- [Cadence](/knowledge/key-concepts/cadence) — Rhythm as design in the small

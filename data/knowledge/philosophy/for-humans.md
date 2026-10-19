---
description: The design philosophy — Sensible defaults, human-readable, the 90% case
source: obsidian-knowledge
---

# For Humans

> *The design philosophy — Sensible defaults, human-readable, the 90% case*

---

## Overview

"For Humans" is Kenneth's core design philosophy — the belief that tools should serve human cognition rather than demanding humans adapt to machine logic. It originated with requests ("HTTP for Humans") and has since become the thread running through everything he touches: simplemind ("AI for Humans"), pipenv, this vault, the way he writes prose, the way he thinks about living.

It is not minimalism for its own sake. It is clarity as an act of respect for the human on the other end.

---

## The Core Principle

> "I don't actually consider myself to be a good programmer. I consider myself to be a good designer disguised as a programmer."

The insight: technical problems often aren't technical at all — they're design problems. The code works; it just doesn't work *for humans*. Kenneth came to programming through design, and that origin story explains everything. A designer looks at a screen and asks, "What does the person sitting here need?" A programmer looks at a screen and asks, "What does this system require?" The difference is who you center. Kenneth centers the person, every time.

---

## Key Tenets

### Sensible Defaults
Things should work out of the box. The common case shouldn't require configuration.

```python
# Bad: Requires configuration to do anything
client = HTTPClient(timeout=30, retries=3, verify_ssl=True)
response = client.get(url)

# Good: Sensible defaults, just works
response = requests.get(url)
```

### Progressive Disclosure
Simple things should be simple. Complex things should be possible.

The 90% use case gets the clean API. The 10% edge cases are still supported — just not at the expense of the common path.

### Human-Readable
Code should read like intention. APIs should speak human language.

```python
# Bad: Technical jargon
conn.send(Method.GET, URI(url), Headers(), Body(None))

# Good: Natural language
requests.get(url)
```

### Minimize Cognitive Load
Every decision the user doesn't have to make is a gift. Every concept they don't have to learn is freedom.

---

## Application Across Domains

| Domain | Application |
|--------|-------------|
| **requests** | HTTP that reads like English |
| **pipenv** | Package workflow without juggling tools |
| **simplemind** | AI without framework complexity |
| **This vault** | Documentation that serves understanding |
| **Photography** | Black and white removes distraction |
| **Essays** | Philosophy without academic gatekeeping |

The philosophy isn't limited to code — it's a stance toward complexity everywhere.

---

## The Anti-Pattern: Algorithm Eats

The Algorithm Eats essays describe the opposite of "For Humans" — systems optimized for engagement, extraction, and machine goals at human expense.

| For Humans | For Algorithms |
|------------|----------------|
| Serves human flourishing | Optimizes engagement metrics |
| Reduces cognitive load | Exploits cognitive vulnerabilities |
| Respects attention | Captures attention |
| Empowers choice | Manufactures compulsion |

"For Humans" isn't just design preference — it's ethical stance.

---

## Origin Story

Kenneth was trying to build a wrapper for the Convore API. The difficulty of making HTTP requests in Python frustrated him so much that he stopped working on the wrapper and started working on requests instead.

The frustration was the signal. When tools make humans feel stupid, the tools are wrong.

---

## The Designer's Eye

What makes Kenneth effective isn't programming skill — it's the ability to see friction.

Notice when something feels harder than it should. Identify the gap between intention and implementation. Design interfaces that match mental models. Remove everything that doesn't serve the human.

This is design work. The code is just the medium.

---

## The Textual Being

From the Flowetry journal (January 2026):

> *"I am a textual being as well as an animal."*

This insight connects the "For Humans" philosophy to Kenneth's own nature. He works in text — code, documentation, essays, this vault — because he *is* textual. The medium isn't arbitrary; it's native.

| Animal | Textual Being |
|--------|---------------|
| Embodied in flesh | Embodied in language |
| Exists in physical space | Exists in syntactic space |
| Biological rhythms | Communicative rhythms |
| DNA as code | Code as DNA |

The "For Humans" philosophy emerges from someone who lives at the intersection of animal and text — understanding both what bodies need (rest, simplicity, sensible defaults) and what minds need (clear syntax, readable structure, human-centered design).

Related: "Syntax is King, he said." — from the same document. The programmer's reverence for syntactic structure isn't mere technical preference; it's recognition that language-structure *is* thought-structure.

---

## Beyond Code

"For Humans" extends from API design to vault design to life design. Making the complex accessible, removing unnecessary barriers, trusting humans to handle power tools with good defaults.

The philosophy applies to this vault itself. Folders are named what they contain. Index files match their folder names. Things are where you'd expect them to be. If you have to explain the organizational scheme, the scheme is wrong. The same instinct that produced `requests.get(url)` produces a knowledge system where the human doesn't fight the structure to find what they need.

It applies to writing. A comma is sacred, a period is divine. Cadence matters more than comprehension — because if the rhythm is right, the meaning arrives on its own. Kenneth writes prose the way he writes code: remove what's unnecessary, reveal what matters. Every word earns its place or gets cut.

It applies to life. Sensible defaults for daily routines. Progressive disclosure in relationships — simple things simple, complex things possible. The same respect for cognitive load that makes a good API makes a good conversation, a good home, a good day.

---

## Related

- Python Libraries — Where it started
- Flowetry — "I am a textual being"
- Algorithm Eats — The anti-pattern
- [AI Research](/knowledge/ai/ai-research) — Applied to consciousness work
- [Spirituality](/knowledge/spirituality) — Ancient wisdom made accessible
- [Design](/knowledge/technology/design) — The designer's eye
- requests — HTTP for Humans
- simplemind — AI for Humans
- pipenv — Package management for Humans
- Open Source — Community-centered design
- [Python](/knowledge/technology/python) — The language that embodies readability
- [Technology](/knowledge/technology) — Applied context

---

*"HTTP libraries should be for humans, not machines."*

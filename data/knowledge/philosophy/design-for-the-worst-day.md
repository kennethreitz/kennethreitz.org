---
description: If it requires your best self to use, it's not designed for humans.
source: obsidian-knowledge
---

# Design for the Worst Day

> *If it requires your best self to use, it's not designed for humans.*

---

## The Principle

You are having the worst day of your life. Your hands are shaking. Your thoughts refuse to assemble into anything resembling a sequence. You need to do one thing -- pull data from a database, send an email, parse a datetime string -- and the tool you reach for either meets you in that diminished state or it doesn't. Most tools don't. They assume you slept well, that your executive function is online, that you can hold five abstractions in working memory while navigating a configuration ritual before you even get to the thing you came to do. They assume you are at your best. They are wrong.

Design for the Worst Day is the principle that the target user is the person at their cognitive lowest. Not the median user. Not the power user reading documentation on a calm Tuesday with a full cup of coffee. The person whose hands tremble and whose thoughts scatter and who needs the tool to do one thing without making them feel stupid. If it works for that person, it works for everyone. This is not a UX heuristic borrowed from a textbook -- it is a survival lesson that turned out to generalize beautifully to software.

---

## Origin

This principle was born from Kenneth's lived experience with schizoaffective disorder. On bad days, working memory shrinks. Abstract reasoning degrades. Decision fatigue accelerates. Error recovery becomes expensive enough to make you stop entirely. These are not edge cases in a clinical population -- they are the universal human experience of diminished capacity. Depression does this. Anxiety does this. Grief does this. Sleep deprivation does this. Being a new parent does this. Being human, on certain days, does this.

Kenneth built every library he ever shipped by writing the API call he would want to make on his worst day first, before any implementation, before any architecture. The code he would type when his hands are shaking and his brain is fog -- that becomes the interface. Everything else is implementation detail. requests was shaped by this question. So were tablib, records, and maya. The question was always the same: what would this feel like if I couldn't think straight?

The answer to that question produces better software than any amount of user research conducted on people having good days.

---

## Compassion Compiled

The phrase "simple defaults aren't dumbing down -- they're compassion compiled" captures the ethical core of this principle. Every layer of abstraction you force someone through is a filter that eliminates people having bad days. Not by malice. By friction. Each layer costs cognitive energy, and people having bad days have less of it. If you require five steps where two would do, you have decided that three steps worth of people don't matter.

This is why the principle goes beyond UX. When you design for the worst day, you are making a statement about who matters. You are saying that the person who is struggling right now, whose brain is betraying them, whose hands won't stop shaking -- that person deserves to use this tool. That person deserves to get their work done. That person deserves to participate. Most software makes the opposite statement quietly, through accumulated friction, through error messages that accuse rather than assist, through abstraction layers that assume you can hold the whole model in your head.

---

## Universality

The insight that makes this principle powerful is that it is not about accessibility in the narrow sense. It is about the universality of diminished capacity. Curb cuts were designed for wheelchairs and everyone uses them -- people with strollers, people with rolling suitcases, people with bicycles. Worst-day design works the same way. What serves the struggling serves everyone. Steady hands benefit from the same interfaces that trembling hands require. The person having a great day still appreciates that `requests.get(url)` does what it says without ceremony.

LLMs represent the frontier of worst-day design. They accept incoherent fragments -- half-formed intentions smeared across a text box -- and reconstruct the meaning you were trying to express. They do not require grammar. They do not require executive function. They meet you wherever you are. For people with mental health conditions, with ADHD, with any neurodivergent wiring that creates a gap between knowing and doing, this is not a luxury. It is a prosthetic for executive function.

---

## The Practice

The interface should meet you where you are, not where it wishes you were. Complexity should be available, never required. Error messages should help, not blame. The best tools disappear -- you think about the work, not the tool. Design for trembling hands and scattered thoughts, and steady hands will thank you too.

These are not theory. They are field notes from fifteen years of building software while managing a condition that regularly puts you on the user side of bad design. Every panic attack that made a complex API unusable, every depressive episode that reduced cognitive bandwidth to a narrow beam -- those experiences are the research. The libraries are the findings.

---

## Related

- [Designing for the Worst Day](/essays/2026-03-18-designing_for_the_worst_day) -- The original essay
- [For Humans](/knowledge/philosophy/for-humans) -- The broader design philosophy this principle serves
- requests -- HTTP for Humans, shaped by this principle
- Schizoaffective Disorder -- Where the principle was born
- Health -- The lived context
- [Programming as Spiritual Practice](/essays/2025-08-26-programming_as_spiritual_practice) -- Compassion compiled into interfaces
- Algorithm Eats -- The anti-pattern: designing for metrics, not humans
- Open Source -- Giving the tools away freely

---

*Design for the person having the worst day of their life. If it works for them, it works for everyone. That's the whole philosophy. Everything else is implementation.*

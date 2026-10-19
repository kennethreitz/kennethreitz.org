---
description: A server that crashes under load doesn't have a character flaw. It has
  insufficient resources for the demand.
source: obsidian-knowledge
---

# Burnout

> *"A server that crashes under load doesn't have a character flaw. It has insufficient resources for the demand."*

---

## Overview

**Burnout** is what happens when demand outruns capacity for long enough that depletion becomes the baseline. It rarely announces itself. It grinds, slowly, until "I'd rather do anything else than this" — about the work you love most — is just the new normal, and by then the hole is hard to climb out of. Kenneth has been writing about it for over a decade: naming the risk in 2013, reporting from mid-crisis in 2017, asking for help in public in 2018, and writing the post-mortem in 2026. The through-line of that arc is a single reframe. Burnout is an architectural failure, not a character flaw. The answer is scaling the infrastructure, not shaming the hardware.

## Identity as Vulnerability

The root cause, in Kenneth's accounting, was never workload alone. Open source gave him an identity when he had none — download counts as a scoreboard, every GitHub star a person saying *you matter*. When your sense of self is welded to a project's success, every issue is personal, every critique is existential, and every yes feels mandatory because no feels like closing the door that saved your life. There is no circuit breaker in that loop; that's the design flaw. And underneath it, undiagnosed Bipolar Disorder supplied the fuel: the Mania looked like productivity, and the culture celebrated exactly the intensity that was doing the damage. Nobody asks what the output costs the person producing it.

## How It Degrades

Burnout under load looks like any interface under load: it degrades before you notice. Response times lengthen. The thoughtful paragraph becomes a sentence, then a word — somewhere in the Requests issue tracker is a review that reads, in full, "No." Not cruelty; collapsed capacity. The worst case is the 410 GONE — deleting everything and walking away, which Kenneth considered and didn't do, because the projects were among the things he was proudest of. The 2018 Pipenv call for help is what the bottleneck looks like in real time: too many incoming issues for a small team, phrased as politely as exhaustion allows.

## In Practice

The remedies are structural too. Distribute the interface before you need to — co-maintainers as load balancers, given real authority rather than triage permissions. Learn to say no; the best pull requests remove lines of code. Go publish-only when the noise itself is the load. Keep hobbies that aren't code. Watch the metrics: if your average reply keeps getting shorter, that's the system reporting on capacity, and "I've been incredibly productive lately" is sometimes a symptom, not a success story. Above all, keep the identity separate: build the thing, release the thing, then go home and be a person who also built a thing — not a person who *is* the thing. And when you fail at all of this, repair beats consistency: come back the next day and write the more thoughtful response.

## Related

- [The Reality of Developer Burnout](/essays/2017-01-the_reality_of_developer_burnout) — the 2017 account, written mid-crisis
- [Open Source Gave Me Everything Until I Had Nothing Left to Give](/essays/2026-03-18-open_source_gave_me_everything_until_i_had_nothing_left_to_give) — the full accounting, a decade later
- [The Maintainer Is the Interface](/essays/2026-03-22-the_maintainer_is_the_interface) — burnout as an architectural problem
- [Growing Open Source Seeds](/essays/2013-01-growing_open_source_seeds) — the 2013 warning: BDFL projects and the risk they carry
- [Pipenv One Year Later & a Call for Help](/essays/2018-01-pipenv_one_year_later_amp_a_call_for_help) — the bottleneck, in real time
- [Be Cordial or Be on Your Way](/essays/2013-01-be_cordial_or_be_on_your_way) — the right instinct through the wrong architecture
- Open Source — the technology-side view of the same territory
- Mania — when the engine past the redline looks like productivity
- Bipolar Disorder — the undiagnosed fuel underneath the crashes
- Psychology — the wider field this belongs to

# Open Source Gave Me Everything Until I Had Nothing Left to Give
*March 2026*

I thought I was having a spiritual awakening. I was having a psychiatric emergency.

I was at a tech conference in Sweden when it started. I hadn't slept in days. I was one of the most prolific open source developers in the Python ecosystem, maintaining the most downloaded HTTP library on Earth, keynoting conferences across the world, and I was losing my mind in a hotel room six thousand miles from home.

Nobody around me knew. The mania looked like productivity. It always does.

This is the story I've been avoiding writing for a decade. Not the origin story of [Requests](/software/requests), the library I built that changed my life. I've told that one plenty of times. This is the story of what it cost.

## What Open Source Gave

Open source didn't just give me a career. It gave me an identity when I had none.

I was a college dropout who had been [working the front line at McDonald's](/essays/2026-03-06-the_coworking_space_saved_my_life) the year before. The education system had written me off. My GPA was 1.14. The standard paths to professional legitimacy were closed, and I had no plan for opening new ones. I was bidding on freelance jobs for pocket change and hoping something would happen.

Open source was the thing that happened.

When Requests took off, it wasn't just a popular library. It was proof that I existed, that I was capable, that the thing I could do had value in the world. The download counts were a scoreboard, and I was winning at the only game that had ever let me play. Every star on GitHub was a person saying: you matter, what you built matters, we see you.

For a kid who had never been seen by any system that was supposed to see him, that was everything. I don't use the word lightly. It was everything.<label for="sn-identity-formation" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-identity-formation" class="margin-toggle"/><span class="sidenote">Identity formation through open source contribution is more common than people realize. For those of us who didn't fit the credentialed paths, community recognition became the primary mirror in which we learned to see ourselves as capable. This is a gift. It becomes a trap only when the mirror is the only one you have.</span>

Open source gave me Heroku. Heroku gave me a salary, health insurance, colleagues who took me seriously, and a front-row seat to the infrastructure of the internet. It gave me a platform to advocate for the ["for humans" philosophy](/essays/2025-08-27-from_http_to_consciousness) that I still believe is one of the most important ideas in software design.

It gave me a life. A real one, built from nothing, through craft and generosity and a community that rewarded good work regardless of where you went to school.

What follows is not ingratitude. It's accounting.

## The Escalation

Here's how it worked, practically. You build something good. People use it. People depend on it. People file issues, request features, report bugs. The community grows. The responsibility grows. The expectations grow. And because the thing that gave you your identity is the thing people are depending on, you can't separate "maintaining the project" from "maintaining yourself."

I didn't have boundaries around this because I didn't know I needed them. The kid who had been invisible was now visible, and visibility felt like oxygen. More users meant more validation. More conferences meant more proof that I mattered. More projects meant more surface area for the world to see me. I said yes to everything because saying no felt like closing the door that had saved my life.

```python
from dataclasses import dataclass


@dataclass
class MaintainerLoop:
    """The cycle that builds careers and breaks people."""

    identity: str
    project_success: float = 0.0
    community_expectations: float = 0.0
    self_worth: float = 0.0

    def cycle(self):
        # Success raises expectations.
        self.community_expectations = self.project_success * 1.5

        # Self-worth tracks community response.
        self.self_worth = self.project_success

        # When identity IS the project,
        # every expectation becomes personal.
        # Every criticism lands on the self,
        # not just the code.

        # There's no circuit breaker here.
        # That's the design flaw.
        pass
```

The pressure was largely self-directed. I want to be honest about that. Nobody at Heroku was cracking a whip over my open source work. The community wasn't threatening me. The pressure came from the fact that I had welded my sense of self to the project's success, and anything that threatened the project threatened me. A rude issue comment wasn't just feedback about code. It was someone questioning whether I deserved to exist in the space I'd carved out.

And underneath all of this, undiagnosed, was bipolar disorder.

## The Crises

I need to talk about this directly, because the connection between open source and my mental health crises is the thing I've been avoiding writing about for a decade.

I've [written about the clinical details](/essays/2016-01-mentalhealtherror_an_exception_occurred) elsewhere. What I haven't written about is the fuel. The manic episodes didn't come from nowhere. They came from a young person with an undiagnosed mood disorder who was running at maximum intensity, sleeping four hours a night, crossing time zones every other week, saying yes to every opportunity, and performing the role of "prolific open source developer" at a pace that would have been unsustainable for anyone and was genuinely dangerous for someone with my brain chemistry.<label for="sn-manic-pressure" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-manic-pressure" class="margin-toggle"/><span class="sidenote">The relationship between external stressors and manic episodes is well-documented in bipolar disorder research. Stress doesn't cause bipolar disorder, but it can trigger episodes in people who have it. Sleep disruption is particularly dangerous, and the open source maintainer lifestyle (conferences across time zones, late-night coding sessions, the always-on expectation of community engagement) is essentially a sleep disruption machine.</span>

I wasn't suicidal. But manic episodes are dangerous in ways people don't talk about enough. You don't sleep for days. Your judgment dissolves. You make decisions that a stable mind would never make. You burn relationships, burn money, burn credibility. You believe things about yourself and the world that aren't true, and you act on those beliefs with absolute conviction. And each episode was worse than the last, escalating in lockstep with the pressure I was putting on myself.

I had my first serious manic break at that conference in Sweden. I stayed awake for a week. I thought I was enlightened. I was psychotic.

The second one put me in a hospital for twelve days. I believed I was God. Then Lucifer. Then Jesus. Then a transterrestrial being from the star system Sirius. The psychosis was total. When I came back to reality, I didn't recognize myself or the wreckage around me.

The same intensity that produced Requests produced the conditions for the worst experiences of my life. The engine was the same. It just had two outputs: beautiful software and shattered minds. Nobody in the open source community talks about this because the survivors go quiet and the ones who don't survive aren't around to write essays.

I am tired of the silence around this. Open source culture celebrates intensity. It celebrates the all-night hack session, the prolific contributor, the person who maintains fifty projects and keynotes ten conferences a year. What it doesn't celebrate, what it actively looks away from, is what that intensity does to people who are wired differently. And a lot of us are wired differently. That's why we're here in the first place.

---

## The Cost

**I sold my twenties to a corporation.** Heroku was a good employer, and I'm grateful for the years I spent there. But the honest truth is that I was there because of open source, maintained open source while I was there, and the two became so entangled that I couldn't tell where the job ended and the volunteer work began. My most productive years as a human being, the years when I had the most energy and the fewest obligations, were spent in service of a project ecosystem that I maintained for free and a company that benefited from my maintaining it for free. That's not a complaint. It's a description of a deal I made without fully understanding the terms.

**I traveled too much.** Conference culture in the 2010s was relentless, and I was in the thick of it. I keynoted, I spoke, I attended, I networked. I saw the inside of more hotel rooms and airport lounges than I can count. At the time it felt like success. In retrospect it was a young person with a mood disorder and no boundaries being fed a steady diet of stimulation and validation that made his condition worse. Every timezone change was a sleep disruption. Every conference was a performance. Every after-party was an opportunity to not rest.

**I gave too much of myself away.** Not just code. Myself. My time, my energy, my emotional bandwidth, my identity. I made myself a public resource and then was surprised when the public felt entitled to my resources. This is the deal that open source offers, and it's not a bad deal for everyone, but it was a bad deal for me specifically, given my specific mental health profile and my specific tendency to derive self-worth from external validation.

**I almost lost my mind.** Literally. Multiple times. And the culture I was embedded in rewarded the exact behaviors that made the losing more likely. The hypomanic productivity wasn't a warning sign to anyone around me. It was a feature. "Kenneth ships so much code." Yeah. There's a reason for that, and it's not discipline.

The part that's hardest to write: I don't know who I would have been without open source. That cuts both ways. I might have been nobody. I might have been happier. I might have found my way to a stable career through some other door that didn't require me to make my inner life a public performance. There's no control group for a life. You just live the one you get and try to learn from it.

## What I'd Do Differently

I would have kept my identity separate from my projects. Requests is a library. I am a person. The conflation of the two was the root cause of most of the damage. When the project is you, every issue is personal, every critique is existential, and every success is addictive in exactly the wrong way. I'd build the thing, release the thing, and then go home and be a person who also built a thing. Not a person who IS the thing.

I wish I'd had the diagnosis earlier. Not because diagnosis is a magic wand that heals things. It's just information, information I didn't have until there was a crash. But knowing the shape of the thing you're dealing with changes how you move through the world, and I was moving through the world blind.

I would have said no more. To conferences, to new projects, to the steady expansion of my surface area in the community. Not because those things were bad, but because each yes was another commitment that increased the pressure on a system that was already under more load than it could handle.

I would not have tied my financial security to the goodwill of a community. That's a fragile foundation for a life, especially when you have a condition that can erode goodwill quickly during an episode.

These aren't recriminations. They're engineering notes from a post-mortem, written a decade after the incident.

## If You're a Maintainer and You're Wired Like Me

I want to say something directly to the person reading this who recognizes themselves in it.

If you're maintaining open source projects and you notice that your productivity comes in surges, that you don't sleep much during the good periods, that your best work happens in states that feel elevated and electric, please pay attention to that. It might just be flow. It might be something else. I didn't know the difference, and by the time I learned, the crash had already happened.

The things that make you a great open source contributor (hyperfocus, intensity, pattern recognition, the ability to hold entire systems in your head) overlap significantly with the things that make certain psychiatric conditions both more likely and harder to detect. The community will celebrate your output without ever asking what it costs you to produce it. That's not malice. It's just a system that optimizes for code, not for the person writing it.

Separate your identity from your projects. Find people who see you when you're not shipping. Get a doctor who understands that "I've been incredibly productive lately" is sometimes a symptom, not a success story. Build a life that doesn't depend on the community's approval to feel real.

I wish someone had told me this when I was twenty-three and staying up for three days straight because the code was flowing so beautifully. The code was beautiful. I was in trouble.

## Where It Lands

Time heals things. That's a cliche because it's true.

All things in tech are seasonal. The fame I experienced in 2013 is a different climate than the quiet I experience in 2026. Both are weather. Neither is permanent. The mistake I made was treating the fame season as though it defined the entire climate of my life, and then being unprepared when the season changed.

I wrote earlier about [the values I outgrew and the ones that stayed](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed). That essay is the companion piece to this one. That essay is about where I've landed. This one is about what the landing cost.

Tech became craft instead of lifestyle. I still write code. I still think about the [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) between code and consciousness. I still believe that programmers have a responsibility to think about what kind of minds they're shaping when they ship software. But the center of gravity moved. The code serves the life now, not the other way around.

I have a son. I have a wife who [sees things before I do](/essays/2026-03-06-sarah_knows_first). I have a faith practice that grounds me in something that doesn't depend on download counts or community approval. I have a diagnosis and a treatment plan and enough self-knowledge to recognize when the engine is running too hot.

I don't know if I'd do it again. That's the truest thing I can say. The kid in the coworking space didn't have better options, and the path that opened was extraordinary. But knowing what it cost, the mental health crises, the community fracture, the years sold to intensity, the identity built on something that could be taken away by one person's blog post. I don't know. I genuinely don't know.

What I know is that it happened. It gave me everything and it almost broke me and now it's a part of my history instead of the center of my present. I'm grateful for what it gave. I'm honest about what it took. And I'm done performing either gratitude or grievance about it.

The house I live in matters more than the code I ship. That's not something I would have written ten years ago. It's the truest thing I can write now.

# The Coworking Space Saved My Life

*March 2026*

I was nineteen years old, smelling like french fry grease, and I had just quit McDonald's without notice.

That sentence contains more information than it seems to. It contains a college dropout who had been told his entire life that grades were the most important thing in the world. It contains $10,000 in student debt and a 1.14 GPA. It contains a kid who had moved back to Winchester, Virginia, defeated, working sixty-five-hour weeks at a fast food restaurant because he didn't have anything better to do. It contains the particular despair of knowing you're capable of more but having no evidence to prove it to anyone, including yourself.

I've [written about this before](/essays/2009-01-your_degree_is_worthless_collaborate), briefly and matter-of-factly, the way you describe something when you're still too close to it to understand what actually happened. In that 2009 essay, I laid out the facts: dropped out of college, worked at McDonald's, found a coworking space, everything changed. Clean narrative. Neat arc. But the real story is messier, and sixteen years later, I think I finally understand what that room actually was and what we've lost by letting spaces like it disappear.

## The Room

Here's what I wrote in 2009:

> In this little building off the historic old-town walking mall was a room. Inside: the COO of a major internet company, tech consultants, graphic designers, writers, author, bloggers, freelancers, and so much more. I met everyone in and around town. I sat in on think tank lunches. People cared about what I had to say. We collaborated.

I want to sit with that paragraph for a moment, because it understates something enormous. I was a teenager with no degree, no credentials, no professional network, and no particular reason for anyone to take me seriously. I had been bidding on freelance jobs for pocket change, the kind of gig economy hustle that existed before we had a word for it. I found a guy on Twitter from my hometown who was into technology, which was rare enough in Winchester that it felt like discovering another species. He led me to a coworking space I didn't know existed.

And in that room, something happened that the education system had failed to produce in twelve years of public school and a year of college: I became engaged.<label for="sn-engagement" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-engagement" class="margin-toggle"/><span class="sidenote">There's a bitter irony in using the word "engagement" here, given how much of my later work has been about critiquing [algorithmic engagement optimization](/essays/2025-08-26-the_algorithm_eats_virtue). The engagement I experienced in that coworking space was the real thing -- mutual curiosity, shared purpose, human presence. The algorithmic version is its hollow simulation.</span>

Not engaged in the way platforms mean when they track your screen time. Engaged the way a mind becomes engaged when it encounters other minds that take it seriously. The COO of an internet company asked me what I thought about web standards. Tech consultants wanted to hear my approach to a problem. Writers shared their work and wanted feedback. Nobody asked to see my transcript. Nobody cared that I'd been making Big Macs the week before. They cared about what I could think and what I could build.

I was finally engaged. *Fully* engaged.

## The Third Space

Sociologists have a name for this: the third space. Not home, not work, but somewhere else entirely. Ray Oldenburg wrote about this in *The Great Good Place* back in 1989, arguing that democracies need informal public gathering places where people encounter others outside their usual social circles. The coffee house. The barbershop. The pub. The town square. Places where serendipity happens.

The coworking space in Winchester was my third space. It functioned as a university without tuition, a professional network without gatekeepers, a mentorship program without applications. It worked because of two properties that are surprisingly rare and getting rarer: physical proximity and generous strangers.<label for="sn-proximity" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-proximity" class="margin-toggle"/><span class="sidenote">Physical proximity matters more than we think. Video calls transmit information but not presence. There is something about being in a room with someone -- hearing them think out loud, catching the edge of a conversation not meant for you, sharing the ambient energy of focused work -- that no digital substitute has managed to replicate.</span>

Physical proximity meant I could overhear a conversation about server architecture and ask a question. It meant someone could see me struggling with a CSS layout and lean over to help. It meant lunch happened together, and lunch is where the real conversations happen. Think tank lunches, I called them. The kind of unstructured time where a graphic designer and a tech consultant and a college dropout accidentally solve each other's problems because they're all in the same room eating the same sandwiches.

Generous strangers meant people who shared knowledge without expecting anything in return. Not because they were saints, but because that's what happens when you put skilled people in a room together with low stakes and good faith. Knowledge flows. Experience diffuses. A nineteen-year-old who can't afford college gets an education that would have cost $150,000 and four years, delivered in real time by people who were actually doing the work.

## The Lineage

I need to be precise about something: my entire career traces back to that room.

Not metaphorically. Literally. The connections I made at that coworking space led to my first real development job. That job gave me the professional context to start building open source tools. Those tools led to Requests, the Python HTTP library that would eventually be downloaded billions of times. Requests led to Heroku. Heroku led to everything else.

The [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) I've written about, where code shapes minds and programmers shape code and therefore programmers shape collective consciousness, that loop has an origin point for me. It starts in a small building off the historic old-town walking mall in Winchester, Virginia, with a handful of people who had no obligation to help a McDonald's dropout but did anyway.

When I designed Requests to be "for humans," that philosophy didn't come from a textbook. It came from experiencing what it feels like when a system is designed for you versus when it isn't. The education system wasn't designed for how I learn. McDonald's wasn't designed for human flourishing. But that coworking space, without trying to be anything in particular, was designed at a human scale for human interaction. The [philosophy I'd later articulate](/essays/2025-08-27-from_http_to_consciousness) about technology serving human mental models rather than forcing adaptation to machine logic, I learned it first in a room full of generous strangers before I had the vocabulary to describe it.

## What a Third Space Actually Does

I've been thinking about why that room worked so well, and I think it comes down to something that's hard to engineer: it created the conditions for serendipitous connection between people at different stages of expertise and different walks of life.

This is different from networking, which is transactional. It's different from mentorship, which is hierarchical. It's different from school, which is credentialed. A good third space has a few specific properties:

- **Low barriers to entry.** I walked in with a laptop and curiosity. That was enough.
- **Mixed expertise levels.** The COO and the dropout were in the same room. This matters more than anything else.
- **Unstructured time.** No agenda. No curriculum. No deliverables. Just people doing their work in proximity to each other.
- **Repeated contact.** You show up again and again. Relationships develop slowly, through accumulated presence, not through scheduled one-on-ones.
- **Physical co-location.** You can't replicate serendipity on Zoom. You can schedule meetings, but you can't schedule the overheard conversation that changes your trajectory.

These properties create what I'd call, borrowing from programming, a fertile runtime environment. You put people in the right conditions and useful things emerge that nobody planned. Not every time. Not predictably. But reliably enough that it matters enormously for the people it touches.

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ThirdSpace:
    """A place where serendipity becomes reliable."""

    barriers_to_entry: float = 0.0  # should be near zero
    expertise_diversity: float = 1.0  # maximum variance
    agenda: Optional[str] = None  # deliberately unstructured
    proximity: str = "physical"  # no substitute exists yet

    def daily_interaction(self, visitors: list) -> list:
        connections = []

        for person_a in visitors:
            for person_b in visitors:
                if person_a == person_b:
                    continue

                # The magic: unplanned relevance
                if self.serendipity_check(person_a, person_b):
                    connections.append(
                        Connection(person_a, person_b, planned=False)
                    )

        # TODO: figure out why this works so much
        # better than any designed system
        return connections
```

The code is playful, but the insight is serious. We keep trying to engineer these connections through apps, platforms, networking events, and LinkedIn. None of them work as well as a room.<label for="sn-engineering-serendipity" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-engineering-serendipity" class="margin-toggle"/><span class="sidenote">This might be because serendipity requires the absence of optimization. The moment you design for a specific outcome, you kill the conditions that produce unexpected ones. Third spaces work because nobody is trying to make them work in any particular way.</span>

## The Death of Third Spaces

Here's where this gets heavy.

America has been systematically losing its third spaces for decades, and the pace has accelerated dramatically. Malls are closing. Independent coffee shops are being replaced by chains that discourage lingering. Public libraries are underfunded. Community centers are shuttered. The places where strangers used to encounter each other, the places where a nineteen-year-old dropout could accidentally meet the people who would change his life, are disappearing.

The coworking space movement was supposed to help. And for a while it did. Small, locally-owned coworking spaces created exactly the kind of fertile environments I'm describing. But then WeWork happened, and the entire concept got financialized and corporatized. A WeWork flex desk is not a third space. It's a product. It has a value proposition and a target market and a per-square-foot revenue model. The serendipity got optimized out in favor of amenities and Instagram-worthy common areas that nobody actually uses for conversation.

Then the pandemic happened, and even the corporate coworking spaces emptied out. Remote work became the default for knowledge workers. And while remote work has genuine benefits, the celebration of it in the tech industry tends to ignore a critical loss: the kid who needs a room to walk into. The dropout who needs to overhear a conversation. The person whose next life chapter starts with a chance encounter they couldn't have planned.

You can't stumble into a Zoom call. You can't overhear a conversation on Slack. The digital tools that replaced physical third spaces are optimized for intentional connection, for people who already know what they're looking for and who they want to talk to. They do nothing for the people who don't know yet.

## The Irony

And here's the part that keeps me up at night: the tech industry I joined, the one that gave me a career because a coworking space gave me a chance, has been one of the primary forces destroying the kind of spaces that created me.

Remote work culture, which tech companies pioneered and celebrated, reduced the need for physical gathering spaces. Platform economies hollowed out local businesses that served as informal community hubs. Algorithmic social media replaced the town square with infinite scroll, trading depth for scale, trading presence for engagement metrics. The attention economy, which I've written about [extensively](/essays/2025-08-26-the_algorithm_eats_virtue), consumes precisely the kind of open-ended, unoptimized time that third spaces require.

You can't have serendipitous conversations if everyone's attention is captured by their phones. You can't build slow relationships through repeated contact if nobody goes to the same physical place anymore. You can't maintain the delicate social ecology of a third space when every interaction is mediated by platforms designed to maximize engagement rather than depth.

The [algorithm eats time](/essays/2025-09-01-the_algorithm_eats_time). And third spaces run on time. Unstructured, unoptimized, unmonetized time. The kind of time that looks like waste from the outside but is actually the raw material of human connection.

I recognize the recursive irony here. I am someone who benefited from physical community and then spent his career building digital tools. I designed Requests to make HTTP accessible, and HTTP is part of the infrastructure that enables the platforms that replaced the physical spaces that saved me. I'm not claiming innocence in this. The [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) cuts both ways.

## The Next Kid at McDonald's

This is not nostalgia. I'm not romanticizing the past or arguing that we need to go back to some golden age of community centers and town squares. I'm raising a specific, practical concern: there is a kid right now, working a dead-end job, who is capable of extraordinary things but has no way to discover that because the spaces where that discovery used to happen no longer exist.

When I was nineteen and working at McDonald's, the coworking space was right there. I found it through Twitter, back when Twitter was a place where local communities could actually form. I walked in with nothing but a laptop and found people who took me seriously. The barriers were low, the people were generous, and the physical space existed.

What does that kid do today? The local coworking space has been replaced by a WeWork that costs $400 a month. Twitter is an algorithmic hellscape optimized for outrage. The coffee shop has a two-hour laptop limit. The library closes at five. The community college is online now, which sounds accessible until you realize that accessibility without community is just content delivery.<label for="sn-content-delivery" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-content-delivery" class="margin-toggle"/><span class="sidenote">This is the fundamental misunderstanding of online education. The value of a learning environment is not primarily the information transmitted -- that's been freely available since the early internet. The value is the community formed around learning, the relationships that emerge from shared struggle, the serendipitous encounters that redirect careers. You can put lectures online. You cannot put a room online.</span>

I think about this a lot. I think about all the potential Requests that don't get built because the person who would have built them never stumbled into the right room. I think about the careers that don't happen, the open source projects that don't exist, the contributions to collective human capability that simply vanish because we eliminated the conditions under which they emerge.

This is a problem I was [probably ahead of my time](/essays/2025-08-26-ahead_of_my_time_i_think) in recognizing, which is cold comfort.

## What We Need to Build

I don't have a clean solution. This is one of those problems where the impulse to solve it with technology is part of what caused it. But I have some thoughts about what would help, drawn from what actually worked for me:

**Fund local, independent coworking spaces.** Not WeWork clones. Small rooms with low barriers to entry and no venture capital breathing down anyone's neck. Subsidize them the way we subsidize libraries, because they serve the same democratic function: giving people access to the community resources they need to develop their capabilities.

**Design for mixed expertise.** The most valuable thing about my coworking space was that the COO and the dropout were in the same room. Most modern coworking spaces stratify by industry, price point, and status. This is exactly backward. The value comes from the mix.

**Protect unstructured time.** Stop filling every gathering with agendas, speakers, and networking activities. The best conversations happen in the gaps. Design spaces that have gaps.

**Resist the urge to digitize everything.** Some things need to happen in physical space. The serendipitous encounter, the overheard conversation, the slow accumulation of trust through repeated presence. These are not features you can add to an app.

**Recognize this as infrastructure.** Third spaces are social infrastructure, as essential as roads and water systems. When they disappear, communities don't just lose convenience. They lose the capacity to develop their own members, to surface hidden talent, to create the unexpected connections that drive innovation and human flourishing.

As someone who has spent years thinking about [programming as a spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice), I've come to believe that the most important thing a programmer can build might not be software at all. It might be the conditions under which other people discover what they're capable of. The room matters more than the code.

## The Room Matters

I keep coming back to that building off the walking mall. A room. Some people. No agenda. Low barriers. Generous strangers.

It's almost embarrassingly simple. That's what makes it so hard to replicate and so easy to destroy. It doesn't scale. It can't be monetized. It doesn't have metrics. You can't raise a Series A on it. There is no engagement dashboard for "a nineteen-year-old walked in and his entire life changed."

But that's what happened. And I know it happened to other people in other rooms in other towns, because I've met them. Every industry has these stories: someone who walked into a space they didn't belong in, met people who had no reason to help them, and had their trajectory permanently altered.

The question is whether we're going to keep allowing those spaces to disappear, or whether we're going to recognize them as the essential infrastructure they are and fight to preserve and create them.

I was saved by a room full of generous strangers. The least I can do is argue that the next kid deserves the same chance.<label for="sn-recursive-responsibility" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-recursive-responsibility" class="margin-toggle"/><span class="sidenote">This is the recursive responsibility in its most concrete form. The room shaped me. I shaped code. The code shaped how millions of people interact with the internet. If that room hadn't existed, none of it happens. What rooms are we failing to create right now?</span>

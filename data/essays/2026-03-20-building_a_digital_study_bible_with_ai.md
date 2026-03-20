# Building a Digital Study Bible with AI: Weeks, Not Years
*March 2026*

In [The Lego Bricks Era](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed), I wrote that if I opened a blank file and wrote my values from scratch, the first two lines would be: *Drink more water. Pray continuously.*

That essay was about identity shifting. Tech becoming craft instead of lifestyle. Faith becoming the center of gravity that everything else orbits. But a value that just lives on a page is a value that hasn't been tested. "Pray continuously" is a nice thing to say. Building something that helps other people engage with Scripture is what it looks like when you actually mean it.

So I built [kjvstudy.org](https://kjvstudy.org).

## What It Is

KJV Study is a comprehensive, free, open Bible study web application built on the King James Version, specifically the 1769 Cambridge Edition. It's what you'd get if you took a study Bible, a concordance, an interlinear Bible, a cross-reference system, and a topical index, merged them into one thing, and put it on the internet for anyone to use without paying or creating an account.

Here's what's in it:

- **31,102 verses** of the complete KJV text.
- **12,321 verses** with detailed verse-by-verse theological commentary including Hebrew and Greek word analysis.
- **31,031 verses** of Hebrew/Greek interlinear data with word-by-word breakdowns.
- **Strong's Concordance**: 8,674 Hebrew entries and 5,624 Greek entries, fully searchable.
- **120,858 cross-references** linking Scripture to Scripture.
- **39 resource categories**: apostles, prophets, parables, covenants, names of God, armor of God, I AM statements, fruits of the Spirit, and dozens more.
- **25+ study guides**, **12+ reading plans** with progress tracking, a biblical timeline, and a family tree explorer.
- **2,007 verses** of Christ's words marked in red (Red Letter edition).
- Full-text search. Bookmarks. PDF export. Dark mode. Keyboard navigation.<label for="sn-data-scale" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-data-scale" class="margin-toggle"/><span class="sidenote">The raw data behind the application is roughly 58 MB of structured JSON spread across 359+ files. That's 66 commentary files (one per book of the Bible), cross-reference datasets, interlinear data, Strong's entries, reading plans, study guides, topical indexes, and resource collections. It's the kind of dataset that would take a team of seminary-trained scholars years to compile manually.</span>

The numbers are worth sitting with. This is not a weekend project. This is a digital library.

## Why This Combination Matters

If you've spent any time in the world of Bible study tools, you know that the landscape is fragmented in a very specific way. Most study Bibles fall into one of two camps.

Camp one: modern translations with Reformed theological notes. The ESV Study Bible is the gold standard here. Excellent scholarship, Calvinist perspective, but the translation is modern English. If you're someone who reads and studies the King James Version, whether for liturgical reasons, literary preference, or denominational tradition, the ESV Study Bible isn't your tool.

Camp two: KJV text with dispensationalist notes. The Scofield Reference Bible. The Dake Annotated Reference Bible. These pair the KJV with a theological framework that emphasizes distinct dispensations, a particular approach to prophecy and end times, and a hermeneutic that many Reformed readers find deeply problematic. If you're Reformed and you want to study the KJV, Scofield isn't your tool either.

What doesn't exist, or didn't exist, is a free digital resource that pairs the King James Version with Reformed, grammatical-historical commentary. The kind of commentary that takes the text seriously as literature and as Scripture simultaneously. That examines the original Hebrew and Greek without requiring you to have seminary training to follow along. That connects Old Testament passages to their New Testament fulfillment. That emphasizes God's sovereignty, grace, and the authority of Scripture in the Reformed tradition.

That's what kjvstudy.org is. And the reason it didn't exist before is that building it would have required resources that no individual person could reasonably assemble.<label for="sn-reformed-kjv" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-reformed-kjv" class="margin-toggle"/><span class="sidenote">There's an interesting historical gap here. The KJV was the Bible of the English Reformation. Calvin's theological descendants read it for centuries. But the major KJV study Bible tradition in America became dominated by dispensationalist theology through Scofield's enormous influence in the early 20th century. A Reformed KJV study Bible is, in some sense, a return to the original pairing.</span>

## No Accounts. No Login. Your Data Stays on Your Device.

There's no account system. No login. No email collection. No analytics tracking your reading habits. When you bookmark a verse, that bookmark lives in your browser's localStorage. When you track progress through a reading plan, that progress lives on your device. When you set dark mode or adjust your preferences, those preferences never leave your machine.

This is intentional and it's theological.

I wrote in [Designing for the Worst Day](/essays/2026-03-18-designing_for_the_worst_day) that tools should meet you where you are, not where they wish you were. The person I'm designing for is someone who is struggling. Maybe they just got a terrible diagnosis. Maybe they're sitting in a hospital waiting room at 2 AM. Maybe they're in the middle of a grief so heavy that forming a complete sentence feels impossible. That person should be able to open their phone, search "hope," and find Scripture with real theological context immediately. Not after creating an account. Not after choosing a subscription tier. Not after dismissing a modal asking for their email.

```python
# What most Bible apps require:
def access_scripture(user):
    if not user.has_account:
        return redirect("/signup")
    if not user.has_verified_email:
        return redirect("/verify")
    if user.is_on_free_tier:
        return show_with_ads_and_limited_features()
    return scripture_with_commentary()


# What kjvstudy.org requires:
def access_scripture():
    return scripture_with_commentary()

# That's the whole function.
# No user object. No tier check. No gates.
# The interface meets you where you are.
```

**The tool serves you. You don't serve the tool.**

This connects directly to the [for humans philosophy](/essays/2025-08-27-from_http_to_consciousness) that has shaped everything I've built since Requests. Technology should adapt to human needs, not force humans to adapt to technology's business model. When someone is searching for "Bible verses about suffering" at 3 AM, the last thing they need is a paywall between them and the Psalms.<label for="sn-localstorage" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-localstorage" class="margin-toggle"/><span class="sidenote">localStorage is a browser API that stores data locally on your device. It's the simplest possible persistence layer: key-value pairs that never leave your machine. No server, no database, no privacy policy needed. Your bookmarks, your reading progress, your preferences. All yours. This is a deliberate architectural choice that embeds a value (your data is yours) into the technical substrate of the application.</span>

## How AI Made This Possible

Let me be direct about the scope. kjvstudy.org has:

- 17 route modules handling everything from verse display to interlinear analysis to PDF generation.
- 75 Jinja2 templates.
- 941 tests.
- 359+ JSON data files totaling roughly 58 MB of structured theological content.
- A complete interlinear Bible with word-by-word Hebrew and Greek analysis.
- Verse-by-verse commentary covering 12,321 verses with specific theological analysis, original language word studies, historical context, and reflection questions.

A project of this scope would traditionally require a full team. You'd need developers, theologians with original language training, content writers, designers, and someone to organize and quality-check the data. You'd need significant funding. You'd need years.

I built it with Claude. The git history tells the story: 1,491 commits, 1,305 of which landed in November and December 2025. Two months. The bulk of a production application, deployed on Fly.io with 941 tests passing, static site generation, a Tauri desktop app variant, and 58 MB of structured theological content. Two months, one person, one AI.

I want to be precise about what that means, because "I built it with AI" can mean anything from "AI autocompleted some variable names" to "AI did all the work while I watched." Neither of those is what happened.

Here's what I did. I directed the theological vision. I defined the Reformed perspective. I specified what kind of commentary I wanted: Christ-centered, emphasizing God's sovereignty and grace, grounded in grammatical-historical hermeneutics, with specific Hebrew and Greek word analysis for every verse. I set the quality bar. I reviewed the output. I made architectural decisions about how the application should work, how data should be structured, what the user experience should feel like.

Here's what AI did. It generated the verse-by-verse commentary, 12,321 verses worth of theological analysis that includes specific Hebrew and Greek words with transliterations, direct engagement with the verse text, historical context, and reflection questions. It helped architect the application across those 17 route modules and 75 templates. It generated and organized the structured data files. It wrote and maintained the test suite.

The commentary generation is worth examining closely. I built a structured agent specifically for this task:

```markdown
# From .claude/agents/commentary-generator.md

## CRITICAL: Avoid Generic Filler Text

**DO NOT** generate commentary with these useless patterns:
- "This profound verse reveals crucial theological truth..."
- "The Hebrew text contains nuances..."
- Starting every verse with the same phrase

**EVERY verse must have:**
- Specific Hebrew/Greek words FROM THAT VERSE with transliterations
- Direct quotes from the verse being analyzed
- Verse-specific content, not generic theology
```

This is the kind of quality control that makes AI-generated content actually useful rather than a wall of eloquent nothing. The agent instructions are prescriptive about what bad commentary looks like and what good commentary requires. Here's the difference in practice:

```json
// BAD: Generic filler that could describe any verse
{
  "analysis": "This profound verse reveals crucial
    theological truth about God's priorities. The
    Hebrew text contains important nuances."
}

// GOOD: Specific engagement with Hosea 6:6
{
  "analysis": "I desired mercy, and not sacrifice
    (חֶסֶד חָפַצְתִּי וְלֹא־זָבַח) — God's priority
    is hesed (covenant loyalty, steadfast love) over
    ritual performance. Jesus quoted this verse twice
    (Matthew 9:13, 12:7) to condemn Pharisaic
    externalism."
}
```

The difference is specificity. The good commentary names the Hebrew words, transliterates them, defines them, and connects them to their New Testament usage. A human theologian would do the same thing. The AI does it at scale, across thousands of verses, with consistent quality, because the instructions are precise enough to prevent the default drift toward generic platitudes.

There's a page on the site called [A Note from Claude](https://kjvstudy.org/about/claude) where the AI speaks directly about its role in the project. It states plainly: "I do not experience faith, worship, or the indwelling of the Holy Spirit. I process language and generate text." It describes its limitations, the ethics of the work, and what it observed in processing all 31,102 verses. Full transparency. You know exactly what built this and what didn't.<label for="sn-ai-theology" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-ai-theology" class="margin-toggle"/><span class="sidenote">There's a legitimate question about whether AI-generated theological commentary can be trustworthy. My answer: it depends entirely on the constraints you give it. Unconstrained AI commentary would be a theological disaster, confidently mixing traditions and inventing connections. But constrained to a specific perspective (Reformed), a specific hermeneutic (grammatical-historical), and specific quality requirements (name the Hebrew, quote the verse, connect to the canon), the output is remarkably consistent with the scholarly tradition it's drawing from. The constraints are where the human theological judgment lives.</span>

## The Topical Index and Finding What You Need

One of the features I'm most proud of is also one of the simplest: the topical verse index.

If you search Google for "Bible verses about hope," you'll find SEO-optimized listicles. Ten verses stripped of context, surrounded by ads, designed to capture traffic rather than serve the reader. The verses are correct. The experience is hollow.

On kjvstudy.org, searching for hope gives you verses with full theological commentary. You get the Hebrew or Greek word for hope in that specific passage. You get the historical context of who wrote it and why. You get reflection questions that push you toward actual engagement with the text rather than passive consumption.

This matters because people searching for "Bible verses about suffering" or "Bible verses about anxiety" at 3 AM are not looking for SEO content. They're looking for help. And the difference between a decontextualized list and a verse with real commentary is the difference between handing someone a map and handing them a compass. The map tells them where things are. The compass helps them find their own way.<label for="sn-seo-vs-service" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-seo-vs-service" class="margin-toggle"/><span class="sidenote">This connects to the [algorithm eats virtue](/essays/2025-08-26-the_algorithm_eats_virtue) thesis. The SEO-optimized Bible verse listicle is engagement optimization applied to Scripture. It extracts attention from people in genuine need and converts it into ad revenue. kjvstudy.org has no ads, no revenue model, no engagement metrics. The absence of a business model is itself a theological statement about what Scripture is for.</span>

## The Recursive Loop, Applied to Faith

I've written extensively about the [recursive loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds): code shapes minds, programmers shape code, therefore programmers shape collective consciousness. kjvstudy.org is the most direct application of that principle I've ever built.

The tool shapes how people engage with Scripture. I shaped the tool. Therefore I'm shaping, in some small way, how people encounter the Bible. That responsibility is not abstract to me. It's the reason the commentary follows a specific theological tradition rather than trying to be everything to everyone. It's the reason the original languages are included: not to show off, but because understanding that the word translated "love" in 1 Corinthians 13 is *agape* (ἀγάπη), not *phileo* or *eros*, changes what the passage means. It's the reason there are reflection questions, not just information. The tool doesn't just deliver content. It shapes the encounter.

```python
from dataclasses import dataclass


@dataclass
class RecursiveLoop:
    """The responsibility that awareness brings."""

    programmer_values: list[str]
    tool_design: dict
    user_experience: str

    def trace_influence(self):
        # What I value shapes what I build.
        values = self.programmer_values
        # ["Reformed theology", "accessibility",
        #  "no monetization", "original languages"]

        # What I build shapes how people engage.
        design = self.tool_design
        # {"commentary": "Reformed, specific, grounded",
        #  "access": "no accounts, no gates",
        #  "languages": "Hebrew and Greek for everyone"}

        # How people engage shapes their understanding.
        experience = self.user_experience
        # "Someone searching 'hope' at 3 AM finds
        #  real scholarship, not SEO content."

        # The loop completes:
        # Their understanding shapes what they value.
        # What they value shapes what they build.
        # What they build shapes the next person.
        return "consciousness shaped, one verse at a time"
```

This is what it looks like when [programming as spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice) stops being a metaphor. I'm not comparing coding to meditation. I'm saying that building a tool to help people study Scripture is itself an act of faith. The craft serves the life. The code serves the prayer.

## What This Means for Technology and Human Flourishing

I've spent over a decade building tools that follow the "for humans" philosophy. Requests made HTTP accessible. Tablib made data format conversion disappear. Records let you just write the query. Maya let you speak like a human about time.

kjvstudy.org is the same philosophy applied to the most important text I know. Make the scholarly resources accessible. Remove the gates. Meet people where they are, not where you wish they were. If it works for the person searching "Bible verses about grief" at 2 AM with trembling hands, it works for everyone.

The thing that AI made possible here is not cleverness. It's scale. One person cannot write commentary for 12,321 verses. One person cannot build an interlinear Bible. One person cannot compile 120,858 cross-references. But one person with clear theological vision, precise quality requirements, and AI as a collaborator can direct the creation of all of it. The human provides the judgment. The AI provides the throughput. The result is something that would have required institutional resources a decade ago, now built by one programmer with a prayer practice and a clear sense of what the tool should be.

This is what human-AI collaboration looks like when it's pointed at flourishing instead of engagement. No one is being optimized. No one is being monetized. No attention is being harvested. The tool exists to help people engage with Scripture, and every architectural decision, from localStorage to no accounts to free access to Reformed specificity, serves that purpose.

## The Simplest Summary

I believe that the values we embody, we embed. That what we optimize for personally, we tend to optimize for professionally. That the recursive loop between programmer consciousness and collective consciousness is real and consequential.

My values simplified to two lines: drink more water, pray continuously.

kjvstudy.org is what "pray continuously" looks like when a programmer takes it seriously. Not as a slogan. As a build spec.

The code serves the prayer. The prayer shapes the code. The tool serves the person who needs it most. And the whole thing, every verse, every commentary, every cross-reference, is free. Because Scripture was always free. The tools to study it should be too.

---

*This essay documents the building of [kjvstudy.org](https://kjvstudy.org), a free Bible study application. It connects to the values evolution described in [The Lego Bricks Era](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed), the design philosophy in [Designing for the Worst Day](/essays/2026-03-18-designing_for_the_worst_day), the "for humans" origin story in [From HTTP to Consciousness](/essays/2025-08-27-from_http_to_consciousness), the recursive responsibility framework in [The Recursive Loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds), and the contemplative approach to technical work in [Programming as Spiritual Practice](/essays/2025-08-26-programming_as_spiritual_practice). For critique of what happens when technology optimizes against human flourishing, see [The Algorithm Eats Virtue](/essays/2025-08-26-the_algorithm_eats_virtue).*

# KJV Study: A Digital Study Bible Built with AI

[kjvstudy.org](https://kjvstudy.org) is a comprehensive digital study companion for the King James Version Bible. Modern tools for an ancient text, built almost entirely through human-AI collaboration.

## What It Is

A free, fast, beautifully designed Bible study platform with the full text of the King James Version, cross-references, study notes, and search. Everything you need to engage deeply with scripture without the friction of clunky interfaces or paywalls.

## Features

- **Full Text Search**: Search across the entire King James Bible with instant results.
- **Cross References**: Extensive cross-referencing connecting related passages across books and testaments.
- **Study Notes**: AI-generated commentary providing historical, linguistic, and theological context.
- **Verse Highlighting**: Personal annotation and highlighting for your own study practice.
- **Reading Plans**: Structured approaches to reading and study.
- **Clean Design**: The technology serves the text, never the other way around.<label for="sn-kjv-for-humans" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-kjv-for-humans" class="margin-toggle"/><span class="sidenote">Same principle as everything else I make: [For Humans](/knowledge/philosophy/for-humans).</span>

## The Story

I built KJV Study as a deeply personal project, a way to bring the same "for humans" design philosophy I'd applied to [HTTP libraries](/software/requests) to something that matters to me spiritually. The King James Version deserves better than the cluttered, ad-laden Bible apps that dominate the market.<label for="sn-kjv-christianity" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-kjv-christianity" class="margin-toggle"/><span class="sidenote">For background on the tradition itself, see [Christianity](/knowledge/religions-of-the-world/christianity) in the Knowledge section.</span>

The entire application was built collaboratively with AI. Not generated and forgotten: designed, iterated, and refined through genuine human-AI partnership. The AI handled the scale (generating study notes for every chapter, building cross-reference databases), while I handled the vision and the care.<label for="sn-kjv-collab" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-kjv-collab" class="margin-toggle"/><span class="sidenote">More on how this kind of partnership works in practice: [Collaboration Patterns](/knowledge/ai/collaboration-patterns).</span>

I wrote about the full process in [Building a Digital Study Bible with AI](/essays/2026-03-20-building_a_digital_study_bible_with_ai).

## Philosophy

Bible study tools should feel like a quiet library, not a casino. No ads. No gamification. No dark patterns trying to maximize your "engagement." Just you and the text, with good tools at hand when you need them.<label for="sn-kjv-attention" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-kjv-attention" class="margin-toggle"/><span class="sidenote">[Attention](/knowledge/philosophy/attention) is the scarce thing here. The design's job is to protect it.</span>

This is what technology serving human consciousness looks like in practice: removing barriers between a person and the thing they're trying to understand.

## Examples

Every verse is reachable at a plain, readable URL, like [John 3:16](https://kjvstudy.org/book/John/chapter/3/verse/16). The same data is available through a REST API, with [interactive documentation](https://kjvstudy.org/api/docs):

```bash
$ curl https://kjvstudy.org/api/verse/John/3/16
{
  "book": "John",
  "chapter": 3,
  "verse": 16,
  "reference": "John 3:16",
  "text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
  "red_letter": "full"
}
```

Strong's numbers work the same way. Here's the Greek word for love:

```bash
$ curl https://kjvstudy.org/api/strongs/G26
{
  "strongs": "G26",
  "language": "Greek",
  "word": "ἀγάπη",
  "transliteration": "agápē",
  "definition": "love, i.e. affection or benevolence; specially (plural) a love-feast",
  ...
}
```

The interlinear view walks word by word through the Greek of the New Testament and the [Hebrew](/knowledge/hebrew-letters) of the Old, with morphological tagging and links into Strong's.

Or run the whole thing yourself:

```bash
$ git clone https://github.com/kennethreitz/kjvstudy.org.git
$ cd kjvstudy.org
$ docker compose up
# → http://localhost:8000
```

## Today

KJV Study is live at [kjvstudy.org](https://kjvstudy.org) and actively maintained by me. It's built with [Responder](/software/responder) and Tufte CSS, and the [source is on GitHub](https://github.com/kennethreitz/kjvstudy.org). It runs on [my own little server](/essays/2026-06-05-a_server_called_mercury), alongside most of my other sites.

Since this page was first written, it has grown well past a reading app: interlinear Hebrew and Greek, Strong's Concordance, red-letter text, family trees of biblical figures, topical studies, PDF export, and that API.

## Visit

- [kjvstudy.org](https://kjvstudy.org)
- [API Documentation](https://kjvstudy.org/api/docs)
- [Source Code on GitHub](https://github.com/kennethreitz/kjvstudy.org)

## Related

- [**Building a Digital Study Bible with AI**](/essays/2026-03-20-building_a_digital_study_bible_with_ai): The full story of building KJV Study.
- [**Designing for the Worst Day**](/essays/2026-03-18-designing_for_the_worst_day): The design philosophy behind tools that serve people.

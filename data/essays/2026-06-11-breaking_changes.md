# Breaking Changes

*June 2026*

The first DSM shipped in 1952. It was a spiral-bound thing of about 130 pages describing roughly a hundred disorders. The current release runs just under a thousand pages and describes around three hundred. Between those two artifacts sit five major versions, several point releases, a complete architectural rewrite in 1980, and a maintainer organization that publishes release notes.

I'm a software person, so I notice version numbers the way carpenters notice joints. A version number is a confession. It says: this document is built by people, it changes, the current release supersedes the last one, and there will be another. Nobody puts a version number on the truth. You version the things you expect to be wrong in ways you'll need to fix.

The APA knows this about its own book, and said so out loud. When the fifth edition was being prepared, they dropped the Roman numerals, DSM-V became DSM-5, and the stated reason was that Arabic numerals would let them ship incremental updates. A 5.1. A 5.2. Their words pointed straight at software release practices.<label for="sn-tr" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-tr" class="margin-toggle"/><span class="sidenote">What actually shipped in 2022 was the DSM-5-TR, a "text revision," which any engineer would recognize as a patch release. It still managed to add a new diagnosis: prolonged grief disorder. Grieving past a year became a billable condition in a point release. New features ship in patches more often than anyone admits.</span> The maintainers of the manual think of it as software. I think they're right. I just don't think the news has reached the people the manual is run against.

Because here's what I've watched for ten years from inside the system the manual organizes: clinicians cite the DSM like case law, insurers enforce it like statute, and patients receive their entry in it like scripture. Three groups treating a versioned document as a fixed one. And the people with the least power in that arrangement, the patients, are the ones who pay when a new version ships.

## Breaking changes

In my field we have a phrase for a release that changes behavior people depend on: a breaking change. There are rules about it, mostly unwritten and mostly honored. You warn people before you ship one. You document what changed and why. You provide a migration path, because you know, the way an adult knows things, that real people built real things on the old behavior, and they did so because you invited them to.

The DSM ships breaking changes to human beings, and it has never once shipped a migration path.

In 1973, homosexuality stopped being a mental disorder. The mechanism wasn't a discovery. There was no experiment, no scan, no blood test. The APA's board voted, the membership ratified it, and millions of people were depathologized by referendum. I wrote about this [in the last essay](/essays/2026-06-06-mental_health_for_humans) as evidence that the manual is a statistical document rather than a sacred one, and that's the cheerful reading: revisability is a feature, and the vote fixed a moral catastrophe. But hold the engineering frame for a second and look at what kind of release that was. An entire category of person, in the manual one printing and out the next. Everyone who had been diagnosed, treated, institutionalized, "cured" under the old version, what was the upgrade path for them? There wasn't one. There never is.

In 2013, the DSM-5 deleted Asperger's. Not renamed: removed, folded into the autism spectrum. By then the word had been load-bearing for almost twenty years. People had organized their self-understanding around it, met each other through it, taught their families what it meant, forgiven themselves a lifetime of friction because of it. The committee had its reasons, some of them good. None of those reasons changed what happened on the ground, which is that a generation woke up holding an identity the new release no longer defined. In software we'd call the old term deprecated. The people were the installed base.

My own migration was smaller, and I've [told it before](/essays/2026-06-06-mental_health_for_humans), so here it is in one breath: diagnosed Bipolar I with psychosis in 2016, re-diagnosed schizoaffective in 2019, and on the day the label changed I did not change. Same brain, same symptoms, same 3 a.m. The data held still while the schema moved. That experience is most of why I can't unsee the version numbers now.

## You don't receive a label. You join one.

Now the part the engineering frame usually misses, because it's not about the document. It's about what people do with it.

Nobody just gets a diagnosis anymore. You get a diagnosis and then you get a community. You google the noun and find the subreddit, the hashtag, the YouTubers, the memes, the merch. And I want to be careful here, because the first thing that happens in those rooms is genuinely precious: you read a stranger describing the inside of your head in better words than you had, and for a moment the loneliest fact of your life becomes a shared one. I've felt that. Anyone who sneers at it has never needed it.

But watch what's structurally happened. A committee's classification, built for routing treatment and billing insurers, drifted downstream and became a people. The label turned into a tribe, the tribe into an identity, the identity into a lens that decides which of your own behaviors you notice and what you call them. Your sense of self now has a dependency on a document you don't maintain. You didn't choose the maintainers. You can't see their roadmap. Their incentives, research fashion, insurance pressure, committee politics, diagnostic turf, have approximately nothing to do with you. And their next release can deprecate your tribe's founding noun, by vote, on a schedule you'll learn about from the news.

Building your identity on the DSM is building on somebody else's API. Every engineer eventually learns this lesson about platforms, usually the hard way: if you don't control it, don't make it load-bearing.<label for="sn-platforms" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-platforms" class="margin-toggle"/><span class="sidenote">The pattern is identical to building a business on a platform's API and waking up to changed terms. The platform was never yours. Neither is the manual. The difference is that nobody's selfhood was riding on the platform.</span>

Here's the thing, though. The communities already figured out the answer, even if nobody framed it this way. Ask the people who still call themselves aspies, a full decade after the committee deleted their word. The clinical establishment tends to read that as lag, or denial. I read it as the healthiest possible relationship to this document: they forked it. The committee kept the trademark; the community kept the meaning, and now maintains its own definition, governed by the people who actually live there. The fork doesn't need the upstream's permission, and the upstream's next release can't break it.

The plural community did it even more completely. The DSM's coverage of that territory is one contested diagnosis that practitioners [mostly use to argue about whether it exists](/essays/2026-06-06-mental_health_for_humans), so the people living it wrote their own vocabulary from scratch: systems, fronting, headmates, [language I've found more useful for my own experience](/plurality) than anything with a billing code attached. That's not anti-clinical rebellion. It's a spec maintained by its users instead of its vendors, and it serves the humans because the humans wrote it.

## Pin it, don't worship it

I keep coming back to the version number, because the version number is the most honest thing about the DSM. Scripture doesn't ship revisions. The manual does, and that's to its credit: a document that can fix the 1973 catastrophe by vote is better than one that can't. The problem was never that the DSM changes. The problem is everything in the culture that handles it like it doesn't, and every patient quietly taught to weld their identity to an artifact whose own maintainers are planning the next release.

So this is how I hold my own entry now, as a person whose label has already changed once underneath him. The diagnosis is a dependency, and I treat it the way I'd treat any dependency: pinned to the version that currently works, used for exactly what it's for, routing me toward [treatment that gives me my actual life](/essays/2026-04-06-what_success_looks_like), watched with mild interest when the maintainers announce changes. It gets no vote on who I am. The fork where I actually live, the self-understanding built with [the people who know me](/essays/2026-03-06-sarah_knows_first) and the communities who share the territory, has different maintainers. I'm one of them.

DSM-6 will ship eventually. Somewhere in it, categories will merge and split, and some number of people will wake up holding deprecated nouns, and the cycle will need writing about again. If my entry moves, I can tell you now what will happen on my end, because it's already happened once.

The schema will change. The data won't. I plan to still be here, unversioned.

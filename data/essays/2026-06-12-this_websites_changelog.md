# This Website's Changelog

*June 2026*

A changelog for a personal website is a strange genre. Nobody asked for release notes. There is no userbase waiting on a fix, unless you count me, and I already know what shipped. But this site is the closest thing I have to a workshop with the door propped open, and today the workshop got a lot of work done, so I'm writing it down. Half the value of [keeping a vault](/essays/2026-06-11-tending_the_vault) is that future-me gets to know what past-me was thinking. This essay is that, for the house itself.

## What Shipped Today

[Responder](/software/responder) put out three more releases this morning: 3.10, 3.11, and 3.12, hours apart, which brings the count to seven releases since [the essay about its five-year freeze](/essays/2026-06-11-a_framework_of_ones_own) went out yesterday. I have now revised that essay's release count upward three times. It is the most cheerful editing problem I have ever had, and I'm told the paragraph is getting suspicious of me.

The site upgraded the same hour, because that's the whole point of [a framework with a userbase of one](/essays/2026-04-16-infrastructure_for_one). The new toys are wired in: every page now carries a content-hash ETag automatically, repeat visitors get `304 Not Modified` instead of re-downloaded HTML, oversized requests bounce at the door, slow handlers get a timeout, and there's a Prometheus metrics endpoint now, because the framework grew one and the site exercises every feature the framework has. That's the deal between them.

Then came the part I didn't plan. I asked Claude to look at the site the way a stranger would, and the stranger found things the resident had stopped seeing.

The photography galleries were serving full-resolution originals as thumbnails. Three hundred fifty megabytes of photographs, and a gallery grid would happily push twenty-four megabytes of JPEG at you to render images three hundred pixels wide. Nobody complained, because nobody profiles their own house. There's a thumbnail service now; the same gallery ships about four hundred kilobytes. The originals are still one click away in the lightbox, untouched.

Dark mode used to flash white on every page load, because the theme was applied by a script at the bottom of the page, after the browser had already painted. If you read this site at night, you knew this site as the one that blinks at you. The theme applies before first paint now. The blink is gone.

And my favorite: the 404 page learned to guess. Mistype an essay slug and the site fuzzy-matches against everything it knows and asks, politely, *were you looking for one of these?* A personal site should treat a lost visitor the way you'd treat a lost guest, by walking them to the right room instead of shrugging.<label for="sn-smaller" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-smaller" class="margin-toggle"/><span class="sidenote">The smaller items, for completeness: static assets cache properly now, content images lazy-load, there's a skip-to-content link for keyboard and screen-reader users, the nav dropdowns finally open without a mouse, and the structured data points at each essay's own social card instead of a generic one. Boring, diligent, done.</span>

The software pages got a full polish pass too, every project page rewritten or tightened, stale download numbers corrected against live stats, broken links repaired. And one hundred sixty-five em-dashes removed, which deserves its own confession: I strip em-dashes from my writing because they're an AI tell, and the AI doing the stripping today was fully aware of the irony. We've made peace with it. The voice is mine; the stamina is borrowed.

## The Vault and the Site Are One Document

Here's the part of the machinery I've never properly documented. The words you're reading were not written in this repository. They were written in [my Obsidian vault](/essays/2026-03-06-obsidian_vaults_and_claude_code), in a folder called Writing/Essays, with wikilinks and footnotes and human-readable filenames, the way notes want to be written. The site wants something else entirely: slugged filenames, Tufte-style sidenote HTML, no frontmatter. Two formats, one body of writing.

A Python script bridges them. It lives in the vault at `.scripts/sync-repo.py`, it's a few hundred lines of standard library, and it syncs bidirectionally: newer file wins, by modification time, with content hashes underneath so that iCloud touching every mtime doesn't trigger a thousand false rewrites. On the way to the repo, vault frontmatter is stripped, footnotes become sidenotes, wikilinks become site URLs, and `Whatever This Is.md` becomes `2026-06-11-whatever_this_is.md` using the date and slug in the note's frontmatter. On the way back, all of it reverses. I edit wherever I happen to be standing, and the two trees converge.

The Obsidian side is a tiny plugin I wrote called KR Vault, which does nothing clever. It puts the scripts in the command palette:

```
Sync Essays (bidirectional)
Sync all (dry run)
Sync & push (commit and push to repo)
Publish draft (move to Essays, sync, push)
```

That last command is the whole writing pipeline in one keystroke. A draft graduates out of the Drafts folder, the sync runs, the commit pushes, and [Mercury](/essays/2026-06-05-a_server_called_mercury) serves it a moment later. There is no CMS, no admin panel, no deploy ceremony. There's a folder of markdown and a script that knows what both sides want. I've come to believe most publishing infrastructure is this, wearing a suit.

## The Part Where uv Makes It All Boring

None of this works without the dullest dependency story Python has ever had, and I mean that as the highest compliment. The site is a [uv](https://github.com/astral-sh/uv) project. `uv run python engine.py` starts it, on my laptop and on Mercury identically. When Responder 3.12 appeared on PyPI this morning, the upgrade was `uv add responder==3.12.0`, and the lockfile guaranteed that what I tested is what the server runs.

I maintained [Pipenv](/software/pipenv) for years, so I'm allowed to say this: the dream was always that environment management would become too fast to think about, and uv is the first tool where that's literally true. The environment resolves faster than I can alt-tab to check on it. Which matters more than it sounds like it should, because hesitation compounds. Every little ceremony between intent and execution is a tax on the impulse to improve things, and the impulse is the scarce resource. Seven framework releases landed on this site within hours of existing because the cost of trying the new version rounds to zero.

[I keep arriving at the same sentence from different directions](/essays/2026-06-11-a_framework_of_ones_own): the bottleneck was never the thinking. uv removed the bottleneck between deciding and running. Claude removed the one between caring and maintaining. What's left is just the thinking, which is the part I wanted to keep.

## Steps Moving Forward

There is no roadmap. A roadmap would imply this site is going somewhere other than deeper into itself.

The honest plan is the one I gave my collaborator this afternoon, in exactly these words: just keep polishing the mirror. [The site reflects what I put into it](/essays/2025-09-08-the_mirror_how_ai_reflects_what_we_put_into_it), the vault feeds the site, the site pressures the framework, the framework improves the site, and around it goes, one small careful pass at a time. Some days that's seven releases and a thumbnail service. Some days it's removing a single clause from the homepage because it stopped feeling true.

Both kinds of days are the work. The mirror doesn't need to be bigger. It needs to be clean.

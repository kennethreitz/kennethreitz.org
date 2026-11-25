# Onyx

**Notes, typeset.** A native Mac app for your Obsidian vault, typeset like a book. Obsidian-compatible, quiet, and fast. Your vault stays yours.

Your notes are a folder of Markdown files. Onyx opens that folder as it is: no import step, no conversion, no account. It does not phone home. Obsidian can keep running right alongside it.

I wrote about why it exists, and how to get it, in [Announcing Onyx](/essays/2026-11-25-announcing_onyx).

## What It Does

Onyx has two modes and one keystroke between them. The editor is IBM Plex Mono, with live Markdown styling. Press ⌘E and the same note becomes a typeset page, set in Latin Modern or ET Book: small caps, hyphenation, collision-free sidenotes, and `$` / `$$` math, with KaTeX bundled so it works offline.

It also opens the rest of a vault in place: Canvas files, Kanban boards, and Bases views. Dataview and DataviewJS run in the reader; DataviewJS runs in a sandbox with no network and no file writing. `partOf::` fields become real links, with an ancestry path in the title bar and their own edges in the graph. The focus graph puts the current note at the center; zoom out and the atlas shows the whole vault as regions you can travel into.

Other things the app already does, as described in the [repository](https://github.com/kennethreitz/onyx):

- Record Audio, with an on-device transcript written into the note. Nothing is uploaded. Read Aloud speaks the current note, or a selection, in the Mac's own voices.
- Drag, drop, or paste an image or file and it lands in your attachments folder, linked the way Obsidian would link it. Attachments open in place.
- Obsidian's core commands in a command palette, folding, split panes, a Markdown linter, and custom shortcuts.
- Optional git commit, pull, and push, and unofficial, opt-in Obsidian Sync, one vault at a time. The default is that nothing leaves your machine.
- File ▸ Export as PDF lays a note out as a printed page, or a folder as one typeset book with a table of contents.
- An OpenDyslexic option in Settings, off by default.

Saves are atomic and conflict-aware. If a file changed underneath you, Onyx asks whether to keep yours, take theirs, or keep both.

## Get It

The latest build is on [the releases page](https://github.com/kennethreitz/onyx/releases/latest). Unzip it and drag Onyx to Applications. It wants macOS 14 (Sonoma) or later, on Apple silicon or Intel.

The build isn't notarized yet, so the first launch needs System Settings ▸ Privacy & Security ▸ **Open Anyway**. After that, it checks for updates and installs them on its own (from v0.1.1 on). It's early, and moving fast. Back up your vault, or point Onyx at a copy, while it settles.

Or build from source:

```bash
$ git clone https://github.com/kennethreitz/onyx && cd onyx
$ make install
```

## License

Onyx is licensed under the [GNU Affero General Public License v3.0](https://github.com/kennethreitz/onyx/blob/master/LICENSE). The bundled typefaces, Latin Modern, ET Book, IBM Plex Mono, and OpenDyslexic, keep their own compatible licenses.

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/onyx)
- [Latest Release](https://github.com/kennethreitz/onyx/releases/latest)
- [Announcing Onyx](/essays/2026-11-25-announcing_onyx)

## Related

- [**Announcing Onyx**](/essays/2026-11-25-announcing_onyx): The announcement, and why the app exists.
- [**Draft to Document: Why I Made My Notes Look Like LaTeX Papers**](/essays/2026-11-04-draft_to_document): The Obsidian theme that came first.
- [**Designing for the Worst Day**](/essays/2026-03-18-designing_for_the_worst_day): The question the app was built around.

"""Sync Kenneth's Obsidian vault into the site.

One entry point publishes three things from a vault root (the directory that
contains ``Knowledge/`` and ``Library/``):

- ``Knowledge/`` regenerates ``data/knowledge/`` (wikilinks, callouts, and
  Dataview become ordinary Markdown).
- ``Library/Books/`` regenerates ``data/library/books/`` only.
- ``Library/Python Libraries/`` refreshes a delimited History block on the
  matching hand-written ``/software`` pages. Those pages are never wiped.

Scrubbed notes are not edited in the vault. A committed override replaces
the vault text at publish time:

    scripts/knowledge_overrides/<path relative to Knowledge/>.md
    scripts/library_overrides/<path relative to Library/>.md

Each directory has a ``manifest.json`` mapping that path to the sha256 of
the vault file the override was written against. If the vault file has
changed, sync prints a warning and still publishes the override. It does
not fail the run. The privacy guard runs on the text that would actually
be published (the override, when there is one).

Personal notes in ``HARD_EXCLUDE`` are never published, even if an override
exists. ``EXCLUDED`` notes are skipped unless an override is present.
``data/knowledge/mythology/egyptian-mythology/maat.md`` is kept across a
full wipe because the vault copy is a duplicate of the page already on
the site.

A full Knowledge sync deletes ``data/knowledge/`` and writes it again. That
is safe only against the whole vault. A vault with fewer than
``MIN_KNOWLEDGE_NOTES`` notes is refused unless ``--allow-partial`` is set,
in which case only the notes present are written and sibling pages stay.

    $ uv run python scripts/sync_vault.py --vault ~/Notes
    $ uv run python scripts/sync_vault.py --vault ~/Notes --dry-run
    $ make sync-vault VAULT=~/Notes

``--check`` exits 1 when the working tree does not already match what this
vault would write. ``--dry-run`` prints the same plan and writes nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
KNOWLEDGE_OVERRIDES = ROOT / "scripts" / "knowledge_overrides"
LIBRARY_OVERRIDES = ROOT / "scripts" / "library_overrides"

MIN_KNOWLEDGE_NOTES = 80

# Never publish these, override or not. Ma'at stays on the site via PRESERVE.
HARD_EXCLUDE = {
    "AI/AI Entities/Lilith.md",
    "AI/Archetype Map.md",
    "Mythology/Egyptian Mythology/Ma'at.md",
    "Psychology/Conditions/DID and OSDD.md",
    "Psychology/Conditions/Schizoaffective Disorder.md",
    "Psychology/Plurality.md",
}

# Personal notes skipped unless a scrubbed override is committed for them.
# Paths are relative to Knowledge/. Folder notes here still get a generated
# index of whatever children were safe to publish.
EXCLUDED = {
    "AI/AI Entities/AI Entities.md",
    "AI/AI Entities/Lilith.md",
    "AI/Archetype Map.md",
    "Key Concepts/Holding Space.md",
    "Key Concepts/Key Concepts.md",
    "Mythology/Egyptian Mythology/Ma'at.md",
    "Philosophy/Algorithm Eats/Algorithm Eats.md",
    "Philosophy/Philosophy.md",
    "Psychology/Conditions/Conditions.md",
    "Psychology/Conditions/DID and OSDD.md",
    "Psychology/Conditions/Schizoaffective Disorder.md",
    "Psychology/Plurality.md",
    "Psychology/Psychology.md",
    "Spirituality/Transformation.md",
    "Technology/Career Timeline.md",
    "Technology/Digital Legacy.md",
    "Technology/Open Source.md",
}

# Published earlier from the vault. A full wipe must not delete it while the
# vault copy stays withheld as a duplicate.
PRESERVE_KNOWLEDGE = {
    "mythology/egyptian-mythology/maat.md",
}

GUARD_ALLOW = {
    "Hebrew Letters/He.md",
    "Angels & Demons/Angels/Raphael.md",
    "Angels & Demons/Ars Goetia/Asmoday.md",
}

BUILTIN_GUARD = [
    r"[\w.+-]+@[\w-]+\.[a-z]{2,}",
    r"\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b",
    r"\b\d{1,5} [A-Z][a-z]+ (Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr)\b",
    r"\b(password|api[_ -]?key)\s*[:=]",
]

PRIVATE_TERMS_FILE = Path(
    os.environ.get(
        "KNOWLEDGE_PRIVATE_TERMS",
        Path.home() / ".config" / "krsite" / "knowledge-private-terms.txt",
    )
)

# Vault path relative to Library/ -> site path relative to data/.
# pytheory.md and pytheory-opxy.md share one History block.
HISTORY_MAP = (
    ("Python Libraries/HTTPBin.md", "software/websites/httpbin.md"),
    ("Python Libraries/Hitchhiker's Guide to Python.md", "software/websites/python-guide.md"),
    ("Python Libraries/Legacy Libraries.md", "software/legacy/index.md"),
    ("Python Libraries/Python Libraries.md", "software/index.md"),
    ("Python Libraries/certifi.md", "software/certifi.md"),
    ("Python Libraries/dj-database-url.md", "software/dj-database-url.md"),
    ("Python Libraries/maya.md", "software/maya.md"),
    ("Python Libraries/pipenv.md", "software/pipenv.md"),
    ("Python Libraries/pytheory.md", "software/pytheory.md"),
    ("Python Libraries/pytheory-opxy.md", "software/pytheory.md"),
    ("Python Libraries/records.md", "software/records.md"),
    ("Python Libraries/requests.md", "software/requests.md"),
    ("Python Libraries/responder.md", "software/responder.md"),
    ("Python Libraries/simplemind.md", "software/simplemind.md"),
    ("Python Libraries/tablib.md", "software/tablib.md"),
)

HISTORY_SUBTITLE = {
    "pytheory.md": "PyTheory",
    "pytheory-opxy.md": "OP-XY presets",
}

LINKIFY_SKIP = {
    "AI",
    "Books",
    "Design",
    "Family",
    "Health",
    "History",
    "Knowledge",
    "Library",
    "Music",
    "Mythology",
    "Notes",
    "Overview",
    "Philosophy",
    "Psychology",
    "Related",
    "Spirituality",
    "Technology",
    "Writing",
}

GREAT_BOOK_NEEDLES = (
    ("Hitchhiker's Guide to Python", "/library/books/hitchhikers-guide-to-python"),
    ("Hitchhiker's Guide to the Galaxy", "/library/books/the-hitchhikers-guide-to-the-galaxy"),
    ("Liber Novus", "/library/books/the-red-book"),
    ("DSM-5", "/library/books/dsm-5"),
    ("Be Here Now", "/library/books/remember-be-here-now"),
    ("Jnana Yoga", "/library/books/jnana-yoga"),
    ("The Power of Now", "/library/books/the-power-of-now"),
    ("The Amplified Bible", "/library/books/the-amplified-bible"),
    ("Liber 777", "/library/books/liber-777"),
    ("The Book of the Law", "/library/books/the-book-of-the-law"),
    ("The Kybalion", "/library/books/the-kybalion"),
)

LOWER_ALIASES = {"dopamine", "serotonin", "gaba", "oxytocin", "norepinephrine"}

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
FENCE = re.compile(r"^(```|~~~)")
# Em dashes, spaced en dashes, and spaced double hyphens. Bare "--" inside
# arrows ("-->") and flags ("--dev") must not match.
DASH = re.compile(r"\s*—\s*|\s+–\s+|\s+--\s+")
CALLOUT = re.compile(r"^(>\s*)\[!(\w+)\][+-]?\s*(.*)$")
HISTORY_BLOCK = re.compile(
    r"<!-- vault:history start -->.*?<!-- vault:history end -->\n?",
    re.DOTALL,
)
DATAVIEW = re.compile(
    r'TABLE\s+WITHOUT\s+ID\s+(?P<cols>.+?)\s+FROM\s+"(?P<src>[^"]+)"'
    r'(?:\s+WHERE\s+(?P<wk>[\w.-]+)\s*=\s*"(?P<wv>[^"]+)")?'
    r'(?:\s+SORT\s+(?P<sk>[\w.-]+)(?:\s+(?P<sd>ASC|DESC))?)?\s*$',
    re.DOTALL | re.IGNORECASE,
)
GENERATED_MARK = "part of the [Knowledge](/knowledge) collection."
CONJUNCTIONS = {
    "a", "an", "and", "as", "but", "for", "from", "in", "it", "it's", "its",
    "not", "of", "on", "or", "that", "the", "to", "when", "where", "which",
    "while", "who", "whose", "with", "without",
}
HISTORY_KEEP = (
    "creation", "problem", "solution", "philosoph", "gift", "first success",
    "manic", "the name", "sale", "heroku", "continuation", "the arc",
    "description", "greenfield", "curl", "invisible", "the pattern",
    "why it", "why not", "context", "pitch", "legacy", "impact",
    "12-factor", "companion", "current status", "landscape", "ecosystem",
    "used in practice", "pipfile", "successor", "transfer",
)


# --- text helpers -------------------------------------------------------


def slugify(name):
    name = name.replace("♭", " flat").replace("♯", " sharp").replace("&", " and ")
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower().replace("'", "").replace("’", "")
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return name or "note"


def heading_anchor(text):
    anchor = re.sub(r"[^\w\s-]", "", text.lower()).replace(" ", "-")
    return re.sub(r"-+", "-", anchor).strip("-")


def url_for(prefix, out_rel):
    out = out_rel[:-3] if out_rel.endswith(".md") else out_rel
    if out == "index" or out.endswith("/index"):
        out = out[: -len("index")].rstrip("/")
    prefix = prefix.rstrip("/")
    return f"{prefix}/{out}" if out else prefix or "/"


def split_frontmatter(text):
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, text[match.end():]


def without_fences(text):
    return re.sub(r"^(```|~~~).*?^\1", "", text, flags=re.DOTALL | re.MULTILINE)


def title_of(body, fallback):
    match = re.search(r"^# (.+?)\s*$", without_fences(body), re.MULTILINE)
    return match.group(1).strip() if match else fallback


def normalize_dashes(text):
    """Turn em dashes, spaced en dashes, and spaced double hyphens into prose."""

    def repl(match):
        before = match.string[: match.start()]
        after = match.string[match.end():]
        nxt = after.lstrip()
        if not nxt:
            return "."
        prev = before.rstrip().rstrip("*_").rstrip()
        name = re.match(
            r"([A-Z][\w.'’-]*(?:\s+[A-Z][\w.'’-]*){0,3})(?=$|[\s,.;:)\]])",
            nxt,
        )
        if prev.endswith((".", "!", "?")):
            # The sentence already ended. Keep the stop; don't add another mark.
            if name and nxt[name.end():].strip() == "":
                return " "
            return " "
        if name and prev.endswith(('"', "”", "'", "’")):
            rest = nxt[name.end():].strip()
            if rest == "":
                return ", "
        first = re.match(r"[A-Za-z''’]+", nxt)
        word = first.group(0) if first else ""
        # Only a lowercase connective is a continuation. "The" starts a sentence.
        if word.lower() in CONJUNCTIONS and word[:1].islower():
            return ", "
        left = before.rstrip()
        left_words = left.split()
        if len(left_words) <= 8 and not left.endswith((".", "!", "?")):
            return ": "
        if nxt[0].isupper() or nxt[0] in "\"“'":
            return ". "
        return ", "

    return DASH.sub(repl, text)


def normalize_prose_line(line):
    parts = re.split(r"(`[^`]*`)", line)
    for i, part in enumerate(parts):
        if len(part) > 1 and part.startswith("`") and part.endswith("`"):
            continue
        parts[i] = normalize_dashes(part)
    return "".join(parts)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key, value in data.items():
        if isinstance(value, dict):
            out[key] = value.get("sha256") or value.get("hash") or ""
        else:
            out[key] = str(value)
    return out


def build_guard(extra_terms=None, terms_file=None, warn_missing=False):
    patterns = list(BUILTIN_GUARD)
    for term in extra_terms or []:
        if term.strip():
            patterns.append(r"\b" + re.escape(term.strip()) + r"\b")
    path = PRIVATE_TERMS_FILE if terms_file is None else Path(terms_file)
    if path and path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(r"\b" + re.escape(line) + r"\b")
    elif warn_missing and terms_file is None:
        print(f"warning: no private term list at {path}", file=sys.stderr)
    return re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)


def warn(message, bucket):
    bucket.append(message)
    print(f"warning: {message}", file=sys.stderr)


# --- notes and links ----------------------------------------------------


class Note:
    def __init__(self, root, path, url_prefix):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.stem = path.stem
        self.slug = slugify(path.stem)
        raw = path.read_bytes()
        self.vault_sha = sha256_bytes(raw)
        self.text = raw.decode("utf-8")
        self.meta, self.body = split_frontmatter(self.text)
        parent = path.parent
        self.is_folder_note = parent != root and parent.name == path.stem
        folder_parts = [slugify(p) for p in parent.relative_to(root).parts]
        if self.is_folder_note:
            self.out_rel = "/".join(folder_parts + ["index.md"])
        else:
            self.out_rel = "/".join(folder_parts + [f"{self.slug}.md"])
        self.url = url_for(url_prefix, self.out_rel)
        self.used_override = False
        self.stale = False

    def replace_text(self, text):
        self.text = text
        self.meta, self.body = split_frontmatter(text)
        self.used_override = True


class Resolver:
    def __init__(self, notes, site_slugs):
        self.by_slug = {}
        self.by_path = {}
        for note in notes:
            self.by_slug.setdefault(note.slug, []).append(note)
            title_slug = slugify(title_of(note.body, note.stem))
            if title_slug != note.slug:
                self.by_slug.setdefault(title_slug, []).append(note)
            self.by_path[note.rel.lower()] = note
        self.site_slugs = site_slugs

    def resolve(self, target, source):
        target = target.strip().removesuffix(".md")
        if not target:
            return None
        key = target.lower()
        if "/" in key:
            note = self.by_path.get(key) or self.by_path.get(key.split("/", 1)[-1])
            # Path links: try the vault-relative path, then the final segment.
            if note is None:
                leaf = key.rsplit("/", 1)[-1]
                return self._from_leaf(leaf, source)
            return note.url
        return self._from_leaf(key, source)

    def _from_leaf(self, leaf, source):
        slug = slugify(leaf)
        candidates = self.by_slug.get(slug) or []
        if len(candidates) == 1:
            return candidates[0].url
        if len(candidates) > 1:
            src = source.rel.rsplit("/", 1)[0] if "/" in source.rel else ""
            best = max(
                candidates,
                key=lambda n: (len(os.path.commonprefix([n.rel, src])), -len(n.rel)),
            )
            return best.url
        return self.site_slugs.get(slug)


def site_slug_index(data_dir):
    """slug -> URL for pages already on disk. Prefer /knowledge, then /library."""
    found = {}

    def rank(url):
        if url.startswith("/knowledge"):
            return 0
        if url.startswith("/library"):
            return 1
        if url.startswith("/software"):
            return 2
        return 3

    def add(slug, url):
        if not slug or slug == "index":
            return
        current = found.get(slug)
        if current is None or rank(url) < rank(current):
            found[slug] = url

    if not data_dir.exists():
        return found
    for md in data_dir.rglob("*.md"):
        rel = md.relative_to(data_dir)
        if md.name == "index.md":
            url = "/" + rel.parent.as_posix()
            if url == "/.":
                url = "/"
            add(slugify(rel.parent.name), url)
        else:
            url = "/" + rel.with_suffix("").as_posix()
            add(slugify(md.stem), url)
        try:
            head = md.read_text(encoding="utf-8")[:2500]
        except (OSError, UnicodeDecodeError):
            continue
        match = re.search(r"^# (.+?)\s*$", head, re.MULTILINE)
        if match:
            add(slugify(match.group(1)), url)
    return found


# --- markdown conversion ------------------------------------------------


def convert_wikilinks(text, note, resolver, labels_only=False):
    def repl(match):
        embed, inner = match.group(1), match.group(2)
        inner = inner.replace("\\|", "|")
        target, _, alias = inner.partition("|")
        target, _, heading = target.partition("#")
        heading = heading.split("^", 1)[0].strip()
        label = (alias or (heading if not target and heading else target.rsplit("/", 1)[-1])).strip()
        if labels_only:
            return label or target.rsplit("/", 1)[-1]
        if not target:
            return f"[{label}](#{heading_anchor(heading)})" if heading else label
        url = resolver.resolve(target, note)
        if url is None:
            if embed and re.search(r"\.(png|jpe?g|gif|webp|svg|pdf)$", target, re.I):
                return ""
            return label
        if heading:
            url += "#" + heading_anchor(heading)
        if embed:
            return f"*See [{label}]({url}).*"
        return f"[{label}]({url})"

    return WIKILINK.sub(repl, text)


def inline_transform(line, note, resolver):
    parts = re.split(r"(`[^`]*`)", line)
    for i, part in enumerate(parts):
        if len(part) > 1 and part.startswith("`") and part.endswith("`"):
            continue
        part = convert_wikilinks(part, note, resolver)
        part = re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", part)
        part = normalize_dashes(part)
        parts[i] = part
    return "".join(parts)


def frontmatter_cell(value, note, resolver):
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(frontmatter_cell(v, note, resolver) for v in value)
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return inline_transform(text.replace("\\\\|", "\\|"), note, resolver)


def _dataview_src(src):
    src = src.strip().strip("/")
    for prefix in ("Knowledge/", "Library/"):
        if src.startswith(prefix):
            src = src[len(prefix):]
    return src.strip("/") + "/"


def render_dataview(query, note, notes_by_rel, resolver):
    match = DATAVIEW.match(query.strip())
    if not match:
        return ""
    cols = []
    for col in re.split(r",\s*(?=[\w.-]+\s+AS\s+\")", match.group("cols"), flags=re.I):
        parsed = re.match(r'([\w.-]+)\s+AS\s+"([^"]+)"', col.strip(), re.I)
        if parsed:
            cols.append(parsed.groups())
    src = _dataview_src(match.group("src"))
    rows = [
        n for rel, n in notes_by_rel.items()
        if rel.startswith(src) and "/" not in rel[len(src):] and not n.is_folder_note
        and (not match.group("wk") or str(n.meta.get(match.group("wk"))) == match.group("wv"))
    ]
    sort_key_name = match.group("sk")
    if sort_key_name:
        def sort_key(n):
            value = n.stem if sort_key_name == "file.name" else n.meta.get(sort_key_name)
            return (value is None, value if isinstance(value, (int, float)) else str(value or ""))

        try:
            rows.sort(key=sort_key, reverse=(match.group("sd") or "ASC").upper() == "DESC")
        except TypeError:
            rows.sort(key=lambda n: str(sort_key(n)))
    if not rows or not cols:
        return ""
    out = [
        "| " + " | ".join(heading for _, heading in cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for n in rows:
        cells = []
        for field, _heading in cols:
            if field == "file.link":
                cells.append(f"[{title_of(n.body, n.stem)}]({n.url})")
            elif field == "file.name":
                cells.append(n.stem)
            else:
                cells.append(frontmatter_cell(n.meta.get(field), note, resolver))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def convert_body(note, resolver, notes_by_rel):
    body = re.sub(r"%%.*?%%", "", note.body, flags=re.DOTALL)
    body = re.sub(r"(?m)^[A-Za-z][\w-]*::[^\n]*\n?", "", body)
    body = re.sub(r"(?m)[ \t]+\^[A-Za-z0-9-]+$", "", body)
    out = []
    fence = None
    for line in body.split("\n"):
        if fence is not None:
            marker, lang, buf = fence
            if line.strip().startswith(marker):
                if lang == "dataview":
                    table = render_dataview("\n".join(buf[1:]), note, notes_by_rel, resolver)
                    if table:
                        out.append(table)
                elif lang in ("dataviewjs", "base"):
                    pass
                elif lang == "mermaid":
                    out.append(buf[0])
                    for inner in buf[1:]:
                        inner = convert_wikilinks(inner, note, resolver, labels_only=True)
                        inner = normalize_dashes(inner)
                        out.append(inner)
                    out.append(line)
                else:
                    out.extend(buf)
                    out.append(line)
                fence = None
            else:
                buf.append(line)
            continue
        fence_match = FENCE.match(line.strip())
        if fence_match:
            fence = (fence_match.group(1), line.strip()[3:].strip().lower(), [line])
            continue
        callout = CALLOUT.match(line)
        if callout:
            title = callout.group(3).strip() or callout.group(2).capitalize()
            out.append(f"{callout.group(1)}**{inline_transform(title, note, resolver)}**")
            out.append(callout.group(1).rstrip())
            continue
        out.append(inline_transform(line, note, resolver))
    if fence is not None and fence[1] not in ("dataview", "dataviewjs", "base"):
        out.extend(fence[2])
    return "\n".join(out)


def clean_description(text):
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
    text = normalize_dashes(text)
    return re.sub(r"\s+", " ", text).strip().strip('"')


def build_page(note, resolver, notes_by_rel, source):
    body = convert_body(note, resolver, notes_by_rel).strip("\n")
    title = title_of(note.body, note.stem)
    if not re.search(r"^# .+$", without_fences(body), re.MULTILINE):
        body = f"# {title}\n\n{body}"
    meta = {}
    description = note.meta.get("description") or note.meta.get("essence")
    if not description:
        quote = re.search(r"^>\s*\*(.+?)\*\s*$", note.body, re.MULTILINE)
        if quote:
            description = quote.group(1)
    if description:
        meta["description"] = clean_description(str(description))
    if source == "obsidian-library":
        if note.meta.get("author"):
            meta["author"] = str(note.meta["author"]).strip()
        if note.meta.get("year") is not None and not note.is_folder_note:
            year = note.meta["year"]
            meta["year"] = year if isinstance(year, int) else str(year).strip()
    aliases = note.meta.get("aliases") or note.meta.get("alias")
    if aliases:
        meta["aliases"] = [aliases] if isinstance(aliases, str) else [str(a) for a in aliases]
    meta["source"] = source
    front = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{front}\n---\n\n{body}\n"


# --- indexes ------------------------------------------------------------


def is_generated_index(text):
    if not text or GENERATED_MARK not in text:
        return False
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return "\n## " not in body


def blurb_from_text(text):
    meta, body = split_frontmatter(text)
    desc = meta.get("description") or ""
    if not desc:
        quote = re.search(r"^>\s*\*(.+?)\*", body, re.MULTILINE)
        desc = quote.group(1) if quote else ""
    desc = clean_description(str(desc)) if desc else ""
    # A dash after a finished sentence sometimes leaves a lowercase tail.
    desc = re.sub(r"\.\s+(?=[a-z]).*$", ".", desc)
    if desc and desc[-1] not in ".!?":
        desc += "."
    return desc


def h1_from_text(text, fallback):
    _meta, body = split_frontmatter(text)
    return title_of(body, fallback)


def render_generated_index(title, items):
    lines = [
        "---",
        "source: obsidian-knowledge",
        "---",
        "",
        f"# {title}",
        "",
        f"Notes on {title}, part of the [Knowledge](/knowledge) collection.",
        "",
    ]
    for item_title, url, blurb in items:
        if blurb:
            lines.append(f"- [{item_title}]({url}): {blurb}")
        else:
            lines.append(f"- [{item_title}]({url}).")
    lines.append("")
    return "\n".join(lines)


def _child_entries(rel_dir, knowledge_root, page_text):
    """Direct children of a knowledge directory, mixing disk and planned pages."""
    children = {}
    disk = knowledge_root / rel_dir if rel_dir else knowledge_root
    prefix = f"{rel_dir}/" if rel_dir else ""
    if disk.exists():
        for path in disk.iterdir():
            if path.name.startswith("."):
                continue
            if path.is_dir():
                children[path.name] = ("dir", None)
            elif path.suffix == ".md" and path.name != "index.md":
                children[path.name] = ("file", path.name)
    for rel in page_text:
        if not rel.startswith(prefix):
            continue
        rest = rel[len(prefix):]
        if "/" not in rest and rest.endswith(".md") and rest != "index.md":
            children[rest] = ("file", rest)
        elif rest.endswith("/index.md") and rest.count("/") == 1:
            children[rest.split("/", 1)[0]] = ("dir", None)
    return children


def _read_planned(rel, knowledge_root, page_text):
    if rel in page_text:
        return page_text[rel]
    path = knowledge_root / rel
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def fill_generated_indexes(knowledge_root, page_text):
    """Replace stub indexes with a list of their published children."""
    dirs = {""}
    for rel in list(page_text):
        parts = Path(rel).parts[:-1]
        for i in range(len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    if knowledge_root.exists():
        for path in knowledge_root.rglob("*"):
            if path.is_dir():
                dirs.add(path.relative_to(knowledge_root).as_posix())
    def _depth(rel_dir):
        return 0 if not rel_dir else len(Path(rel_dir).parts)

    # Deepest directories first so a parent stub can quote a child stub
    # that this same pass just filled. "" is the knowledge root.
    for rel_dir in sorted(dirs, key=lambda d: -_depth(d)):
        index_rel = f"{rel_dir}/index.md" if rel_dir else "index.md"
        # A real folder note from the vault owns this index.
        if index_rel in page_text and not is_generated_index(page_text[index_rel]):
            continue
        existing = page_text.get(index_rel)
        if existing is None:
            disk_index = knowledge_root / index_rel
            if disk_index.exists():
                existing = disk_index.read_text(encoding="utf-8")
        if existing is None:
            # Only synthesize an index when this run actually added pages here
            # and nothing richer is on disk.
            kids = _child_entries(rel_dir, knowledge_root, page_text)
            if not kids:
                continue
            existing = ""
        if existing and not is_generated_index(existing):
            continue
        if not existing and index_rel not in page_text:
            # Don't invent indexes for untouched folders.
            added_here = any(
                (rel.startswith(rel_dir + "/") if rel_dir else True) and rel != index_rel
                for rel in page_text
            )
            if not added_here:
                continue
        kids = _child_entries(rel_dir, knowledge_root, page_text)
        items = []
        for name, (kind, _leaf) in kids.items():
            if kind == "file":
                rel = f"{rel_dir}/{name}" if rel_dir else name
                text = _read_planned(rel, knowledge_root, page_text)
                if not text:
                    continue
                item_title = h1_from_text(text, Path(name).stem)
                items.append((item_title, url_for("/knowledge", rel), blurb_from_text(text)))
            else:
                child_index = f"{rel_dir}/{name}/index.md" if rel_dir else f"{name}/index.md"
                text = _read_planned(child_index, knowledge_root, page_text)
                if not text:
                    continue
                item_title = h1_from_text(text, name.replace("-", " ").title())
                items.append((item_title, url_for("/knowledge", child_index), blurb_from_text(text)))
        items.sort(key=lambda item: item[0].casefold())
        if not items and not existing:
            continue
        fallback = Path(rel_dir).name.replace("-", " ").title() if rel_dir else "Knowledge"
        title = h1_from_text(existing, fallback) if existing else fallback
        page_text[index_rel] = render_generated_index(title, items)


def linkify_text(text, title_to_url, page_url=None):
    """Link the first plain mention of each new title.

    A phrase whose URL is already in the file is left alone, so a second
    sync does not keep linking later mentions. Headings are left alone so
    an index title cannot swallow the words inside it.
    """
    phrases = []
    for phrase in sorted(title_to_url, key=len, reverse=True):
        url = title_to_url[phrase]
        if page_url and url == page_url:
            continue
        if url in text:
            continue
        phrases.append(phrase)
    used = set()

    def link_chunk(chunk):
        for phrase in phrases:
            if phrase in used:
                continue
            url = title_to_url[phrase]
            pattern = re.compile(rf"(?<![\w\[/]){re.escape(phrase)}(?![\w\]])")
            match = pattern.search(chunk)
            if not match:
                continue
            start, end = match.span()
            chunk = chunk[:start] + f"[{phrase}]({url})" + chunk[end:]
            used.add(phrase)
        return chunk

    def link_prose(prose):
        lines = []
        for line in prose.splitlines(keepends=True):
            if re.match(r"#{1,6} ", line):
                lines.append(line)
                continue
            pieces = re.split(r"(\[[^\]]*\]\([^)]*\)|`[^`]*`)", line)
            lines.append("".join(
                piece if piece.startswith(("[", "`")) else link_chunk(piece)
                for piece in pieces
            ))
        return "".join(lines)

    blocks = re.split(r"(```.*?```)", text, flags=re.DOTALL)
    return "".join(block if block.startswith("```") else link_prose(block) for block in blocks)


def linkify_indexes(knowledge_root, page_text, title_to_url):
    if not title_to_url:
        return
    index_rels = set()
    for rel in page_text:
        if rel.endswith("index.md") or rel == "index.md":
            index_rels.add(rel)
    if knowledge_root.exists():
        for path in knowledge_root.rglob("index.md"):
            index_rels.add(path.relative_to(knowledge_root).as_posix())
    for rel in sorted(index_rels):
        current = page_text.get(rel)
        if current is None:
            disk = knowledge_root / rel
            if not disk.exists():
                continue
            current = disk.read_text(encoding="utf-8")
        updated = linkify_text(current, title_to_url, url_for("/knowledge", rel))
        if updated != current:
            page_text[rel] = updated


# --- history ------------------------------------------------------------


def _keep_history_heading(heading):
    lowered = heading.lower().strip()
    return any(key in lowered for key in HISTORY_KEEP)


def _strip_stale_figures(text):
    kept = []
    for line in text.splitlines():
        if re.search(r"\b\d[\d,]*\s*(?:\+|plus)?\s*(?:million|billion)\b", line, re.I):
            continue
        if re.search(r"\bdownloads?\b", line, re.I) and re.search(r"\d", line):
            continue
        if re.search(r"\bv?\d+\.\d+\.\d+\b", line):
            continue
        if re.search(r"\b\d+(?:-\d+)?x\b", line, re.I):
            continue
        if re.match(r"\s*[-*]\s+\**\d", line):
            continue
        kept.append(line)
    return "\n".join(kept)


def _strip_tables_and_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    lines = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            continue
        lines.append(line)
    return "\n".join(lines)


def extract_history(page_markdown):
    """Short origin prose from a converted library note. No version stats."""
    _meta, body = split_frontmatter(page_markdown)
    body = _strip_tables_and_code(body)
    sections = re.split(r"(?m)^(#{2,3} .+)$", body)
    # sections[0] is the preamble (title and blockquote). Then pairs.
    kept = []
    preamble = sections[0]
    # Drop the H1 and the opening blockquote from the preamble.
    preamble = re.sub(r"(?m)^# .+\n+", "", preamble)
    preamble = re.sub(r"(?m)^>.*\n?", "", preamble).strip()
    chunks = [preamble] if preamble else []
    for i in range(1, len(sections), 2):
        heading = sections[i].lstrip("#").strip()
        section_body = sections[i + 1] if i + 1 < len(sections) else ""
        if _keep_history_heading(heading):
            chunks.append(section_body.strip())
    text = "\n\n".join(chunk for chunk in chunks if chunk.strip())
    text = _strip_stale_figures(text)
    text = re.sub(r"(?m)^---+\s*$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    clipped = []
    total = 0
    for paragraph in paragraphs:
        if len(clipped) >= 8 or total >= 2200:
            break
        clipped.append(paragraph)
        total += len(paragraph)
    return "\n\n".join(clipped).strip()


def render_history_block(parts):
    """parts: list of (optional subtitle, prose)."""
    parts = [(subtitle, prose) for subtitle, prose in parts if prose]
    body = []
    multiple = len(parts) > 1
    for subtitle, prose in parts:
        if multiple and subtitle:
            body.append(f"### {subtitle}\n\n{prose}")
        else:
            body.append(prose)
    if not body:
        return ""
    inner = "\n\n".join(body).strip()
    return (
        "<!-- vault:history start -->\n"
        "## History\n\n"
        f"{inner}\n"
        "<!-- vault:history end -->\n"
    )


def upsert_history(text, block):
    if not block:
        return text
    if HISTORY_BLOCK.search(text):
        return HISTORY_BLOCK.sub(lambda _m: block if block.endswith("\n") else block + "\n", text, count=1)
    match = re.search(r"(?m)^## Related\b", text)
    insertion = "\n" + block
    if not insertion.endswith("\n"):
        insertion += "\n"
    if match:
        return text[: match.start()] + insertion + "\n" + text[match.start():]
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block


# --- great books --------------------------------------------------------


def crosslink_great_books(text):
    lines = []
    for line in text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        raw = line[:-1] if newline else line
        if "/library/books/" in raw:
            lines.append(line)
            continue
        for needle, url in GREAT_BOOK_NEEDLES:
            if needle in raw and "amzn.to" in raw:
                raw = re.sub(
                    r"\]\((https://amzn\.to/[^)]+)\)",
                    lambda m, url=url: f"]({url}) ([buy]({m.group(1)}))",
                    raw,
                    count=1,
                )
                raw = re.sub(r"\)\s+[—–]\s+", "): ", raw, count=1)
                raw = normalize_prose_line(raw)
                break
        lines.append(raw + newline)
    text = "".join(lines)
    footer = (
        "\nNotes on these, and the rest of the shelf, are in the "
        "[library](/library/books).\n"
    )
    if "rest of the shelf" not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += footer
    return text


def crosslink_knowledge_books(text):
    old = "See also Books in the Library for the reading that feeds these domains."
    new = "See also [Books](/library/books) for the reading that feeds these domains."
    if old in text:
        text = text.replace(old, new)
    return text


# --- source selection ---------------------------------------------------


def iter_markdown(root):
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        yield path


def choose_text(note, overrides_dir, manifest, guard, hard_exclude, excluded, warnings):
    """Return publishable source text, or None if the note is withheld.

    The reason is appended to note.withhold when skipped. Stale overrides
    publish anyway.
    """
    rel = note.rel
    if rel in hard_exclude:
        return None, "excluded"
    override = overrides_dir / rel
    recorded = manifest.get(rel)
    if override.exists():
        text = override.read_text(encoding="utf-8")
        if not recorded:
            note.stale = True
            warn(f"override has no recorded source hash: {rel}", warnings)
        elif recorded != note.vault_sha:
            note.stale = True
            warn(
                f"override stale for {rel}: the vault note changed since it was scrubbed",
                warnings,
            )
        if rel not in GUARD_ALLOW and guard.search(text):
            return None, "privacy guard"
        return text, None
    if recorded:
        warn(f"scrub override missing for {rel}; vault note withheld", warnings)
        return None, "scrub override missing"
    if rel in excluded:
        return None, "excluded"
    if rel not in GUARD_ALLOW and guard.search(note.text):
        return None, "privacy guard"
    return note.text, None


def collect_notes(
    root, url_prefix, overrides_dir, manifest, guard, hard_exclude, excluded, warnings,
    include_prefix=None,
):
    published = []
    withheld = []
    if not root.is_dir():
        return published, withheld
    for path in iter_markdown(root):
        note = Note(root, path, url_prefix)
        if include_prefix and not note.rel.startswith(include_prefix):
            continue
        text, reason = choose_text(
            note, overrides_dir, manifest, guard, hard_exclude, excluded, warnings
        )
        if text is None:
            withheld.append((note.rel, reason))
            continue
        if (overrides_dir / note.rel).exists():
            note.replace_text(text)
        published.append(note)
    return published, withheld


# --- planning ------------------------------------------------------------


class SyncResult:
    def __init__(self):
        self.writes = {}  # Path -> text
        self.deletes = []
        self.withheld = []
        self.stale = []
        self.warnings = []
        self.added = []
        self.updated = []
        self.unchanged = []
        self.removed = []

    def summary(self):
        lines = [
            f"add {len(self.added)}, update {len(self.updated)}, "
            f"unchanged {len(self.unchanged)}, remove {len(self.removed)}",
            f"withheld {len(self.withheld)}, stale overrides {len(self.stale)}",
        ]
        for rel, reason in self.withheld:
            lines.append(f"  withheld ({reason}): {rel}")
        for rel in self.stale:
            lines.append(f"  stale: {rel}")
        return "\n".join(lines)


def _classify(result):
    for path, content in result.writes.items():
        rel = str(path)
        if not path.exists():
            result.added.append(rel)
        elif path.read_text(encoding="utf-8") != content:
            result.updated.append(rel)
        else:
            result.unchanged.append(rel)
    for path in result.deletes:
        if path.exists():
            result.removed.append(str(path))


def _history_title_map(notes):
    titles = {}
    for note in notes:
        if note.is_folder_note:
            continue
        # Title is read from the source body, which still has the H1.
        titles[title_of(note.body, note.stem)] = note.url
        if note.slug in LOWER_ALIASES or title_of(note.body, note.stem).lower() in LOWER_ALIASES:
            titles[title_of(note.body, note.stem).lower()] = note.url
    return titles


def plan_sync(
    vault,
    data_dir=DATA_DIR,
    *,
    allow_partial=False,
    min_knowledge_notes=MIN_KNOWLEDGE_NOTES,
    knowledge_overrides=KNOWLEDGE_OVERRIDES,
    library_overrides=LIBRARY_OVERRIDES,
    extra_terms=None,
    terms_file=None,
    warn_missing_terms=False,
):
    vault = Path(vault).expanduser()
    data_dir = Path(data_dir)
    knowledge_root_vault = vault / "Knowledge"
    library_root = vault / "Library"
    books_root = library_root / "Books"
    libraries_root = library_root / "Python Libraries"
    if not knowledge_root_vault.is_dir() and not books_root.is_dir() and not libraries_root.is_dir():
        raise SystemExit(f"no Knowledge/ or Library/ under {vault}")

    knowledge_count = sum(1 for _ in iter_markdown(knowledge_root_vault)) if knowledge_root_vault.is_dir() else 0
    partial = allow_partial
    if knowledge_root_vault.is_dir() and knowledge_count < min_knowledge_notes and not allow_partial:
        raise SystemExit(
            f"vault Knowledge/ has {knowledge_count} notes. Refusing to wipe "
            f"data/knowledge without --allow-partial. A full sync expects the "
            f"whole vault ({min_knowledge_notes}+ notes)."
        )

    result = SyncResult()
    guard = build_guard(extra_terms, terms_file=terms_file, warn_missing=warn_missing_terms)
    k_manifest = load_manifest(Path(knowledge_overrides) / "manifest.json")
    l_manifest = load_manifest(Path(library_overrides) / "manifest.json")

    knowledge_notes, knowledge_withheld = collect_notes(
        knowledge_root_vault,
        "/knowledge",
        Path(knowledge_overrides),
        k_manifest,
        guard,
        HARD_EXCLUDE,
        EXCLUDED,
        result.warnings,
    )
    # Root is Library/ so Books/Books.md becomes data/library/books/index.md
    # and override paths stay relative to Library/.
    book_notes, book_withheld = collect_notes(
        library_root,
        "/library",
        Path(library_overrides),
        l_manifest,
        guard,
        set(),
        set(),
        result.warnings,
        include_prefix="Books/",
    )
    # Python library notes are history sources, not pages. Same Library-relative paths.
    library_notes, library_withheld = collect_notes(
        library_root,
        "/library",
        Path(library_overrides),
        l_manifest,
        guard,
        set(),
        set(),
        result.warnings,
        include_prefix="Python Libraries/",
    )
    result.withheld.extend(knowledge_withheld)
    result.withheld.extend(book_withheld)
    result.withheld.extend(library_withheld)
    result.stale = [n.rel for n in knowledge_notes + book_notes + library_notes if n.stale]

    seen = {}
    for note in knowledge_notes:
        if note.out_rel in seen:
            raise SystemExit(f"slug collision: {note.rel} and {seen[note.out_rel]} -> {note.out_rel}")
        seen[note.out_rel] = note.rel

    site = site_slug_index(data_dir)
    # Planned notes win over whatever is already on disk when slugs collide.
    resolver = Resolver(knowledge_notes + book_notes, site)
    knowledge_by_rel = {n.rel: n for n in knowledge_notes}
    books_by_rel = {n.rel: n for n in book_notes}
    all_by_rel = {**knowledge_by_rel, **books_by_rel}

    knowledge_pages = {}
    preexisting_knowledge = set()
    k_root = data_dir / "knowledge"
    if k_root.exists():
        for path in k_root.rglob("*.md"):
            preexisting_knowledge.add(path.relative_to(k_root).as_posix())

    for note in knowledge_notes:
        knowledge_pages[note.out_rel] = build_page(
            note, resolver, all_by_rel, "obsidian-knowledge"
        )

    new_titles = {}
    for note in knowledge_notes:
        title = title_of(note.body, note.stem)
        if title in LINKIFY_SKIP:
            continue
        if note.used_override or note.out_rel not in preexisting_knowledge:
            new_titles[title] = note.url
            if title.lower() in LOWER_ALIASES:
                new_titles[title.lower()] = note.url
    for note in book_notes:
        if note.is_folder_note:
            continue
        title = title_of(note.body, note.stem)
        new_titles[title] = note.url

    fill_generated_indexes(k_root, knowledge_pages)
    # Stub titles worth linking from other indexes, except generic domain names.
    for rel, text in list(knowledge_pages.items()):
        if rel.endswith("index.md") and is_generated_index(text):
            title = h1_from_text(text, "")
            if title and title not in LINKIFY_SKIP and note_added(rel, knowledge_notes):
                new_titles.setdefault(title, url_for("/knowledge", rel))
    linkify_indexes(k_root, knowledge_pages, new_titles)

    knowledge_index = knowledge_pages.get("index.md")
    if knowledge_index is None and (k_root / "index.md").exists():
        knowledge_index = (k_root / "index.md").read_text(encoding="utf-8")
    if knowledge_index is not None:
        linked = crosslink_knowledge_books(knowledge_index)
        if linked != knowledge_index:
            knowledge_pages["index.md"] = linked

    for rel, text in knowledge_pages.items():
        result.writes[k_root / rel] = text

    if not partial and knowledge_root_vault.is_dir():
        if k_root.exists():
            for path in k_root.rglob("*.md"):
                rel = path.relative_to(k_root).as_posix()
                if rel in PRESERVE_KNOWLEDGE and (k_root / rel) not in result.writes:
                    result.writes[path] = path.read_text(encoding="utf-8")
                elif (k_root / rel) not in result.writes and rel not in PRESERVE_KNOWLEDGE:
                    result.deletes.append(path)
    elif k_root.exists():
        for rel in PRESERVE_KNOWLEDGE:
            path = k_root / rel
            if path.exists() and path not in result.writes:
                # Partial runs do not delete it. Nothing to do.
                pass

    library_data = data_dir / "library"
    for note in book_notes:
        result.writes[library_data / note.out_rel] = build_page(
            note, resolver, all_by_rel, "obsidian-library"
        )
    books_out = library_data / "books"
    if books_root.is_dir() and books_out.exists():
        planned = {library_data / n.out_rel for n in book_notes}
        for path in books_out.rglob("*.md"):
            if path not in planned:
                result.deletes.append(path)

    # History blocks. Group sources by destination page.
    by_target = {}
    notes_by_rel = {n.rel: n for n in library_notes}
    for src_rel, dest_rel in HISTORY_MAP:
        by_target.setdefault(dest_rel, []).append(src_rel)
    # Library notes must not steal /software slugs. Resolve their wikilinks
    # against published knowledge, books, and pages already on the site.
    lib_resolver = Resolver(knowledge_notes + book_notes, site)
    for dest_rel, sources in by_target.items():
        parts = []
        present = False
        for src_rel in sources:
            note = notes_by_rel.get(src_rel)
            if note is None:
                continue
            present = True
            page = build_page(note, lib_resolver, all_by_rel, "obsidian-library")
            prose = extract_history(page)
            subtitle = HISTORY_SUBTITLE.get(Path(src_rel).name, "")
            parts.append((subtitle, prose))
        if not present:
            continue
        block = render_history_block(parts)
        dest = data_dir / dest_rel
        if not dest.exists():
            warn(f"history target missing, skipped: {dest_rel}", result.warnings)
            continue
        original = dest.read_text(encoding="utf-8")
        updated = upsert_history(original, block) if block else original
        if updated != original:
            result.writes[dest] = updated
        elif block and dest not in result.writes:
            # Still record it so check sees the managed block as unchanged.
            result.writes[dest] = original

    great = data_dir / "great-books.md"
    if great.exists() and book_notes:
        original = great.read_text(encoding="utf-8")
        updated = crosslink_great_books(original)
        result.writes[great] = updated

    _classify(result)
    return result


def note_added(index_rel, notes):
    parent = index_rel[: -len("index.md")].rstrip("/")
    for note in notes:
        if note.out_rel == index_rel:
            return False
        if parent and note.out_rel.startswith(parent + "/"):
            return True
        if not parent and "/" not in note.out_rel:
            return True
    return False


def apply_result(result):
    for path in result.deletes:
        if path.exists():
            path.unlink()
    # Remove empty directories left under managed trees.
    for path, content in result.writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")


def sync_all(vault, dry_run=False, check=False, **kwargs):
    result = plan_sync(vault, **kwargs)
    if check:
        changed = result.added or result.updated or result.removed
        print(result.summary())
        if changed:
            print("check failed: working tree does not match this vault", file=sys.stderr)
            return result, 1
        return result, 0
    if not dry_run:
        apply_result(result)
    print(result.summary())
    return result, 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--vault", default=os.environ.get("OBSIDIAN_VAULT", str(Path.home() / "Notes")))
    parser.add_argument("--dry-run", action="store_true", help="report changes and write nothing")
    parser.add_argument("--check", action="store_true", help="exit 1 if the tree does not match")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="sync a vault that is not the full Knowledge folder; do not wipe siblings",
    )
    parser.add_argument("--data", default=str(DATA_DIR), help="data directory to write")
    args = parser.parse_args(argv)
    try:
        _result, code = sync_all(
            args.vault,
            dry_run=args.dry_run,
            check=args.check,
            allow_partial=args.allow_partial,
            data_dir=Path(args.data),
            warn_missing_terms=True,
        )
    except SystemExit as exc:
        if exc.code not in (0, None):
            print(exc.code, file=sys.stderr)
            return exc.code if isinstance(exc.code, int) else 1
        raise
    return code


if __name__ == "__main__":
    sys.exit(main())

"""Publish the Knowledge folder of the Obsidian vault as /knowledge.

Re-runnable: wipes data/knowledge/ and regenerates it from the vault, so
the site can be re-synced whenever the vault grows.

    $ uv run python scripts/import_knowledge.py --vault ~/Notes

What it does:

- Mirrors the vault's ``Knowledge/`` hierarchy under ``data/knowledge/``
  with URL-friendly slugs. Obsidian folder notes (``Tarot/Tarot.md``)
  become the folder's ``index.md``.
- Converts Obsidian syntax: ``[[wikilinks]]`` and ``[[target|alias]]``
  become site links when the target is published (in Knowledge or
  elsewhere on the site), and plain text otherwise -- never a broken
  link. ``![[embeds]]`` become links, callouts become blockquotes,
  ``%%comments%%`` are stripped, ``==highlights==`` become ``<mark>``,
  and the vault's Dataview tables are rendered to static Markdown.
- Withholds anything personal. Notes in ``EXCLUDED`` are never
  published, and every remaining note is checked against a privacy
  guard (contact details, plus an optional private term list kept
  *outside* this repo); a note that trips the guard is withheld too.
"""

import argparse
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "knowledge"

# Notes withheld from the public site because they are personal: they
# describe family, relationships, health specifics, or private history
# rather than the subject itself. Paths are relative to Knowledge/.
# A withheld folder note still gets a generated index page.
EXCLUDED = {
    "AI/AI Entities/AI Entities.md",
    "AI/AI Entities/Lilith.md",
    "AI/AI Entities/Lumina.md",
    "AI/AI and Shadow Work.md",
    "AI/Archetype Map.md",
    "AI/The Recursive Loop.md",
    "AI/Writing with AI.md",
    "Key Concepts/Holding Space.md",
    "Key Concepts/Key Concepts.md",
    "Key Concepts/Writing as a Vehicle for the Unconscious.md",
    "Neuroscience/Dopamine.md",
    "Neuroscience/GABA.md",
    "Neuroscience/Neurotransmitters.md",
    "Neuroscience/Serotonin.md",
    "Philosophy/Algorithm Eats/Algorithm Eats.md",
    "Philosophy/Philosophy.md",
    "Psychology/Conditions/Anxiety.md",
    "Psychology/Conditions/Bipolar Disorder.md",
    "Psychology/Conditions/Conditions.md",
    "Psychology/Conditions/DID and OSDD.md",
    "Psychology/Conditions/Depression.md",
    "Psychology/Conditions/Mania.md",
    "Psychology/Conditions/Narcissism.md",
    "Psychology/Conditions/PTSD.md",
    "Psychology/Conditions/Psychosis.md",
    "Psychology/Conditions/Schizoaffective Disorder.md",
    "Psychology/Freudian/Transference.md",
    "Psychology/Jungian/Inflation.md",
    "Psychology/Jungian/Projection.md",
    "Psychology/Plurality.md",
    "Psychology/Psychology.md",
    "Psychology/The Fundamental Elements of Love and Attraction.md",
    "Psychology/Trauma & Healing/Grounding.md",
    "Psychology/Trauma & Healing/Healing.md",
    "Psychology/Trauma & Healing/Integration.md",
    "Psychology/Trauma & Healing/Trauma.md",
    "Spirituality/Transformation.md",
    "Technology/Career Timeline.md",
    "Technology/Digital Legacy.md",
    "Technology/Open Source.md",
}

# Notes that trip the private-term guard only through scripture or
# myth (a namesake in Genesis or Tobit), reviewed by hand.
GUARD_ALLOW = {
    "Hebrew Letters/He.md",
    "Angels & Demons/Angels/Raphael.md",
    "Angels & Demons/Ars Goetia/Asmoday.md",
}

# Never publish from these vault areas, whatever links point there.
NEVER = ("System 777", "Transmissions")

# Built-in guard: contact details and credentials.
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


def load_guard():
    patterns = list(BUILTIN_GUARD)
    if PRIVATE_TERMS_FILE.exists():
        for line in PRIVATE_TERMS_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(r"\b" + re.escape(line) + r"\b")
    else:
        print(f"warning: no private term list at {PRIVATE_TERMS_FILE}", file=sys.stderr)
    return re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)


# --- Slugs -------------------------------------------------------------


def slugify(name):
    name = name.replace("♭", " flat").replace("♯", " sharp").replace("&", " and ")
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower().replace("'", "").replace("’", "")
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return name or "note"


def heading_anchor(text):
    """Mirror tuftecms' add_heading_anchor_ids()."""
    anchor = re.sub(r"[^\w\s-]", "", text.lower()).replace(" ", "-")
    return re.sub(r"-+", "-", anchor).strip("-")


# --- Vault model ---------------------------------------------------------


FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def split_frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[m.end():]


class Note:
    def __init__(self, vault_root, path):
        self.path = path
        self.rel = path.relative_to(vault_root).as_posix()  # relative to Knowledge/
        self.stem = path.stem
        self.text = path.read_text(encoding="utf-8")
        self.meta, self.body = split_frontmatter(self.text)
        parent = path.parent
        self.is_folder_note = parent != vault_root and parent.name == path.stem
        self.is_root = parent == vault_root and path.stem == "Knowledge"
        folder_parts = [slugify(p) for p in path.parent.relative_to(vault_root).parts]
        if self.is_root:
            self.out_rel = "index.md"
        elif self.is_folder_note:
            self.out_rel = "/".join(folder_parts + ["index.md"])
        else:
            self.out_rel = "/".join(folder_parts + [slugify(path.stem) + ".md"])
        out = self.out_rel[: -len(".md")]
        if out.endswith("index"):
            out = out[: -len("index")].rstrip("/")
        self.url = "/knowledge" + ("/" + out if out else "")


def without_fences(text):
    return re.sub(r"^(```|~~~).*?^\1", "", text, flags=re.DOTALL | re.MULTILINE)


def title_of(body, fallback):
    m = re.search(r"^# (.+?)\s*$", without_fences(body), re.MULTILINE)
    return m.group(1).strip() if m else fallback


def norm_title(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def site_title_map():
    """Exact page titles elsewhere on the site -> URL (for non-Knowledge links)."""
    titles = {}
    for md in sorted(DATA_DIR.rglob("*.md")):
        rel = md.relative_to(DATA_DIR)
        if rel.parts[0] == "knowledge":
            continue
        try:
            head = md.read_text(encoding="utf-8")[:2000]
        except (OSError, UnicodeDecodeError):
            continue
        m = re.search(r"^# (.+?)\s*$", head, re.MULTILINE)
        if not m:
            continue
        if md.name == "index.md":
            url = "/" + rel.parent.as_posix()
        else:
            url = "/" + rel.with_suffix("").as_posix()
        titles.setdefault(norm_title(m.group(1)), url)
    return titles


class Resolver:
    def __init__(self, published, withheld_names, site_titles):
        self.by_name = {}
        self.by_path = {}
        for note in published:
            self.by_name.setdefault(note.stem.lower(), []).append(note)
            self.by_path[note.rel[:-3].lower()] = note
            self.by_path["knowledge/" + note.rel[:-3].lower()] = note
        self.withheld = withheld_names
        self.site_titles = site_titles

    def resolve(self, target, source):
        """Return a URL for an Obsidian link target, or None."""
        target = target.strip().removesuffix(".md")
        key = target.lower()
        if any(key.startswith(n.lower()) for n in NEVER):
            return None
        if "/" in key:
            note = self.by_path.get(key)
            if note:
                return note.url
            key = key.rsplit("/", 1)[-1]
        if key in self.withheld:
            return None
        candidates = self.by_name.get(key)
        if candidates:
            if len(candidates) == 1:
                return candidates[0].url
            # Prefer the candidate closest to the linking note.
            src_dir = source.rel.rsplit("/", 1)[0] if "/" in source.rel else ""
            best = max(
                candidates,
                key=lambda n: (len(os.path.commonprefix([n.rel, src_dir])), -len(n.rel)),
            )
            return best.url
        return self.site_titles.get(norm_title(target.rsplit("/", 1)[-1]))


# --- Markdown conversion ------------------------------------------------------


WIKILINK = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
FENCE = re.compile(r"^(```|~~~)")


def convert_wikilinks(text, note, resolver):
    def repl(m):
        embed, inner = m.group(1), m.group(2)
        inner = inner.replace("\\|", "|")
        target, _, alias = inner.partition("|")
        target, _, heading = target.partition("#")
        heading = heading.split("^", 1)[0].strip()
        label = (alias or (heading if not target and heading else target.rsplit("/", 1)[-1])).strip()
        if not target:  # same-note heading link
            return f"[{label}](#{heading_anchor(heading)})" if heading else label
        url = resolver.resolve(target, note)
        if url is None:
            return "" if embed and re.search(r"\.(png|jpe?g|gif|webp|svg|pdf)$", target, re.I) else label
        if heading:
            url += "#" + heading_anchor(heading)
        if embed:
            return f"*See [{label}]({url}).*"
        return f"[{label}]({url})"

    return WIKILINK.sub(repl, text)


def inline_transform(line, note, resolver):
    # Leave `inline code` untouched.
    parts = re.split(r"(`[^`]*`)", line)
    for i, part in enumerate(parts):
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            continue
        part = convert_wikilinks(part, note, resolver)
        part = re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", part)
        parts[i] = part
    return "".join(parts)


def frontmatter_cell(value, note, resolver):
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(frontmatter_cell(v, note, resolver) for v in value)
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return inline_transform(text.replace("\\\\|", "\\|"), note, resolver)


DATAVIEW = re.compile(
    r'TABLE\s+WITHOUT\s+ID\s+(?P<cols>.+?)\s+FROM\s+"(?P<src>[^"]+)"'
    r'(?:\s+WHERE\s+(?P<wk>[\w.-]+)\s*=\s*"(?P<wv>[^"]+)")?'
    r'(?:\s+SORT\s+(?P<sk>[\w.-]+)(?:\s+(?P<sd>ASC|DESC))?)?\s*$',
    re.DOTALL | re.IGNORECASE,
)


def render_dataview(query, note, notes_by_rel, resolver):
    m = DATAVIEW.match(query.strip())
    if not m:
        return ""
    cols = []
    for col in re.split(r",\s*(?=[\w.-]+\s+AS\s+\")", m.group("cols")):
        cm = re.match(r'([\w.-]+)\s+AS\s+"([^"]+)"', col.strip())
        if cm:
            cols.append(cm.groups())
    src = m.group("src").removeprefix("Knowledge/").rstrip("/") + "/"
    rows = [
        n for rel, n in notes_by_rel.items()
        if rel.startswith(src) and "/" not in rel[len(src):] and not n.is_folder_note
        and (not m.group("wk") or str(n.meta.get(m.group("wk"))) == m.group("wv"))
    ]
    sk = m.group("sk")
    if sk:
        def sort_key(n):
            v = n.stem if sk == "file.name" else n.meta.get(sk)
            return (v is None, v if isinstance(v, (int, float)) else str(v or ""))
        try:
            rows.sort(key=sort_key, reverse=(m.group("sd") or "ASC").upper() == "DESC")
        except TypeError:
            rows.sort(key=lambda n: str(sort_key(n)))
    if not rows or not cols:
        return ""
    out = ["| " + " | ".join(h for _, h in cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for n in rows:
        cells = []
        for field, _ in cols:
            if field == "file.link":
                cells.append(f"[{n.stem}]({n.url})")
            elif field == "file.name":
                cells.append(n.stem)
            else:
                cells.append(frontmatter_cell(n.meta.get(field), note, resolver))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


CALLOUT = re.compile(r"^(>\s*)\[!(\w+)\][+-]?\s*(.*)$")


DROP_FENCES = ("dataviewjs", "base")


def convert_body(note, resolver, notes_by_rel):
    body = re.sub(r"%%.*?%%", "", note.body, flags=re.DOTALL)
    out = []
    fence = None  # (marker, lang, buffered lines)
    for line in body.split("\n"):
        if fence is not None:
            marker, lang, buf = fence
            if line.strip().startswith(marker):
                if lang == "dataview":
                    table = render_dataview("\n".join(buf[1:]), note, notes_by_rel, resolver)
                    if table:
                        out.append(table)
                elif lang not in DROP_FENCES:
                    out.extend(buf)
                    out.append(line)
                fence = None
            else:
                buf.append(line)
            continue
        fm = FENCE.match(line.strip())
        if fm:
            fence = (fm.group(1), line.strip()[3:].strip().lower(), [line])
            continue
        cm = CALLOUT.match(line)
        if cm:
            title = cm.group(3).strip() or cm.group(2).capitalize()
            out.append(f"{cm.group(1)}**{inline_transform(title, note, resolver)}**")
            out.append(cm.group(1).rstrip())
            continue
        out.append(inline_transform(line, note, resolver))
    if fence is not None and fence[1] not in DROP_FENCES + ("dataview",):
        out.extend(fence[2])  # unterminated fence: keep as written
    return "\n".join(out)


def build_page(note, resolver, notes_by_rel):
    body = convert_body(note, resolver, notes_by_rel).strip("\n")
    title = title_of(note.body, note.stem)
    if not re.search(r"^# .+$", without_fences(body), re.MULTILINE):
        body = f"# {title}\n\n{body}"
    meta = {}
    description = note.meta.get("description") or note.meta.get("essence")
    if not description:
        q = re.search(r"^>\s*\*(.+?)\*\s*$", note.body, re.MULTILINE)
        if q:
            description = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", q.group(1))
    if description:
        meta["description"] = str(description).strip().strip('"')
    aliases = note.meta.get("aliases") or note.meta.get("alias")
    if aliases:
        meta["aliases"] = [aliases] if isinstance(aliases, str) else [str(a) for a in aliases]
    meta["source"] = "obsidian-knowledge"
    front = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{front}\n---\n\n{body}\n"


def generated_index(folder_title):
    return (
        "---\nsource: obsidian-knowledge\n---\n\n"
        f"# {folder_title}\n\n"
        f"Notes on {folder_title}, part of the [Knowledge](/knowledge) collection.\n"
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", default=os.environ.get("OBSIDIAN_VAULT", str(Path.home() / "Notes")))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    knowledge = Path(args.vault).expanduser() / "Knowledge"
    if not knowledge.is_dir():
        sys.exit(f"no Knowledge folder at {knowledge}")

    guard = load_guard()
    published, withheld = [], []
    for path in sorted(knowledge.rglob("*.md")):
        rel = path.relative_to(knowledge).as_posix()
        if any(part.startswith(".") for part in path.relative_to(knowledge).parts):
            continue
        if any(n in rel for n in NEVER):
            withheld.append((rel, "protected vault area"))
            continue
        if rel in EXCLUDED:
            withheld.append((rel, "personal"))
            continue
        note = Note(knowledge, path)
        if rel not in GUARD_ALLOW and guard.search(note.text):
            withheld.append((rel, "privacy guard"))
            continue
        published.append(note)

    # Folders whose folder note is withheld still need an index page.
    withheld_names = {Path(r).stem.lower() for r, _ in withheld}
    published_names = {n.stem.lower() for n in published}
    withheld_names -= published_names
    resolver = Resolver(published, withheld_names, site_title_map())
    notes_by_rel = {n.rel: n for n in published}

    # Slug collision check.
    seen = {}
    for n in published:
        if n.out_rel in seen:
            sys.exit(f"slug collision: {n.rel} and {seen[n.out_rel]} -> {n.out_rel}")
        seen[n.out_rel] = n.rel

    pages = {n.out_rel: build_page(n, resolver, notes_by_rel) for n in published}
    for d in sorted({p.parent for p in knowledge.rglob("*.md")}):
        if d == knowledge:
            continue
        rel_parts = [slugify(p) for p in d.relative_to(knowledge).parts]
        index_rel = "/".join(rel_parts + ["index.md"])
        has_content = any(k.startswith("/".join(rel_parts) + "/") for k in pages)
        if index_rel not in pages and has_content:
            pages[index_rel] = generated_index(d.name)

    if args.dry_run:
        print(f"would publish {len(published)} notes as {len(pages)} pages")
    else:
        if OUT_DIR.exists():
            shutil.rmtree(OUT_DIR)
        for rel, text in sorted(pages.items()):
            dest = OUT_DIR / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
        print(f"published {len(published)} notes as {len(pages)} pages in {OUT_DIR.relative_to(ROOT)}")
    folders = len({p.rsplit('/', 1)[0] for p in pages if '/' in p}) + 1
    print(f"folders: {folders}; withheld: {len(withheld)}")
    for rel, reason in withheld:
        print(f"  withheld ({reason}): {rel}", file=sys.stderr)


if __name__ == "__main__":
    main()

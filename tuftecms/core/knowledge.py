"""The Knowledge section as a site-wide resource.

Builds a concept index from the published notes under ``data/knowledge``
(titles plus frontmatter aliases) and uses it three ways:

- ``link_html()`` auto-links the first mention of a concept on ordinary
  pages to its Knowledge note -- never inside headings, code, existing
  links, or sidenotes, and capped per page so prose stays prose.
- ``mentions`` records which site pages mention which concepts, so each
  Knowledge note can list where it turns up across the site.
- ``related`` holds the link graph between Knowledge notes in both
  directions.
"""

import html as html_lib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

KNOWLEDGE = "knowledge"
MAX_LINKS_PER_PAGE = 6
MIN_TERM_LENGTH = 4
# A concept whose lowercase spelling shows up this often in ordinary
# site prose is a common word ("love", "the moon"), not a reference.
GENERIC_THRESHOLD = 3
# Titles that name the collection rather than a concept.
SKIP_TITLES = {"knowledge", "index", "related", "overview"}
# Ambiguous on this site: everyday words, people's first names, software
# (Obsidian the app, not the stone), and names the site already uses for
# its own personalities. Matched case-insensitively.
AMBIGUOUS = {
    "obsidian", "michael", "daniel", "gabriel", "ariel", "raphael", "victoria",
    "diana", "phoebe", "sophia", "luna", "selene", "selah", "hecate", "charity",
    "chastity", "diligence", "fortitude", "vine", "swords", "wands", "pentacles",
    "cups", "cube", "torus", "flam", "sloth", "thrones", "dominions", "exiles",
    "firefighters", "backlash", "unburdening", "trailheads", "houses", "lesson 25",
    "judgement", "nike", "atlas", "pluto", "mercury", "luna", "full moon",
    "new moon", "the hero", "the maiden", "the devil", "the lovers", "the emperor",
    "the chariot", "the magician", "the hermit", "power chord", "cadences",
    "veritas", "fortuna", "janus", "terminus", "victoria",
}

# Sections that never gain concept links or count as mentions: personal
# documentation, where a name like "Hermes" means someone, not the god.
NO_LINK_SECTIONS = {"system-777"}

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1 = re.compile(r"^# (.+?)\s*$", re.MULTILINE)
KNOWLEDGE_LINK = re.compile(r"\]\((/knowledge(?:/[^)\s#]*)?)(?:#[^)\s]*)?\)")

# Tags whose text must never gain a concept link.
SKIP_TAGS = {
    "a", "h1", "h2", "h3", "h4", "h5", "h6", "code", "pre", "script",
    "style", "label", "button", "sup", "kbd", "samp", "textarea", "svg",
    "title", "figcaption", "select", "option",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "source", "track", "wbr",
}
SIDENOTE_CLASS = re.compile(r"""class\s*=\s*["'][^"']*\b(sidenote|marginnote)\b""")
TAG = re.compile(r"(<[^>]*>)")
TAG_NAME = re.compile(r"^</?\s*([a-zA-Z][a-zA-Z0-9]*)")


@dataclass
class Concept:
    term: str
    url: str
    title: str


@dataclass
class Page:
    url: str
    title: str
    date: str = ""


def _split_frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[m.end():]


def _url_for(md, data_dir):
    rel = md.relative_to(data_dir)
    if md.name == "index.md":
        return "/" + rel.parent.as_posix()
    return "/" + rel.with_suffix("").as_posix()


def clean_title(title):
    """Card numbering and disambiguators aren't part of the term."""
    title = re.split(r"\s+·\s+", title)[0]
    title = re.sub(r"\s*\([^)]*\)\s*$", "", title)
    return re.sub(r"[*_`]", "", title).strip()


def _without_fences(markdown):
    return re.sub(r"^(```|~~~).*?^\1", "", markdown, flags=re.DOTALL | re.MULTILINE)


def plain_text(markdown):
    """Readable prose from markdown: no code, URLs, tags, or frontmatter."""
    text = FRONTMATTER.sub("", markdown, count=1)
    text = re.sub(r"^(```|~~~).*?^\1", " ", text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"<span[^>]*class=\"(?:sidenote|marginnote)\"[^>]*>.*?</span>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return text


WORD = re.compile(r"[\w'’]+")
MAX_NGRAM = 5


def _lowercase_ngrams(texts):
    """Counts of all-lowercase word runs (up to MAX_NGRAM words) in prose."""
    counts = Counter()
    for text in texts:
        words = WORD.findall(text)
        for i, w in enumerate(words):
            if not w.islower():
                continue
            for n in range(1, MAX_NGRAM + 1):
                gram = words[i:i + n]
                if len(gram) < n or not gram[-1].islower():
                    break
                counts[tuple(gram)] += 1
    return counts


def links_allowed(url):
    """Whether a site page (by URL) takes concept crosslinks."""
    section = url.strip("/").split("/", 1)[0]
    return section not in NO_LINK_SECTIONS and section != KNOWLEDGE


class KnowledgeIndex:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.root = self.data_dir / KNOWLEDGE
        self.concepts = {}  # term -> Concept
        self.titles = {}  # knowledge url -> title
        self.related = defaultdict(list)  # knowledge url -> [urls], both directions
        self.mentions = defaultdict(list)  # knowledge url -> [Page]
        self.page_concepts = {}  # site url -> [knowledge urls], first-mention order
        self._pattern = None
        self._by_key = {}
        if self.root.is_dir():
            self._build()

    # --- building -----------------------------------------------------

    def _site_pages(self):
        for md in sorted(self.data_dir.rglob("*.md")):
            if md.relative_to(self.data_dir).parts[0] in {KNOWLEDGE} | NO_LINK_SECTIONS:
                continue
            try:
                yield md, md.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

    def _build(self):
        site = list(self._site_pages())
        corpus = _lowercase_ngrams(plain_text(text) for _, text in site)

        candidates = defaultdict(list)  # term -> [(priority, url, title)]
        outgoing = {}
        for md in sorted(self.root.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            meta, body = _split_frontmatter(text)
            url = _url_for(md, self.data_dir)
            m = H1.search(_without_fences(body))
            title = m.group(1).strip() if m else md.stem.replace("-", " ").title()
            self.titles[url] = title
            outgoing[url] = []
            for link in KNOWLEDGE_LINK.findall(body):
                link = link.rstrip("/")
                if link != url and link not in outgoing[url]:
                    outgoing[url].append(link)
            terms = [clean_title(title)]
            aliases = meta.get("aliases") or []
            terms += [str(a) for a in ([aliases] if isinstance(aliases, str) else aliases)]
            disambiguated = clean_title(title) != title.strip()
            for term in terms:
                term = term.strip()
                if self._usable(term, corpus):
                    candidates[term].append((disambiguated, len(url), url, title))

        for term, options in candidates.items():
            _, _, url, title = min(options)
            self.concepts[term] = Concept(term, url, title)

        incoming = defaultdict(list)
        for src, targets in outgoing.items():
            for dst in targets:
                if dst in self.titles:
                    incoming[dst].append(src)
        for url in self.titles:
            seen = []
            for other in outgoing.get(url, []) + incoming.get(url, []):
                if other in self.titles and other != url and other not in seen:
                    seen.append(other)
            self.related[url] = seen

        self._compile()

        for md, text in site:
            page_url = _url_for(md, self.data_dir)
            found = self.find(plain_text(text))
            if not found:
                continue
            self.page_concepts[page_url] = found
            m = H1.search(text)
            title = m.group(1).strip() if m else md.stem.replace("-", " ").title()
            date = re.match(r"(\d{4}-\d{2}(?:-\d{2})?)", md.stem)
            page = Page(page_url, title, date.group(1) if date else "")
            for url in found:
                self.mentions[url].append(page)
        for pages in self.mentions.values():
            pages.sort(key=lambda p: (p.date, p.title), reverse=True)

    @staticmethod
    def _usable(term, corpus):
        if len(term) < MIN_TERM_LENGTH or term.lower() in SKIP_TITLES | AMBIGUOUS:
            return False
        if not re.search(r"[A-Za-z]", term) or term.isupper() and len(term) < 5:
            return False
        # Concepts are matched as capitalised; if the lowercase spelling
        # is everyday prose on the site, the term is too generic to link.
        lowered = term.lower()
        if lowered != term:
            key = tuple(WORD.findall(lowered))
            if corpus.get(key, 0) >= GENERIC_THRESHOLD:
                return False
        return True

    def _compile(self):
        if not self.concepts:
            self._pattern = None
            return
        variants = {}
        for term, concept in self.concepts.items():
            for v in {term, html_lib.escape(term, quote=False), term.replace("'", "’")}:
                variants[v] = concept
        self._by_key = variants
        alternation = "|".join(re.escape(v) for v in sorted(variants, key=len, reverse=True))
        self._pattern = re.compile(r"(?<![\w/#-])(" + alternation + r")(?![\w-])")

    # --- querying -----------------------------------------------------

    def find(self, text):
        """Knowledge URLs mentioned in plain text, in first-mention order."""
        if not self._pattern:
            return []
        seen = []
        for m in self._pattern.finditer(text):
            url = self._by_key[m.group(1)].url
            if url not in seen:
                seen.append(url)
        return seen

    def link_html(self, html, page_url=None, max_links=MAX_LINKS_PER_PAGE):
        """Link the first mention of each concept in rendered HTML.

        Returns ``(html, linked_urls)``.
        """
        if not self._pattern or not html or max_links <= 0:
            return html, []
        linked = []
        stack = []  # (tag name, skip?)
        out = []
        for token in TAG.split(html):
            if not token:
                continue
            if token.startswith("<"):
                out.append(token)
                m = TAG_NAME.match(token)
                if not m or token.startswith("<!") or token.startswith("<?"):
                    continue
                name = m.group(1).lower()
                if token.startswith("</"):
                    for i in range(len(stack) - 1, -1, -1):
                        if stack[i][0] == name:
                            del stack[i:]
                            break
                elif name not in VOID_TAGS and not token.rstrip().endswith("/>"):
                    skip = name in SKIP_TAGS or bool(SIDENOTE_CLASS.search(token))
                    stack.append((name, skip))
                continue
            if len(linked) >= max_links or any(skip for _, skip in stack):
                out.append(token)
                continue

            def repl(m):
                concept = self._by_key[m.group(1)]
                if (
                    len(linked) >= max_links
                    or concept.url in linked
                    or concept.url == page_url
                ):
                    return m.group(0)
                linked.append(concept.url)
                title = html_lib.escape(concept.title, quote=True)
                return (
                    f'<a href="{concept.url}" class="concept-link" '
                    f'title="Knowledge: {title}">{m.group(0)}</a>'
                )

            out.append(self._pattern.sub(repl, token))
        return "".join(out), linked

    def related_for(self, url, limit=12):
        return [
            {"url": u, "title": self.titles[u]} for u in self.related.get(url, [])[:limit]
        ]

    def mentions_for(self, url, limit=15):
        return [
            {"url": p.url, "title": p.title, "date": p.date}
            for p in self.mentions.get(url, [])[:limit]
        ]

    def concepts_for(self, page_url, limit=6):
        return [
            {"url": u, "title": self.titles[u]}
            for u in self.page_concepts.get(page_url, [])[:limit]
            if u in self.titles
        ]

    def stats(self):
        return {
            "concepts": len(self.concepts),
            "notes": len(self.titles),
            "pages_mentioning": len(self.page_concepts),
        }

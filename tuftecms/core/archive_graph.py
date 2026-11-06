"""Cross-reference data for ``/archive/graph``.

Reads every markdown page under ``data/`` except the folders and root
pages named in ``EXCLUDED``. The archive view uses the link and
correspondence edges. Those edges come from what the notes already record:

- markdown cross-links
- frontmatter ``themes``, ``tags``, and ``series``
- correspondence tables (a card's Hebrew letter, a sphere's planet,
  an element's suit, and the rows of the table of correspondences)

Nothing in the graph is hand-listed. A new page appears because the
page exists. ``EXCLUDED`` is the one list to edit when a private
section should join the map, or leave it.
"""

from collections import defaultdict
import re

from tuftecms.core.knowledge import (
    H1,
    _split_frontmatter,
    _url_for,
    _without_fences,
    clean_title,
)

# Private shelves. Drop a name to let that folder or root page in.
EXCLUDED = (
    "system-777",
    "family",
    "mental-health",
    "contact",
)

SECTION_TITLES = {
    "knowledge": "Knowledge",
    "themes": "Themes",
    "essays": "Essays",
    "poetry": "Poetry",
    "software": "Software",
    "music": "Music",
    "artificial-intelligence": "Artificial Intelligence",
    "talks": "Talks",
    "photography": "Photography",
    "pages": "Pages",
}

SECTION_ORDER = (
    "knowledge",
    "themes",
    "essays",
    "poetry",
    "software",
    "music",
    "artificial-intelligence",
    "talks",
    "photography",
    "pages",
)

CORRESPONDENCE_PAGE = "/knowledge/table-of-correspondences"

_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\((/[^)\s#]*)")
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
_DATE_LINE = re.compile(
    r"^\*?(?:[A-Za-z]+ \d{4}|\d{4})\*?$"
)
_ALIAS_STOP = {
    "index", "overview", "related", "knowledge", "notes", "the", "and",
    "page", "pages",
}


def build_graph(data_dir, excluded=EXCLUDED):
    """Return ``{excluded, sections, domains, nodes, edges}`` for ``data_dir``."""
    excluded = tuple(str(name).strip().lower() for name in excluded)
    pages = _load_pages(data_dir, excluded)
    by_url = {page["url"]: page for page in pages}
    _assign_structure(pages, by_url)

    edges = {}

    def add(src, dst, kind, label=None):
        if not src or not dst or src == dst:
            return
        if src not in by_url or dst not in by_url:
            return
        if kind == "link" and _containment(src, dst, by_url):
            return
        rec = edges.get((src, dst))
        if rec is None:
            rec = {"source": src, "target": dst, "kinds": [], "labels": []}
            edges[(src, dst)] = rec
        if kind not in rec["kinds"]:
            rec["kinds"].append(kind)
        if label and label not in rec["labels"] and len(rec["labels"]) < 6:
            rec["labels"].append(label)

    link_text = defaultdict(set)
    for page in pages:
        # Full body, tables included, so a column that writes "Beth" teaches
        # that spelling to the letter it links. Link edges use link_body,
        # which drops the correspondence grid so that page does not become a star.
        for text, raw in _LINK.findall(page["body"]):
            url = _norm_url(raw)
            if url in by_url and text.strip():
                link_text[url].add(text.strip())
        for text, raw in _LINK.findall(page["link_body"]):
            url = _norm_url(raw)
            if url in by_url:
                add(page["url"], url, "link", _short(text) or None)

    _add_frontmatter_edges(pages, by_url, add)
    _add_series_edges(pages, add)
    _add_correspondences(pages, by_url, link_text, add)

    nodes = [_public_node(page) for page in pages]
    nodes.sort(key=lambda n: n["url"])
    edge_list = list(edges.values())
    edge_list.sort(key=lambda e: (e["source"], e["target"]))

    return {
        "excluded": list(excluded),
        "sections": _sections(nodes),
        "domains": _domains(nodes),
        "nodes": nodes,
        "edges": edge_list,
    }


def to_archive_graph(graph):
    """The cross-reference graph: essays and knowledge notes, plus what they cite.

    Same shape ``/archive/graph`` already consumes (id, title, url, category).
    """
    by_url = {node["url"]: node for node in graph["nodes"]}
    nodes = {}
    seen = set()
    edges = []

    def add_node(url):
        node = by_url.get(url)
        if node is None:
            return None
        nid = url.strip("/")
        if nid not in nodes:
            section = node["section"]
            category = "pages" if section == "pages" else section
            nodes[nid] = {
                "id": nid,
                "title": node["title"],
                "label": node["title"],
                "url": url,
                "category": category,
                "group": category,
            }
        return nid

    for edge in graph["edges"]:
        kinds = set(edge["kinds"])
        if not kinds & {"link", "correspondence"}:
            continue
        src = edge["source"]
        dst = edge["target"]
        source = by_url.get(src)
        if source is None or source["section"] not in {"essays", "knowledge"}:
            continue
        if dst not in by_url:
            continue
        sid = add_node(src)
        tid = add_node(dst)
        if not sid or not tid or sid == tid or (sid, tid) in seen:
            continue
        seen.add((sid, tid))
        label = edge["labels"][0] if edge["labels"] else by_url[dst]["title"]
        edges.append({
            "source": sid,
            "target": tid,
            "label": label,
            "link_text": label,
        })

    return {"nodes": list(nodes.values()), "edges": edges}


# --- loading ----------------------------------------------------------


def _load_pages(data_dir, excluded):
    pages = []
    root = data_dir
    if not root.is_dir():
        return pages
    for md in sorted(root.rglob("*.md")):
        if not md.is_file():
            continue
        rel = md.relative_to(root)
        if _excluded_path(rel, excluded):
            continue
        try:
            raw = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        meta, body = _split_frontmatter(raw)
        if not isinstance(meta, dict):
            meta = {}
        plain = _without_fences(body)
        url = _norm_url(_url_for(md, root))
        title = _title(plain, md)
        summary = _summary(meta, plain)
        pages.append({
            "url": url,
            "root_file": len(rel.parts) == 1,
            "title": title,
            "summary": summary,
            "body": plain,
            "link_body": plain,
            "meta": meta,
            "tags": _as_list(meta.get("tags")),
            "themes": _as_list(meta.get("themes")),
            "aliases": _as_list(meta.get("aliases")),
            "series": meta.get("series").strip() if isinstance(meta.get("series"), str) else "",
        })
    return pages


def _excluded_path(rel, excluded):
    parts = rel.parts
    if not parts:
        return True
    first = parts[0]
    if first.endswith(".md"):
        first = first[:-3]
    if first.lower() in excluded:
        return True
    if len(parts) == 1 and rel.stem.lower() in excluded:
        return True
    return False


def _title(body, md):
    match = H1.search(body)
    raw = match.group(1).strip() if match else md.stem.replace("-", " ").replace("_", " ")
    title = clean_title(raw) or raw.strip()
    return title or md.stem


def _summary(meta, body):
    desc = meta.get("description") or meta.get("summary") or ""
    if not isinstance(desc, str) or not desc.strip():
        desc = _first_paragraph(body)
    return _plain_snippet(desc)


def _first_paragraph(body):
    lines = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            if lines:
                break
            continue
        if line.startswith(("#", ">", "|", "<", "```", "~~~")) or line in {"---", "***"}:
            if lines:
                break
            continue
        if _DATE_LINE.match(line):
            continue
        lines.append(line)
    return " ".join(lines)


def _plain_snippet(text, limit=240):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def _as_list(value):
    if value is None or value is False:
        return []
    if isinstance(value, str):
        parts = re.split(r"\s*,\s*", value)
    elif isinstance(value, (list, tuple)):
        parts = [str(item) for item in value]
    else:
        parts = [str(value)]
    return [part.strip() for part in parts if part and str(part).strip()]


def _norm_url(url):
    url = (url or "").split("?")[0].split("#")[0].rstrip("/")
    return url or "/"


def _norm_name(text):
    text = re.sub(r"[*_`]", "", text or "")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def _slugify(text):
    text = _norm_name(text).replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def _short(text, limit=80):
    text = re.sub(r"\s+", " ", re.sub(r"[*_`]", "", text or "")).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


# --- structure --------------------------------------------------------


def _assign_structure(pages, by_url):
    parents = set()
    for url in by_url:
        parts = [part for part in url.strip("/").split("/") if part]
        for i in range(1, len(parts)):
            parents.add("/" + "/".join(parts[:i]))

    for page in pages:
        parts = [part for part in page["url"].strip("/").split("/") if part]
        section = "pages" if page["root_file"] else parts[0]
        if section == "knowledge":
            domain = parts[1] if len(parts) > 1 else "knowledge"
        elif len(parts) >= 3:
            domain = parts[1]
        else:
            domain = section

        if section == "knowledge" and len(parts) == 1:
            kind = "section"
        elif section == "knowledge" and len(parts) == 2:
            kind = "domain"
        elif section == "themes" and len(parts) == 2:
            kind = "theme"
        elif section not in {"pages", "knowledge"} and len(parts) == 1:
            kind = "section"
        else:
            kind = "page"

        if section == "knowledge":
            hub = "" if len(parts) == 1 else "/knowledge/" + parts[1]
        elif section == "themes":
            hub = "" if len(parts) == 1 else page["url"]
        elif section == "pages":
            hub = page["url"]
        else:
            hub = "/" + section

        page["section"] = section
        page["domain"] = domain
        page["kind"] = kind
        page["hub"] = hub
        # Root pages (worldview, values, and the like) stay searchable
        # and show up under Pages. The opening picture is domains, themes,
        # and one point for each other shelf.
        page["overview"] = bool(hub) and page["url"] == hub and section != "pages"
        page["has_children"] = page["url"] in parents

        if page["url"] == CORRESPONDENCE_PAGE:
            page["link_body"] = _without_table_lines(page["body"])


def _without_table_lines(text):
    kept = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("|"):
            continue
        kept.append(line)
    return "".join(kept)


def _containment(src, dst, by_url):
    for parent, child in ((src, dst), (dst, src)):
        node = by_url.get(parent)
        if node is None or node["kind"] not in {"domain", "section"}:
            continue
        if child.startswith(parent.rstrip("/") + "/"):
            return True
    return False


def _public_node(page):
    tags = []
    for value in page["tags"] + page["aliases"]:
        if value not in tags:
            tags.append(value)
    return {
        "id": page["url"],
        "title": page["title"],
        "url": page["url"],
        "section": page["section"],
        "domain": page["domain"],
        "kind": page["kind"],
        "hub": page["hub"],
        "overview": page["overview"],
        "summary": page["summary"],
        "tags": tags,
    }


def _sections(nodes):
    counts = defaultdict(int)
    for node in nodes:
        counts[node["section"]] += 1
    ordered = []
    seen = set()
    for sid in SECTION_ORDER:
        if counts[sid]:
            ordered.append({
                "id": sid,
                "title": SECTION_TITLES.get(sid, sid.replace("-", " ").title()),
                "count": counts[sid],
            })
            seen.add(sid)
    for sid in sorted(counts):
        if sid not in seen:
            ordered.append({
                "id": sid,
                "title": sid.replace("-", " ").title(),
                "count": counts[sid],
            })
    return ordered


def _domains(nodes):
    grouped = defaultdict(list)
    hubs = {}
    for node in nodes:
        if node["section"] != "knowledge" or not node["hub"]:
            continue
        grouped[node["hub"]].append(node)
        if node["url"] == node["hub"]:
            hubs[node["hub"]] = node
    domains = []
    for hub, members in grouped.items():
        node = hubs.get(hub)
        if node is None or node["kind"] != "domain":
            continue
        domains.append({
            "id": node["domain"],
            "title": node["title"],
            "url": hub,
            "count": len(members),
        })
    domains.sort(key=lambda d: d["title"].lower())
    return domains


# --- frontmatter ------------------------------------------------------


def _add_frontmatter_edges(pages, by_url, add):
    by_slug, by_title = _name_indexes(pages)
    for page in pages:
        for value in page["themes"]:
            target = _resolve_ref(value, by_url, by_slug, by_title, prefer_themes=True)
            add(page["url"], target, "theme", "Theme")
        for value in page["tags"]:
            target = _resolve_ref(value, by_url, by_slug, by_title, prefer_themes=False)
            add(page["url"], target, "tag", "Tag")


def _name_indexes(pages):
    slug_owner = {}
    slug_ambiguous = set()
    title_owner = {}
    title_ambiguous = set()
    for page in pages:
        slug = page["url"].rstrip("/").split("/")[-1].lower()
        if slug and slug != "index":
            if slug in slug_owner and slug_owner[slug] != page["url"]:
                slug_ambiguous.add(slug)
            else:
                slug_owner[slug] = page["url"]
        title = _norm_name(page["title"])
        if len(title) >= 3:
            if title in title_owner and title_owner[title] != page["url"]:
                title_ambiguous.add(title)
            else:
                title_owner[title] = page["url"]
    for slug in slug_ambiguous:
        slug_owner.pop(slug, None)
    for title in title_ambiguous:
        title_owner.pop(title, None)
    return slug_owner, title_owner


def _resolve_ref(value, by_url, by_slug, by_title, prefer_themes):
    value = (value or "").strip()
    if not value:
        return None
    if value.startswith("/"):
        url = _norm_url(value)
        return url if url in by_url else None
    slug = _slugify(value)
    if prefer_themes and slug:
        themed = "/themes/" + slug
        if themed in by_url:
            return themed
    title = _norm_name(value)
    if title in by_title:
        return by_title[title]
    if slug and slug in by_slug:
        return by_slug[slug]
    if slug:
        themed = "/themes/" + slug
        if themed in by_url:
            return themed
    return None


def _add_series_edges(pages, add):
    groups = defaultdict(list)
    for page in pages:
        if page["series"]:
            groups[page["series"]].append(page["url"])
    for members in groups.values():
        if not 2 <= len(members) <= 12:
            continue
        ordered = sorted(members)
        for left, right in zip(ordered, ordered[1:]):
            add(left, right, "series", "Series")


# --- correspondences --------------------------------------------------


_SCOPE_RULES = (
    ("hebrew", lambda node: node["domain"] == "hebrew-letters" and node["kind"] != "domain"),
    ("tarot", lambda node: node["section"] == "knowledge" and node["domain"] == "tarot" and node["kind"] != "domain"),
    ("sephirah", lambda node: node["domain"] == "tree-of-life" and node["kind"] != "domain"),
    ("planet", lambda node: "/astrology/planets/" in node["url"] and node["kind"] != "domain"),
    ("element", lambda node: node["domain"] == "elements" and node["kind"] != "domain"),
    ("sign", lambda node: "/astrology/signs/" in node["url"] and node["kind"] != "domain"),
    ("chakra", lambda node: node["domain"] == "chakras" and node["kind"] != "domain"),
)


def _attribute_scope(label):
    text = _norm_name(label)
    if "hebrew" in text:
        return "hebrew"
    if "tarot" in text or "trump" in text or "arcana" in text:
        return "tarot"
    if "sephir" in text or "tree of life" in text:
        return "sephirah"
    if "planet" in text:
        return "planet"
    if "element" in text:
        return "element"
    if "sign" in text or "zodiac" in text or "triplicity" in text:
        return "sign"
    if "chakra" in text:
        return "chakra"
    return None


def _add_correspondences(pages, by_url, link_text, add):
    scopes = _scope_matchers(pages, link_text)
    for page in pages:
        if page["url"] == CORRESPONDENCE_PAGE:
            regions = [(page["body"], "cross")]
        else:
            regions = [(_slice, "local") for _slice in _correspondence_slices(page["body"])]
        for text, mode in regions:
            for table in _parse_tables(text):
                _edges_from_table(page, table, mode, by_url, scopes, add)


def _scope_matchers(pages, link_text):
    matchers = {}
    for name, pred in _SCOPE_RULES:
        owners = {}
        ambiguous = set()

        def claim(alias, url, owners=owners, ambiguous=ambiguous):
            alias = _norm_name(alias)
            if len(alias) < 3 or alias in _ALIAS_STOP or not re.search(r"[a-z]", alias):
                return
            if alias in owners and owners[alias] != url:
                ambiguous.add(alias)
            else:
                owners[alias] = url

        for page in pages:
            if not pred(page):
                continue
            claim(page["title"], page["url"])
            bare = re.sub(r"^the\s+", "", _norm_name(page["title"]))
            if bare != _norm_name(page["title"]):
                claim(bare, page["url"])
            for text in link_text.get(page["url"], ()):
                for alias in _alias_candidates(text):
                    claim(alias, page["url"])
        for alias in ambiguous:
            owners.pop(alias, None)
        if not owners:
            matchers[name] = None
            continue
        ordered = sorted(owners, key=len, reverse=True)
        pattern = re.compile(
            r"(?<![A-Za-z0-9])(" + "|".join(re.escape(alias) for alias in ordered) + r")(?![A-Za-z0-9])",
            re.IGNORECASE,
        )
        matchers[name] = (pattern, owners)
    return matchers


def _alias_candidates(text):
    text = re.sub(r"\s+", " ", re.sub(r"[*_`]", "", text or "")).strip()
    if not text or len(text) > 48 or text.count(" ") > 5:
        return []
    found = [text]
    stripped = re.sub(r"\s*\([^)]*\)\s*", " ", text).strip()
    if stripped and stripped.lower() != text.lower():
        found.append(stripped)
    return found


def _correspondence_slices(body):
    marks = list(_HEADING.finditer(body))
    slices = []
    for index, mark in enumerate(marks):
        title = mark.group(2).strip().lower()
        if "correspond" not in title:
            continue
        level = len(mark.group(1))
        end = len(body)
        for nxt in marks[index + 1:]:
            if len(nxt.group(1)) <= level:
                end = nxt.start()
                break
        slices.append(body[mark.end():end])
    return slices


def _parse_tables(text):
    lines = text.splitlines()
    tables = []
    index = 0
    while index < len(lines):
        if lines[index].lstrip().startswith("|"):
            block = []
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                block.append(lines[index])
                index += 1
            rows = []
            for raw in block:
                cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
                if _is_separator(cells):
                    continue
                rows.append(cells)
            if len(rows) >= 2:
                tables.append(rows)
        else:
            index += 1
    return tables


def _is_separator(cells):
    if not cells:
        return False
    marks = 0
    for cell in cells:
        compact = cell.replace(" ", "")
        if not compact:
            continue
        if re.fullmatch(r":?-{2,}:?", compact):
            marks += 1
        else:
            return False
    return marks > 0


def _edges_from_table(page, table, mode, by_url, scopes, add):
    header = table[0]
    local = mode == "local" and (
        _norm_name(header[0] if header else "") == "attribute" or len(header) <= 2
    )
    for row in table[1:]:
        if local:
            label = _short(row[0]) if row else ""
            value = row[1] if len(row) > 1 else ""
            scope = _attribute_scope(label)
            for target in _refs_in_cell(value, scope, by_url, scopes):
                add(page["url"], target, "correspondence", label or "Correspondence")
            continue
        subject = None
        cells = []
        for col, cell in enumerate(row):
            urls = _explicit_urls(cell, by_url)
            header_label = header[col] if col < len(header) else ""
            cells.append((header_label, cell, urls))
            if subject is None and urls:
                subject = urls[0]
        if subject is None:
            continue
        for header_label, cell, urls in cells:
            label = _short(header_label) or "Correspondence"
            scope = _attribute_scope(header_label)
            targets = [url for url in urls if url != subject]
            targets.extend(
                url for url in _named_urls(cell, scope, scopes) if url != subject and url not in targets
            )
            for target in targets:
                add(subject, target, "correspondence", label)


def _refs_in_cell(cell, scope, by_url, scopes):
    found = []
    for url in _explicit_urls(cell, by_url):
        if url not in found:
            found.append(url)
    for url in _named_urls(cell, scope, scopes):
        if url not in found:
            found.append(url)
    return found


def _explicit_urls(cell, by_url):
    found = []
    for _text, raw in _LINK.findall(cell or ""):
        url = _norm_url(raw)
        if url in by_url and url not in found:
            found.append(url)
    return found


def _named_urls(cell, scope, scopes):
    if not scope or not cell:
        return []
    matcher = scopes.get(scope)
    if not matcher:
        return []
    pattern, owners = matcher
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)
    found = []
    for match in pattern.finditer(text):
        url = owners.get(match.group(1).lower())
        if url and url not in found:
            found.append(url)
    return found

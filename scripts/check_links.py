"""Internal link checker for the digital garden.

Mirrors the routing logic in engine.py exactly, so it can tell the
difference between three very different fates for a link:

  OK        -- resolves directly (markdown file, directory, raw file,
               or a real dynamic route)
  REDIRECT  -- 404s as written but the legacy resolver rescues it with
               a 301 (works for readers, costs them a round-trip)
  BROKEN    -- a genuine 404; the link rot we actually care about

Usage:
    uv run python scripts/check_links.py            # report broken links
    uv run python scripts/check_links.py --redirects  # also show redirects
    uv run python scripts/check_links.py --quiet      # exit code only

Exit code is 1 if any BROKEN links exist, so this can run in CI.
"""

import re
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
STATIC_DIR = ROOT / "tuftecms" / "static"

# Dynamic routes served by engine.py that have no markdown behind them.
DYNAMIC_EXACT = {
    "/", "/health", "/random", "/search", "/robots.txt", "/sitemap",
    "/sitemap.xml", "/feed.xml", "/rss.xml", "/archive", "/directory",
    "/api",
}
DYNAMIC_PREFIXES = ("/archive/", "/api/", "/og-image/")

LINK_RE = re.compile(
    r"""\[[^\]]*\]\(([^)\s]+)\)      # markdown links
        |href="([^"]+)"               # html links (sidenotes etc.)
        |src="([^"]+)"                # html images
    """,
    re.X,
)
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def _build_legacy_index():
    """Same tables engine.py builds for legacy URL resolution."""
    legacy_dirs, legacy_files = {}, {}
    for match in DATA_DIR.rglob("*/"):
        if (match / "index.md").exists():
            rel = match.relative_to(DATA_DIR)
            legacy_dirs[match.name] = f"/{rel}"
    for match in DATA_DIR.rglob("*.md"):
        if match.name == "index.md":
            continue
        stem = match.stem
        stripped = re.sub(r"^\d{4}-\d{2}-", "", stem)
        rel = match.relative_to(DATA_DIR)
        url = f"/{rel.with_suffix('')}"
        legacy_files[stripped] = url
        legacy_files[stem] = url
    return legacy_dirs, legacy_files


LEGACY_DIRS, LEGACY_FILES = _build_legacy_index()


def resolve_legacy(path):
    """Mirror of engine.py:_resolve_legacy_url."""
    m = re.match(r"essays/(\d{4})/(\d{2})(?:/\d{2})?/(.+)$", path)
    if m:
        year, month, slug = m.groups()
        normalized = slug.replace("-", "_")
        candidate = DATA_DIR / "essays" / f"{year}-{month}-{normalized}.md"
        if candidate.exists():
            return f"/essays/{year}-{month}-{normalized}"
        for f in (DATA_DIR / "essays").glob(f"{year}-{month}-*"):
            if normalized in f.stem:
                return f"/essays/{f.stem}"
    slug = path.strip("/").split("/")[-1]
    normalized = slug.replace("-", "_")
    if slug in LEGACY_DIRS:
        return LEGACY_DIRS[slug]
    if normalized in LEGACY_DIRS:
        return LEGACY_DIRS[normalized]
    if normalized in LEGACY_FILES:
        return LEGACY_FILES[normalized]
    if slug in LEGACY_FILES:
        return LEGACY_FILES[slug]
    return None


def classify(url):
    """Return (status, detail) for an internal URL, mirroring catch_all."""
    url = url.split("#")[0].split("?")[0]
    if not url:
        return "OK", "anchor"
    path = urllib.parse.unquote(url).strip("/")

    if url in DYNAMIC_EXACT or any(("/" + path + "/").startswith(p) or url.startswith(p)
                                   for p in DYNAMIC_PREFIXES):
        return "OK", "dynamic route"
    if url.startswith("/static/"):
        target = STATIC_DIR / path[len("static/"):]
        return ("OK", "static") if target.is_file() else ("BROKEN", "missing static file")
    if url.startswith("/data/"):
        target = DATA_DIR / path[len("data/"):]
        return ("OK", "data file") if target.is_file() else ("BROKEN", "missing data file")

    if path.endswith(".pdf"):
        md = DATA_DIR / (path[:-4] + ".md")
        return ("OK", "pdf") if md.exists() else ("BROKEN", "missing pdf source")
    if path.endswith(".md"):
        return ("OK", "raw md") if (DATA_DIR / path).exists() else ("BROKEN", "missing raw md")

    if (DATA_DIR / f"{path}.md").exists():
        return "OK", "markdown"
    if (DATA_DIR / path).is_dir():
        return "OK", "directory"
    if (DATA_DIR / path).is_file():
        return "OK", "raw file"

    redirect = resolve_legacy(path)
    if redirect:
        return "REDIRECT", redirect
    return "BROKEN", "404"


def iter_links():
    for md in sorted(DATA_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        # strip fenced code blocks -- example links in code aren't content
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for m in LINK_RE.finditer(text):
            url = next(g for g in m.groups() if g)
            if url.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            if not url.startswith("/"):
                continue  # relative links are rare and resolved per-page
            line = text[: m.start()].count("\n") + 1
            yield md.relative_to(ROOT), line, url


def main():
    show_redirects = "--redirects" in sys.argv
    quiet = "--quiet" in sys.argv
    broken = defaultdict(list)
    redirects = defaultdict(list)
    total = 0
    for src, line, url in iter_links():
        total += 1
        status, detail = classify(url)
        if status == "BROKEN":
            broken[str(src)].append((line, url))
        elif status == "REDIRECT":
            redirects[str(src)].append((line, url, detail))

    n_broken = sum(len(v) for v in broken.values())
    n_redir = sum(len(v) for v in redirects.values())
    if not quiet:
        for src in sorted(broken):
            for line, url in broken[src]:
                print(f"BROKEN    {src}:{line}  {url}")
        if show_redirects:
            for src in sorted(redirects):
                for line, url, to in redirects[src]:
                    print(f"REDIRECT  {src}:{line}  {url}  ->  {to}")
        print(f"\n{total} internal links checked: "
              f"{n_broken} broken, {n_redir} via legacy redirect.")
    sys.exit(1 if n_broken else 0)


if __name__ == "__main__":
    main()

"""Responder-based engine for kennethreitz.org."""

import responder
from responder import Query  # responder.Path is referenced fully to avoid clashing with pathlib.Path
from responder.ext.pagination import Page, paginate  # v6.2: Page[T] envelope + slicing
from responder.ext.query import filter_items, sort_items  # v6.3: equality filter + sort spec

from pydantic import BaseModel

from tuftecms.core.markdown import render_markdown_file
from tuftecms.core.cache import (
    get_blog_cache,
    clear_all_caches,
    get_sidenotes_cache,
    get_outlines_cache,
    get_quotes_cache,
    get_connections_cache,
    get_terms_cache,
    get_themes_cache,
)
from tuftecms.utils.content import (
    get_directory_structure,
    extract_intelligent_date,
    generate_folder_icon,
    get_cached_markdown_title,
)
from tuftecms.utils.svg_icons import generate_unique_svg_icon
from tuftecms.blueprints.content import extract_exif_data

from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from collections import defaultdict
import asyncio
import difflib
import hashlib
import html
import io
import logging
import random
import re
import shutil
import textwrap
import threading
import os

DATA_DIR = Path("data")

# --- Search index (built once at startup) ---
_search_index = []
_search_index_lock = threading.Lock()


def _ensure_search_index():
    """Build the search index on first use if warming hasn't gotten to it yet."""
    if not _search_index:
        with _search_index_lock:
            if not _search_index:
                _build_search_index()


def _build_search_index():
    """Scan all markdown files once and build a cached search index."""
    global _search_index
    index = []

    for md_file in DATA_DIR.rglob("*.md"):
        if md_file.name == "index.md":
            url = "/" + str(md_file.parent.relative_to(DATA_DIR))
        else:
            url = "/" + str(md_file.relative_to(DATA_DIR).with_suffix(""))

        try:
            raw = md_file.read_text()
        except (OSError, UnicodeDecodeError):
            continue

        # Extract title from first heading
        title = md_file.stem.replace("-", " ").replace("_", " ").title()
        for line in raw.split("\n"):
            line_stripped = line.strip()
            if line_stripped.startswith("# "):
                title = line_stripped[2:].strip()
                break

        # Determine section from path
        parts = md_file.relative_to(DATA_DIR).parts
        section = parts[0] if len(parts) > 1 else ""

        # Generate icon
        if md_file.name == "index.md":
            icon = generate_folder_icon(title, size=18)
        else:
            icon = generate_unique_svg_icon(title, size=18)

        index.append({
            "title": title,
            "url": url,
            "raw_text": raw.lower(),
            "raw": raw,
            "section": section,
            "icon": icon,
        })

    _search_index = index


def _suggest_pages(path, limit=3):
    """Closest-matching pages for a 404, by slug similarity."""
    want = path.rstrip("/").split("/")[-1].lower().replace("_", "-").replace("-", " ")
    if not want or not _search_index:
        return []

    scored = []
    for entry in _search_index:
        slug = entry["url"].rstrip("/").split("/")[-1].lower()
        slug = slug.replace("_", "-").replace("-", " ")
        score = difflib.SequenceMatcher(None, want, slug).ratio()
        if len(want) >= 4 and (want in slug or slug in want):
            score = max(score, 0.85)
        if score >= 0.6:
            scored.append((score, entry))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    suggestions, seen_titles = [], set()
    for _, e in scored:
        if e["title"] in seen_titles:
            continue
        seen_titles.add(e["title"])
        suggestions.append({"title": e["title"], "url": e["url"], "icon": e.get("icon")})
        if len(suggestions) >= limit:
            break
    return suggestions


@asynccontextmanager
async def _lifespan(app):
    """Warm caches in a background thread so the first requests aren't slow."""

    def _warm():
        app.log.info("Starting background cache warming...")
        try:
            get_blog_cache()
            get_sidenotes_cache()
            get_outlines_cache()
            get_quotes_cache()
            get_connections_cache()
            get_terms_cache()
            get_themes_cache()
            _build_search_index()
            app.log.info("Cache warming complete!")
        except Exception as e:
            app.log.error("Cache warming failed: %s", e)

    threading.Thread(target=_warm, daemon=True).start()
    yield


api = responder.API(
    templates_dir="tuftecms/templates",
    static_dir="tuftecms/static",
    static_route="/static",
    lifespan=_lifespan,
    enable_logging=True,
    request_id=True,  # X-Request-ID on every response, attached to log lines
    security_headers=True,  # nosniff, X-Frame-Options, Referrer-Policy
    auto_etag=True,
    max_request_size=1024 * 1024,  # every route is GET; nobody needs to send us a megabyte
    request_timeout=60,  # PDF generation is the slow path
    metrics_route="/metrics",
    health_route="/health",
    sessions=False,  # every route is stateless GET; no sessions to sign
    problem_details=True,
    title="kennethreitz.org",
    description="API for kennethreitz.org",
    version="1.0",
    openapi="3.0.0",  # responder builds the spec from route type hints
    openapi_route="/api/schema",
    docs_route="/api",  # interactive Swagger UI
)


def _content_health_check():
    """Verify the markdown garden exists before advertising readiness."""
    return (
        DATA_DIR.is_dir()
        and (DATA_DIR / "colophon.md").is_file()
        and (DATA_DIR / "essays").is_dir()
    )


api.add_health_check("content", _content_health_check)

# --- Rate limiting ---
from responder.ext.ratelimit import RateLimiter


def _int_from_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


RateLimiter(
    requests=_int_from_env("RATE_LIMIT_REQUESTS", 1800),
    period=_int_from_env("RATE_LIMIT_PERIOD", 60),
).install(api)


# --- Long-lived caching for static assets ---
class _StaticCacheMiddleware:
    """CSS carries a content-hash ?v=, so versioned assets can cache forever;
    everything else under /static gets a week."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope["path"].startswith("/static/"):
            await self.app(scope, receive, send)
            return

        versioned = b"v=" in scope.get("query_string", b"")

        async def send_with_cache(message):
            if message["type"] == "http.response.start" and message.get("status") == 200:
                headers = message.setdefault("headers", [])
                if not any(k.lower() == b"cache-control" for k, _ in headers):
                    value = (
                        b"public, max-age=31536000, immutable"
                        if versioned
                        else b"public, max-age=604800"
                    )
                    headers.append((b"cache-control", value))
            await send(message)

        await self.app(scope, receive, send_with_cache)


api.add_middleware(_StaticCacheMiddleware)

# Suppress access logging for static assets.
class _StaticFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return "/static/" not in msg and not msg.endswith((".js", ".css", ".ico", ".png", ".woff2"))

logging.getLogger("responder.access").addFilter(_StaticFilter())
logging.getLogger("fontTools.subset").setLevel(logging.WARNING)

# --- Markdown render cache ---
_render_cache = {}


def _cached_render(file_path):
    """Cache rendered markdown by file path."""
    key = str(file_path)
    if key not in _render_cache:
        _render_cache[key] = render_markdown_file(file_path)
    return _render_cache[key]


# Custom template filters
api.templates.context["current_year"] = datetime.now().year


def strftime_filter(value, fmt="%B %d, %Y"):
    if value == "now":
        return datetime.now().strftime(fmt)
    if hasattr(value, "strftime"):
        return value.strftime(fmt)
    return value


api.templates._env.filters["strftime"] = strftime_filter


class FakeConfig(dict):
    """Minimal config stand-in for Flask template compatibility."""
    def get(self, key, default=None):
        return os.environ.get(key, default)


class RequestWrapper:
    """Wraps Responder request to provide Flask-like interface for templates."""
    def __init__(self, req, path):
        self._req = req
        self.path = path
        self.environ = {}

    def __getattr__(self, name):
        return getattr(self._req, name)


_config = FakeConfig()

try:
    from weasyprint import HTML
    _pdf_available = True
except (ImportError, OSError):
    _pdf_available = False


api.state.nav_cache = {}


def _nav_data():
    """Server-rendered nav dropdown data (crawlable; no JS fetch)."""
    if "themes" not in api.state.nav_cache:
        themes_dir = DATA_DIR / "themes"
        items = []
        if themes_dir.is_dir():
            for f in sorted(themes_dir.glob("*.md")):
                if f.name == "index.md":
                    continue
                title = get_cached_markdown_title(f) or f.stem.replace("-", " ").replace("_", " ").title()
                items.append({
                    "name": title,
                    "path": f"/themes/{f.stem}",
                    "icon": generate_unique_svg_icon(title, size=18),
                })
        api.state.nav_cache["themes"] = items
    if "browse" not in api.state.nav_cache:
        folders = []
        files = []
        for item in sorted(DATA_DIR.iterdir()):
            if item.name.startswith(".") or item.name in ["__pycache__", "node_modules"]:
                continue
            if item.is_dir():
                display_name = item.name.replace("-", " ").replace("_", " ").title()
                index_file = item / "index.md"
                if index_file.exists():
                    title = get_cached_markdown_title(index_file)
                    if title:
                        display_name = title
                folders.append({
                    "name": display_name,
                    "path": f"/{item.name}",
                    "is_dir": True,
                    "icon": generate_folder_icon(display_name, size=18),
                })
            elif item.suffix == ".md" and item.name != "index.md":
                display_name = get_cached_markdown_title(item) or item.stem
                files.append({
                    "name": display_name,
                    "path": f"/{item.stem}",
                    "is_dir": False,
                    "icon": generate_unique_svg_icon(display_name, size=18),
                })
        api.state.nav_cache["browse"] = folders + files
    return api.state.nav_cache


def _static_version():
    """Cache-busting version for stylesheets: content hash of the CSS files.

    A content hash (unlike mtime) is deterministic across machines and
    deploys -- the URL only changes when the bytes actually change.
    """
    static_dir = Path("tuftecms/static")
    digest = hashlib.md5()
    for name in ("site.css", "custom.css", "tufte/tufte.css"):
        css_path = static_dir / name
        if css_path.exists():
            digest.update(css_path.read_bytes())
    return digest.hexdigest()[:12]


_static_v = _static_version()


def render(template, req, path="/", **kwargs):
    """Render a template with common context."""
    kwargs.setdefault("current_year", datetime.now().year)
    kwargs.setdefault("current_path", path)
    kwargs["request"] = RequestWrapper(req, path)
    kwargs["config"] = _config
    kwargs.setdefault("pdf_available", _pdf_available)
    kwargs.setdefault("static_v", _static_v)
    nav = _nav_data()
    kwargs.setdefault("nav_themes", nav["themes"])
    kwargs.setdefault("nav_browse", nav["browse"])
    return api.templates.render(template, **kwargs)


def respond_html(resp, template, req, path="/", **kwargs):
    """Render a template into the response with a content-based ETag.

    Responder turns matching If-None-Match requests into automatic 304s,
    so repeat visitors skip the body bytes entirely.
    """
    html_out = render(template, req, path, **kwargs)
    resp.html = html_out
    resp.etag = 'W/"' + hashlib.md5(html_out.encode("utf-8")).hexdigest()[:16] + '"'


# --- Cache for OG images ---
api.state.og_images = {}
_OG_CACHE_MAX = 256


# --- Bot detection ---

_BOT_PATTERNS = re.compile(
    r"(?i)(googlebot|bingbot|slurp|duckduckbot|baiduspider|yandexbot|sogou|"
    r"exabot|facebookexternalhit|facebot|ia_archiver|alexa|msnbot|"
    r"semrushbot|ahrefsbot|dotbot|petalbot|mj12bot|bytespider|"
    r"gptbot|chatgpt|claudebot|anthropic|ccbot|commoncrawl|"
    r"scrapy|python-requests|httpx|curl|wget|go-http-client|"
    r"applebot|twitterbot|linkedinbot|whatsapp|telegrambot|"
    r"dataprovider|censys|zgrab|masscan|nuclei|httpie)"
)


def _detect_bot(req):
    """Detect and log bot/scraper requests. Returns bot name or None."""
    ua = req.headers.get("User-Agent", "")
    if not ua:
        return "unknown (no user-agent)"
    m = _BOT_PATTERNS.search(ua)
    if m:
        return m.group(1)
    return None


# --- Routes ---
# IMPORTANT: All specific routes must be defined BEFORE the catch-all route.


@api.route("/")
async def homepage(req, resp):
    blog_data = get_blog_cache()
    recent_posts = blog_data.get("posts", [])[:5]
    respond_html(resp, "homepage.html", req, "/",
        title="Home",
        recent_posts=recent_posts,
    )


@api.route("/random")
async def random_post(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])
    if posts:
        chosen = random.choice(posts)
        api.log.info("Redirecting to random post: %s", chosen["url"])
        resp.cache_control(no_cache=True, no_store=True, must_revalidate=True)
        api.redirect(resp, chosen["url"])
    else:
        resp.status_code = 404


@api.route("/search")
async def search_page(req, resp):
    respond_html(resp, "search.html", req, "/search",
        title="Search",
    )


# --- Feed routes ---


@api.route("/robots.txt")
async def robots_txt(req, resp):
    bot = _detect_bot(req)
    ua = req.headers.get("User-Agent", "no user-agent")
    api.log.info("Bot detected: %s (%s)", bot or "unknown", ua)
    robots_content = """# Robots.txt for kennethreitz.org
# Welcome, friendly crawlers!

User-agent: *
Allow: /

# Sitemap location
Sitemap: https://kennethreitz.org/sitemap.xml

# Crawl-delay suggestion (be gentle)
Crawl-delay: 1

# Disallow admin/internal paths (none currently, but good practice)
# Disallow: /admin/"""
    resp.text = robots_content.strip()
    resp.headers["Content-Type"] = "text/plain"


@api.route("/sitemap")
async def sitemap_page(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    sitemap_data = {
        "homepage": [{"url": "/", "title": "Home", "modified": None}],
        "directory": [
            {"url": "/archive", "title": "Archive", "modified": None},
            {"url": "/sidenotes", "title": "Sidenotes", "modified": None},
            {"url": "/outlines", "title": "Outlines", "modified": None},
            {"url": "/quotes", "title": "Quotes", "modified": None},
            {"url": "/connections", "title": "Connections", "modified": None},
            {"url": "/terms", "title": "Terms", "modified": None},
            {"url": "/graph", "title": "Graph", "modified": None},
            {"url": "/search", "title": "Search", "modified": None},
        ],
        "article": [
            {"url": post["url"], "title": post["title"], "modified": post["pub_date"]}
            for post in posts
        ],
    }

    total_items = (
        len(sitemap_data["homepage"])
        + len(sitemap_data["directory"])
        + len(sitemap_data["article"])
    )

    respond_html(resp, "sitemap.html", req, "/sitemap",
        sitemap_data=sitemap_data,
        total_items=total_items,
        title="Sitemap",
    )


@api.route("/sitemap.xml")
async def sitemap_xml(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    urls = []

    # Add homepage
    urls.append({
        "url": "https://kennethreitz.org/",
        "lastmod": datetime.now().strftime("%Y-%m-%d"),
        "priority": "1.0",
    })

    # Add static pages
    static_pages = [
        "/archive",
        "/sidenotes",
        "/outlines",
        "/quotes",
        "/connections",
        "/terms",
        "/graph",
        "/search",
    ]

    for page in static_pages:
        urls.append({
            "url": f"https://kennethreitz.org{page}",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "priority": "0.8",
        })

    # Add blog posts
    for post in posts:
        urls.append({
            "url": f"https://kennethreitz.org{post['url']}",
            "lastmod": post["date_str"],
            "priority": "0.9",
        })

    # Generate XML
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url_data in urls:
        xml_lines.append("    <url>")
        xml_lines.append(f"        <loc>{url_data['url']}</loc>")
        xml_lines.append(f"        <lastmod>{url_data['lastmod']}</lastmod>")
        xml_lines.append(f"        <priority>{url_data['priority']}</priority>")
        xml_lines.append("    </url>")

    xml_lines.append("</urlset>")
    xml_content = "\n".join(xml_lines)

    resp.text = xml_content
    resp.headers["Content-Type"] = "application/xml"


@api.route("/feed.xml")
async def feed_xml(req, resp):
    await _rss_feed(req, resp)


@api.route("/rss.xml")
async def rss_xml(req, resp):
    await _rss_feed(req, resp)


def _rss_full_content(url):
    """Full rendered HTML for a post, prepared for a feed reader.

    Absolute URLs, and Tufte sidenotes flattened into inline parentheticals
    since the margin-toggle checkbox trick doesn't work outside the site.
    """
    md_path = DATA_DIR / f"{url.lstrip('/')}.md"
    if not md_path.exists():
        return None
    try:
        content = _cached_render(md_path)["content"]
    except Exception:
        return None

    content = re.sub(r'<label[^>]*class="margin-toggle[^>]*>.*?</label>', "", content, flags=re.DOTALL)
    content = re.sub(r'<input[^>]*class="margin-toggle"[^>]*/?>', "", content)
    content = re.sub(
        r'<span class="sidenote">(.*?)</span>',
        r"<em> (\1)</em>",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(r'(src|href)="/(?!/)', r'\1="https://kennethreitz.org/', content)
    return content


async def _rss_feed(req, resp):
    """Generate RSS feed."""
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    recent_posts = posts[:20]

    rss_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    rss_lines.append('<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">')
    rss_lines.append("    <channel>")
    rss_lines.append("        <title>Kenneth Reitz</title>")
    rss_lines.append("        <link>https://kennethreitz.org</link>")
    rss_lines.append(
        "        <description>Creator of Requests, Pipenv, and other tools. Writing about technology, consciousness, and human-centered design.</description>"
    )
    rss_lines.append("        <language>en-us</language>")
    # Latest post date, not now(): keeps the feed bytes stable so the
    # content ETag below actually matches between requests.
    last_build = None
    if recent_posts and recent_posts[0].get("pub_date"):
        last_build = recent_posts[0]["pub_date"]
    rss_lines.append(
        f'        <lastBuildDate>{(last_build or datetime.now()).strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>'
    )

    for post in recent_posts:
        rss_lines.append("        <item>")
        rss_lines.append(f'            <title>{html.escape(post["title"])}</title>')
        rss_lines.append(
            f'            <link>https://kennethreitz.org{post["url"]}</link>'
        )
        rss_lines.append(
            f'            <guid>https://kennethreitz.org{post["url"]}</guid>'
        )
        rss_lines.append(
            f'            <description>{html.escape(post.get("description", post.get("excerpt", "")))}</description>'
        )

        full_html = _rss_full_content(post["url"])
        if full_html:
            cdata_safe = full_html.replace("]]>", "]]]]><![CDATA[>")
            rss_lines.append(
                f"            <content:encoded><![CDATA[{cdata_safe}]]></content:encoded>"
            )

        pub_date = post["pub_date"]
        rss_date = pub_date.strftime("%a, %d %b %Y %H:%M:%S %z") if pub_date else ""
        if rss_date:
            rss_lines.append(f"            <pubDate>{rss_date}</pubDate>")

        rss_lines.append("        </item>")

    rss_lines.append("    </channel>")
    rss_lines.append("</rss>")

    rss_content = "\n".join(rss_lines)

    resp.text = rss_content
    resp.headers["Content-Type"] = "application/xml"
    resp.etag = hashlib.md5(rss_content.encode("utf-8")).hexdigest()[:16]


# --- OG image route ---


def _extract_og_excerpt(content):
    """First real paragraph of a markdown file, plain-texted for the OG card."""
    content = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

    paragraphs = []
    block = []
    in_code = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            block = []
            continue
        if in_code:
            continue
        if not stripped:
            if block:
                paragraphs.append(" ".join(block))
                block = []
            continue
        # Skip headings, quotes, lists, tables, raw html, images, and the
        # *Month Year* date line; they make poor card excerpts.
        if stripped.startswith(("#", ">", "-", "*", "|", "<", "!", "$")):
            if block:
                paragraphs.append(" ".join(block))
                block = []
            continue
        block.append(stripped)
    if block:
        paragraphs.append(" ".join(block))

    for para in paragraphs:
        text = re.sub(r"<label.*?</span>", "", para, flags=re.DOTALL)  # sidenotes
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
        text = text.replace("**", "").replace("`", "").replace("*", "")
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 80:
            return text
    return None


@api.route("/og-image/{path:path}.png")
async def og_image(req, resp, *, path):
    """Generate a dynamic Open Graph image for a post."""
    from PIL import Image, ImageDraw, ImageFont

    api.log.info("Generating OG image for /%s", path)

    # Check cache
    cache_key = path
    if cache_key in api.state.og_images:
        png = api.state.og_images[cache_key]
        resp.content = png
        resp.headers["Content-Type"] = "image/png"
        resp.cache_control(public=True, max_age=86400)
        resp.etag = hashlib.md5(png).hexdigest()[:16]
        return

    # Validate path stays within data directory
    file_path = (DATA_DIR / f"{path}.md").resolve()
    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        resp.status_code = 403
        return

    # Resolve the post title and an excerpt from the markdown file
    title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()
    subtitle = None
    excerpt = None

    if file_path.exists():
        content = file_path.read_text()
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("*") and line.endswith("*") and len(line) < 60:
                subtitle = line.strip("*")
                break
        excerpt = _extract_og_excerpt(content)

    # Image dimensions (standard OG)
    width, height = 1200, 630

    # Create image with Tufte cream background
    img = Image.new("RGB", (width, height), "#fffff8")
    draw = ImageDraw.Draw(img)

    # Draw subtle bottom gradient
    for y in range(height - 80, height):
        alpha = (y - (height - 80)) / 80
        r = int(255 * (1 - alpha) + 245 * alpha)
        g = int(255 * (1 - alpha) + 245 * alpha)
        b = int(248 * (1 - alpha) + 232 * alpha)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load fonts (bundled et-book)
    font_dir = Path(__file__).parent / "tuftecms" / "static" / "tufte" / "et-book"
    try:
        font_italic = ImageFont.truetype(
            str(font_dir / "et-book-display-italic-old-style-figures" / "et-book-display-italic-old-style-figures.ttf"),
            62,
        )
        font_roman = ImageFont.truetype(
            str(font_dir / "et-book-roman-line-figures" / "et-book-roman-line-figures.ttf"),
            26,
        )
        font_excerpt = ImageFont.truetype(
            str(font_dir / "et-book-roman-line-figures" / "et-book-roman-line-figures.ttf"),
            29,
        )
        font_small = ImageFont.truetype(
            str(font_dir / "et-book-roman-line-figures" / "et-book-roman-line-figures.ttf"),
            22,
        )
    except (OSError, IOError):
        font_italic = ImageFont.load_default()
        font_roman = ImageFont.load_default()
        font_excerpt = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw accent line
    draw.rectangle([80, 130, 200, 134], fill="#333333")

    # Word-wrap and draw title
    max_chars = 28 if len(title) > 28 else 40
    wrapped = textwrap.wrap(title, width=max_chars)
    y_pos = 156
    for line in wrapped[:3]:
        draw.text((80, y_pos), line, font=font_italic, fill="#111111")
        y_pos += 72

    # Draw subtitle/date if available
    if subtitle:
        draw.text((80, y_pos + 12), subtitle, font=font_roman, fill="#666666")
        y_pos += 50

    # Draw the opening of the piece, so the card shows actual content.
    if excerpt:
        y_pos += 28
        lines = textwrap.wrap(excerpt, width=70)
        line_height = 42
        max_lines = max(0, (height - 120 - y_pos) // line_height)
        shown = lines[:max_lines]
        if shown and len(lines) > max_lines:
            shown[-1] = shown[-1].rstrip(".,;:") + " ..."
        for line in shown:
            draw.text((80, y_pos), line, font=font_excerpt, fill="#444444")
            y_pos += line_height
    else:
        # Decorative circles for pages with no prose to preview.
        cx, cy = 1060, 300
        for r_val, c in [(50, "#dddddd"), (35, "#cccccc"), (20, "#bbbbbb")]:
            draw.ellipse([cx - r_val, cy - r_val, cx + r_val, cy + r_val], outline=c, width=2)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill="#999999")

    # Draw separator line
    draw.rectangle([80, height - 110, width - 80, height - 108], fill="#dddddd")

    # Draw site URL
    draw.text((80, height - 85), "kennethreitz.org", font=font_small, fill="#999999")

    # Draw author name on right
    author_text = "Kenneth Reitz"
    bbox = draw.textbbox((0, 0), author_text, font=font_small)
    author_width = bbox[2] - bbox[0]
    draw.text((width - 80 - author_width, height - 85), author_text, font=font_small, fill="#999999")

    # Export to PNG bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    png_bytes = buf.getvalue()

    # Cache it (bounded)
    if len(api.state.og_images) >= _OG_CACHE_MAX:
        api.state.og_images.pop(next(iter(api.state.og_images)))
    api.state.og_images[cache_key] = png_bytes

    resp.content = png_bytes
    resp.headers["Content-Type"] = "image/png"
    resp.cache_control(public=True, max_age=86400)
    resp.etag = hashlib.md5(png_bytes).hexdigest()[:16]


# --- Image thumbnails ---

_THUMB_DIR = Path(".cache/thumbs")
_THUMB_WIDTHS = (320, 640, 1280)
_THUMB_TYPES = {".jpg", ".jpeg", ".png", ".webp"}


def _make_thumbnail(source, dest, width):
    """Resize an image to fit `width`, honoring EXIF orientation."""
    from PIL import Image, ImageOps

    with Image.open(source) as img:
        img = ImageOps.exif_transpose(img)
        img.thumbnail((width, width * 3))
        if "A" in img.getbands() or img.mode == "P":
            background = Image.new("RGB", img.size, (255, 255, 248))
            background.paste(img.convert("RGBA"), mask=img.convert("RGBA"))
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, format="JPEG", quality=82, optimize=True, progressive=True)


@api.route("/thumb/{path:path}")
async def thumbnail(req, resp, *, path):
    """Resized gallery thumbnails; originals remain one click away in the lightbox."""
    source = (DATA_DIR / path).resolve()
    if not str(source).startswith(str(DATA_DIR.resolve())):
        resp.status_code = 403
        return
    if not source.is_file() or source.suffix.lower() not in _THUMB_TYPES:
        resp.status_code = 404
        return

    try:
        requested = int(req.params.get("w", "640"))
    except (TypeError, ValueError):
        requested = 640
    width = min(_THUMB_WIDTHS, key=lambda w: abs(w - requested))

    key = hashlib.md5(
        f"{path}:{source.stat().st_mtime_ns}:{width}".encode()
    ).hexdigest()
    cached = _THUMB_DIR / f"{key}.jpg"
    if not cached.exists():
        try:
            await asyncio.to_thread(_make_thumbnail, source, cached, width)
        except OSError:
            resp.file(str(source))
            return

    resp.etag = key[:16]
    resp.cache_control(public=True, max_age=31536000, immutable=True)
    resp.file(str(cached), content_type="image/jpeg")


# --- Archive routes ---


@api.route("/archive")
async def archive(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Group posts by year
    grouped_posts = defaultdict(list)
    for post in posts:
        year = post["pub_date"].year
        grouped_posts[year].append(post)

    # Sort years in descending order
    grouped_posts = dict(sorted(grouped_posts.items(), reverse=True))

    respond_html(resp, "archive.html", req, "/archive",
        posts=posts,
        grouped_posts=grouped_posts,
        archive_title="Complete Archive",
        title="Archive",
    )


@api.route("/archive/by-length")
async def archive_by_length(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Calculate reading time (average 200 words per minute)
    for post in posts:
        word_count = post.get("word_count", 0)
        post["reading_time"] = max(1, round(word_count / 200))

    # Group by reading time ranges
    quick_reads = [p for p in posts if p["reading_time"] <= 3]
    short_reads = [p for p in posts if 4 <= p["reading_time"] <= 7]
    medium_reads = [p for p in posts if 8 <= p["reading_time"] <= 15]
    long_reads = [p for p in posts if p["reading_time"] > 15]

    # Sort each group by word count descending
    quick_reads.sort(key=lambda x: x.get("word_count", 0), reverse=True)
    short_reads.sort(key=lambda x: x.get("word_count", 0), reverse=True)
    medium_reads.sort(key=lambda x: x.get("word_count", 0), reverse=True)
    long_reads.sort(key=lambda x: x.get("word_count", 0), reverse=True)

    grouped_posts = {}
    if quick_reads:
        grouped_posts["Quick Reads (1-3 min)"] = quick_reads
    if short_reads:
        grouped_posts["Short Reads (4-7 min)"] = short_reads
    if medium_reads:
        grouped_posts["Medium Reads (8-15 min)"] = medium_reads
    if long_reads:
        grouped_posts["Long Reads (15+ min)"] = long_reads

    respond_html(resp, "archive-by-length.html", req, "/archive/by-length",
        posts=posts,
        grouped_posts=grouped_posts,
        archive_title="By Reading Time",
        title="Archive by Reading Time",
    )


@api.route("/archive/sidenotes")
async def sidenotes(req, resp):
    cache_data = get_sidenotes_cache()
    blog_data = get_blog_cache()

    # Create lookup for post metadata
    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    # Convert cache format to template format
    articles = []
    total_sidenotes = 0

    for _, sidenotes_list in cache_data.get("sidenotes", {}).items():
        if sidenotes_list:
            first_sidenote = sidenotes_list[0]
            article_title = first_sidenote.get("title", "Unknown")
            article_url = first_sidenote.get("url", "#")

            post_data = post_lookup.get(article_url, {})

            articles.append({
                "title": article_title,
                "url": article_url,
                "sidenotes": sidenotes_list,
                "category": "essays",
                "date": post_data.get("pub_date"),
                "unique_icon": post_data.get("unique_icon"),
            })
            total_sidenotes += len(sidenotes_list)

    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    respond_html(resp, "sidenotes.html", req, "/archive/sidenotes",
        articles=articles,
        total_count=total_sidenotes,
        title="Sidenotes",
    )


@api.route("/archive/outlines")
async def outlines(req, resp):
    cache_data = get_outlines_cache()
    blog_data = get_blog_cache()

    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    articles = []
    total_headings = 0

    for _, headings_list in cache_data.get("outlines", {}).items():
        if headings_list:
            first_heading = headings_list[0]
            article_title = first_heading.get("title", "Unknown")
            article_url = first_heading.get("url", "#")

            post_data = post_lookup.get(article_url, {})

            articles.append({
                "title": article_title,
                "url": article_url,
                "headings": headings_list,
                "category": "essays",
                "date": post_data.get("pub_date"),
                "unique_icon": post_data.get("unique_icon"),
            })
            total_headings += len(headings_list)

    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    respond_html(resp, "outlines.html", req, "/archive/outlines",
        articles=articles,
        total_count=total_headings,
        title="Outlines",
    )


@api.route("/archive/quotes")
async def quotes(req, resp):
    cache_data = get_quotes_cache()
    blog_data = get_blog_cache()

    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    articles = []
    total_quotes = 0

    for _, quotes_list in cache_data.get("quotes", {}).items():
        if quotes_list:
            first_quote = quotes_list[0]
            article_title = first_quote.get("title", "Unknown")
            article_url = first_quote.get("url", "#")

            post_data = post_lookup.get(article_url, {})

            articles.append({
                "title": article_title,
                "url": article_url,
                "quotes": quotes_list,
                "category": "essays",
                "date": post_data.get("pub_date"),
                "unique_icon": post_data.get("unique_icon"),
            })
            total_quotes += len(quotes_list)

    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    respond_html(resp, "quotes.html", req, "/archive/quotes",
        articles=articles,
        total_count=total_quotes,
        title="Quotes",
    )


@api.route("/archive/connections")
async def connections(req, resp):
    cache_data = get_connections_cache()
    blog_data = get_blog_cache()

    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    articles = []
    outgoing_data = cache_data.get("outgoing", {})
    incoming_data = cache_data.get("incoming", {})
    stats = cache_data.get("stats", {})

    for file_path, connections_list in outgoing_data.items():
        if connections_list:
            file_stem = Path(file_path).stem
            article_url = f"/essays/{file_stem}"

            post_data = post_lookup.get(article_url, {})
            article_title = post_data.get("title", file_stem.replace("-", " ").title())

            incoming_connections = incoming_data.get(article_url, [])

            formatted_outgoing = []
            for conn in connections_list:
                formatted_outgoing.append(
                    {"link_text": conn["text"], "target_url": conn["url"]}
                )

            formatted_incoming = []
            for conn in incoming_connections:
                formatted_incoming.append({
                    "link_text": conn["text"],
                    "source_url": conn.get("source_url", "#"),
                    "context": conn.get("context", ""),
                })

            articles.append({
                "title": article_title,
                "url": article_url,
                "outgoing_connections": formatted_outgoing,
                "incoming_connections": formatted_incoming,
                "category": "essays",
                "date": post_data.get("pub_date"),
                "unique_icon": post_data.get("unique_icon"),
            })

    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    respond_html(resp, "connections.html", req, "/archive/connections",
        articles=articles,
        total_outgoing=stats.get("total_outgoing", 0),
        total_incoming=stats.get("total_incoming", 0),
        title="Connections",
    )


@api.route("/archive/terms")
async def terms(req, resp):
    terms_data = get_terms_cache()
    stats = terms_data.get("stats", {})
    respond_html(resp, "terms.html", req, "/archive/terms",
        terms=terms_data.get("terms", {}),
        total_terms=stats.get("total_terms", 0),
        total_occurrences=stats.get("total_references", 0),
        title="Index of Terms",
    )


@api.route("/archive/themes")
async def themes_archive(req, resp):
    themes_data = get_themes_cache()
    themes = themes_data.get("themes", {})
    stats = themes_data.get("stats", {})

    sorted_themes = sorted(themes.items(), key=lambda x: x[0])

    respond_html(resp, "themes.html", req, "/archive/themes",
        themes=dict(sorted_themes),
        total_themes=stats.get("total_themes", 0),
        total_occurrences=stats.get("total_occurrences", 0),
        title="Themes",
    )


@api.route("/archive/graph")
async def graph(req, resp):
    respond_html(resp, "graph.html", req, "/archive/graph",
        title="Knowledge Graph",
    )


# Bare aliases for the archive views (the sitemap advertises these).
def _make_archive_alias(target):
    async def archive_alias(req, resp):
        api.redirect(resp, target, status_code=308)
    return archive_alias


for _page in ("sidenotes", "outlines", "quotes", "connections", "terms", "graph"):
    api.route(f"/{_page}")(_make_archive_alias(f"/archive/{_page}"))


_GRAPH_SKIP_PREFIXES = ("static/", "data/", "api/", "archive", "feed", "search", "sitemap")
_GRAPH_ASSET_SUFFIXES = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
    ".pdf", ".md", ".mp3", ".xml", ".css", ".js",
)


def _graph_skip(path):
    """Content pages only: no assets, indexes, or machine endpoints."""
    lowered = path.lower()
    return (
        not path
        or lowered.startswith(_GRAPH_SKIP_PREFIXES)
        or lowered.endswith(_GRAPH_ASSET_SUFFIXES)
    )


@api.route("/archive/graph/data")
async def graph_data(req, resp):
    connections_data = get_connections_cache()
    blog_data = get_blog_cache()

    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    def make_node(path):
        url = f"/{path}"
        post = post_lookup.get(url, {})
        title = post.get("title") or path.split("/")[-1].replace("-", " ").replace("_", " ").title()
        category = path.split("/")[0] if "/" in path else "pages"
        return {
            "id": path,
            "title": title,
            "label": title,
            "url": url,
            "category": category,
            "group": category,
        }

    nodes = {}
    edges = []
    seen_edges = set()

    for source, targets in connections_data.get("outgoing", {}).items():
        source_path = source.replace("data/", "", 1).removesuffix(".md").strip("/")
        if _graph_skip(source_path):
            continue

        for target_info in targets:
            target_path = target_info["url"].strip("/")
            if _graph_skip(target_path) or target_path == source_path:
                continue
            key = (source_path, target_path)
            if key in seen_edges:
                continue
            seen_edges.add(key)

            nodes.setdefault(source_path, make_node(source_path))
            nodes.setdefault(target_path, make_node(target_path))
            edges.append({
                "source": source_path,
                "target": target_path,
                "label": target_info["text"],
                "link_text": target_info["text"],
            })

    resp.media = {"nodes": list(nodes.values()), "edges": edges}


# --- Directory route ---


@api.route("/directory")
async def directory(req, resp):
    items = get_directory_structure(DATA_DIR)
    respond_html(resp, "directory.html", req, "/directory",
        items=items,
        current_path="/",
        breadcrumb=[],
        title="Directory",
    )


# --- API routes ---


# --- JSON API response models ---
#
# These drive both runtime validation and the OpenAPI spec at /api/schema:
# responder validates each route's resp.media against its response_model and
# documents the shape in the Swagger UI. Routes whose output isn't stable
# enough to promise (the oEmbed proxy, fortune command, cache debug dump) stay
# lightly described rather than fully modeled.


class BlogPostOut(BaseModel):
    title: str
    url: str
    category: str
    date: str
    word_count: int
    unique_icon: str


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    section: str
    score: int
    matches: list[str]
    unique_icon: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int = 0
    error: str | None = None


class AutocompleteResult(BaseModel):
    title: str
    url: str
    icon: str


class AutocompleteResponse(BaseModel):
    results: list[AutocompleteResult]


class IconResponse(BaseModel):
    success: bool
    path: str
    icon: str


class DirectoryItem(BaseModel):
    name: str
    path: str
    is_dir: bool
    icon: str


class DirectoryTreeResponse(BaseModel):
    items: list[DirectoryItem]


class ThemeItem(BaseModel):
    name: str
    path: str
    icon: str


class ThemesResponse(BaseModel):
    themes: list[ThemeItem]


_EXAMPLE_ICON = "data:image/svg+xml;base64,PHN2Zy8+"


def _json_object_response(description):
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": {"type": "object", "additionalProperties": True}
            }
        },
    }


def _fortune_response(description):
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "fortune": {"type": "string"},
                        "offensive": {"type": "boolean"},
                    },
                    "required": ["fortune", "offensive"],
                }
            }
        },
    }


OPENAPI_EXAMPLES = {
    "blog": {
        "first_page": {
            "summary": "A page of recent essays",
            "value": {
                "items": [
                    {
                        "title": "Programming as Spiritual Practice",
                        "url": "/essays/2025-08-26-programming_as_spiritual_practice",
                        "category": "essays",
                        "date": "2025-08-26",
                        "word_count": 2870,
                        "unique_icon": _EXAMPLE_ICON,
                    }
                ],
                "total": 42,
                "page": 1,
                "size": 20,
                "pages": 3,
            },
        }
    },
    "search": {
        "matches": {
            "summary": "Search results for a site concept",
            "value": {
                "query": "consciousness",
                "results": [
                    {
                        "title": "The Recursive Loop",
                        "url": "/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds",
                        "snippet": "...code shapes minds, programmers shape code...",
                        "section": "essays",
                        "score": 15,
                        "matches": ["title", "content"],
                        "unique_icon": _EXAMPLE_ICON,
                    }
                ],
                "total": 1,
                "error": None,
            },
        },
        "too_short": {
            "summary": "A query that is too short to search",
            "value": {
                "query": "a",
                "results": [],
                "total": 0,
                "error": "Query must be at least 2 characters long",
            },
        },
    },
    "autocomplete": {
        "suggestions": {
            "summary": "Title suggestions for the search box",
            "value": {
                "results": [
                    {
                        "title": "The Recursive Loop",
                        "url": "/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds",
                        "icon": _EXAMPLE_ICON,
                    }
                ]
            },
        }
    },
    "icon": {
        "article_icon": {
            "summary": "Generated icon for an article path",
            "value": {
                "success": True,
                "path": "essays/2025-08-26-programming_as_spiritual_practice",
                "icon": _EXAMPLE_ICON,
            },
        }
    },
    "debug_cache": {
        "cache_stats": {
            "summary": "Current cache counters",
            "value": {
                "status": "Cache data loaded successfully",
                "cache_stats": {
                    "blog": {"total_posts": 42},
                    "sidenotes": {"total_sidenotes": 128, "total_articles": 24},
                },
                "lru_cache_info": {
                    "blog_cache": {
                        "hits": 12,
                        "misses": 1,
                        "maxsize": 1,
                        "currsize": 1,
                    }
                },
            },
        }
    },
    "directory_tree": {
        "root_items": {
            "summary": "Top-level garden entries",
            "value": {
                "items": [
                    {
                        "name": "essays",
                        "path": "/essays",
                        "is_dir": True,
                        "icon": _EXAMPLE_ICON,
                    },
                    {
                        "name": "worldview",
                        "path": "/worldview",
                        "is_dir": False,
                        "icon": _EXAMPLE_ICON,
                    },
                ]
            },
        }
    },
    "themes": {
        "theme_list": {
            "summary": "Curated conceptual themes",
            "value": {
                "themes": [
                    {
                        "name": "The Algorithm Eats",
                        "path": "/themes/algorithmic-critique",
                        "icon": _EXAMPLE_ICON,
                    },
                    {
                        "name": "For Humans Philosophy",
                        "path": "/themes/for-humans-philosophy",
                        "icon": _EXAMPLE_ICON,
                    },
                ]
            },
        }
    },
    "oembed": {
        "embed": {
            "summary": "Discovered oEmbed payload",
            "value": {
                "type": "rich",
                "version": "1.0",
                "title": "Example Embed",
                "provider_name": "Example",
                "html": '<iframe src="https://example.com/embed"></iframe>',
                "width": 640,
                "height": 360,
            },
        }
    },
    "fortune": {
        "fortune": {
            "summary": "A fortune response",
            "value": {
                "fortune": "The interface is the contract.",
                "offensive": False,
            },
        }
    },
}


OPENAPI_ERROR_EXAMPLES = {
    "oembed": {
        400: {
            "invalid_url": {
                "summary": "Missing or invalid URL",
                "value": {"error": "Missing or invalid url parameter"},
            }
        },
        404: {
            "not_found": {
                "summary": "No oEmbed endpoint discovered",
                "value": {"error": "No oEmbed endpoint found"},
            }
        },
        502: {
            "upstream_failure": {
                "summary": "Discovery or fetch failed",
                "value": {"error": "oEmbed discovery failed"},
            }
        },
    },
    "fortune": {
        404: {
            "offensive_unavailable": {
                "summary": "Requested fortune set is unavailable",
                "value": {
                    "error": "offensive fortunes are not available",
                    "offensive": True,
                },
            }
        },
        503: {
            "missing_binary": {
                "summary": "Fortune command is unavailable",
                "value": {"error": "fortune command is not installed"},
            }
        },
    },
}


@api.route(
    "/api/blog",
    response_model=Page[BlogPostOut],
    examples=OPENAPI_EXAMPLES["blog"],
)
async def api_blog(
    req,
    resp,
    *,
    category: str | None = Query(
        None,
        description="Filter posts by category.",
        examples=["essays"],
    ),
    sort: str = Query(
        "-pub_date",
        description=(
            "Sort by title, word_count, or pub_date. Prefix with - for "
            "descending."
        ),
        examples=["-pub_date"],
    ),
    page: int = Query(
        1,
        ge=1,
        description="One-based page number.",
        examples=[1],
    ),
    size: int = Query(
        20,
        ge=1,
        le=100,
        description="Posts per page.",
        examples=[20],
    ),
):
    """List blog posts as a paginated envelope.

    Filter with ?category=, order with ?sort= (title, word_count, or pub_date;
    prefix a field with - for descending), and page with ?page=/?size=. Returns
    {items, total, page, size, pages}.
    """
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Filter and sort on the cached posts (which still carry the real pub_date
    # datetime and category) before projecting down to the public fields.
    posts = filter_items(posts, {"category": category})
    posts = sort_items(posts, sort, allowed={"title", "word_count", "pub_date"})

    posts_data = [
        {
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "category": post.get("category", ""),
            "date": post.get("date_str", ""),
            "word_count": post.get("word_count", 0),
            "unique_icon": post.get("unique_icon", ""),
        }
        for post in posts
    ]

    resp.media = paginate(posts_data, page=page, size=size).model_dump()


@api.route(
    "/api/search",
    response_model=SearchResponse,
    examples=OPENAPI_EXAMPLES["search"],
)
async def api_search(
    req,
    resp,
    *,
    q: str = Query(
        "",
        description="Full-text query. Must be at least two characters.",
        examples=["consciousness"],
    ),
):
    """Full-text search across the site. Pass ?q= (minimum two characters)."""
    query = q.strip()
    api.log.info("Search query: %s", query)

    if len(query) < 2:
        resp.media = {
            "query": query,
            "results": [],
            "error": "Query must be at least 2 characters long",
        }
        return

    _ensure_search_index()
    results = []
    query_lower = query.lower()

    for entry in _search_index:
        score = 0
        matches = []

        # Search in title (highest weight)
        if query_lower in entry["title"].lower():
            score += 10
            matches.append("title")

        # Search in content (medium weight)
        if query_lower in entry["raw_text"]:
            score += 5
            matches.append("content")

        if score > 0:
            snippet = ""
            if "content" in matches:
                query_index = entry["raw_text"].find(query_lower)
                if query_index != -1:
                    raw = entry["raw"]
                    start = max(0, query_index - 100)
                    end = min(len(raw), query_index + len(query) + 100)
                    snippet = raw[start:end].strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(raw):
                        snippet = snippet + "..."

            results.append({
                "title": entry["title"],
                "url": entry["url"],
                "snippet": snippet,
                "section": entry["section"],
                "score": score,
                "matches": matches,
                "unique_icon": entry["icon"],
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:50]

    resp.media = {"query": query, "results": results, "total": len(results)}


@api.route(
    "/api/search/autocomplete",
    response_model=AutocompleteResponse,
    examples=OPENAPI_EXAMPLES["autocomplete"],
)
async def api_search_autocomplete(
    req,
    resp,
    *,
    q: str = Query(
        "",
        description="Title fragment to autocomplete.",
        examples=["rec"],
    ),
):
    """Title-only autocomplete suggestions for the search box."""
    query = q.strip()

    if len(query) < 1:
        resp.media = {"results": []}
        return

    _ensure_search_index()
    query_lower = query.lower()
    matches = []

    for entry in _search_index:
        if query_lower in entry["title"].lower():
            matches.append({
                "title": entry["title"],
                "url": entry["url"],
                "icon": entry["icon"],
            })
            if len(matches) >= 8:
                break

    resp.media = {"results": matches}


@api.route(
    "/api/icon/{article_path:path}",
    response_model=IconResponse,
    examples=OPENAPI_EXAMPLES["icon"],
)
async def api_icon(
    req,
    resp,
    *,
    article_path: str = responder.Path(
        ...,
        description="Markdown article path without the data/ prefix or .md suffix.",
        examples=["essays/2025-08-26-programming_as_spiritual_practice"],
    ),
):
    """Generate and return an SVG icon for a given article."""
    title = article_path  # fallback to path
    is_folder = False

    data_path = Path("data") / f"{article_path}.md"
    if data_path.exists():
        cached_title = get_cached_markdown_title(data_path)
        if cached_title:
            title = cached_title
    else:
        dir_path = Path("data") / article_path
        if dir_path.is_dir():
            index_file = dir_path / "index.md"
            if index_file.exists():
                is_folder = True
                cached_title = get_cached_markdown_title(index_file)
                if cached_title:
                    title = cached_title
            else:
                title = article_path.split("/")[-1].replace("-", " ").replace("_", " ").title()
        else:
            title = article_path.split("/")[-1].replace("-", " ").replace("_", " ").title()

    if is_folder:
        icon_data = generate_folder_icon(title, size=24)
    else:
        icon_data = generate_unique_svg_icon(title, size=24)

    resp.media = {"success": True, "path": article_path, "icon": icon_data}


@api.route(
    "/api/debug-cache",
    responses={200: _json_object_response("Cache statistics and LRU counters.")},
    examples=OPENAPI_EXAMPLES["debug_cache"],
)
async def api_debug_cache(req, resp):
    cache_info = {
        "blog": get_blog_cache()["stats"],
        "sidenotes": get_sidenotes_cache()["stats"],
        "outlines": get_outlines_cache()["stats"],
        "quotes": get_quotes_cache()["stats"],
        "connections": get_connections_cache()["stats"],
        "terms": get_terms_cache()["stats"],
    }

    lru_cache_info = {
        "blog_cache": {
            "hits": get_blog_cache.cache_info().hits,
            "misses": get_blog_cache.cache_info().misses,
            "maxsize": get_blog_cache.cache_info().maxsize,
            "currsize": get_blog_cache.cache_info().currsize,
        },
        "sidenotes_cache": {
            "hits": get_sidenotes_cache.cache_info().hits,
            "misses": get_sidenotes_cache.cache_info().misses,
            "maxsize": get_sidenotes_cache.cache_info().maxsize,
            "currsize": get_sidenotes_cache.cache_info().currsize,
        },
        "outlines_cache": {
            "hits": get_outlines_cache.cache_info().hits,
            "misses": get_outlines_cache.cache_info().misses,
            "maxsize": get_outlines_cache.cache_info().maxsize,
            "currsize": get_outlines_cache.cache_info().currsize,
        },
        "quotes_cache": {
            "hits": get_quotes_cache.cache_info().hits,
            "misses": get_quotes_cache.cache_info().misses,
            "maxsize": get_quotes_cache.cache_info().maxsize,
            "currsize": get_quotes_cache.cache_info().currsize,
        },
        "connections_cache": {
            "hits": get_connections_cache.cache_info().hits,
            "misses": get_connections_cache.cache_info().misses,
            "maxsize": get_connections_cache.cache_info().maxsize,
            "currsize": get_connections_cache.cache_info().currsize,
        },
        "terms_cache": {
            "hits": get_terms_cache.cache_info().hits,
            "misses": get_terms_cache.cache_info().misses,
            "maxsize": get_terms_cache.cache_info().maxsize,
            "currsize": get_terms_cache.cache_info().currsize,
        },
    }

    resp.media = {
        "status": "Cache data loaded successfully",
        "cache_stats": cache_info,
        "lru_cache_info": lru_cache_info,
    }


@api.route(
    "/api/directory-tree",
    response_model=DirectoryTreeResponse,
    examples=OPENAPI_EXAMPLES["directory_tree"],
)
async def api_directory_tree(req, resp):
    folders = []
    files = []

    try:
        for item in sorted(DATA_DIR.iterdir()):
            if item.name.startswith(".") or item.name in ["__pycache__", "node_modules"]:
                continue

            relative_path = item.relative_to(DATA_DIR)
            url_path = "/" + str(relative_path)

            if item.is_dir():
                display_name = item.name.replace("-", " ").replace("_", " ").title()
                index_file = item / "index.md"
                if index_file.exists():
                    title = get_cached_markdown_title(index_file)
                    if title:
                        display_name = title

                icon_svg = generate_folder_icon(display_name, size=18)
                folders.append({
                    "name": item.name,
                    "path": url_path,
                    "is_dir": True,
                    "icon": icon_svg,
                })
            elif item.suffix == ".md" and item.name != "index.md":
                display_name = item.stem
                title = get_cached_markdown_title(item)
                if title:
                    display_name = title

                icon_svg = generate_unique_svg_icon(display_name, size=18)
                files.append({
                    "name": item.stem,
                    "path": url_path.replace(".md", ""),
                    "is_dir": False,
                    "icon": icon_svg,
                })
    except (PermissionError, OSError):
        pass

    items = folders + files
    resp.media = {"items": items}


@api.route(
    "/api/themes",
    response_model=ThemesResponse,
    examples=OPENAPI_EXAMPLES["themes"],
)
async def api_themes(req, resp):
    themes_dir = DATA_DIR / "themes"
    items = []
    if themes_dir.is_dir():
        for f in sorted(themes_dir.glob("*.md")):
            if f.name == "index.md":
                continue
            title = get_cached_markdown_title(f) or f.stem.replace("-", " ").replace("_", " ").title()
            icon = generate_unique_svg_icon(title, size=18)
            items.append({"name": title, "path": f"/themes/{f.stem}", "icon": icon})
    resp.media = {"themes": items}


# The OpenAPI spec (/api/schema) and its Swagger UI (/api) are now generated by
# responder from each route's type hints; see the API() constructor above.


@api.route(
    "/api/oembed",
    responses={200: _json_object_response("Provider-specific oEmbed payload.")},
    examples=OPENAPI_EXAMPLES["oembed"],
    response_examples=OPENAPI_ERROR_EXAMPLES["oembed"],
)
async def api_oembed(
    req,
    resp,
    *,
    url: str = Query(
        "",
        description="HTTPS page URL to discover and fetch oEmbed data for.",
        examples=["https://example.com/video"],
    ),
):
    """Proxy oEmbed discovery and fetch to avoid CORS issues."""
    import json
    import re
    import urllib.request

    url = url.strip()
    if not url or not url.startswith("https://"):
        resp.status_code = 400
        resp.media = {"error": "Missing or invalid url parameter"}
        return

    try:
        # Step 1: Discover oEmbed endpoint from the target page.
        r = urllib.request.Request(url, headers={"User-Agent": "kennethreitz.org"})
        res = urllib.request.urlopen(r, timeout=5)
        page_html = res.read().decode("utf-8", errors="replace")

        endpoint = None
        for pattern in [
            r'<link[^>]+type=["\']application/json\+oembed["\'][^>]+href=["\']([^"\']+)["\']',
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+type=["\']application/json\+oembed["\']',
        ]:
            match = re.search(pattern, page_html)
            if match:
                endpoint = match.group(1)
                break

        if not endpoint:
            resp.status_code = 404
            resp.media = {"error": "No oEmbed endpoint found"}
            return

        # Step 2: Fetch oEmbed data from the discovered endpoint.
        r = urllib.request.Request(
            endpoint, headers={"User-Agent": "kennethreitz.org"}
        )
        res = urllib.request.urlopen(r, timeout=5)
        data = json.loads(res.read())

        resp.media = data
    except Exception:
        resp.status_code = 502
        resp.media = {"error": "oEmbed discovery failed"}


# Debian tucks the fortune binary in /usr/games, which isn't on PATH for
# non-login shells; fall back to the full path when shutil.which misses.
_FORTUNE_BIN = shutil.which("fortune") or "/usr/games/fortune"


@api.route(
    "/api/fortune",
    responses={200: _fortune_response("Random fortune text.")},
    examples=OPENAPI_EXAMPLES["fortune"],
    response_examples=OPENAPI_ERROR_EXAMPLES["fortune"],
)
async def api_fortune(
    req,
    resp,
    *,
    offensive: bool = Query(
        False,
        description="Use the optional offensive fortune set when available.",
        examples=[False],
    ),
):
    """Return a random fortune. Pass ?offensive=1 for the potentially offensive set."""

    if not Path(_FORTUNE_BIN).exists():
        resp.status_code = 503
        resp.media = {"error": "fortune command is not installed"}
        return

    cmd = [_FORTUNE_BIN]
    if offensive:
        cmd.append("-o")  # offensive only; -a would mix both sets

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
    except OSError as exc:
        api.log.error("fortune failed to run: %s", exc)
        resp.status_code = 503
        resp.media = {"error": "fortune command failed to run"}
        return

    if proc.returncode != 0:
        err = stderr.decode(errors="replace").strip()
        # Debian bookworm ships no English offensive set, so `fortune -o` finds
        # nothing. Report that cleanly rather than as a generic failure.
        if offensive and "No fortunes found" in err:
            resp.status_code = 404
            resp.media = {"error": "offensive fortunes are not available", "offensive": True}
            return
        api.log.error("fortune exited %s: %s", proc.returncode, err)
        resp.status_code = 500
        resp.media = {"error": "fortune command failed"}
        return

    resp.media = {
        "fortune": stdout.decode("utf-8", errors="replace").strip(),
        "offensive": offensive,
    }


# --- Data file serving ---


@api.route("/data/{path:path}")
async def serve_data_file(req, resp, *, path):
    """Serve static files from the data directory."""
    file_path = (DATA_DIR / path).resolve()
    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        resp.status_code = 403
        return
    if file_path.exists() and file_path.is_file():
        resp.file(str(file_path))
    else:
        resp.status_code = 404


# --- PDF export ---


def _generate_pdf(md_path):
    """Generate PDF bytes from a markdown file. Returns bytes or raises."""
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration

    content_data = render_markdown_file(md_path)
    pdf_html = api.templates.render(
        "pdf.html",
        content=content_data["content"],
        title=content_data["title"],
        metadata=content_data.get("metadata", {}),
        current_year=datetime.now().year,
        reading_time=content_data.get("reading_time"),
        word_count=content_data.get("word_count"),
        unique_icon=content_data.get("unique_icon"),
    )
    font_config = FontConfiguration()
    pdf_buffer = io.BytesIO()
    HTML(string=pdf_html, base_url="https://kennethreitz.org/").write_pdf(
        pdf_buffer, font_config=font_config
    )
    pdf_buffer.seek(0)
    return pdf_buffer.read()


@api.route("/{path:path}.pdf")
async def serve_pdf(req, resp, *, path):
    """Generate and serve a PDF version of content."""
    file_path = DATA_DIR / f"{path}.md"
    if not file_path.exists():
        resp.status_code = 404
        return

    try:
        api.log.info("Generating PDF for /%s", path)
        resp.content = _generate_pdf(file_path)
        resp.headers["Content-Type"] = "application/pdf"
        resp.headers["Content-Disposition"] = f'inline; filename="{path.split("/")[-1]}.pdf"'
    except (ImportError, OSError):
        resp.status_code = 503
        resp.text = "PDF generation requires WeasyPrint"


# --- Legacy URL resolver ---


# Pre-built lookup tables for legacy URL resolution (built once at import time).
_legacy_dirs = {}  # slug -> url
_legacy_files = {}  # stripped_slug -> url


def _build_legacy_index():
    """Build lookup tables from the data directory for fast legacy URL resolution."""
    for match in DATA_DIR.rglob("*/"):
        if (match / "index.md").exists():
            rel = match.relative_to(DATA_DIR)
            _legacy_dirs[match.name] = f"/{rel}"
    for match in DATA_DIR.rglob("*.md"):
        if match.name == "index.md":
            continue
        stem = match.stem
        stripped = re.sub(r"^\d{4}-\d{2}(?:-\d{2})?-", "", stem)
        rel = match.relative_to(DATA_DIR)
        url = f"/{rel.with_suffix('')}"
        _legacy_files[stripped] = url
        _legacy_files[stem] = url


_build_legacy_index()


def _resolve_legacy_url(path):
    """Try to find current content matching a legacy URL pattern.

    Handles:
    - Date-path URLs: essays/2013/01/27/slug -> essays/2013-01-slug
    - Bare slugs: /tattoos -> /photography/tattoos, /slug -> /essays/...-slug
    - Hyphen/underscore normalization
    """
    # Pattern 1: /essays/YYYY/MM/DD/slug or /essays/YYYY/MM/slug
    m = re.match(r"essays/(\d{4})/(\d{2})(?:/\d{2})?/(.+)$", path)
    if m:
        year, month, slug = m.groups()
        normalized = slug.replace("-", "_")
        candidate = DATA_DIR / "essays" / f"{year}-{month}-{normalized}.md"
        if candidate.exists():
            return f"/essays/{year}-{month}-{normalized}"
        # Try fuzzy match on just the slug within that year
        for f in (DATA_DIR / "essays").glob(f"{year}-{month}-*"):
            if normalized in f.stem:
                return f"/essays/{f.stem}"

    # Pattern 2: bare slug — fast lookup in pre-built index
    slug = path.strip("/").split("/")[-1]
    normalized = slug.replace("-", "_")

    # Check directories first
    if slug in _legacy_dirs:
        return _legacy_dirs[slug]
    if normalized in _legacy_dirs:
        return _legacy_dirs[normalized]

    # Check files
    if normalized in _legacy_files:
        return _legacy_files[normalized]
    if slug in _legacy_files:
        return _legacy_files[slug]

    return None


# --- Catch-all route (MUST be last) ---


@api.route("/static/{path:path}")
async def serve_static(req, resp, *, path):
    """Serve static files explicitly."""
    static_path = Path("tuftecms/static") / path
    if static_path.exists() and static_path.is_file():
        resp.file(str(static_path))
        stat = static_path.stat()
        resp.etag = f"{int(stat.st_mtime)}-{stat.st_size}"
        resp.last_modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    else:
        resp.status_code = 404


@api.route("/{path:path}")
async def catch_all(req, resp, *, path):
    """Main content route -- serves markdown files or directories."""
    bot = _detect_bot(req)
    if bot:
        api.log.info("Bot detected: %s crawling /%s", bot, path)

    # Mirror redirect_slashes for the catch-all, which matches everything
    # and would otherwise shadow Responder's built-in trailing-slash redirect.
    if path.endswith("/"):
        api.redirect(resp, "/" + path.rstrip("/"), status_code=307)
        return

    file_path = DATA_DIR / f"{path}.md"
    dir_path = DATA_DIR / path
    index_path = dir_path / "index.md"
    raw_path = DATA_DIR / path

    # Serve raw markdown source
    if path.endswith(".md"):
        source_path = DATA_DIR / path
        if source_path.exists():
            resp.text = source_path.read_text()
            resp.headers["Content-Type"] = "text/plain; charset=utf-8"
            return
        resp.status_code = 404
        return

    # Serve PDF export
    if path.endswith(".pdf"):
        md_path = DATA_DIR / f"{path[:-4]}.md"
        if md_path.exists():
            api.log.info("Generating PDF for /%s", path[:-4])
            try:
                resp.content = _generate_pdf(md_path)
                resp.headers["Content-Type"] = "application/pdf"
                resp.headers["Content-Disposition"] = f'inline; filename="{path.split("/")[-1]}"'
            except (ImportError, OSError):
                resp.status_code = 503
                resp.text = "PDF generation requires WeasyPrint"
            return
        resp.status_code = 404
        return

    # Serve raw files (images, etc.) directly from data directory
    if raw_path.exists() and raw_path.is_file():
        resp.file(str(raw_path))
        return

    # Serve markdown file
    if file_path.exists():
        api.log.info("Serving content: /%s", path)
        content_data = _cached_render(file_path)

        # article:published_time from the dated filename; modified from mtime.
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", file_path.stem)
        published_iso = date_match.group(1) if date_match else None
        modified_iso = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d")

        # Detect themes for essays, and gather related essays from shared themes
        article_themes = []
        related_posts = []
        if path.startswith("essays/"):
            themes_data = get_themes_cache().get("themes", {})
            essay_url = f"/essays/{file_path.stem}"
            candidates = {}
            for theme_name, theme_info in themes_data.items():
                articles = theme_info.get("articles", [])
                if not any(a.get("url") == essay_url for a in articles):
                    continue
                article_themes.append({"name": theme_name})
                for article in articles:
                    url = article.get("url")
                    if url == essay_url:
                        continue
                    entry = candidates.setdefault(url, {"post": article, "shared": 0})
                    entry["shared"] += 1
            # Most shared themes first, then most recent
            ranked = sorted(
                candidates.values(),
                key=lambda c: (c["shared"], c["post"].get("date") or ""),
                reverse=True,
            )
            related_posts = [c["post"] for c in ranked[:3]]

        # Chronological neighbors for essays (blog cache is newest-first)
        newer_post = older_post = None
        if path.startswith("essays/"):
            essay_url = f"/essays/{file_path.stem}"
            posts = get_blog_cache().get("posts", [])
            for i, p in enumerate(posts):
                if p["url"] == essay_url:
                    newer_post = posts[i - 1] if i > 0 else None
                    older_post = posts[i + 1] if i + 1 < len(posts) else None
                    break

        respond_html(resp, "post.html", req, f"/{path}",
            content=content_data["content"],
            title=content_data["title"],
            metadata=content_data.get("metadata", {}),
            github_file=f"data/{path}.md",
            reading_time=content_data.get("reading_time"),
            word_count=content_data.get("word_count"),
            tags=content_data.get("tags", []),
            series_posts=content_data.get("series_posts", []),
            series_name=content_data.get("series_name"),
            unique_icon=content_data.get("unique_icon"),
            article_themes=article_themes,
            related_posts=related_posts,
            newer_post=newer_post,
            older_post=older_post,
            published_iso=published_iso,
            modified_iso=modified_iso,
        )
        return

    # Serve directory with index.md
    if dir_path.is_dir() and index_path.exists():
        api.log.info("Serving directory: /%s", path)
        content_data = _cached_render(index_path)
        items = get_directory_structure(dir_path)

        # Check for image gallery
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
        image_items = []
        for item in items:
            if not item["is_dir"]:
                item_path = DATA_DIR / item["url_path"].lstrip("/")
                if item_path.suffix.lower() in image_extensions:
                    item["is_image"] = True
                    item["static_path"] = item["url_path"]
                    item["is_data_file"] = True
                    if item_path.suffix.lower() in {".jpg", ".jpeg"}:
                        item["exif"] = extract_exif_data(item_path)
                    else:
                        item["exif"] = {}
                    image_items.append(item)
                else:
                    item["is_image"] = False
            else:
                item["is_image"] = False

        is_image_gallery = len(image_items) > 0

        if is_image_gallery:
            parts = path.split("/")
            breadcrumb = []
            current = ""
            for part in parts:
                current = f"{current}/{part}" if current else part
                breadcrumb.append({
                    "name": part.replace("-", " ").replace("_", " ").title(),
                    "path": f"/{current}",
                })

            folder_icon = generate_folder_icon(content_data["title"], size=32)

            respond_html(resp, "directory.html", req, f"/{path}",
                items=items,
                image_items=image_items,
                is_image_gallery=True,
                title=content_data["title"],
                current_path=f"/{path}",
                breadcrumb=breadcrumb,
                current_year=datetime.now().year,
                folder_icon=folder_icon,
                index_content={"content": content_data["content"]},
                content_position="top",
            )
        else:
            respond_html(resp, "post.html", req, f"/{path}",
                content=content_data["content"],
                title=content_data["title"],
                metadata=content_data.get("metadata", {}),
                items=items,
                current_path=f"/{path}",
                github_file=f"data/{path}/index.md",
                current_year=datetime.now().year,
                reading_time=content_data.get("reading_time"),
                word_count=content_data.get("word_count"),
                unique_icon=content_data.get("unique_icon"),
            )
        return

    # Serve directory listing (no index.md)
    if dir_path.is_dir():
        api.log.info("Serving directory listing: /%s", path)
        items = get_directory_structure(dir_path)
        title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()

        parts = path.split("/")
        breadcrumb = []
        current = ""
        for part in parts:
            current = f"{current}/{part}" if current else part
            breadcrumb.append({
                "name": part.replace("-", " ").replace("_", " ").title(),
                "path": f"/{current}",
            })

        folder_icon = generate_folder_icon(title, size=32)

        respond_html(resp, "directory.html", req, f"/{path}",
            items=items,
            title=title,
            current_path=f"/{path}",
            breadcrumb=breadcrumb,
            current_year=datetime.now().year,
            folder_icon=folder_icon,
        )
        return

    # Try to resolve legacy URLs before giving up
    redirect_to = _resolve_legacy_url(path)
    if redirect_to:
        api.log.info("Legacy redirect: /%s -> %s", path, redirect_to)
        resp.status_code = 301
        resp.headers["Location"] = redirect_to
        return

    # Nothing found
    api.log.warning("Not found: /%s", path)
    resp.status_code = 404
    resp.html = render("error.html", req, f"/{path}",
        title="Not Found",
        current_year=datetime.now().year,
        error_code=404,
        error_message="Page not found.",
        suggestions=_suggest_pages(path),
    )


# Keep the OpenAPI docs focused on the JSON API: hide the HTML page and asset
# routes (and the catch-alls) so only /api/* endpoints appear in the spec.
# `_include_in_schema` is the same flag the `@api.route(..., include_in_schema=)`
# decorator sets; we apply it in bulk so new page routes stay out by default.
for _route in api.router.routes:
    _endpoint = getattr(_route, "endpoint", None)
    if _endpoint is None or (getattr(_route, "route", "") or "").startswith("/api/"):
        continue
    try:
        _endpoint._include_in_schema = False
    except (AttributeError, TypeError):
        # responder's own internal routes are bound methods with no __dict__;
        # they're already kept out of the schema, so nothing to do.
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    try:
        api.run(port=port, server="granian")
    except KeyboardInterrupt:
        pass

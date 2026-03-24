"""Responder-based engine for kennethreitz.org."""

import responder

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
    find_related_posts,
    find_adjacent_posts,
    extract_intelligent_date,
    generate_folder_icon,
    get_cached_markdown_title,
)
from tuftecms.utils.svg_icons import generate_unique_svg_icon
from tuftecms.blueprints.content import extract_exif_data

from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib
import html
import io
import logging
import random
import re
import textwrap
import os

DATA_DIR = Path("data")

api = responder.API(
    templates_dir="tuftecms/templates",
    static_dir="tuftecms/static",
    static_route="/static",
    enable_logging=True,
)

# Suppress access logging for static assets.
class _StaticFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return "/static/" not in msg and not msg.endswith((".js", ".css", ".ico", ".png", ".woff2"))

logging.getLogger("responder.access").addFilter(_StaticFilter())
logging.getLogger("fontTools.subset").setLevel(logging.WARNING)

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


def render(template, req, path="/", **kwargs):
    """Render a template with common context."""
    kwargs.setdefault("current_year", datetime.now().year)
    kwargs.setdefault("current_path", path)
    kwargs["request"] = RequestWrapper(req, path)
    kwargs["config"] = _config
    kwargs.setdefault("pdf_available", _pdf_available)
    return api.templates.render(template, **kwargs)


# --- Cache for OG images ---
_og_image_cache = {}


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
    recent_posts = blog_data.get("posts", [])[:6]
    resp.html = render("homepage.html", req, "/",
        title="Home",
        recent_posts=recent_posts,
    )


@api.route("/health")
async def health(req, resp):
    resp.media = {"status": "healthy", "timestamp": datetime.now().isoformat()}


@api.route("/random")
async def random_post(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])
    if posts:
        chosen = random.choice(posts)
        api.log.info("Redirecting to random post: %s", chosen["url"])
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        api.redirect(resp, chosen["url"])
    else:
        resp.status_code = 404


@api.route("/search")
async def search_page(req, resp):
    resp.html = render("search.html", req, "/search",
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

    resp.html = render("sitemap.html", req, "/sitemap",
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
        "/docs",
        "/docs/getting-started",
        "/docs/content-structure",
        "/docs/sidenotes",
        "/docs/customization",
        "/docs/deployment",
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


async def _rss_feed(req, resp):
    """Generate RSS feed."""
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    recent_posts = posts[:20]

    rss_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    rss_lines.append('<rss version="2.0">')
    rss_lines.append("    <channel>")
    rss_lines.append("        <title>Kenneth Reitz</title>")
    rss_lines.append("        <link>https://kennethreitz.org</link>")
    rss_lines.append(
        "        <description>Creator of Requests, Pipenv, and other tools. Writing about technology, consciousness, and human-centered design.</description>"
    )
    rss_lines.append("        <language>en-us</language>")
    rss_lines.append(
        f'        <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>'
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


# --- OG image route ---


@api.route("/og-image/{path:path}.png")
async def og_image(req, resp, *, path):
    """Generate a dynamic Open Graph image for a post."""
    from PIL import Image, ImageDraw, ImageFont

    api.log.info("Generating OG image for /%s", path)

    # Check cache
    cache_key = path
    if cache_key in _og_image_cache:
        resp.content = _og_image_cache[cache_key]
        resp.headers["Content-Type"] = "image/png"
        resp.headers["Cache-Control"] = "public, max-age=86400"
        return

    # Resolve the post title from the markdown file
    file_path = DATA_DIR / f"{path}.md"
    title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()
    subtitle = None

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
        font_small = ImageFont.truetype(
            str(font_dir / "et-book-roman-line-figures" / "et-book-roman-line-figures.ttf"),
            22,
        )
    except (OSError, IOError):
        font_italic = ImageFont.load_default()
        font_roman = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw accent line
    draw.rectangle([80, 180, 200, 184], fill="#333333")

    # Word-wrap and draw title
    max_chars = 28 if len(title) > 28 else 40
    wrapped = textwrap.wrap(title, width=max_chars)
    y_pos = 210
    for line in wrapped[:3]:
        draw.text((80, y_pos), line, font=font_italic, fill="#111111")
        y_pos += 72

    # Draw subtitle/date if available
    if subtitle:
        draw.text((80, y_pos + 20), subtitle, font=font_roman, fill="#666666")

    # Draw separator line
    draw.rectangle([80, height - 110, width - 80, height - 108], fill="#dddddd")

    # Draw site URL
    draw.text((80, height - 85), "kennethreitz.org", font=font_small, fill="#999999")

    # Draw author name on right
    author_text = "Kenneth Reitz"
    bbox = draw.textbbox((0, 0), author_text, font=font_small)
    author_width = bbox[2] - bbox[0]
    draw.text((width - 80 - author_width, height - 85), author_text, font=font_small, fill="#999999")

    # Draw decorative circles
    cx, cy = 1060, 300
    for r_val, c in [(50, "#dddddd"), (35, "#cccccc"), (20, "#bbbbbb")]:
        draw.ellipse([cx - r_val, cy - r_val, cx + r_val, cy + r_val], outline=c, width=2)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill="#999999")

    # Export to PNG bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    png_bytes = buf.getvalue()

    # Cache it
    _og_image_cache[cache_key] = png_bytes

    resp.content = png_bytes
    resp.headers["Content-Type"] = "image/png"
    resp.headers["Cache-Control"] = "public, max-age=86400"


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

    resp.html = render("archive.html", req, "/archive",
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

    resp.html = render("archive-by-length.html", req, "/archive/by-length",
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

    resp.html = render("sidenotes.html", req, "/archive/sidenotes",
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

    resp.html = render("outlines.html", req, "/archive/outlines",
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

    resp.html = render("quotes.html", req, "/archive/quotes",
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

    resp.html = render("connections.html", req, "/archive/connections",
        articles=articles,
        total_outgoing=stats.get("total_outgoing", 0),
        total_incoming=stats.get("total_incoming", 0),
        title="Connections",
    )


@api.route("/archive/terms")
async def terms(req, resp):
    terms_data = get_terms_cache()
    stats = terms_data.get("stats", {})
    resp.html = render("terms.html", req, "/archive/terms",
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

    sorted_themes = sorted(themes.items(), key=lambda x: len(x[1]), reverse=True)

    resp.html = render("themes.html", req, "/archive/themes",
        themes=dict(sorted_themes),
        total_themes=stats.get("total_themes", 0),
        total_occurrences=stats.get("total_occurrences", 0),
        title="Themes",
    )


@api.route("/archive/graph")
async def graph(req, resp):
    resp.html = render("graph.html", req, "/archive/graph",
        title="Knowledge Graph",
    )


@api.route("/archive/graph/data")
async def graph_data(req, resp):
    connections_data = get_connections_cache()
    blog_data = get_blog_cache()

    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    nodes = []
    edges = []
    node_ids = set()

    for source, targets in connections_data.get("outgoing", {}).items():
        source_id = source.replace("data/", "").replace(".md", "")
        source_url = (
            f"/essays/{source_id.split('/')[-1]}"
            if "essays" in source_id
            else f"/{source_id}"
        )

        if source_id not in node_ids:
            post_data = post_lookup.get(source_url, {})

            nodes.append({
                "id": source_id,
                "title": post_data.get(
                    "title", source_id.split("/")[-1].replace("-", " ").title()
                ),
                "label": post_data.get(
                    "title", source_id.split("/")[-1].replace("-", " ").title()
                ),
                "url": source_url,
                "category": source_id.split("/")[0] if "/" in source_id else "root",
                "group": source_id.split("/")[0] if "/" in source_id else "root",
            })
            node_ids.add(source_id)

        for target_info in targets:
            target_url = target_info["url"].strip("/")
            if target_url:
                target_id = target_url.replace("/", "_")

                if target_id not in node_ids:
                    target_post_data = post_lookup.get(f"/{target_url}", {})

                    nodes.append({
                        "id": target_id,
                        "title": target_post_data.get(
                            "title",
                            target_url.split("/")[-1].replace("-", " ").title(),
                        ),
                        "label": target_post_data.get(
                            "title",
                            target_url.split("/")[-1].replace("-", " ").title(),
                        ),
                        "url": f"/{target_url}",
                        "category": (
                            target_url.split("/")[0]
                            if "/" in target_url
                            else "root"
                        ),
                        "group": (
                            target_url.split("/")[0]
                            if "/" in target_url
                            else "root"
                        ),
                    })
                    node_ids.add(target_id)

                edges.append({
                    "source": source_id,
                    "target": target_id,
                    "label": target_info["text"],
                    "link_text": target_info["text"],
                })

    resp.media = {"nodes": nodes, "edges": edges}


# --- Directory route ---


@api.route("/directory")
async def directory(req, resp):
    items = get_directory_structure(DATA_DIR)
    resp.html = render("directory.html", req, "/directory",
        items=items,
        current_path="/",
        breadcrumb=[],
        title="Directory",
    )


# --- API routes ---


@api.route("/api/blog")
async def api_blog(req, resp):
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    posts_data = [
        {
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "unique_icon": post.get("unique_icon", ""),
        }
        for post in posts
    ]

    resp.media = {"posts": posts_data, "total": len(posts_data)}


@api.route("/api/search")
async def api_search(req, resp):
    query = req.params.get("q", "").strip()
    api.log.info("Search query: %s", query)

    if len(query) < 2:
        resp.media = {
            "query": query,
            "results": [],
            "error": "Query must be at least 2 characters long",
        }
        return

    results = []
    query_lower = query.lower()

    # Search all markdown files across the entire data directory
    for md_file in DATA_DIR.rglob("*.md"):
        if md_file.name == "index.md":
            # Include index files but use parent dir for URL
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
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break

        score = 0
        matches = []

        # Search in title (highest weight)
        if query_lower in title.lower():
            score += 10
            matches.append("title")

        # Search in content (medium weight)
        if query_lower in raw.lower():
            score += 5
            matches.append("content")

        if score > 0:
            snippet = ""
            if "content" in matches:
                raw_lower = raw.lower()
                query_index = raw_lower.find(query_lower)
                if query_index != -1:
                    start = max(0, query_index - 100)
                    end = min(len(raw), query_index + len(query) + 100)
                    snippet = raw[start:end].strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(raw):
                        snippet = snippet + "..."

            # Determine section from path
            parts = md_file.relative_to(DATA_DIR).parts
            section = parts[0] if len(parts) > 1 else ""

            if md_file.name == "index.md":
                icon = generate_folder_icon(title, size=18)
            else:
                icon = generate_unique_svg_icon(title, size=18)

            results.append({
                "title": title,
                "url": url,
                "snippet": snippet,
                "section": section,
                "score": score,
                "matches": matches,
                "unique_icon": icon,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:50]

    resp.media = {"query": query, "results": results, "total": len(results)}


@api.route("/api/icon/{article_path}")
async def api_icon(req, resp, *, article_path):
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


@api.route("/api/debug-cache")
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


@api.route("/api/directory-tree")
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


@api.route("/api/themes")
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


# --- Data file serving ---


@api.route("/data/{path:path}")
async def serve_data_file(req, resp, *, path):
    """Serve static files from the data directory."""
    file_path = DATA_DIR / path
    if file_path.exists() and file_path.is_file():
        resp.file(str(file_path))
    else:
        resp.status_code = 404


# --- PDF export ---


@api.route("/{path:path}.pdf")
async def serve_pdf(req, resp, *, path):
    """Generate and serve a PDF version of content."""
    file_path = DATA_DIR / f"{path}.md"
    if not file_path.exists():
        resp.status_code = 404
        return

    try:
        from weasyprint import HTML
        from weasyprint.text.fonts import FontConfiguration
    except (ImportError, OSError):
        resp.status_code = 503
        resp.text = "PDF generation requires WeasyPrint"
        return

    api.log.info("Generating PDF for /%s", path)
    content_data = render_markdown_file(file_path)
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

    resp.content = pdf_buffer.read()
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f'inline; filename="{path.split("/")[-1]}.pdf"'


# --- Legacy URL resolver ---


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

    # Pattern 2: bare slug — search for matching directories and files
    slug = path.strip("/").split("/")[-1]
    normalized = slug.replace("-", "_")

    # Check for directory match anywhere in data/
    for match in DATA_DIR.rglob("*/"):
        if match.name == slug or match.name == normalized:
            rel = match.relative_to(DATA_DIR)
            if (match / "index.md").exists():
                return f"/{rel}"

    # Check for file match by slug anywhere in data/
    for match in DATA_DIR.rglob("*.md"):
        stem = match.stem
        # Strip date prefix for comparison
        stripped = re.sub(r"^\d{4}-\d{2}-", "", stem)
        if stripped == normalized or stripped == slug:
            rel = match.relative_to(DATA_DIR)
            return f"/{rel.with_suffix('')}"

    return None


# --- Catch-all route (MUST be last) ---


@api.route("/static/{path:path}")
async def serve_static(req, resp, *, path):
    """Serve static files explicitly."""
    static_path = Path("tuftecms/static") / path
    if static_path.exists() and static_path.is_file():
        resp.file(str(static_path))
    else:
        resp.status_code = 404


@api.route("/{path:path}")
async def catch_all(req, resp, *, path):
    """Main content route -- serves markdown files or directories."""
    bot = _detect_bot(req)
    if bot:
        api.log.info("Bot detected: %s crawling /%s", bot, path)
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
                resp.content = pdf_buffer.read()
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
        content_data = render_markdown_file(file_path)

        # Find related and adjacent posts for essays
        related_posts = []
        prev_post = None
        next_post = None
        if path.startswith("essays/"):
            blog_data = get_blog_cache()
            posts = blog_data.get("posts", [])
            related_posts = find_related_posts(file_path)
            prev_post, next_post = find_adjacent_posts(file_path)

        resp.html = render("post.html", req, f"/{path}",
            content=content_data["content"],
            title=content_data["title"],
            metadata=content_data.get("metadata", {}),
            reading_time=content_data.get("reading_time"),
            word_count=content_data.get("word_count"),
            tags=content_data.get("tags", []),
            series_posts=content_data.get("series_posts", []),
            series_name=content_data.get("series_name"),
            unique_icon=content_data.get("unique_icon"),
            related_posts=related_posts,
            prev_post=prev_post,
            next_post=next_post,
        )
        return

    # Serve directory with index.md
    if dir_path.is_dir() and index_path.exists():
        api.log.info("Serving directory: /%s", path)
        content_data = render_markdown_file(index_path)
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

            resp.html = render("directory.html", req, f"/{path}",
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
            resp.html = render("post.html", req, f"/{path}",
                content=content_data["content"],
                title=content_data["title"],
                metadata=content_data.get("metadata", {}),
                items=items,
                current_path=f"/{path}",
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

        resp.html = render("directory.html", req, f"/{path}",
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
    )


# Warm caches on startup
@api.on_event("startup")
async def warm_caches():
    import threading
    def _warm():
        api.log.info("Starting background cache warming...")
        try:
            get_blog_cache()
            from tuftecms.core.cache import (
                get_sidenotes_cache, get_outlines_cache,
                get_quotes_cache, get_connections_cache,
                get_terms_cache, get_themes_cache,
            )
            get_sidenotes_cache()
            get_outlines_cache()
            get_quotes_cache()
            get_connections_cache()
            get_terms_cache()
            get_themes_cache()
            api.log.info("Cache warming complete!")
        except Exception as e:
            api.log.error("Cache warming failed: %s", e)
    threading.Thread(target=_warm, daemon=True).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    api.run(port=port)

"""Feeds blueprint for RSS and sitemap generation."""

from flask import Blueprint, render_template, Response
from datetime import datetime

feeds_bp = Blueprint("feeds", __name__)


@feeds_bp.route("/sitemap")
def sitemap():
    """Generate HTML sitemap."""
    from ..core.cache import get_blog_cache

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

    return render_template(
        "sitemap.html",
        sitemap_data=sitemap_data,
        total_items=total_items,
        current_year=datetime.now().year,
        title="Sitemap",
    )


@feeds_bp.route("/sitemap.xml")
def sitemap_xml():
    """Generate XML sitemap."""
    from ..core.cache import get_blog_cache

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Build URL list
    urls = []

    # Add homepage
    urls.append(
        {
            "url": "https://kennethreitz.org/",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "priority": "1.0",
        }
    )

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
        urls.append(
            {
                "url": f"https://kennethreitz.org{page}",
                "lastmod": datetime.now().strftime("%Y-%m-%d"),
                "priority": "0.8",
            }
        )

    # Add blog posts
    for post in posts:
        urls.append(
            {
                "url": f"https://kennethreitz.org{post['url']}",
                "lastmod": post["date_str"],
                "priority": "0.9",
            }
        )

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

    return Response(xml_content, mimetype="application/xml")


@feeds_bp.route("/feed.xml")
@feeds_bp.route("/rss.xml")
def rss_feed():
    """Generate RSS feed."""
    from ..core.cache import get_blog_cache
    import html

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Get the 20 most recent posts
    recent_posts = posts[:20]

    # Generate RSS
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

        # Format date for RSS (RFC 822 format)
        pub_date = post["pub_date"]
        rss_date = pub_date.strftime("%a, %d %b %Y %H:%M:%S %z") if pub_date else ""
        if rss_date:
            rss_lines.append(f"            <pubDate>{rss_date}</pubDate>")

        rss_lines.append("        </item>")

    rss_lines.append("    </channel>")
    rss_lines.append("</rss>")

    rss_content = "\n".join(rss_lines)

    return Response(rss_content, mimetype="application/xml")

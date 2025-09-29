"""Main blueprint for basic routes."""

from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage using the homepage.html template."""
    return render_template(
        "homepage.html", current_year=datetime.now().year, title="Home"
    )


@main_bp.route("/health")
def health_check():
    """Simple health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@main_bp.route("/search")
def search_page():
    """Search page with interactive search functionality."""
    return render_template(
        "search.html", current_year=datetime.now().year, title="Search"
    )


@main_bp.route("/archive/sidenotes")
def sidenotes():
    """Display all sidenotes from all posts."""
    from ..core.cache import get_sidenotes_cache, get_blog_cache

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
            # Get article info from first sidenote
            first_sidenote = sidenotes_list[0]
            article_title = first_sidenote.get("title", "Unknown")
            article_url = first_sidenote.get("url", "#")

            # Get additional metadata from blog cache if available
            post_data = post_lookup.get(article_url, {})

            articles.append(
                {
                    "title": article_title,
                    "url": article_url,
                    "sidenotes": sidenotes_list,
                    "category": "essays",
                    "date": post_data.get("pub_date"),
                    "unique_icon": post_data.get("unique_icon"),
                }
            )
            total_sidenotes += len(sidenotes_list)

    # Sort articles by publish date (newest first)
    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    return render_template(
        "sidenotes.html",
        articles=articles,
        total_count=total_sidenotes,
        current_year=datetime.now().year,
        title="Sidenotes",
    )


@main_bp.route("/archive/outlines")
def outlines():
    """Display outlines (headings) from all posts."""
    from ..core.cache import get_outlines_cache, get_blog_cache

    cache_data = get_outlines_cache()
    blog_data = get_blog_cache()

    # Create lookup for post metadata
    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    # Convert cache format to template format
    articles = []
    total_headings = 0

    for _, headings_list in cache_data.get("outlines", {}).items():
        if headings_list:
            # Get article info from first heading
            first_heading = headings_list[0]
            article_title = first_heading.get("title", "Unknown")
            article_url = first_heading.get("url", "#")

            # Get additional metadata from blog cache if available
            post_data = post_lookup.get(article_url, {})

            articles.append(
                {
                    "title": article_title,
                    "url": article_url,
                    "headings": headings_list,
                    "category": "essays",
                    "date": post_data.get("pub_date"),
                    "unique_icon": post_data.get("unique_icon"),
                }
            )
            total_headings += len(headings_list)

    # Sort articles by publish date (newest first)
    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    return render_template(
        "outlines.html",
        articles=articles,
        total_count=total_headings,
        current_year=datetime.now().year,
        title="Outlines",
    )


@main_bp.route("/archive/quotes")
def quotes():
    """Display quotes (blockquotes) from all posts."""
    from ..core.cache import get_quotes_cache, get_blog_cache

    cache_data = get_quotes_cache()
    blog_data = get_blog_cache()

    # Create lookup for post metadata
    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    # Convert cache format to template format
    articles = []
    total_quotes = 0

    for _, quotes_list in cache_data.get("quotes", {}).items():
        if quotes_list:
            # Get article info from first quote
            first_quote = quotes_list[0]
            article_title = first_quote.get("title", "Unknown")
            article_url = first_quote.get("url", "#")

            # Get additional metadata from blog cache if available
            post_data = post_lookup.get(article_url, {})

            articles.append(
                {
                    "title": article_title,
                    "url": article_url,
                    "quotes": quotes_list,
                    "category": "essays",
                    "date": post_data.get("pub_date"),
                    "unique_icon": post_data.get("unique_icon"),
                }
            )
            total_quotes += len(quotes_list)

    # Sort articles by publish date (newest first)
    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    return render_template(
        "quotes.html",
        articles=articles,
        total_count=total_quotes,
        current_year=datetime.now().year,
        title="Quotes",
    )


@main_bp.route("/archive/connections")
def connections():
    """Display cross-references and connections between posts."""
    from ..core.cache import get_connections_cache, get_blog_cache

    cache_data = get_connections_cache()
    blog_data = get_blog_cache()

    # Create lookup for post metadata
    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    # Convert cache format to template format
    articles = []
    outgoing_data = cache_data.get("outgoing", {})
    incoming_data = cache_data.get("incoming", {})
    stats = cache_data.get("stats", {})

    # Process outgoing connections
    for file_path, connections_list in outgoing_data.items():
        if connections_list:
            # Get article info from file path
            file_stem = Path(file_path).stem
            article_url = f"/essays/{file_stem}"

            # Get additional metadata from blog cache if available
            post_data = post_lookup.get(article_url, {})
            article_title = post_data.get("title", file_stem.replace("-", " ").title())

            # Get incoming connections for this article
            incoming_connections = incoming_data.get(article_url, [])

            # Format outgoing connections
            formatted_outgoing = []
            for conn in connections_list:
                formatted_outgoing.append(
                    {"link_text": conn["text"], "target_url": conn["url"]}
                )

            # Format incoming connections
            formatted_incoming = []
            for conn in incoming_connections:
                formatted_incoming.append(
                    {
                        "link_text": conn["text"],
                        "source_url": conn.get("source_url", "#"),
                        "context": conn.get("context", ""),
                    }
                )

            articles.append(
                {
                    "title": article_title,
                    "url": article_url,
                    "outgoing_connections": formatted_outgoing,
                    "incoming_connections": formatted_incoming,
                    "category": "essays",
                    "date": post_data.get("pub_date"),
                    "unique_icon": post_data.get("unique_icon"),
                }
            )

    # Sort articles by publish date (newest first)
    articles.sort(key=lambda x: x.get("date") or datetime.min, reverse=True)

    return render_template(
        "connections.html",
        articles=articles,
        total_outgoing=stats.get("total_outgoing", 0),
        total_incoming=stats.get("total_incoming", 0),
        current_year=datetime.now().year,
        title="Connections",
    )


@main_bp.route("/archive/graph")
def graph():
    """Interactive graph visualization of content connections."""
    return render_template(
        "graph.html", current_year=datetime.now().year, title="Knowledge Graph"
    )


@main_bp.route("/archive/graph/data")
def graph_data():
    """Provide data for the interactive graph visualization."""
    from ..core.cache import get_connections_cache, get_blog_cache
    import json

    connections_data = get_connections_cache()
    blog_data = get_blog_cache()

    # Create lookup for post metadata
    post_lookup = {
        f"/essays/{post['path'].split('/')[-1]}": post
        for post in blog_data.get("posts", [])
    }

    nodes = []
    edges = []
    node_ids = set()

    # Create nodes and edges from connections
    for source, targets in connections_data.get("outgoing", {}).items():
        # Add source node
        source_id = source.replace("data/", "").replace(".md", "")
        source_url = (
            f"/essays/{source_id.split('/')[-1]}"
            if "essays" in source_id
            else f"/{source_id}"
        )

        if source_id not in node_ids:
            # Get metadata from blog cache if available
            post_data = post_lookup.get(source_url, {})

            nodes.append(
                {
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
                }
            )
            node_ids.add(source_id)

        # Add target nodes and edges
        for target_info in targets:
            target_url = target_info["url"].strip("/")
            if target_url:
                target_id = target_url.replace("/", "_")  # Create unique ID for target

                if target_id not in node_ids:
                    # Get metadata for target if it's an essay
                    target_post_data = post_lookup.get(f"/{target_url}", {})

                    nodes.append(
                        {
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
                        }
                    )
                    node_ids.add(target_id)

                edges.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "label": target_info["text"],
                        "link_text": target_info["text"],  # For template compatibility
                    }
                )

    return jsonify({"nodes": nodes, "edges": edges})


@main_bp.route("/archive/terms")
def terms():
    """Display index of terms used across the site."""
    from ..core.cache import get_terms_cache

    terms_data = get_terms_cache()
    stats = terms_data.get("stats", {})
    return render_template(
        "terms.html",
        terms=terms_data.get("terms", {}),
        total_terms=stats.get("total_terms", 0),
        total_occurrences=stats.get("total_references", 0),
        current_year=datetime.now().year,
        title="Index of Terms",
    )


@main_bp.route("/archive")
def archive():
    """Display the blog archive."""
    from ..core.cache import get_blog_cache
    from collections import defaultdict

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Group posts by year
    grouped_posts = defaultdict(list)
    for post in posts:
        year = post["pub_date"].year
        grouped_posts[year].append(post)

    # Sort years in descending order
    grouped_posts = dict(sorted(grouped_posts.items(), reverse=True))

    return render_template(
        "archive.html",
        posts=posts,
        grouped_posts=grouped_posts,
        archive_title="Complete Archive of kennethreitz.org",
        current_year=datetime.now().year,
        title="Archive",
    )


@main_bp.route("/archive/by-length")
def archive_by_length():
    """Display blog archive sorted by reading time."""
    from ..core.cache import get_blog_cache

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

    return render_template(
        "archive-by-length.html",
        posts=posts,
        grouped_posts=grouped_posts,
        archive_title="By Reading Time",
        current_year=datetime.now().year,
        title="Archive by Reading Time",
    )


@main_bp.route("/archive/themes")
def themes_archive():
    """Display themes index."""
    from ..core.cache import get_themes_cache

    themes_data = get_themes_cache()
    themes = themes_data.get("themes", {})
    stats = themes_data.get("stats", {})
    
    # Sort themes by number of articles
    sorted_themes = sorted(themes.items(), key=lambda x: len(x[1]), reverse=True)
    
    return render_template(
        "themes.html",
        themes=dict(sorted_themes),
        total_themes=stats.get("total_themes", 0),
        total_occurrences=stats.get("total_occurrences", 0),
        current_year=datetime.now().year,
        title="Themes",
    )


@main_bp.route("/directory")
def directory():
    """File browser for the data directory."""
    from pathlib import Path
    from ..utils.content import get_directory_structure

    DATA_DIR = Path("data")
    items = get_directory_structure(DATA_DIR)

    return render_template(
        "directory.html",
        items=items,
        current_path="/",
        breadcrumb=[],
        current_year=datetime.now().year,
        title="Directory",
    )

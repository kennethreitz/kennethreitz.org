"""Content blueprint for serving markdown files and static content."""

import os
import re
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    jsonify,
    redirect,
    render_template,
    send_from_directory,
)

content_bp = Blueprint("content", __name__)

DATA_DIR = Path("data")
STATIC_DIR = Path("static")


@content_bp.route("/static/")
@content_bp.route("/static/<path:path>/")
def browse_static_directory(path=""):
    """Browse static directory contents."""
    from datetime import datetime
    from flask import request

    static_path = STATIC_DIR / path

    if not static_path.exists() or not static_path.is_dir():
        abort(404)

    items = []
    for item in sorted(static_path.iterdir()):
        if item.name.startswith("."):
            continue

        item_url = f"/static/{path}/{item.name}" if path else f"/static/{item.name}"
        if item.is_dir():
            item_url += "/"

        items.append(
            {
                "name": item.name,
                "url": item_url,
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else None,
                "modified": datetime.fromtimestamp(item.stat().st_mtime),
            }
        )

    # Check if JSON is requested
    if request.headers.get("Accept") == "application/json":
        return jsonify(
            {"path": f"/static/{path}" if path else "/static", "items": items}
        )

    # Return HTML directory listing
    breadcrumb = []
    if path:
        parts = path.split("/")
        current = "/static"
        for part in parts:
            current = f"{current}/{part}"
            breadcrumb.append({"name": part, "path": current})

    return render_template(
        "directory.html",
        items=items,
        current_path=f"/static/{path}" if path else "/static",
        breadcrumb=breadcrumb,
        current_year=datetime.now().year,
        title=f"Static Directory: {path}" if path else "Static Directory",
    )


@content_bp.route("/static/data/<path:path>")
def serve_data_file(path):
    """Serve static files from the data directory."""
    from flask import make_response

    file_path = DATA_DIR / path

    if not file_path.exists() or not file_path.is_file():
        abort(404)

    # Serve the file with proper caching headers
    response = make_response(send_from_directory(DATA_DIR, path))

    # Add caching headers for static assets
    if file_path.suffix.lower() in [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".ico",
    ]:
        # Cache images for 7 days
        response.headers["Cache-Control"] = "public, max-age=604800"
    else:
        # Cache other static files for 1 hour
        response.headers["Cache-Control"] = "public, max-age=3600"

    return response


@content_bp.route("/<path:path>")
def serve_content(path):
    """Serve content from markdown files or directories."""
    from ..core.markdown import render_markdown_file
    from ..utils.content import get_directory_structure
    from datetime import datetime

    # Remove trailing slash for consistency
    path = path.rstrip("/")

    # Check for various file patterns
    file_path = DATA_DIR / f"{path}.md"
    dir_path = DATA_DIR / path
    index_path = dir_path / "index.md"

    # Handle directories
    if dir_path.is_dir():
        # Check for index.md in the directory
        if index_path.exists():
            content_data = render_markdown_file(index_path)

            # Get items in the directory for display
            items = get_directory_structure(dir_path)

            # Calculate themes for this article
            article_themes = []
            try:
                import re
                raw_content = index_path.read_text()
                content_lower = raw_content.lower()
                
                theme_patterns = {
                    "consciousness": "Exploring the nature of awareness, identity, and the recursive loop between code and mind.",
                    "technology": "Human-first approaches to building tools that serve rather than exploit.",
                    "mental health": "Reality-checking, debugging consciousness, and navigating neurodivergence.",
                    "programming": "Code as meditation, API design as compassion, and software as spiritual practice.",
                    "AI": "Human-AI collaboration as partnership, not replacement—augmenting consciousness through digital minds.",
                    "human centered": "Designing systems that adapt to human mental models rather than forcing humans to adapt.",
                    "recursive": "The feedback loops between programmer consciousness, code patterns, and collective impact.",
                    "spiritual": "Technical work as contemplative practice—finding transcendence in systematicity.",
                    "mindful": "Bringing awareness and intentionality to the craft of building software.",
                    "contemplative": "Reflective approaches to technology, blending Eastern wisdom with Western pragmatism.",
                }
                
                for theme_name, description in theme_patterns.items():
                    regex_pattern = theme_name.replace(" ", r"[- ]")
                    if re.search(regex_pattern, content_lower):
                        article_themes.append({
                            "name": theme_name,
                            "description": description
                        })
            except Exception as e:
                print(f"Error calculating themes: {e}")
            
            return render_template(
                "post.html",
                content=content_data["content"],
                title=content_data["title"],
                metadata=content_data["metadata"],
                items=items,
                current_year=datetime.now().year,
                reading_time=content_data.get("reading_time"),
                word_count=content_data.get("word_count"),
                tags=content_data.get("tags", []),
                series_posts=content_data.get("series_posts", []),
                series_name=content_data.get("series_name"),
                unique_icon=content_data.get("unique_icon"),
                article_themes=article_themes,
            )
        else:
            # Show directory listing
            items = get_directory_structure(dir_path)

            # Create breadcrumb navigation
            parts = path.split("/")
            breadcrumb = []
            current = ""
            for part in parts:
                current = f"{current}/{part}" if current else part
                breadcrumb.append(
                    {
                        "name": part.replace("-", " ").replace("_", " ").title(),
                        "path": f"/{current}",
                    }
                )

            # Get title from directory name
            title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()

            return render_template(
                "directory.html",
                items=items,
                current_path=f"/{path}",
                breadcrumb=breadcrumb,
                current_year=datetime.now().year,
                title=title,
            )

    # Handle markdown files
    elif file_path.exists():
        content_data = render_markdown_file(file_path)

        # Check if this is a special page
        is_special_page = any(
            path.startswith(prefix)
            for prefix in [
                "essays/",
                "software/",
                "poetry/",
                "personality/",
                "reactions/",
            ]
        )

        # Get related posts if it's an essay
        related_posts = []
        adjacent_posts = {"prev": None, "next": None}
        if "essays/" in path:
            from ..utils.content import find_related_posts, find_adjacent_posts

            related_posts = find_related_posts(file_path)
            adjacent_posts = find_adjacent_posts(file_path)

        # Calculate themes for this article
        article_themes = []
        try:
            import re
            raw_content = file_path.read_text()
            content_lower = raw_content.lower()
            
            theme_patterns = {
                "consciousness": "Exploring the nature of awareness, identity, and the recursive loop between code and mind.",
                "technology": "Human-first approaches to building tools that serve rather than exploit.",
                "mental health": "Reality-checking, debugging consciousness, and navigating neurodivergence.",
                "programming": "Code as meditation, API design as compassion, and software as spiritual practice.",
                "AI": "Human-AI collaboration as partnership, not replacement—augmenting consciousness through digital minds.",
                "human centered": "Designing systems that adapt to human mental models rather than forcing humans to adapt.",
                "recursive": "The feedback loops between programmer consciousness, code patterns, and collective impact.",
                "spiritual": "Technical work as contemplative practice—finding transcendence in systematicity.",
                "mindful": "Bringing awareness and intentionality to the craft of building software.",
                "contemplative": "Reflective approaches to technology, blending Eastern wisdom with Western pragmatism.",
            }
            
            for theme_name, description in theme_patterns.items():
                regex_pattern = theme_name.replace(" ", r"[- ]")
                if re.search(regex_pattern, content_lower):
                    article_themes.append({
                        "name": theme_name,
                        "description": description
                    })
        except Exception as e:
            print(f"Error calculating themes: {e}")

        return render_template(
            "post.html",
            content=content_data["content"],
            title=content_data["title"],
            metadata=content_data["metadata"],
            current_year=datetime.now().year,
            reading_time=content_data.get("reading_time"),
            word_count=content_data.get("word_count"),
            tags=content_data.get("tags", []),
            series_posts=content_data.get("series_posts", []),
            series_name=content_data.get("series_name"),
            unique_icon=content_data.get("unique_icon"),
            related_posts=related_posts,
            adjacent_posts=adjacent_posts,
            article_themes=article_themes,
        )

    # Check for redirects or alternative paths
    # For example, handle /archive/2025 -> show year archive
    if path.startswith("archive/"):
        parts = path.split("/")
        if len(parts) == 2 and parts[1].isdigit():
            year = int(parts[1])
            return archive_year(year)
        elif len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            year = int(parts[1])
            month = int(parts[2])
            return archive_month(year, month)

    # Handle random redirects
    if path == "random":
        return random_post()
    elif path.startswith("random/"):
        collection = path.split("/", 1)[1]
        return random_from_collection(collection)

    # File not found
    abort(404)


def archive_year(year):
    """Display archive for a specific year."""
    from ..core.cache import get_blog_cache
    from datetime import datetime

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Filter posts by year
    year_posts = [p for p in posts if p["pub_date"].year == year]

    return render_template(
        "archive.html",
        posts=year_posts,
        year=year,
        current_year=datetime.now().year,
        title=f"Archive - {year}",
    )


def archive_month(year, month):
    """Display archive for a specific month."""
    from ..core.cache import get_blog_cache
    from datetime import datetime
    import calendar

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    # Filter posts by year and month
    month_posts = [
        p for p in posts if p["pub_date"].year == year and p["pub_date"].month == month
    ]

    month_name = calendar.month_name[month]

    return render_template(
        "archive.html",
        posts=month_posts,
        year=year,
        month=month,
        month_name=month_name,
        current_year=datetime.now().year,
        title=f"Archive - {month_name} {year}",
    )


def random_post():
    """Redirect to a random post."""
    from ..core.cache import get_blog_cache
    import random

    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])

    if posts:
        random_post = random.choice(posts)
        return redirect(random_post["url"])
    else:
        abort(404)


def random_from_collection(collection):
    """Redirect to a random post from a specific collection."""
    from pathlib import Path
    import random

    # Handle special case for personality
    if collection in ["personality", "personality/"]:
        collection_path = DATA_DIR / "personality"
    else:
        collection_path = DATA_DIR / collection

    if not collection_path.exists() or not collection_path.is_dir():
        abort(404)

    # Get all markdown files in the collection
    md_files = list(collection_path.glob("**/*.md"))
    md_files = [f for f in md_files if f.name != "index.md"]

    if md_files:
        random_file = random.choice(md_files)
        # Create URL path
        relative_path = random_file.relative_to(DATA_DIR)
        url_path = "/" + str(relative_path.with_suffix(""))
        return redirect(url_path)
    else:
        abort(404)

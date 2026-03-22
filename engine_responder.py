"""Responder-based engine for kennethreitz.org."""

import responder

from tuftecms.core.markdown import render_markdown_file
from tuftecms.core.cache import get_blog_cache, clear_all_caches
from tuftecms.utils.content import (
    get_directory_structure,
    find_related_posts,
    find_adjacent_posts,
    extract_intelligent_date,
    generate_folder_icon,
)
from tuftecms.blueprints.content import extract_exif_data

from pathlib import Path
from datetime import datetime
import random
import os

DATA_DIR = Path("data")

api = responder.API(
    templates_dir="tuftecms/templates",
    static_dir="tuftecms/static",
    static_route="/static",
)

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


def render(template, req, path="/", **kwargs):
    """Render a template with common context."""
    kwargs.setdefault("current_year", datetime.now().year)
    kwargs.setdefault("current_path", path)
    kwargs["request"] = RequestWrapper(req, path)
    kwargs["config"] = _config
    return api.templates.render(template, **kwargs)


# --- Routes ---


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
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        api.redirect(resp, chosen["url"])
    else:
        resp.status_code = 404


@api.route("/data/{path}")
async def serve_data_file(req, resp, *, path):
    """Serve static files from the data directory."""
    file_path = DATA_DIR / path
    if file_path.exists() and file_path.is_file():
        resp.file(str(file_path))
    else:
        resp.status_code = 404


@api.route("/{path:path}")
async def catch_all(req, resp, *, path):
    """Main content route — serves markdown files or directories."""
    file_path = DATA_DIR / f"{path}.md"
    dir_path = DATA_DIR / path
    index_path = dir_path / "index.md"

    # Serve markdown file
    if file_path.exists():
        content_data = render_markdown_file(file_path)

        # Find related and adjacent posts for essays
        related_posts = []
        prev_post = None
        next_post = None
        if path.startswith("essays/"):
            blog_data = get_blog_cache()
            posts = blog_data.get("posts", [])
            related_posts = find_related_posts(file_path, posts)
            prev_post, next_post = find_adjacent_posts(file_path, posts)

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
                breadcrumb.append(
                    {
                        "name": part.replace("-", " ").replace("_", " ").title(),
                        "path": f"/{current}",
                    }
                )

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
        items = get_directory_structure(dir_path)
        title = path.split("/")[-1].replace("-", " ").replace("_", " ").title()

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

    # Nothing found
    resp.status_code = 404
    resp.html = render("error.html", req, f"/{path}",
            title="Not Found",
        current_year=datetime.now().year,
        error_code=404,
        error_message="Page not found.",
    )


if __name__ == "__main__":
    # Warm caches
    import threading

    def warm():
        get_blog_cache()

    threading.Thread(target=warm, daemon=True).start()

    port = int(os.environ.get("PORT", 8001))
    api.run(port=port)

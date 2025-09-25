"""API blueprint for search and data endpoints."""

from pathlib import Path

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)

DATA_DIR = Path("data")


@api_bp.route("/search")
def search():
    """API endpoint for search functionality."""
    query = request.args.get("q", "").strip()

    if len(query) < 2:
        return jsonify(
            {
                "query": query,
                "results": [],
                "error": "Query must be at least 2 characters long",
            }
        )

    # TODO: Implement actual search functionality
    # For now, return empty results
    return jsonify({"query": query, "results": [], "total": 0})


@api_bp.route("/icon/<path:article_path>")
def get_icon(article_path):
    """Generate and return an SVG icon for a given article."""
    from pathlib import Path

    from ..utils.content import get_cached_markdown_title
    from ..utils.svg_icons import generate_unique_svg_icon

    # Try to get the actual article title for better icon generation
    title = article_path  # fallback to path

    # Check if this is a markdown file path
    data_path = Path("data") / f"{article_path}.md"
    if data_path.exists():
        # Extract the actual title from the markdown file
        cached_title = get_cached_markdown_title(data_path)
        if cached_title:
            title = cached_title
    else:
        # For directory paths, clean up the path for title
        title = article_path.split("/")[-1].replace("-", " ").replace("_", " ").title()

    # Generate icon based on actual title
    icon_data = generate_unique_svg_icon(title, size=24)

    return jsonify({"success": True, "path": article_path, "icon": icon_data})


@api_bp.route("/debug-cache")
def debug_cache():
    """Debug endpoint to view cache status."""
    # TODO: Implement cache debugging
    return jsonify({"status": "Cache debugging not yet implemented", "cache_keys": []})

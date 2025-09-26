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

    # Get cached blog data for search
    from ..core.cache import get_blog_cache
    
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])
    
    # Search through posts
    results = []
    query_lower = query.lower()
    
    for post in posts:
        score = 0
        matches = []
        
        # Search in title (highest weight)
        if query_lower in post.get("title", "").lower():
            score += 10
            matches.append("title")
            
        # Search in content (medium weight)
        content = post.get("content", "")
        if query_lower in content.lower():
            score += 5
            matches.append("content")
            
        # Search in excerpt (medium weight)
        excerpt = post.get("excerpt", "")
        if query_lower in excerpt.lower():
            score += 3
            matches.append("excerpt")
            
        # Search in tags if they exist (low weight)
        tags = post.get("tags", [])
        for tag in tags:
            if query_lower in tag.lower():
                score += 2
                matches.append("tags")
                break
        
        if score > 0:
            # Extract a snippet around the match
            snippet = ""
            if "content" in matches:
                # Find the query in content and extract surrounding text
                content_lower = content.lower()
                query_index = content_lower.find(query_lower)
                if query_index != -1:
                    start = max(0, query_index - 100)
                    end = min(len(content), query_index + len(query) + 100)
                    snippet = content[start:end].strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(content):
                        snippet = snippet + "..."
            elif "excerpt" in matches:
                snippet = excerpt
            else:
                snippet = post.get("excerpt", "")
            
            results.append({
                "title": post.get("title", ""),
                "url": post.get("url", ""),
                "excerpt": post.get("excerpt", ""),
                "snippet": snippet,
                "date": post.get("date_str", ""),
                "score": score,
                "matches": matches
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit to top 50 results
    results = results[:50]
    
    return jsonify({
        "query": query,
        "results": results,
        "total": len(results)
    })


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

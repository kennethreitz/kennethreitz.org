"""API blueprint for search and data endpoints."""

from pathlib import Path

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)

DATA_DIR = Path("data")


@api_bp.route("/blog")
def blog():
    """API endpoint to get all blog posts for autocomplete."""
    from ..core.cache import get_blog_cache
    
    blog_data = get_blog_cache()
    posts = blog_data.get("posts", [])
    
    # Return minimal data needed for autocomplete
    posts_data = [
        {
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "unique_icon": post.get("unique_icon", "")
        }
        for post in posts
    ]
    
    return jsonify({
        "posts": posts_data,
        "total": len(posts_data)
    })


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
                "matches": matches,
                "unique_icon": post.get("unique_icon", "")
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

    from ..utils.content import get_cached_markdown_title, generate_folder_icon
    from ..utils.svg_icons import generate_unique_svg_icon

    # Try to get the actual article title for better icon generation
    title = article_path  # fallback to path
    is_folder = False

    # Check if this is a markdown file path
    data_path = Path("data") / f"{article_path}.md"
    if data_path.exists():
        # Extract the actual title from the markdown file
        cached_title = get_cached_markdown_title(data_path)
        if cached_title:
            title = cached_title
    else:
        # Check if it's a directory with index.md
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
            # For paths without files, clean up the path for title
            title = article_path.split("/")[-1].replace("-", " ").replace("_", " ").title()

    # Generate icon based on type and title
    if is_folder:
        icon_data = generate_folder_icon(title, size=24)
    else:
        icon_data = generate_unique_svg_icon(title, size=24)

    return jsonify({"success": True, "path": article_path, "icon": icon_data})


@api_bp.route("/debug-cache")
def debug_cache():
    """Debug endpoint to view cache status."""
    from ..core.cache import (
        get_blog_cache,
        get_connections_cache,
        get_outlines_cache,
        get_quotes_cache,
        get_sidenotes_cache,
        get_terms_cache,
    )

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

    return jsonify(
        {
            "status": "Cache data loaded successfully",
            "cache_stats": cache_info,
            "lru_cache_info": lru_cache_info,
        }
    )


@api_bp.route("/directory-tree")
def directory_tree():
    """API endpoint to get flat directory listing."""
    from ..utils.content import get_cached_markdown_title, generate_folder_icon
    from ..utils.svg_icons import generate_unique_svg_icon

    folders = []
    files = []

    try:
        for item in sorted(DATA_DIR.iterdir()):
            # Skip hidden files and special directories
            if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules']:
                continue

            # Build URL path
            relative_path = item.relative_to(DATA_DIR)
            url_path = '/' + str(relative_path)

            if item.is_dir():
                # For folders, try to get title from index.md
                display_name = item.name
                index_file = item / 'index.md'
                if index_file.exists():
                    title = get_cached_markdown_title(index_file)
                    if title:
                        display_name = title

                icon_svg = generate_folder_icon(display_name, size=18)
                folders.append({
                    'name': item.name,
                    'path': url_path,
                    'is_dir': True,
                    'icon': icon_svg
                })
            elif item.suffix == '.md' and item.name != 'index.md':
                # For markdown files, get title from the file
                display_name = item.stem
                title = get_cached_markdown_title(item)
                if title:
                    display_name = title

                icon_svg = generate_unique_svg_icon(display_name, size=18)
                files.append({
                    'name': item.stem,
                    'path': url_path.replace('.md', ''),
                    'is_dir': False,
                    'icon': icon_svg
                })
    except (PermissionError, OSError):
        pass

    # Folders first, then files
    items = folders + files
    return jsonify({'items': items})

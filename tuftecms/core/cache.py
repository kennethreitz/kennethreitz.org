"""Cache management for TufteCMS."""

import re
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path("data")

# Simple in-memory cache
_cache_store = {}


def clear_cache():
    """Clear all caches."""
    global _cache_store
    _cache_store.clear()
    get_blog_cache.cache_clear()
    get_sidenotes_cache.cache_clear()
    get_outlines_cache.cache_clear()
    get_quotes_cache.cache_clear()
    get_connections_cache.cache_clear()
    get_terms_cache.cache_clear()


@lru_cache(maxsize=1)
def get_blog_cache():
    """Get cached blog posts data."""
    if "blog_posts" in _cache_store:
        return _cache_store["blog_posts"]

    blog_posts = []

    # Get all markdown files from essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                # Import here to avoid circular imports
                from ..core.markdown import render_markdown_file
                from ..utils.content import extract_intelligent_date

                # Render the markdown file to get metadata
                content_data = render_markdown_file(file_path)

                # Extract date
                date_obj = extract_intelligent_date(file_path, content_data)

                if date_obj:
                    # Extract excerpt and full content
                    raw_content = file_path.read_text()
                    excerpt = extract_excerpt(raw_content)

                    # Get clean content for search (remove markdown formatting but keep text)
                    clean_content = clean_content_for_search(raw_content)

                    blog_posts.append(
                        {
                            "title": content_data["title"],
                            "path": f"/essays/{file_path.stem}",
                            "url": f"/essays/{file_path.stem}",
                            "file_path": str(file_path),
                            "pub_date": date_obj,
                            "date_str": date_obj.strftime("%Y-%m-%d"),
                            "excerpt": excerpt,
                            "description": excerpt,
                            "content": clean_content,
                            "word_count": content_data.get("word_count", 0),
                            "category": "essays",
                            "unique_icon": content_data.get("unique_icon"),
                        }
                    )
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

    # Sort by date (newest first)
    blog_posts.sort(key=lambda x: x["pub_date"], reverse=True)

    result = {"posts": blog_posts, "stats": {"total_posts": len(blog_posts)}}

    _cache_store["blog_posts"] = result
    return result


def clean_content_for_search(content):
    """Clean content for search indexing - preserve text, remove formatting."""
    # Remove front matter
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
    # Remove title (first # line)
    content = re.sub(r"^# .+?$", "", content, flags=re.MULTILINE)
    # Remove date lines
    content = re.sub(r"^\*[A-Za-z]+ \d{4}\*\s*$", "", content, flags=re.MULTILINE)
    # Remove ALL HTML tags (including sidenotes) but keep the text content
    content = re.sub(r"<[^>]+>", "", content)
    # Remove code blocks but keep content
    content = re.sub(r"```[a-z]*\n(.*?)\n```", r"\1", content, flags=re.DOTALL)
    # Remove inline code but keep content
    content = re.sub(r"`([^`]+)`", r"\1", content)
    # Remove images
    content = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", content)
    # Remove links but keep text
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)
    # Remove markdown formatting chars but keep text
    content = re.sub(r"[*_#]", "", content)
    # Clean up multiple whitespace
    content = re.sub(r"\s+", " ", content)

    return content.strip()


def extract_excerpt(content, max_words=50):
    """Simple excerpt extraction."""
    # Use the same cleaning function for consistency
    clean_content = clean_content_for_search(content)

    # Get first meaningful paragraph
    lines = [line.strip() for line in clean_content.split("\n") if line.strip()]
    for line in lines:
        if len(line) > 20:  # Skip very short lines
            words = line.split()[:max_words]
            excerpt = " ".join(words)
            if len(words) == max_words:
                excerpt += "..."
            return excerpt

    return ""


@lru_cache(maxsize=1)
def get_sidenotes_cache():
    """Get cached sidenotes data."""
    if "sidenotes" in _cache_store:
        return _cache_store["sidenotes"]

    sidenotes_data = {}
    total_sidenotes = 0
    total_articles = 0

    # Process all markdown files in essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                # Import here to avoid circular imports
                from ..core.markdown import render_markdown_file

                content_data = render_markdown_file(file_path)
                html_content = content_data["content"]

                # Extract sidenotes with their IDs
                # Pattern matches the full sidenote structure: input + span
                sidenote_pattern = r'<input[^>]*id="([^"]*)"[^>]*class="margin-toggle"[^>]*/>.*?<span class="sidenote">(.*?)</span>'
                sidenotes = re.findall(sidenote_pattern, html_content, re.DOTALL)

                if sidenotes:
                    file_key = str(file_path)
                    sidenotes_data[file_key] = []

                    for sidenote_id, sidenote_content in sidenotes:
                        clean_sidenote = re.sub(
                            r"<[^>]+>", "", sidenote_content
                        ).strip()
                        if clean_sidenote:
                            sidenotes_data[file_key].append(
                                {
                                    "text": clean_sidenote,
                                    "html": sidenote_content.strip(),
                                    "id": sidenote_id,
                                    "title": content_data["title"],
                                    "url": f"/essays/{file_path.stem}",
                                }
                            )
                            total_sidenotes += 1

                    if sidenotes_data[file_key]:
                        total_articles += 1

            except Exception as e:
                print(f"Error processing sidenotes in {file_path}: {e}")
                continue

    result = {
        "sidenotes": sidenotes_data,
        "stats": {"total_sidenotes": total_sidenotes, "total_articles": total_articles},
    }

    _cache_store["sidenotes"] = result
    return result


@lru_cache(maxsize=1)
def get_outlines_cache():
    """Get cached outlines data."""
    if "outlines" in _cache_store:
        return _cache_store["outlines"]

    outlines_data = {}
    total_headings = 0
    total_articles = 0

    # Process all markdown files in essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                # Import here to avoid circular imports
                from ..core.markdown import render_markdown_file

                content_data = render_markdown_file(file_path)
                html_content = content_data["content"]

                # Extract outlines (headings)
                heading_pattern = r"(<h([1-6])[^>]*>.*?</h[1-6]>)"
                headings = re.findall(heading_pattern, html_content)

                if headings:
                    file_key = str(file_path)
                    outlines_data[file_key] = []

                    for full_tag, level in headings:
                        # Extract just the inner content for text
                        inner_pattern = r"<h[1-6][^>]*>(.*?)</h[1-6]>"
                        inner_match = re.search(inner_pattern, full_tag)
                        if inner_match:
                            clean_heading = re.sub(
                                r"<[^>]+>", "", inner_match.group(1)
                            ).strip()
                            if clean_heading and not clean_heading.startswith("fn:"):
                                outlines_data[file_key].append(
                                    {
                                        "level": int(level),
                                        "text": clean_heading,
                                        "html": full_tag.strip(),
                                        "title": content_data["title"],
                                        "url": f"/essays/{file_path.stem}",
                                    }
                                )
                                total_headings += 1

                    if outlines_data[file_key]:
                        total_articles += 1

            except Exception as e:
                print(f"Error processing outlines in {file_path}: {e}")
                continue

    result = {
        "outlines": outlines_data,
        "stats": {"total_headings": total_headings, "total_articles": total_articles},
    }

    _cache_store["outlines"] = result
    return result


@lru_cache(maxsize=1)
def get_quotes_cache():
    """Get cached quotes data."""
    if "quotes" in _cache_store:
        return _cache_store["quotes"]

    quotes_data = {}
    total_quotes = 0
    total_articles = 0

    # Process all markdown files in essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                # Import here to avoid circular imports
                from ..core.markdown import render_markdown_file

                content_data = render_markdown_file(file_path)
                html_content = content_data["content"]

                # Extract quotes (blockquotes)
                quote_pattern = r"<blockquote[^>]*>(.*?)</blockquote>"
                quotes = re.findall(quote_pattern, html_content, re.DOTALL)

                if quotes:
                    file_key = str(file_path)
                    quotes_data[file_key] = []

                    for quote in quotes:
                        clean_quote = re.sub(r"<[^>]+>", "", quote).strip()
                        if clean_quote:
                            quotes_data[file_key].append(
                                {
                                    "text": clean_quote,
                                    "html": quote.strip(),
                                    "title": content_data["title"],
                                    "url": f"/essays/{file_path.stem}",
                                }
                            )
                            total_quotes += 1

                    if quotes_data[file_key]:
                        total_articles += 1

            except Exception as e:
                print(f"Error processing quotes in {file_path}: {e}")
                continue

    result = {
        "quotes": quotes_data,
        "stats": {"total_quotes": total_quotes, "total_articles": total_articles},
    }

    _cache_store["quotes"] = result
    return result


@lru_cache(maxsize=1)
def get_connections_cache():
    """Get cached connections data."""
    if "connections" in _cache_store:
        return _cache_store["connections"]

    connections_outgoing = {}
    connections_incoming = {}
    total_outgoing = 0
    total_incoming = 0

    # Process all markdown files in essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                raw_content = file_path.read_text()

                # Extract connections (cross-references)
                connection_pattern = r"\[([^\]]+)\](\(/[^)]+\))"
                connections = re.findall(connection_pattern, raw_content)

                if connections:
                    file_key = str(file_path)
                    connections_outgoing[file_key] = []

                    for link_text, link_url in connections:
                        # Remove parentheses from URL
                        clean_url = link_url.strip("()")
                        # Include all internal links (starting with /) except external ones
                        if clean_url.startswith("/") and not clean_url.startswith("//"):
                            connections_outgoing[file_key].append(
                                {
                                    "text": link_text,
                                    "url": clean_url,
                                    "target_file": clean_url,
                                }
                            )
                            total_outgoing += 1

                            # Track incoming references
                            if clean_url not in connections_incoming:
                                connections_incoming[clean_url] = []
                            connections_incoming[clean_url].append(
                                {
                                    "text": link_text,
                                    "source_file": file_key,
                                    "context": link_text,
                                    "source_url": f"/essays/{file_path.stem}",
                                }
                            )
                            total_incoming += 1

            except Exception as e:
                print(f"Error processing connections in {file_path}: {e}")
                continue

    result = {
        "outgoing": connections_outgoing,
        "incoming": connections_incoming,
        "stats": {
            "total_outgoing": total_outgoing,
            "total_incoming": total_incoming,
            "total_connections": total_outgoing + total_incoming,
            "total_articles": len(connections_outgoing),
        },
    }

    _cache_store["connections"] = result
    return result


@lru_cache(maxsize=1)
def get_terms_cache():
    """Get cached terms data."""
    if "terms" in _cache_store:
        return _cache_store["terms"]

    terms_data = {}
    total_term_occurrences = 0

    # Process all markdown files in essays directory
    essays_dir = DATA_DIR / "essays"
    if essays_dir.exists():
        for file_path in essays_dir.glob("*.md"):
            if file_path.name == "index.md":
                continue

            try:
                # Import here to avoid circular imports
                from ..core.markdown import render_markdown_file

                content_data = render_markdown_file(file_path)
                raw_content = file_path.read_text()
                article_title = content_data["title"]

                # Extract terms for index
                # Simple approach: extract words that appear in multiple files
                words = re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", raw_content)
                for word in set(words):
                    if len(word) > 3 and word not in [
                        "This",
                        "That",
                        "They",
                        "When",
                        "Where",
                        "What",
                        "Which",
                        "HTTP",
                        "HTML",
                        "JSON",
                        "API",
                    ]:
                        if word not in terms_data:
                            terms_data[word] = []
                        terms_data[word].append(
                            {
                                "file": str(file_path),
                                "context": word,
                                "url": f"/essays/{file_path.stem}",
                                "title": article_title,
                            }
                        )
                        total_term_occurrences += 1

            except Exception as e:
                print(f"Error processing terms in {file_path}: {e}")
                continue

    # Filter terms to only include ones that appear in multiple files
    filtered_terms = {
        term: refs
        for term, refs in terms_data.items()
        if len(set(ref["file"] for ref in refs)) >= 2
    }

    final_terms = {}
    total_occurrences = 0
    for term, refs in sorted(filtered_terms.items()):
        # Group by file to get counts per article
        file_counts = {}
        for ref in refs:
            file_path = ref["file"]
            if file_path not in file_counts:
                file_counts[file_path] = 0
            file_counts[file_path] += 1

        articles = []
        for file_path, count in file_counts.items():
            # Get the URL and title for this file
            matching_refs = [ref for ref in refs if ref["file"] == file_path]
            if matching_refs:
                ref = matching_refs[0]
                articles.append(
                    {"url": ref["url"], "title": ref["title"], "count": count}
                )

        if articles:
            final_terms[term] = {
                "articles": articles,
                "total_count": sum(file_counts.values()),
                "article_count": len(articles),
            }
            total_occurrences += sum(file_counts.values())

    result = {
        "terms": final_terms,
        "stats": {
            "total_terms": len(final_terms),
            "total_references": total_occurrences,
        },
    }

    _cache_store["terms"] = result
    return result


def get_themes_cache():
    """Get cached themes data."""
    # TODO: Implement actual themes
    return {}


def clear_all_caches():
    """Clear all LRU caches and in-memory cache store."""
    global _cache_store

    # Clear the in-memory cache store
    _cache_store.clear()

    # Clear all LRU caches
    get_blog_cache.cache_clear()
    get_sidenotes_cache.cache_clear()
    get_outlines_cache.cache_clear()
    get_quotes_cache.cache_clear()
    get_connections_cache.cache_clear()
    get_terms_cache.cache_clear()

    print("🧹 All caches cleared!")


class CacheManager:
    """Manager for application caching."""

    def __init__(self):
        """Initialize cache manager."""
        self._cache = {}

    def get(self, key):
        """Get value from cache."""
        return self._cache.get(key)

    def set(self, key, value):
        """Set value in cache."""
        self._cache[key] = value

    def clear(self):
        """Clear all cache."""
        self._cache.clear()

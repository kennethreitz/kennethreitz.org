"""Content processing utilities."""

import hashlib
import html
import re
from collections import Counter
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from .svg_icons import generate_unique_svg_icon


TOKEN_PATTERN = re.compile(r"[a-z]{4,}")
STOPWORDS = {
    "this",
    "that",
    "with",
    "have",
    "from",
    "will",
    "there",
    "their",
    "which",
    "about",
    "when",
    "where",
    "because",
    "while",
    "these",
    "those",
    "into",
    "would",
    "could",
    "should",
    "after",
    "before",
    "being",
    "over",
    "under",
    "only",
    "other",
    "some",
    "such",
    "very",
    "than",
    "each",
    "many",
    "more",
    "most",
    "much",
    "just",
    "like",
    "also",
    "make",
    "made",
    "used",
    "using",
    "through",
    "since",
    "still",
    "even",
    "well",
    "back",
    "them",
    "then",
    "they",
    "been",
    "here",
    "your",
    "every",
    "within",
    "around",
    "across",
}


@lru_cache(maxsize=1000)
def get_cached_markdown_title(file_path):
    """Extract and cache the H1 title from a markdown file for performance."""
    try:
        # Convert Path object to string for caching compatibility
        file_path_str = str(file_path)

        # Quick check - if file was modified recently, we might want to skip cache
        # For now, let's just extract title efficiently
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(1000)  # Only read first 1000 chars to find title

        # Look for first H1 markdown title
        title_match = re.search(r"^#\s+(.+?)$", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

        # Fallback: look for HTML H1 if markdown was already rendered
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE)
        if title_match:
            # Remove HTML tags from title
            title = re.sub(r"<[^>]+>", "", title_match.group(1))
            return html.unescape(title).strip()

        return None
    except:
        return None


@lru_cache(maxsize=500)
def generate_folder_icon(title, size=24):
    """Generate a folder icon with unique accent color based on title."""
    hash_obj = hashlib.md5(title.encode())
    hash_bytes = hash_obj.digest()

    # Generate accent color
    hue = (hash_bytes[0] * 360) // 256
    saturation = 60 + (hash_bytes[1] * 20) // 256  # 60-80%
    lightness = 45 + (hash_bytes[2] * 20) // 256  # 45-65%

    accent_color = f"hsl({hue}, {saturation}%, {lightness}%)"
    folder_base = "#e8e8e8"

    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="folder_grad_{abs(hash(title)) % 1000}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{folder_base}"/>
                <stop offset="100%" stop-color="{accent_color}"/>
            </linearGradient>
        </defs>
        <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2h-8l-2-2z" 
              fill="url(#folder_grad_{abs(hash(title)) % 1000})" 
              stroke="{accent_color}" 
              stroke-width="0.5"/>
        <circle cx="18" cy="7" r="2" fill="{accent_color}" opacity="0.8"/>
    </svg>"""

    import base64

    svg_b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_b64}"


def get_directory_structure(path):
    """Get the directory structure for a given path."""
    from pathlib import Path

    DATA_DIR = Path("data")
    items = []
    if not path.exists() or not path.is_dir():
        return items

    # Separate directories and files for better organization
    dirs = []
    files = []

    for item in sorted(path.iterdir(), reverse=True):
        if (
            item.name.startswith(".")
            or item.name.lower() == "index.md"
            or item.name.endswith(".bak")
        ):
            continue

        # Create display name without extension for files
        display_name = item.stem if item.is_file() and item.suffix else item.name
        display_name = display_name.replace("-", " ").replace("_", " ").title()

        # Create clean URL path without .md extension
        if item.is_dir():
            url_path = "/" + str(item.relative_to(DATA_DIR)) + "/"
        elif item.suffix == ".md":
            # Remove .md extension for clean URLs
            relative_path = str(item.relative_to(DATA_DIR))
            url_path = "/" + relative_path[:-3]  # Remove .md extension
        else:
            url_path = "/" + str(item.relative_to(DATA_DIR))

        # Extract date from markdown files
        file_date = None
        if item.is_file() and item.suffix == ".md":
            try:
                with open(item, "r", encoding="utf-8") as f:
                    # Read first few lines to find date
                    for i, line in enumerate(f):
                        if i > 10:  # Only check first 10 lines
                            break
                        # Look for date patterns like *January 2009* or *2014*
                        date_match = re.match(
                            r"^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$", line.strip()
                        )
                        if date_match:
                            file_date = date_match.group(1)
                            break
            except:
                pass

        # Generate unique SVG icon based on actual content title for consistency
        icon_title = display_name  # Default to filename-based display name

        # For directories, try to get title from index.md
        if item.is_dir():
            try:
                index_file = item / "index.md"
                if index_file.exists():
                    cached_title = get_cached_markdown_title(index_file)
                    if cached_title:
                        icon_title = cached_title
                        # Also update display_name to use the actual title
                        display_name = cached_title
            except:
                # Fallback to filename-based display name if parsing fails
                pass

        # For markdown files, try to extract the actual H1 title from content
        if item.is_file() and item.suffix == ".md":
            try:
                # Use cached title extraction for performance
                cached_title = get_cached_markdown_title(item)
                if cached_title:
                    icon_title = cached_title
                    # Also update display_name to use the actual title
                    display_name = cached_title
            except:
                # Fallback to filename-based display name if parsing fails
                pass

        if item.is_dir():
            unique_icon = generate_folder_icon(icon_title, size=32)
        else:
            unique_icon = generate_unique_svg_icon(icon_title, size=32)

        item_info = {
            "name": item.name,
            "display_name": display_name,
            "path": str(item.relative_to(DATA_DIR)),
            "url_path": url_path,
            "is_dir": item.is_dir(),
            "is_markdown": item.suffix == ".md",
            "is_image": item.suffix.lower()
            in [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "size": item.stat().st_size if item.is_file() else None,
            "created": datetime.fromtimestamp(item.stat().st_ctime),
            "modified": datetime.fromtimestamp(item.stat().st_mtime),
            "file_date": file_date,  # Date extracted from file content
            "file_type": item.suffix.lower() if item.is_file() else "directory",
            "static_path": (
                f"/static/data/{item.relative_to(DATA_DIR)}"
                if not item.is_dir()
                else None
            ),
            "unique_icon": unique_icon,  # Generated SVG icon
        }

        if item.is_dir():
            dirs.append(item_info)
        else:
            files.append(item_info)

    # Return directories first, then files
    return dirs + files


def calculate_reading_time(text):
    """Calculate estimated reading time based on word count."""
    # Remove HTML tags for more accurate word count
    clean_text = re.sub(r"<[^>]+>", "", text)
    # Average reading speed is 200-250 words per minute, using 225 as middle ground
    word_count = len(clean_text.split())
    reading_time = max(1, round(word_count / 225))  # Minimum 1 minute
    return reading_time, word_count


def extract_tags_from_content(content, metadata, file_path):
    """Extract tags from content and metadata for categorization."""
    tags = set()

    # Only use explicitly defined tags from YAML front matter
    if metadata.get("tags"):
        if isinstance(metadata["tags"], list):
            tags.update(tag.lower().strip() for tag in metadata["tags"])
        else:
            tags.update(tag.lower().strip() for tag in str(metadata["tags"]).split(","))

    return list(tags)


def find_series_posts(metadata, current_path):
    """Find all posts in the same series as the current post."""
    import os
    import yaml
    from pathlib import Path

    DATA_DIR = Path("data")
    series_posts = []
    if not metadata.get("series"):
        return series_posts

    series_name = metadata["series"]

    # Search through all markdown files to find posts in the same series
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                file_path = Path(root) / file

                # Skip the current file
                if str(file_path) == str(current_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract metadata
                    yaml_pattern = r"^---\s*\n(.*?)\n---\s*\n"
                    yaml_match = re.match(yaml_pattern, content, re.DOTALL)
                    if yaml_match:
                        post_metadata = yaml.safe_load(yaml_match.group(1)) or {}

                        if post_metadata.get("series") == series_name:
                            # Create URL path for this post
                            relative_path = str(file_path.relative_to(DATA_DIR))
                            url_path = "/" + relative_path[:-3]  # Remove .md

                            # Get title from metadata or filename
                            title = (
                                post_metadata.get("title")
                                or file_path.stem.replace("-", " ").title()
                            )

                            series_posts.append(
                                {
                                    "title": title,
                                    "url": url_path,
                                    "order": post_metadata.get("series_order", 999),
                                    "description": post_metadata.get("description", ""),
                                }
                            )
                except:
                    continue

    # Sort by series_order
    series_posts.sort(key=lambda x: x["order"])
    return series_posts


def extract_intelligent_date(item_path, content_data=None):
    """Extract date intelligently from various sources."""
    from datetime import datetime
    import re

    # PRIORITY 1: Try to extract from filename first (most reliable)
    filename = item_path.name

    # Try full date format first (YYYY-MM-DD) - must have day followed by dash
    date_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", filename)
    if date_match:
        year, month, day = map(int, date_match.groups())
        return datetime(year, month, day)

    # Try year-month format (YYYY-MM) - must NOT have a day after month
    date_match = re.match(r"^(\d{4})-(\d{2})-(?!\d{2})", filename)
    if date_match:
        year, month = map(int, date_match.groups())
        return datetime(year, month, 1)  # Default to first of month

    # PRIORITY 2: Try to get date from metadata
    if content_data and content_data.get("metadata", {}).get("date"):
        date_str = content_data["metadata"]["date"]
        try:
            # Try various date formats
            for fmt in ["%Y-%m-%d", "%B %Y", "%Y", "%B %d, %Y"]:
                try:
                    return datetime.strptime(str(date_str), fmt)
                except ValueError:
                    continue
        except:
            pass

    # PRIORITY 3: Fall back to file modification time
    try:
        return datetime.fromtimestamp(item_path.stat().st_mtime)
    except:
        return None


def find_related_posts(current_post_path, limit=3):
    """Find related posts based on tags and content similarity."""
    from ..core.cache import get_blog_cache

    blog_data = get_blog_cache() or {}
    posts = blog_data.get("posts", [])
    if not posts:
        return []

    def normalize(path_value):
        path_str = str(path_value).replace("\\", "/")
        return path_str[2:] if path_str.startswith("./") else path_str

    post_lookup = {}
    for post in posts:
        file_path = post.get("file_path")
        if not file_path:
            continue
        post_lookup[normalize(file_path)] = post

    current_key = normalize(Path(current_post_path))
    current_post = post_lookup.get(current_key)
    if not current_post:
        return []

    @lru_cache(maxsize=512)
    def get_terms(post_key):
        post = post_lookup.get(post_key)
        if not post:
            return {}, set()

        content = (post.get("content") or "").lower()
        words = [w for w in TOKEN_PATTERN.findall(content) if w not in STOPWORDS]
        if not words:
            return {}, set()

        top_terms = dict(Counter(words).most_common(40))
        title_terms = {
            w
            for w in TOKEN_PATTERN.findall((post.get("title") or "").lower())
            if w not in STOPWORDS
        }
        return top_terms, title_terms

    def fallback_posts():
        fallback = [post for key, post in post_lookup.items() if key != current_key]
        fallback.sort(key=lambda p: (p.get("pub_date") or datetime.min), reverse=True)
        return [compact(post) for post in fallback[:limit]]

    current_terms, current_title_terms = get_terms(current_key)
    if not current_terms and not current_title_terms:
        return fallback_posts()

    current_weight = sum(current_terms.values()) or 1
    current_date = current_post.get("pub_date")

    def compact(post):
        return {
            "title": post.get("title"),
            "url": post.get("url") or post.get("path"),
            "description": post.get("description"),
            "pub_date": post.get("pub_date"),
            "date_str": post.get("date_str"),
            "unique_icon": post.get("unique_icon"),
        }

    scored_posts = []
    for key, candidate in post_lookup.items():
        if key == current_key:
            continue

        candidate_terms, candidate_title_terms = get_terms(key)

        shared_terms = set(current_terms).intersection(candidate_terms)
        shared_weight = sum(
            min(current_terms[word], candidate_terms[word]) for word in shared_terms
        )

        normalization = 0
        if shared_weight:
            candidate_weight = sum(candidate_terms.values()) or 1
            normalization = (shared_weight * 100) // (current_weight + candidate_weight)

        title_overlap = len(current_title_terms & candidate_title_terms)

        date_bonus = 0
        candidate_date = candidate.get("pub_date")
        if current_date and candidate_date:
            month_delta = abs(
                (current_date.year - candidate_date.year) * 12
                + (current_date.month - candidate_date.month)
            )
            if month_delta < 24:
                date_bonus = 24 - month_delta

        score = shared_weight * 10 + normalization * 2 + title_overlap * 5 + date_bonus

        if score:
            scored_posts.append((score, candidate))

    if not scored_posts:
        return fallback_posts()

    scored_posts.sort(
        key=lambda item: (
            item[0],
            item[1].get("pub_date") or datetime.min,
        ),
        reverse=True,
    )

    return [compact(post) for score, post in scored_posts[:limit]]


def find_adjacent_posts(current_post_path):
    """Find previous and next posts in chronological order."""
    from ..core.cache import get_blog_cache

    blog_data = get_blog_cache() or {}
    posts = blog_data.get("posts", [])
    if not posts:
        return {"prev": None, "next": None}

    def normalize(path_value):
        path_str = str(path_value).replace("\\", "/")
        return path_str[2:] if path_str.startswith("./") else path_str

    current_key = normalize(Path(current_post_path))

    current_index = None
    for idx, post in enumerate(posts):
        file_path = post.get("file_path")
        if file_path and normalize(file_path) == current_key:
            current_index = idx
            break

    if current_index is None:
        return {"prev": None, "next": None}

    def compact_post(post):
        if not post:
            return None
        return {
            "title": post.get("title"),
            "url": post.get("url") or post.get("path"),
            "pub_date": post.get("pub_date"),
            "date_str": post.get("date_str"),
            "description": post.get("description"),
            "unique_icon": post.get("unique_icon"),
        }

    prev_post = posts[current_index + 1] if current_index + 1 < len(posts) else None
    next_post = posts[current_index - 1] if current_index - 1 >= 0 else None

    return {"prev": compact_post(prev_post), "next": compact_post(next_post)}

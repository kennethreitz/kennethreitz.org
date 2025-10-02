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


def extract_exif_data(image_path):
    """Extract EXIF data from an image file."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        img = Image.open(image_path)
        exif_data = {}

        # Get basic image info
        exif_data['width'] = img.width
        exif_data['height'] = img.height
        exif_data['format'] = img.format

        # Get EXIF data if available
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif = img._getexif()
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)

                # Extract commonly useful fields
                if tag == 'Make':
                    exif_data['camera_make'] = str(value).strip()
                elif tag == 'Model':
                    exif_data['camera_model'] = str(value).strip()
                elif tag == 'DateTime':
                    exif_data['date_taken'] = str(value)
                elif tag == 'DateTimeOriginal':
                    exif_data['date_original'] = str(value)
                elif tag == 'LensModel':
                    exif_data['lens'] = str(value).strip()
                elif tag == 'FocalLength':
                    # Convert to readable format
                    if isinstance(value, tuple):
                        exif_data['focal_length'] = f"{value[0]/value[1]:.0f}mm"
                    else:
                        exif_data['focal_length'] = f"{value}mm"
                elif tag == 'FNumber':
                    # Convert to readable format
                    if isinstance(value, tuple):
                        f_num = value[0]/value[1]
                        # Round to 1 decimal place, but show as integer if whole number
                        if f_num == int(f_num):
                            exif_data['aperture'] = f"f/{int(f_num)}"
                        else:
                            exif_data['aperture'] = f"f/{f_num:.1f}"
                    else:
                        exif_data['aperture'] = f"f/{value}"
                elif tag == 'ISOSpeedRatings':
                    exif_data['iso'] = f"ISO {value}"
                elif tag == 'ExposureTime':
                    # Convert to readable format as fraction
                    from fractions import Fraction

                    if isinstance(value, tuple):
                        frac = Fraction(value[0], value[1])
                    else:
                        # Convert float to fraction
                        frac = Fraction(value).limit_denominator(8000)

                    if frac >= 1:
                        # For exposures >= 1 second, show as decimal
                        exif_data['shutter_speed'] = f"{float(frac):.1f}s"
                    else:
                        # For fast shutter speeds, show as fraction
                        exif_data['shutter_speed'] = f"1/{int(1/frac)}s"

        return exif_data
    except Exception as e:
        print(f"Error extracting EXIF from {image_path}: {e}")
        return {}


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


@content_bp.route("/data/<path:path>")
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


@content_bp.route("/<path:path>.md")
def serve_content_markdown(path):
    """Serve the raw markdown source of the content."""
    from flask import make_response

    # Remove trailing slash for consistency
    path = path.rstrip("/")

    # Check for the markdown file
    file_path = DATA_DIR / f"{path}.md"

    if not file_path.exists():
        abort(404)

    # Read the raw markdown content
    markdown_content = file_path.read_text()

    # Create response with proper headers
    response = make_response(markdown_content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Content-Disposition'] = f'inline; filename="{path.split("/")[-1]}.md"'

    return response


@content_bp.route("/<path:path>.pdf")
def serve_content_pdf(path):
    """Generate and serve a PDF version of the content."""
    from ..core.markdown import render_markdown_file
    from flask import make_response, request
    import io

    # Check if WeasyPrint is available
    try:
        from weasyprint import HTML
        from weasyprint.text.fonts import FontConfiguration
        WEASYPRINT_AVAILABLE = True
    except (ImportError, OSError) as e:
        # WeasyPrint or its system dependencies are not available
        print(f"WeasyPrint not available: {e}")
        WEASYPRINT_AVAILABLE = False

    # Remove trailing slash for consistency
    path = path.rstrip("/")

    # Check for the markdown file
    file_path = DATA_DIR / f"{path}.md"

    if not file_path.exists():
        abort(404)

    # If WeasyPrint is not available, return a helpful error page
    if not WEASYPRINT_AVAILABLE:
        from datetime import datetime
        error_html = render_template(
            "error.html",
            title="PDF Generation Unavailable",
            message="PDF generation requires WeasyPrint and system dependencies to be installed.",
            details="Please see the README for installation instructions, or use the browser's print dialog (Cmd+P / Ctrl+P) to save as PDF.",
            current_year=datetime.now().year,
        )
        response = make_response(error_html, 503)
        return response

    # Render the markdown content
    content_data = render_markdown_file(file_path)

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

    # Render HTML for PDF
    from datetime import datetime
    html_content = render_template(
        "pdf.html",
        content=content_data["content"],
        title=content_data["title"],
        metadata=content_data["metadata"],
        current_year=datetime.now().year,
        reading_time=content_data.get("reading_time"),
        word_count=content_data.get("word_count"),
        article_themes=article_themes,
        unique_icon=content_data.get("unique_icon"),
    )

    # Generate PDF
    font_config = FontConfiguration()

    # Get the base URL for resolving relative URLs in CSS/images
    base_url = request.url_root

    pdf_file = io.BytesIO()
    HTML(string=html_content, base_url=base_url).write_pdf(
        pdf_file,
        font_config=font_config
    )
    pdf_file.seek(0)

    # Create response
    response = make_response(pdf_file.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{path.split("/")[-1]}.pdf"'

    return response


@content_bp.route("/<path:path>")
def serve_content(path):
    """Serve content from markdown files or directories."""
    from ..core.markdown import render_markdown_file
    from ..utils.content import get_directory_structure
    from datetime import datetime

    # Remove trailing slash for consistency
    path = path.rstrip("/")

    # Check if this is an image file request
    raw_file_path = DATA_DIR / path
    if raw_file_path.exists() and raw_file_path.is_file():
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico'}
        suffix = raw_file_path.suffix.lower()
        if suffix in image_extensions:
            # Serve the image file directly
            from flask import make_response
            # Use absolute path for send_from_directory
            abs_data_dir = DATA_DIR.resolve()
            response = make_response(send_from_directory(abs_data_dir, path))
            response.headers["Cache-Control"] = "public, max-age=604800"
            return response

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
            
            from flask import make_response
            response = make_response(render_template(
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
            ))

            # Add Link headers for alternate formats
            response.headers.add('Link', f'</{path}.pdf>; rel="alternate"; type="application/pdf"')
            response.headers.add('Link', f'</{path}.md>; rel="alternate"; type="text/plain"')

            return response
        else:
            # Show directory listing
            items = get_directory_structure(dir_path)

            # Detect if this is an image gallery
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
            image_items = []
            for item in items:
                if not item['is_dir']:
                    item_path = DATA_DIR / item['url_path'].lstrip('/')
                    if item_path.suffix.lower() in image_extensions:
                        # Mark as image and create path that will be caught by serve_data_file
                        item['is_image'] = True
                        # The path is the URL path which will be handled by the catch-all route
                        # We need to mark these to be served as files
                        item['static_path'] = item['url_path']
                        item['is_data_file'] = True

                        # Extract EXIF data for JPEGs
                        if item_path.suffix.lower() in {'.jpg', '.jpeg'}:
                            item['exif'] = extract_exif_data(item_path)
                        else:
                            item['exif'] = {}

                        image_items.append(item)
                    else:
                        item['is_image'] = False
                else:
                    item['is_image'] = False

            is_image_gallery = len(image_items) > 0

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

            # Generate folder icon for this directory
            from ..utils.content import generate_folder_icon
            folder_icon = generate_folder_icon(title, size=32)

            return render_template(
                "directory.html",
                items=items,
                current_path=f"/{path}",
                breadcrumb=breadcrumb,
                current_year=datetime.now().year,
                title=title,
                is_image_gallery=is_image_gallery,
                image_items=image_items,
                folder_icon=folder_icon,
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

        from flask import make_response
        response = make_response(render_template(
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
        ))

        # Add Link headers for alternate formats
        response.headers.add('Link', f'</{path}.pdf>; rel="alternate"; type="application/pdf"')
        response.headers.add('Link', f'</{path}.md>; rel="alternate"; type="text/plain"')

        return response

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

"""Markdown processing core module."""

import re
from html import escape as html_escape
from urllib.parse import quote as url_quote

import mistune
import yaml

from ..utils.svg_icons import generate_unique_svg_icon
from ..utils.content import (
    calculate_reading_time,
    extract_tags_from_content,
    find_series_posts,
)


def _process_oembed(html):
    """Replace bare URLs in paragraphs with client-side oEmbed placeholders."""

    def _replace_link(match):
        url = match.group(1)

        # SoundCloud: render inline, no discovery needed.
        if re.match(r"https?://(?:www\.)?soundcloud\.com/.+", url):
            encoded = url_quote(url, safe="")
            return (
                f'<iframe width="100%" height="20" scrolling="no" frameborder="no"'
                f' src="https://w.soundcloud.com/player/?url={encoded}'
                f'&color=%23333333&auto_play=false&hide_related=true'
                f'&show_comments=false&show_user=false&show_reposts=false'
                f'&show_teaser=false&show_artwork=false&visual=false"></iframe>'
            )

        # Everything else: render a placeholder for client-side oEmbed.
        safe_url = html_escape(url, quote=True)
        return (
            f'<div class="oembed-placeholder" data-oembed-url="{safe_url}">'
            f'<a href="{safe_url}" target="_blank" rel="noopener">{safe_url}</a>'
            f'</div>'
        )

    # Match any <p> containing only a single bare <a> link (any https URL).
    return re.sub(
        r'<p><a href="(https?://[^"]+)">[^<]+</a></p>',
        _replace_link,
        html,
    )


class TufteMarkdownRenderer:
    """Custom Markdown renderer for Tufte-style output."""

    def __init__(self):
        """Initialize the renderer with Mistune."""
        self.markdown = mistune.create_markdown(
            escape=False,
            plugins=[
                "strikethrough",
                "footnotes",
                "table",
                "task_lists",
                "def_list",
                "url",
            ],
        )

    def render(self, content):
        """Render markdown content to HTML."""
        html = self.markdown(content.strip())
        return _process_oembed(html)


def render_markdown_file(file_path):
    """Render a markdown file to HTML with metadata extraction."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract YAML front matter if it exists
        metadata = {}
        yaml_pattern = r"^---\s*\n(.*?)\n---\s*\n"
        yaml_match = re.match(yaml_pattern, content, re.DOTALL)
        if yaml_match:
            try:
                metadata = yaml.safe_load(yaml_match.group(1)) or {}
                content = content[yaml_match.end() :]
            except:
                pass

        # Extract first h1 header if it exists
        first_h1 = None
        # Look for the first H1 at the start of the file (must be on first line or after blank line)
        h1_match = re.search(r"^# (.+?)$", content, re.MULTILINE)
        if h1_match:
            first_h1 = h1_match.group(1).strip()
            # Remove only the first h1 line from content to avoid duplication
            content = re.sub(r"^# .+?$", "", content, count=1, flags=re.MULTILINE)

        # Extract date from italic date pattern (e.g., "*August 2025*")
        # Only match dates that look like month/year patterns, not quotes or long text
        date_match = re.search(
            r"^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$", content, re.MULTILINE
        )
        if date_match and not metadata.get("date"):
            date_text = date_match.group(1).strip()
            # Skip only if it's "January 2025" (current year placeholder)
            if not (date_text.lower().startswith("january") and "2025" in date_text):
                # Format "January YYYY" (not 2025) as just "YYYY" for cleaner display
                if (
                    re.match(r"^january\s+(\d{4})$", date_text.lower())
                    and "2025" not in date_text
                ):
                    year_match = re.search(r"(\d{4})", date_text)
                    if year_match:
                        date_text = year_match.group(1)
                # Keep other months like "August 2025" as full format
                metadata["date"] = date_text
            # Remove the date line from content
            content = re.sub(
                r"^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$",
                "",
                content,
                count=1,
                flags=re.MULTILINE,
            )

        # Create renderer and process content
        renderer = TufteMarkdownRenderer()
        html_content = renderer.render(content)

        # Add anchor IDs to headings using post-processing on HTML
        html_content = add_heading_anchor_ids(html_content)

        # Post-processing for poetry line breaks
        # Check if this is likely a poetry file based on file path
        if file_path and "poetry" in str(file_path):
            # For poetry, convert single line breaks within paragraphs to <br> tags
            html_content = re.sub(
                r"<p>(.*?)</p>",
                lambda m: "<p>" + m.group(1).replace("\n", "<br>\n") + "</p>",
                html_content,
                flags=re.DOTALL,
            )

        # Add classes to headers to prevent conflicts with page headers
        html_content = html_content.replace("<h1>", '<h1 class="content-header">')
        html_content = html_content.replace("<h2>", '<h2 class="content-header">')
        html_content = html_content.replace("<h3>", '<h3 class="content-header">')
        html_content = html_content.replace("<h4>", '<h4 class="content-header">')
        html_content = html_content.replace("<h5>", '<h5 class="content-header">')
        html_content = html_content.replace("<h6>", '<h6 class="content-header">')

        # Use the first h1 as title if available, otherwise fallback to metadata or filename
        if first_h1:
            title = first_h1
        elif "title" in metadata:
            title = metadata["title"]
        else:
            title = file_path.stem.replace("-", " ").replace("_", " ").title()

        # Calculate reading time
        reading_time, word_count = calculate_reading_time(html_content)

        # Extract tags
        tags = extract_tags_from_content(html_content, metadata, file_path)

        # Find series posts if this post is part of a series
        series_posts = find_series_posts(metadata, file_path)

        # Generate unique icon for this content
        # Use folder icon for index.md files (directory pages)
        if file_path.name == "index.md":
            from ..utils.content import generate_folder_icon
            unique_icon = generate_folder_icon(title, size=32)
        else:
            unique_icon = generate_unique_svg_icon(title, size=32)

        return {
            "content": html_content,
            "title": title,
            "metadata": metadata,
            "reading_time": reading_time,
            "word_count": word_count,
            "tags": tags,
            "series_posts": series_posts,
            "series_name": metadata.get("series"),
            "unique_icon": unique_icon,
        }
    except Exception as e:
        return {
            "content": f"<p>Error reading file: {str(e)}</p>",
            "title": "Error",
            "metadata": {},
        }


def add_heading_anchor_ids(html_content):
    """Add anchor IDs to headings for navigation."""

    def replace_heading(match):
        tag = match.group(1)  # h1, h2, etc.
        level = int(tag[1])  # 1, 2, etc.
        classes = match.group(2) or ""  # existing classes if any
        text = match.group(3)

        # Generate anchor ID from heading text (remove HTML tags first)
        clean_text = re.sub(r"<[^>]+>", "", text)
        anchor_id = re.sub(r"[^\w\s-]", "", clean_text.lower()).replace(" ", "-")
        anchor_id = re.sub(r"-+", "-", anchor_id).strip("-")  # Clean up multiple dashes

        # Add id attribute, preserving any existing classes
        if classes:
            return f'<{tag} id="{anchor_id}"{classes}>{text}</{tag}>'
        else:
            return f'<{tag} id="{anchor_id}">{text}</{tag}>'

    # Match h1-h6 tags with optional class attributes
    return re.sub(
        r"<(h[1-6])(\s+[^>]*)?>([^<]+)</h[1-6]>", replace_heading, html_content
    )

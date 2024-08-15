import os
import pathlib
import re
import shutil
from typing import List, Optional, Tuple
from datetime import datetime
import mistune
from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image
from PIL.ExifTags import TAGS

from tuftedoc import (
    process_markdown_file,
    generate_breadcrumbs,
    generate_title_from_breadcrumbs,
    process_directory,
    get_file_creation_date,
    is_image,
    get_exif_data,
)


# Configuration
MARKDOWN_DIR = pathlib.Path("./data").resolve()
STATIC_DIR = pathlib.Path("./static").resolve()
OUTPUT_DIR = pathlib.Path("./output").resolve()
TEMPLATE_DIR = pathlib.Path("./templates").resolve()

# Mistune setup
markdown = mistune.create_markdown(
    plugins=["table", "url", "strikethrough", "footnotes"],
    escape=False,
)

# Jinja2 setup
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
)


# Custom Jinja2 filter for datetime formatting
def format_datetime(value):
    if isinstance(value, (int, float)):
        value = datetime.fromtimestamp(value)
    return value.strftime("%Y-%m-%d %H:%M:%S")


env.filters["datetime"] = format_datetime


# Helper functions
def is_image(file_path: pathlib.Path) -> bool:
    return file_path.suffix.lower() in (".jpg", ".jpeg")


def get_exif_data(image_path: pathlib.Path) -> dict:
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                exif = {TAGS.get(key, key): value for key, value in exif_data.items()}
                return {
                    "Camera": exif.get("Model", "Unknown"),
                    "Lens": exif.get("LensModel", "Unknown"),
                    "Aperture": exif.get("FNumber", "Unknown"),
                    "Shutter Speed": exif.get("ExposureTime", "Unknown"),
                    "ISO": exif.get("ISOSpeedRatings", "Unknown"),
                    "Focal Length": exif.get("FocalLength", "Unknown"),
                }
    except Exception as e:
        print(f"Error reading EXIF data: {e}")
    return {}


# ... (other helper functions remain the same)


def generate_static_site():
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copy static files
    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static", dirs_exist_ok=True)

    # Process markdown files
    for markdown_file in MARKDOWN_DIR.rglob("*.md"):
        relative_path = markdown_file.relative_to(MARKDOWN_DIR)
        output_path = OUTPUT_DIR / relative_path.with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate content
        content = process_markdown_file(markdown_file)
        breadcrumbs = generate_breadcrumbs(str(relative_path))
        page_title = generate_title_from_breadcrumbs(breadcrumbs)

        # If it's a directory index, process directory contents
        if markdown_file.name == "index.md":
            all_items, _ = process_directory(markdown_file.parent)
            has_images = any(item.is_image for item in all_items)
        else:
            all_items = None
            has_images = False

        # Render template
        template = env.get_template("index.html")
        html_content = template.render(
            title=page_title,
            breadcrumbs=breadcrumbs,
            files=all_items,
            content=content,
            date_created=get_file_creation_date(markdown_file),
            has_images=has_images,
        )

        # Write to file
        with output_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

    # Process images (both .jpg and .jpeg)
    for image_file in MARKDOWN_DIR.rglob("*"):
        if is_image(image_file):
            relative_path = image_file.relative_to(MARKDOWN_DIR)
            output_path = OUTPUT_DIR / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(image_file, output_path)


if __name__ == "__main__":
    generate_static_site()

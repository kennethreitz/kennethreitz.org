import logging
import os
import pathlib
import random
import difflib
import re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional, Tuple

import background
import boto3
import mistune
from flask import Flask, render_template, request, send_file, abort, redirect, url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from PIL import Image
from PIL.ExifTags import TAGS


d

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
MARKDOWN_DIR = pathlib.Path("./data").resolve()
STATIC_DIR = pathlib.Path("./static").resolve()
BUCKET_NAME = os.environ["BUCKET_NAME"]
S3_ZIP_FILES = ["photos.zip"]

logger.info(f"MARKDOWN_DIR set to: {MARKDOWN_DIR}")
logger.info(f"STATIC_DIR set to: {STATIC_DIR}")


app = Flask(__name__)

# Mistune setup
markdown = mistune.create_markdown(
    plugins=["table", "url", "strikethrough", "footnotes"], escape=False, hard_wrap=True
)


# Helper functions
@background.task
def download_and_extract_s3_zips():
    s3 = boto3.client("s3")

    for zip_file in S3_ZIP_FILES:
        extracted_folder = MARKDOWN_DIR / zip_file.split(".")[0]
        if extracted_folder.exists() and any(extracted_folder.iterdir()):
            logger.info(
                f"Folder {extracted_folder} already exists and is not empty. Skipping download."
            )
            continue

        logger.info(f"Downloading {zip_file} from S3 bucket: {BUCKET_NAME}")

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            try:
                s3.download_fileobj(BUCKET_NAME, zip_file, temp_file)
                temp_file_path = pathlib.Path(temp_file.name)
            except Exception as e:
                logger.error(f"Failed to download {zip_file}: {str(e)}")
                continue

            logger.info(f"Extracting {zip_file} to {MARKDOWN_DIR}")
            try:
                with zipfile.ZipFile(temp_file_path, "r") as zip_ref:
                    zip_ref.extractall(MARKDOWN_DIR)
            except Exception as e:
                logger.error(f"Failed to extract {zip_file}: {str(e)}")
            finally:
                temp_file_path.unlink(missing_ok=True)

            # Remove the __MACOSX folder.
            macos_folder = MARKDOWN_DIR / "__MACOSX"
            if macos_folder.exists():
                shutil.rmtree(macos_folder)

    logger.info("S3 zip downloads and extractions completed.")


def find_similar_path(path: str, threshold: float = 0.6) -> Optional[str]:
    target_name = os.path.basename(path)
    all_paths = [
        str(p.relative_to(MARKDOWN_DIR))
        for p in MARKDOWN_DIR.glob("**/*")
        if p.is_file() or p.is_dir()
    ]

    # Filter paths that have the same final component length (±1) as the target
    filtered_paths = [p for p in all_paths if abs(len(os.path.basename(p)) - len(target_name)) <= 1]

    if not filtered_paths:
        return None

    matches = difflib.get_close_matches(target_name, [os.path.basename(p) for p in filtered_paths], n=1, cutoff=threshold)

    if matches:
        matched_name = matches[0]
        # Find the full path that matches the similar filename
        for p in filtered_paths:
            if os.path.basename(p) == matched_name:
                return p

    return None

def title_case(s: str) -> str:
    return " ".join(
        word.capitalize() for word in s.replace("-", " ").replace("_", " ").split()
    )


def get_h1_from_markdown(file_path: pathlib.Path) -> Optional[str]:
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"^---\n.*?^---\n", "", content, flags=re.MULTILINE | re.DOTALL)
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1) if match else None


def get_directory_title(dir_path: pathlib.Path) -> str:
    index_file = dir_path / "index.md"
    return (
        get_h1_from_markdown(index_file)
        if index_file.exists()
        else title_case(dir_path.name)
    )


def get_clean_url(path: str) -> str:
    return "/" + path.rsplit(".", 1)[0] if path.endswith(".md") else "/" + path


def get_file_creation_date(file_path: pathlib.Path) -> datetime:
    return datetime.fromtimestamp(file_path.stat().st_ctime)


def is_image(file_path: pathlib.Path) -> bool:
    return file_path.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif")


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
        logger.error(f"Error reading EXIF data: {e}")
    return {}


def process_directory(full_path: pathlib.Path) -> Tuple[List[FileInfo], Optional[str]]:
    logger.info(f"Processing directory: {full_path}")
    all_items = []
    for item in full_path.iterdir():
        if item.name in [".DS_Store", "index.md"] or item.name.startswith("."):
            continue
        is_image_file = is_image(item)
        exif_data = get_exif_data(item) if is_image_file else None
        item_data = FileInfo(
            name=title_case(item.name),
            url=get_clean_url(str(item.relative_to(MARKDOWN_DIR))),
            ctime=os.path.getctime(item),
            is_dir=item.is_dir(),
            title=(
                get_directory_title(item)
                if item.is_dir()
                else (get_h1_from_markdown(item) if item.suffix == ".md" else None)
            ),
            is_image=is_image_file,
            exif_data=exif_data,
        )
        all_items.append(item_data)

    # Sort items alphabetically by name, with directories first
    all_items.sort(key=lambda x: (not x.is_dir, x.name.lower()))

    index_file = full_path / "index.md"
    content = process_markdown_file(index_file) if index_file.exists() else None

    logger.info(f"Processed {len(all_items)} items in directory: {full_path}")
    return all_items, content


def process_markdown_file(file_path: pathlib.Path) -> str:
    logger.info(f"Processing markdown file: {file_path}")
    with file_path.open("r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Remove front matter for display in the browser.
    markdown_content = re.sub(
        r"^---\n.*?^---\n", "", markdown_content, flags=re.MULTILINE | re.DOTALL
    )
    return markdown(markdown_content)


def generate_breadcrumbs(path: str) -> List[Breadcrumb]:
    breadcrumbs = []
    current_path = MARKDOWN_DIR
    for part in pathlib.Path(path).parts:
        current_path = current_path / part
        crumb = Breadcrumb(
            name=title_case(part),
            url=get_clean_url(str(current_path.relative_to(MARKDOWN_DIR))),
            title=(
                get_directory_title(current_path)
                if current_path.is_dir()
                else (
                    get_h1_from_markdown(current_path)
                    if current_path.suffix == ".md"
                    else None
                )
            ),
        )
        breadcrumbs.append(crumb)
    return breadcrumbs


def generate_title_from_breadcrumbs(breadcrumbs: List[Breadcrumb]) -> str:
    return " > ".join(crumb.title or crumb.name for crumb in breadcrumbs)


def clean_url(url: str) -> str:
    return re.sub(r"(?<!:)//+", "/", url)


def generate_sitemap(base_url: str) -> str:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    def add_url(
        loc: str,
        lastmod: datetime = None,
        changefreq: str = None,
        priority: float = None,
    ):
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = clean_url(
            f"{base_url.rstrip('/')}/{loc.lstrip('/')}"
        )
        if lastmod:
            ET.SubElement(url, "lastmod").text = lastmod.strftime("%Y-%m-%d")
        if changefreq:
            ET.SubElement(url, "changefreq").text = changefreq
        if priority:
            ET.SubElement(url, "priority").text = str(priority)

    def traverse_directory(path: pathlib.Path, relative_path: str = ""):
        for item in path.iterdir():
            if item.name.startswith(".") or item.name == "index.md":
                continue
            item_relative_path = f"{relative_path}/{item.name}"
            clean_item_path = clean_url(get_clean_url(item_relative_path))
            if item.is_dir():
                add_url(
                    clean_item_path,
                    lastmod=datetime.fromtimestamp(item.stat().st_mtime),
                    changefreq="weekly",
                    priority=0.8,
                )
                traverse_directory(item, item_relative_path)
            elif item.suffix == ".md":
                add_url(
                    clean_item_path,
                    lastmod=datetime.fromtimestamp(item.stat().st_mtime),
                    changefreq="monthly",
                    priority=0.6,
                )

    add_url("/", lastmod=datetime.now(), changefreq="daily", priority=1.0)
    traverse_directory(MARKDOWN_DIR)

    return ET.tostring(urlset, encoding="unicode", method="xml")


@app.before_first_request
def before_first_request():
    download_and_extract_s3_zips()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def browse(path):
    logger.info(f"Browsing path: {path}")
    full_path = MARKDOWN_DIR / path
    if not full_path.exists():
        full_path_with_md = full_path.with_suffix(".md")
        if full_path_with_md.exists():
            full_path = full_path_with_md
        elif is_image(full_path.with_suffix(".jpg")) or is_image(full_path.with_suffix(".jpeg")):
            image_path = full_path.with_suffix(".jpg") if is_image(full_path.with_suffix(".jpg")) else full_path.with_suffix(".jpeg")
            return send_file(image_path, mimetype='image/jpeg')
        else:
            logger.warning(f"Path not found: {full_path}")
            similar_path = find_similar_path(path)
            if similar_path:
                return redirect(f"/{similar_path}", code=301)
            else:
                abort(404)

    if full_path.is_dir():
        all_items, content = process_directory(full_path)
        date_created = None
    else:
        try:
            if is_image(full_path):
                return send_file(full_path, mimetype='image/jpeg')
            content = process_markdown_file(full_path)
            all_items = None
            date_created = get_file_creation_date(full_path)
        except UnicodeDecodeError:
            logger.error(f"UnicodeDecodeError when processing file: {full_path}")
            return send_file(full_path, as_attachment=True)

    breadcrumbs = generate_breadcrumbs(path)
    page_title = generate_title_from_breadcrumbs(breadcrumbs)
    has_images = any(item.is_image for item in all_items or [])

    if has_images:
        random.shuffle(all_items or [])

    return render_template(
        "index.html",
        title=page_title,
        breadcrumbs=breadcrumbs,
        files=all_items,
        content=content,
        date_created=date_created,
        has_images=has_images,
    )


@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root
    sitemap_content = generate_sitemap(base_url)
    response = app.response_class(sitemap_content, mimetype='application/xml')
    return response


@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('browse'))


if __name__ == "__main__":
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/static': app.send_static_file,
        '/data': app.send_static_file
    })
    run_simple('0.0.0.0', 8000, app, use_reloader=True, use_debugger=True)

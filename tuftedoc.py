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
import json
import yaml
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any, Union

import background
import boto3
import mistune
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import FileResponse, HTMLResponse, Response, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from PIL.ExifTags import TAGS
from pydantic import BaseModel, Field


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
MARKDOWN_DIR = pathlib.Path("./data").resolve()
STATIC_DIR = pathlib.Path("./static").resolve()


if "BUCKET_NAME" in os.environ:
    BUCKET_NAME = os.environ["BUCKET_NAME"]
else:
    BUCKET_NAME = None

S3_ZIP_FILES = ["photos.zip"]

logger.info(f"MARKDOWN_DIR set to: {MARKDOWN_DIR}")
logger.info(f"STATIC_DIR set to: {STATIC_DIR}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    download_and_extract_s3_zips()
    yield
    logger.info("Shutting down...")


# FastAPI setup
app = FastAPI(
    title="Tufte Markdown Browser API",
    description="API for browsing and rendering markdown content using Tailwind CSS and tuftedoc",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; in production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 setup
templates = Jinja2Templates(directory="templates")
templates.env.filters["datetime"] = lambda value: (
    datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, (int, float))
    else value.strftime("%Y-%m-%d %H:%M:%S")
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/data", StaticFiles(directory=str(MARKDOWN_DIR)), name="data")

# Mistune setup
markdown = mistune.create_markdown(
    plugins=["table", "url", "strikethrough", "footnotes"], escape=False, hard_wrap=True
)


# Models
class Metadata(BaseModel):
    """Metadata extracted from frontmatter in markdown files."""
    title: Optional[str] = Field(None, description="Title from the document frontmatter")
    date: Optional[str] = Field(None, description="Date of publication")
    author: Optional[str] = Field(None, description="Author of the document")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the document")
    description: Optional[str] = Field(None, description="Brief description of the content")
    featured_image: Optional[str] = Field(None, description="Path to a featured image")
    draft: Optional[bool] = Field(False, description="Whether the content is a draft")
    layout: Optional[str] = Field(None, description="Layout template to use")
    extra: Optional[Dict[str, Any]] = Field(None, description="Additional custom metadata")


class FileInfo(BaseModel):
    name: str = Field(..., description="Name of the file or directory")
    url: str = Field(..., description="URL path to the file or directory")
    title: Optional[str] = Field(
        None, description="Title of the file or directory, if available"
    )
    slug: str = Field(..., description="Slug/basename of the file or directory")
    ctime: float = Field(..., description="Creation time of the file or directory")
    mtime: float = Field(..., description="Modification time of the file or directory")
    is_dir: bool = Field(..., description="Whether the item is a directory")
    is_image: bool = Field(False, description="Whether the item is an image")
    exif_data: Optional[dict] = Field(None, description="EXIF data for image files")
    metadata: Optional[Metadata] = Field(None, description="Frontmatter metadata if available")
    summary: Optional[str] = Field(None, description="Brief summary of the content")


class Breadcrumb(BaseModel):
    name: str = Field(..., description="Name of the breadcrumb")
    url: str = Field(..., description="URL path of the breadcrumb")
    title: Optional[str] = Field(
        None, description="Title of the breadcrumb, if available"
    )


# Helper functions
@background.task
def download_and_extract_s3_zips():
    s3 = boto3.client("s3")

    for zip_file in S3_ZIP_FILES:
        if not BUCKET_NAME:
            logger.error("BUCKET_NAME is not set. Skipping download.")
            continue

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
    filtered_paths = [
        p for p in all_paths if abs(len(os.path.basename(p)) - len(target_name)) <= 1
    ]

    if not filtered_paths:
        return None

    matches = difflib.get_close_matches(
        target_name,
        [os.path.basename(p) for p in filtered_paths],
        n=1,
        cutoff=threshold,
    )

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


def extract_frontmatter(markdown_content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Extract frontmatter from markdown content."""
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)", markdown_content, re.DOTALL)
    
    if frontmatter_match:
        try:
            # Parse the YAML frontmatter
            frontmatter_yaml = frontmatter_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_yaml)
            content = frontmatter_match.group(2)
            return frontmatter, content
        except Exception as e:
            logger.error(f"Error parsing frontmatter: {e}")
            # If there's an error in parsing, return the original content without frontmatter
            content = re.sub(r"^---\n.*?^---\n", "", markdown_content, flags=re.MULTILINE | re.DOTALL)
            return None, content
    else:
        # No frontmatter found
        return None, markdown_content


def parse_metadata(frontmatter: Optional[Dict[str, Any]]) -> Optional[Metadata]:
    """Parse frontmatter into a Metadata object."""
    if not frontmatter:
        return None
    
    # Extract known fields
    metadata_dict = {
        "title": frontmatter.get("title"),
        "date": frontmatter.get("date"),
        "author": frontmatter.get("author"),
        "tags": frontmatter.get("tags", []),
        "description": frontmatter.get("description"),
        "featured_image": frontmatter.get("featured_image"),
        "draft": frontmatter.get("draft", False),
        "layout": frontmatter.get("layout"),
    }
    
    # Copy any extra fields to the extra dict
    extra_fields = {k: v for k, v in frontmatter.items() 
                  if k not in metadata_dict}
    
    if extra_fields:
        metadata_dict["extra"] = extra_fields
        
    return Metadata(**metadata_dict)


def get_h1_from_markdown(file_path: pathlib.Path) -> Optional[str]:
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract frontmatter and content
    _, content_without_frontmatter = extract_frontmatter(content)
    
    # Look for the first heading
    match = re.search(r"^#\s+(.+)$", content_without_frontmatter, re.MULTILINE)
    return match.group(1) if match else None


def get_markdown_metadata(file_path: pathlib.Path) -> Optional[Metadata]:
    """Extract metadata from a markdown file."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        frontmatter, _ = extract_frontmatter(content)
        return parse_metadata(frontmatter)
    except Exception as e:
        logger.error(f"Error reading metadata from {file_path}: {e}")
        return None


def generate_summary(markdown_content: str, max_length: int = 150) -> str:
    """Generate a summary from markdown content."""
    # Remove frontmatter if present
    _, content = extract_frontmatter(markdown_content)
    
    # Remove markdown formatting
    # Strip headers
    content = re.sub(r"^#{1,6}\s+.*$", "", content, flags=re.MULTILINE)
    # Strip links
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)
    # Strip images
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    # Strip code blocks
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    # Strip inline code
    content = re.sub(r"`[^`]+`", "", content)
    # Strip bold/italic
    content = re.sub(r"\*\*|\*|__|\b_\b", "", content)
    
    # Clean up whitespace
    content = re.sub(r"\s+", " ", content).strip()
    
    # Truncate to max_length
    if len(content) > max_length:
        content = content[:max_length-3] + "..."
        
    return content


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


def process_directory(full_path: pathlib.Path) -> Tuple[List[FileInfo], Optional[str], Optional[Metadata]]:
    logger.info(f"Processing directory: {full_path}")
    all_items = []
    
    # For sorting, we'll track directories and files separately
    directories = []
    files = []
    
    for item in full_path.iterdir():
        if item.name in [".DS_Store", ".git", "node_modules"] or item.name.startswith("."):
            continue
            
        if item.name == "index.md":
            continue
            
        is_image_file = is_image(item)
        exif_data = get_exif_data(item) if is_image_file else None
        
        # Get metadata for markdown files
        metadata = get_markdown_metadata(item) if item.suffix == ".md" else None
        
        # Get summary for markdown files
        summary = None
        if item.suffix == ".md":
            try:
                with item.open("r", encoding="utf-8") as f:
                    content = f.read()
                summary = generate_summary(content)
            except Exception as e:
                logger.error(f"Error generating summary for {item}: {e}")
                
        # Use metadata title if available, otherwise use H1 or directory title
        title = None
        if metadata and metadata.title:
            title = metadata.title
        else:
            title = (
                get_directory_title(item)
                if item.is_dir()
                else (get_h1_from_markdown(item) if item.suffix == ".md" else None)
            )
            
        item_data = FileInfo(
            name=title_case(item.name),
            url=get_clean_url(str(item.relative_to(MARKDOWN_DIR))),
            slug=item.name,
            ctime=os.path.getctime(item),
            mtime=os.path.getmtime(item),
            is_dir=item.is_dir(),
            title=title,
            is_image=is_image_file,
            exif_data=exif_data,
            metadata=metadata,
            summary=summary,
        )
        
        if item.is_dir():
            directories.append(item_data)
        else:
            # Skip draft content unless we're in debug mode
            if metadata and metadata.draft and not os.environ.get("DEBUG"):
                continue
            files.append(item_data)

    # Sort directories and files separately
    directories.sort(key=lambda x: x.name.lower())
    
    # Sort files by modification time (newest first) by default,
    # but can be sorted by other fields based on query parameters
    files.sort(key=lambda x: x.mtime, reverse=True)
    
    # Combine directories and files
    all_items = directories + files

    # Process index file
    index_file = full_path / "index.md"
    index_content = None
    index_metadata = None
    
    if index_file.exists():
        index_content, index_metadata = process_markdown_file_with_metadata(index_file)

    logger.info(f"Processed {len(all_items)} items in directory: {full_path}")
    return all_items, index_content, index_metadata


def process_markdown_file(file_path: pathlib.Path) -> str:
    """Process markdown file and return the rendered HTML content."""
    logger.info(f"Processing markdown file: {file_path}")
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Extract frontmatter and content
        _, content_without_frontmatter = extract_frontmatter(markdown_content)
        
        # Convert markdown to HTML
        html_content = markdown(content_without_frontmatter)
        return html_content
    except Exception as e:
        logger.error(f"Error processing markdown file {file_path}: {e}")
        return f"<p>Error processing markdown file: {str(e)}</p>"


def process_markdown_file_with_metadata(file_path: pathlib.Path) -> Tuple[str, Optional[Metadata]]:
    """Process markdown file and return both the rendered content and metadata."""
    logger.info(f"Processing markdown file with metadata: {file_path}")
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Extract frontmatter and content
        frontmatter, content_without_frontmatter = extract_frontmatter(markdown_content)
        
        # Parse metadata
        metadata = parse_metadata(frontmatter)
        
        # Convert markdown to HTML
        html_content = markdown(content_without_frontmatter)
        
        return html_content, metadata
    except Exception as e:
        logger.error(f"Error processing markdown file with metadata {file_path}: {e}")
        return f"<p>Error processing markdown file: {str(e)}</p>", None


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


class XMLResponse(Response):
    media_type = "application/xml"

    def __init__(self, content: str, *args, **kwargs):
        super().__init__(content=content, *args, **kwargs)


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


@app.get("/sitemap.xml", response_class=XMLResponse)
async def sitemap(request: Request):
    base_url = str(request.base_url)
    sitemap_content = generate_sitemap(base_url)
    return XMLResponse(content=sitemap_content, media_type="application/xml")


# API endpoints
@app.get("/api/content/{path:path}", response_model=Dict[str, Any], tags=["API"])
async def get_content_api(
    request: Request, 
    path: str = "", 
    format: str = Query("json", description="Response format (json or html)")
):
    """
    Get the content and metadata for a specific path.
    
    - For directories: returns list of items and index content if available
    - For files: returns the file content and metadata
    """
    logger.info(f"API request for path: {path}")
    
    try:
        full_path = MARKDOWN_DIR / path
        
        # Handle file extensions
        if not full_path.exists():
            full_path_with_md = full_path.with_suffix(".md")
            if full_path_with_md.exists():
                full_path = full_path_with_md
        
        # Process directory
        if full_path.is_dir():
            all_items, content, metadata = process_directory(full_path)
            result = {
                "type": "directory",
                "items": [item.dict() for item in all_items],
                "index_content": content,
                "metadata": metadata.dict() if metadata else None,
                "path": path,
            }
        # Process file
        elif full_path.suffix == ".md":
            content, metadata = process_markdown_file_with_metadata(full_path)
            result = {
                "type": "file",
                "content": content,
                "metadata": metadata.dict() if metadata else None,
                "path": path,
                "last_modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat(),
            }
        # Other file types
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {full_path.suffix}"}
            )
        
        if format.lower() == "html":
            # Return HTML response
            return HTMLResponse(content=content if content else "")
        else:
            # Return JSON response
            return result
            
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/api/search", response_model=Dict[str, Any], tags=["API"])
async def search_content(
    q: str = Query(..., description="Search query"),
    path: str = Query("", description="Path to limit search to"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags")
):
    """Search content in the repository."""
    logger.info(f"Search request: q={q}, path={path}, tags={tags}")
    
    results = []
    search_path = MARKDOWN_DIR / path if path else MARKDOWN_DIR
    
    # Simple search implementation - could be improved with a real search engine
    for item in search_path.glob("**/*.md"):
        try:
            relative_path = str(item.relative_to(MARKDOWN_DIR))
            
            # Skip hidden files and directories
            if any(part.startswith(".") for part in item.parts):
                continue
                
            with item.open("r", encoding="utf-8") as f:
                content = f.read()
                
            # Get metadata
            frontmatter, content_text = extract_frontmatter(content)
            metadata = parse_metadata(frontmatter)
            
            # Skip drafts
            if metadata and metadata.draft and not os.environ.get("DEBUG"):
                continue
                
            # Filter by tags if specified
            if tags and metadata and metadata.tags:
                if not any(tag in metadata.tags for tag in tags):
                    continue
            
            # Check for matches in content or title
            if (q.lower() in content_text.lower() or 
                (metadata and metadata.title and q.lower() in metadata.title.lower())):
                
                title = metadata.title if metadata and metadata.title else get_h1_from_markdown(item)
                summary = generate_summary(content)
                
                results.append({
                    "title": title or item.stem,
                    "path": get_clean_url(relative_path),
                    "summary": summary,
                    "tags": metadata.tags if metadata and metadata.tags else [],
                    "date": metadata.date if metadata and metadata.date else None,
                })
        except Exception as e:
            logger.error(f"Error processing file {item} during search: {e}")
            
    # Sort results by relevance (could be improved)
    results.sort(key=lambda x: 0 if x.get("title", "").lower().startswith(q.lower()) else 1)
    
    return {
        "query": q,
        "path": path,
        "tags": tags,
        "count": len(results),
        "results": results
    }


@app.get("/api/tags", response_model=Dict[str, Any], tags=["API"])
async def get_all_tags():
    """Get all tags used in the content with counts."""
    tags_count = {}
    
    # Collect all tags
    for item in MARKDOWN_DIR.glob("**/*.md"):
        try:
            # Skip hidden files
            if any(part.startswith(".") for part in item.parts):
                continue
                
            metadata = get_markdown_metadata(item)
            if metadata and metadata.tags:
                for tag in metadata.tags:
                    if tag in tags_count:
                        tags_count[tag] += 1
                    else:
                        tags_count[tag] = 1
        except Exception as e:
            logger.error(f"Error processing tags for file {item}: {e}")
            
    # Sort tags by count
    sorted_tags = [{"name": tag, "count": count} for tag, count in tags_count.items()]
    sorted_tags.sort(key=lambda x: x["count"], reverse=True)
    
    return {
        "count": len(sorted_tags),
        "tags": sorted_tags
    }


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/{path:path}", response_class=HTMLResponse, include_in_schema=False)
async def browse(
    request: Request, 
    path: str = "", 
    sort: str = Query(None, description="Sort order for files"),
    tag: str = Query(None, description="Filter by tag")
):
    logger.info(f"Browsing path: {path}")
    full_path = MARKDOWN_DIR / path
    
    if not full_path.exists():
        full_path_with_md = full_path.with_suffix(".md")
        if full_path_with_md.exists():
            full_path = full_path_with_md
        elif is_image(full_path.with_suffix(".jpg")) or is_image(
            full_path.with_suffix(".jpeg")
        ):
            image_path = (
                full_path.with_suffix(".jpg")
                if is_image(full_path.with_suffix(".jpg"))
                else full_path.with_suffix(".jpeg")
            )
            return FileResponse(image_path, media_type="image/jpeg")
        else:
            logger.warning(f"Path not found: {full_path}")
            similar_path = find_similar_path(path)
            if similar_path:
                return RedirectResponse(url=f"/{similar_path}", status_code=301)
            else:
                raise HTTPException(status_code=404, detail="Item not found")

    metadata = None
    template_name = "index.html"
    
    if full_path.is_dir():
        all_items, content, metadata = process_directory(full_path)
        date_created = None
        
        # Apply tag filter if specified
        if tag:
            all_items = [
                item for item in all_items
                if not item.is_dir and item.metadata and item.metadata.tags and tag in item.metadata.tags
            ]
        
        # Apply sort if specified
        if sort and all_items:
            if sort == "name":
                all_items.sort(key=lambda x: x.name.lower())
            elif sort == "name-desc":
                all_items.sort(key=lambda x: x.name.lower(), reverse=True)
            elif sort == "date":
                all_items.sort(key=lambda x: x.mtime)
            elif sort == "date-desc":
                all_items.sort(key=lambda x: x.mtime, reverse=True)
    else:
        try:
            if is_image(full_path):
                return FileResponse(full_path, media_type="image/jpeg")
                
            content, metadata = process_markdown_file_with_metadata(full_path)
            all_items = None
            date_created = get_file_creation_date(full_path)
            
            # Use post template for markdown files
            template_name = "post.html"
        except UnicodeDecodeError:
            logger.error(f"UnicodeDecodeError when processing file: {full_path}")
            return FileResponse(full_path, filename=full_path.name)

    breadcrumbs = generate_breadcrumbs(path)
    
    # Use metadata title if available, otherwise use breadcrumbs
    if metadata and metadata.title:
        page_title = metadata.title
    else:
        page_title = generate_title_from_breadcrumbs(breadcrumbs)
        
    has_images = any(item.is_image for item in all_items or [])

    # If in image gallery, consider randomizing
    if has_images and template_name == "index.html":
        # Separate images and non-images
        image_items = [item for item in all_items if item.is_image]
        non_image_items = [item for item in all_items if not item.is_image]
        
        # Randomize images
        random.shuffle(image_items)
        
        # Recombine
        all_items = non_image_items + image_items

    # Special handling for index page
    is_root = path == ""
    
    # Determine if we should use photo_browser for image-heavy directories
    if has_images and len([item for item in all_items if item.is_image]) > 5:
        template_name = "photo_browser.html"
        
    # Check for layout override in metadata
    if metadata and metadata.layout:
        template_name = f"{metadata.layout}.html"

    # If we're at root and using index.html, use directory.html template
    if is_root and template_name == "index.html":
        template_name = "directory.html"
        
    # Determine if we're in photos path
    is_photos = path.startswith("photos") or path.find("/photos") >= 0
    
    return templates.TemplateResponse(
        template_name,
        {
            "title": page_title,
            "request": request,
            "breadcrumbs": breadcrumbs,
            "files": all_items,
            "content": content,
            "date_created": date_created,
            "has_images": has_images,
            "is_root": is_root,
            "is_photos": is_photos,
            "metadata": metadata,
            "path": path,
            "tag_filter": tag,
            "sort": sort,
        },
    )


@app.exception_handler(500)
async def custom_404_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

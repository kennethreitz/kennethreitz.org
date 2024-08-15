# The Source Code

Instead of creating a public GitHub repository, I decided to host the source code for this website on my own server.
This way, I can keep the code private and make changes without worrying about breaking anything.

I've written some about the tech stack I'm using [here](/essays/2024/hello).


## Source Code

Here is the source code for the main engine of this website:

```python
import logging
import os
import pathlib
import random
import re
import shutil
import tempfile
import zipfile
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional, Tuple

import background
import boto3
import mistune
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
BUCKET_NAME = os.environ["BUCKET_NAME"]
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
    title="Markdown Browser API",
    description="API for browsing markdown content",
    version="1.0.0",
    lifespan=lifespan,
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
    plugins=["table", "url", "strikethrough", "footnotes"], escape=False
)


# Models
class FileInfo(BaseModel):
    name: str = Field(..., description="Name of the file or directory")
    url: str = Field(..., description="URL path to the file or directory")
    title: Optional[str] = Field(
        None, description="Title of the file or directory, if available"
    )
    ctime: float = Field(..., description="Creation time of the file or directory")
    is_dir: bool = Field(..., description="Whether the item is a directory")
    is_image: bool = Field(False, description="Whether the item is an image")
    exif_data: Optional[dict] = Field(None, description="EXIF data for image files")


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
        if item.name in [".DS_Store", "index.md"]:
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

    all_items.sort(key=lambda x: (not x.is_dir, x.name.lower()))

    index_file = full_path / "index.md"
    content = process_markdown_file(index_file) if index_file.exists() else None

    logger.info(f"Processed {len(all_items)} items in directory: {full_path}")
    return all_items, content


def process_markdown_file(file_path: pathlib.Path) -> str:
    logger.info(f"Processing markdown file: {file_path}")
    with file_path.open("r", encoding="utf-8") as f:
        markdown_content = f.read()
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


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/{path:path}", response_class=HTMLResponse, include_in_schema=False)
async def browse(request: Request, path: str = ""):
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
            logger.error(f"Path not found: {full_path}")
            raise HTTPException(status_code=404, detail="Item not found")

    if full_path.is_dir():
        all_items, content = process_directory(full_path)
        date_created = None
    else:
        try:
            if is_image(full_path):
                return FileResponse(full_path, media_type="image/jpeg")
            content = process_markdown_file(full_path)
            all_items = None
            date_created = get_file_creation_date(full_path)
        except UnicodeDecodeError:
            logger.error(f"UnicodeDecodeError when processing file: {full_path}")
            return FileResponse(full_path, filename=full_path.name)

    breadcrumbs = generate_breadcrumbs(path)
    page_title = generate_title_from_breadcrumbs(breadcrumbs)
    has_images = any(item.is_image for item in all_items or [])

    if has_images:
        random.shuffle(all_items or [])

    return templates.TemplateResponse(
        "index.html",
        {
            "title": page_title,
            "request": request,
            "breadcrumbs": breadcrumbs,
            "files": all_items,
            "content": content,
            "date_created": date_created,
            "has_images": has_images,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Notes

- There are hacks in places, and I'm not proud of them, but it works for now. I'll clean it up later.
- Claude 3.5 Sonnet wrote most of the code for this, with my direction.
- The biggest challenge with hosting this site is the [11,000 images](/photos) it contains.

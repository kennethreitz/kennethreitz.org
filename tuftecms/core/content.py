"""Content processing core functionality."""

from pathlib import Path
import random


class ContentProcessor:
    """Process and manage content operations."""

    def __init__(self, data_dir="data"):
        """Initialize content processor."""
        self.data_dir = Path(data_dir)

    def get_random_post(self):
        """Get a random post from essays."""
        essays_dir = self.data_dir / "essays"
        if not essays_dir.exists():
            return None

        md_files = list(essays_dir.glob("*.md"))
        if md_files:
            return random.choice(md_files)
        return None

    def get_random_from_collection(self, collection):
        """Get a random post from a specific collection."""
        collection_dir = self.data_dir / collection
        if not collection_dir.exists():
            return None

        md_files = list(collection_dir.glob("**/*.md"))
        md_files = [f for f in md_files if f.name != "index.md"]

        if md_files:
            return random.choice(md_files)
        return None

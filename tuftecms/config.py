"""Configuration module for TufteCMS."""

import os


class Config:
    """Base configuration."""

    # Flask settings
    DISABLE_ANALYTICS = os.environ.get("DISABLE_ANALYTICS", "false").lower() == "true"

    # Cache settings
    SEARCH_CACHE_TIMEOUT = 60
    CACHE_KEY_PREFIX = "tuftecms_"

    # Content settings
    DATA_DIR = "data"
    TEMPLATES_DIR = "templates"

    # Search settings
    MIN_SEARCH_QUERY_LENGTH = 2
    MAX_SEARCH_RESULTS = 50

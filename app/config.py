"""Configuration constants for the image analysis service."""

import os
from pathlib import Path

# File size limits
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
}

# MIME type to file extension mapping
MIME_TO_EXTENSION = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
}

# Storage paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
ANALYSIS_DIR = DATA_DIR / "analysis"

# Ensure directories exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


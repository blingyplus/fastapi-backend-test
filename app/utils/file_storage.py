"""Filesystem operations for image and analysis storage."""

import json
from pathlib import Path
from typing import Optional

from app.config import IMAGES_DIR, ANALYSIS_DIR, MIME_TO_EXTENSION


def save_image(image_id: str, content: bytes, extension: str) -> Path:
    """
    Save image file to filesystem.

    Args:
        image_id: Unique image identifier
        content: Image file content as bytes
        extension: File extension (e.g., 'jpg', 'png')

    Returns:
        Path to saved image file
    """
    file_path = IMAGES_DIR / f"{image_id}.{extension}"
    file_path.write_bytes(content)
    return file_path


def image_exists(image_id: str) -> bool:
    """
    Check if image exists in storage.

    Args:
        image_id: Image identifier to check

    Returns:
        True if image exists, False otherwise
    """
    for ext in MIME_TO_EXTENSION.values():
        file_path = IMAGES_DIR / f"{image_id}.{ext}"
        if file_path.exists():
            return True
    return False


def get_image_path(image_id: str) -> Optional[Path]:
    """
    Get path to image file if it exists.

    Args:
        image_id: Image identifier

    Returns:
        Path to image file if exists, None otherwise
    """
    for ext in MIME_TO_EXTENSION.values():
        file_path = IMAGES_DIR / f"{image_id}.{ext}"
        if file_path.exists():
            return file_path
    return None


def save_analysis_result(image_id: str, result: dict) -> Path:
    """
    Save analysis result to filesystem as JSON.

    Args:
        image_id: Image identifier
        result: Analysis result dictionary

    Returns:
        Path to saved analysis file
    """
    file_path = ANALYSIS_DIR / f"{image_id}.json"
    file_path.write_text(json.dumps(result, indent=2))
    return file_path


def load_analysis_result(image_id: str) -> Optional[dict]:
    """
    Load analysis result from filesystem.

    Args:
        image_id: Image identifier

    Returns:
        Analysis result dictionary if exists, None otherwise
    """
    file_path = ANALYSIS_DIR / f"{image_id}.json"
    if not file_path.exists():
        return None

    try:
        content = file_path.read_text()
        return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return None


"""Validation utilities for file uploads."""

from app.config import ALLOWED_MIME_TYPES, MAX_FILE_SIZE


def validate_mime_type(mime_type: str) -> bool:
    """
    Validate if MIME type is allowed.

    Args:
        mime_type: MIME type string to validate

    Returns:
        True if MIME type is allowed, False otherwise
    """
    return mime_type.lower() in ALLOWED_MIME_TYPES


def validate_file_size(size: int) -> bool:
    """
    Validate if file size is within limits.

    Args:
        size: File size in bytes

    Returns:
        True if file size is within limits, False otherwise
    """
    return 0 < size <= MAX_FILE_SIZE


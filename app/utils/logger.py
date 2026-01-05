"""Logging configuration and utilities."""

import logging
import sys

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("image_analysis_service")


def log_request(method: str, path: str, status_code: int = None):
    """Log HTTP request."""
    if status_code:
        logger.info(f"Request: {method} {path} - Status: {status_code}")
    else:
        logger.info(f"Request: {method} {path}")


def log_image_upload(image_id: str, file_size: int, mime_type: str):
    """Log successful image upload."""
    logger.info(
        f"Image uploaded - image_id: {image_id}, size: {file_size} bytes, type: {mime_type}"
    )


def log_analysis(image_id: str, cached: bool = False):
    """Log analysis operation."""
    if cached:
        logger.info(f"Analysis retrieved from cache - image_id: {image_id}")
    else:
        logger.info(f"Analysis performed - image_id: {image_id}")


def log_error(operation: str, error: str, image_id: str = None):
    """Log error with context."""
    context = f"image_id: {image_id}, " if image_id else ""
    logger.error(f"Error in {operation} - {context}error: {error}")


"""Image upload and storage service."""

from fastapi import UploadFile

from app.config import MIME_TO_EXTENSION
from app.services.exceptions import FileTooLargeError, InvalidFileTypeError
from app.utils.file_storage import save_image
from app.utils.id_generator import generate_image_id
from app.utils.validators import validate_file_size, validate_mime_type


def process_upload(file: UploadFile) -> str:
    """
    Process and save uploaded image file.

    Args:
        file: FastAPI UploadFile object

    Returns:
        Generated image_id

    Raises:
        InvalidFileTypeError: If MIME type is not allowed
        FileTooLargeError: If file size exceeds maximum
    """
    # Validate MIME type
    mime_type = file.content_type or ""
    if not validate_mime_type(mime_type):
        raise InvalidFileTypeError(f"Invalid file type: {mime_type}")

    # Read file content
    content = file.file.read()
    file_size = len(content)

    # Validate file size
    if not validate_file_size(file_size):
        raise FileTooLargeError(f"File size {file_size} exceeds maximum allowed size")

    # Generate image ID
    image_id = generate_image_id()

    # Extract extension from MIME type
    extension = MIME_TO_EXTENSION.get(mime_type.lower(), "jpg")

    # Save image to filesystem
    save_image(image_id, content, extension)

    return image_id


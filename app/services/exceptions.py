"""Custom exceptions for the image analysis service."""


class InvalidFileTypeError(Exception):
    """Raised when file type is not allowed."""

    pass


class FileTooLargeError(Exception):
    """Raised when file size exceeds maximum allowed size."""

    pass


class ImageNotFoundError(Exception):
    """Raised when image with given ID is not found."""

    pass


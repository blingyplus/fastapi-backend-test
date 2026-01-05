"""ID generation utilities."""

import uuid


def generate_image_id() -> str:
    """
    Generate a unique image identifier.

    Returns:
        UUID4 string as image identifier
    """
    return str(uuid.uuid4())


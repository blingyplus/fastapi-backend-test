"""Image analysis service with idempotent analysis logic."""

import hashlib
import random

from app.services.exceptions import ImageNotFoundError
from app.utils.file_storage import image_exists, load_analysis_result, save_analysis_result

# Mock analysis data
SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal"]
ISSUES = ["Hyperpigmentation", "Acne", "Wrinkles", "Redness", "Dark Spots"]


def _generate_deterministic_analysis(image_id: str) -> dict:
    """
    Generate deterministic analysis results based on image_id hash.

    Args:
        image_id: Image identifier

    Returns:
        Analysis result dictionary
    """
    # Create deterministic seed from image_id hash
    hash_obj = hashlib.md5(image_id.encode())
    seed = int(hash_obj.hexdigest(), 16) % (2**32)
    rng = random.Random(seed)

    # Select skin type deterministically
    skin_type = rng.choice(SKIN_TYPES)

    # Select 1-3 issues deterministically
    num_issues = rng.randint(1, 3)
    selected_issues = rng.sample(ISSUES, num_issues)

    # Generate confidence score (0.7-0.95 range)
    confidence = 0.7 + (rng.random() * 0.25)

    return {
        "image_id": image_id,
        "skin_type": skin_type,
        "issues": selected_issues,
        "confidence": round(confidence, 2),
    }


def analyze_image(image_id: str) -> dict:
    """
    Analyze image with idempotent behavior.

    If analysis result exists, return cached result.
    Otherwise, perform mock analysis and save result.

    Args:
        image_id: Image identifier to analyze

    Returns:
        Analysis result dictionary

    Raises:
        ImageNotFoundError: If image with given ID does not exist
    """
    # Check if analysis result already exists (idempotency)
    cached_result = load_analysis_result(image_id)
    if cached_result is not None:
        return cached_result

    # Verify image exists
    if not image_exists(image_id):
        raise ImageNotFoundError(f"Image with ID {image_id} not found")

    # Generate deterministic analysis
    result = _generate_deterministic_analysis(image_id)

    # Save result for future idempotent calls
    save_analysis_result(image_id, result)

    return result


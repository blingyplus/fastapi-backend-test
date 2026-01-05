"""Image analysis endpoint."""

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from app.services.analysis_service import analyze_image
from app.services.exceptions import ImageNotFoundError

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post(
    "",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Image not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def analyze_image_endpoint(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze an uploaded image.

    Performs mock AI-style analysis and returns structured results.
    Analysis is idempotent: repeated calls with the same image_id return the same result.
    """
    try:
        result = analyze_image(request.image_id)
        return AnalyzeResponse(**result)
    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


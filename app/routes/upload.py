"""Image upload endpoint."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.schemas import ErrorResponse, UploadResponse
from app.services.exceptions import FileTooLargeError, InvalidFileTypeError
from app.services.image_service import process_upload
from app.utils.logger import log_error, log_request

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type"},
        413: {"model": ErrorResponse, "description": "File too large"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload an image file.

    Accepts JPEG and PNG images up to 5MB.
    Returns a unique image_id for the uploaded image.
    """
    log_request("POST", "/upload")
    try:
        image_id = process_upload(file)
        log_request("POST", "/upload", status.HTTP_201_CREATED)
        return UploadResponse(image_id=image_id)
    except InvalidFileTypeError as e:
        log_error("upload", str(e))
        log_request("POST", "/upload", status.HTTP_400_BAD_REQUEST)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except FileTooLargeError as e:
        log_error("upload", str(e))
        log_request("POST", "/upload", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )
    except Exception as e:
        log_error("upload", str(e))
        log_request("POST", "/upload", status.HTTP_500_INTERNAL_SERVER_ERROR)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


"""Pydantic models for request and response schemas."""

from typing import List
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response model for image upload endpoint."""

    image_id: str = Field(..., description="Unique identifier for the uploaded image")


class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint."""

    image_id: str = Field(..., description="Image identifier to analyze")


class AnalyzeResponse(BaseModel):
    """Response model for analysis endpoint."""

    image_id: str = Field(..., description="Image identifier")
    skin_type: str = Field(..., description="Detected skin type")
    issues: List[str] = Field(..., description="List of detected skin issues")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(..., description="Error message")
    detail: str = Field(default="", description="Additional error details")


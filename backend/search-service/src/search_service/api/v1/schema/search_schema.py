"""API schemas for search endpoints."""

from typing import List

from pydantic import BaseModel, Field


class SearchResultItemSchema(BaseModel):
    """Single search result item."""
    object_name: str = Field(..., description="S3 object name for the image")
    image_filename: str = Field(..., description="Original filename of the image")
    image_url: str = Field(..., description="URL to retrieve the image")
    user_id: str = Field(..., description="ID of the user who uploaded the image")
    score: float = Field(..., description="Similarity score (higher is better)")
    point_id: str = Field(..., description="Qdrant point ID")


class SearchResponseSchema(BaseModel):
    """Search response with results and metadata."""
    query: str = Field(..., description="Original search query")
    items: List[SearchResultItemSchema] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results returned")


class SearchRequestSchema(BaseModel):
    """Search request."""
    query: str = Field(..., description="Text description to search for", min_length=1)
    limit: int = Field(20, description="Maximum number of results to return", ge=1, le=100)
    user_id: str | None = Field(None, description="Optional user ID to filter results")


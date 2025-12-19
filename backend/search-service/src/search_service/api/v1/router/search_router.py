"""Search API router."""

from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request, status

from search_service.api.v1.schema import (
    SearchRequestSchema,
    SearchResponseSchema,
    SearchResultItemSchema,
)
from search_service.app.dependency import get_search_service
from search_service.config import config
from search_service.core.interface.service.search_service import SearchService

search_router = APIRouter()


@search_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Search images by text description",
    response_model=SearchResponseSchema,
)
async def search_images(
    payload: SearchRequestSchema,
    request: Request,
    search_service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponseSchema:
    """
    Search for images by text description using CLIP embeddings.
    
    The service will:
    1. Convert the text query to a vector embedding using CLIP
    2. Search for similar image embeddings in Qdrant vector database
    3. Return matching images sorted by similarity score with URLs to retrieve them
    """
    result = await search_service.search_images(
        query=payload.query,
        limit=payload.limit,
        user_id=payload.user_id,
    )
    
    # Generate base URL for image retrieval
    base_url = str(request.base_url).rstrip("/")
    image_base_path = f"{base_url}{config.api.prefix}{config.api.v1.prefix}/images"
    
    return SearchResponseSchema(
        query=result.query,
        items=[
            SearchResultItemSchema(
                object_name=item.object_name,
                image_filename=item.image_filename,
                image_url=f"{image_base_path}/{quote(item.object_name, safe='')}",
                user_id=item.user_id,
                score=item.score,
                point_id=item.point_id,
            )
            for item in result.items
        ],
        total_results=result.total_results,
    )


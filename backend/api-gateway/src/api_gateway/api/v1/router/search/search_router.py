"""Search API router for API Gateway."""

import logging

from fastapi import APIRouter, Depends, status

from api_gateway.api.dependency import SearchApiServiceDep, get_current_user_id_from_token
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.auth import TokenValidationResponse
from api_gateway.api.v1.schema.search import SearchRequestSchema, SearchResponseSchema

logger = logging.getLogger(__name__)

search_router = APIRouter(tags=[ApiTags.SEARCH])


@search_router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Search images by text description",
    description="Search for images by text query using CLIP embeddings. Requires authentication.",
    response_model=SearchResponseSchema,
)
async def search_images(
    payload: SearchRequestSchema,
    search_service: SearchApiServiceDep,
    token_data: TokenValidationResponse = Depends(require_roles("User", "Admin", "Moderator")),
) -> SearchResponseSchema:
    """Search for images by text description."""
    user_id = get_current_user_id_from_token(token_data) if payload.user_id is None else payload.user_id
    
    logger.info(
        f"User {user_id} searching images",
        extra={"query": payload.query[:100], "limit": payload.limit}
    )
    
    result = await search_service.search_images(
        query=payload.query,
        limit=payload.limit,
        user_id=user_id if payload.user_id else None,
    )
    
    logger.info(
        f"Search completed for user {user_id}",
        extra={"results_count": result.get('total_results', 0)}
    )
    
    return result


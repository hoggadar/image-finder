import logging
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request, status

from api_gateway.api.dependency import SearchApiServiceDep, get_current_user_id_from_token
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.auth import TokenValidationResponse
from api_gateway.api.v1.schema.search import SearchRequestSchema, SearchResponseSchema, SearchResultItemSchema
from api_gateway.config import config

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
    request: Request,
    search_service: SearchApiServiceDep,
    token_data: TokenValidationResponse = Depends(require_roles("User", "Admin", "Moderator")),
) -> SearchResponseSchema:
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
    
    base_url_str = str(request.base_url)
    if "://" in base_url_str:
        scheme = base_url_str.split("://")[0]
        host_part = base_url_str.split("://")[1].split("/")[0]
        if ":" in host_part:
            hostname = host_part.split(":")[0]
        else:
            hostname = host_part
        image_base_path = f"{scheme}://{hostname}:4040{config.api.prefix}{config.api.v1.prefix}/images"
    else:
        image_base_path = f"http://localhost:4040{config.api.prefix}{config.api.v1.prefix}/images"
    
    items = []
    for item in result.get('items', []):
        object_name = item.get('object_name', '')
        items.append(
            SearchResultItemSchema(
                object_name=object_name,
                image_filename=item.get('image_filename', ''),
                image_url=f"{image_base_path}/{quote(object_name, safe='')}",
                user_id=item.get('user_id', ''),
                score=item.get('score', 0.0),
                point_id=item.get('point_id', ''),
            )
        )
    
    logger.info(
        f"Search completed for user {user_id}",
        extra={"results_count": result.get('total_results', 0)}
    )
    
    return SearchResponseSchema(
        query=result.get('query', ''),
        items=items,
        total_results=result.get('total_results', 0),
    )


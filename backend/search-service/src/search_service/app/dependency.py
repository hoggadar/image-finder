"""Dependencies for services."""

from functools import lru_cache

from search_service.app.service.clip_api_service import ClipApiServiceImpl
from search_service.app.service.search_service import SearchServiceImpl
from search_service.config import config
from search_service.core.interface.service.search_service import SearchService
from search_service.infrastructure.qdrant_search_service import qdrant_search_service


@lru_cache
def get_clip_api_service() -> ClipApiServiceImpl:
    """Get CLIP API service instance."""
    clip_service = next(
        (s for s in config.services if s.name == "clip-service"), None
    )
    if not clip_service:
        raise RuntimeError("CLIP service configuration not found")
    
    endpoints = {endpoint.name: endpoint.service_path for endpoint in clip_service.endpoints}
    
    return ClipApiServiceImpl(
        base_url=clip_service.base_url,
        endpoints=endpoints,
        timeout=30.0,
        max_retries=3,
        retry_delay=2.0,
    )


@lru_cache
def get_search_service() -> SearchService:
    """Get search service instance."""
    return SearchServiceImpl(
        clip_service=get_clip_api_service(),
        vector_search_service=qdrant_search_service,
    )


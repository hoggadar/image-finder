"""Dependencies for services."""

from functools import lru_cache

from vector_loader_service.app.service.clip_api_service import ClipApiServiceImpl
from vector_loader_service.config import config


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
        timeout=60.0,
    )


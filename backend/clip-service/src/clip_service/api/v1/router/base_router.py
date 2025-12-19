from fastapi import APIRouter

from clip_service.config import config
from clip_service.api.v1.router.clip_router import clip_router
from clip_service.api.dependency import is_model_ready

router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(clip_router, prefix=config.api.v1.clip_prefix)


@router_v1.get("/health")
async def health_check():
    ready = is_model_ready()
    return {
        "status": "healthy",
        "model_ready": ready,
        "model_status": "ready" if ready else "loading"
    }

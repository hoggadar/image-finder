from fastapi import APIRouter

from clip_service.config import config
from clip_service.api.v1.router.clip_router import clip_router

router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(clip_router, prefix=config.api.v1.clip_prefix)

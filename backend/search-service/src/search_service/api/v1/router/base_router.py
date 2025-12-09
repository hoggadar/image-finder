"""API v1 routers."""

from fastapi import APIRouter

from search_service.config import config
from search_service.api.v1.router.image_router import image_router
from search_service.api.v1.router.search_router import search_router


router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(search_router, prefix=config.api.v1.search_prefix)
router_v1.include_router(image_router, prefix="/images")


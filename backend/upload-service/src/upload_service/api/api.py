from fastapi import APIRouter

from upload_service.api.v1.router.base_router import router_v1
from upload_service.config import config


router = APIRouter(prefix=config.api.prefix)
router.include_router(router_v1)


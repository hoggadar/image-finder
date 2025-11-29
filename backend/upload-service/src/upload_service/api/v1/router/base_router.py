from fastapi import APIRouter

from upload_service.api.v1.router.upload_router import upload_router
from upload_service.config import config


router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(upload_router, prefix=config.api.v1.upload_prefix)


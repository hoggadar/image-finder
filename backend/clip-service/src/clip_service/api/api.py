from fastapi import APIRouter

from clip_service.config import config
from clip_service.api.v1.router.base_router import router_v1


router = APIRouter(prefix="{}".format(config.api.prefix))

router.include_router(router_v1)

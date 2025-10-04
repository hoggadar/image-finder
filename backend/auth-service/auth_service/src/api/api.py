from fastapi import APIRouter

from auth_service.src.config import config
from auth_service.src.api.v1.router.base_router import router_v1


router = APIRouter(prefix="{}{}".format(config.api.prefix, config.api.service_prefix))

router.include_router(router_v1)


from fastapi import APIRouter

from src.auth_service.config import config
from src.auth_service.api.v1.router.base_router import router_v1


router = APIRouter(prefix="{}{}".format(config.api.prefix, config.api.service_prefix))

router.include_router(router_v1)


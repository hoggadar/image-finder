from fastapi import APIRouter

from api_gateway.config import config
from api_gateway.api.v1.router.base_router import router_v1


router = APIRouter(prefix="{}".format(config.api.prefix))
router.include_router(router_v1)


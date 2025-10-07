from fastapi import APIRouter

from auth_service.config import config
from auth_service.api.v1.router.auth_router import auth_router
from auth_service.api.v1.router.token_router import token_router
from auth_service.api.v1.router.user_router import user_router


router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(auth_router, prefix=config.api.v1.auth_prefix)
router_v1.include_router(token_router, prefix=config.api.v1.token_prefix)
router_v1.include_router(user_router, prefix=config.api.v1.user_prefix)

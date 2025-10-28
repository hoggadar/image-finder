from fastapi import APIRouter

from auth_service.config import config
from auth_service.api.v1.router.auth_router import auth_router
from auth_service.api.v1.router.user_router import user_router
from auth_service.api.v1.router.role_router import role_router


router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(auth_router, prefix=config.api.v1.auth_prefix)
router_v1.include_router(user_router, prefix=config.api.v1.user_prefix)
router_v1.include_router(role_router, prefix=config.api.v1.role_prefix)

from fastapi import APIRouter

from api_gateway.config import config
from api_gateway.api.v1.router.auth import auth_router, role_router, user_router
from api_gateway.api.v1.router.clip import clip_router
from api_gateway.api.v1.router.upload import upload_router
from api_gateway.api.v1.router.search import search_router


router_v1 = APIRouter(prefix=config.api.v1.prefix)

router_v1.include_router(clip_router, prefix="/clip")
router_v1.include_router(auth_router, prefix="/auth")
router_v1.include_router(user_router, prefix="/user")
router_v1.include_router(role_router, prefix="/role")
router_v1.include_router(upload_router, prefix="/upload")
router_v1.include_router(search_router, prefix="/search")

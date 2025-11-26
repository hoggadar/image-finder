from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Dict

from fastapi import Depends, Request

from api_gateway.app.service.auth.auth_api_service import AuthApiServiceImpl
from api_gateway.app.service.auth.role_api_service import RoleApiServiceImpl
from api_gateway.app.service.auth.user_api_service import UserApiServiceImpl
from api_gateway.app.service.clip_api_service import ClipApiServiceImpl
from api_gateway.app.service.upload_api_service import UploadApiServiceImpl
from api_gateway.app.service.search_api_service import SearchApiServiceImpl
from api_gateway.config import config, ServiceConfig


def _find_service_config(name: str) -> ServiceConfig:
    for service in config.services:
        if service.name == name:
            return service
    raise RuntimeError(f"Service configuration for '{name}' not found")


def _build_endpoints_map(service_cfg: ServiceConfig) -> Dict[str, str]:
    return {endpoint.name: endpoint.service_path for endpoint in service_cfg.endpoints}


@lru_cache
def get_auth_api_service() -> AuthApiServiceImpl:
    service_cfg = _find_service_config("auth-service")
    endpoints = _build_endpoints_map(service_cfg)
    return AuthApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


@lru_cache
def get_user_api_service() -> UserApiServiceImpl:
    service_cfg = _find_service_config("auth-service")
    endpoints = _build_endpoints_map(service_cfg)
    return UserApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


@lru_cache
def get_role_api_service() -> RoleApiServiceImpl:
    service_cfg = _find_service_config("auth-service")
    endpoints = _build_endpoints_map(service_cfg)
    return RoleApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


@lru_cache
def get_clip_api_service() -> ClipApiServiceImpl:
    service_cfg = _find_service_config("clip-service")
    endpoints = _build_endpoints_map(service_cfg)
    return ClipApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


@lru_cache
def get_upload_api_service() -> UploadApiServiceImpl:
    service_cfg = _find_service_config("upload-service")
    endpoints = _build_endpoints_map(service_cfg)
    return UploadApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


@lru_cache
def get_search_api_service() -> SearchApiServiceImpl:
    service_cfg = _find_service_config("search-service")
    endpoints = _build_endpoints_map(service_cfg)
    return SearchApiServiceImpl(base_url=service_cfg.base_url, endpoints=endpoints)


async def get_current_user_id(
    request: Request,
    auth_service: AuthApiServiceImpl = Depends(get_auth_api_service),
) -> str:
    """
    Извлечь user_id из токена в заголовке Authorization.
    
    Эта функция должна использоваться после декоратора @require_roles,
    который уже проверил валидность токена.
    """
    from api_gateway.api.v1.schema.auth import ValidateTokenSchema
    from fastapi import HTTPException, status
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or malformed"
        )
    
    token = auth_header.split(" ", 1)[1].strip()
    # Валидируем токен с пустой ролью, чтобы просто получить user_id
    # (требуется только валидный токен, роль не важна)
    schema = ValidateTokenSchema(access_token=token, required_role="")
    try:
        response = await auth_service.validate_token(schema)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to validate token"
        ) from e
    
    if not response.is_valid or not response.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or user_id not found"
        )
    
    return response.user_id


AuthApiServiceDep = Annotated[AuthApiServiceImpl, Depends(get_auth_api_service)]
UserApiServiceDep = Annotated[UserApiServiceImpl, Depends(get_user_api_service)]
RoleApiServiceDep = Annotated[RoleApiServiceImpl, Depends(get_role_api_service)]
ClipApiServiceDep = Annotated[ClipApiServiceImpl, Depends(get_clip_api_service)]
UploadApiServiceDep = Annotated[UploadApiServiceImpl, Depends(get_upload_api_service)]
SearchApiServiceDep = Annotated[SearchApiServiceImpl, Depends(get_search_api_service)]
CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]


__all__ = [
    "AuthApiServiceDep",
    "UserApiServiceDep",
    "RoleApiServiceDep",
    "ClipApiServiceDep",
    "UploadApiServiceDep",
    "SearchApiServiceDep",
    "CurrentUserIdDep",
    "get_auth_api_service",
    "get_user_api_service",
    "get_role_api_service",
    "get_clip_api_service",
    "get_upload_api_service",
    "get_search_api_service",
    "get_current_user_id",
]

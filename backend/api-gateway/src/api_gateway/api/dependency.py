from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Dict, TYPE_CHECKING

from fastapi import Depends, HTTPException, status

from api_gateway.app.service.auth.auth_api_service import AuthApiServiceImpl
from api_gateway.app.service.auth.role_api_service import RoleApiServiceImpl
from api_gateway.app.service.auth.user_api_service import UserApiServiceImpl
from api_gateway.app.service.clip_api_service import ClipApiServiceImpl
from api_gateway.app.service.upload_api_service import UploadApiServiceImpl
from api_gateway.app.service.search_api_service import SearchApiServiceImpl
from api_gateway.config import config, ServiceConfig

if TYPE_CHECKING:
    from api_gateway.api.v1.schema.auth import TokenValidationResponse


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
    token_data: "TokenValidationResponse" = Depends(lambda: None),
) -> str:
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token validation not performed. Use require_roles or get_token_payload first."
        )
    
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    
    return token_data.user_id


def get_current_user_id_from_token(
    token_data: "TokenValidationResponse",
) -> str:
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    
    return token_data.user_id


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
    "get_current_user_id_from_token",
]

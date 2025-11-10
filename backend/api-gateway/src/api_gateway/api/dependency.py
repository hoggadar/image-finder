from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Dict

from fastapi import Depends

from api_gateway.app.service.auth.auth_api_service import AuthApiServiceImpl
from api_gateway.app.service.auth.role_api_service import RoleApiServiceImpl
from api_gateway.app.service.auth.user_api_service import UserApiServiceImpl
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


AuthApiServiceDep = Annotated[AuthApiServiceImpl, Depends(get_auth_api_service)]
UserApiServiceDep = Annotated[UserApiServiceImpl, Depends(get_user_api_service)]
RoleApiServiceDep = Annotated[RoleApiServiceImpl, Depends(get_role_api_service)]


__all__ = [
    "AuthApiServiceDep",
    "UserApiServiceDep",
    "RoleApiServiceDep",
    "get_auth_api_service",
    "get_user_api_service",
    "get_role_api_service",
]


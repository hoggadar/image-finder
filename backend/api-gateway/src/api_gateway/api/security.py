from __future__ import annotations

from functools import wraps
from typing import Iterable

from fastapi import Depends, HTTPException, Request, status

from api_gateway.api.dependency import get_auth_api_service
from api_gateway.api.v1.schema.auth import ValidateTokenSchema
from api_gateway.core.interface.service.auth import AuthApiService


def _role_guard_factory(roles_to_check: Iterable[str]):
    async def dependency(
        request: Request,
        auth_service: AuthApiService = Depends(get_auth_api_service),
    ) -> None:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or malformed",
            )

        token = auth_header.split(" ", 1)[1].strip()
        last_error_detail: str | None = None

        for role in roles_to_check:
            schema = ValidateTokenSchema(access_token=token, required_role=role)
            response = await auth_service.validate_token(schema)

            if not response.is_valid:
                last_error_detail = response.message or "Invalid or expired token"
                continue

            if response.has_required_role:
                return

            last_error_detail = response.message or "Insufficient permissions"

        if last_error_detail == "Invalid or expired token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=last_error_detail,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=last_error_detail or "Insufficient permissions",
        )

    return dependency


def require_roles(*roles: str):
    """Decorator enforcing that the requester possesses at least one of the given roles."""

    roles_to_check: Iterable[str] = roles or ("",)
    dependency = Depends(_role_guard_factory(roles_to_check))

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, role_check=dependency, **kwargs):  # noqa: B008 - dependency placeholder
            return await func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["require_roles"]


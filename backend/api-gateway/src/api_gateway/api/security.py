from __future__ import annotations

import logging
from functools import wraps
from inspect import Parameter, Signature, signature
from typing import Iterable

from fastapi import Depends, HTTPException, Request, status

from api_gateway.api.dependency import get_auth_api_service
from api_gateway.api.v1.schema.auth import ValidateTokenSchema
from api_gateway.core.interface.service.auth import AuthApiService


logger = logging.getLogger(__name__)


def _build_role_guard(roles_to_check: Iterable[str]):
    async def role_guard(
        request: Request,
        auth_service: AuthApiService = Depends(get_auth_api_service),
    ) -> None:
        auth_header = request.headers.get("Authorization")
        headers_snapshot = {
            key: (value if key.lower() != "authorization" else "Bearer ***")
            for key, value in request.headers.items()
        }
        query_string = str(request.url.query) if request.url.query else ""

        logger.debug(
            "Role guard invoked",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query": query_string,
                "headers": headers_snapshot,
                "required_roles": list(roles_to_check),
            },
        )

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.debug(
                "Authorization header missing or malformed",
                extra={"path": request.url.path, "query": query_string},
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or malformed",
            )

        token = auth_header.split(" ", 1)[1].strip()
        last_error_detail: str | None = None

        for role in roles_to_check:
            logger.debug(
                "Validating token against required role",
                extra={"role": role, "path": request.url.path, "query": query_string},
            )
            schema = ValidateTokenSchema(access_token=token, required_role=role)
            try:
                response = await auth_service.validate_token(schema)
            except Exception:
                logger.exception(
                    "Auth service validation request failed",
                    extra={"role": role, "path": request.url.path, "query": query_string},
                )
                raise

            response_dump = response.model_dump()

            if not response.is_valid:
                last_error_detail = response.message or "Invalid or expired token"
                logger.debug(
                    "Token validation failed",
                    extra={
                        "role": role,
                        "path": request.url.path,
                        "query": query_string,
                        "detail": last_error_detail,
                        "validation_result": response_dump,
                    },
                )
                continue

            if response.has_required_role:
                logger.debug(
                    "Access granted by role guard",
                    extra={
                        "role": role,
                        "path": request.url.path,
                        "query": query_string,
                        "validation_result": response_dump,
                    },
                )
                return

            last_error_detail = response.message or "Insufficient permissions"
            logger.debug(
                "Token does not satisfy required role",
                extra={
                    "role": role,
                    "path": request.url.path,
                    "query": query_string,
                    "detail": last_error_detail,
                    "validation_result": response_dump,
                },
            )

        if last_error_detail == "Invalid or expired token":
            logger.debug(
                "Access denied: token invalid or expired",
                extra={"path": request.url.path, "query": query_string, "detail": last_error_detail},
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=last_error_detail,
            )

        logger.debug(
            "Access denied: insufficient permissions",
            extra={"path": request.url.path, "query": query_string, "detail": last_error_detail},
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=last_error_detail or "Insufficient permissions",
        )

    return role_guard


def require_roles(*roles: str):
    """Decorator enforcing that the requester possesses at least one of the given roles."""

    roles_to_check: Iterable[str] = roles or ("",)
    dependency = Depends(_build_role_guard(roles_to_check))

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs.pop("__role_guard", None)
            return await func(*args, **kwargs)

        # Extend signature with the dependency parameter to let FastAPI inject it
        sig: Signature = signature(func)
        params = list[Parameter](sig.parameters.values())
        params.append(
            Parameter(
                "__role_guard",
                kind=Parameter.KEYWORD_ONLY,
                default=dependency,
            )
        )
        wrapper.__signature__ = sig.replace(parameters=params)

        return wrapper

    return decorator


__all__ = ["require_roles"]


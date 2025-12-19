from __future__ import annotations

import logging
from typing import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api_gateway.api.dependency import get_auth_api_service
from api_gateway.api.v1.schema.auth import TokenValidationResponse, ValidateTokenSchema
from api_gateway.core.interface.service.auth import AuthApiService


logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(
    scheme_name="Bearer",
    description="Введите JWT токен",
    auto_error=True,
)


async def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthApiService = Depends(get_auth_api_service),
) -> TokenValidationResponse:
    token = credentials.credentials
    
    logger.debug(
        "Token validation requested",
        extra={"token_prefix": token[:10] if len(token) > 10 else "***"},
    )

    schema = ValidateTokenSchema(access_token=token, required_role="")
    
    try:
        response = await auth_service.validate_token(schema)
    except Exception:
        logger.exception("Auth service validation request failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )

    if not response.is_valid:
        error_detail = response.message or "Invalid or expired token"
        logger.debug(
            "Token validation failed",
            extra={"detail": error_detail},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail,
        )

    logger.debug(
        "Token validated successfully",
        extra={
            "user_id": response.user_id,
            "role": response.role,
        },
    )

    return response


def require_roles(*roles: str):
    roles_to_check: Iterable[str] = roles or ("",)

    async def role_guard(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        auth_service: AuthApiService = Depends(get_auth_api_service),
    ) -> TokenValidationResponse:
        token = credentials.credentials
        last_error_detail: str | None = None
        last_response: TokenValidationResponse | None = None

        logger.debug(
            "Role guard invoked",
            extra={
                "required_roles": list(roles_to_check),
                "token_prefix": token[:10] if len(token) > 10 else "***",
            },
        )

        for role in roles_to_check:
            logger.debug(
                "Validating token against required role",
                extra={"role": role},
            )
            
            schema = ValidateTokenSchema(access_token=token, required_role=role)
            
            try:
                response = await auth_service.validate_token(schema)
            except Exception:
                logger.exception(
                    "Auth service validation request failed",
                    extra={"role": role},
                )
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service unavailable",
                )

            last_response = response
            response_dump = response.model_dump()

            if not response.is_valid:
                last_error_detail = response.message or "Invalid or expired token"
                logger.debug(
                    "Token validation failed",
                    extra={
                        "role": role,
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
                        "user_id": response.user_id,
                        "validation_result": response_dump,
                    },
                )
                return response

            last_error_detail = response.message or "Insufficient permissions"
            logger.debug(
                "Token does not satisfy required role",
                extra={
                    "role": role,
                    "detail": last_error_detail,
                    "validation_result": response_dump,
                },
            )

        if last_error_detail == "Invalid or expired token":
            logger.debug(
                "Access denied: token invalid or expired",
                extra={"detail": last_error_detail},
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=last_error_detail,
            )

        logger.debug(
            "Access denied: insufficient permissions",
            extra={
                "detail": last_error_detail,
                "user_role": last_response.role if last_response else None,
                "required_roles": list(roles_to_check),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=last_error_detail or "Insufficient permissions",
        )

    return role_guard


__all__ = ["require_roles", "get_token_payload", "http_bearer"]


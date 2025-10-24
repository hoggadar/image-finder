import uuid
import jwt
import secrets

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from auth_service.config import config
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.core.interface.service.token_service import TokenService
from auth_service.core.interface.service.user_service import UserService
from auth_service.core.dto.token_dto import TokenPayload
from auth_service.api.v1.schema.user_schema import CreateUserSchema, UserSchema
from auth_service.api.v1.schema.auth_schema import LoginSchema, SignupSchema
from auth_service.api.v1.schema.token_schema import CreateTokenSchema, TokenPairSchema, TokenSchema
from auth_service.api.exception.auth_exception import TokenExpiredError


class AuthServiceImpl(AuthService):
    def __init__(self, user_service: UserService, token_service: TokenService):
        self.user_service = user_service
        self.token_service = token_service
        self.default_role = "User"
    
    # TODO: handle exceptions and rollbacks
    async def signup(self, schema: SignupSchema) -> TokenPairSchema:
        user = CreateUserSchema(
            first_name=schema.first_name,
            last_name=schema.last_name,
            username=schema.username,
            email=schema.email,
            password=schema.password,
            role=self.default_role
        )
        created_user = await self.user_service.create(user)
        
        payload = TokenPayload(user_id=created_user.id)
        access_token = self.generate_access_token(payload)
        refresh_token = self.generate_refresh_token()
        token = CreateTokenSchema(
            value=refresh_token,
            expires=config.jwt.refresh_expire_minutes,
            is_active=True,
            user_id=created_user.id
        )
        created_token: TokenSchema = await self.token_service.create(token)
        
        return TokenPairSchema(
            access_token=access_token,
            refresh_token=created_token.value,
        )
        
    async def login(schema: LoginSchema) -> TokenPairSchema:
        pass
    
    def generate_access_token(self, payload: TokenPayload) -> str:
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=config.jwt.access_expire_minutes)
        token_data = {
            "sub": str(payload.user_id),
            "iat": now.timestamp(),
            "nbf": now.timestamp(),
            "exp": expires.timestamp(),
            "type": "access"
        }
        token = jwt.encode(token_data, config.jwt.secret, algorithm=config.jwt.algorithm)
        return token
    
    def generate_refresh_token(self) -> str:
        return secrets.token_hex(64)
    
    def decode_token(token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, config.jwt.secret, algorithms=[config.jwt.algorithm])
            return TokenPayload(user_id=uuid.UUID(payload["sub"]), user_email=payload["email"])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except (jwt.InvalidTokenError, KeyError):
            raise jwt.InvalidTokenError()
    
    def validate_refresh_token(refresh_token: str) -> bool:
        pass
    
    def refresh_access_token(access_token: str, refresh_token: str) -> TokenPayload:
        pass
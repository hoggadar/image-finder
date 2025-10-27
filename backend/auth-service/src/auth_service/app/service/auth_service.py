import uuid
import jwt
import secrets
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.config import config
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.core.interface.service.token_service import TokenService
from auth_service.core.interface.service.user_service import UserService
from auth_service.core.dto.token_dto import TokenPayload
from auth_service.api.v1.schema.user_schema import CreateUserSchema, UserSchema
from auth_service.api.v1.schema.auth_schema import LoginSchema, SignupSchema
from auth_service.api.v1.schema.token_schema import CreateTokenSchema, TokenPairSchema, TokenSchema
from auth_service.app.exception import (
    UserAlreadyExistsException,
    UserNotFoundException,
    TokenExpiredException,
    InvalidTokenException,
    LoginException,
    AuthenticationException,
)


class AuthServiceImpl(AuthService):
    def __init__(self, user_service: UserService, token_service: TokenService, session: AsyncSession):
        self.user_service = user_service
        self.token_service = token_service
        self.session = session
        self.default_role = "User"
        self.logger = logging.getLogger(__name__)
    
    async def signup(self, schema: SignupSchema) -> TokenPairSchema:
        try:
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
        except (UserAlreadyExistsException, UserNotFoundException) as e:
            self.logger.warning(f"Signup failed: {e.message}")
            raise
        except Exception as e:
            # Note: No rollback here because user_service and token_service manage their own transactions
            # If token creation fails, user is already committed - this is a known limitation
            # TODO: Refactor to use single transaction across all operations
            self.logger.error(f"Unexpected error during signup: {str(e)}", exc_info=True)
            raise AuthenticationException(f"Signup failed: {str(e)}")
        
    async def login(self, schema: LoginSchema) -> TokenPairSchema:
        try:
            user = await self.user_service.get_by_email(schema.email)
            if not user:
                self.logger.warning(f"Login failed: User with email '{schema.email}'not found")
                raise LoginException("Invalid username or password")
            
            # TODO: Verify password (need to implement password verification in user_service)
            # For now, just a placeholder
            # if not self.verify_password(schema.password, user.password):
            #     raise LoginException("Invalid username or password")
            
            payload = TokenPayload(user_id=user.id)
            access_token = self.generate_access_token(payload)
            refresh_token = self.generate_refresh_token()
            
            token = CreateTokenSchema(
                value=refresh_token,
                expires=config.jwt.refresh_expire_minutes,
                is_active=True,
                user_id=user.id
            )
            created_token = await self.token_service.create(token)
            
            return TokenPairSchema(
                access_token=access_token,
                refresh_token=created_token.value,
            )
        except (UserNotFoundException, LoginException) as e:
            self.logger.warning(f"Login failed: {str(e)}")
            raise LoginException("Invalid email or password")
        except Exception as e:
            self.logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
            raise AuthenticationException(f"Login failed: {str(e)}")
    
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
    
    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, config.jwt.secret, algorithms=[config.jwt.algorithm])
            return TokenPayload(user_id=uuid.UUID(payload["sub"]))
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            raise TokenExpiredException()
        except (jwt.InvalidTokenError, KeyError) as e:
            self.logger.warning(f"Invalid token: {str(e)}")
            raise InvalidTokenException(f"Invalid token: {str(e)}")
    
    async def validate_refresh_token(self, refresh_token: str) -> bool:
        try:
            token = await self.token_service.get_by_value(refresh_token)
            if not token or not token.is_active:
                return False
            if token.expires < datetime.now(timezone.utc):
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating refresh token: {str(e)}", exc_info=True)
            return False
    
    async def refresh_access_token(self, refresh_token: str) -> TokenPairSchema:
        try:
            if not await self.validate_refresh_token(refresh_token):
                self.logger.warning("Invalid or expired refresh token")
                raise TokenExpiredException()

            token = await self.token_service.get_by_value(refresh_token)
            
            payload = TokenPayload(user_id=token.user_id)
            new_access_token = self.generate_access_token(payload)
            
            return TokenPairSchema(
                access_token=new_access_token,
                refresh_token=refresh_token,
            )
        except TokenExpiredException:
            raise
        except Exception as e:
            self.logger.error(f"Error refreshing access token: {str(e)}", exc_info=True)
            raise AuthenticationException(f"Failed to refresh token: {str(e)}")
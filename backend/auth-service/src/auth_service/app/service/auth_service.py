import uuid
import jwt
import secrets
import logging
import bcrypt

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.config import config
from auth_service.app.util.converter import Converter
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.core.interface.service.token_service import TokenService
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.service.user_service import UserService
from auth_service.core.interface.repository.user_repository import UserRepository
from auth_service.core.interface.repository.token_repository import TokenRepository
from auth_service.core.entity.user_entity import UserEntity
from auth_service.core.entity.token_entity import RefreshTokenEntity
from auth_service.core.dto.token_dto import AccessTokenPayloadDTO, TokensPairDTO, TokenValidationResultDTO
from auth_service.core.dto.user_dto import CreateUserDTO
from auth_service.core.dto.auth_dto import LoginDTO, SignupDTO
from auth_service.app.exception import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserCreationException,
    TokenExpiredException,
    InvalidTokenException,
    LoginException,
    AuthenticationException,
    RoleNotFoundException,
    TokenCreationException,
)
from auth_service.infrastructure.exception.repository_exception import (
    RetrievalException,
    CreationExeption,
)


class AuthServiceImpl(AuthService):
    def __init__(
        self, 
        user_repo: UserRepository,
        token_repo: TokenRepository,
        user_service: UserService,
        role_service: RoleService,
        token_service: TokenService,
        session: AsyncSession
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.user_service = user_service
        self.role_service = role_service
        self.token_service = token_service
        self.session = session
        self.default_role = "User"
        self.logger = logging.getLogger(__name__)
    
    async def signup(self, dto: SignupDTO) -> TokensPairDTO:
        try:
            existing_user_by_username = await self.user_repo.get_by_username(dto.username)
            if existing_user_by_username:
                self.logger.warning(f"User with username '{dto.username}' already exists")
                raise UserAlreadyExistsException(field="username", value=dto.username)
            
            existing_user_by_email = await self.user_repo.get_by_email(dto.email)
            if existing_user_by_email:
                self.logger.warning(f"User with email '{dto.email}' already exists")
                raise UserAlreadyExistsException(field="email", value=dto.email)
            
            role = await self.role_service.get_by_name(self.default_role)
            
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(dto.password.encode("utf-8"), salt).decode("utf-8")
            
            user_entity = UserEntity(
                first_name=dto.first_name,
                last_name=dto.last_name,
                username=dto.username,
                email=dto.email,
                password=hashed_password,
                role_id=role.id,
            )
            created_user = await self.user_repo.create(user_entity)
            if not created_user:
                self.logger.error(f"Failed to create user '{dto.username}': repository returned None")
                raise UserCreationException("User was not created")
            
            payload = AccessTokenPayloadDTO(user_id=created_user.id, role=role.name)
            access_token = self.generate_access_token(payload)
            refresh_token_value = self.generate_refresh_token()
            
            now = datetime.now(timezone.utc)
            expires = now + timedelta(minutes=config.jwt.refresh_expire_minutes)
            token_entity = RefreshTokenEntity(
                value=refresh_token_value,
                expires_at=expires,
                is_locked=False,
                user_id=created_user.id,
            )
            created_token = await self.token_repo.create(token_entity)
            if not created_token:
                self.logger.error(f"Failed to create token for user '{dto.username}': repository returned None")
                raise TokenCreationException("Token was not created")
            
            await self.session.commit()
            
            return TokensPairDTO(
                access_token=access_token,
                refresh_token=created_token.value,
            )
            
        except (UserAlreadyExistsException, RoleNotFoundException, UserCreationException, TokenCreationException):
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error during signup for '{dto.username}': {e.message}", exc_info=True)
            raise AuthenticationException(f"Signup failed: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error during signup for '{dto.username}': {str(e)}", exc_info=True)
            raise AuthenticationException(f"Signup failed: {str(e)}")
        
    async def login(self, dto: LoginDTO) -> TokensPairDTO:
        try:
            user = await self.user_repo.get_by_email(dto.email)
            if not user:
                self.logger.warning(f"Login failed: User with email '{dto.email}' not found")
                raise LoginException("Invalid email or password")
            
            if not bcrypt.checkpw(dto.password.encode("utf-8"), user.password.encode("utf-8")):
                self.logger.warning(f"Login failed: Invalid password for user '{dto.email}'")
                raise LoginException("Invalid email or password")
            
            role = await self.role_service.get_by_id(user.role_id)
            
            existing_token = await self.token_repo.get_by_user_id(user.id)
            if existing_token:
                await self.token_repo.delete(existing_token.id)
            
            payload = AccessTokenPayloadDTO(user_id=user.id, role=role.name)
            access_token = self.generate_access_token(payload)
            refresh_token_value = self.generate_refresh_token()
            
            now = datetime.now(timezone.utc)
            expires = now + timedelta(minutes=config.jwt.refresh_expire_minutes)
            token_entity = RefreshTokenEntity(
                value=refresh_token_value,
                expires_at=expires,
                is_locked=False,
                user_id=user.id,
            )
            created_token = await self.token_repo.create(token_entity)
            if not created_token:
                self.logger.error(f"Failed to create token for user '{dto.email}': repository returned None")
                raise TokenCreationException("Token was not created")
            
            await self.session.commit()
            
            return TokensPairDTO(
                access_token=access_token,
                refresh_token=created_token.value,
            )
            
        except LoginException:
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error during login for '{dto.email}': {e.message}", exc_info=True)
            raise AuthenticationException(f"Login failed: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error during login for '{dto.email}': {str(e)}", exc_info=True)
            raise AuthenticationException(f"Login failed: {str(e)}")
    
    def generate_access_token(self, payload: AccessTokenPayloadDTO) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=config.jwt.access_expire_minutes)
        token_data = {
            "sub": str(payload.user_id),
            "role": payload.role,
            "iat": now.timestamp(),
            "nbf": now.timestamp(),
            "exp": expires_at.timestamp(),
            "type": "access"
        }
        token = jwt.encode(token_data, config.jwt.secret, algorithm=config.jwt.algorithm)
        return token
    
    def generate_refresh_token(self) -> str:
        return secrets.token_hex(64)
    
    def decode_token(self, token: str) -> AccessTokenPayloadDTO:
        try:
            payload = jwt.decode(token, config.jwt.secret, algorithms=[config.jwt.algorithm])
            
            if "role" not in payload:
                self.logger.warning("Token does not contain role field")
                raise InvalidTokenException("Token is missing required 'role' field")
            
            return AccessTokenPayloadDTO(
                user_id=uuid.UUID(payload["sub"]),
                role=payload["role"]
            )
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            raise TokenExpiredException()
        except (jwt.InvalidTokenError, KeyError, ValueError) as e:
            self.logger.warning(f"Invalid token: {str(e)}")
            raise InvalidTokenException(f"Invalid token: {str(e)}")
    
    async def validate_access_token_with_role(
        self, 
        access_token: str, 
        required_role: str
    ) -> TokenValidationResultDTO:
        try:
            token_payload = self.decode_token(access_token)
            
            has_required_role = token_payload.role == required_role
            
            if not has_required_role:
                self.logger.warning(
                    f"Role mismatch: user {token_payload.user_id} has role '{token_payload.role}', "
                    f"but '{required_role}' is required"
                )
            
            return TokenValidationResultDTO(
                is_valid=True,
                user_id=token_payload.user_id,
                role=token_payload.role,
                has_required_role=has_required_role,
                message="Token is valid" if has_required_role else f"Insufficient permissions: '{required_role}' role required"
            )
            
        except TokenExpiredException:
            self.logger.warning("Token validation failed: token has expired")
            return TokenValidationResultDTO(
                is_valid=False,
                user_id=None,
                role=None,
                has_required_role=False,
                message="Token has expired"
            )
        except InvalidTokenException as e:
            self.logger.warning(f"Token validation failed: {str(e)}")
            return TokenValidationResultDTO(
                is_valid=False,
                user_id=None,
                role=None,
                has_required_role=False,
                message=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            self.logger.error(f"Unexpected error during token validation: {str(e)}", exc_info=True)
            return TokenValidationResultDTO(
                is_valid=False,
                user_id=None,
                role=None,
                has_required_role=False,
                message=f"Token validation error: {str(e)}"
            )
    
    async def refresh_access_token(self, access_token: str, refresh_token: str) -> TokensPairDTO:
        try:
            decoded_payload = jwt.decode(
                access_token, 
                config.jwt.secret, 
                algorithms=[config.jwt.algorithm],
                options={"verify_exp": False}
            )
            user_id_from_access = uuid.UUID(decoded_payload["sub"])
            
            stored_token = await self.token_repo.get_by_user_id(user_id_from_access)
            
            self._validate_token_entity(
                stored_token=stored_token,
                expected_value=refresh_token,
                user_id=user_id_from_access
            )
            
            user_dto = await self.user_service.get_by_id(user_id_from_access)
            
            role = await self.role_service.get_by_id(user_dto.role_id)
            
            payload = AccessTokenPayloadDTO(user_id=user_dto.id, role=role.name)
            new_access_token = self.generate_access_token(payload)
            new_refresh_token_value = self.generate_refresh_token()
            
            await self.token_repo.delete(stored_token.id)
            
            now = datetime.now(timezone.utc)
            expires = now + timedelta(minutes=config.jwt.refresh_expire_minutes)
            new_token_entity = RefreshTokenEntity(
                value=new_refresh_token_value,
                expires_at=expires,
                is_locked=False,
                user_id=user_id_from_access,
            )
            created_token = await self.token_repo.create(new_token_entity)
            if not created_token:
                await self.session.rollback()
                self.logger.error(f"Failed to create new refresh token for user: {user_id_from_access}")
                raise TokenCreationException("Failed to create new refresh token")
            
            await self.session.commit()
            
            return TokensPairDTO(
                access_token=new_access_token,
                refresh_token=created_token.value,
            )
            
        except jwt.ExpiredSignatureError:
            await self.session.rollback()
            self.logger.warning("Access token has expired (should not happen with verify_exp=False)")
            raise TokenExpiredException("Access token has expired")
        except (jwt.InvalidTokenError, KeyError, ValueError) as e:
            await self.session.rollback()
            self.logger.warning(f"Invalid access token: {str(e)}")
            raise InvalidTokenException(f"Invalid access token: {str(e)}")
        except (TokenExpiredException, InvalidTokenException, UserNotFoundException, TokenCreationException, RoleNotFoundException):
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error during token refresh: {e.message}", exc_info=True)
            raise AuthenticationException(f"Failed to refresh tokens: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error during token refresh: {str(e)}", exc_info=True)
            raise AuthenticationException(f"Failed to refresh tokens: {str(e)}")
    
    def _validate_token_entity(
        self, 
        stored_token: RefreshTokenEntity, 
        expected_value: str = None,
        user_id: uuid.UUID = None
    ) -> None:
        if not stored_token:
            self.logger.warning(f"Token not found{f' for user: {user_id}' if user_id else ''}")
            raise TokenExpiredException("Refresh token not found")
        
        if expected_value and stored_token.value != expected_value:
            self.logger.warning(f"Token value mismatch{f' for user: {user_id}' if user_id else ''}")
            raise InvalidTokenException("Refresh token does not match")
        
        if stored_token.is_locked:
            self.logger.warning(f"Token is inactive{f' for user: {user_id}' if user_id else ''}")
            raise TokenExpiredException("Refresh token is inactive")
        
        if stored_token.expires_at < datetime.now(timezone.utc):
            self.logger.warning(f"Token has expired{f' for user: {user_id}' if user_id else ''}")
            raise TokenExpiredException("Refresh token has expired")
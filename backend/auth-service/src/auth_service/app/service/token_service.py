import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.app.util.converter import Converter
from auth_service.core.dto.token_dto import RefreshTokenDTO, CreateRefreshTokenDTO, UpdateRefreshTokenDTO
from auth_service.core.entity.token_entity import RefreshTokenEntity
from auth_service.core.interface.repository.token_repository import TokenRepository
from auth_service.core.interface.service.token_service import TokenService
from auth_service.app.exception import (
    TokenNotFoundException,
    TokenAlreadyExistsException,
    TokenCreationException,
    TokenValidationException,
    TokenRevocationException,
    TokenRefreshException,
)
from auth_service.infrastructure.exception.repository_exception import (
    RetrievalException,
    CreationExeption,
    UpdateException,
    DeletionException,
)


class TokenServiceImpl(TokenService):
    def __init__(self, token_repo: TokenRepository, session: AsyncSession):
        self.token_repo = token_repo
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RefreshTokenDTO]:
        try:
            tokens = await self.token_repo.get_all(offset=offset, limit=limit, search=search)
            return [self._entity_to_dto(token) for token in tokens]
        except RetrievalException as e:
            self.logger.error(f"Failed to retrieve tokens: {e.message}", exc_info=True)
            raise TokenNotFoundException()
    
    async def get_by_id(self, id: str) -> Optional[RefreshTokenDTO]:
        try:
            converted_id = Converter.get_uuid(id)
            token = await self.token_repo.get_by_id(converted_id)
            if not token:
                self.logger.warning(f"Token with id '{id}' not found")
                raise TokenNotFoundException()
            return self._entity_to_dto(token)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving token by id '{id}': {e.message}", exc_info=True)
            raise TokenNotFoundException()

    async def get_by_value(self, value: str) -> Optional[RefreshTokenDTO]:
        try:
            token = await self.token_repo.get_by_value(value)
            if not token:
                self.logger.warning(f"Token with value not found")
                raise TokenNotFoundException(value)
            return self._entity_to_dto(token)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving token by value: {e.message}", exc_info=True)
            raise TokenNotFoundException(value)

    async def get_by_user_id(self, user_id: str) -> Optional[RefreshTokenDTO]:
        try:
            converted_user_id = Converter.get_uuid(user_id)
            token = await self.token_repo.get_by_user_id(converted_user_id)
            if not token:
                self.logger.warning(f"Token for user_id '{user_id}' not found")
                raise TokenNotFoundException()
            return self._entity_to_dto(token)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving token by user_id '{user_id}': {e.message}", exc_info=True)
            raise TokenNotFoundException()

    async def create(self, dto: CreateRefreshTokenDTO) -> Optional[RefreshTokenDTO]:
        try:
            existing_token = await self.token_repo.get_by_user_id(dto.user_id)
            if existing_token:
                self.logger.warning(f"Token for user_id '{dto.user_id}' already exists")
                raise TokenAlreadyExistsException(existing_token.value)
            
            token = RefreshTokenEntity(
                value=dto.value,
                expires=dto.expires_at,
                is_active=not dto.is_locked,
                user_id=dto.user_id,
            )
            
            created_token = await self.token_repo.create(token)
            if not created_token:
                await self.session.rollback()
                self.logger.error(f"Failed to create token for user_id '{dto.user_id}': repository returned None")
                raise TokenCreationException("Token was not created")
            
            await self.session.commit()
            return self._entity_to_dto(created_token)
            
        except TokenAlreadyExistsException:
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while creating token for user_id '{dto.user_id}': {e.message}", exc_info=True)
            raise TokenCreationException(f"Failed to create token: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while creating token for user_id '{dto.user_id}': {str(e)}", exc_info=True)
            raise TokenCreationException(f"Unexpected error during token creation")
    
    async def update(self, dto: UpdateRefreshTokenDTO) -> Optional[RefreshTokenDTO]:
        try:
            existing_token = await self.token_repo.get_by_id(dto.id)
            if not existing_token:
                self.logger.warning(f"Token with id '{dto.id}' not found for update")
                raise TokenNotFoundException()
            
            existing_token.value = dto.value
            existing_token.expires = dto.expires_at
            existing_token.is_active = not dto.is_locked
            existing_token.user_id = dto.user_id
            existing_token.updated_at = datetime.now(timezone.utc)
            
            updated_token = await self.token_repo.update(existing_token)
            if not updated_token:
                await self.session.rollback()
                self.logger.error(f"Failed to update token '{dto.id}': repository returned None")
                raise TokenValidationException("Token update failed")
            
            await self.session.commit()
            return self._entity_to_dto(updated_token)
            
        except TokenNotFoundException:
            await self.session.rollback()
            raise
        except (RetrievalException, UpdateException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while updating token '{dto.id}': {e.message}", exc_info=True)
            raise TokenValidationException(f"Failed to update token: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while updating token '{dto.id}': {str(e)}", exc_info=True)
            raise TokenValidationException(f"Unexpected error during token update")
    
    async def delete(self, id: str) -> Optional[RefreshTokenDTO]:
        try:
            converted_id = Converter.get_uuid(id)
            token = await self.token_repo.get_by_id(converted_id)
            if not token:
                self.logger.warning(f"Token with id '{id}' not found for deletion")
                raise TokenNotFoundException()
            
            deleted_token = await self.token_repo.delete(converted_id)
            if not deleted_token:
                await self.session.rollback()
                self.logger.error(f"Failed to delete token '{id}': repository returned None")
                raise TokenRevocationException("Token deletion failed")
            
            await self.session.commit()
            return self._entity_to_dto(deleted_token)
            
        except TokenNotFoundException:
            await self.session.rollback()
            raise
        except (RetrievalException, DeletionException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while deleting token '{id}': {e.message}", exc_info=True)
            raise TokenRevocationException(f"Failed to delete token: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while deleting token '{id}': {str(e)}", exc_info=True)
            raise TokenRevocationException(f"Unexpected error during token deletion")

    async def deactivate(self, token_value: str) -> Optional[RefreshTokenDTO]:
        try:
            token_dto = await self.get_by_value(token_value)
            token_entity = await self.token_repo.get_by_value(token_value)
            if not token_entity:
                raise TokenNotFoundException(token_value)
            
            token_entity.is_active = False
            token_entity.updated_at = datetime.now(timezone.utc)
            
            updated_token = await self.token_repo.update(token_entity)
            if not updated_token:
                await self.session.rollback()
                self.logger.error("Failed to deactivate token: repository returned None")
                raise TokenRevocationException("Token deactivation failed")
            
            await self.session.commit()
            return self._entity_to_dto(updated_token)
            
        except UpdateException as e:
            await self.session.rollback()
            self.logger.error(f"Database error while deactivating token: {e.message}", exc_info=True)
            raise TokenRevocationException(f"Failed to deactivate token: {e.message}")
        except TokenNotFoundException:
            await self.session.rollback()
            raise
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while deactivating token: {str(e)}", exc_info=True)
            raise TokenRevocationException(f"Unexpected error during token deactivation")
    
    def _entity_to_dto(self, entity: RefreshTokenEntity) -> RefreshTokenDTO:
        return RefreshTokenDTO(
            id=entity.id,
            value=entity.value,
            expires_at=entity.expires_at,
            is_locked=entity.is_locked,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
        )
from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence
from auth_service.app.util.converter import Converter
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.api.exception.token_exception import TokenAlreadyExistsError, TokenNotFoundError
from auth_service.api.v1.schema.token_schema import CreateTokenSchema, TokenSchema, UpdateTokenSchema
from auth_service.api.v1.schema.user_schema import UserSchema
from auth_service.core.entity.token_entity import TokenEntity
from auth_service.core.interface.repository.token_repository import TokenRepository
from auth_service.core.interface.service.token_service import TokenService


class TokenServiceImpl(TokenService):
    def __init__(self, token_repo: TokenRepository, session: AsyncSession):
        self.token_repo = token_repo
        self.session = session
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[TokenSchema]:
        tokens = await self.token_repo.get_all(offset=offset, limit=limit, search=search)
        return [self._entity_to_dto(token) for token in tokens]
    
    async def get_by_id(self, id: str):
        converted_id = Converter.get_uuid(id)
        token = await self.token_repo.get_by_id(converted_id)
        return self._entity_to_dto(token)

    async def get_by_value(self, value: str) -> Optional[TokenSchema]:
        token = await self.token_repo.get_by_value(value)
        if not token:
            raise TokenNotFoundError(value)
        return self._entity_to_dto(token)

    async def get_by_user_id(self, user_id: str) -> Optional[TokenSchema]:
        converted_user_id = Converter.get_uuid(user_id)
        token = await self.token_repo.get_by_user_id(converted_user_id)
        if not token:
            raise TokenNotFoundError()
        return self._entity_to_dto(token)

    async def create(self, dto: CreateTokenSchema) -> Optional[TokenSchema]:
        converted_user_id = Converter.get_uuid(dto.user_id)
        existing_token = await self.token_repo.get_by_user_id(converted_user_id)
        if existing_token:
            raise TokenAlreadyExistsError(token.value)
        
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=dto.expires)
        token = TokenEntity(
            value=dto.value,
            expires=expires,
            is_active=dto.is_active,
            user_id=dto.user_id,
        )
        created_token = await self.token_repo.create(token)
        if not created_token:
            await self.session.rollback()
            return None
        await self.session.commit()
        return created_token
    
    async def update(self, dto: UpdateTokenSchema) -> Optional[TokenSchema]:
        converted_id = Converter.get_uuid(dto.id)
        existing_token = await self.token_repo.get_by_id(converted_id)
        if existing_token:
            raise TokenAlreadyExistsError(existing_token.value)
        
        existing_token.value = dto.value
        existing_token.expires = dto.expires
        existing_token.is_active = dto.is_active
        existing_token.user_id = dto.user_id
        existing_token.updated_at = datetime.now(timezone.utc)
        
        updated_token = await self.token_repo.update(existing_token)
        if not updated_token:
            await self.session.rollback()
            return None
        await self.session.commit()
        return self._entity_to_dto(updated_token)
    
    async def delete(self, id: str) -> TokenSchema:
        converted_id = Converter.get_uuid(id)
        token = await self.token_repo.get_by_id(converted_id)
        if not token:
            raise TokenNotFoundError(str(id))
        
        deleted_token = await self.token_repo.delete(converted_id)
        if not deleted_token:
            await self.session.rollback()
            return None 
        await self.session.commit()
        return self._entity_to_dto(deleted_token)

    async def deactivate(self, token_value: str) -> Optional[TokenSchema]:
        token = await self.get_by_value(token_value)
        token.is_active = False
        updated_token = await self.token_repo.update(token)
        if not updated_token:
            await self.session.rollback()
            return None
        await self.session.commit()
        return updated_token
    
    def _entity_to_dto(self, entity: TokenEntity) -> TokenSchema:
        return TokenSchema(
            id=str(entity.id),
            value=entity.value,
            expires=entity.expires,
            is_active=entity.is_active,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
import uuid
import logging

from sqlalchemy import insert, select, update, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.infrastructure.exception.repository_exception import (
    RetrievalException,
    CreationExeption,
    UpdateException,
    DeletionException
)
from auth_service.core.entity.token_entity import RefreshTokenEntity
from auth_service.core.interface.repository.token_repository import TokenRepository


class TokenRepositoryImpl(TokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RefreshTokenEntity]:
        try:
            stmt = select(RefreshTokenEntity).order_by(RefreshTokenEntity.created_at.desc())
            if search:
                stmt = stmt.where(
                    or_(
                        RefreshTokenEntity.id.ilike(f"%{search}%"),
                        RefreshTokenEntity.value.ilike(f"%{search}%"),
                        RefreshTokenEntity.user_id.ilike(f"%{search}%")
                    )
                )
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            message = f"Failed to retrieve tokens (offset={offset}, limit={limit}, search='{search}')"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"offset": offset, "limit": limit, "search": search, "error": str(e)},
            )
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[RefreshTokenEntity]:
        try:
            stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve token by id: {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )
    
    async def get_by_value(self, value: str) -> Optional[RefreshTokenEntity]:
        try:
            stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.value == value)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve token by value"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"error": str(e)},
            )
    
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[RefreshTokenEntity]:
        try:
            stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve token by user_id: {user_id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"user_id": str(user_id), "error": str(e)},
            )
    
    async def create(self, token: RefreshTokenEntity) -> Optional[RefreshTokenEntity]:
        current_time = datetime.now(timezone.utc)
        try:
            stmt = (
                insert(RefreshTokenEntity)
                .values(
                    id=uuid.uuid4(),
                    value=token.value,
                    is_locked=token.is_locked,
                    expires_at=token.expires_at,
                    created_at=current_time,
                    updated_at=current_time,
                    user_id=token.user_id,
                )
                .returning(RefreshTokenEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to create token for user_id: {token.user_id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise CreationExeption(
                message=message,
                details={
                    "user_id": str(token.user_id),
                    "expires_at": str(token.expires_at),
                    "error": str(e),
                },
            )
    
    async def update(self, token: RefreshTokenEntity) -> Optional[RefreshTokenEntity]:
        try:
            stmt = (
                update(RefreshTokenEntity)
                .where(RefreshTokenEntity.id == token.id)
                .values(
                    value=token.value,
                    expires=token.expires,
                    is_active=token.is_active,
                    updated_at=datetime.now(timezone.utc),
                )
                .returning(RefreshTokenEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to update token with id {token.id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise UpdateException(
                message=message,
                details={"id": str(token.id), "error": str(e)},
            )
    
    async def delete(self, id: uuid.UUID) -> Optional[RefreshTokenEntity]:
        try:
            stmt = delete(RefreshTokenEntity).where(RefreshTokenEntity.id == id).returning(RefreshTokenEntity)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to delete token with id {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise DeletionException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )
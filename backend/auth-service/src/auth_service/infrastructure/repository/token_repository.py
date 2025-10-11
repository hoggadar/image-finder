import uuid

from sqlalchemy import insert, select, update, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.entity.token_entity import TokenEntity
from auth_service.core.interface.repository.token_repository import TokenRepository


class TokenRepositoryImpl(TokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[TokenEntity]:
        try:
            stmt = select(TokenEntity).order_by(TokenEntity.created_at.desc())
            if search:
                stmt = stmt.where(
                    or_(
                        TokenEntity.id.ilike(f"%{search}%"),
                        TokenEntity.value.ilike(f"%{search}%"),
                        TokenEntity.user_id.ilike(f"%{search}%")
                    )
                )
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[TokenEntity]:
        try:
            stmt = select(TokenEntity).where(TokenEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_by_value(self, value: str) -> Optional[TokenEntity]:
        try:
            stmt = select(TokenEntity).where(TokenEntity.value == value)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[TokenEntity]:
        try:
            stmt = select(TokenEntity).where(TokenEntity.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def create(self, token: TokenEntity) -> Optional[TokenEntity]:
        current_time = datetime.now(timezone.utc)
        try:
            stmt = (
                insert(TokenEntity)
                .values(
                    id=uuid.uuid4(),
                    value=token.value,
                    expires=token.expires,
                    is_active=token.is_active,
                    created_at=current_time,
                    updated_at=current_time,
                    user_id=token.user_id,
                )
                .returning(TokenEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def update(self, token: TokenEntity) -> Optional[TokenEntity]:
        try:
            stmt = (
                update(TokenEntity)
                .where(TokenEntity.id == token.id)
                .values(
                    value=token.value,
                    expires=token.expires,
                    is_active=token.is_active,
                    updated_at=datetime.now(timezone.utc),
                )
                .returning(TokenEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def delete(self, id: uuid.UUID) -> Optional[TokenEntity]:
        try:
            stmt = delete(TokenEntity).where(TokenEntity.id == id).returning(TokenEntity)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
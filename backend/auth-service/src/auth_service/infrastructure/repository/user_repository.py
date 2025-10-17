import uuid
import logging

from sqlalchemy import insert, select, update, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.entity.user_entity import UserEntity
from auth_service.core.interface.repository.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserEntity]:
        try:
            stmt = select(UserEntity).order_by(UserEntity.id.asc())
            if search:
                stmt = stmt.where(
                    or_(
                        UserEntity.first_name.ilike(f"%{search}%"),
                        UserEntity.last_name.ilike(f"%{search}%"),
                        UserEntity.user_name.ilike(f"%{search}%"),
                        UserEntity.email.ilike(f"%{search}%"),
                    )
                )
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[UserEntity]:
        try:
            stmt = select(UserEntity).where(UserEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_by_full_name(self, full_name: str, offset: int = 0, limit: int = 10) -> Sequence[UserEntity]:
        try:
            parts = full_name.strip().split()
            stmt = select(UserEntity).order_by(UserEntity.first_name.asc())

            if len(parts) == 1:
                stmt = stmt.where(
                    or_(
                        UserEntity.first_name.ilike(f"%{parts[0]}%"),
                        UserEntity.last_name.ilike(f"%{parts[0]}%"),
                    )
                )
            elif len(parts) >= 2:
                first, last = parts[0], parts[1]
                stmt = stmt.where(
                    and_(
                        UserEntity.first_name.ilike(f"%{first}%"),
                        UserEntity.last_name.ilike(f"%{last}%"),
                    )
                )
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_user_name(self, user_name: str) -> Optional[UserEntity]:
        try:
            stmt = (
                select(UserEntity)
                .where(UserEntity.user_name == user_name)
                .order_by(UserEntity.user_name.asc())
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            stmt = (
                select(UserEntity)
                .where(UserEntity.email == email)
                .order_by(UserEntity.email.asc())
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def create(self, user: UserEntity) -> Optional[UserEntity]:
        current_time = datetime.now(timezone.utc)
        try:
            stmt = (
                insert(UserEntity)
                .values(
                    id=uuid.uuid4(),
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    role_id=user.role_id,
                    created_at=current_time,
                    updated_at=current_time,
                )
                .returning(UserEntity)
            )
            
            # Important:
            # SQLAlchemy Result objects are *consumed after one access* (e.g., scalar_one_or_none(), fetchall(), etc.).
            # Calling these methods more than once closes the underlying cursor and raises ResourceClosedError.
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            return None
    
    async def update(self, user: UserEntity) -> Optional[UserEntity]:
        try:
            stmt = (
                update(UserEntity)
                .where(UserEntity.id == user.id)
                .values(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    role_id=user.role_id,
                    updated_at=datetime.now(timezone.utc),
                )
                .returning(UserEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def delete(self, id: uuid.UUID) -> Optional[UserEntity]:
        try:
            stmt = (
                delete(UserEntity)
                .where(UserEntity.id == id)
                .returning(UserEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
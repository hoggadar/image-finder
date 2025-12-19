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
from auth_service.core.entity.user_entity import UserEntity
from auth_service.core.interface.repository.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserEntity]:
        try:
            stmt = select(UserEntity).order_by(UserEntity.id.asc())
            if search:
                stmt = stmt.where(
                    # or_(
                    #     UserEntity.first_name.ilike(f"%{search}%"),
                    #     UserEntity.last_name.ilike(f"%{search}%"),
                    #     UserEntity.username.ilike(f"%{search}%"),
                    #     UserEntity.email.ilike(f"%{search}%"),
                    # )
                    UserEntity.username.ilike(f"%{search}%"),
                )
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            message = f"Failed to retrieve users (offset={offset}, limit={limit}, search='{search}')"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"offset": offset, "limit": limit, "search": search, "error": str(e)},
            )
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[UserEntity]:
        try:
            stmt = select(UserEntity).where(UserEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve user by id: {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        try:
            stmt = (
                select(UserEntity)
                .where(UserEntity.username == username)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve user by username: {username}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"username": username, "error": str(e)},
            )

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            stmt = (
                select(UserEntity)
                .where(UserEntity.email == email)
                .order_by(UserEntity.email.asc())
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve user by email: {email}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"email": email, "error": str(e)},
            )

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
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to create user with username '{user.username}'"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise CreationExeption(
                message=message,
                details={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "error": str(e),
                },
            )
    
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
        except Exception as e:
            message = f"Failed to update user with id {user.id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise UpdateException(
                message=message,
                details={"id": str(user.id), "error": str(e)},
            )
    
    async def delete(self, id: uuid.UUID) -> Optional[UserEntity]:
        try:
            stmt = (
                delete(UserEntity)
                .where(UserEntity.id == id)
                .returning(UserEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to delete user with id {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise DeletionException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )
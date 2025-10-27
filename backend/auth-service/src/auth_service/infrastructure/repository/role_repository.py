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
from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.interface.repository.role_repository import RoleRepository


class RoleRepositoryImpl(RoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleEntity]:
        try:
            stmt = select(RoleEntity).order_by(RoleEntity.id.asc())
            if search:
                stmt = stmt.where(RoleEntity.name.ilike(f"%{search}%"))
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            message = f"Failed to retrieve roles (offset={offset}, limit={limit}, search='{search}')"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"offset": offset, "limit": limit, "search": search, "error": str(e)},
            )
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleEntity]:
        try:
            stmt = select(RoleEntity).where(RoleEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve role by id: {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )
    
    async def get_by_name(self, name: str) -> Optional[RoleEntity]:
        try:
            stmt = select(RoleEntity).where(RoleEntity.name == name)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to retrieve role by name: {name}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise RetrievalException(
                message=message,
                details={"name": name, "error": str(e)},
            )
    
    
    async def create(self, role: RoleEntity) -> Optional[RoleEntity]:
        current_time = datetime.now(timezone.utc)
        try:
            stmt = (
                insert(RoleEntity)
                .values(
                    id=uuid.uuid4(),
                    name=role.name,
                    description=role.description,
                    created_at=current_time,
                    updated_at=current_time,
                )
                .returning(RoleEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to create role with name '{role.name}'"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise CreationExeption(
                message=message,
                details={
                    "name": role.name,
                    "description": role.description,
                    "error": str(e),
                },
            )
        
        
    async def update(self, role: RoleEntity) -> Optional[RoleEntity]:
        try:
            stmt = (
                update(RoleEntity)
                .where(RoleEntity.id == role.id)
                .values(
                    name=role.name,
                    description=role.description,
                    updated_at=datetime.now(timezone.utc),
                )
                .returning(RoleEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to update role with id {role.id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise UpdateException(
                message=message,
                details={"id": str(role.id), "error": str(e)},
            )
    
    async def delete(self, id: uuid.UUID) -> Optional[RoleEntity]:
        try:
            stmt = (
                delete(RoleEntity)
                .where(RoleEntity.id == id)
                .returning(RoleEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            message = f"Failed to delete role with id {id}"
            self.logger.error(f"{message}: {e}", exc_info=True)
            raise DeletionException(
                message=message,
                details={"id": str(id), "error": str(e)},
            )
        
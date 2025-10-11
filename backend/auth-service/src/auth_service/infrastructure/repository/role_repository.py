import uuid

from sqlalchemy import insert, select, update, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.interface.repository.role_repository import RoleRepository


class RoleRepositoryImpl(RoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleEntity]:
        try:
            stmt = select(RoleEntity).order_by(RoleEntity.id.asc())
            if search:
                stmt = stmt.where(RoleEntity.name.ilike(f"%{search}%"))
            stmt = stmt.offset(offset).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleEntity]:
        try:
            stmt = select(RoleEntity).where(RoleEntity.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    
    async def get_by_name(self, name: str) -> Optional[RoleEntity]:
        try:
            stmt = select(RoleEntity).where(RoleEntity.name == name)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    
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
            print(result)
            return result.scalar_one_or_none()
        except Exception:
            return None
        
        
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
        except Exception:
            return None
    
    
    async def delete(self, id: uuid.UUID) -> Optional[RoleEntity]:
        try:
            stmt = (
                delete(RoleEntity)
                .where(RoleEntity.id == id)
                .returning(RoleEntity)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
        
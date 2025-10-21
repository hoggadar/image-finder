import uuid

from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.repository.role_repository import RoleRepository
from auth_service.core.entity.role_entity import RoleEntity
from auth_service.api.v1.schema.role_schema import RoleSchema, CreateRoleSchema, UpdateRoleSchema

class RoleServiceImpl(RoleService):
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo
    
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleSchema]:
        roles = await self.role_repo.get_all(offset=offset, limit=limit, search=search)
        return [self._entity_to_dto(role) for role in roles]
    
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleSchema]:
        role = await self.role_repo.get_by_id(id)
        if not role:
            return None
        return self._entity_to_dto(role)
    
    
    async def get_by_name(self, name: str) -> Optional[RoleSchema]:
        role = await self.role_repo.get_by_name(name)
        if not role:
            return None
        return self._entity_to_dto(role)
    
    
    async def create(self, dto: CreateRoleSchema) -> Optional[RoleSchema]:
        role = RoleEntity(
            name=dto.name,
            description=dto.description
        )
        created = await self.role_repo.create(role)
        if not created:
            return None
        await self.role_repo.session.commit()
        return self._entity_to_dto(created)
        
        
    
    async def update(self, dto: UpdateRoleSchema) -> Optional[RoleSchema]:
        existing_role = await self.role_repo.get_by_id(dto.id)
        if not existing_role:
            return None
        existing_role.name = dto.name
        existing_role.description = dto.description
        existing_role.updated_at = datetime.now(timezone.utc)
        updated = await self.role_repo.update(existing_role)
        if not updated:
            return None
        await self.role_repo.session.commit()
        return self._entity_to_dto(updated)
        
    
    async def delete(self, id: uuid.UUID) -> Optional[RoleSchema]:
        existing_role = await self.role_repo.get_by_id(id)
        if not existing_role:
            return None
        deleted = await self.role_repo.delete(id)
        if not deleted:
            return None
        await self.role_repo.session.commit()
        return self._entity_to_dto(deleted)
    
    
    def _entity_to_dto(self, entity: RoleEntity) -> RoleSchema:
        return RoleSchema(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
import uuid
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.repository.role_repository import RoleRepository
from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.dto.role_dto import RoleDTO, CreateRoleDTO, UpdateRoleDTO
from auth_service.app.exception import (
    RoleNotFoundException,
    RoleAlreadyExistsException,
    RoleCreationException,
    RoleUpdateException,
    RoleDeletionException,
)
from auth_service.infrastructure.exception.repository_exception import (
    RetrievalException,
    CreationExeption,
    UpdateException,
    DeletionException,
)


class RoleServiceImpl(RoleService):
    def __init__(self, role_repo: RoleRepository, session: AsyncSession):
        self.role_repo = role_repo
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleDTO]:
        try:
            roles = await self.role_repo.get_all(offset=offset, limit=limit, search=search)
            return [self._entity_to_dto(role) for role in roles]
        except RetrievalException as e:
            self.logger.error(f"Failed to retrieve roles: {e.message}", exc_info=True)
            raise RoleNotFoundException("Unable to retrieve roles list")
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleDTO]:
        try:
            role = await self.role_repo.get_by_id(id)
            if not role:
                self.logger.warning(f"Role with id '{id}' not found")
                raise RoleNotFoundException(str(id))
            return self._entity_to_dto(role)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving role by id '{id}': {e.message}", exc_info=True)
            raise RoleNotFoundException(str(id))
    
    async def get_by_name(self, name: str) -> Optional[RoleDTO]:
        try:
            role = await self.role_repo.get_by_name(name)
            if not role:
                self.logger.warning(f"Role with name '{name}' not found")
                raise RoleNotFoundException(name)
            return self._entity_to_dto(role)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving role by name '{name}': {e.message}", exc_info=True)
            raise RoleNotFoundException(name)
    
    async def create(self, dto: CreateRoleDTO) -> Optional[RoleDTO]:
        try:
            existing_role = await self.role_repo.get_by_name(dto.name)
            if existing_role:
                self.logger.warning(f"Role with name '{dto.name}' already exists")
                raise RoleAlreadyExistsException(dto.name)
            
            role = RoleEntity(
                name=dto.name,
                description=dto.description
            )
            created = await self.role_repo.create(role)
            if not created:
                await self.session.rollback()
                self.logger.error(f"Failed to create role '{dto.name}': repository returned None")
                raise RoleCreationException("Role was not created")
            await self.session.commit()
            return self._entity_to_dto(created)
            
        except RoleAlreadyExistsException:
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while creating role '{dto.name}': {e.message}", exc_info=True)
            raise RoleCreationException(f"Failed to create role: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while creating role '{dto.name}': {str(e)}", exc_info=True)
            raise RoleCreationException(f"Unexpected error during role creation")
        
        
    
    async def update(self, dto: UpdateRoleDTO) -> Optional[RoleDTO]:
        try:
            existing_role = await self.role_repo.get_by_id(dto.id)
            if not existing_role:
                self.logger.warning(f"Role with id '{dto.id}' not found for update")
                raise RoleNotFoundException(str(dto.id))
            
            if existing_role.name != dto.name:
                role_with_name = await self.role_repo.get_by_name(dto.name)
                if role_with_name and str(role_with_name.id) != str(dto.id):
                    self.logger.warning(f"Role name '{dto.name}' is already taken by another role")
                    raise RoleAlreadyExistsException(dto.name)
            
            existing_role.name = dto.name
            existing_role.description = dto.description
            existing_role.updated_at = datetime.now(timezone.utc)
            
            updated = await self.role_repo.update(existing_role)
            if not updated:
                await self.session.rollback()
                self.logger.error(f"Failed to update role '{dto.id}': repository returned None")
                raise RoleUpdateException("Role update failed")
            await self.session.commit()
            return self._entity_to_dto(updated)
            
        except (RoleNotFoundException, RoleAlreadyExistsException):
            await self.session.rollback()
            raise
        except (RetrievalException, UpdateException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while updating role '{dto.id}': {e.message}", exc_info=True)
            raise RoleUpdateException(f"Failed to update role: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while updating role '{dto.id}': {str(e)}", exc_info=True)
            raise RoleUpdateException(f"Unexpected error during role update")
        
    
    async def delete(self, id: uuid.UUID) -> Optional[RoleDTO]:
        try:
            existing_role = await self.role_repo.get_by_id(id)
            if not existing_role:
                self.logger.warning(f"Role with id '{id}' not found for deletion")
                raise RoleNotFoundException(str(id))
            
            deleted = await self.role_repo.delete(id)
            if not deleted:
                await self.session.rollback()
                self.logger.error(f"Failed to delete role '{id}': repository returned None")
                raise RoleDeletionException("Role deletion failed")
            
            await self.session.commit()
            return self._entity_to_dto(deleted)
            
        except RoleNotFoundException:
            await self.session.rollback()
            raise
        except (RetrievalException, DeletionException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while deleting role '{id}': {e.message}", exc_info=True)
            raise RoleDeletionException(f"Failed to delete role: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while deleting role '{id}': {str(e)}", exc_info=True)
            raise RoleDeletionException(f"Unexpected error during role deletion")
    
    
    def _entity_to_dto(self, entity: RoleEntity) -> RoleDTO:
        return RoleDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
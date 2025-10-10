from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.dto.role_dto import CreateRoleDTO
from auth_service.core.interface.service.role_service import RoleService


class DataSeeder:
    def __init__(self, session: AsyncSession, role_service: RoleService):
        self.session = session
        self.role_service = role_service
    
    
    async def seed_roles(self):
        default_roles = [
            CreateRoleDTO(name="Admin", description="Default"),
            CreateRoleDTO(name="Moderator", description="Default"),
            CreateRoleDTO(name="User", description="Default"),
        ]
        for role in default_roles:
            existing_role = await self.role_service.get_by_name(role.name)
            if not existing_role:
                await self.role_service.create(role)
        await self.session.commit()
    
    
    async def seed_users(self):
        pass
            
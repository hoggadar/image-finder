import logging

from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.entity.user_entity import UserEntity
from auth_service.core.dto.role_dto import CreateRoleDTO
from auth_service.core.dto.user_dto import CreateUserDTO
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.service.user_service import UserService


class DataSeeder:
    def __init__(self, role_service: RoleService, user_service: UserService):
        self.role_service = role_service
        self.user_service = user_service
    
    
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
    
    
    async def seed_users(self):
        default_user = [
            CreateUserDTO(
                first_name="Andrew",
                last_name="Ermolenko",
                email="admin@admin",
                username="a.ermolenko",
                password="admin",
                role="Admin"
            ),
            CreateUserDTO(
                first_name="Egor",
                last_name="Iniankov",
                email="e.iniankov@moderator",
                username="e.iniankov",
                password="e.iniankov",
                role="Moderator"
            ),
            CreateUserDTO(
                first_name="Lidia",
                last_name="Olgejzer",
                email="l.olgejzer@moderator",
                username="l.olgejzer",
                password="l.olgejzer",
                role="Moderator"
            ),
            CreateUserDTO(
                first_name="Rahmonjhon",
                last_name="Umarow",
                email="r.umarov@user",
                username="r.umarov",
                password="r.umarov",
                role="User"
            ),
        ]
        for user in default_user:
            existing_user = await self.user_service.get_by_email(user.email)
            if not existing_user:
                await self.user_service.create(user)
            
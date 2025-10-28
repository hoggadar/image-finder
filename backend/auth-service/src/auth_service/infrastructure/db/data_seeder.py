import logging

from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

from auth_service.core.dto.role_dto import CreateRoleDTO
from auth_service.core.dto.user_dto import CreateUserDTO
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.service.user_service import UserService
from auth_service.app.exception import (
    RoleNotFoundException,
    RoleAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyExistsException,
)


class DataSeeder:
    def __init__(self, role_service: RoleService, user_service: UserService):
        self.role_service = role_service
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)
    
    
    async def seed_roles(self):
        default_roles = [
            CreateRoleDTO(name="Admin", description="Default"),
            CreateRoleDTO(name="Moderator", description="Default"),
            CreateRoleDTO(name="User", description="Default"),
        ]
        for role in default_roles:
            try:
                existing_role = await self.role_service.get_by_name(role.name)
                self.logger.info(f"Role '{role.name}' already exists, skipping creation")
            except RoleNotFoundException:
                await self.role_service.create(role)
                self.logger.info(f"Successfully created role: {role.name}")
            except RoleAlreadyExistsException:
                self.logger.warning(f"Role '{role.name}' already exists (race condition)")
            except Exception as e:
                self.logger.error(f"Error processing role '{role.name}': {str(e)}", exc_info=True)
    
    
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
            try:
                existing_user = await self.user_service.get_by_email(user.email)
                self.logger.info(f"User with email '{user.email}' already exists, skipping creation")
            except UserNotFoundException:
                await self.user_service.create(user)
                self.logger.info(f"Successfully created user: {user.username} ({user.email})")
            except UserAlreadyExistsException:
                self.logger.warning(f"User '{user.username}' already exists (race condition)")
            except Exception as e:
                self.logger.error(f"Error processing user '{user.email}': {str(e)}", exc_info=True)
            
import uuid
import bcrypt
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.app.util.converter import Converter
from auth_service.core.entity.user_entity import UserEntity
from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema
from auth_service.core.interface.repository.user_repository import UserRepository
from auth_service.core.interface.service.user_service import UserService
from auth_service.app.service.role_service import RoleService
from auth_service.app.exception import (
    UserCreationException,
    UserNotFoundException,
    UserAlreadyExistsException,
    UserUpdateException,
    UserDeletionException,
    PasswordChangeException,
    RoleNotFoundException,
)
from auth_service.infrastructure.exception.repository_exception import (
    RetrievalException,
    CreationExeption,
    UpdateException,
    DeletionException,
)


class UserServiceImpl(UserService):
    def __init__(self, user_repo: UserRepository, role_service: RoleService, session: AsyncSession):
        self.user_repo = user_repo
        self.role_service = role_service
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserSchema]:
        try:
            users = await self.user_repo.get_all(offset=offset, limit=limit, search=search)
            return [self._entity_to_dto(user) for user in users]
        except RetrievalException as e:
            self.logger.error(f"Failed to retrieve users: {e.message}", exc_info=True)
            raise UserNotFoundException()

    async def get_by_id(self, id: str) -> Optional[UserSchema]:
        try:
            converted_id = Converter.get_uuid(id)
            user = await self.user_repo.get_by_id(converted_id)
            if not user:
                self.logger.warning(f"User with id '{id}' not found")
                raise UserNotFoundException(field="id", value=id)
            return self._entity_to_dto(user)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving user by id '{id}': {e.message}", exc_info=True)
            raise UserNotFoundException(field="id", value=id)
    
    async def get_by_full_name(self, fullname: str, offset: int = 0, limit: int = 10) -> Sequence[UserSchema]:
        try:
            users = await self.user_repo.get_by_full_name(fullname, offset=offset, limit=limit)
            self.logger.info(f"Successfully retrieved {len(users)} users with full name matching '{fullname}'")
            return [self._entity_to_dto(user) for user in users]
        except RetrievalException as e:
            self.logger.error(f"Failed to retrieve users by full name '{fullname}': {e.message}", exc_info=True)
            raise UserNotFoundException(field="full_name", value=fullname)

    async def get_by_username(self, username: str) -> Optional[UserSchema]:
        try:
            user = await self.user_repo.get_by_username(username)
            if not user:
                self.logger.warning(f"User with username '{username}' not found")
                raise UserNotFoundException(field="username", value=username)
            return self._entity_to_dto(user)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving user by username '{username}': {e.message}", exc_info=True)
            raise UserNotFoundException(field="username", value=username)

    async def get_by_email(self, email: str) -> Optional[UserSchema]:
        try:
            user = await self.user_repo.get_by_email(email)
            if not user:
                self.logger.warning(f"User with email '{email}' not found")
                raise UserNotFoundException(field="email", value=email)
            return self._entity_to_dto(user)
        except RetrievalException as e:
            self.logger.error(f"Database error while retrieving user by email '{email}': {e.message}", exc_info=True)
            raise UserNotFoundException(field="email", value=email)
    
    async def create(self, dto: CreateUserSchema) -> Optional[UserSchema]:
        try:
            existing_user_by_username = await self.user_repo.get_by_username(dto.username)
            if existing_user_by_username:
                self.logger.warning(f"User with username '{dto.username}' already exists")
                raise UserAlreadyExistsException(field="username", value=dto.username)
            
            existing_user_by_email = await self.user_repo.get_by_email(dto.email)
            if existing_user_by_email:
                self.logger.warning(f"User with email '{dto.email}' already exists")
                raise UserAlreadyExistsException(field="email", value=dto.email)
            
            role = await self.role_service.get_by_name(dto.role)
            if not role:
                self.logger.warning(f"Role '{dto.role}' not found")
                raise RoleNotFoundException(dto.role)
            
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(dto.password.encode("utf-8"), salt).decode("utf-8")
            
            user = UserEntity(
                first_name=dto.first_name,
                last_name=dto.last_name,
                username=dto.username,
                email=dto.email,
                password=hashed_password,
                role_id=role.id,
            )
            
            created_user = await self.user_repo.create(user)
            if not created_user:
                await self.session.rollback()
                self.logger.error(f"Failed to create user '{dto.username}': repository returned None")
                raise UserCreationException("User was not created")
            
            await self.session.commit()
            return self._entity_to_dto(created_user)
            
        except (UserAlreadyExistsException, RoleNotFoundException):
            await self.session.rollback()
            raise
        except (RetrievalException, CreationExeption) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while creating user '{dto.username}': {e.message}", exc_info=True)
            raise UserCreationException(f"Failed to create user: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while creating user '{dto.username}': {str(e)}", exc_info=True)
            raise UserCreationException(f"Unexpected error during user creation")
    
    async def update(self, dto: UpdateUserSchema) -> Optional[UserSchema]:
        try:
            converted_id = Converter.get_uuid(dto.id)
            existing_user = await self.user_repo.get_by_id(converted_id)
            if not existing_user:
                self.logger.warning(f"User with id '{dto.id}' not found for update")
                raise UserNotFoundException(field="id", value=str(dto.id))
            
            if existing_user.username != dto.username:
                user_with_username = await self.user_repo.get_by_username(dto.username)
                if user_with_username and str(user_with_username.id) != dto.id:
                    self.logger.warning(f"Username '{dto.username}' is already taken by another user")
                    raise UserAlreadyExistsException(field="username", value=dto.username)
            
            if existing_user.email != dto.email:
                user_with_email = await self.user_repo.get_by_email(dto.email)
                if user_with_email and str(user_with_email.id) != dto.id:
                    self.logger.warning(f"Email '{dto.email}' is already taken by another user")
                    raise UserAlreadyExistsException(field="email", value=dto.email)
            
            role = await self.role_service.get_by_name(dto.role)
            if not role:
                self.logger.warning(f"Role '{dto.role}' not found")
                raise RoleNotFoundException(dto.role)

            existing_user.first_name = dto.first_name
            existing_user.last_name = dto.last_name
            existing_user.username = dto.username
            existing_user.email = dto.email
            existing_user.role_id = role.id
            existing_user.updated_at = datetime.now(timezone.utc)

            updated_user = await self.user_repo.update(existing_user)
            if not updated_user:
                await self.session.rollback()
                self.logger.error(f"Failed to update user '{dto.id}': repository returned None")
                raise UserUpdateException("User update failed")
            
            await self.session.commit()
            return self._entity_to_dto(updated_user)
            
        except (UserNotFoundException, UserAlreadyExistsException, RoleNotFoundException):
            await self.session.rollback()
            raise
        except (RetrievalException, UpdateException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while updating user '{dto.id}': {e.message}", exc_info=True)
            raise UserUpdateException(f"Failed to update user: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while updating user '{dto.id}': {str(e)}", exc_info=True)
            raise UserUpdateException(f"Unexpected error during user update")
    
    async def delete(self, id: str) -> Optional[UserSchema]:
        try:
            converted_id = Converter.get_uuid(id)
            user = await self.user_repo.get_by_id(converted_id)
            if not user:
                self.logger.warning(f"User with id '{id}' not found for deletion")
                raise UserNotFoundException(field="id", value=id)

            deleted_user = await self.user_repo.delete(converted_id)
            if not deleted_user:
                await self.session.rollback()
                self.logger.error(f"Failed to delete user '{id}': repository returned None")
                raise UserDeletionException("User deletion failed")
            
            await self.session.commit()
            self.logger.info(f"Successfully deleted user with id: {id}")
            return self._entity_to_dto(deleted_user)
            
        except UserNotFoundException:
            await self.session.rollback()
            raise
        except (RetrievalException, DeletionException) as e:
            await self.session.rollback()
            self.logger.error(f"Database error while deleting user '{id}': {e.message}", exc_info=True)
            raise UserDeletionException(f"Failed to delete user: {e.message}")
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Unexpected error while deleting user '{id}': {str(e)}", exc_info=True)
            raise UserDeletionException(f"Unexpected error during user deletion")
    
    async def change_password(self, dto):
        raise NotImplementedError("Password change functionality is not yet implemented")
    
    def _entity_to_dto(self, entity: UserEntity) -> UserSchema:
        return UserSchema(
            id=str(entity.id),
            first_name=entity.first_name,
            last_name=entity.last_name,
            username=entity.username,
            email=entity.email,
            role_id=str(entity.role_id),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
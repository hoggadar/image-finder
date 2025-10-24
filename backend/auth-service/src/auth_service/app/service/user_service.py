import uuid
from auth_service.app.util.converter import Converter
import bcrypt
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import Sequence, Optional
from datetime import datetime, timezone

from auth_service.core.entity.user_entity import UserEntity
from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema
from auth_service.core.interface.repository.user_repository import UserRepository
from auth_service.core.interface.service.user_service import UserService
from auth_service.app.service.role_service import RoleService
from auth_service.api.exception.user_exception import UserNotFoundError, UserAlreadyExistsError, PasswordChangeError
from auth_service.api.exception.role_exception import RoleNotFoundError


class UserServiceImpl(UserService):
    def __init__(self, user_repo: UserRepository, role_service: RoleService, session: AsyncSession):
        self.user_repo = user_repo
        self.role_service = role_service
        self.session = session
    
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserSchema]:
        users = await self.user_repo.get_all(offset=offset, limit=limit, search=search)
        return [self._entity_to_dto(user) for user in users]

    async def get_by_id(self, id: str) -> Optional[UserSchema]:
        converted_id = Converter.get_uuid(id)
        user = await self.user_repo.get_by_id(converted_id)
        if not user:
            raise UserNotFoundError(id)
        return self._entity_to_dto(user)
    
    async def get_by_fullname(self, fullname: str, offset: int = 0, limit: int = 10) -> Sequence[UserSchema]:
        users = await self.user_repo.get_by_fullname(fullname, offset=offset, limit=limit)
        return [self._entity_to_dto(user) for user in users]

    async def get_by_username(self, username: str) -> Optional[UserSchema]:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundError(username)
        return self._entity_to_dto(user)

    async def get_by_email(self, email: str) -> Optional[UserSchema]:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserNotFoundError(email)
        return self._entity_to_dto(user)
    
    async def create(self, dto: CreateUserSchema) -> Optional[UserSchema]:
        role = await self.role_service.get_by_name(dto.role)
        if not role:
            raise RoleNotFoundError(dto.role)
        
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError("email")
        
        existing_user = await self.user_repo.get_by_username(dto.username)
        if existing_user:
            raise UserAlreadyExistsError("username")
        
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
            return None
        await self.session.commit()
        return self._entity_to_dto(created_user)
        
    
    async def update(self, dto: UpdateUserSchema) -> Optional[UserSchema]:
        converted_id = Converter.get_uuid(dto.id)
        existing_user = await self.user_repo.get_by_id(converted_id)
        if not existing_user:
            raise UserAlreadyExistsError(str(dto.id))
        
        role = await self.role_service.get_by_name(dto.role)
        if not role:
            raise RoleNotFoundError(dto.role)

        existing_user.first_name = dto.first_name
        existing_user.last_name = dto.last_name
        existing_user.username = dto.username
        existing_user.email = dto.email
        existing_user.role_id = role.id
        existing_user.updated_at = datetime.now(timezone.utc)

        updated_user = await self.user_repo.update(existing_user)
        if not updated_user:
            await self.session.rollback()
            return None
        await self.session.commit()
        return self._entity_to_dto(updated_user)
    
    async def delete(self, id: str) -> Optional[UserSchema]:
        logging.info("types of input: {} {}".format(type(id), type(Converter.get_uuid(id))))
        converted_id = Converter.get_uuid(id)
        user = await self.user_repo.get_by_id(converted_id)
        if not user:
            raise UserNotFoundError(id)

        deleted_user = await self.user_repo.delete(converted_id)
        if not deleted_user:
            await self.session.rollback()
            return None
        await self.session.commit()
        return self._entity_to_dto(deleted_user)
    
    async def change_password(self, dto):
        raise NotImplemented
    
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
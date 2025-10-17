from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.infrastructure.db.database import database
from auth_service.core.interface.repository.role_repository import RoleRepository
from auth_service.core.interface.repository.user_repository import UserRepository
# from auth_service.core.interface.repository.token_repository import TokenRepository
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.service.user_service import UserService
# from auth_service.core.interface.service.token_service import TokenService
from auth_service.infrastructure.repository.role_repository import RoleRepositoryImpl
from auth_service.infrastructure.repository.user_repository import UserRepositoryImpl
from auth_service.app.service.role_service import RoleServiceImpl
from auth_service.app.service.user_service import UserServiceImpl


# Repositories

def get_role_repo(session: AsyncSession = Depends(database.get_session)):
    return RoleRepositoryImpl(session=session)

def get_user_repo(session: AsyncSession = Depends(database.get_session)):
    return UserRepositoryImpl(session=session)

# Services

def get_role_service(role_repo: RoleRepository = Depends(get_role_repo)):
    return RoleServiceImpl(role_repo=role_repo)

def get_user_service(user_repo: UserRepository = Depends(get_user_repo),
                     role_service: RoleService = Depends(get_role_service),
                     session: AsyncSession = Depends(database.get_session)):
    return UserServiceImpl(user_repo=user_repo, role_service=role_service, session=session)

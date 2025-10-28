import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.core.entity.base_entity import Base

if TYPE_CHECKING:
    from auth_service.core.entity.role_entity import RoleEntity
    from auth_service.core.entity.token_entity import RefreshTokenEntity


class UserEntity(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    username: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    role_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("roles.id"), nullable=False)
    role: Mapped["RoleEntity"] = relationship(back_populates="users")
    
    refresh_token: Mapped["RefreshTokenEntity"] = relationship(back_populates="user")
    
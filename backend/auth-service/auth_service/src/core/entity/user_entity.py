import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.entity.base import Base

if TYPE_CHECKING:
    from core.entity.role_entity import RoleEntity
    from core.entity.token_entity import TokenEntity


class UserEntity(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    user_name: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    
    role_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    role: Mapped["RoleEntity"] = relationship(back_populates="roles.id")
    
    token: Mapped["TokenEntity"] = relationship(back_populates="user")
    
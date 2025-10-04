import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.src.core.entity.base import Base

if TYPE_CHECKING:
    from auth_service.src.core.entity.user_entity import UserEntity


class RoleEntity(Base):
    __tablename__ = "roles"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    users: Mapped[list["UserEntity"]] = relationship(back_populates="role")

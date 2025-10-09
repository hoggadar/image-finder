import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID, String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.core.entity.base import Base

if TYPE_CHECKING:
    from auth_service.core.entity.user_entity import UserEntity


class TokenEntity(Base):
    __tablename__ = "tokens"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), unique=True, nullable=False)
    user: Mapped["UserEntity"] = relationship(back_populates="token")
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth_service.core.entity.base import Base

if TYPE_CHECKING:
    from src.auth_service.core.entity.user_entity import UserEntity


class TokenEntity(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True)
    user: Mapped["UserEntity"] = relationship(back_populates="token")
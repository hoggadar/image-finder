from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from auth_service.config import config


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=config.db.naming_convention
    )
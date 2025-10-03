from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=config.db.naming_convention
    )
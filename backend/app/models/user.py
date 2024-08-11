from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.types import Integer

from app.models.base import Base, EmptyBase


class User(SQLAlchemyBaseUserTable[int], Base):
    pass


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], EmptyBase):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
        )

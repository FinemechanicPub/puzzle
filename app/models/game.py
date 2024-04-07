from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import SmallInteger

from app.models.base import Base


class Game(Base):

    width: Mapped[int] = mapped_column(SmallInteger)
    height: Mapped[int] = mapped_column(SmallInteger)

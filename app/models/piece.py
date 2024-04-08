from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, SmallInteger, String

from app.models.base import Base


class Piece(Base):
    name: Mapped[str] = mapped_column(String(1))
    size: Mapped[int] = mapped_column(SmallInteger)
    points: Mapped[list] = mapped_column(JSON)

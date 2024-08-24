from sqlalchemy import JSON, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Menu(Base):
    order: Mapped[int] = mapped_column(SmallInteger)
    title: Mapped[str]
    query: Mapped[dict[str, str]] = mapped_column(JSON)

    def __repr__(self) -> str:
        return (
            f"Menu(id={self.id}, title={self.title}, "
            f"query={self.query}, order={self.order})"
        )

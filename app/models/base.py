from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)


# https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html
class EmptyBase(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Base(EmptyBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

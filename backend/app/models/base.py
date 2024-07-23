from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)


# https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html
class EmptyBase(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Base(EmptyBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

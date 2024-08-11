from typing import Generic, Optional, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnExpressionArgument, func

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class RepositoryBase(Generic[ModelType]):

    force_unique = False

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def selector(self):
        return select(self.model)

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        db_obj = await session.execute(
            self.selector().where(self.model.id == id)
        )
        return db_obj.scalars().first()

    async def list(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: Optional[int] = None,
        ids: Optional[Sequence[int]] = None,
        clause: Optional[ColumnExpressionArgument[bool]] = None,
        random: bool = False,
        **kwargs,
    ):
        statement = self.selector(**kwargs)
        if ids is not None:
            statement = statement.where(self.model.id.in_(ids))
        if clause is not None:
            statement = statement.where(clause)
        if random:
            statement = statement.order_by(func.random())
        db_objs = await session.execute(statement.offset(offset).limit(limit))
        refined_objs = db_objs.unique() if self.force_unique else db_objs
        return refined_objs.scalars().all()

    async def create(
        self, session: AsyncSession, data: BaseModel, commit: bool = True
    ):
        instance = self.model(**data.model_dump())
        session.add(instance)
        if commit:
            await session.commit()
            await session.refresh(instance)
        return instance

    async def update(
        self,
        session: AsyncSession,
        instance: ModelType,
        data: BaseModel,
        commit: bool = True,
    ):
        instance_data = jsonable_encoder(instance)
        updates_dict = data.model_dump(exclude_unset=True)
        for field in instance_data:
            if field in updates_dict:
                setattr(instance, field, updates_dict[field])
        session.add(instance)
        if commit:
            await session.commit()
            await session.refresh(instance)
        return instance

    async def remove(self, session: AsyncSession, instance: ModelType):
        await session.delete(instance)
        await session.commit()
        return instance

from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            instance_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == instance_id
            )
        )
        return db_obj.scalars().first()

    async def get_many(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            data: BaseModel,
            session: AsyncSession,
            extra: Optional[dict] = None,
            commit: Optional[bool] = True
    ):
        data_dict = data.model_dump()
        if extra is not None:
            data_dict.update(extra)
        instance = self.model(**data_dict)
        session.add(instance)
        if commit:
            await session.commit()
            await session.refresh(instance)
        return instance

    async def update(
            self,
            instance,
            data: BaseModel,
            session: AsyncSession,
            commit: Optional[bool] = True
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

    async def remove(
            self,
            instance,
            session: AsyncSession,
    ):
        await session.delete(instance)
        await session.commit()
        return instance

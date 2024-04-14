from typing import Optional

from app.crud.base import AsyncSession, CRUDBase
from app.core.base import Piece
from app.models.game import PieceRotation
from engine.piece import produce_rotations
from app.schemas.piece import PieceBase as PieceSchema


class CRUDGame(CRUDBase):
    async def create_piece(
            self,
            data: PieceSchema,
            session: AsyncSession,
            commit: Optional[bool] = True
    ):
        extra = {"size": len(data.points)}
        instance: Piece = await self.create(data, session, extra, commit=False)
        rotations = produce_rotations(data.points)
        for order, rotation in enumerate(rotations, 1):
            instance.rotations.append(
                PieceRotation(piece=instance, order=order, points=rotation)
            )
        if commit:
            await session.commit()
            await session.refresh(instance)
        return instance


piece_crud = CRUDGame(Piece)

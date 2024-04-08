from typing import Optional

from app.crud.base import AsyncSession, CRUDBase
from app.models.piece import Piece
from app.schemas.piece import Piece as PieceSchema


class CRUDGame(CRUDBase):
    async def create_piece(
            self,
            data: PieceSchema,
            session: AsyncSession,
            commit: Optional[bool] = True
    ):
        extra = {"size": len(data.points)}
        instance = await self.create(data, session, extra, commit)
        return instance


piece_crud = CRUDGame(Piece)

from pydantic import BaseModel, Field

from app.schemas.piece import PiecePlacement


class HintRequest(BaseModel):
    game_id: int = Field(..., ge=0)
    pieces: list[PiecePlacement]

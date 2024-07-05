from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.piece import PiecePlacement


class GameStatus(IntEnum):
    progress = 1
    complete = 2
    deadlock = 3


class HintRequest(BaseModel):
    game_id: int = Field(..., ge=0)
    pieces: list[PiecePlacement]


class HintResponse(BaseModel):
    status: GameStatus
    hint: Optional[PiecePlacement]

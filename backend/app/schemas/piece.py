from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.core.config import settings


class PieceBase(BaseModel):
    name: str = Field(..., max_length=1)
    points: tuple[tuple[int, int], ...]

    @computed_field
    @property
    def size(self) -> int:
        return len(self.points)


class PieceGetResponse(PieceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PiecePlacement(BaseModel):
    piece_id: int = Field(..., ge=0)
    rotation_id: int = Field(..., ge=0)
    position: int = Field(..., ge=0, le=settings.max_cells)

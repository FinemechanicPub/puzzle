from pydantic import BaseModel, ConfigDict, Field


class PieceBase(BaseModel):
    name: str = Field(..., max_length=1)
    points: tuple[tuple[int, int], ...]


class PieceGetResponse(PieceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

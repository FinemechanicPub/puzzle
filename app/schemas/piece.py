from pydantic import BaseModel, ConfigDict, Field


# class Point(BaseModel):
#     row: int = Field(..., ge=0)
#     col: int = Field(..., ge=0)


class PieceBase(BaseModel):
    name: str = Field(..., max_length=1)
    points: tuple[tuple[int, int], ...]


class PieceGetResponse(PieceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PieceGetLongResponse(PieceGetResponse):
    rotations: list[list[tuple[int, int]]]

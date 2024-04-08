from pydantic import BaseModel, ConfigDict, Field


class Piece(BaseModel):
    name: str = Field(..., max_length=1)
    points: list[tuple[int, int]]

    model_config = ConfigDict(title='Фигура')


class PieceEntity(Piece):
    id: int

    model_config = ConfigDict(from_attributes=True)

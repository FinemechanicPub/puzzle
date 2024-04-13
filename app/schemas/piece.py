from pydantic import BaseModel, ConfigDict, Field


class PieceCreateRequest(BaseModel):
    name: str = Field(..., max_length=1)
    points: list[tuple[int, int]]


class PieceGetResponse(PieceCreateRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)

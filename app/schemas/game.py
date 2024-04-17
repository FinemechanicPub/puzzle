from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class PieceColor(BaseModel):
    id: int
    color: int | str

    @field_validator('color')
    def validate_color(cls, value, info: FieldValidationInfo):
        if isinstance(value, str):
            return int(value, 16)
        if isinstance(value, int):
            return value
        raise ValueError("Value cannot be converted to integer number")


class CreateGameRequest(BaseModel):
    width: int = Field(..., ge=1, le=60)
    height: int = Field(..., ge=1, le=60)
    pieces: list[PieceColor]


class GamePieceResponse(BaseModel):
    id: int = Field(..., validation_alias='piece_id')
    name: str = Field(..., validation_alias='piece_name')
    color: int
    points: list[tuple[int, int]]

    model_config = ConfigDict(from_attributes=True)


class Rotation(BaseModel):
    id: int
    points: list[tuple[int, int]]


class GamePieceResponseLong(BaseModel):
    id: int = Field(..., validation_alias='piece_id')
    name: str = Field(..., validation_alias='piece_name')
    color: int

    rotations: list[Rotation]

    model_config = ConfigDict(from_attributes=True)


class GameResponseBase(BaseModel):
    id: int
    width: int
    height: int

    model_config = ConfigDict(from_attributes=True)


class GameResponse(GameResponseBase):

    pieces: list[GamePieceResponse] = Field(
        ..., validation_alias='game_pieces'
    )

    model_config = ConfigDict(from_attributes=True)


class GameResponseLong(GameResponseBase):

    pieces: list[GamePieceResponseLong] = Field(
        ..., validation_alias='game_pieces'
    )

    model_config = ConfigDict(from_attributes=True)

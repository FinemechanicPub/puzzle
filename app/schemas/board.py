from pydantic import BaseModel, ConfigDict, Field


class Board(BaseModel):
    width: int = Field(..., ge=1, le=60)
    height: int = Field(..., ge=1, le=60)

    model_config = ConfigDict(title='Конфигурация игрового поля')


class BoardEntity(Board):
    id: int

    model_config = ConfigDict(from_attributes=True)

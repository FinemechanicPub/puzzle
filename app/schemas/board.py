from pydantic import BaseModel, ConfigDict, Field


class Board(BaseModel):
    width: int = Field(..., ge=1, le=10)
    height: int = Field(..., ge=1, le=6)

    model_config = ConfigDict(title='Конфигурация игрового поля')

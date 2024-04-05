from pydantic import BaseModel, Field


class Board(BaseModel):
    width: int = Field(..., ge=1, le=10)
    height: int = Field(..., ge=1, le=6)

    class Config:
        title = 'Конфигурация игрового поля'

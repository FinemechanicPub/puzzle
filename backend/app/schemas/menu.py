from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MenuBase(BaseModel):
    title: str = Field(..., min_length=1)
    query: dict[str, str | int]
    order: int = Field(..., ge=0)


class MenuUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    query: Optional[dict[str, str | int]] = Field(None)
    order: Optional[int] = Field(None, ge=0)


class MenuResponse(MenuBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

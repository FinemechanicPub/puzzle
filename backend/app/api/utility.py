from fastapi import Query
from app.core.config import settings


class OffsetLimit:
    def __init__(self, offset: int = 0, limit: int = settings.page_limit):
        self.offset = offset
        self.limit = limit


class GameParameters:
    def __init__(
        self,
        height: int = Query(5, ge=3, le=20),
        width: int = Query(5, ge=3, le=20),
    ):
        self.height = height
        self.width = width

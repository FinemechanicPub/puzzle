from app.core.config import settings


class OffsetLimit:
    def __init__(self, offset: int = 0, limit: int = settings.page_limit):
        self.offset = offset
        self.limit = limit

from fastapi import FastAPI

from app.core.config import settings
from app.api.endpoints import router

# Создание объекта приложения.
app = FastAPI(title=settings.app_title)
app.include_router(router)

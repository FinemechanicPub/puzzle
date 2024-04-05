from fastapi import FastAPI

from app.api.endpoints import router

# Создание объекта приложения.
app = FastAPI()
app.include_router(router)

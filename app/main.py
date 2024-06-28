from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers import main_router

# Создание объекта приложения.
app = FastAPI(title=settings.app_title)

# Подключение роутера
app.include_router(main_router)

# Включение заголовков CORS в ответы сервера
# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

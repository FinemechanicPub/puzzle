from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.core.config import settings
from app.api.routers import main_router


# Настройка идентификаторов для OpenAPI
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


# Создание объекта приложения.
app = FastAPI(
    title=settings.app_title,
    generate_unique_id_function=custom_generate_unique_id,
)

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

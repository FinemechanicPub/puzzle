from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.api.routers import main_router


# Настройка идентификаторов для OpenAPI
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


# Создание объекта приложения.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan,
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

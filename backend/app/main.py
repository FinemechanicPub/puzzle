import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
import uvicorn

from app.color_logging import ColorFormatter
from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.api.routers import main_router


# Настройка протоколирования
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter(
    fmt="{levelname}{asctime} - {message}",
    datefmt="%H:%M:%S",
    style="{"
))
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger(__name__)


# Настройка идентификаторов для OpenAPI
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


# Создание объекта приложения.
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await create_first_superuser()
    yield


app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

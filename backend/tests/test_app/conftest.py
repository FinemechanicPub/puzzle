# https://gist.github.com/e-kondr01/969ae24f2e2f31bd52a81fa5a1fe0f96

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)

# Importing fastapi.Depends that is used to retrieve SQLAlchemy's session
from app.core.db import get_async_session

# Importing main FastAPI instance
from app.main import app

# Importing model base
from app.core.base import Base

# To run async tests
pytestmark = pytest.mark.anyio

# Supply connection string
engine = create_async_engine("sqlite+aiosqlite:///:memory:")


SAVEPOINT_MODE = "conditional_savepoint"


# Required per
# https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def create_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction
        await transaction.rollback()


@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode=SAVEPOINT_MODE,
    )
    yield async_session


@pytest.fixture()
async def user_client(
    session: AsyncSession, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:

    async def override_get_async_session() -> (
        AsyncGenerator[AsyncSession, None]
    ):
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session
    # https://www.python-httpx.org/advanced/transports/#asgi-transport
    transport = ASGITransport(app=app)  # type: ignore until 0.27.1 of httpx
    yield AsyncClient(transport=transport, base_url="http://testserver")
    del app.dependency_overrides[get_async_session]

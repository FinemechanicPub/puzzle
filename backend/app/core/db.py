from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlite3 import Connection as SQLite3Connection

from app.core.config import settings

engine = create_async_engine(settings.connection_string)
AsyncSessionLocal = async_sessionmaker(engine)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session

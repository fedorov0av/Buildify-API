import contextlib
from typing import Any, AsyncIterator, Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from ..config.consts import config


DATABASE_URL = config["DATABASE_URL"]
DATABASE_IP = config["DB_HOST"]
DATABASE_USER = config["DB_USER"]
DATABASE_PASSWORD = config["DB_PASSWORD"]
DATABASE_NAME = config["DB_NAME"]

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(DATABASE_URL, {"echo": True})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
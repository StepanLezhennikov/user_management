from typing import AsyncGenerator

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.sqla import SqlAlchemyDatabase
from app.core.config import Settings
from tests.alembic.utils import drop_database, create_database, apply_migrations


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = Settings()
    settings.DATABASE_URL += "_test"
    return settings


@pytest.fixture(scope="session")
async def setup_sqla_db(settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
    await create_database(settings.DATABASE_URL)

    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)

    try:
        async with engine.begin() as conn:
            await conn.run_sync(apply_migrations)
        yield engine
    finally:
        await drop_database(settings.DATABASE_URL)
        await engine.dispose()


@pytest.fixture(scope="session")
async def test_sqla_db(settings: Settings, setup_sqla_db) -> SqlAlchemyDatabase:
    return SqlAlchemyDatabase(settings)


@pytest.fixture(scope="session")
async def sqla_engine(
    test_sqla_db: SqlAlchemyDatabase,
) -> AsyncGenerator[AsyncEngine, None]:
    yield test_sqla_db.engine
    await test_sqla_db.engine.dispose()


@pytest.fixture()
async def session_factory(
    sqla_engine: AsyncEngine,
    test_sqla_db: SqlAlchemyDatabase,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    connection = await sqla_engine.connect()
    trans = await connection.begin()
    yield async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    await trans.rollback()
    await connection.close()


@pytest.fixture()
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session

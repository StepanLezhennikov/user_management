import asyncio
from typing import Generator, AsyncGenerator
from asyncio import AbstractEventLoop

import pytest
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.sqla import SqlAlchemyDatabase
from app.core.config import Settings
from app.schemas.user import User, UserCreate
from tests.alembic.utils import drop_database, create_database, apply_migrations
from app.infra.repositories.models.user_model import User as UserModel


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = Settings()
    settings.DATABASE_URL += "_test"
    return settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


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
def test_sqla_db(settings: Settings, setup_sqla_db) -> SqlAlchemyDatabase:
    return SqlAlchemyDatabase(settings)


@pytest.fixture(scope="function", autouse=True)
async def clean_db(session: AsyncSession) -> None:
    await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    await session.commit()


@pytest.fixture(scope="session")
async def sqla_engine(
    test_sqla_db: SqlAlchemyDatabase,
) -> AsyncGenerator[AsyncEngine, None]:
    yield test_sqla_db.engine
    await test_sqla_db.engine.dispose()


@pytest.fixture(scope="session")
async def session_factory(
    sqla_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=sqla_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture(scope="session")
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncSession:
    async with session_factory() as session:
        yield session


@pytest.fixture
async def user_create() -> UserCreate:
    return UserCreate(
        username="test_user",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="test_password",
    )


@pytest.fixture
async def created_user(session: AsyncSession, user_create: UserCreate) -> User:
    added_user = UserModel(
        username=user_create.username,
        email=str(user_create.email),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=user_create.password,
    )
    session.add(added_user)
    await session.flush()
    await session.commit()
    return added_user

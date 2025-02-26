import asyncio
from typing import Generator, AsyncGenerator
from asyncio import AbstractEventLoop

import redis
import pytest
import aioboto3
from pydantic import EmailStr
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.sqla import SqlAlchemyDatabase
from app.db.redis import redis_db
from app.core.config import Settings, Constants
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.user import User, UserCreate
from app.infra.uow.uow import Uow
from tests.alembic.utils import drop_database, create_database, apply_migrations
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.services.services.jwt import JwtService
from app.infra.clients.aws.email import EmailClient
from app.infra.repositories.user import UserRepository
from app.api.interfaces.services.jwt import AJwtService
from app.services.interfaces.uow.uow import AUnitOfWork
from app.services.services.password_security import PasswordSecurityService
from app.infra.repositories.models.user_model import Role
from app.infra.repositories.models.user_model import User as UserModel
from app.infra.repositories.models.user_model import Permission as PermissionModel
from app.api.interfaces.services.password_security import APasswordSecurityService
from app.services.interfaces.repositories.user_repository import AUserRepository


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


@pytest.fixture(autouse=True)
async def clean_db(session: AsyncSession) -> None:
    await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    await session.execute(text("TRUNCATE TABLE roles RESTART IDENTITY CASCADE"))
    await session.execute(text("TRUNCATE TABLE permissions RESTART IDENTITY CASCADE"))
    redis_db.flushall()
    await session.commit()


@pytest.fixture(scope="session")
async def sqla_engine(
    test_sqla_db: SqlAlchemyDatabase,
) -> AsyncGenerator[AsyncEngine, None]:
    yield test_sqla_db.engine
    await test_sqla_db.engine.dispose()


@pytest.fixture(scope="session")
def session_factory(
    sqla_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=sqla_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture(scope="function")
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncSession:
    async with session_factory() as session:
        yield session
        await session.flush()
        await session.rollback()


@pytest.fixture
def user_create() -> UserCreate:
    return UserCreate(
        username="test_user",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="test_password",
        roles=["Admin"],
    )


@pytest.fixture
def role_create() -> RoleCreate:
    return RoleCreate(role="Admin", permissions_ids=[1])


@pytest.fixture
def permission_create() -> PermissionCreate:
    return PermissionCreate(name="test_permission", description="test_permission")


@pytest.fixture
def permission_update() -> PermissionUpdate:
    return PermissionUpdate(name="new", description="new")


@pytest.fixture
def role_update() -> RoleUpdate:
    return RoleUpdate(role="new role")


@pytest.fixture
async def created_user(
    session: AsyncSession,
    user_create: UserCreate,
    password_security_service: PasswordSecurityService,
) -> User:
    added_user = UserModel(
        username=user_create.username,
        email=str(user_create.email),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=password_security_service.hash_password(user_create.password),
    )
    session.add(added_user)
    await session.flush()
    await session.commit()
    return added_user


@pytest.fixture
async def created_role(
    session: AsyncSession,
    role_create: RoleCreate,
) -> RoleCreate:
    new_role = Role(role=role_create.role)
    session.add(new_role)
    await session.flush()
    await session.commit()
    return role_create


@pytest.fixture
async def created_permission(
    session: AsyncSession,
    permission_create: PermissionCreate,
) -> PermissionCreate:
    new_perm = PermissionModel(
        name=permission_create.name, description=permission_create.description
    )
    session.add(new_perm)
    session.add(new_perm)
    await session.flush()
    await session.commit()
    return permission_create


@pytest.fixture
def email() -> EmailStr:
    return "test@example.com"


@pytest.fixture
def code() -> int:
    return 1111


@pytest.fixture
def aioboto3_session(settings) -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )


@pytest.fixture(scope="session")
async def uow(session_factory: async_sessionmaker[AsyncSession]) -> AUnitOfWork:
    return Uow(session_factory)


@pytest.fixture
def email_client(aioboto3_session) -> EmailClient:
    return EmailClient(aioboto3_session=aioboto3_session)


@pytest.fixture
async def user_repo(session: AsyncSession) -> AUserRepository:
    return UserRepository(session)


@pytest.fixture
async def password_security_service(uow: AUnitOfWork) -> APasswordSecurityService:
    return PasswordSecurityService(uow=uow)


@pytest.fixture
def jwt_service(user_repo: UserRepository) -> AJwtService:
    return JwtService(user_repo)


@pytest.fixture
def redis_database(settings) -> redis.Redis:
    return redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


@pytest.fixture
def created_code(email: EmailStr, redis_database: redis.Redis, code: int) -> int:
    return (
        code
        if bool(
            redis_database.set(str(email), code, ex=Constants.expiration_time_for_code)
        )
        else 0
    )


@pytest.fixture
def new_password() -> str:
    return "new_password"


@pytest.fixture
def new_hashed_password(
    password_security_service: PasswordSecurityService, new_password
) -> str:
    return password_security_service.hash_password(new_password)

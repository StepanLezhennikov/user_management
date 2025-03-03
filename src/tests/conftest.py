import asyncio
from typing import Generator, AsyncGenerator
from asyncio import AbstractEventLoop

import redis
import pytest
import aioboto3
from pydantic import EmailStr
from sqlalchemy import NullPool, text, select
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
from app.schemas.user import User, UserCreate, UserSignIn, UserForToken
from app.infra.uow.uow import Uow
from tests.alembic.utils import drop_database, create_database, apply_migrations
from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
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
    return RoleCreate(role="test_role", permissions_ids=[1])


@pytest.fixture
async def role_create_admin(
    permission_create_list: list[PermissionCreate],
    session: AsyncSession,
) -> RoleCreate:
    query = select(PermissionModel.id).where(
        PermissionModel.name.in_([perm.name for perm in permission_create_list])
    )
    result = await session.execute(query)
    permissions_ids = list(result.scalars().all())
    return RoleCreate(role="Admin", permissions_ids=permissions_ids)


@pytest.fixture
def permission_create() -> PermissionCreate:
    return PermissionCreate(name="test_permission", description="test_permission")


@pytest.fixture
def permission_create_list() -> list[PermissionCreate]:
    permissions = [
        PermissionCreate(name=name, description=description)
        for name, description in Constants().PERMISSIONS.items()
    ]
    return permissions


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
    created_role_admin: RoleCreate,
) -> User:
    added_user = UserModel(
        username=user_create.username,
        email=str(user_create.email),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=password_security_service.hash_password(user_create.password),
    )

    query = select(Role).where(Role.role == created_role_admin.role)
    result = await session.execute(query)
    role = result.scalar_one_or_none()

    added_user.roles = [role]

    session.add(added_user)
    await session.flush()
    await session.commit()
    return User.model_validate(added_user)


@pytest.fixture
async def created_role_admin(
    session: AsyncSession,
    role_create_admin: RoleCreate,
    created_permission_list: list[PermissionCreate],
) -> RoleCreate:
    new_role = Role(role=role_create_admin.role)

    query = select(PermissionModel).filter(
        PermissionModel.name.in_(
            [permission.name for permission in created_permission_list]
        )
    )
    result = await session.execute(query)
    permissions = result.scalars().all()
    new_role.permissions = permissions

    session.add(new_role)
    await session.flush()
    await session.commit()
    return role_create_admin


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
async def created_permission_list(
    session: AsyncSession,
    permission_create_list: list[PermissionCreate],
) -> list[Permission]:

    new_permissions = [
        PermissionModel(name=permission.name, description=permission.description)
        for permission in permission_create_list
    ]
    session.add_all(new_permissions)
    await session.flush()
    await session.commit()
    return new_permissions


@pytest.fixture
async def created_permission(
    session: AsyncSession,
    permission_create: PermissionCreate,
) -> Permission:

    new_permission = PermissionModel(
        name=permission_create.name, description=permission_create.description
    )

    session.add(new_permission)
    await session.flush()
    await session.commit()
    return new_permission


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


@pytest.fixture
def user_for_token(
    created_user: User, permission_create_list: list[PermissionCreate]
) -> UserForToken:
    return UserForToken(
        id=created_user.id,
        permissions=[permission.name for permission in permission_create_list],
    )


@pytest.fixture
def created_access_token(jwt_service: JwtService, user_for_token: UserForToken) -> str:
    return jwt_service.create_access_token(user_for_token.model_dump())


@pytest.fixture
def user_sign_in() -> UserSignIn:
    return UserSignIn(email="test@example.com", password="test_password")

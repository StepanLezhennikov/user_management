import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infra.uow.uow import Uow
from app.services.services.auth import AuthService
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.auth import AAuthService


@pytest.fixture(scope="session")
async def uow(session_factory: async_sessionmaker[AsyncSession]) -> AUnitOfWork:
    return Uow(session_factory)


@pytest.fixture(scope="function")
async def auth_service(uow: AUnitOfWork) -> AAuthService:
    return AuthService(uow)

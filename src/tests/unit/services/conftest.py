import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.redis import redis_db
from app.core.config import Constants
from app.infra.uow.uow import Uow
from app.services.services.auth import AuthService
from app.services.services.email import EmailService
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.auth import AAuthService
from app.api.interfaces.services.email import AEmailService
from app.services.services.code_verification import CodeVerificationService
from app.infra.repositories.code_verification import CodeVerificationRepository
from app.services.interfaces.clients.aws.email import AEmailClient
from app.api.interfaces.services.code_verification import ACodeVerificationService
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


@pytest.fixture(scope="session")
def uow(session_factory: async_sessionmaker[AsyncSession]) -> AUnitOfWork:
    return Uow(session_factory)


@pytest.fixture
def auth_service(uow: AUnitOfWork) -> AAuthService:
    return AuthService(uow)


@pytest.fixture
def code_verification_repo(session: AsyncSession) -> ACodeVerificationRepository:
    return CodeVerificationRepository()


@pytest.fixture
def code_verification_service(code_verification_repo) -> ACodeVerificationService:
    return CodeVerificationService(code_verification_repo)


@pytest.fixture
def created_code(email: EmailStr, code) -> int:
    return (
        code
        if bool(redis_db.set(email, code, ex=Constants.expiration_time_for_code))
        else 0
    )


@pytest.fixture
def email_service(email_client: AEmailClient) -> AEmailService:
    return EmailService(email_client)

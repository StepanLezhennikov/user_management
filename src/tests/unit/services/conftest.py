from datetime import datetime, timezone, timedelta

import jwt
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.schemas.user import UserSignIn
from app.services.services.jwt import JwtService
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


@pytest.fixture(scope="function")
async def auth_service(uow: AUnitOfWork) -> AAuthService:
    return AuthService(uow)


@pytest.fixture
async def code_verification_repo(session: AsyncSession) -> ACodeVerificationRepository:
    return CodeVerificationRepository()


@pytest.fixture(scope="function")
async def code_verification_service(code_verification_repo) -> ACodeVerificationService:
    return CodeVerificationService(code_verification_repo)


@pytest.fixture
def email_service(email_client: AEmailClient) -> AEmailService:
    return EmailService(email_client)


@pytest.fixture
def user_sign_in() -> UserSignIn:
    return UserSignIn(email="test@example.com", password="test_password")


@pytest.fixture
def created_access_token(jwt_service: JwtService, user_sign_in: UserSignIn) -> str:
    return jwt_service.create_access_token(user_sign_in.model_dump())


@pytest.fixture
def expired_access_token(created_access_token: str, settings: Settings) -> str:
    payload = jwt.decode(
        created_access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        options={"verify_exp": False},
    )

    payload["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)

    expired_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return expired_token


@pytest.fixture
def invalid_access_token(created_access_token: str) -> str:
    return created_access_token[:-5] + "abcde"

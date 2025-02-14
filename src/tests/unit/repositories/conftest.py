import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import redis_db
from app.core.config import Constants
from app.infra.repositories.user import UserRepository
from app.infra.repositories.code_verification import CodeVerificationRepository
from app.services.interfaces.repositories.user_repository import AUserRepository
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


@pytest.fixture
async def user_repo(session: AsyncSession) -> AUserRepository:
    return UserRepository(session)


@pytest.fixture
async def code_verification_repo(session: AsyncSession) -> ACodeVerificationRepository:
    return CodeVerificationRepository()


@pytest.fixture
def created_code(email: EmailStr, code) -> int:
    return (
        code
        if bool(redis_db.set(email, code, ex=Constants.expiration_time_for_code))
        else 0
    )

import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import redis_db
from app.core.config import Constants
from app.infra.repositories.role import RoleRepository
from app.infra.repositories.permission import PermissionRepository
from app.infra.repositories.code_verification import CodeVerificationRepository
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


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


@pytest.fixture
async def role_repo(session: AsyncSession) -> RoleRepository:
    return RoleRepository(session)


@pytest.fixture
async def permission_repo(session: AsyncSession) -> PermissionRepository:
    return PermissionRepository(session)

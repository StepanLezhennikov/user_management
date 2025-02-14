import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.repositories.user import UserRepository


@pytest.fixture
async def user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)

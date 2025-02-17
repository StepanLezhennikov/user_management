import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate
from app.api.exceptions.auth_service import UserNotFound
from app.api.interfaces.services.auth import AAuthService


async def test_create_user(auth_service: AAuthService, user_create: UserCreate) -> None:
    user = await auth_service.create(user_create)
    assert user.email == user_create.email
    assert user.username == user_create.username
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


async def test_check_user_exists(
    auth_service: AAuthService, created_user: User, session: AsyncSession
) -> None:
    assert await auth_service.check_user_exists(created_user.email)


async def test_check_user_not_exists(
    auth_service: AAuthService, user_create: UserCreate, session: AsyncSession
) -> None:
    with pytest.raises(UserNotFound):
        await auth_service.check_user_exists(user_create.email)

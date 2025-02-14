import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate
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
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.check_user_exists(created_user.email)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User is already registered"


async def test_check_user_not_exists(
    auth_service: AAuthService, user_create: UserCreate, session: AsyncSession
) -> None:
    result = await auth_service.check_user_exists(user_create.email)
    assert result is False

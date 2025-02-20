import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate, UserSignIn
from app.api.exceptions.auth_service import UserNotFoundError
from app.api.interfaces.services.auth import AAuthService
from app.services.services.password_security import PasswordSecurityService


async def test_create_user(auth_service: AAuthService, user_create: UserCreate) -> None:
    user = await auth_service.create(user_create)
    assert user.email == user_create.email
    assert user.username == user_create.username
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


async def test_check_user_exists(
    auth_service: AAuthService, created_user: User, session: AsyncSession
) -> None:
    assert await auth_service.check_user_exists(email=str(created_user.email))


async def test_check_user_not_exists(
    auth_service: AAuthService, user_create: UserCreate, session: AsyncSession
) -> None:
    with pytest.raises(UserNotFoundError):
        await auth_service.check_user_exists(email=str(user_create.email))


async def test_get_user_id(
    auth_service: AAuthService,
    created_user: User,
) -> None:
    user_id = await auth_service.get_user_id(email=str(created_user.email))
    assert user_id == created_user.id


async def test_get_user_id_not_found(
    auth_service: AAuthService,
    user_create: UserCreate,
) -> None:
    with pytest.raises(UserNotFoundError):
        await auth_service.get_user_id(email=str(user_create.email))


async def test_reset_password(
    auth_service: AAuthService,
    created_user: User,
    new_hashed_password: str,
    new_password: str,
    session: AsyncSession,
    password_security_service: PasswordSecurityService,
) -> None:
    assert await auth_service.reset_password(created_user.id, new_hashed_password)

    assert not await password_security_service.verify_password(
        UserSignIn(email=created_user.email, password=new_password)
    )

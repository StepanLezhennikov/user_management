import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleCreate
from app.schemas.user import User, UserCreate, UserSignIn
from app.api.exceptions.user_service import UserNotFoundError
from app.api.interfaces.services.user import AUserService
from app.services.services.password_security import PasswordSecurityService


async def test_create_user(
    user_service: AUserService, user_create: UserCreate, created_role_admin: RoleCreate
) -> None:
    user = await user_service.create(user_create)
    assert user.email == user_create.email
    assert user.username == user_create.username
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name
    assert user.roles[0].role == created_role_admin.role


async def test_check_user_exists(
    user_service: AUserService, created_user: User, session: AsyncSession
) -> None:
    assert await user_service.check_user_exists(email=str(created_user.email))


async def test_check_user_not_exists(
    user_service: AUserService, user_create: UserCreate, session: AsyncSession
) -> None:
    with pytest.raises(UserNotFoundError):
        await user_service.check_user_exists(email=str(user_create.email))


async def test_get_user_id(
    user_service: AUserService,
    created_user: User,
) -> None:
    user = await user_service.get(email=str(created_user.email))
    assert user.id == created_user.id


async def test_get_user_id_not_found(
    user_service: AUserService,
    user_create: UserCreate,
) -> None:
    with pytest.raises(UserNotFoundError):
        await user_service.get(email=str(user_create.email))


async def test_reset_password(
    user_service: AUserService,
    created_user: User,
    new_hashed_password: str,
    new_password: str,
    session: AsyncSession,
    password_security_service: PasswordSecurityService,
) -> None:
    assert await user_service.reset_password(created_user.id, new_hashed_password)

    assert not await password_security_service.verify_password(
        UserSignIn(email=created_user.email, password=new_password)
    )

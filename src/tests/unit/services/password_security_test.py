import pytest

from app.schemas.user import User, UserSignIn
from app.api.exceptions.auth_service import UserNotFoundError
from app.services.services.password_security import PasswordSecurityService
from app.api.exceptions.password_security_service import IncorrectPasswordError


async def test_verify_password(
    created_user: User,
    user_sign_in: UserSignIn,
    password_security_service: PasswordSecurityService,
) -> None:
    assert not await password_security_service.verify_password(user_sign_in)


async def test_verify_password_user_not_found(
    user_sign_in: UserSignIn,
    password_security_service: PasswordSecurityService,
) -> None:
    with pytest.raises(UserNotFoundError):
        await password_security_service.verify_password(user_sign_in)


async def test_verify_password_incorrect_password(
    created_user: User,
    user_sign_in: UserSignIn,
    password_security_service: PasswordSecurityService,
) -> None:
    user_sign_in.password = "incorrect password"
    with pytest.raises(IncorrectPasswordError):
        assert not await password_security_service.verify_password(user_sign_in)


async def test_hash_password(
    new_password: str,
    password_security_service: PasswordSecurityService,
) -> None:
    new_password_hash = password_security_service.hash_password(new_password)
    assert new_password_hash != new_password

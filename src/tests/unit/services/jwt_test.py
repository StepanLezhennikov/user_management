import pytest

from app.schemas.user import User, UserSignIn
from app.services.services.jwt import JwtService
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)
from app.api.exceptions.auth_service import UserNotFoundError


async def test_create_access_token(
    jwt_service: JwtService, user_sign_in: UserSignIn
) -> None:
    token = jwt_service.create_access_token(user_sign_in.model_dump())
    assert isinstance(token, str)


async def test_create_refresh_token(
    jwt_service: JwtService, user_sign_in: UserSignIn
) -> None:
    token = jwt_service.create_refresh_token(user_sign_in.model_dump())
    assert isinstance(token, str)


async def test_decode_token(
    jwt_service: JwtService, created_access_token: str, user_sign_in: UserSignIn
) -> None:
    decoded_token = jwt_service.decode_token(created_access_token)
    assert decoded_token["email"] == user_sign_in.email


async def test_decode_token_expired(
    jwt_service: JwtService, expired_access_token: str, user_sign_in: UserSignIn
) -> None:
    with pytest.raises(ExpiredSignatureException):
        jwt_service.decode_token(expired_access_token)


async def test_decode_token_invalid_signature(
    jwt_service: JwtService, invalid_access_token: str, user_sign_in: UserSignIn
) -> None:
    with pytest.raises(InvalidSignatureException):
        jwt_service.decode_token(invalid_access_token)


async def test_get_current_user(
    jwt_service: JwtService,
    created_access_token: str,
    user_sign_in: UserSignIn,
    created_user: User,
) -> None:
    user = await jwt_service.get_current_user(created_access_token)
    assert user.email == user_sign_in.email
    assert user.hashed_password == user_sign_in.password


async def test_get_current_user_not_found(
    jwt_service: JwtService, created_access_token: str, user_sign_in: UserSignIn
) -> None:
    with pytest.raises(UserNotFoundError):
        await jwt_service.get_current_user(created_access_token)

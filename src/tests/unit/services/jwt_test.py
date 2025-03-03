import pytest

from app.schemas.user import UserForToken
from app.services.services.jwt import JwtService
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)


async def test_create_access_token(
    jwt_service: JwtService, user_for_token: UserForToken
) -> None:
    token = jwt_service.create_access_token(user_for_token.model_dump())
    assert isinstance(token, str)


async def test_create_refresh_token(
    jwt_service: JwtService, user_for_token: UserForToken
) -> None:
    token = jwt_service.create_refresh_token(user_for_token.model_dump())
    assert isinstance(token, str)


async def test_decode_token(
    jwt_service: JwtService, created_access_token: str, user_for_token: UserForToken
) -> None:
    decoded_token = jwt_service.decode_token(created_access_token)
    assert decoded_token["id"] == user_for_token.id
    assert decoded_token["permissions"] == user_for_token.permissions


async def test_decode_token_expired(
    jwt_service: JwtService, expired_access_token: str
) -> None:
    with pytest.raises(ExpiredSignatureException):
        jwt_service.decode_token(expired_access_token)


async def test_decode_token_invalid_signature(
    jwt_service: JwtService, invalid_access_token: str
) -> None:
    with pytest.raises(InvalidSignatureException):
        jwt_service.decode_token(invalid_access_token)

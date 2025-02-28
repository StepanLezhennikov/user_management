from typing import Annotated
from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Depends, Security
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dependency_injector.wiring import Provide, inject

from app.core.config import settings
from app.schemas.user import UserAuthenticated
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)
from app.api.interfaces.services.jwt import AJwtService
from app.services.interfaces.repositories.user_repository import AUserRepository

http_bearer = HTTPBearer()


class JwtService(AJwtService):

    def __init__(self, user_repository: AUserRepository) -> None:
        self.user_repository = user_repository

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_reset_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.RESET_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except ExpiredSignatureError:
            raise ExpiredSignatureException()
        except InvalidSignatureError:
            raise InvalidSignatureException()


@inject
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(http_bearer)],
    jwt_service: AJwtService = Depends(Provide["jwt_service"]),
) -> UserAuthenticated:
    decoded_token = jwt_service.decode_token(token=credentials.credentials)

    current_user = UserAuthenticated(
        id=decoded_token["id"], permissions=decoded_token["permissions"]
    )
    return current_user

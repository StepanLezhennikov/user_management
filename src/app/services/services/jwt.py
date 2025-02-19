from datetime import datetime, timezone, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.schemas.user import User, UserSignIn
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)
from app.api.exceptions.auth_service import UserNotFoundError
from app.api.interfaces.services.jwt import AJwtService
from app.services.interfaces.repositories.user_repository import AUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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

    def decode_token(self, token: str) -> UserSignIn:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return UserSignIn(email=payload["email"], password=payload["password"])
        except ExpiredSignatureError:
            raise ExpiredSignatureException()
        except InvalidSignatureError:
            raise InvalidSignatureException()

    async def get_current_user(self, token: str) -> User:
        decoded_token = self.decode_token(token)
        user = await self.user_repository.get(email=decoded_token.email)
        if not user:
            raise UserNotFoundError()
        return user

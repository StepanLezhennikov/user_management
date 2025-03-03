from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.jwt import Token
from app.schemas.user import User, UserCreate, UserSignIn, UserForToken
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)
from app.api.exceptions.user_service import (
    InvalidRoleError,
    UserNotFoundError,
    UserIsAlreadyRegisteredError,
)
from app.api.interfaces.services.jwt import AJwtService
from app.api.interfaces.services.user import AUserService
from app.services.services.password_security import PasswordSecurityService
from app.api.exceptions.password_security_service import IncorrectPasswordError

logger = getLogger(__name__)

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
@inject
async def sign_up(
    user_data: UserCreate,
    user_service: AUserService = Depends(Provide["user_service"]),
    password_security_service: PasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
) -> User:
    user_data.password = password_security_service.hash_password(user_data.password)
    try:
        new_user = await user_service.create(user_data)
    except UserIsAlreadyRegisteredError:
        raise HTTPException(status_code=409, detail="User is already registered")
    except InvalidRoleError:
        raise HTTPException(status_code=403, detail="Invalid role")

    return new_user


@router.post("/token")
@inject
async def get_tokens(
    user_data: UserSignIn,
    user_service: AUserService = Depends(Provide["user_service"]),
    jwt_service: AJwtService = Depends(Provide["jwt_service"]),
    password_security_service: PasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
) -> Token:
    try:
        await password_security_service.verify_password(user_data)
        permissions = await user_service.get_user_permissions(email=user_data.email)
        user = await user_service.get(email=user_data.email)
    except (IncorrectPasswordError, UserNotFoundError):
        raise HTTPException(status_code=403, detail="Invalid password or email")

    user_for_token = UserForToken(id=user.id, permissions=permissions)

    access_token = jwt_service.create_access_token(user_for_token.model_dump())
    refresh_token = jwt_service.create_refresh_token(user_for_token.model_dump())
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
@inject
async def refresh_access_token(
    refresh_token: str, jwt_service: AJwtService = Depends(Provide["jwt_service"])
) -> Token:
    try:
        payload = jwt_service.decode_token(refresh_token)
    except ExpiredSignatureException:
        raise HTTPException(status_code=401, detail="Expired refresh token")
    except InvalidSignatureException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = jwt_service.create_access_token(payload)
    new_refresh_token = jwt_service.create_refresh_token(payload)

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)

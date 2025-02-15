from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from dependency_injector.wiring import Provide, inject

from app.schemas.user import UserCreate, UserSignIn
from app.api.exceptions.auth_service import UserNotFound, UserIsRegistered
from app.api.interfaces.services.jwt import AJwtService
from app.api.interfaces.services.auth import AAuthService
from app.api.exceptions.password_security_service import IncorrectPassword
from app.api.interfaces.services.password_security import APasswordSecurityService

logger = getLogger(__name__)

router = APIRouter()


@router.post("/users")
@inject
async def sign_up(
    user_data: UserCreate,
    auth_service: AAuthService = Depends(Provide["auth_service"]),
    password_security_service: APasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
) -> UserCreate:
    try:
        await auth_service.check_user_exists(user_data.email)
    except UserIsRegistered:
        raise HTTPException(status_code=409, detail="User is already registered")
    user_data.password = password_security_service.hash_password(user_data.password)
    new_user = await auth_service.create(user_data)
    return new_user


@router.post("/sign_in")
@inject
async def sign_in(
    user_data: UserSignIn,
    auth_service: AAuthService = Depends(Provide["auth_service"]),
    password_security_service: APasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
    jwt_service: AJwtService = Depends(Provide["jwt_service"]),
) -> bool:
    try:
        hashed_pass = await auth_service.get_user_hashed_password(user_data.email)
        password_security_service.verify_password(user_data.password, hashed_pass)
    except (UserNotFound, IncorrectPassword):
        raise HTTPException(status_code=404, detail="User not found")
    # TODO логика с jwt
    return True

from logging import getLogger

from fastapi import Depends, APIRouter
from dependency_injector.wiring import Provide, inject

from app.schemas.user import UserCreate, UserSignIn
from app.api.interfaces.services.jwt import AJwtService
from app.api.interfaces.services.auth import AAuthService
from app.api.interfaces.services.password_security import APasswordSecurityService

logger = getLogger(__name__)

router = APIRouter()


@router.post("/sign_up")
@inject
async def sign_up(
    user_data: UserCreate,
    auth_service: AAuthService = Depends(Provide["auth_service"]),
    password_security_service: APasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
) -> UserCreate:
    await auth_service.check_user_exists(user_data.email)
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
    hashed_pass = await auth_service.get_user_hashed_password(user_data.email)
    print(hashed_pass)
    password_security_service.verify_password(user_data.password, hashed_pass)
    # TODO логика с jwt
    return True

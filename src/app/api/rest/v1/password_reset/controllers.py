from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from pydantic import EmailStr
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.response import CustomResponse
from app.api.exceptions.jwt_service import (
    ExpiredSignatureException,
    InvalidSignatureException,
)
from app.api.exceptions.user_service import UserNotFoundError
from app.api.interfaces.services.jwt import AJwtService
from app.api.interfaces.services.user import AUserService
from app.api.interfaces.services.email import AEmailService
from app.api.interfaces.services.password_security import APasswordSecurityService

logger = getLogger(__name__)

router = APIRouter()


@router.post("/request", status_code=status.HTTP_201_CREATED)
@inject
async def request_password_reset(
    email: EmailStr,
    email_service: AEmailService = Depends(Provide["email_service"]),
    user_service: AUserService = Depends(Provide["user_service"]),
    jwt_service: AJwtService = Depends(Provide["jwt_service"]),
) -> CustomResponse:
    try:
        user = await user_service.get(email=str(email))
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = jwt_service.create_reset_token({"user_id": user.id})
    await email_service.send_password_reset_link(email, reset_token)

    return CustomResponse(message="Password reset link sent successfully")


@router.post("/")
@inject
async def password_reset(
    token: str,
    new_password: str,
    user_service: AUserService = Depends(Provide["user_service"]),
    jwt_service: AJwtService = Depends(Provide["jwt_service"]),
    password_security_service: APasswordSecurityService = Depends(
        Provide["password_security_service"]
    ),
) -> CustomResponse:
    try:
        payload = jwt_service.decode_token(token)
        hashed_password = password_security_service.hash_password(new_password)
        await user_service.reset_password(int(payload["user_id"]), hashed_password)

    except ExpiredSignatureException:
        raise HTTPException(status_code=401, detail="Expired refresh token")

    except InvalidSignatureException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    return CustomResponse(message="Password reset successfully")

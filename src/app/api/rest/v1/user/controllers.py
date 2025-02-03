from logging import getLogger

from fastapi import Depends, APIRouter
from dependency_injector.wiring import Provide, inject

from app.api.interfaces.services.email_service import AEmailService
from app.schemas.user import UserCreate
from app.api.interfaces.services.auth_service import AAuthService

logger = getLogger(__name__)

router = APIRouter()


@router.post("")
@inject
async def sign_up(
    user_data: UserCreate,
    auth_service: AAuthService = Depends(Provide["auth_service"]),
    email_service: AEmailService = Depends(Provide["email_service"]),
):
    logger.info("Вызов sign_up ручки")
    await email_service.send_message(
        email=user_data.email,
        subject="Подтверждение почты",
        message="Подтвердите почту",
    )
    # Подтверждение почты
    return await auth_service.register(user_data)  # Создание пользователя


# @router.post("/token")
# async def

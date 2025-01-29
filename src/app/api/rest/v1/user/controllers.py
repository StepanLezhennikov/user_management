from logging import getLogger

from fastapi import Depends, APIRouter
from dependency_injector.wiring import Provide, inject

from src.app.containers import Container
from src.app.schemas.user import UserCreate
from src.app.services.auth import AuthService

logger = getLogger(__name__)

router = APIRouter()


@router.post("")
@inject
async def sign_up(
    user_data: UserCreate,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    logger.info("Вызов sign_up ручки")
    return await auth_service.register(user_data)

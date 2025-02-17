from logging import getLogger

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate
from app.api.exceptions.auth_service import (
    UserNotFoundError,
    UserIsAlreadyRegisteredError,
)
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.auth import AAuthService

logger = getLogger(__name__)


class AuthService(AAuthService):
    def __init__(self, uow: AUnitOfWork):
        logger.info("Вызов AuthService __init__")
        self._uow = uow

    async def create(self, user_data: UserCreate) -> UserCreate:
        logger.info("Вызов AuthService register")
        async with self._uow as uow:
            try:
                new_user = await uow.users.create(user_data)
                await uow.commit()
                return new_user
            except IntegrityError:
                raise UserIsAlreadyRegisteredError()

    async def check_user_exists(self, email: EmailStr) -> bool:
        async with self._uow as uow:
            user = await uow.users.get(email=email)
            if not user:
                raise UserNotFoundError()
            return True

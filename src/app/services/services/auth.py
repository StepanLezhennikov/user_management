from logging import getLogger

from app.schemas.user import UserCreate
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
            new_user = await uow.users.create(user_data)
            await uow.commit()
            return new_user

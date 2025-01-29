from logging import getLogger

from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.repositories.uow.impl_uow import Uow
from app.repositories.abs_repositories.user_repository import AUserRepository

logger = getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: AUserRepository):
        logger.info("Вызов AuthService __init__")
        self._user_repository = user_repository

    async def register(self, user_data: UserCreate) -> UserCreate:
        logger.info("Вызов AuthService register")
        async with Uow(SessionLocal) as uow:
            # Добавить сюда логику проверки
            new_user = await uow.users.create(user_data)
            await uow.commit()
            return new_user

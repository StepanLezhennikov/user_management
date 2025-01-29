from logging import getLogger

from app.schemas.user import User, UserCreate
from app.repositories.abs_repositories.user_repository import AUserRepository

logger = getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: AUserRepository):
        logger.info("Вызов AuthService __init__")
        self._user_repository = user_repository

    async def register(self, user: UserCreate) -> User:
        logger.info("Вызов AuthService register")
        # Добавить сюда логику аутентификации
        new_user = await self._user_repository.create(user)
        return new_user

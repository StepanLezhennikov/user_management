from logging import getLogger

from fastapi import HTTPException
from pydantic import EmailStr

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

    async def check_user_exists(self, email: EmailStr) -> bool:
        async with self._uow as uow:
            user = await uow.users.get(email=email)
            if user:
                raise HTTPException(
                    status_code=409, detail="User is already registered"
                )
            return False

    async def get_user_hashed_password(self, email: EmailStr) -> str:
        async with self._uow as uow:
            user = await uow.users.get(email=email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user.hashed_password

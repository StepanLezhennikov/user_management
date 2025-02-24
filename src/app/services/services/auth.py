from logging import getLogger

from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate
from app.api.exceptions.auth_service import (
    InvalidRoleError,
    UserNotFoundError,
    UserIsAlreadyRegisteredError,
)
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.auth import AAuthService

logger = getLogger(__name__)


class AuthService(AAuthService):
    def __init__(self, uow: AUnitOfWork):
        self._uow = uow

    async def create(self, user_data: UserCreate) -> UserCreate:
        async with self._uow as uow:
            try:
                roles = await uow.roles.filter(user_data.roles)
                roles_ids = [role.id for role in roles]
                if user_data.roles and not roles_ids:
                    raise InvalidRoleError()
                new_user = await uow.users.create(user_data, roles_ids)
                await uow.commit()
                return new_user
            except IntegrityError:
                raise UserIsAlreadyRegisteredError()

    async def check_user_exists(self, **filters) -> int:
        async with self._uow as uow:
            user = await uow.users.get(**filters)
            if not user:
                raise UserNotFoundError()
            return True

    async def get_user_id(self, email: str) -> int:
        async with self._uow as uow:
            user = await uow.users.get(email=email)
            if not user:
                raise UserNotFoundError()
            return user.id

    async def reset_password(self, user_id: int, hashed_password: str) -> bool:
        await self.check_user_exists(id=user_id)
        async with self._uow as uow:
            await uow.users.update_password(
                user_id=user_id, new_hashed_password=hashed_password
            )
        return True

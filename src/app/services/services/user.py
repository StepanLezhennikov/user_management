from logging import getLogger

from sqlalchemy.exc import IntegrityError

from app.schemas.user import User, UserCreate, UserUpdate, DeletedUser
from app.schemas.sort_filter import SortBy, SortOrder
from app.api.exceptions.user_service import (
    InvalidRoleError,
    UserNotFoundError,
    UserIsAlreadyRegisteredError,
)
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.user import AUserService

logger = getLogger(__name__)


class UserService(AUserService):
    def __init__(self, uow: AUnitOfWork):
        self._uow = uow

    async def create(self, user_data: UserCreate) -> User:
        async with self._uow as uow:
            try:
                roles = await uow.roles.filter(user_data.roles)
                roles_ids = [role.id for role in roles]

                if user_data.roles and not roles_ids:
                    raise InvalidRoleError()

                new_user = await uow.users.create(user_data, roles_ids)
                await uow.commit()
                return User.model_validate(new_user)

            except IntegrityError:
                raise UserIsAlreadyRegisteredError()

    async def check_user_exists(self, **filters) -> int:
        async with self._uow as uow:
            user = await uow.users.get(**filters)
            if not user:
                raise UserNotFoundError()
            return True

    async def get(self, **filters) -> User:
        async with self._uow as uow:
            user = await uow.users.get(**filters)
            if not user:
                raise UserNotFoundError()
            return user

    async def get_all(
        self,
        sort_by: SortBy,
        sort_order: SortOrder,
        limit: int = 10,
        offset: int = 0,
        **filters
    ) -> list[User]:
        async with self._uow as uow:
            users = await uow.users.get_all(
                sort_by, sort_order, limit, offset, **filters
            )
            if not users:
                raise UserNotFoundError()
            return users

    async def get_permissions(self, email: str) -> list[str]:
        async with self._uow as uow:
            permissions = await uow.users.get_permissions(email)
            if permissions is None:
                raise UserNotFoundError()

        return permissions

    async def update(self, user_id: int, user_update: UserUpdate) -> User:
        async with self._uow as uow:
            updated_user = await uow.users.update(user_id, **user_update.model_dump())
            return User.model_validate(updated_user)

    async def reset_password(self, user_id: int, hashed_password: str) -> bool:
        await self.check_user_exists(id=user_id)
        async with self._uow as uow:
            await uow.users.update_password(
                user_id=user_id, new_hashed_password=hashed_password
            )
        return True

    async def delete(self, user_id: int) -> DeletedUser:
        async with self._uow as uow:
            deleted_user = await uow.users.delete(user_id)
            if deleted_user is None:
                raise UserNotFoundError()
            return deleted_user

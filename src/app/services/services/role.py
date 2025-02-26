from sqlalchemy.exc import IntegrityError

from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.api.exceptions.role_service import RoleNotFoundError, RoleAlreadyExistsError
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.interfaces.services.role import ARoleService


class RoleService(ARoleService):
    def __init__(self, uow: AUnitOfWork):
        self._uow = uow

    async def create(self, role_create: RoleCreate) -> RoleCreate:
        try:
            async with self._uow as uow:
                await uow.roles.create(role_create)
                await uow.commit()
        except IntegrityError:
            raise RoleAlreadyExistsError()

        return role_create

    async def get(self, **filters) -> list[Role]:
        filters = {k: v for k, v in filters.items() if v is not None}
        async with self._uow as uow:
            roles = await uow.roles.get(**filters)

            if not roles:
                raise RoleNotFoundError()

        return roles

    async def update(self, role_id: int, role_update: RoleUpdate) -> Role:
        values = role_update.model_dump(exclude_unset=True)
        async with self._uow as uow:
            role = await uow.roles.update(role_id, **values)

            if not role:
                raise RoleNotFoundError()

        return Role.model_validate(role)

    async def delete(self, role_id: int) -> Role:
        async with self._uow as uow:
            role = await uow.roles.delete(role_id)

            if not role:
                raise RoleNotFoundError()

        return role

from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.exceptions.permission_service import PermissionsNotFoundError
from app.api.interfaces.services.permission import APermissionService


class PermissionService(APermissionService):
    def __init__(self, uow: AUnitOfWork):
        self._uow = uow

    async def create(self, permission_create: PermissionCreate) -> PermissionCreate:
        async with self._uow as uow:
            await uow.permissions.create(permission_create)

        return permission_create

    async def get(self, **filters) -> list[Permission]:
        filters = {k: v for k, v in filters.items() if v is not None}
        async with self._uow as uow:
            permissions = await uow.permissions.get(**filters)

            if not permissions:
                raise PermissionsNotFoundError()

        return permissions

    async def update(
        self, permission_id: int, permission_update: PermissionUpdate
    ) -> Permission:
        values = permission_update.model_dump(exclude_unset=True)
        async with self._uow as uow:
            permission = await uow.permissions.update(permission_id, **values)

            if not permission:
                raise PermissionsNotFoundError()

        return Permission.model_validate(permission)

    async def delete(self, permission_id: int) -> Permission:
        async with self._uow as uow:
            permission = await uow.permissions.delete(permission_id)

            if not permission:
                raise PermissionsNotFoundError()

        return permission

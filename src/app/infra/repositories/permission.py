from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.permission import Permission, PermissionCreate
from app.api.exceptions.permission_service import PermissionAlreadyExistsError
from app.infra.repositories.models.user_model import Permission as PermissionModel
from app.services.interfaces.repositories.permission_repository import (
    APermissionRepository,
)


class PermissionRepository(APermissionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, permission: PermissionCreate) -> PermissionCreate:
        try:
            new_permission = PermissionModel(
                name=permission.name, description=permission.description
            )
            self._session.add(new_permission)
            await self._session.flush()

        except IntegrityError:
            raise PermissionAlreadyExistsError()

        return permission

    async def get(self, **filters) -> list[Permission] | None:
        query = select(PermissionModel).filter_by(**filters)
        result = await self._session.execute(query)
        raw_results = result.scalars().all()

        permissions = list(
            map(lambda perm: Permission.model_validate(perm), raw_results)
        )
        return permissions

    async def update(self, permission_id: int, **values) -> Permission | None:
        stmt = (
            update(PermissionModel)
            .where(PermissionModel.id == permission_id)
            .values(**values)
            .returning(PermissionModel)
        )
        result = await self._session.execute(stmt)

        perm = result.scalar_one_or_none()

        return Permission.model_validate(perm) if perm else None

    async def delete(self, permission_id: int) -> Permission | None:
        query = (
            delete(PermissionModel)
            .where(PermissionModel.id == permission_id)
            .returning(PermissionModel)
        )
        result = await self._session.execute(query)
        perm = result.scalar_one_or_none()

        return Permission.model_validate(perm) if perm else None

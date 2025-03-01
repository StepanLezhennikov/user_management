from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import Role, RoleCreate
from app.api.exceptions.role_service import RoleAlreadyExistsError
from app.infra.repositories.models.user_model import Role as RoleModel
from app.infra.repositories.models.user_model import Permission as PermissionModel
from app.infra.repositories.models.user_model import user_role, role_permission
from app.services.interfaces.repositories.role_repository import ARoleRepository


class RoleRepository(ARoleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, role: RoleCreate) -> RoleCreate:
        new_role = RoleModel(role=role.role)

        if role.permissions_ids:
            query = select(PermissionModel).filter(
                PermissionModel.id.in_(role.permissions_ids)
            )
            result = await self._session.execute(query)
            permissions = result.scalars().all()
            new_role.permissions = permissions

        try:
            self._session.add(new_role)
            await self._session.flush()
        except IntegrityError:
            raise RoleAlreadyExistsError()

        return role

    async def get(self, **filters) -> list[Role] | None:
        query = select(RoleModel).filter_by(**filters)
        result = await self._session.execute(query)
        raw_results = result.scalars().all()

        permissions = list(map(lambda perm: Role.model_validate(perm), raw_results))
        return permissions

    async def update(self, role_id: int, **values) -> Role | None:
        stmt = (
            update(RoleModel)
            .where(RoleModel.id == role_id)
            .values(**values)
            .returning(RoleModel)
        )
        result = await self._session.execute(stmt)

        role = result.scalar_one_or_none()

        return Role.model_validate(role) if role else None

    async def delete(self, role_id: int) -> Role | None:
        delete_role_permission_query = delete(role_permission).where(
            role_permission.c.role_id == role_id
        )
        await self._session.execute(delete_role_permission_query)

        delete_user_role_query = delete(user_role).where(user_role.c.role_id == role_id)
        await self._session.execute(delete_user_role_query)

        query = delete(RoleModel).where(RoleModel.id == role_id).returning(RoleModel)
        result = await self._session.execute(query)
        role = result.scalar_one_or_none()

        return Role.model_validate(role) if role else None

    async def filter(self, roles: list[str]) -> list[Role] | None:
        query = select(RoleModel).where(RoleModel.role.in_(roles))
        result = await self._session.execute(query)
        roles = result.scalars().all()
        return list(map(Role.model_validate, roles))

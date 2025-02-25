from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import Role, RoleCreate
from app.infra.repositories.models.user_model import Role as RoleModel
from app.services.interfaces.repositories.role_repository import ARoleRepository


class RoleRepository(ARoleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, role: RoleCreate) -> RoleCreate:
        new_role = RoleModel(role=role.role)
        self._session.add(new_role)
        return role

    async def get(self, **filters) -> Role | None:
        query = select(RoleModel).filter_by(**filters)
        result = await self._session.execute(query)
        role = result.scalar_one_or_none()
        return Role.model_validate(role) if role else None

    async def update(self, role: Role, **values) -> Role:
        pass

    async def delete(self, role: Role) -> Role:
        pass

    async def filter(self, roles: list[str]) -> list[Role] | None:
        query = select(RoleModel).where(RoleModel.role.in_(roles))
        result = await self._session.execute(query)
        roles = result.scalars().all()
        return list(map(Role.model_validate, roles))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import Role, RoleCreate
from app.infra.repositories.role import RoleRepository
from app.infra.repositories.models.user_model import Role as RoleModel


async def test_create_role(
    role_repo: RoleRepository,
    role_create: RoleCreate,
    session: AsyncSession,
) -> None:
    await role_repo.create(role_create)

    query = select(RoleModel).filter_by(role=role_create.role)
    result = await session.execute(query)
    role = result.scalar_one_or_none()

    assert role.role == role_create.role


async def test_get_role(
    role_repo: RoleRepository,
    created_role: Role,
) -> None:
    role = await role_repo.get(role=created_role.role)
    assert role.role == created_role.role


async def test_get_role_not_found(
    role_repo: RoleRepository,
    role_create: RoleCreate,
) -> None:
    role = await role_repo.get(role=role_create.role)
    assert role is None

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.infra.repositories.role import RoleRepository
from app.infra.repositories.models.user_model import Role as RoleModel
from app.infra.repositories.models.user_model import RolePermission


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
    created_role_admin: Role,
) -> None:
    role = await role_repo.get(role=created_role_admin.role)
    assert role[0].role == created_role_admin.role


async def test_get_role_not_found(
    role_repo: RoleRepository,
    role_create: RoleCreate,
) -> None:
    role = await role_repo.get(role=role_create.role)
    assert not role


async def test_update_role(
    role_repo: RoleRepository,
    created_role_admin: RoleCreate,
    role_update: RoleUpdate,
) -> None:
    role = await role_repo.update(1, **(role_update.model_dump()))

    assert role_update.role == role.role


async def test_update_role_not_found(
    role_repo: RoleRepository,
    role_create: RoleCreate,
    role_update: RoleUpdate,
) -> None:
    role = await role_repo.update(1, **(role_update.model_dump()))

    assert not role


async def test_delete_role(
    role_repo: RoleRepository,
    created_role_admin: RoleCreate,
    session: AsyncSession,
) -> None:
    deleted_role = await role_repo.delete(1)

    assert deleted_role.role == created_role_admin.role

    query = select(RoleModel).filter_by(role=created_role_admin.role)
    result = await session.execute(query)
    role = result.scalar_one_or_none()

    delete_permissions_query = select(RolePermission).where(
        RolePermission.c.role_id == 1
    )
    result = await session.execute(delete_permissions_query)

    assert result.scalar_one_or_none() is None

    assert role is None


async def test_delete_role_not_found(
    role_repo: RoleRepository,
    role_create: RoleCreate,
) -> None:
    deleted_role = await role_repo.delete(1)

    assert not deleted_role

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.infra.repositories.permission import PermissionRepository
from app.infra.repositories.models.user_model import Permission as PermissionModel


async def test_create_permission(
    permission_repo: PermissionRepository,
    permission_create: PermissionCreate,
    session: AsyncSession,
) -> None:
    await permission_repo.create(permission_create)

    query = select(PermissionModel).filter_by(name=permission_create.name)
    result = await session.execute(query)
    permission = result.scalar_one_or_none()

    assert permission.name == permission.name


async def test_get_permission(
    permission_repo: PermissionRepository,
    created_permission: PermissionCreate,
) -> None:
    perm = await permission_repo.get(name=created_permission.name)
    assert created_permission.name == perm[0].name


async def test_get_permission_not_found(
    permission_repo: PermissionRepository,
    permission_create: PermissionCreate,
) -> None:
    perm = await permission_repo.get(name=permission_create.name)
    assert not perm


async def test_update_permission(
    permission_repo: PermissionRepository,
    created_permission: PermissionCreate,
    permission_update: PermissionUpdate,
) -> None:
    perm = await permission_repo.update(1, **(permission_update.model_dump()))

    assert permission_update.name == perm.name
    assert permission_update.description == perm.description


async def test_update_permission_not_found(
    permission_repo: PermissionRepository,
    permission_create: PermissionCreate,
    permission_update: PermissionUpdate,
) -> None:
    perm = await permission_repo.update(1, **(permission_create.model_dump()))

    assert not perm


async def test_delete_permission(
    permission_repo: PermissionRepository,
    created_permission: PermissionCreate,
    session: AsyncSession,
) -> None:
    deleted_perm = await permission_repo.delete(1)

    assert deleted_perm.name == created_permission.name

    query = select(PermissionModel).filter_by(name=created_permission.name)
    result = await session.execute(query)
    permission = result.scalar_one_or_none()

    assert permission is None


async def test_delete_permission_not_found(
    permission_repo: PermissionRepository,
    permission_create: PermissionCreate,
    session: AsyncSession,
) -> None:
    deleted_perm = await permission_repo.delete(1)

    assert not deleted_perm

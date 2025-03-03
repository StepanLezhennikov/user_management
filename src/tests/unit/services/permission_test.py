import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.services.services.permission import PermissionService
from app.api.exceptions.permission_service import PermissionsNotFoundError
from app.infra.repositories.models.user_model import Permission as PermissionModel


async def test_create_permission(
    permission_service: PermissionService,
    permission_create: PermissionCreate,
    session: AsyncSession,
) -> None:
    await permission_service.create(permission_create)

    query = select(PermissionModel).filter_by(name=permission_create.name)
    result = await session.execute(query)
    permission = result.scalar_one_or_none()

    assert permission.name == permission.name


async def test_get_permission(
    permission_service: PermissionService,
    created_permission: PermissionCreate,
) -> None:
    perm = await permission_service.get(name=created_permission.name)
    assert created_permission.name == perm[0].name


async def test_get_permission_not_found(
    permission_service: PermissionService,
    permission_create: PermissionCreate,
) -> None:
    with pytest.raises(PermissionsNotFoundError):
        await permission_service.get(name=permission_create.name)


async def test_update_permission(
    permission_service: PermissionService,
    created_permission: PermissionCreate,
    permission_update: PermissionUpdate,
) -> None:
    perm = await permission_service.update(1, permission_update)

    assert permission_update.name == perm.name
    assert permission_update.description == perm.description


async def test_update_permission_not_found(
    permission_service: PermissionService,
    permission_update: PermissionUpdate,
) -> None:
    with pytest.raises(PermissionsNotFoundError):
        await permission_service.update(1, permission_update)


async def test_delete_permission(
    permission_service: PermissionService,
    created_permission: PermissionCreate,
    session: AsyncSession,
) -> None:
    deleted_perm = await permission_service.delete(1)

    assert deleted_perm.name == created_permission.name

    query = select(PermissionModel).filter_by(name=created_permission.name)
    result = await session.execute(query)
    permission = result.scalar_one_or_none()

    assert permission is None


async def test_delete_permission_not_found(
    permission_service: PermissionService,
    permission_create: PermissionCreate,
    session: AsyncSession,
) -> None:
    with pytest.raises(PermissionsNotFoundError):
        await permission_service.delete(1)

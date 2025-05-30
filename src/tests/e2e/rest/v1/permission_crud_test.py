from httpx import AsyncClient
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.infra.repositories.models.user_model import Permission as PermissionModel


async def test_create_permission(
    http_client: AsyncClient,
    crud_permission_url: str,
    permission_create: PermissionCreate,
    session: AsyncSession,
    created_access_token: str,
) -> None:
    response = await http_client.post(
        crud_permission_url,
        json=permission_create.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED

    query = select(PermissionModel).where(
        PermissionModel.name == permission_create.name
    )
    result = await session.execute(query)
    perm = result.scalar_one_or_none()
    assert perm.name == permission_create.name
    assert perm.description == permission_create.description


async def test_create_permission_already_exists(
    http_client: AsyncClient,
    crud_permission_url: str,
    created_permission: Permission,
    permission_create: PermissionCreate,
    session: AsyncSession,
    created_access_token: str,
) -> None:
    response = await http_client.post(
        crud_permission_url,
        json=permission_create.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_get_permission(
    http_client: AsyncClient,
    crud_permission_url: str,
    created_permission: PermissionCreate,
    created_access_token: str,
) -> None:
    response = await http_client.get(
        crud_permission_url + "?name={}".format(created_permission.name),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )
    permissions = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert created_permission.name in permissions[0]["name"]


async def test_get_permission_not_found(
    http_client: AsyncClient,
    crud_permission_url: str,
    permission_create: PermissionCreate,
    created_access_token: str,
) -> None:
    response = await http_client.get(
        crud_permission_url + "?name={}".format(permission_create.name),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_permission(
    http_client: AsyncClient,
    crud_permission_url: str,
    created_permission: PermissionCreate,
    permission_update: PermissionUpdate,
    created_access_token: str,
) -> None:
    response = await http_client.put(
        crud_permission_url + "?permission_id=1",
        json=permission_update.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    updated_perm = response.json()
    assert updated_perm["name"] == permission_update.name


async def test_update_permission_not_found(
    http_client: AsyncClient,
    crud_permission_url: str,
    permission_update: PermissionUpdate,
    created_access_token: str,
) -> None:
    response = await http_client.put(
        crud_permission_url + "?permission_id=99999",
        json=permission_update.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_permission(
    http_client: AsyncClient,
    crud_permission_url: str,
    created_permission: PermissionCreate,
    permission_update: PermissionUpdate,
    session: AsyncSession,
    created_access_token: str,
) -> None:
    response = await http_client.delete(
        crud_permission_url + "?permission_id=1",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    query = select(PermissionModel).where(PermissionModel.id == 1)
    result = await session.execute(query)
    perm = result.scalar_one_or_none()

    assert perm is None


async def test_delete_permission_not_found(
    http_client: AsyncClient,
    crud_permission_url: str,
    permission_update: PermissionUpdate,
    session: AsyncSession,
    created_access_token: str,
) -> None:
    response = await http_client.delete(
        crud_permission_url + "?permission_id=99999",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

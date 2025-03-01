from httpx import AsyncClient
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleCreate, RoleUpdate
from app.infra.repositories.models.user_model import Role as RoleModel


async def test_create_role(
    http_client: AsyncClient,
    crud_role_url: str,
    role_create: RoleCreate,
    created_access_token: str,
    session: AsyncSession,
) -> None:
    response = await http_client.post(
        crud_role_url,
        json=role_create.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED

    query = select(RoleModel).where(RoleModel.role == role_create.role)

    result = await session.execute(query)
    role = result.scalar_one_or_none()
    assert role.role == role_create.role


async def test_create_role_already_exists(
    http_client: AsyncClient,
    crud_role_url: str,
    created_role: RoleCreate,
    created_access_token: str,
) -> None:
    response = await http_client.post(
        crud_role_url,
        json=created_role.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_get_role(
    http_client: AsyncClient,
    crud_role_url: str,
    created_role_admin: RoleCreate,
    created_access_token: str,
) -> None:
    response = await http_client.get(
        crud_role_url + "?role={}".format(created_role_admin.role),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )
    roles = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert created_role_admin.role in roles[0]["role"]


async def test_get_role_not_found(
    http_client: AsyncClient,
    crud_role_url: str,
    role_create: RoleCreate,
    created_access_token: str,
) -> None:
    response = await http_client.get(
        crud_role_url + "?role={}".format(role_create.role),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_role(
    http_client: AsyncClient,
    crud_role_url: str,
    created_role_admin: RoleCreate,
    role_update: RoleUpdate,
    created_access_token: str,
) -> None:
    response = await http_client.put(
        crud_role_url + "?role_id=1",
        json=role_update.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    updated_role = response.json()
    assert updated_role["role"] == role_update.role


async def test_update_role_not_found(
    http_client: AsyncClient,
    crud_role_url: str,
    role_update: RoleUpdate,
    created_access_token: str,
) -> None:
    response = await http_client.put(
        crud_role_url + "?role_id=99999",
        json=role_update.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_role(
    http_client: AsyncClient,
    crud_role_url: str,
    session: AsyncSession,
    created_access_token: str,
) -> None:
    response = await http_client.delete(
        crud_role_url + "?role_id=1",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    query = select(RoleModel).where(RoleModel.id == 1)
    result = await session.execute(query)
    role = result.scalar_one_or_none()

    assert role is None


async def test_delete_role_not_found(
    http_client: AsyncClient,
    crud_role_url: str,
    role_update: RoleUpdate,
    created_access_token: str,
) -> None:
    response = await http_client.delete(
        crud_role_url + "?role_id=99999",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

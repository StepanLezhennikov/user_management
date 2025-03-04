from httpx import AsyncClient
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate, UserUpdate
from app.infra.repositories.models.user_model import User as UserModel


async def test_create_user(
    http_client: AsyncClient,
    crud_user_url: str,
    user_create: UserCreate,
    created_access_token: str,
    session: AsyncSession,
) -> None:
    user_create.email = "new_email@gmail.com"
    user_create.username = "new_username"
    user_create.password = "new_password"

    response = await http_client.post(
        crud_user_url,
        json=user_create.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED

    query = select(UserModel).where(UserModel.email == user_create.email)
    result = await session.execute(query)
    user = result.scalars().first()

    assert user.email == user_create.email


async def test_get_users(
    http_client: AsyncClient,
    crud_user_url: str,
    created_users: list[User],
    created_access_token: str,
) -> None:
    response = await http_client.get(
        crud_user_url + "?limit=1&offset=1",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    users = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(users) == 1

    response = await http_client.get(
        crud_user_url + "?limit=11&offset=0",
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    users = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(users) == 11


async def test_update_me(
    http_client: AsyncClient,
    crud_user_url_me: str,
    created_access_token: str,
    user_update: UserUpdate,
    session: AsyncSession,
) -> None:

    response = await http_client.put(
        crud_user_url_me,
        json=user_update.model_dump(),
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    query = select(UserModel).where(UserModel.id == 1)
    result = await session.execute(query)
    user = result.scalars().first()
    assert user.username == user_update.username
    assert user.email == user_update.email


async def test_delete_me(
    http_client: AsyncClient,
    crud_user_url_me: str,
    created_access_token: str,
    session: AsyncSession,
) -> None:

    response = await http_client.delete(
        crud_user_url_me,
        headers={"Authorization": f"Bearer {created_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    query = select(UserModel).where(UserModel.id == 1)
    result = await session.execute(query)
    user = result.scalars().first()
    assert not user

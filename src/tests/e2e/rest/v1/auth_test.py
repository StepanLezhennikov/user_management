from httpx import AsyncClient
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleCreate
from app.schemas.user import User, UserCreate, UserSignIn
from app.schemas.permission import PermissionCreate
from app.services.services.jwt import JwtService
from app.infra.repositories.models.user_model import User as UserModel


async def test_sign_up(
    http_client: AsyncClient,
    user_create: UserCreate,
    sign_up_url: str,
    session: AsyncSession,
    created_role_admin: RoleCreate,
) -> None:
    response = await http_client.post(
        sign_up_url,
        json=user_create.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED

    query = select(UserModel).where(UserModel.email == user_create.email)
    result = await session.execute(query)
    user = result.scalars().first()

    assert user.email == user_create.email
    assert user.roles[0].role == created_role_admin.role
    assert user.username == user_create.username


async def test_sign_up_already_registered(
    http_client: AsyncClient,
    created_user: User,
    created_role_admin: RoleCreate,
    user_create: UserCreate,
    sign_up_url: str,
    session: AsyncSession,
) -> None:
    response = await http_client.post(
        sign_up_url,
        json=user_create.model_dump(),
    )

    assert response.status_code == status.HTTP_409_CONFLICT


async def test_get_tokens(
    http_client: AsyncClient,
    user_sign_in: UserSignIn,
    created_user: User,
    get_tokens_url: str,
    jwt_service: JwtService,
    permission_create_list: list[PermissionCreate],
) -> None:
    tokens = await http_client.post(get_tokens_url, json=user_sign_in.model_dump())

    assert tokens.status_code == status.HTTP_200_OK
    access_token = tokens.json().get("access_token")
    decoded_token = jwt_service.decode_token(access_token)
    assert decoded_token.get("id") == created_user.id

    assert len(decoded_token.get("permissions")) == len(permission_create_list)
    assert set(decoded_token.get("permissions")) == set(
        [perm.name for perm in permission_create_list]
    )


async def test_get_tokens_user_not_found(
    http_client: AsyncClient,
    get_tokens_url: str,
    user_sign_in: UserSignIn,
    jwt_service: JwtService,
) -> None:
    user_sign_in.email = "wrong_email@example.com"
    response = await http_client.post(
        get_tokens_url,
        json=user_sign_in.model_dump(),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_refresh_access_token(
    http_client: AsyncClient,
    refresh_access_token_url: str,
    refresh_token: str,
    jwt_service: JwtService,
):
    response = await http_client.post(
        refresh_access_token_url,
        params={"refresh_token": refresh_token},
    )
    assert response.status_code == status.HTTP_200_OK

from httpx import AsyncClient
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleCreate
from app.schemas.user import User, UserCreate, UserSignIn
from app.services.services.jwt import JwtService
from app.services.services.password_security import PasswordSecurityService
from app.infra.repositories.models.user_model import User as UserModel


async def test_sign_up(
    http_client: AsyncClient,
    user_create: UserCreate,
    sign_up_url: str,
    session: AsyncSession,
    created_role: RoleCreate,
) -> None:
    response = await http_client.post(
        sign_up_url,
        json=user_create.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED

    query = select(UserModel).where(UserModel.email == user_create.email)
    result = await session.execute(query)
    assert result.scalar_one_or_none() is not None


async def test_sign_up_already_registered(
    http_client: AsyncClient,
    created_user: User,
    created_role: RoleCreate,
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
    user_data: UserSignIn,
    created_user: User,
    get_tokens_url: str,
    jwt_service: JwtService,
    password_security_service: PasswordSecurityService,
) -> None:
    tokens = await http_client.post(
        get_tokens_url,
        json=user_data.model_dump(),
    )
    assert tokens.status_code == status.HTTP_200_OK
    access_token = tokens.json().get("access_token")
    decoded_token = jwt_service.decode_token(access_token)
    assert decoded_token.get("email") == user_data.email
    assert decoded_token.get("password") == user_data.password


async def test_get_tokens_incorrect_password(
    http_client: AsyncClient,
    user_data_incorrect_password: UserSignIn,
    created_user: User,
    get_tokens_url: str,
    jwt_service: JwtService,
    password_security_service: PasswordSecurityService,
) -> None:
    tokens = await http_client.post(
        get_tokens_url,
        json=user_data_incorrect_password.model_dump(),
    )
    assert tokens.status_code == status.HTTP_404_NOT_FOUND


async def test_get_tokens_user_not_found(
    http_client: AsyncClient,
    user_data: UserSignIn,
    created_user: User,
    get_tokens_url: str,
    jwt_service: JwtService,
    password_security_service: PasswordSecurityService,
) -> None:
    user_data.email = "invalid@email.com"
    tokens = await http_client.post(
        get_tokens_url,
        json=user_data.model_dump(),
    )
    assert tokens.status_code == status.HTTP_404_NOT_FOUND


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

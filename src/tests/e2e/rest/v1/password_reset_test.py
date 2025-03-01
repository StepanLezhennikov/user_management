from httpx import AsyncClient
from pydantic import EmailStr
from starlette import status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate, UserSignIn
from app.services.services.password_security import PasswordSecurityService
from app.infra.repositories.models.user_model import User as UserModel
from app.infra.repositories.models.user_model import user_role


async def test_request_password_reset(
    http_client: AsyncClient,
    request_password_reset_url: str,
    email: EmailStr,
    created_user: User,
) -> None:
    response = await http_client.post(
        request_password_reset_url,
        params={"email": email},
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_request_password_reset_user_not_found(
    http_client: AsyncClient,
    request_password_reset_url: str,
    email: EmailStr,
) -> None:
    response = await http_client.post(
        request_password_reset_url,
        params={"email": email},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_password_reset_url(
    http_client: AsyncClient,
    password_reset_url: str,
    reset_token: str,
    new_password: str,
    created_user: User,
    password_security_service: PasswordSecurityService,
) -> None:
    response = await http_client.post(
        password_reset_url,
        params={"token": reset_token, "new_password": new_password},
    )
    assert response.status_code == status.HTTP_200_OK

    assert not await password_security_service.verify_password(
        UserSignIn(email=created_user.email, password=new_password)
    )


async def test_password_reset_url_expired_signature(
    http_client: AsyncClient,
    password_reset_url: str,
    reset_token_expired: str,
    new_password: str,
) -> None:
    response = await http_client.post(
        password_reset_url,
        params={"token": reset_token_expired, "new_password": new_password},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.text == '{"detail":"Expired refresh token"}'


async def test_password_reset_url_invalid_signature(
    http_client: AsyncClient,
    password_reset_url: str,
    reset_token_invalid: str,
    new_password: str,
) -> None:
    response = await http_client.post(
        password_reset_url,
        params={"token": reset_token_invalid, "new_password": new_password},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.text == '{"detail":"Invalid refresh token"}'


async def test_password_reset_url_user_not_found(
    http_client: AsyncClient,
    password_reset_url: str,
    reset_token: str,
    new_password: str,
    user_create: UserCreate,
    password_security_service: PasswordSecurityService,
    session: AsyncSession,
) -> None:
    delete_relations = delete(user_role).where(user_role.c.user_id == 1)
    await session.execute(delete_relations)
    query = delete(UserModel).where(UserModel.email == user_create.email)

    await session.execute(query)

    await session.commit()

    response = await http_client.post(
        password_reset_url,
        params={"token": reset_token, "new_password": new_password},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

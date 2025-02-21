from httpx import AsyncClient
from pydantic import EmailStr
from starlette import status

from app.schemas.user import User
from app.schemas.code_verification import CodeVerification


async def test_send_code(
    http_client: AsyncClient,
    send_code_url: str,
    email: EmailStr,
    created_user: User,
) -> None:
    response = await http_client.post(
        send_code_url,
        params={"user_email": email},
    )
    assert response.status_code == status.HTTP_200_OK
    assert 999 < int(response.json().get("code")) < 10000


async def test_send_code_user_not_found(
    http_client: AsyncClient,
    send_code_url: str,
    email: EmailStr,
) -> None:
    response = await http_client.post(
        send_code_url,
        params={"user_email": email},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_verify_code(
    http_client: AsyncClient,
    verify_code_url: str,
    code_ver: CodeVerification,
    created_user: User,
) -> None:
    response = await http_client.post(
        verify_code_url,
        json=code_ver.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK


async def test_verify_expired_code(
    http_client: AsyncClient,
    verify_code_url: str,
    code_ver_expired: CodeVerification,
    created_user: User,
) -> None:
    response = await http_client.post(
        verify_code_url,
        json=code_ver_expired.model_dump(),
    )
    assert response.status_code == status.HTTP_410_GONE

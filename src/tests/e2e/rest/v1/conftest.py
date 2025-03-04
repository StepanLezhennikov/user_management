from typing import AsyncGenerator
from datetime import datetime, timezone

import jwt
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from pydantic import EmailStr

from app.main import app
from app.containers import Container
from app.core.config import Settings
from app.schemas.user import User, UserUpdate, UserForToken
from app.schemas.permission import PermissionFilter
from app.services.services.jwt import JwtService
from app.schemas.code_verification import CodeVerification


@pytest.fixture
def container() -> Container:
    return Container()


@pytest.fixture
def application(
    container: Container,
    settings: Settings,
) -> FastAPI:

    container.config = settings
    container.wire(
        modules=[__name__, "src.app.api.rest.v1.code_verification.controllers"]
    )
    container.wire(modules=[__name__, "src.app.api.rest.v1.auth.controllers"])
    container.wire(modules=[__name__, "src.app.api.rest.v1.password_reset.controllers"])
    app.container = container
    return app


@pytest.fixture
async def http_client(application: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def sign_up_url() -> str:
    return "/v1/auth/users"


@pytest.fixture
def get_tokens_url() -> str:
    return "/v1/auth/token"


@pytest.fixture
def refresh_access_token_url() -> str:
    return "/v1/auth/refresh"


@pytest.fixture
def send_code_url() -> str:
    return "/v1/code_verification/code_sending"


@pytest.fixture
def request_password_reset_url() -> str:
    return "/v1/password_reset/request"


@pytest.fixture
def password_reset_url() -> str:
    return "/v1/password_reset/"


@pytest.fixture
def verify_code_url() -> str:
    return "/v1/code_verification/verifying_code"


@pytest.fixture
def user_data() -> UserForToken:
    return UserForToken(email="test@example.com", password="test_password")


@pytest.fixture
def user_data_incorrect_password() -> UserForToken:
    return UserForToken(email="test@example.com", password="incorrect_password")


@pytest.fixture
def refresh_token(user_for_token: UserForToken, jwt_service: JwtService) -> str:
    return jwt_service.create_refresh_token(user_for_token.model_dump())


@pytest.fixture
def code_ver(created_code: int, email: EmailStr) -> CodeVerification:
    return CodeVerification(code=created_code, email=email)


@pytest.fixture
def code_ver_expired(code: int, email: EmailStr) -> CodeVerification:
    return CodeVerification(code=code, email=email)


@pytest.fixture
def reset_token(created_user: User, jwt_service: JwtService) -> str:
    return jwt_service.create_reset_token({"user_id": created_user.id})


@pytest.fixture
def new_password() -> str:
    return "new_password"


@pytest.fixture
def reset_token_expired(
    created_user: User, jwt_service: JwtService, settings: Settings
) -> str:
    data = {"user_id": created_user.id}
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.fixture
def reset_token_invalid(reset_token: str) -> str:
    return reset_token[:-5] + "abcde"


@pytest.fixture
def permission_filter() -> PermissionFilter:
    return PermissionFilter(name="test_permission", description="test_permission")


@pytest.fixture
def crud_permission_url() -> str:
    return "/v1/permissions/"


@pytest.fixture
def crud_role_url() -> str:
    return "/v1/roles/"


@pytest.fixture
def crud_user_url() -> str:
    return "/v1/users/"


@pytest.fixture
def crud_user_url_me() -> str:
    return "/v1/users/me/"


@pytest.fixture
def user_update() -> UserUpdate:
    return UserUpdate(
        email="new_email@example.com",
        first_name="new_first_name",
        last_name="new_last_name",
        username="new_username",
    )

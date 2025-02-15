import pytest
from pydantic import EmailStr

from app.services.exceptions.code_verification_repo import CodeIsExpired
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


def test_create(
    code_verification_repo: ACodeVerificationRepository,
    email: EmailStr,
    code: int,
) -> None:
    assert code_verification_repo.create(email, code)


def test_get_code(
    code_verification_repo: ACodeVerificationRepository,
    email: EmailStr,
    created_code: int,
) -> None:
    assert code_verification_repo.get_code(email) == created_code


def test_get_code_expired(
    code_verification_repo: ACodeVerificationRepository,
    email: EmailStr,
) -> None:
    with pytest.raises(CodeIsExpired):
        code_verification_repo.get_code(email)

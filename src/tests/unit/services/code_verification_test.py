import pytest
from fastapi import HTTPException
from pydantic import EmailStr

from app.api.interfaces.services.code_verification import ACodeVerificationService


async def test_verify_code(
    code_verification_service: ACodeVerificationService,
    email: EmailStr,
    created_code: int,
) -> None:
    assert code_verification_service.verify_code(email, created_code)


async def test_verify_code_invalid(
    code_verification_service: ACodeVerificationService, email: EmailStr, code: int
) -> None:
    with pytest.raises(HTTPException):
        assert code_verification_service.verify_code(email, code)


async def test_generate_code(
    code_verification_service: ACodeVerificationService,
) -> None:
    assert code_verification_service.generate_code()


async def test_create(
    code_verification_service: ACodeVerificationService, email: EmailStr, code: int
) -> None:
    assert code_verification_service.create(email, code)

from logging import getLogger

from fastapi import Depends, APIRouter
from pydantic import EmailStr
from dependency_injector.wiring import Provide, inject

from app.schemas.code_verification import Code, CodeVerification
from app.api.interfaces.services.email_service import AEmailService
from app.api.interfaces.services.code_verification_service import (
    ACodeVerificationService,
)

logger = getLogger(__name__)

router = APIRouter()


@router.post("/send_code")
@inject
async def send_code(
    user_email: EmailStr,
    email_service: AEmailService = Depends(Provide["email_service"]),
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> Code:
    code = code_verification_service.generate_code()
    await email_service.send_code(
        email=user_email,
        subject="Подтверждение почты",
        code=code,
    )
    code_verification_service.create(user_email, code)
    return Code(code=code)


@router.post("/verify_code")
@inject
async def verify_code(
    code_ver: CodeVerification,
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> bool:
    return code_verification_service.verify_code(code_ver.email, code_ver.code)

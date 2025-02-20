from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from pydantic import EmailStr
from dependency_injector.wiring import Provide, inject

from app.services.services.auth import AuthService
from app.services.services.email import EmailService
from app.schemas.code_verification import Code, CodeVerification
from app.api.exceptions.auth_service import UserNotFoundError
from app.services.services.code_verification import CodeVerificationService
from app.services.exceptions.code_verification_repo import CodeIsExpiredError

logger = getLogger(__name__)

router = APIRouter()


@router.post("/code_sending")
@inject
async def send_code(
    user_email: EmailStr,
    email_service: EmailService = Depends(Provide["email_service"]),
    code_verification_service: CodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
    auth_service: AuthService = Depends(Provide["auth_service"]),
) -> Code:
    try:
        await auth_service.check_user_exists(email=str(user_email))
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    code = code_verification_service.generate_code()
    await email_service.send_code(user_email, code)
    code_verification_service.create(user_email, code)
    return Code(code=code)


@router.post("/verifying_code")
@inject
async def verify_code(
    code_ver: CodeVerification,
    code_verification_service: CodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> bool:
    try:
        return code_verification_service.verify_code(code_ver.email, code_ver.code)
    except CodeIsExpiredError:
        raise HTTPException(status_code=410, detail="Code is expired")

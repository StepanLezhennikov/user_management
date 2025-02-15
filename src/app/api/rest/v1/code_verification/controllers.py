from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from pydantic import EmailStr
from dependency_injector.wiring import Provide, inject

from app.core.config import Constants
from app.schemas.code_verification import Code, CodeVerification
from app.api.interfaces.services.auth import AAuthService
from app.api.interfaces.services.email import AEmailService
from app.api.interfaces.services.code_verification import ACodeVerificationService
from app.services.exceptions.code_verification_repo import CodeIsExpired

logger = getLogger(__name__)

router = APIRouter()


@router.post("/code_sending")
@inject
async def send_code(
    user_email: EmailStr,
    email_service: AEmailService = Depends(Provide["email_service"]),
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
    auth_service: AAuthService = Depends(Provide["auth_service"]),
) -> Code:
    await auth_service.check_user_exists(user_email)
    code = code_verification_service.generate_code()
    await email_service.send_code(user_email, Constants.subject_for_email, code)
    code_verification_service.create(user_email, code)
    return Code(code=code)


@router.post("/verifying_code")
@inject
async def verify_code(
    code_ver: CodeVerification,
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> bool:
    try:
        return code_verification_service.verify_code(code_ver.email, code_ver.code)
    except CodeIsExpired:
        raise HTTPException(status_code=410, detail="Code is expired")

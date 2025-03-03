from logging import getLogger

from fastapi import Depends, APIRouter, HTTPException
from pydantic import EmailStr
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.response import CustomResponse
from app.schemas.code_verification import Code, CodeVerification
from app.api.exceptions.user_service import UserNotFoundError
from app.api.interfaces.services.user import AUserService
from app.api.interfaces.services.email import AEmailService
from app.api.interfaces.services.code_verification import ACodeVerificationService
from app.services.exceptions.code_verification_repo import CodeIsExpiredError

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
    user_service: AUserService = Depends(Provide["user_service"]),
) -> Code:
    try:
        await user_service.check_user_exists(email=str(user_email))
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    code = code_verification_service.generate_code()
    await email_service.send_code(user_email, code)
    code_verification_service.create(user_email, code)
    return Code(code=code)


@router.post("/verifying_code")
@inject
async def verify_code(
    code_ver: CodeVerification,
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> CustomResponse:
    try:
        code_verification_service.verify_code(code_ver.email, code_ver.code)
        return CustomResponse(message="Code is valid")
    except CodeIsExpiredError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Code is expired")

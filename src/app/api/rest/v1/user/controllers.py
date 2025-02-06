from logging import getLogger

from fastapi import Depends, APIRouter
from pydantic import EmailStr
from dependency_injector.wiring import Provide, inject

from app.schemas.code_verification import Code, CodeVerification
from app.api.interfaces.use_cases.send_code import ASendCodeUseCase
from app.api.interfaces.services.code_verification import ACodeVerificationService

logger = getLogger(__name__)

router = APIRouter()


@router.post("/code_sending")
@inject
async def send_code(
    user_email: EmailStr,
    send_code_use_case: ASendCodeUseCase = Depends(Provide["send_code_use_case"]),
) -> Code:
    return await send_code_use_case.send_code(user_email)

    # # TODO: проверка что пользователь не зарегистрирован
    # code = code_verification_service.generate_code()
    # await email_service.send_code(
    #     email=user_email,
    #     subject=Constants.subject_for_email,
    #     code=code,
    # )
    # code_verification_service.create(user_email, code)
    # return Code(code=code)


@router.post("/code_verification")
@inject
async def verify_code(
    code_ver: CodeVerification,
    code_verification_service: ACodeVerificationService = Depends(
        Provide["code_verification_service"]
    ),
) -> bool:
    return code_verification_service.verify_code(code_ver.email, code_ver.code)

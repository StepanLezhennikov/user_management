from fastapi import Depends
from pydantic import EmailStr
from dependency_injector.wiring import Provide, inject

from app.core.config import Constants
from app.schemas.code_verification import Code
from app.api.interfaces.services.email import AEmailService
from app.api.interfaces.use_cases.send_code import ASendCodeUseCase
from app.api.interfaces.services.code_verification import ACodeVerificationService


class SendCodeUseCase(ASendCodeUseCase):
    @inject
    def __init__(
        self,
        email_service: AEmailService = Depends(Provide["email_service"]),
        code_verification_service: ACodeVerificationService = Depends(
            Provide["code_verification_service"]
        ),
    ):
        self.email_service = email_service
        self.code_verification_service = code_verification_service

    async def send_code(self, user_email: EmailStr) -> Code:
        code = self.code_verification_service.generate_code()
        await self.email_service.send_code(
            user_email, Constants.subject_for_email, code
        )
        self.code_verification_service.create(user_email, code)
        return Code(code=code)

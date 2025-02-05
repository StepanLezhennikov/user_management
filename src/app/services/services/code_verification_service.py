import random

from pydantic import EmailStr

from app.api.interfaces.services.code_verification_service import (
    ACodeVerificationService,
)
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


class CodeVerificationService(ACodeVerificationService):
    def __init__(self, code_ver_repo: ACodeVerificationRepository):
        self._code_ver_repo = code_ver_repo

    def verify_code(self, email: EmailStr, code: int) -> bool:
        cd = self._code_ver_repo.get_code(email)
        return cd == code

    def create(self, email: EmailStr, code: int) -> bool:
        return self._code_ver_repo.create(email, code)

    def generate_code(self) -> int:
        return random.randint(1000, 9999)

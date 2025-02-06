from abc import ABC, abstractmethod

from pydantic import EmailStr

from app.schemas.code_verification import Code


class ASendCodeUseCase(ABC):
    @abstractmethod
    async def send_code(self, user_email: EmailStr) -> Code: ...

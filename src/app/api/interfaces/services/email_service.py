from abc import ABC, abstractmethod

from pydantic import EmailStr


class AEmailService(ABC):
    @abstractmethod
    async def send_code(self, email: EmailStr, subject: str, code: int) -> bool: ...

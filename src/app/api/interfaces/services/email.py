from abc import ABC, abstractmethod

from pydantic import EmailStr


class AEmailService(ABC):
    @abstractmethod
    async def send_code(self, email: EmailStr, code: int) -> bool: ...

    async def send_password_reset_link(self, email: EmailStr, token: str) -> bool: ...

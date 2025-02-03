from abc import ABC, abstractmethod

from pydantic import EmailStr


class AEmailService(ABC):
    @abstractmethod
    async def send_message(self, email: EmailStr, subject: str, message: str) -> bool:
        raise NotImplementedError()

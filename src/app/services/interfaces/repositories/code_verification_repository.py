from abc import ABC, abstractmethod

from pydantic import EmailStr


class ACodeVerificationRepository(ABC):
    @abstractmethod
    def get_code(self, email: EmailStr) -> int:
        pass

    @abstractmethod
    def create(self, email: EmailStr, code: int) -> bool:
        pass

from abc import ABC, abstractmethod

from pydantic import EmailStr


class ACodeVerificationService(ABC):
    @abstractmethod
    def verify_code(self, email: EmailStr, code: int) -> bool: ...

    @abstractmethod
    def create(self, email: EmailStr, code: int) -> bool: ...

    @abstractmethod
    def generate_code(self) -> int: ...

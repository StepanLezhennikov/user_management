from abc import ABC, abstractmethod

from app.schemas.user import User


class AJwtService(ABC):
    @abstractmethod
    def create_access_token(self, data: dict) -> str: ...

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str: ...

    @abstractmethod
    def create_reset_token(self, data: dict) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...

    @abstractmethod
    async def get_current_user(self, token: str) -> User: ...

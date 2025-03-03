from abc import ABC, abstractmethod


class AJwtService(ABC):
    @abstractmethod
    def create_access_token(self, data: dict) -> str: ...

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str: ...

    @abstractmethod
    def create_reset_token(self, data: dict) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...

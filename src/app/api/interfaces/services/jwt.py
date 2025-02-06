from abc import ABC, abstractmethod


class AJwtService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int) -> str:
        raise NotImplementedError()

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        raise NotImplementedError()

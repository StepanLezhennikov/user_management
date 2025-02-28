from abc import ABC, abstractmethod

from app.schemas.user import UserForToken


class APasswordSecurityService(ABC):
    @abstractmethod
    async def verify_password(self, user_data: UserForToken) -> bool:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

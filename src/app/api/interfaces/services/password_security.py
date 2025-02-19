from abc import ABC, abstractmethod

from app.schemas.user import UserSignIn


class APasswordSecurityService(ABC):
    @abstractmethod
    async def verify_password(self, user_data: UserSignIn) -> bool:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

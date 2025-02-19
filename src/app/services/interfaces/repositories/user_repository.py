from abc import ABC, abstractmethod

from app.schemas.user import User, UserCreate


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserCreate) -> UserCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> User:
        pass

    @abstractmethod
    async def update_password(self, user_id: int, new_password: str) -> str:
        pass
